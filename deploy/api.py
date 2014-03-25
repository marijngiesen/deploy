import requests
import registry
import json


class Api:
    def __init__(self):
        pass


    @staticmethod
    def get_projects():
        response = requests.get(registry.config["api"]["url"] + "/projects")

        return response.json()


    @staticmethod
    def get_project(id):
        response = requests.get(registry.config["api"]["url"] + "/projects/%s" % str(id))

        return response.json()


    @staticmethod
    def add_commit(project_id, commit_hash, date_added, message, author, changes):
        payload = {"Hash": commit_hash, "DateAdded": date_added, "Message": message, "Author": author,
                   "Changes": changes}
        headers = {'content-type': 'application/json'}

        response = requests.post(registry.config["api"]["url"] + "/projects/%s/commit" % str(project_id),
                                 data=json.dumps(payload), headers=headers)
        return response.json()


    @staticmethod
    def get_queue():
        response = requests.get(registry.config["api"]["url"] + "/queue")
        return response.json()


    @staticmethod
    def remove_from_queue(id):
        response = requests.delete(registry.config["api"]["url"] + "/queue/%s" % str(id))
        return response
