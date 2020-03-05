import os
import subprocess

import click


@click.command()
def sentry_release():
    version = os.getenv("APP_VERSION")
    sentry_token = os.getenv("SENTRY_AUTH_TOKEN")
    org = os.getenv("SENTRY_ORG")
    project = os.getenv("SENTRY_PROJECT")

    message = (
        " The environment variable '{var_name}' is not set, and as such the release request cannot be completed.\n\t"
        "Please set this variable and make sure it contains {message}.\n\t"
        "Example: {example} \n"
    )

    if version is None:
        raise click.ClickException(
            message.format(
                var_name="APP_VERSION",
                message="the new version tag",
                example="APP_VERSION=v0.0.0",
            )
        )
    if sentry_token is None:
        raise click.ClickException(
            message.format(
                var_name="SENTRY_AUTH_TOKEN",
                message="a valid Sentry authorization token",
                example="SENTRY_AUTH_TOKEN=dg636f1b35444f9db658d981d7e79d277898f11f388c4a18805ba67419415d78",
            )
        )
    if org is None:
        raise click.ClickException(
            message.format(
                var_name="SENTRY_ORG",
                message="the name of a valid Sentry organization",
                example="SENTRY_ORG=org-name",
            )
        )
    if project is None:
        raise click.ClickException(
            message.format(
                var_name="SENTRY_PROJECT",
                message="the name of a valid Sentry project",
                example="SENTRY_ORG=project-name",
            )
        )
    rc = subprocess.run(f"{os.path.dirname(os.path.abspath(__file__))}/sentry-release.sh")


if __name__ == "__main__":
    sentry_release()
