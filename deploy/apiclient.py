import requests
import registry
import json


class ApiClient:
    def __init__(self):
        pass


    def get_projects(self):
        response = requests.get(registry.config["api"]["url"] + "/projects")
        return response.json()


    def get_project(self, id):
        response = requests.get(registry.config["api"]["url"] + "/projects/%s" % str(id))
        return response.json()


    def add_commit(self, project_id, commit_hash, date_added, message, author, changes):
        payload = {"Hash": commit_hash, "DateAdded": date_added, "Message": message, "Author": author,
                   "Changes": changes}
        response = requests.post(registry.config["api"]["url"] + "/projects/%s/commit" % str(project_id),
                                 data=json.dumps(payload))
        return response


    def get_queue(self):
        response = requests.get(registry.config["api"]["url"] + "/queue")
        return response.json()


    def remove_from_queue(self, id):
        response = requests.delete(registry.config["api"]["url"] + "/queue/%s" % str(id))
        return response
