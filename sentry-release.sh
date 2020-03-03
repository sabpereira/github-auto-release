#!/usr/bin/env bash

# To get sentry-cli:
# curl -sL https://sentry.io/get-cli/ | bash

# Create a release
sentry-cli releases new $SENTRY_PROJECT@$APP_VERSION

# Automatically associate commits with the release
sentry-cli releases set-commits --auto $SENTRY_PROJECT@$APP_VERSION

sentry-cli releases finalize $SENTRY_PROJECT@$APP_VERSION