import pytest
from git_release.git_release import validate_semver

@pytest.mark.parametrize("string",[
    "v1.0.0", "1.0.0", "493248.234324.23423", "v324234.2689.423432"
])
def test_valid(string):
    semver = validate_semver(string)
    assert semver.major >= 0
    assert semver.minor >= 0
    assert semver.patch >= 0

@pytest.mark.parametrize("string",[
    "v1.0","hello","world"
])
def test_invalid_numbers(string):
    with pytest.raises(Exception):
        validate_semver(string)
