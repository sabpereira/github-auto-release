#!/usr/bin/env bash

# To get sentry-cli:
# curl -sL https://sentry.io/get-cli/ | bash

# Create a release
sentry-cli releases new $APP_VERSION

# Associate commits with the release, if no commits does the latest 20
sentry-cli releases set-commits --auto $APP_VERSION || sentry-cli releases set-commits $APP_VERSION --commit "$REPO"

sentry-cli releases finalize $VERSION