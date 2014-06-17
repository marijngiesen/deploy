from _pygit2 import GitError
import time
import debug
import registry
import repository
from git import Git
from build import Build


def watch(queue):
    while True:
        debug.set_prefix("build_watcher")
        try:
            project = queue.get()

            prepare_repository(project)
            build = Build(project)
            build.run()

        except ValueError, e:
            debug.exception("Error communicating with API", e)
        except GitError, e:
            debug.exception("Error with Git repository", e)
        except Exception, e:
            debug.exception("Unknown error", e)

        time.sleep(registry.config["build"]["check_interval"])


def prepare_repository(project):
    debug.message("Checkout commit %s" % project["commit"], indent=1)

    repo = Git(repository.get_path(project), repository.get_origin_url(project))

    # Check out the correct commit and create a reference to it (deployed)
    repo.checkout_commit(project["commit"])
