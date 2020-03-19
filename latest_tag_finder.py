"""
Latest tag finder
"""

import os
import re

import github


def latest_tag(repo):
    """
    Takes in repo.
    Gets list of tags, returns the latest tag.
    (Latest indicated by larger number in sequence that follows semantic versioning - v0.0.1 > v.0.0.0)
    """

    tag_objects_list = repo.get_tags()
    semver_pattern = r"\bv(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[\da-z\-]+(?:\.[\da-z\-]+)*)?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?\b"

    tags_list = [
        tag_object.name
        for tag_object in tag_objects_list
        if re.match(semver_pattern, tag_object.name) is not None
    ]
    return tags_list[0]


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")
    github_repo = github.Github(github_token).get_repo(repo)

    latest_tag = latest_tag(github_repo)
    print(latest_tag)
