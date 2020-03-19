"""
Github automated release generator
"""
import os
import re

import click
import github
from emoji import emojize

from latest_tag_finder import latest_tag
from release_body_generator import create_release_body
from tag_generator import tag_gen


def validate_version(ctx, param, value):
    if value not in ["major", "minor", "patch"]:
        raise click.BadParameter(
            'Run again specifying a valid version bump (ie. "major", "minor", or "patch")'
        )
    return value


@click.command()
@click.argument("version", callback=validate_version)
@click.option(
    "--target_commitish",
    default="master",
    help="The commitish value that determines where the Git tag is created from. Can be any branch or commit SHA. Default is master.",
)
def auto_release(version, target_commitish):

    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")

    if github_token is None:
        raise click.ClickException(
            " The environment variable 'GITHUB_TOKEN' is not set, and as such the release request cannot be completed.\n\t"
            "Please set this variable and make sure it contains a valid GitHub authorization token.\n\t"
            "Example: GITHUB_TOKEN=db02a72441032669ce797eaa3328f6c21d05120f \n"
        )
    if repo is None:
        raise click.ClickException(
            " The environment variable 'REPO' is not set, and as such the release request cannot be completed.\n\t"
            "Please set this variable and make sure it contains the name of a valid GitHub repository.\n\t"
            "Example: REPO=test_repo \n"
        )

    g = github.Github(github_token)
    github_repo = g.get_repo(repo)
    current_tag = latest_tag(github_repo)
    semver_pattern = r"\bv(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[\da-z\-]+(?:\.[\da-z\-]+)*)?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?\b"

    if re.match(semver_pattern, current_tag) is None:
        raise click.ClickException(
            f"Latest release does not have proper semantic version formatting, auto release cannot continue. {emojize(':disappointed:', use_aliases=True)} \n"
        )

    else:
        new_tag = tag_gen(current_tag=current_tag, bump_type=version)
        message = create_release_body(
            repo=github_repo, latest_tag=current_tag, target_commitish=target_commitish
        )

        click.secho(f"Current Tag: {current_tag}", fg="yellow", bold=True)
        click.secho(
            f"New Tag:  {emojize(':star2:', use_aliases=True)} {new_tag} {emojize(':star2:', use_aliases=True)}",
            fg="green",
            bold=True,
        )
        click.echo("")
        click.secho(
            f"Changelog {emojize(':page_with_curl:',use_aliases=True)}", bold=True
        )
        click.echo(message + "\n")

        if click.confirm("Do you want to continue?"):

            new_release = github_repo.create_git_release(
                tag=new_tag,
                name=new_tag,
                message=message,
                draft=False,
                prerelease=False,
                target_commitish=target_commitish,
            )
            click.secho(
                f"Release successful! {emojize(':grin:', use_aliases=True)}", bold=True
            )
            click.echo(f"Link to release page: {new_release.html_url}\n")
        else:
            click.echo(f"OK bye {emojize(':disappointed:', use_aliases=True)} \n")


if __name__ == "__main__":
    auto_release()
