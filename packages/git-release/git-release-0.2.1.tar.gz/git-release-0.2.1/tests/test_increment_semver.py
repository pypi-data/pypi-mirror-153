import copy

import pytest
from git_release.git_release import (
    increment_semver,
    increment_major_semver_by_one,
    increment_minor_semver_by_one,
    increment_patch_semver_by_one,
)


@pytest.mark.parametrize("major", [0, 1, 10])
@pytest.mark.parametrize("minor", [0, 1, 234])
@pytest.mark.parametrize("patch", [0, 1, 23423])
def test_valid(semver, major, minor, patch):
    old_semver = copy.deepcopy(semver)
    semver = increment_semver(semver, major, minor, patch)

    assert semver.major == old_semver.major + major
    assert semver.minor == old_semver.minor + minor
    assert semver.patch == old_semver.patch + patch


def test_inc_major_by_one(semver):
    old_semver = copy.deepcopy(semver)
    semver = increment_major_semver_by_one(semver)
    assert semver.major == old_semver.major + 1
    assert semver.minor == 0
    assert semver.patch == 0


def test_inc_minor_by_one(semver):
    old_semver = copy.deepcopy(semver)
    semver = increment_minor_semver_by_one(semver)
    assert semver.major == old_semver.major
    assert semver.minor == old_semver.minor + 1
    assert semver.patch == 0


def test_inc_patch_by_one(semver):
    old_semver = copy.deepcopy(semver)
    semver = increment_patch_semver_by_one(semver)
    assert semver.major == old_semver.major
    assert semver.minor == old_semver.minor
    assert semver.patch == old_semver.patch + 1
