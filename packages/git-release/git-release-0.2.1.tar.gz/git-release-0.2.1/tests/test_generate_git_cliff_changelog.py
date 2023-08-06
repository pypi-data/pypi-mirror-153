from git_release.git_release import find_git_cliff, generate_git_cliff_changelog


def test_valid(repo):
    generate_git_cliff_changelog(repo._tag, find_git_cliff())
