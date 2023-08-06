import sys

from git_release.git_release import find_git_cliff


def test_in_path(tmpdir):
    path = tmpdir
    bin_path = tmpdir / "git-cliff"
    with open(bin_path, "w") as f:
        f.write("empty")

    assert find_git_cliff(str(path)) == bin_path


def test_not_in_path():
    assert find_git_cliff("") is None
