import subprocess
import os
import click

@click.command()
def sentry_release():
    version = os.getenv("APP_VERSION")
    sentry_token = os.getenv("SENTRY_AUTH_TOKEN")
    org = os.getenv("SENTRY_ORG")
    project = os.getenv("SENTRY_PROJECT")


    if version is None:
        raise click.ClickException(
            " The environment variable 'APP_VERSION' is not found, and as such the release request cannot be completed.\n\t"
        )
    if sentry_token is None:
        raise click.ClickException(
            " The environment variable 'SENTRY_AUTH_TOKEN' is not set, and as such the release request cannot be completed.\n\t"
            "Please set this variable and make sure it contains a valid Sentry authorization token.\n\t"
            "Example: SENTRY_AUTH_TOKEN=dg636f1b35444f9db658d981d7e79d277898f11f388c4a18805ba67419415d78 \n"
        )
    if org is None:
        raise click.ClickException(
            " The environment variable 'SENTRY_ORG' is not set, and as such the release request cannot be completed.\n\t"
            "Please set this variable and make sure it contains the name of a valid Sentry organization.\n\t"
            "Example: SENTRY_ORG=org-name \n"
        )
    if project is None:
        raise click.ClickException(
            " The environment variable 'SENTRY_PROJECT' is not set, and as such the release request cannot be completed.\n\t"
            "Please set this variable and make sure it contains the name of a valid Sentry project.\n\t"
            "Example: SENTRY_ORG=project-name \n"
        )
    rc = subprocess.run('./sentry-release.sh')

if __name__ == "__main__":
    sentry_release()



