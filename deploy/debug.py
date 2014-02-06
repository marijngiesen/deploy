from datetime import datetime


class Debug(object):
    logfile = None
    logfile_handle = None
    process = ""
    enabled = 0


def enable(process):
    Debug.enabled = 1
    Debug.process = process


def disable():
    Debug.enabled = 0


def message(msg):
    if Debug.enabled:
        print str(datetime.today()) + " " + str(Debug.process) + ": " + str(msg)


def exception(msg, e):
    write_log(msg + ":")
    write_log("+ " + str(e))
    message(msg + ":")
    message("+ " + str(e))


def open_log(process, logfile):
    Debug.logfile = logfile
    try:
        Debug.logfile_handle = open(Debug.logfile, "a")
    except Exception, e:
        pass


def write_log(message):
    if Debug.logfile_handle is not None:
        try:
            Debug.logfile_handle.write(str(datetime.today()) + " " + str(Debug.process) + ": " + str(message) + "\n")
        except Exception, e:
            pass


def close_log():
    try:
        Debug.logfile_handle.close()
    except Exception, e:
        pass