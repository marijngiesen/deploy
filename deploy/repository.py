import os
import time
import registry
from lib.git import Git
from lib import debug
from api import Api
from datetime import datetime


def watch():
    while True:
        debug.message("Retrieving projects")
        try:
            projects = Api.get_projects()

            for project in projects:
                debug.message("Check repository status for project %s" % project["Name"])
                check_repository_status(project)

        except ValueError, e:
            debug.exception("Error retrieving projects", e)

        time.sleep(registry.config["repositories"]["check_interval"] * 60)


def check_repository_status(project):
    origin_url = get_origin_url(project)
    repository = Git(os.path.join(registry.config["repositories"]["path"], project["FormattedName"]), origin_url)
    commit_count = save_commits(repository.check_for_new_commits_on_origin(), project)

    if commit_count > 0:
        repository.merge_origin()

    # Add 20 commits if this is a new repository
    if project["Commits"] is None or len(project["Commits"]) == 0:
        save_commits(repository.get_commits(), project)


def get_origin_url(project):
    if project["OriginUsername"] is not None and project["OriginPassword"] is not None:
        protocol = project["OriginUrl"][0:project["OriginUrl"].index("/") + 2]
        url = project["OriginUrl"][project["OriginUrl"].index("/") + 2:]

        origin_url = "%s%s:%s@%s" % (protocol, project["OriginUsername"], project["OriginPassword"], url)
    else:
        origin_url = project["OriginUrl"]

    return origin_url


def save_commits(commits, project):
    for commit in commits:
        debug.message("Add commit %s to database" % commit.oid, indent=2)

        commit_date = datetime.fromtimestamp(int(commit.commit_time)).strftime('%Y-%m-%d %H:%M:%S')
        Api.add_commit(project["ID"], commit.oid, commit_date, commit.message, commit.author.name, "")

    return len(commits)