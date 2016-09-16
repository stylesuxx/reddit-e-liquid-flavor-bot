import sys
import settings


def log(message):
    if settings.debug:
        print message


def logOk(message):
    if settings.debug:
        print('%s[OK]%s %s' % (colors.OKGREEN, colors.ENDC, message))


def logErr(message):
    if settings.debug:
        print('%s[Err]%s %s' % (colors.FAIL, colors.ENDC, message))


def logWarn(message):
    if settings.debug:
        print('%s[Warn]%s %s' % (colors.WARNING, colors.ENDC, message))


def logNote(message):
    if settings.debug:
        print('%s[=>]%s %s' % (colors.OKBLUE, colors.ENDC, message))


def signalHandler(signal, frame):
    sys.exit(0)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
