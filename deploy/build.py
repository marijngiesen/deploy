import os
import shutil
from lib import debug
import registry
import repository
from subprocess import call


def run(queueitem):
    debug.message("Starting build of project %s" % queueitem["Commit"]["Project"]["Name"], indent=1)

    builddirectory = get_builddirectory(queueitem["Commit"]["Project"])
    debug.message("Build output directory is: %s" % builddirectory, indent=2)

    solution = get_solution(repository.get_path(queueitem["Commit"]["Project"]))
    debug.message("Solution is: %s" % solution, indent=2)

    run_build(builddirectory, solution)


def get_builddirectory(project):
    builddirectory = os.path.join(registry.config["build"]["path"], project["FormattedName"])

    if os.path.isdir(builddirectory):
        shutil.rmtree(builddirectory)

    os.makedirs(builddirectory)

    return builddirectory


def run_build(builddirectory, solution):
    command = get_command(builddirectory, solution)
    debug.message("Build command is: %s" % command, indent=2)

    retcode = call(command, shell=True)

    if retcode != 0:
        raise Exception("Build failed")


def get_solution(projectdirectory):
    for root, dirs, files in os.walk(projectdirectory):
        solution = [filename for filename in files if filename.endswith(".sln")]

        if len(solution) > 0:
            return os.path.join(projectdirectory, solution.pop())

    raise IOError("Solution file not found in project")


def get_command(builddirectory, solution):
    return str(registry.config["build"]["command"]).replace("{builddirectory}", builddirectory).replace("{solution}",
                                                                                                        solution)


def get_buildlog(builddirectory):
    pass