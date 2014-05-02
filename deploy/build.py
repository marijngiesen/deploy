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

    projectdirectory = repository.get_path(queueitem["Commit"]["Project"])
    solution = get_solution(projectdirectory)
    debug.message("Solution is: %s" % solution, indent=2)

    build_result = run_build(builddirectory, projectdirectory, solution)
    # save_buildlog(queueitem, builddirectory)

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


def run_build(builddirectory, projectdirectory, solution):
    command = get_command(builddirectory, solution)
    debug.message("Build command is: %s" % command, indent=2)

    return call(command, shell=True, cwd=projectdirectory)


def get_solution(projectdirectory):
    for root, dirs, files in os.walk(projectdirectory):
        solution = [filename for filename in files if filename.endswith(".sln")]

        if len(solution) > 0:
            return solution.pop()

    raise IOError("Solution file not found in project")


def get_command(builddirectory, solution):
    return str(registry.config["build"]["environment"]) + str(registry.config["build"]["command"]).replace(
        "{builddirectory}", builddirectory).replace("{solution}", solution)


def save_buildlog(queueitem, builddirectory):
    with (open(os.path.join(builddirectory, "build.log"))) as logfile:
        Api.update_buildlog(queueitem["Commit"]["ID"], logfile.read())
