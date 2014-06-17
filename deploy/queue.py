from _pygit2 import GitError
import time

import debug
import registry
import repository
from api import Api
from git import Git
from build import Build
from enums import ProjectType, CommitStatus


def watch():
    while True:
        debug.set_prefix("queue_watcher")
        debug.message("Checking deploy queue")
        try:
            queue = Api.get_queue()

            for queueitem in queue:
                debug.message("Deploying project %s version %s" % (
                    queueitem["Commit"]["Project"]["Name"], queueitem["Commit"]["Hash"]))

                deploy_project(queueitem)

        except ValueError, e:
            debug.exception("Error communicating with API", e)
        except GitError, e:
            debug.exception("Error with Git repository", e)
        except Exception, e:
            debug.exception("Unknown error", e)

        time.sleep(registry.config["queue"]["check_interval"])


def prepare_repository(queueitem):
    debug.message("Checkout commit %s" % queueitem["Commit"]["Hash"], indent=1)

    repo = Git(repository.get_path(queueitem["Commit"]["Project"]),
               repository.get_origin_url(queueitem["Commit"]["Project"]))

    # Check out the correct commit and create a reference to it (deployed)
    repo.checkout_commit(queueitem["Commit"]["Hash"])


def deploy_project(queueitem):
    debug.message("Deploy project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)
    Api.update_status(queueitem["Commit"]["ID"], CommitStatus.Deployed)
