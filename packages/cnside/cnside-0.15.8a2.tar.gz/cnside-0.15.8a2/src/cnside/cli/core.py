import logging
import subprocess
from typing import List, Text, Tuple

import colorama

from cnside.cli.documents import CLIParsedCommand


class PrintColors(object):
    def __init__(self, level: int = None):
        colorama.init()
        self._header = colorama.Fore.LIGHTMAGENTA_EX
        self._blue = colorama.Fore.BLUE
        self._success = colorama.Fore.GREEN
        self._yellow = colorama.Fore.LIGHTYELLOW_EX
        self._warning = colorama.Fore.LIGHTYELLOW_EX
        self._fail = colorama.Fore.RED
        self._end = colorama.Style.RESET_ALL
        self._bold = colorama.Style.BRIGHT

        self._level = logging.INFO if not level else level

    def header(self, text):
        print(u"\n{}{}[H] {}{}".format(self._bold, self._header, text, self._end))

    def header_point(self, text):
        print(u"{}[-]{} {}".format(self._header, self._end, text))

    def footer(self, text):
        print(u"\n{}{}[F] {}{}\n".format(self._bold, self._header, text, self._end))

    def point(self, text):
        print(u"[-] {}".format(text))

    def point_ok(self, text):
        print(u"{}[V] {}{}".format(self._success, text, self._end))

    def point_warning(self, text):
        print(u"{}[X] {}{}".format(self._warning, text, self._end))

    def point_warning_prefix(self, text):
        self.point_warning("WARNING: " + text)

    def point_fail(self, text):
        print(u"{}[X] {}{}".format(self._fail, text, self._end))

    def out_data(self, text):
        print(u"[D] {}".format(text), end="")

    def err_data(self, text):
        print(u"[ED] {}".format(text), end="")

    def point_fail_prefix(self, text):
        self.point_fail("ERROR: " + text)

    def custom(self, text):
        print(text)

    def empty_line(self):
        print("")

    def debug(self, text):
        if self._level == logging.DEBUG:
            print(u"[DEBUG] {}".format(text))


def execute_subprocess_popen_command(command: List[Text], **kwargs) -> Tuple[List[Text], List[Text]]:
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, **kwargs)

    std_out = []
    std_err = []

    for line in iter(process.stdout.readline, b''):
        std_out.append(line.decode("utf-8"))

    for line in iter(process.stderr.readline, b''):
        std_err.append(line.decode("utf-8"))

    process.stdout.close()
    process.stderr.close()
    process.wait()

    return std_out, std_err


def execute_cli_parsed_command(command: CLIParsedCommand):
    std_out, std_err = execute_subprocess_popen_command(command.subprocess_popen_list_command())
    return std_out, std_err
