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
    def add_commit(project_id, commit_hash, date_added, message, author, changes):
        if len(message) == 0:
            message = "empty commit message"

        payload = {"Hash": str(commit_hash), "DateAdded": str(date_added), "Message": message, "Author": str(author),
                   "Changes": str(changes)}

        headers = {'content-type': 'application/json'}
        response = requests.post(registry.config["api"]["url"] + "/projects/%s/commit" % str(project_id),
                                 data=json.dumps(payload), headers=headers)

        return response.json()

    @staticmethod
    def update_status(commit_id, status):
        """
        Update the status of a commit

        :param commit_id: The ID of the commit
        :param status: The status
        :type commit_id: int
        :type status: CommitStatus
        """
        payload = {"Status": status.name}
        headers = {'content-type': 'application/json'}
        response = requests.post(registry.config["api"]["url"] + "/commits/%s/status" % str(commit_id),
                                 data=json.dumps(payload), headers=headers)

        return response.json()

    @staticmethod
    def update_buildlog(commit_id, buildlog):
        payload = {"BuildLog": str(buildlog)}
        headers = {'content-type': 'application/json'}
        response = requests.post(registry.config["api"]["url"] + "/commits/%s/buildlog" % str(commit_id),
                                 data=json.dumps(payload), headers=headers)

        print headers
        print response
        print response.text

        return response.json()

    @staticmethod
    def get_queue():
        response = requests.get(registry.config["api"]["url"] + "/queue")

        return response.json()

    @staticmethod
    def remove_from_queue(id):
        response = requests.delete(registry.config["api"]["url"] + "/queue/%s" % str(id))

        return response
