import pytest
from git_release.git_release import semver_dataclass_to_string

@pytest.mark.parametrize("with_v", [True,False])
def test_valid(semver, with_v):
    string = semver_dataclass_to_string(semver, with_v=with_v)

    if with_v:
        assert "v" in string

    assert str(semver.major) in string
    assert str(semver.minor) in string
    assert str(semver.patch) in string
    assert len(string.split('.')) == 3
