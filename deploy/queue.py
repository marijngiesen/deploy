from _pygit2 import GitError
import time
import build
import registry
import repository
from api import Api
from lib.git import Git
from lib import debug
from commitstatus import CommitStatus
from projecttype import ProjectType


def watch():
    while True:
        debug.set_prefix("queue_watcher")
        debug.message("Checking deploy queue")
        try:
            queue = Api.get_queue()

            for queueitem in queue:
                debug.message("Deploying project %s version %s" % (
                    queueitem["Commit"]["Project"]["Name"], queueitem["Commit"]["Hash"]))

                # Prepare the repository
                prepare_repository(queueitem)

                # If the project is CSharp, it has to be built
                if queueitem["Commit"]["Project"]["Type"] == ProjectType.CSharp:
                    build_project(queueitem)

                deploy_project(queueitem)

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

    # Check out the correct commit and create a reference to it (deployed)
    repo.checkout_commit(queueitem["Commit"]["Hash"])


def build_project(queueitem):
    debug.message("Build project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)
    build.start(queueitem)
    Api.update_status(queueitem["Commit"]["ID"], CommitStatus.Build)


def deploy_project(queueitem):
    debug.message("Deploy project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)
    Api.update_status(queueitem["Commit"]["ID"], CommitStatus.Deployed)
