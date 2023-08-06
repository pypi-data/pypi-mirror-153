#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
import subprocess
from datetime import date
from argparse import ArgumentParser
from pathlib import Path
from distutils.core import run_setup
from redbaron import RedBaron

from release_new.changelog import generate_changelog
from release_new import REVSET_QUERY


class RepositoryNotReadForReleaseError(ValueError):
    pass


def _compute_release_tags(revset_query):
    commit_desc_since_last_release = (
        subprocess.check_output(
            f"hg log -r '{revset_query}' " "-T '{desc}\n'",
            shell=True,
        )
        .decode("utf-8")
        .casefold()
    )

    current_branch = subprocess.check_output('hg log -T "{branch}" -r .', shell=True)

    # if we are already on a branch for a specific release
    if re.match(b"^[0-9.]+$", current_branch.strip()):
        number_of_dots = len(re.findall(rb"(\.)", current_branch.strip()))

        # apparently we only have "x.y" branches for now on cubicweb and jsonschema
        if number_of_dots == 1:  # x.y
            return "patch"

        # we'll find out on how to handle other situations later

    # XXX this may be a little bit too naive. But let's make things simple for a
    # first implementation.

    if "break" in commit_desc_since_last_release:
        return "major"
    if "feat" in commit_desc_since_last_release:
        return "minor"
    if "fix" in commit_desc_since_last_release:
        return "patch"

    raise RepositoryNotReadForReleaseError(
        "We did not find any breaking change, nor feature nor fix in your "
        "commits. Are you sure you are using conventional commits ? "
        "Please, update your commit descriptions, or specify explicitly your "
        "release choice using the --release-type CLI argument."
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--release-type",
        "-r",
        choices=["patch", "minor", "major", "auto", "calendar"],
        default="auto",
        help=(
            "Use either\n:"
            " - semantic version: major.minor.patch \n"
            " - calendar version: YY.M.num where num is the version number in the month \n"
            "auto use semantic versionning and detect the correct version from commit messages."
        ),
    )
    parser.add_argument("--no-previous-tag-check", action="store_true")
    parser.add_argument(
        "-c",
        "--preview-changelog",
        action="store_true",
        help="only display generated changelog without actually doing the release",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="simulate a full run of release-new while not committing",
    )
    parser.add_argument(
        "-q",
        "--revset-query",
        help="the mercurial revset query to get the commit used to generate the changelog",
        default=REVSET_QUERY,
    )

    args = parser.parse_args()

    if args.preview_changelog:
        if Path("doc/changes/changelog.rst").exists():
            changelog_format = "rst"
        else:
            changelog_format = "md"

        print(
            generate_changelog(
                "upcoming release", format=changelog_format, revset=args.revset_query
            ).strip()
        )
        return

    try:
        do_release(
            args.release_type,
            args.no_previous_tag_check,
            dry_run=args.dry_run,
            revset_query=args.revset_query,
        )
    except RepositoryNotReadForReleaseError as exception:
        # kdo Arthur
        print(f"⚠️ Error: {exception} 🤯🙉🙈💥")
        sys.exit(1)


def do_release(release_type, no_previous_tag_check, dry_run, revset_query):
    root = Path(".")

    # assert there is a pkginfo and a setup.py
    pkginfo_path = root / "__pkginfo__.py"
    if not pkginfo_path.exists():
        try:
            pkginfo_path = next(root.glob("cubicweb*/__pkginfo__.py"))
        except StopIteration:
            raise RepositoryNotReadForReleaseError("no pkginfo")

    setup_path = root / "setup.py"
    if not setup_path.exists():
        raise RepositoryNotReadForReleaseError("no setup.py")

    # assert hg status is happy
    # Check only (d)eleted, (a)dded, (m)odified files
    hg_not_clean = subprocess.check_output("hg status -dram", shell=True)
    if hg_not_clean:
        raise RepositoryNotReadForReleaseError(
            "You have some work in progress. Please, make a commit and "
            "rerun the command"
        )

    current_branch = subprocess.check_output(["hg", "branch"]).strip()

    # assert on public head, and clean environment
    id_last_public = subprocess.check_output(
        [
            "hg",
            "id",
            "-r",
            f"last(public() and branch({current_branch.decode()}))",
            "--template",
            "{node}",
        ]
    )
    current_id = subprocess.check_output(
        ["hg", "id", "-r", ".", "--template", "{node}"]
    )

    if current_id != id_last_public:
        current_id_is_on_last_public = id_last_public.decode("utf-8") in set(
            subprocess.check_output(
                "hg log -r 'ancestors(.) and public()' -T '{node}\n'", shell=True
            )
            .decode("utf-8")
            .strip()
            .split("\n")
        )
        if current_id_is_on_last_public:
            raise RepositoryNotReadForReleaseError(
                "There are some non-public commits.\n"
                "Please, run `hg phase -p .` to publish your commits and rerun the "
                "command"
            )
        raise RepositoryNotReadForReleaseError(
            "You are not on the last public head, please, rebase your work on "
            f"{id_last_public.decode('utf-8')}"
        )

    # get current version in the setup.py -> compare with existing tags. If it

    setup_result = run_setup(setup_path, stop_after="init")
    current_version = setup_result.get_version()

    existing_tags = (
        subprocess.check_output(["hg", "tags", "--template", "{tags}\n"])
        .decode("utf-8")
        .split("\n")
    )

    if not any(current_version in tag for tag in existing_tags):
        if not no_previous_tag_check:
            raise RepositoryNotReadForReleaseError(
                "cannot handle this situation right now. "
                f"Your current version ({current_version}) is not found in "
                f"the existing mercurial tags (last found {existing_tags[1]}).\n"
                "You can by pass previous tag check with the option: --no-previous-tag-check"
            )

    # should we check the version against pypi ?

    if release_type == "auto":
        effective_release_type = _compute_release_tags(revset_query)
    else:
        effective_release_type = release_type

    red = RedBaron(pkginfo_path.read_text())
    assignement = red.find("assign", target=lambda x: x.value == "numversion")
    assert assignement

    major = int(assignement.value[0].value)
    minor = int(assignement.value[1].value)
    patch = int(assignement.value[2].value)

    old_version = ".".join(str(x.value) for x in assignement.value)

    if effective_release_type == "patch":
        assignement.value[2].value = str(patch + 1)

    elif effective_release_type == "minor":
        assignement.value[2].value = "0"
        assignement.value[1].value = str(minor + 1)

    elif effective_release_type == "major":
        assignement.value[2].value = "0"
        assignement.value[1].value = "0"
        assignement.value[0].value = str(major + 1)

    elif effective_release_type == "calendar":
        today = date.today()
        year = today.strftime("%y")
        month = str(today.month)
        new_patch = "0"
        if f"{major}.{minor}" == f"{year}.{month}":
            new_patch = str(patch + 1)
        assignement.value[2].value = new_patch
        assignement.value[1].value = month
        assignement.value[0].value = year

    else:
        raise Exception("unhandled situation")

    pkginfo_path.write_text(red.dumps())

    new_version = ".".join(str(x.value) for x in assignement.value)

    print(
        f"Let's go for {effective_release_type} release {new_version} (from {old_version})"
    )

    if release_type in ["auto", "calendar"]:
        msg = "Automatic"
        if release_type == "calendar":
            msg = "Calendar"
        print(
            f"{msg} release guesser decided to release the version '{new_version}' "
            f"({effective_release_type})"
        )
        answer = input("Are you ok with that? [Y/n]: ")

        if answer.strip().lower() == "n":
            subprocess.check_call("hg revert .", shell=True)
            return

    changelog_path = Path("CHANGELOG.md")
    changelog_format = "md"
    if changelog_path.exists():
        previous_content = changelog_path.read_text()
    elif Path("doc/changes/changelog.rst").exists():
        # we are in CubicWeb
        minor_version = f"{assignement.value[0].value}.{assignement.value[1].value}"
        changelog_path = Path(f"doc/changes/{minor_version}.rst")
        changelog_format = "rst"
        previous_content = ""

        if changelog_path.exists():
            with open(changelog_path, "r") as f:
                previous_content = f.read()

        with open("doc/changes/changelog.rst", "r") as f:
            changelog_rst = f.read()

        if f".. include:: {minor_version}.rst" not in changelog_rst:
            title, includes = changelog_rst.split("\n\n", 1)

            with open("doc/changes/changelog.rst", "w") as f:
                f.write(title)
                f.write("\n\n")
                f.write(f".. include:: {minor_version}.rst\n")
                f.write(includes)

    else:
        print("You don't have any CHANGELOG, let's create one")
        print("and let's add it to your MANIFEST.in if necessary.")
        previous_content = ""
        manifest_path = Path("MANIFEST.in")
        if manifest_path.exists():
            manifest_content = manifest_path.read_text()
            if changelog_path.name not in manifest_content:
                manifest_path.write_text(
                    manifest_content.rstrip() + f"\nexclude {changelog_path.name}\n"
                )

    changelog_content = (
        generate_changelog(
            new_version, format=changelog_format, revset=revset_query
        ).rstrip()
        + "\n\n"
        + previous_content.lstrip()
    ).strip()

    changelog_path.write_text(changelog_content)

    text_editor_command = os.environ.get("EDITOR", "nano")

    subprocess.check_call([f"{text_editor_command}", f"{changelog_path}"])

    subprocess.check_call(f"hg add '{changelog_path}'", shell=True)

    if not dry_run:
        subprocess.check_call(
            f'hg commit -m "chore(pkg): new {effective_release_type} release ({new_version})"',
            shell=True,
        )

        subprocess.check_call(f'hg tag "{new_version}"', shell=True)
        subprocess.check_call("hg phase -p .", shell=True)

        # emojis for Arthur
        print(
            f"🎉 Congratulation, we've made a new {effective_release_type} release {new_version} "
            "\\o/ 🎇"
        )
        print()
        print("✨ 🍰 ✨")
        print()
        print("Now you need to hg push the new commits")

    else:
        subprocess.check_call("hg status", shell=True)
        subprocess.check_call("hg diff", shell=True)
