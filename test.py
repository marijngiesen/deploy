from deploy.git import Git

repository = Git("/var/www/deploy/deploy+ui", "https://github.com/marijngiesen/deploy-ui.git")

repository.check_for_new_commits_on_origin()
repository.merge_origin()