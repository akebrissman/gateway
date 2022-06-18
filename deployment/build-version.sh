#!/bin/bash
# Bash script creating the version number for Docker tagging in Github actions.
BRANCH=$([ "${GITHUB_EVENT_NAME}" = "pull_request" ] && echo "${GITHUB_HEAD_REF}" || echo "${GITHUB_REF#refs/heads/}")
VERSION="$(python setup.py --version)"
if [ "${BRANCH}" = "master" ]
then
  echo "${VERSION}"
else
  echo "${VERSION}-${BRANCH}-${GITHUB_RUN_NUMBER}"
fi