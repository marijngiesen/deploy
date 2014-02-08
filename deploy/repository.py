import pygit2


class GitRepo:
    repository_path = None
    repository = None
    origin_url = None
    origin_branch = None

    def __init__(self, repository_path, origin_url, origin_branch="master"):
        self.repository_path = repository_path
        self.origin_url = origin_url
        self.origin_branch = origin_branch

        try:
            self.repository = pygit2.Repository(repository_path)
        except KeyError:
            self.clone()


    def clone(self):
        self.repository = pygit2.clone_repository(self.origin_url, self.repository_path,
                                                  checkout_branch=self.origin_branch)
        self.repository.checkout()


    def status(self):
        return self.repository.status()


    def check_origin(self):
        origin_index = [index for index, remote in enumerate(self.repository.remotes) if "origin" in remote.name]

        if len(origin_index) == 0:
            return self.repository.create_remote("origin", self.origin_url)

        remote = self.repository.remotes[origin_index[0]]

        if remote.url != self.origin_url:
            remote.url = self.origin_url

        return remote


    def check_for_new_commits_on_origin(self):
        remote = self.check_origin()
        remote.fetch()

        return len(self.repository.diff("master", "origin/%s" % self.origin_branch))


    def merge_origin(self):
        remote_commit = self.repository.revparse_single("origin/%s" % self.origin_branch)
        merge_result = self.repository.merge(remote_commit.oid)

        if merge_result.is_fastforward:
            reference = self.repository.lookup_reference("refs/heads/master")
            reference.target = merge_result.fastforward_oid.hex

            return True

        return False


    def get_references(self):
        return self.repository.listall_references()


    def log(self):
        last = self.repository[self.repository.head.target]

        return self.repository.walk(last.oid, pygit2.GIT_SORT_TIME)
