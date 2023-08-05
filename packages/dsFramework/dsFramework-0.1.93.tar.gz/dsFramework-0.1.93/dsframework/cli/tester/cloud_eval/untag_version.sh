#!/bin/sh
set -e

if [ "$1" != "" ]; then
  VERSION="$1"
else
  echo Please provide a version name
  exit 9
fi

git tag -d "${VERSION}"
git config --global push.default current
git push --delete origin "${VERSION}"
