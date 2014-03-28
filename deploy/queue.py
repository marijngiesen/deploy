from _pygit2 import GitError
import time
import registry
import repository
from api import Api
from lib.git import Git
from lib import debug


def watch():
    while True:
        debug.set_prefix("queue_watcher")
        debug.message("Retrieving queue")
        try:
            queue = Api.get_queue()

            for queueitem in queue:
                debug.message("Deploying project %s version %s" % (
                    queueitem["Commit"]["Project"]["Name"], queueitem["Commit"]["Hash"]))

                # Prepare the repository
                prepare_repository(queueitem)

                # If the project is CSharp, it has to be built
                if queueitem["Commit"]["Project"]["Type"] == 0:
                    build(queueitem)

                deploy(queueitem)

        except ValueError, e:
            debug.exception("Error retrieving queue", e)
        except GitError, e:
            debug.exception("Error with Git repository", e)
        except Exception, e:
            debug.exception("Unknown error", e)

        time.sleep(registry.config["queue"]["check_interval"])


def prepare_repository(queueitem):
    debug.message("Checkout commit %s" % queueitem["Commit"]["Hash"], indent=1)

    repo = Git(repository.get_path(queueitem["Commit"]["Project"]),
               repository.get_origin_url(queueitem["Commit"]["Project"]))

    # Move the HEAD to the correct commit
    repo.checkout_commit(queueitem["Commit"]["Hash"])


def build(queueitem):
    debug.message("Build project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)


def deploy(queueitem):
    debug.message("Deploy project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)
