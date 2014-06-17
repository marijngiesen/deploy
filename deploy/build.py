import os
import shutil
from subprocess import call

from api import Api
from enums import CommitStatus, CSharpProjectTypes

import debug
import registry
import repository


class Build:
    project = None
    commit = None
    project_directory = None
    build_directory = None

    def __init__(self, queue_item):
        self.project = queue_item["Commit"]["Project"]
        self.commit = queue_item["Commit"]
        self.project_directory = repository.get_path(self.project)

        self.create_build_directory()

    def run(self):
        debug.message("Starting build of project %s" % self.project["Name"], indent=1)

        build_result = 0
        for solution in self.get_solutions():
            build_result += self.run_build(solution)

            if build_result != 0:
                Api.update_status(self.commit["ID"], CommitStatus.BuildError)
                raise Exception("Build of solution %s failed" % solution["name"])

            self.publish()
            debug.message("Build of solution %s succeeded!" % solution["name"], indent=2)

        Api.update_status(self.commit["ID"], CommitStatus.Build)
        debug.message("Build of project %s completed" % self.project["Name"], indent=1)

    def run_build(self, solution):
        return call(self.get_command(solution["file"], solution["directory"]), shell=True, cwd=solution["directory"])

    def publish(self):
        projects = self.get_projects()

        for project in projects:
            debug.message("Publishing project %s" % project["name"], indent=3)
            build_directory = self.create_build_subdirectory(project)
            project_directory = os.path.join(project["directory"], registry.config["build"]["outdir"], "Release")

            project_type = self.get_project_type(project)
            if project_type == CSharpProjectTypes.Console or project_type == CSharpProjectTypes.Test:
                self.publish_project(project_directory, build_directory)
            elif project_type == CSharpProjectTypes.WebApp:
                self.publish_project(os.path.join(project_directory, "_PublishedWebsites", project["name"]),
                                     build_directory)
            else:
                raise Exception("Invalid project type or project type could not be inferred.")

    def publish_project(self, project_directory, build_directory):
        for entry in os.listdir(project_directory):
            shutil.move(os.path.join(project_directory, entry), build_directory)

    # =============================================================================================================
    # Internal methods
    # =============================================================================================================
    def create_build_directory(self):
        build_directory = os.path.join(registry.config["build"]["path"], self.project["FormattedName"])

        if not os.path.isdir(build_directory):
            os.makedirs(build_directory)

        self.build_directory = build_directory

    def create_build_subdirectory(self, project):
        build_directory = os.path.join(self.build_directory, project["name"], self.commit["Hash"])

        if os.path.isdir(build_directory):
            shutil.rmtree(build_directory)

        os.makedirs(build_directory)
        return build_directory

    def get_projects(self):
        return self.find_files("csproj")

    def get_solutions(self):
        return self.find_files("sln")

    def find_files(self, extension):
        extension = "." + extension

        files = [
            [root, filename]
            for root, dirs, files in os.walk(self.project_directory)
            for filename in files if filename.endswith(extension)
        ]

        if len(files) < 1:
            raise IOError("No files found with extension %s" % extension)

        return [
            {"name": filepath[1].replace(extension, ""),
             "file": filepath[1],
             "directory": filepath[0]}
            for filepath in files
        ]

    def get_project_type(self, project):
        build_directory = os.path.join(project["directory"], registry.config["build"]["outdir"], "Release")

        if os.path.isdir(os.path.join(build_directory, "_PublishedWebsites")):
            return CSharpProjectTypes.WebApp
        else:
            return CSharpProjectTypes.Console

    def get_command(self, solution, build_directory):
        return "%s%s" % (str(registry.config["build"]["environment"]),
                         str(registry.config["build"]["command"])
                         .replace("{builddirectory}", build_directory)
                         .replace("{outdir}", registry.config["build"]["outdir"])
                         .replace("{solution}", solution)
                         .replace("{configuration}", "Release"))

    def save_buildlog(self):
        with (open(os.path.join(self.build_directory, "build.log"))) as logfile:
            Api.update_buildlog(self.commit["ID"], logfile.read())
