#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .secrets
chmod 700 .secrets
read -r -p 'Jenkins username: ' username
read -r -s -p 'Jenkins password or API token (local input only): ' credential
printf '\n'
umask 077
printf 'machine 127.0.0.1 login %s password %s\n' "$username" "$credential" > .secrets/jenkins.netrc
unset credential
curl --fail --silent --netrc-file .secrets/jenkins.netrc http://127.0.0.1:8080/whoAmI/api/json
printf '\n'
