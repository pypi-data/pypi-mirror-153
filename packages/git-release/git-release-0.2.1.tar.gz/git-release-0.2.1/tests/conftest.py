import git
import pytest
import random
from git_release.git_release import SemVer


@pytest.fixture
def semver(request):
    if hasattr(request, "param"):
        major, minor, patch = request.param
    else:
        major, minor, patch = [random.randint(0, 100) for _ in range(3)]

    yield SemVer(major, minor, patch)


@pytest.fixture
def actor():
    git_actor = git.Actor("pytest-actor", "pytest@actor.com")
    yield git_actor


@pytest.fixture
def repo(request, tmpdir, semver, actor):
    if hasattr(request, "param"):
        tags = request.param["tags"]
    else:
        tags = [str(semver)]

    tmprepo = git.Repo.init(tmpdir)

    for f in tags:
        tmprepo.index.commit(
            f"empty commit to enable a tag with name {f}", author=actor
        )
        tmprepo.create_tag(f, message="Test tag created by pytest")

    setattr(tmprepo, "_tag", semver)

    yield tmprepo
