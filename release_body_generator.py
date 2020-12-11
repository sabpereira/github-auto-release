"""
Release message body generator
"""

import os
from collections import defaultdict

import click
import github
from emoji import emojize

from latest_tag_finder import latest_tag


def clean_commit_message(full_commit_message, separator):
    """
    Takes in a commit message string and a separator indicating the end of the prefix tag and start of message.
    If there is a prefix tag, returns the message excluding it.  Ex. "[Added] New method" returns "New method"
    If there is not a prefix tag, returns original. Ex. "New method" returns "New method"

    """
    seperated_commit = full_commit_message.partition(separator)

    if seperated_commit[2]:
        return seperated_commit[2].partition("\n\n")[0]
    else:
        return full_commit_message.partition("\n\n")[0]


def clean_tag(full_commit_message, separator, leading_character=""):
    """
    Takes in a commit message string and a separator for the end of the prefix tag, optional char for start of tag.
    If there is a prefix tag, and it is valid, returns capitalized version.  Ex. "[ADdeD] New method" returns "Added"
    If there is a prefix tag, and it is not valid, returns "Other".
    If there is not a prefix tag, returns "Other"

    """
    default_tag = "Other"
    valid_tags = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security", "Migrations"]

    split_commit = full_commit_message.split(sep=separator, maxsplit=1)

    possible_tag = split_commit[0].lstrip(leading_character).capitalize()

    if len(split_commit) > 1 and possible_tag in valid_tags:
        return possible_tag

    return default_tag


def create_commit_message_dict(commit_objects_list, separator, leading_character=""):
    """
    Takes in a list of commit objects (or None if it doesn't exist)
    Returns a dictionary with:
        Key:   A valid tag
        Value: List of commit messages that fall under that tag
    Returns an empty dictionary if no commits exist

    """

    commits_dict = defaultdict(list)
    ordered_tags = [
        "Added",
        "Changed",
        "Deprecated",
        "Removed",
        "Fixed",
        "Security",
        "Migrations",
        "Other",
    ]

    for tag in ordered_tags:
        commits_dict[tag]

    for commit_object in commit_objects_list:
        full_commit_message = commit_object.commit.message
        tag = clean_tag(
            full_commit_message=full_commit_message,
            separator=separator,
            leading_character=leading_character,
        )
        commit_message = clean_commit_message(
            full_commit_message=full_commit_message, separator=separator
        )
        commits_dict[tag].append(commit_message)

    contain_migrations = any(v for k, v in commits_dict.items() if k == "Migrations")
    contain_others = any(v for k, v in commits_dict.items() if k != "Migrations")
    if contain_migrations and contain_others:
        raise click.ClickException(
            f"Release contains Migrations with other type of changes {emojize(':disappointed:', use_aliases=True)} \n"
        )

    commits_dict = {k: v for k, v in commits_dict.items() if v}

    return commits_dict


def create_release_body(
    repo, latest_tag, target_commitish="master", separator="] ", leading_character="["
):
    """
    Takes in repo, latest tag, and target branch/commit for release, master is default.
    Takes in separator and leading_character parameters based on tag formatting, [TAG] is the default.
    Returns a string with the commit messages separated by tag and listed by bullet points.
    """

    commit_objects_list = repo.compare(latest_tag, target_commitish).commits

    commits_dict = create_commit_message_dict(
        commit_objects_list=commit_objects_list,
        separator=separator,
        leading_character=leading_character,
    )

    release_body_list = []
    bullets_string = "\n   * "

    for key in commits_dict:
        commits_dict[key].insert(0, f"#### {key}:")
        commits_and_tag = bullets_string.join(commits_dict[key])
        release_body_list.append(commits_and_tag)

    release_body = "\n\n".join(release_body_list)

    if not release_body:
        release_body = "No previous commit messages to display"

    return release_body


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")
    g = github.Github(github_token)
    github_repo = g.get_repo(repo)

    latest_tag = latest_tag(github_repo)
    latest_release_tag = github_repo.get_latest_release().tag_name
    target_commitish = "master"

    release_body = create_release_body(github_repo, latest_tag)

    print(release_body)
