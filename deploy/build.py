import os
import shutil
import registry
from subprocess import Popen, PIPE, STDOUT


def run(queueitem):
    builddirectory = get_builddirectory(queueitem["Commit"]["Project"])


def get_builddirectory(project):
    builddirectory = os.path.join(registry.config["build"]["path"], project["FormattedName"])

    if os.path.isdir(builddirectory):
        shutil.rmtree(builddirectory)

    os.makedirs(builddirectory)

    return builddirectory


def run_buildcommands(project, builddirectory):
    process = Popen(project["BuildCommands"], shell=True, stdout=PIPE, stderr=STDOUT)
    output, err = process.communicate()
    retcode = process.poll()

    if retcode != 0:
        pass
