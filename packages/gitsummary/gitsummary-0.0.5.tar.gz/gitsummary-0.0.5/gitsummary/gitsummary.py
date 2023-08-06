"""helper function obtains git repository, branch, and hash

When writing data to disk it is useful to record in the metadata the
version of the code that produced the data.  That information is
helpful in determining whether a data file is up to date, and also
sometimes for debugging.

"""

import git


def print_cwd_git_version():
    """return a string describing source control version information

    The string contains the git repository, branch and revision hash
    of current working directory
    """
    try:
        _repo = git.Repo(search_parent_directories=True)
        try:
            _repo_name = _repo.remotes.origin.url.split(".git")[0].split("/")[-1]
        except AttributeError as e:
            _repo_name = _repo.git_dir
        _git_sha = _repo.head.object.hexsha
        _git_short_sha = _repo.git.rev_parse(_git_sha, short=7)
        try:
            _git_branch = _repo.active_branch
        except TypeError as e:
            if "detached" in str(e):
                branch_str = "detached head;"
            else:
                raise
        else:
            branch_str = "On branch {}".format(_git_branch)
        return "{}:{} at rev {}".format(_repo_name, branch_str, _git_short_sha)
    except git.InvalidGitRepositoryError:
        return "No git repository detected."
