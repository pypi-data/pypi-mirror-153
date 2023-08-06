from functools import partial, wraps
from .connect_sock import ConnectSock

try:
    from ..__version__ import __version__
except:
    from __version__ import __version__

from ..utils.data import ResponseField, RequestField
from ..utils.utils import *


class ControlChain(ConnectSock):
    success_state = {
        "backup": "backup done",
        "prune": "pruning done",
        "restore": "success",
        "start": "started",
        "stop": "stopped",
        "import_stop": "import_icon finished"
    }

    def __init__(
            self,
            unix_socket="/app/goloop/data/cli.sock",
            url="/", cid=None, timeout=10,
            debug=False, auto_prepare=True, wait_state=True,
            increase_sec=0.5,
            wait_socket=False,
            logger=None,
            check_args=True,
            retry=3
    ):
        """
        ChainControl class init

        :param unix_socket: Path of file based unix domain socket
        :param url: reuqest url
        :param cid: channel id for goloop
        :param timeout: Maximum time in seconds that you allow the connection to the server to take
        :param debug: debug mode
        :param auto_prepare: Prepare before execution. e.g., Backup should be done after stopping.
        :param wait_state: Wait until the required state(success_state dict) is reached.
        """

        self.headers = {
            "Host": "*",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "socket-request"
        }

        super().__init__(unix_socket=unix_socket, timeout=timeout, debug=debug, headers=self.headers, wait_socket=wait_socket)
        self.url = url
        self.unix_socket = unix_socket
        self.cid = cid
        # self.action_model = ChainActionModel()

        self.payload = {}
        self.files = {}
        self.detail = False
        self.debug = debug
        self.auto_prepare = auto_prepare
        self.wait_state = wait_state
        self.state = {}
        self.gs_file = None
        self.increase_sec = increase_sec
        self.logger = logger
        self.check_args = check_args
        self.blockheight = None
        self.restore_name = None
        self.seedAddress = []
        self.retry = retry

        self.last_block = {}

        self.logging(f"Load ControlChain Version={__version__}")

        if self.cid is None and self._health_check():
            self.debug_print("cid not found. Guess it will get the cid.")
            self.cid = self.guess_cid()
            self.debug_print(f"guess_cid = {self.cid}")

    # def _get_args_dict(fn, args, kwargs):
    #     args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    #     return {**dict(zip(args_names, args)), **kwargs}

    def logging(self, message=None, level="info"):
        if self.logger:
            if level == "info" and hasattr(self.logger, "info"):
                self.logger.info(f"[SR] {message}")
            elif level == "error" and hasattr(self.logger, "error"):
                self.logger.error(f"[SR] {message}")

    def _decorator_stop_start(func):
        def stop_start(self, *args, **kwargs):
            func_name = func.__name__

            if func_name == "restore" and self.check_backup_file(restore_name=kwargs.get("restore_name")) is False:
                return

            if func_name == "prune" and isinstance(kwargs.get("blockheight"), int) is False:
                raise Exception(red(f"Required blockheight {kwargs.get('blockheight')}"))

            if self.auto_prepare:
                # self.stop(*args, **kwargs)
                self.stop()
                ret = func(self, *args, **kwargs)

                if func_name == "restore":
                    exec_function = self.get_restore_status
                else:
                    exec_function = self.view_chain
                if self.wait_state and self.success_state.get(func_name):
                    wait_state_loop(
                        exec_function=exec_function,
                        check_key="state",
                        wait_state=self.success_state.get(func_name),
                        increase_sec=self.increase_sec,
                        description=f"'{func_name}'",
                        logger=self.logger
                    )
                # self.start(*args, **kwargs)
                self.start()
            else:
                ret = func(self, **kwargs)
            return ret
        return stop_start

    def _decorator_wait_state(func):
        def wait_state(self, *args, **kwargs):
            func_name = func.__name__
            ret = func(self, *args, **kwargs)
            if self.wait_state and self.success_state.get(func_name):
                wait_state_loop(
                    exec_function=self.view_chain,
                    check_key="state",
                    wait_state=self.success_state.get(func_name),
                    increase_sec=self.increase_sec,
                    description=f"'{func_name}'",
                    logger=self.logger
                )
            return ret
        return wait_state

    def get_restore_status(self):
        return self.request(url="/system/restore",  method="GET", return_dict=True)

    def _decorator_kwargs_checker(check_mandatory=True):
        def real_deco(func):
            @wraps(func)
            def from_kwargs(self, *args, **kwargs):
                func_name = func.__name__
                if func_name != "stop_start":
                    self.debug_print(f"Start '{func_name}' function", "WHITE")
                    # color_print(f"['{func_name}'] Start function ", "WHITE")
                # defined default value for function

                if self.auto_prepare:
                    if func_name not in ["view_chain", "join"]:
                        self.view_chain()
                    if self.state.get("state") and self.success_state.get(func_name) == self.state.get("state"):
                        # print(red(f"Already {self.state.get('state')}"))
                        # return f"Already {self.state.get('state')}"
                        return ResponseField(status_code=202, text=f"Already {self.state.get('state')}")

                if check_mandatory is not True:
                    # if func_name == "restore":
                    #     self.check_backup_file("sdsd")
                    func_params = get_function_parameters(func)
                    # input parameters for function
                    func_params['kwargs'].update(**kwargs)
                    for key, value in func_params.get("kwargs").items():
                        if value is not None:
                            setattr(self, key, value)
                        default_param = getattr(self, key)

                        if (self.check_args and check_mandatory and True) \
                                and value is None \
                                and (default_param is None
                                     or default_param == {} or default_param == []):
                            raise Exception(red(f"Required '{key}' parameter for {func_name}()"))

                    self.debug_print(f"_decorator_kwargs_checker(), kwargs = {kwargs}")

                # if func_name == "restore":
                #     print(f"{func_name} " * 100)
                #     a = func(self, *args, **kwargs)
                #     ret = self._decorator_stop_start(a)
                # else:
                ret = func(self, *args, **kwargs)

                self.payload = {}
                self.files = []
                self.r_headers = []
                self.r_headers_string = ""
                self.r_body = []
                self.r_body_string = ""
                self.gs_file = ""
                return ret
            return from_kwargs
        # return real_deco
        return real_deco(check_mandatory) if callable(check_mandatory) else real_deco

    @_decorator_kwargs_checker(check_mandatory=False)
    def guess_cid(self):
        res = self.view_chain()
        if res.json and res.get_json("cid"):
            self.state = res.get_json()
            self.cid = res.get_json('cid')
            return self.cid

    @_decorator_kwargs_checker
    def _kwargs_test(self, cid=None):
        print(self.cid)

    def _is_cid(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid:
            return self.cid
        else:
            print("[ERROR] Required cid")
            return False

    # def get_state(self):
    #     if self._health_check():
    #         res = self.view_chain().get_json()
    #         if isinstance(res, list) and len(res) == 0:
    #             self.state = {}
    #         else:
    #             self.state = res
    #     else:
    #         self.state = {
    #             "error": self.connect_error
    #         }
    #     return self.state

    def get_state(self):
        # res = self.view_chain().get_json()
        result = self.view_chain()
        if result.status_code == 200:
            res = self.view_chain().get_json()
            if isinstance(res, list) and len(res) == 0:
                self.state = {}
            else:
                self.state = res
                if self.state.get("cid"):
                    self.cid = self.state["cid"]
        else:
            self.state['error'] = result.text
        return self.state

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def start(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        res = self.request(url=f"/chain/{self.cid}/start", payload={}, method="POST")
        return res

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def stop(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()
        res = self.request(url=f"/chain/{self.cid}/stop", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def import_finish(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        stop_res_1 = None
        stop_res_2 = None

        try:
            stop_res_1 = self.import_stop()
            time.sleep(3)
            stop_res_2 = self.stop()
            time.sleep(3)
            if stop_res_1.status_code == 200 and stop_res_2.status_code == 200:
                color_print("Congrats! Successfully imported")
                color_print(f"{self.get_state()}")
            else:
                color_print(f"[FAIL] stop_res_1={stop_res_1}, stop_res_2={stop_res_2}", "red")
        except Exception as e:
            color_print(f"{self.get_state()}, e={e}")
        return stop_res_2

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def import_stop(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        res = self.request(url=f"/chain/{self.cid}/stop", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def reset(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        self.stop(cid)
        res = self.request(url=f"/chain/{self.cid}/reset", payload={}, method="POST")
        return res

    def import_icon(self, payload=None):
        res = self.request(
            url=f"/chain/{self.cid}/import_icon",
            payload=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        self.guess_cid()
        return res

    @_decorator_kwargs_checker
    def join(self,
             seedAddress=[],
             role=3,
             maxBlockTxBytes=2048000,
             normalTxPool=10000,
             channel="icon_dex",
             autoStart=True,
             platform="icon",
             gs_file="config/icon_genesis.zip",
             dbType="rocksdb",
             txTimeout=60000,
             nodeCache="small"
             ):

        config_payload = dict(
            seedAddress=",".join(seedAddress),
            role=int(role),
            maxBlockTxBytes=int(maxBlockTxBytes),
            normalTxPool=int(normalTxPool),
            channel=channel,
            autoStart=autoStart,
            platform=platform,
            dbType=dbType,
            txTimeout=int(txTimeout),
            nodeCache=nodeCache
        )

        print(f"seedAddress => {seedAddress}")
        if not seedAddress:
            raise Exception(red(f"[ERROR] seedAddress is None"))

        if not os.path.exists(self.gs_file):
            raise Exception(red(f"[ERROR] Genesis file not found - '{gs_file}'"))

        with open(gs_file, "rb") as genesis_fd:
            fd_data = genesis_fd.read()

        files = {
            "json": (None, json.dumps(config_payload)),
            "genesisZip": (os.path.basename(gs_file), fd_data)
        }

        res = self.request(url=f"/chain", payload={}, method="POST", files=files)
        self.guess_cid()
        debug(res.status_code)
        return res
        # else:
        #     print(f"[ERROR] Required files")

    # @_decorator_kwargs_checker
    def leave(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        if self.cid is None:
            return ResponseField(status_code=400, text=f"Already leave, cid not found")

        res = self.request(url=f"/chain/{self.cid}", payload={}, method="delete")
        return res

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def backup(self, cid=None):
        res = self.request(url=f"/chain/{self.cid}/backup", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def backup_list(self, cid=None):
        res = self.request(url=f"/system/backup", payload={}, method="GET")
        return res

    def check_backup_file(self, restore_name):
        backup_list = self.backup_list()
        is_backup_file = False
        for backup_item in backup_list.json:
            if isinstance(backup_item, dict) and backup_item.get("name") == restore_name:
                is_backup_file = True

        if is_backup_file is False:
            raise Exception(red(f"[ERROR] Unable to restore file, backup file not found -> {restore_name}"))

        return is_backup_file


    @_decorator_kwargs_checker
    @_decorator_stop_start
    def restore(self, restore_name=None, cid=None):

        if restore_name:
            payload = {
                "name": restore_name,
                "overwrite": True
            }
            res = self.request(url=f"/system/restore", payload=payload, method="POST")
            return res
        else:
            print(f"[ERROR] restore_name not found")
            # sys.exit(127)

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def prune(self, blockheight=None):
        if blockheight and blockheight >= 0:
            payload = {
                # "dbType": "gorocksdb",
                "dbType": "goleveldb",
                "height": blockheight
            }
            res = self.request(url=f"/chain/{self.cid}/prune", payload=payload, method="POST")
            return res
        else:
            print(f"[ERROR] height is {blockheight}")
            sys.exit(127)

    # @_decorator_kwargs_checker
    def view_chain(self, cid=None, detail=False, inspect=False):
        payload = {}
        if cid:
            self.cid = cid

        if self.cid and inspect:
            url = f"/chain/{self.cid}"
            # payload = {"informal": "true"}
        elif self.cid and detail:
            url = f"/chain/{self.cid}/configure"
        else:
            url = f"/chain"
        res = self.request(url=url, payload=payload, method="GET", return_dict=True)

        if res.status_code != 200:
            self.logging(f"view_chain res.status_code={res.status_code}, res = {res.text}")
        if hasattr(res, 'json'):
            self.state = res.json
            try:
                self.get_tps()
                res.set_dict(self.state)
            except:
                pass
            # self.connect_error = res.get('error')
        else:
            self.state = {}
            self.connect_error = res.text
        return res

    def get_tps(self):
        if self.state.get("height"):
            if self.last_block.get('height') is None:
                self.last_block = {
                    "height": self.state.get("height"),
                    "time": time.time()
                }

            diff_block = self.state['height'] - self.last_block['height']
            diff_time = time.time() - self.last_block['time']
            tps = diff_block / diff_time
            # print(diff_block, diff_time, tps)
            self.state['tps'] = round(tps)
            self.last_block = {
                "height": self.state.get("height"),
                "time": time.time()
            }

    def multi_payload_request(self, url=None, payload=None, method="POST"):
        result = {
            "state": "OK",
            "payload": payload,
            "error": []
        }
        status_code = 201

        if not isinstance(payload, dict):
            raise Exception(red(f"[ERROR] Invalid payload '{payload}'"))

        if payload.get("key") and payload.get("value"):
            return self.request(url=f"/chain/{self.cid}/configure",  payload=payload, method="POST")

        for key, value in payload.items():
            if isinstance(value, bool):
                value = bool2str(value)
            elif isinstance(value, int):
                value = str(value)
            elif isinstance(value, float):
                value = str(value)

            debug(key, value) if self.debug else False
            each_payload = {"key": key, "value": value}
            res = self.request(url=url, payload=each_payload,  method=method)
            debug(res) if self.debug else False

            if res.status_code != 200:
                if len(res.text) > 1:
                    return_text = res.text.split("\n")[0]
                else:
                    return_text = res.text
                result['error'].append({
                    "key": key,
                    "value": value,
                    "message": return_text
                })
                result['state'] = "FAIL"
                status_code = 400
        return ResponseField(status_code=status_code, text=result)

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def chain_config(self, payload=None):
        return self.multi_payload_request(url=f"/chain/{self.cid}/configure", payload=payload, method="POST")

    # def view_system_config(self, detail=True, inspect=False):
    def view_system_config(self, detail=True):
        if detail:
            url = "/system"
        else:
            url = "/system/configure"
        res = self.request(url=url,  method="GET")
        return res

    @_decorator_kwargs_checker
    def system_config(self, payload=None):
        payload = payload_bool2string(payload)
        return self.multi_payload_request(url="/system/configure", payload=payload, method="POST")
