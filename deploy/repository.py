from _pygit2 import GitError
import os
import time
from datetime import datetime

import debug
from deploy.build import Build
from deploy.enums import ProjectType
import registry
from git import Git
from api import Api


def watch(build_queue):
    while True:
        debug.set_prefix("repository_watcher")
        debug.message("Retrieving projects")
        try:
            projects = Api.get_projects()

            for project in projects:
                debug.message("Check repository status for project %s" % project["Name"])
                repository = Git(get_path(project), get_origin_url(project))
                commit_count = handle_incoming_commits(repository.check_for_new_commits_on_origin(), project,
                                                       repository, build_queue)
                if commit_count > 0:
                    repository.merge_origin()

                # Add <initial_nr_commits> commits if this is a new repository
                if project["Commits"] is None or len(project["Commits"]) == 0:
                    handle_incoming_commits(
                        repository.get_commits(registry.config["repositories"]["initial_nr_commits"]), project,
                        repository, build_queue)

        except ValueError, e:
            debug.exception("Error retrieving projects", e)
        except GitError, e:
            debug.exception("Error with Git repository", e)
        except OSError, e:
            debug.exception("Error connecting to remote", e)
        except Exception, e:
            debug.exception("Unknown error", e)

        time.sleep(registry.config["repositories"]["check_interval"])


def get_path(project):
    return os.path.join(registry.config["repositories"]["path"], project["FormattedName"])


def get_origin_url(project):
    if project["OriginUsername"] is not None and project["OriginPassword"] is not None:
        protocol = project["OriginUrl"][0:project["OriginUrl"].index("/") + 2]
        url = project["OriginUrl"][project["OriginUrl"].index("/") + 2:]

        origin_url = "%s%s:%s@%s" % (protocol, project["OriginUsername"], project["OriginPassword"], url)
    else:
        origin_url = project["OriginUrl"]

    return origin_url


def handle_incoming_commits(commits, project, repository, build_queue):
    for commit in commits:
        debug.message("Add commit %s to database" % commit.oid, indent=2)

        commit_date = datetime.fromtimestamp(int(commit.commit_time)).strftime('%Y-%m-%d %H:%M:%S')

        if len(commit.parents) > 0:
            changes = repository.get_changes(commit, commit.parents[0])
        else:
            changes = repository.get_changes(commit)

        Api.add_commit(project["ID"], commit.oid, commit_date, commit.message, commit.author.name, changes)

        project["commit"] = commit.oid
        build_queue.put(project)

    return len(commits)

