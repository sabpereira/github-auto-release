# Automated GitHub Releases
<!---
# Automated GitHub and Sentry Releases
-->


## :heavy_check_mark: Prerequisites
* Python 3.5+

<!---
#### To use Sentry releases
* curl
* sentry-cli 
-->



## :gear: Installation 
To install, run:

```bash
$ pip install -e git+https://github.com/belvo-finance/github-auto-release.git#egg=github-auto-release
```

<!---
For the Sentry releases, you must install the Sentry CLI. You can find the instructions [here.](https://docs.sentry.io/cli/installation/#automatic-installation)

If you are on OS X or Linux, you can use the automated downloader which will fetch the latest release version for you and install it:

```bash
$ curl -sL https://sentry.io/get-cli/ | bash
```
-->

## :wrench: How to use - GitHub releases
> **_NOTE:_** Make sure environment variables `GITHUB_TOKEN` and `REPO` are set.


Run `new-release` followed by the desired version bump type: `major`, `minor`, `patch`. 

For example, the following will allow you to create tag bumped by a minor version:

```bash
$ new-release minor
```

### Target commitish option

The default commitish value where the Git tag is created from is the `master` branch. To specify a different commitish value, run with the `--target_commitish` option. For example:

```bash
$ new-release minor --target_commitish eb6bc2c21ff896f159da74608f0a96330419a3g5
```
### Changelog formatting for GitHub release descriptions

Release descriptions are automatically generated based on the commits created and their messages, organized by types of changes.
We are using [keep a changelog](https://keepachangelog.com/en/1.0.0/) as a reference for the types of changes and their definitions.

For proper formatting of the changelog descriptions, all commits to master should be formatted as follows:

```markdown
[LABEL] MESSAGE
```
Where "LABEL" is one of the valid types of changes listed below:
* **[Added]** for new features.
* **[Changed]** for changes in existing functionality.
* **[Deprecated]** for soon-to-be removed features.
* **[Removed]** for now removed features.
* **[Fixed]** for any bug fixes.
* **[Security]** in case of vulnerabilities.
* **[Migrations]** for database migrations(need to be stand alone).
* **[Other]** for all other changes (or mislabeled changes).

Any commit message that is missing a label or improperly labeled will be automatically labeled as **[Other]**.


<!---
## :hammer_and_wrench: How to use - Sentry releases
> **_NOTE:_** Make sure environment variables `SENTRY_AUTH_TOKEN`, `SENTRY_ORG` and `SENTRY_PROJECT` are set. 
You must also have the latest release version tag available as `APP_VERSION`.

Run the following:

```bash
$ sentry-release 
```
-->



## :question: Usage help

For usage help, run:

```bash
$ new-release --help
```


