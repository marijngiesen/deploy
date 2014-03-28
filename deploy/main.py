import sys
import time
from multiprocessing import Process, Queue
from lib import daemon, debug
import registry
import repository
import queue


def run():
    processes = []

    # Start repository watcher
    repository_watcher = Process(target=repository.watch)
    repository_watcher.start()
    processes.append(repository_watcher)

    # Start deploy queue watcher
    queue_watcher = Process(target=queue.watch)
    queue_watcher.start()
    processes.append(queue_watcher)

    # The main loop
    while len(processes) > 0:
        for process in processes:
            if not process.is_alive():
                process.join(2)
                processes.remove(process)

        time.sleep(1)


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
