import sys
import debug
import daemon
import registry
from repository import *


def run():
    repository = GitRepo("/tmp/repo", "https://github.com/marijngiesen/zabbix-ems.git")

    remote_status = repository.check_for_new_commits_on_origin()
    if remote_status == 1:
        text = "commit"
    else:
        text = "commits"

    debug.message("master is %d %s behind origin/master" % (remote_status, text))
    if remote_status > 0:
        repository.merge_origin()


def main():
    foreground = False

    for arg in sys.argv:
        if "-d" in arg:
            debug.enable(registry.process)
        if "-l" in arg:
            debug.open_log(registry.process, registry.logfile)
        if "-f" in arg:
            # daemon.run(run, foreground=True)
            foreground = True

    daemon.start(run, foreground)


if __name__ == "__main__":
    main()
