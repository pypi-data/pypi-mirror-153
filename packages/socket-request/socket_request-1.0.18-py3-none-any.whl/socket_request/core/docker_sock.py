from .connect_sock import ConnectSock


class DockerSock(ConnectSock):
    def __init__(self, unix_socket="/var/run/docker.sock", url="/", timeout=5, debug=False, auto_prepare=False, wait_state=False):
        super().__init__(unix_socket=unix_socket, timeout=timeout, debug=debug)
        self.url = url
        self.unix_socket = unix_socket
        # self.action_model = ChainActionModel()
        self.headers = {
            "Host": "*",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "socket-request"
        }
        self.payload = {}
        self.files = {}
        self.detail = False
        self.debug = debug
        self.simple_name = True
        self.auto_prepare = auto_prepare
        self.wait_state = wait_state

    def get_docker_images(self, return_type="each", simple_name=True):
        self.request(url="/containers/json")
        self.simple_name = simple_name
        return_values = []
        if self.Response.json:
            for image in self.Response.json:
                return_values.append(dict(
                    # names=image.get("Names")[0][1:],
                    images=image.get("Image"),
                    state=image.get("State"),
                    status=image.get("Status")
                ))

        if return_type == "merge" and len(return_values) > 0:
            self.return_merged_values = {key: "" for key in return_values[0].keys()}
            for values in return_values:
                for r_key, r_val in values.items():
                    self._merge_value(r_key, self.get_simple_image_name(r_val))
            return self.return_merged_values

        return return_values

    def get_simple_image_name(self, name):
        if self.simple_name:
            if "/" in name:
                name_arr = name.split("/")
                return name_arr[-1]
        return name

    def _merge_value(self, key, value, separator="|"):
        # jmon_lib.cprint(self.return_merged_values.get(key))
        prev_value = self.return_merged_values.get(key)
        if prev_value:
            self.return_merged_values[key] = f"{prev_value}{separator}{value}"
        else:
            self.return_merged_values[key] = f"{value}"
