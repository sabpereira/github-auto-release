# Automated GitHub and Sentry Releases

## :heavy_check_mark: Prerequisites
* Python 3.5+




## :gear: Installation 
To install, run:

```bash
$ pip install -e git+https://github.com/sabpereira/github-auto-release.git#egg=github-auto-release
```

For the Sentry releases, you must install the Sentry CLI. You can find the instructions [here.](https://docs.sentry.io/cli/installation/#automatic-installation)

If you are on OS X or Linux, you can use the automated downloader which will fetch the latest release version for you and install it:

```bash
$ curl -sL https://sentry.io/get-cli/ | bash
```


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
$ new-release minor --target_commitish eb6bc2c21ff896f159da74608f0a96330419a3e5
```

## :hammer_and_wrench: How to use - Sentry releases
> **_NOTE:_** Make sure environment variables `SENTRY_AUTH_TOKEN`, `SENTRY_ORG` and `SENTRY_PROJECT` are set. 
You must also have the latest release version tag available as `APP_VERSION`.

Run the following:

```bash
$ sentry-release 
```




## :question: Usage help

For usage help, run:

```bash
$ new-release --help
```


