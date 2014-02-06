import requests
import registry


class ApiClient:
    def __init__(self):
        pass

    def getProjects(self):
        response = requests.get(registry.config["api"]["url"] + "/projects")
        return response.json()

    def setVersion(self, hash):
        response = requests.post(registry.config["api"]["url"] + "/projects/addversion")
        return response