import pygit2
import debug


class Git:
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
        """
        Clone a remote repository
        """
        self.repository = pygit2.clone_repository(self.origin_url, self.repository_path,
                                                  checkout_branch=self.origin_branch)
        self.repository.checkout()

    def check_origin(self):
        """
        Check if the origin of the repository matches the origin_url given with object creation. If not, add the
        correct one.

        :rtype : pygit2.Remotes
        :return: The list of remotes
        """
        origin_index = [index for index, remote in enumerate(self.repository.remotes) if "origin" in remote.name]

        if len(origin_index) == 0:
            return self.repository.create_remote("origin", self.origin_url)

        remote = self.repository.remotes[origin_index[0]]

        if remote.url != self.origin_url:
            remote.url = self.origin_url

        return remote

    def check_for_new_commits_on_origin(self):
        """
        Check for new commits on remote repository.

        :rtype : list
        :return: a list of commits
        """
        remote = self.check_origin()
        remote.fetch()

        remote_commit = self.repository.revparse_single("origin/%s" % self.origin_branch)
        local_commit = self.repository.revparse_single("master")

        debug.message("Local is at %s" % str(local_commit.oid), indent=1)
        debug.message("Remote is at %s" % str(remote_commit.oid), indent=1)

        commits = []
        for commit in self.repository.walk(remote_commit.oid, pygit2.GIT_SORT_TIME):
            if local_commit.oid == commit.oid:
                break

            commits.append(commit)

        commit_count = len(commits)
        if commit_count == 1:
            text = "commit"
        else:
            text = "commits"

        debug.message("Master is %d %s behind origin/master" % (commit_count, text), indent=1)

        return commits

    def merge_origin(self):
        """
        Merge commits from origin.

        :rtype : bool
        :return: True if merge is fast-forward, false otherwise.
        """
        remote_commit = self.repository.revparse_single("origin/%s" % self.origin_branch)

        debug.message("Merge origin/master", indent=1)
        merge_result = self.repository.merge(remote_commit.oid)

        if merge_result.is_fastforward:
            reference = self.repository.lookup_reference("refs/heads/master")
            reference.target = merge_result.fastforward_oid.hex

            return True

        return False
