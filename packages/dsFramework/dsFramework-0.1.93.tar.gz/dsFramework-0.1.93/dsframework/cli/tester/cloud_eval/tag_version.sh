#!/bin/sh
set -e

if [ "$1" != "" ]; then
  VERSION="$1"
else
  echo Please provide a version name
  exit 9
fi

if [ "$2" != "" ]; then
  DESCRIPTION="$2"
else
  DESCRIPTION="version ${VERSION}"
fi

# create and push git tag (git rev-parse <version> returns SHA1 hashes, if the version exists)
if git rev-parse $VERSION >/dev/null 2>&1
then
    echo "Found tag"
else
    echo "Tag not found, creating and pushing git tag "${VERSION}"..."
    git tag -a "${VERSION}" -m "${DESCRIPTION}"
    git config --global push.default current
    git push --follow-tags origin
fi

