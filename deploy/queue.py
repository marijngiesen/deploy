import time
import registry
from api import Api


def watch():
    while True:
        queue = Api.get_queue()

        for queueitem in queue:
            pass

        time.sleep(registry.config["queue"]["check_interval"] * 60)
