import pytest
from git_release.git_release import SemVer, validate_semver

def test_int():
    assert int(SemVer(1,1,1)) == 4295032833
    assert int(SemVer(123,123,123)) == 528289038459

def test_equalities(semver):
    assert SemVer(semver.major,semver.minor,semver.patch-1) < semver
    assert SemVer(semver.major,semver.minor-1,semver.patch) < semver
    assert SemVer(semver.major-1,semver.minor,semver.patch) < semver
    assert semver > SemVer(semver.major-1,semver.minor,semver.patch)
    assert semver > SemVer(semver.major,semver.minor-1,semver.patch)
    assert semver > SemVer(semver.major,semver.minor,semver.patch-1)
    assert semver <= SemVer(semver.major,semver.minor,semver.patch)
    assert semver >= SemVer(semver.major,semver.minor,semver.patch)
    assert semver == SemVer(semver.major,semver.minor,semver.patch)
    assert semver != SemVer(semver.major,semver.minor,semver.patch+1)

    assert semver != "string"
    assert semver != tuple()
    assert semver != dict()

@pytest.mark.parametrize(
    "semvers,largest",[
        [("0.0.0","0.1.1","1.0.0","5.5.5","5.6.6"),"5.6.6"],
        [("0.1.0","0.0.10"),"0.1.0"],
        [("1.0.0","0.0.10"),"1.0.0"],
        [("1.0.0","0.1.0"),"1.0.0"],
        [("1.0.1","1.1.0","0.0.0"),"1.1.0"]
    ]
)
def test_get_largest(semvers,largest):
    semvers_objs = [validate_semver(f) for f in semvers]

    assert validate_semver(largest) == max(semvers_objs)
