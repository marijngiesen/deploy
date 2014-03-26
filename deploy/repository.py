from datetime import datetime
import os
import time
import debug
import registry
from git import Git
from api import Api


def watch():
    while True:
        debug.message("Retrieving projects")
        projects = Api.get_projects()

        for project in projects:
            debug.message("Check repository status for project %s" % project["Name"])
            check_repository_status(project)

        time.sleep(registry.config["repositories"]["check_interval"] * 60)


def check_repository_status(project):
    origin_url = get_origin_url(project)

    repository = Git(os.path.join(registry.config["repositories"]["path"], project["FormattedName"]), origin_url)

    commit_count = save_commits(repository.check_for_new_commits_on_origin(), project)

    if commit_count > 0:
        repository.merge_origin()


def get_origin_url(project):
    if len(project["OriginUsername"]) > 0 and len(project["OriginPassword"]) > 0:
        protocol = project["OriginUrl"][0:project["OriginUrl"].index("/") + 2]
        url = project["OriginUrl"][project["OriginUrl"].index("/") + 2:]

        origin_url = "%s%s:%s@%s" % (protocol, project["OriginUsername"], project["OriginPassword"], url)
    else:
        origin_url = project["OriginUrl"]

    return origin_url


def save_commits(commits, project):
    commits.reverse()
    for commit in commits:
        debug.message("Add commit %s to database" % commit.oid, indent=2)

        commit_date = datetime.fromtimestamp(int(commit.commit_time)).strftime('%Y-%m-%d %H:%M:%S')
        Api.add_commit(project["ID"], commit.oid, commit_date, commit.message, commit.author.name, "")

    return len(commits)