#!/bin/sh
# -->
APP_NAME="$APPNAME"

if [ -z "APPNAME" ]; then
  echo "Please pass a name for this app as a command-line option" >&2
  exit 1
fi
echo "You are running $APP_NAME as name of your app"
cp  ./examples/settings_override.prod.py /app/${APP_NAME}/settings_override.py
# shift  # drops first parameter
# export APPNAME  # makes it an environment variable
exec "$@"