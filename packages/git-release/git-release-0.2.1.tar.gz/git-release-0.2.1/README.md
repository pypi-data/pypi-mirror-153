# git-release

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/iwishiwasaneagle/git-release/master.svg)](https://results.pre-commit.ci/latest/github/iwishiwasaneagle/git-release/master)
[![CI](https://github.com/iwishiwasaneagle/git-release/actions/workflows/CI.yml/badge.svg)](https://github.com/iwishiwasaneagle/git-release/actions/workflows/CI.yml)
[![License](https://img.shields.io/github/license/iwishiwasaneagle/git-release)](https://github.com/iwishiwasaneagle/git-release/blob/master/LICENSE.txt)
![OS: Linux](https://img.shields.io/badge/Supported%20OS-Linux,%20Mac-informational)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/git-release)](https://pypi.org/project/git-release/)
[![PyPI](https://img.shields.io/pypi/v/git-release)](https://pypi.org/project/git-release/)
[![codecov](https://codecov.io/gh/iwishiwasaneagle/git-release/branch/master/graph/badge.svg?token=AY8CB7ZLM1)](https://codecov.io/gh/iwishiwasaneagle/git-release)

Easily generate tag-based releases. Uses the powerful [`git-cliff`](https://github.com/orhun/git-cliff) to generate changelogs. These can then be leveraged via [github actions](https://github.com/iwishiwasaneagle/git-release/blob/master/.github/workflows/CD.yml)

## Installation

```bash
# Install dependencies
cargo install git-cliff

# Install git-release
pip install git-release
```

## Usage

```txt
usage: git-release [-h] [--comment COMMENT] [--remote REMOTE] [-v] [--semver SEMVER] [--major | --minor | --patch | --no-inc]

optional arguments:
  -h, --help            show this help message and exit
  --comment COMMENT, -c COMMENT
                        A comment to describe the release. Synonymous to a tag message. Defaults to the generated changelog.
  --remote REMOTE, -r REMOTE
                        The repository remote (defaults to 'origin')
  -v, --verbose         NOT IMPLEMENTED YET

Semantic Version:
  Options to manipulate the version. If --semver is not passed, git-release uses the most recent tag.

  --semver SEMVER       Custom semantic version. Use --no-inc to use as is.
  --major, -M           Increment the major version by 1 (resets minor and patch)
  --minor, -m           Increment the minor version by 1 (resets patch)
  --patch, -P           Increment the patch version by 1 (default behaviour)
  --no-inc              Don't increment anything
```

## Contributing

Ensure that `pre-commit` is installed and working. Otherwise the pre-commit CI will most likely fail.

```bash
# Install and setup pre-commit
pip install pre-commit
pre-commit install --install-hooks
```

## Repos that have used git-release

- [iwishiwasaneagle/jsim](https://github.com/iwishiwasaneagle/jsim)
