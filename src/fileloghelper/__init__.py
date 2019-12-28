import os
import datetime
import platform


class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    """A class for logging data to a file"""

    def __init__(self, filename="log.txt", context="", verbose=True):
        """
        Example for a log in file filename (verbose == False):

        [context] [12:34:56] Hello World!

        (verbose == True)

        [DEBUG] [context] [12:34:56] Hello World!
        """
        self.filename = filename
        self.lines = []
        self.set_context(context)
        self.verbose = self.set_verbose(verbose)

    def set_context(self, context):
        """specifies context which will be added to all outputs (file & terminal) in front"""
        if not "[" in context and not "] " in context:
            if (context == "" or context == " "):
                self._context = ""
            else:
                self._context = f"[{context}] "
        else:
            self._context = context

    def set_verbose(self, verbose):
        if type(verbose) == bool:
            self._verbose = verbose
        else:
            e = TypeError("verbose is of type bool")
            self.show_error(e)
            raise e

    def save(self):
        """save file under default/at declaration specified filename"""
        self.file = open(self.filename, "w")
        self.file.writelines(self.lines)
        self.file.close()

    def _timestamp_now_(self, extra_long=False):
        now = datetime.datetime.now()
        ex = "%H:%M:%S"
        if extra_long:
            ex += ":%f"
        string = "[" + now.strftime(ex) + "]"
        return string

    def _get_success_(self, text, display=True):
        if display:
            print(col.OKGREEN + self._context + self._timestamp_now_() +
                  col.ENDC + " " + text)
        string = self._context
        string += "[SUCCESS] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_debug_(self, text, display=False):
        if display:
            print(col.OKBLUE + self._context + self._timestamp_now_() +
                  col.ENDC + " " + text)
        string = self._context
        string += "[DEBUG] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_warning_(self, text, display=True, extra_context=""):
        if display:
            print(col.WARNING + self._context + self._timestamp_now_() +
                  col.ENDC + " " + extra_context + ": " + text)
        string = self._context
        string += "[" + extra_context + "] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_error_(self, text, display=True, extra_context=""):
        if display:
            print(col.FAIL + self._context + self._timestamp_now_() +
                  col.ENDC + " " + extra_context + ": " + text)
        string = self._context
        string += "[" + extra_context + "] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_plain_(self, text, display=True, extra_long=False):
        string = self._context + self._timestamp_now_(extra_long) + " " + text
        if display:
            print(string)
        return string

    def success(self, text, display=True):
        string = self._get_success_(str(text), display)
        string += "\n"
        self.lines.append(string)

    def debug(self, text, display=False):
        string = self._get_debug_(str(text), display)
        string += "\n"
        self.lines.append(string)

    def warning(self, text, display=True, extra_context=""):
        """writes text to file and optionally with yellow indication in console(if display == True)"""
        string = self._get_warning_(
            str(text), display, extra_context)
        string += "\n"
        self.lines.append(string)

    def error(self, text, display=True, extra_context=""):
        """writes text to file and optionally with red indication in console (if display==True)"""
        string = self._get_error_(
            str(text), display, extra_context)
        string += "\n"
        self.lines.append(string)

    def show_warning(self, warning, display=True):
        self.warning(str(warning), display,
                     extra_context=type(warning).__name__)

    def show_error(self, error, display=True):
        self.error(str(error), display,
                   extra_context=type(error).__name__)

    def handle_exception(self, exception):
        if issubclass(exception.__class__, Warning):
            self.show_warning(exception)
        else:
            self.show_error(exception)

    def plain(self, text, display=False, extra_long=False, very_plain=False):
        """write and optionally display text to file. extra_long specifies time format (12:34:56; 12:34:56:123456). If very_plain==True, no timestamp or somethings similar will be outputted"""
        if not very_plain:
            string = self._get_plain_(str(text), display, extra_long)
        else:
            string = text
            if display:
                print(string)
        string += "\n"
        self.lines.append(string)

    def header(self, sys_stat=False, date=False, description="", display=0):
        """
        Display options:

        0 (standard): nothing, only log

        1: only description

        2: only date

        3: only sys_stat

        4: description & date

        5: description & sys_stat

        6: date & sys_stat

        7: all
        """
        # yes, this is kinda awfull, but it does the job reliably
        now = datetime.datetime.now()

        systemstrin = f"{platform.system()} ({platform.machine()})\n{platform.version()}\n{platform.platform()}\n{platform.processor()}\n"
        date_string = f"{now.strftime('%A, %d %B %Y %H:%M:%S')}\n"
        if display == 0:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 1:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 2:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 3:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 4:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 5:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 6:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 7:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=True)

    def clear(self):
        """Clear all lines"""
        self.lines = []
