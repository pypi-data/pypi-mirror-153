from datetime import datetime
import os
import json
import binascii
import codecs
import sys
import re
from halo import Halo
from devtools import debug
import time
from ..utils.data import ResponseField, RequestField


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'


def get_bcolors(text, color, bold=False, width=None):
    if width and len(text) <= width:
        text = text.center(width, ' ')
    return_text = f"{getattr(bcolors, color)}{text}{bcolors.ENDC}"
    if bold:
        return_text = f"{bcolors.BOLD}{return_text}"
    return str(return_text)


def classdump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            print(bcolors.GREEN + f"obj.{attr} = " + bcolors.WARNING + f"{value}" + bcolors.ENDC)


def color_print(text, color="GREEN", date=True, **kwargs):
    date_string = ""
    if date:
        date_string = todaydate("ms")
    if isinstance(text, dict) or isinstance(text, list):
        text = str(text)

    print(f"{get_bcolors(date_string + ' ' + text, color.upper())}", **kwargs)


def red(text):
    return get_bcolors(f"{text}", "FAIL")


def todaydate(type=None):
    if type is None:
        return '%s' % datetime.now().strftime("%Y%m%d")
    elif type == "ms":
        return '[%s]' % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    elif type == "ms_text":
        return '%s' % datetime.now().strftime("%Y%m%d-%H%M%S%f")[:-3]


def append_new_line(data, check_string="\r\n"):
    if data.endswith(check_string) is False:
        return f"{data}{check_string}"


def b(s):
    return s.encode("latin-1")


def _append_new_line(data, check_string="\r\n"):
    if data.endswith(check_string) is False:
        return f"{data}{check_string}"


def choose_boundary():
    return binascii.hexlify(os.urandom(16)).decode("ascii")


def _replace_multiple(value, needles_and_replacements):
    def replacer(match):
        return needles_and_replacements[match.group(0)]

    pattern = re.compile(
        r"|".join([re.escape(needle) for needle in needles_and_replacements.keys()])
    )

    result = pattern.sub(replacer, value)

    return result


def wait_state_loop(
        exec_function=None,
        func_args=[],
        check_key="status",
        wait_state="0x1",
        timeout_limit=30,
        increase_sec=0.5,
        health_status=None,
        description="",
        force_dict=True,
        logger=None
):
    start_time = time.time()
    count = 0
    # arguments 가 한개만 있을 때의 예외
    # if type(func_args) is str:
    if isinstance(func_args, str):
        tmp_args = ()
        tmp_args = tmp_args + (func_args,)
        func_args = tmp_args

    exec_function_name = exec_function.__name__
    # classdump(exec_function.__qualname__)
    # print(exec_function.__qualname__)
    act_desc = f"desc={description}, function={exec_function_name}, args={func_args}"
    spinner = Halo(text=f"[START] Wait for {description} , {exec_function_name}, {func_args}", spinner='dots')
    if logger and hasattr(logger, "info"):
        logger.info(f"[SR] [START] {act_desc}")

    spinner.start()

    while True:
        if isinstance(func_args, dict):
            response = exec_function(**func_args)
        else:
            response = exec_function(*func_args)

        if not isinstance(response, dict):
            response = response.__dict__

        if force_dict:
            if isinstance(response.get("json"), list):
                response['json'] = response['json'][0]

        check_state = ""
        error_msg = ""

        if response.get("json") or health_status:
            response_result = response.get("json")
            check_state = response_result.get(check_key, "")
            response_status = response.get("status_code")
            if check_state == wait_state or health_status == response_status:
                status_header = bcolors.OKGREEN + "[DONE]" + bcolors.ENDC
                text = f"\t[{description}] count={count}, func={exec_function_name}, args={str(func_args)[:30]}, wait_state='{wait_state}', check_state='{check_state}'"
                if health_status:
                    text += f", health_status={health_status}, status={response_status}"
                spinner.succeed(f'{status_header} {text}')
                spinner.stop()
                spinner.clear()
                # spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text="[DONE]")
                break
            else:
                if type(response_result) == dict or type(check_state) == dict:
                    if response_result.get("failure"):
                        if response_result.get("failure").get("message"):
                            print("\n\n\n")
                            spinner.fail(f'[FAIL] {response_result.get("failure").get("message")}')
                            spinner.stop()
                            spinner.clear()
                            break

        text = f"[{count:.1f}s] Waiting for {exec_function_name} / {func_args} :: '{wait_state}' -> '{check_state}' , {error_msg}"
        spinner.start(text=text)

        if logger and hasattr(logger, "info"):
            logger.info(f"[SR] {text}")

        try:
            assert time.time() < start_time + timeout_limit
        except AssertionError:
            text = f"[{count:.1f}s] [{timeout_limit}s Timeout] Waiting for {exec_function_name} / '{func_args}' :: '{wait_state}' -> {check_state} , {error_msg}"
            spinner.start(text=text)

            if logger and hasattr(logger, "error"):
                logger.info(f"[SR] {text}")

        count = count + increase_sec
        time.sleep(increase_sec)

        spinner.stop()

    if logger and hasattr(logger, "info"):
        logger.info(f"[SR] [DONE] {act_desc}")

    if health_status:
        return response

    # return {
    #     "elapsed": time.time() - start_time,
    #     "json": response.get("json"),
    #     "status_code": response.get("status_code", 0),
    # }


def get_function_parameters(func=None):
    if func:
        keys = func.__code__.co_varnames[:func.__code__.co_argcount][::-1]
        sorter = {j: i for i, j in enumerate(keys[::-1])}
        if func.__defaults__ is None:
            func.__defaults__ = ()
        values = func.__defaults__[::-1]
        kwargs = {i: j for i, j in zip(keys, values)}
        sorted_args = tuple(
            sorted([i for i in keys if i not in kwargs], key=sorter.get)
        )
        sorted_kwargs = {
            i: kwargs[i] for i in sorted(kwargs.keys(), key=sorter.get)
        }
        return {
            "args": sorted_args,
            "kwargs": sorted_kwargs
        }
    else:
        return {}


def payload_bool2string(payload=None):
    """
    In goloop, boolean values ​​must be string.
    :param payload:
    :return:
    """
    if payload and isinstance(payload, dict):
        for k, v in payload.items():
            payload[k] = bool2str(v)
    return payload


def bool2str(v):
    if type(v) == bool:
        if v:
            return "true"
        elif v:
            return "false"

        else:
            return "false"
    else:
        return v


def str2bool(v):
    if v is None:
        return False
    elif type(v) == bool:
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return False


class Table:
    def __init__(self, title, headers, rows, view_header=True):
        title = bcolors.WARNING + title + bcolors.ENDC
        self.title = title
        self.headers = headers
        self.rows = rows
        self.view_header = view_header
        self.nrows = len(self.rows)
        self.fieldlen = []

        self.warn_string = ["stopped", "unused"]
        self.ok_string = ["running"]

        ncols = len(headers)

        for i in range(ncols):
            max = 0
            for j in rows:
                if len(str(j[i])) > max:
                    max = len(str(j[i]))
            self.fieldlen.append(max)

        for i in range(len(headers)):
            if len(str(headers[i])) > self.fieldlen[i]:
                self.fieldlen[i] = len(str(headers[i]))

        self.width = sum(self.fieldlen) + (ncols - 1) * 3 + 4

    def __str__(self):
        bar = "-" * self.width
        # title = "| "+self.title+" "*(self.width-3-(len(self.title)))+"|"
        title = "| " + self.title + " " * (self.width + 6 - (len(self.title))) + "|"
        out = [bar, title, bar]
        header = ""
        for i in range(len(self.headers)):
            header += "| %s" % (str(self.headers[i])) + " " * \
                      (self.fieldlen[i] - len(str(self.headers[i]))) + " "
        header += "|"

        if self.view_header:
            out.append(header)
            out.append(bar)
        for i in self.rows:
            line = ""
            for j in range(len(i)):
                column = str(i[j])
                # for item in self.warn_string:
                #     if (line.find(item)) != -1:
                # column = bcolors.FAIL + column + bcolors.ENDC

                # for item in self.warn_string:
                #     if (item.find(item)) != -1:
                #         column = bcolors.FAIL + column + bcolors.ENDC
                #         is_warn_string = 1

                # for item in self.ok_string:
                #     if (line.find(item)) != -1:
                #         is_ok_string = 1

                # if intersection(i, self.warn_string):
                #     column = bcolors.FAIL + column + bcolors.ENDC
                # if intersection(i, self.ok_string):
                #     column = bcolors.OKGREEN + column + bcolors.ENDC

                line += "| %s" % (column) + " " * \
                        (self.fieldlen[j] - len(column)) + " "

            for item in self.warn_string:
                if (line.find(item)) != -1:
                    line = bcolors.FAIL + line + bcolors.ENDC
            for item in self.ok_string:
                if (line.find(item)) != -1:
                    line = bcolors.OKGREEN + line + bcolors.ENDC

            out.append(line + "|")
        out.append(bar)
        return "\r\n".join(out)


def minimize_names(object_dict):
    replace_dest = {
        "consensus_height": "bh",
        "duration": "d",
        "network": "net",
        "txlatency_commit": "tx_com",
        "txlatency_finalize": "tx_fin",
        "txpool": "tx",
        "user": "usr",
        "consensus_round": "c_rnd"
    }
    new_dict = {}
    if isinstance(object_dict, dict):
        for key, value in object_dict.items():
            new_key = key
            for k2, v2 in replace_dest.items():
                if k2 in key:
                    new_key = new_key.replace(k2, v2)
            new_dict[new_key] = value
            print(new_key, value)
        return new_dict
    else:
        return object_dict


def print_table(title, source_dict=None, view_header=True, vertical=False):
    rows = []
    columns = []
    source_input = []
    source_dict = minimize_names(source_dict)

    if isinstance(source_dict, dict):
        source_input = source_dict.keys()
        columns = list(source_input)
        is_dict = 1

    elif isinstance(source_dict, list) and len(source_dict) > 0:
        source_input = source_dict
        columns = list(source_dict[0].keys())
        is_dict = 0

    index = 0
    for item in source_input:
        if is_dict:
            columns_list = [source_dict.get(col, None) for col in columns]
        else:
            columns_list = [item.get(col, None) for col in columns]
        # print(columns_list)
        index += 1
        columns_list.insert(0, index)
        rows.append(columns_list)
        if is_dict:
            break

    columns.insert(0, "idx")
    print(Table(title, columns, rows, view_header))


def is_hex(s):
    try:
        int(s, 16)
        return True
    except:
        return False


def dump(obj, nested_level=0, output=sys.stdout, hex_to_int=False):
    spacing = '   '
    def_spacing = '   '
    if type(obj) == dict:
        print('%s{' % (def_spacing + (nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output, hex_to_int)
            else:
                # print >>  bcolors.OKGREEN + '%s%s: %s' % ( (nested_level + 1) * spacing, k, v) + bcolors.ENDC
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC,
                      file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing + (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output, hex_to_int)
            else:
                print(bcolors.WARNING + '%s%s' % (def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % (def_spacing + (nested_level) * spacing), file=output)
    else:
        if hex_to_int and is_hex(obj):
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, str(round(int(obj, 16) / 10 ** 18, 8)) + bcolors.ENDC))
        else:
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, obj) + bcolors.ENDC)


def iteritems(d, **kw):
    return iter(d.items(**kw))


def iter_field_objects(fields):
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    if isinstance(fields, dict):
        i = iteritems(fields)
    else:
        i = iter(fields)

    for field in i:
        if isinstance(field, RequestField):
            yield field
        else:
            yield RequestField.from_tuples(*field)
