import sys
import settings


def log(message):
    if settings.debug:
        print message


def signalHandler(signal, frame):
    sys.exit(0)
