#!/bin/bash
set -e

DEPLOY_DIR=/home/devops/Documents/deploy/raven

cd "${DEPLOY_DIR}"

exec /home/devops/.pyenv/shims/raven bot
