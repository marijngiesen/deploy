# from deploy.lib.git import Git
#
# repository = Git("/var/www/deploy/deploy+ui", "https://github.com/marijngiesen/deploy-ui.git")
#
# commit1 = repository.get_commit("e1fa886aaa84319be90cceaaadda860b00ffd232")
# commit2 = repository.get_commit("e1fa886aaa84319be90cceaaadda860b00ffd232^")
#
# print commit1.parents
#
# print repository.get_changes(commit1, commit2)

from deploy import registry
from deploy.commitstatus import CommitStatus
from deploy.lib.config import Config
from deploy.api import Api

cfg = Config("config.yaml")
registry.config = cfg.all()

# queue = Api.get_queue()
#
# for queueitem in queue:
#     print queueitem["Commit"]["Project"]["Type"]

# repository = Git("/var/www/deploy/deploy+ui", "https://github.com/marijngiesen/deploy-ui.git")
# repository.checkout_commit("42283823caefd4e3622e661ff7e7dd1ec4637109")

Api.update_buildlog(65, "Test build log")
Api.update_status(65, CommitStatus.Build)