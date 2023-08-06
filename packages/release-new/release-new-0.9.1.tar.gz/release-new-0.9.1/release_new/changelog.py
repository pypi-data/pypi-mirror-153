#!/usr/bin/env python3
# coding: utf-8


import re
import pathlib
import sys
from enum import Enum
from datetime import date
from dataclasses import dataclass
from collections import defaultdict

from jinja2 import Template
from mercurial import ui, hg

from release_new import REVSET_QUERY

ROOT = pathlib.Path(__file__).parent


class ChangeType(Enum):
    chore = "chore"
    ci = "ci"
    docs = "docs"
    feat = "feat"
    fix = "fix"
    perf = "perf"
    refactor = "refactor"
    style = "style"
    test = "test"
    revert = "revert"
    unknown = "unknown"


@dataclass
class Change:
    change_type: ChangeType
    title: str
    issue: str
    scope: str
    breaking_change: str

    BLACKLISTED_TITLES = ("Added tag",)

    RE_PARSE_CONVENTIONAL_TITLE = re.compile(
        r"^(?P<type>\w+)\!?(\((?P<scope>.+?)\))?\!? *: *(?P<title>.*)$"
    )

    RE_PARSE_TITLE = re.compile(r"^(\[(?P<scope>.+?)\])? *:? *(?P<title>.*)$")

    RE_PARSE_ISSUE = re.compile(
        r"\b((?:clos(?:e[sd]?|ing)|"
        r"\bfix(?:e[sd]|ing)?|"
        r"\brelat(?:e[sd]|ing)?|"
        r"\bresolv(?:e[sd]?|ing)|"
        r"\bimplement(?:s|ed|ing)?)(:?))"
        r"(?P<issue>.+)",
        re.IGNORECASE,
    )

    # match “BC” on those patterns
    # type!: BC
    # type!(topic): BC
    # BREAKING CHANGE: BC

    RE_PARSE_BREAKING_CHANGE = re.compile(
        r"((BREAKING CHANGE *)|(^.+!(\(.+\))?)): *(?P<breaking_change>.+)",
        re.IGNORECASE,
    )

    @classmethod
    def from_commit(cls, commit):
        description = commit.description().decode("utf-8")
        title, *body = description.splitlines()
        match_title = cls.RE_PARSE_CONVENTIONAL_TITLE.match(title)

        for blacklisted in cls.BLACKLISTED_TITLES:
            if blacklisted in title:
                return None

        if not match_title:
            match_title = cls.RE_PARSE_TITLE.match(title)
        if not match_title:
            print("Unable to parse the title commit {commit.rev()}", file=sys.stderr)
            return None

        try:
            change_type = ChangeType(match_title["type"])
        except (IndexError, ValueError):
            change_type = ChangeType.unknown

        breaking_change = ""
        issue = ""
        for line in body:
            match_issue = cls.RE_PARSE_ISSUE.match(line)
            if match_issue:
                issue = match_issue["issue"].strip()
                continue

            match_breaking_change = cls.RE_PARSE_BREAKING_CHANGE.match(line)
            if match_breaking_change:
                breaking_change += match_breaking_change["breaking_change"]

        # no breaking change detected in the body
        # let's parse the title
        if not breaking_change:
            match_breaking_change = cls.RE_PARSE_BREAKING_CHANGE.match(title)
            if match_breaking_change:
                breaking_change = match_breaking_change["breaking_change"]

        return Change(
            change_type=change_type,
            title=match_title["title"],
            scope=match_title["scope"],
            issue=issue,
            breaking_change=breaking_change,
        )

    @property
    def fulltitle(self):
        if self.scope:
            return f"{self.scope}: {self.title}"
        return self.title


class Changelog:
    def __init__(self, version):
        self.version = version
        self.changes = defaultdict(list)

    def add_commit(self, commit):
        change = self._change_from_commit(commit)
        if not change:
            return

        self.changes[change.change_type].append(change)

    def _change_from_commit(self, commit):
        return Change.from_commit(commit)

    def render(self, format="md"):
        with open(ROOT / "templates" / f"changelog.{format}") as fobj:
            change_log_template = Template(fobj.read())

        return change_log_template.render(
            changelog=self, ChangeType=ChangeType, date=date, len=len
        )


def generate_changelog(version, revset=REVSET_QUERY, repopath=".", format="md"):
    changelog = Changelog(version)
    repo = hg.repository(ui.ui(), repopath.encode("utf-8"))

    for rev in repo.revs(revset.encode("utf-8")):
        commit = repo[rev]
        if len(commit.parents()) > 1:
            # ignore merge
            continue

        changelog.add_commit(commit)

    return changelog.render(format=format)
