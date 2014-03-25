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
	repository = Git(os.path.join(registry.config["repositories"]["path"], project["FormattedName"]),
	                 project["OriginUrl"])

	remote_status = repository.check_for_new_commits_on_origin()
	if remote_status == 1:
		text = "commit"
	else:
		text = "commits"

	debug.message("master is %d %s behind origin/master" % (remote_status, text))
	if remote_status > 0:
		repository.merge_origin()
