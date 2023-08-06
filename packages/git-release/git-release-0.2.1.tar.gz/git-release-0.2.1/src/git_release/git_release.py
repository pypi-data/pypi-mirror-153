import dataclasses
import os
import random
import re
import argparse as ap
import distutils.spawn
import string
import subprocess
import tempfile
from typing import Optional, Union
import git
import pathlib
from loguru import logger

_PARSER = None

def setup_ap() -> ap.ArgumentParser:  # pragma: no cover
    parser = ap.ArgumentParser(prog="git-release")
    parser.add_argument(
        "--comment",
        "-c",
        type=str,
        help="A comment to describe the release. "
        "Synonymous to a tag message. Defaults "
        "to the generated changelog.",
    )

    parser.add_argument(
        "--remote",
        "-r",
        type=str,
        default="origin",
        help="The repository remote (" "defaults to 'origin')",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="NOT IMPLEMENTED YET"
    )

    # -- SemVer --- #
    semver_behaviour = parser.add_argument_group(
        "Semantic Version",
        description="Options to manipulate the version. If --semver is not passed, "
        "git-release uses the most recent tag.",
    )

    semver_behaviour.add_argument(
        "--semver",
        type=validate_semver,
        help="Custom semantic version. Use --no-inc to use as is.",
    )

    increment = semver_behaviour.add_mutually_exclusive_group()

    increment.add_argument(
        "--major",
        "-M",
        dest="inc_major",
        action="store_true",
        help="Increment the major version by 1 (resets minor and patch)",
    )
    increment.add_argument(
        "--minor",
        "-m",
        dest="inc_minor",
        action="store_true",
        help="Increment the minor version by 1 (resets patch). Default behaviour",
    )
    increment.add_argument(
        "--patch",
        "-P",
        action="store_true",
        help="Increment the patch version by 1",
        dest="inc_patch",
    )
    increment.add_argument(
        "--no-inc",
        action="store_true",
        help="Don't increment " "anything",
        default=False,
    )
    global _PARSER
    _PARSER = parser
    return parser


def main():  # pragma: no cover
    logger.trace("Start of main")
    parser = setup_ap()
    args = parser.parse_args()

    git_cliff_bin = find_git_cliff()
    if not args.comment and git_cliff_bin is None:
        logger.critical(
            f"--comment was not set, and git-cliff cannot be found within $PATH."
            f" Either install git-cliff or add a comment when rerunning."
        )
        exit(1)

    if args.semver is None:
        semver = get_current_repo_version()
    else:
        semver = args.semver

    if not args.no_inc:
        if args.inc_major:
            semver = increment_major_semver_by_one(semver)
        elif args.inc_minor:
            semver = increment_minor_semver_by_one(semver)
        elif args.inc_patch:
            semver = increment_patch_semver_by_one(semver)
        else:
            semver = increment_minor_semver_by_one(semver)
        logger.debug(f"New version: {semver}")
    else:
        logger.warning(
            f"You have chosen not to increment the semantic version. This "
            f"may cause errors within Git"
        )

    if args.comment:
        message = args.comment
    else:
        changelog = generate_git_cliff_changelog(semver, git_cliff_bin)
        write_and_commit_changelog(changelog, semver)
        message = generate_git_cliff_message(git_cliff_bin)

    create_tag(semver, message)
    push_to_remote(semver, args.remote)
    logger.trace("End of main")


@dataclasses.dataclass
class SemVer:
    major: int
    minor: int
    patch: int

    def __int__(self):
        shift = 16
        return (self.major << 2 * shift) + (self.minor << shift) + self.patch

    def __eq__(self, other: object):
        if not isinstance(other, SemVer):
            return False
        return int(self) == int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __str__(self):
        return semver_dataclass_to_string(self)


def find_git_cliff(path: Optional[pathlib.Path] = None) -> Optional[pathlib.Path]:
    ex_path = distutils.spawn.find_executable("git-cliff", path)
    if ex_path is None:
        logger.error("Unable to find git-cliff binary. Is it even installed?")
        return None
    logger.debug(f"Found git-cliff binary at {ex_path}")
    return pathlib.Path(ex_path)


def generate_git_cliff_changelog(tag: SemVer, executable: pathlib.Path) -> str:
    logger.debug(f"Generating git-cliff changelog")
    changelog = subprocess.run(
        [str(executable), "--tag", semver_dataclass_to_string(tag)], capture_output=True
    ).stdout.decode("utf-8")
    return changelog


__print_once = True


def get_repo(path: Optional[pathlib.Path] = None) -> git.repo:
    try:
        repo = git.Repo(
            path if path is not None else pathlib.Path.cwd(),
            search_parent_directories=True,
        )
        global __print_once
        if __print_once := False:
            logger.debug(f"Repo found at {repo.working_tree_dir}")
        return repo
    except git.exc.InvalidGitRepositoryError as e:
        logger.critical("git-release was run outwith a valid git repository")
        global _PARSER
        _PARSER.print_help()
        exit(1)


def write_and_commit_changelog(
    changelog: str, tag: SemVer, path: Optional[pathlib.Path] = None
):
    logger.debug("Writing changelog to CHANGELOG.md and committing")
    repo = get_repo(path)

    with open("CHANGELOG.md", "w") as f:
        f.write(changelog)

    repo.index.add(["CHANGELOG.md"])
    repo.index.write()
    repo.git.commit(
        "-S", "-m", f"chore(release): update changelog for {tag} [skip pre-commit.ci]",
        "--no-verify"
    )


def generate_git_cliff_message(executable: pathlib.Path) -> str:
    logger.debug(f"Generating git-cliff message")
    message = subprocess.run(
        [str(executable), "--unreleased", "--strip", "all"], capture_output=True
    ).stdout.decode("utf-8")
    return message


def create_tag(tag: SemVer, message: str, path: pathlib.Path = None) -> None:
    repo = get_repo(path)

    repo.create_tag(semver_dataclass_to_string(tag), message=message)


def push_to_remote(tag: SemVer, remote: str = "origin", path: pathlib.Path = None):
    repo = get_repo(path)
    logger.info(f"Pushing tag {tag} and branch {repo.active_branch} to {remote}")

    origin = repo.remotes[remote]
    origin.push([str(repo.active_branch)],no_verify=True).raise_if_error()
    origin.push([semver_dataclass_to_string(tag)],no_verify=True).raise_if_error()


def get_current_repo_version(path: pathlib.Path = None):
    repo = get_repo(path)
    if repo.is_dirty():
        logger.warning(
            "This repo has unstaged changes. Git-release needs to be run in "
            "a up-to-date one in order to be effective. Please stage your "
            "changes and re-run."
        )

    tags = repo.tags
    semver_list = []
    for tag in tags:
        try:
            semver_list.append(validate_semver(tag.name))
        except Exception:  # TODO Use custom exceptions
            pass

    if len(semver_list) == 0:
        logger.warning(
            "No valid semver tags were found in this repo. Running with "
            "v0.0.0 and following increment procedure."
        )
        return SemVer(0, 0, 0)
    max_tag = max(semver_list)
    logger.debug(f"Found highest semantic version: {max_tag}")
    return max_tag


def validate_semver(tocheck: str) -> SemVer:
    semver_regex = r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$"
    result = re.findall(semver_regex, tocheck)

    if len(result) == 1:
        major, minor, patch = [int(f) for f in result[0]]
        return SemVer(major, minor, patch)
    raise Exception(
        f"Expected a single semver (v<major>.<minor>.<patch>) but got "
        f"{len(result)} instead"
    )


def increment_major_semver_by_one(semver: SemVer):
    semver = increment_semver(semver, major=1)
    semver.minor = 0
    semver.patch = 0
    return semver


def increment_minor_semver_by_one(semver: SemVer):
    semver = increment_semver(semver, minor=1)
    semver.patch = 0
    return semver


def increment_patch_semver_by_one(semver: SemVer):
    return increment_semver(semver, patch=1)


def increment_semver(
    semver: SemVer, major: int = 0, minor: int = 0, patch: int = 0
) -> SemVer:
    semver.major += major
    semver.minor += minor
    semver.patch += patch
    return semver


def semver_dataclass_to_string(semver: SemVer, with_v: bool = True) -> str:
    return f"{'v' if with_v else ''}{semver.major}.{semver.minor}.{semver.patch}"
