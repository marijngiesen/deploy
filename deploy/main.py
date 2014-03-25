import sys
import time
import debug
import daemon
import registry
import repository
import queue
from multiprocessing import Process


def run():
    process_count = 2

    # Start repository watcher
    repository_watcher = Process(target=repository.watch)
    repository_watcher.start()

    # Start deploy queue watcher
    queue_watcher = Process(target=queue.watch)
    queue_watcher.start()

    # The main loop
    while process_count > 0:
        if not repository_watcher.is_alive():
            repository_watcher.join(2)
            process_count -= 1

        if not queue_watcher.is_alive():
            queue_watcher.join(2)
            process_count -= 1

        time.sleep(5)


def main():
    foreground = False

    for arg in sys.argv:
        if "-d" in arg:
            debug.enable(registry.process)
        if "-l" in arg:
            debug.open_log(registry.process, registry.logfile)
        if "-f" in arg:
            foreground = True

    daemon.start(run, foreground)


if __name__ == "__main__":
    main()
