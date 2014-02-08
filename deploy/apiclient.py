import requests
import registry


class ApiClient:
    def __init__(self):
        pass

    # Returns:
    # Projects: {
    #   Id: <id>,
    #   Name: <name>,
    #   Url: <url>,
    #   Servers: {[
    #       Id: <id>,
    #       HostName: <hostname>,
    #       IpAddress: <ipaddress>,
    #   ]}
    # }
    def get_projects(self):
        response = requests.get(registry.config["api"]["url"] + "/projects")
        return response.json()


    def get_project(self, id):
        response = requests.get(registry.config["api"]["url"] + "/projects/%s" % str(id))
        return response.json()

    def update_version(self, project_id, hash, committer, message):
        response = requests.post(registry.config["api"]["url"] + "/projects/%s/version" % str(project_id))
        return response

    # Returns: {QueueId: <id>, ProjectId: <id>, VersionHash: <hash>}
    def get_queue(self):
        response = requests.get(registry.config["api"]["url"] + "/queue")
        return response.json()


    def remove_from_queue(self, id):
        response = requests.delete(registry.config["api"]["url"] + "/queue/%s" % str(id))
        return response
