import os
import shutil
from api import Api
from commitstatus import CommitStatus
from lib import debug
import registry
import repository
from subprocess import call


def run(queueitem):
	debug.message("Starting build of project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)

	builddirectory = get_builddirectory(queueitem["Commit"]["Project"])
	debug.message("Build output directory is: %s" % builddirectory, indent=2)

	solutiondirectory = repository.get_path(queueitem["Commit"]["Project"])
	projects = get_projects(solutiondirectory)

	build_result = 0
	for project in projects:
		build_result += run_build(builddirectory, project)

	if build_result != 0:
		Api.update_status(queueitem["Commit"]["ID"], CommitStatus.BuildError)
		raise Exception("Build failed")

	debug.message("Build succeeded!", indent=2)
	Api.update_status(queueitem["Commit"]["ID"], CommitStatus.Build)


def get_builddirectory(project):
	builddirectory = os.path.join(registry.config["build"]["path"], project["FormattedName"])

	if os.path.isdir(builddirectory):
		shutil.rmtree(builddirectory)

	os.makedirs(builddirectory)

	return builddirectory


def run_build(builddirectory, project):
	builddirectory = os.path.join(builddirectory, project["name"])
	os.makedirs(builddirectory)

	command = get_command(builddirectory, project["file"])
	debug.message("Build command is: %s" % command, indent=2)

	return call(command, shell=True, cwd=project["directory"])


def get_projects(solutiondirectory):
	projectfiles = find_project_files(solutiondirectory)

	if len(projectfiles) < 1:
		raise IOError("No project files found in solution")

	return [
		{"name": projectfile[1].replace(".csproj", ""),
		 "file": projectfile[1],
		 "directory": projectfile[0]}
		for projectfile in projectfiles
	]

def get_project_type(projectfile):
	pass


def find_project_files(solutiondirectory):
	return [
		[root, filename]
		for root, dirs, files in os.walk(solutiondirectory)
		for filename in files if filename.endswith(".csproj")
	]


def get_command(builddirectory, projectfile):
	return "%s%s" % (str(registry.config["build"]["environment"]), str(registry.config["build"]["command"]).replace(
		"{builddirectory}", builddirectory).replace("{projectfile}", projectfile))


def save_buildlog(queueitem, builddirectory):
	with (open(os.path.join(builddirectory, "build.log"))) as logfile:
		Api.update_buildlog(queueitem["Commit"]["ID"], logfile.read())
