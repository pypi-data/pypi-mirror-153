import signal
import subprocess
import sys
import os
from typing import List, TextIO


def linger():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGPIPE, signal.SIG_IGN) # ! this interferes with tee?


def eavesdrop(out_file: str, targets: List[TextIO] = [sys.stdout, sys.stdout]):
    tee = subprocess.Popen(["tee", out_file], stdin=subprocess.PIPE)
    assert tee.stdin is not None
    for target in targets:
        os.dup2(tee.stdin.fileno(), target.fileno())
