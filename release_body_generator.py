"""
Release message body generator
"""

import os

import github


def clean_commit_message(full_commit_message, separator):
    """
    Takes in a commit message string and a separator indicating the end of the prefix tag and start of message.
    If there is a prefix tag, returns the message excluding it.  Ex. "[Added] New method" returns "New method"
    If there is not a prefix tag, returns original. Ex. "New method" returns "New method"

    """
    seperated_commit = full_commit_message.partition(separator)

    if seperated_commit[2]:
        return seperated_commit[2]
    else:
        return full_commit_message


def clean_tag(full_commit_message, separator, leading_character=""):
    """
    Takes in a commit message string and a separator for the end of the prefix tag, optional char for start of tag.
    If there is a prefix tag, and it is valid, returns capitalized version.  Ex. "[ADdeD] New method" returns "Added"
    If there is a prefix tag, and it is not valid, returns "Other".
    If there is not a prefix tag, returns "Other"

    """
    tag = "Other"
    valid_tags = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]

    split_commit = full_commit_message.split(sep=separator, maxsplit=1)

    possible_tag = split_commit[0].lstrip(leading_character).capitalize()

    if len(split_commit) > 1 and possible_tag in valid_tags:
        tag = possible_tag

    return tag


def create_commit_message_dict(commit_objects_list):
    """
    Takes in a list of commit objects (or None if it doesn't exist)

    Parses through each commit message per object and pulls out the clean tag and clean commit message.

    Returns a dictionary with:
        Key:   A valid tag
        Value: List of commit messages that fall under that tag

    Returns an empty dictionary if no commits exist

    """


def create_release_body(repo, target_commitish="master"):
    """
    Takes in repo and target branch/commit for release, master is default.
    Gathers all commit messages created since the last release to be put into message body.
    Returns a string with these commit messages separated by bullet points.
    """

    latest_release_tag = repo.get_latest_release().tag_name

    commit_objects = repo.compare(latest_release_tag, target_commitish).commits
    commit_message_list = [
        "* " + commit_object.commit.message for commit_object in commit_objects
    ]

    release_body = "\n".join(commit_message_list)

    if not release_body:
        release_body = "No previous commit messages to display"

    return release_body


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN")
    g = github.Github(github_token)
    repo = os.getenv("REPO")
    github_repo = g.get_user().get_repo(repo)

    print(create_release_body(repo))
