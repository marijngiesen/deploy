import os
import sys
import time
import signal
import debug
import registry


def run(callback, foreground=False):
    signal.signal(signal.SIGTERM, shutdown)
    if foreground: signal.signal(signal.SIGINT, shutdown)

    while True:
        callback()
        time.sleep(registry.config["repositories"]["check_interval"] * 60)


def shutdown(signal, frame):
    debug.message("Caught signal %s, shutting down." % str(signal))

    if registry.pid_file is not None:
        try:
            os.unlink(registry.pid_file)
        except OSError:
            pass

    sys.exit(0)


def write_pid(pid):
    try:
        with open(registry.pid_file, "w") as pid_file:
            pid_file.write(str(pid))
            pid_file.close()
    except OSError, e:
        debug.exception("Exception while writing PID file", e)
        sys.exit(1)


def start(callback, foreground=False):
    if foreground:
        debug.message("Running in foreground mode")
        run(callback, foreground)

    pid = os.fork()
    if pid:
        debug.message("Running in daemon mode, pid: %s" % str(pid))
        write_pid(pid)
        sys.exit(0)
    else:
        run(callback)
