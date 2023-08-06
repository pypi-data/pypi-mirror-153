import git
import pytest
from git_release.git_release import get_current_repo_version, SemVer


@pytest.mark.parametrize(
    "repo,expected",
    [
        (dict(tags=[SemVer(0, 0, 2), SemVer(0, 0, 1)]), SemVer(0, 0, 2)),
        (
            dict(tags=[SemVer(213, 2354, 6546), SemVer(0, 0, 1)]),
            SemVer(213, 2354, 6546),
        ),
        (dict(tags=[SemVer(i,0,0) for i in range(100)]), SemVer(99,0,0))
    ],
    indirect=["repo"],
)
def test_run(repo: git.Repo, expected):
    tag = get_current_repo_version(repo.working_tree_dir)
    assert isinstance(tag, SemVer)
    assert tag > SemVer(0, 0, 0)
    assert tag == expected


@pytest.mark.parametrize(
    "repo",
    [dict(tags=[]), dict(tags=["faulty"]), dict(tags=["test"])],
    indirect=["repo"],
)
def test_faulty_tags(repo: git.Repo):
    tag = get_current_repo_version(repo.working_tree_dir)
    assert tag == SemVer(0, 0, 0)
