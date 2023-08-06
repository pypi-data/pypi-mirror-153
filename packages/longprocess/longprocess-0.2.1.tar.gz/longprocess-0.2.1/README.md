# `longprocess`

Utilities for running processes that take a long time. 

Call `linger()` to prevent a process from exiting when its terminal is closed.
Call `evesdrop(out_file: str, targets: List[TextIO] = [sys.stdout, sys.stdout])` to tee the output to a file, to keep track of what happens after.