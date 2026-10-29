#!/bin/bash
# Optional native fallback: unpack Ubuntu packages inside this project, without sudo.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .tools/jdk .tools/postgres
if [[ ! -x .tools/jdk/root/usr/lib/jvm/java-21-openjdk-amd64/bin/javac ]]; then
  (cd .tools/jdk
   apt download openjdk-21-jdk-headless openjdk-21-jre-headless
   for package in ./*.deb; do dpkg-deb -x "$package" root; done)
fi
if [[ ! -x .tools/postgres/root/usr/lib/postgresql/16/bin/postgres ]]; then
  (cd .tools/postgres
   apt download postgresql-16 postgresql-client-16 libpq5
   for package in ./*.deb; do dpkg-deb -x "$package" root; done)
fi
.tools/jdk/root/usr/lib/jvm/java-21-openjdk-amd64/bin/javac -version
.tools/postgres/root/usr/lib/postgresql/16/bin/postgres --version
echo 'Local tools ready. Exact tested versions are listed in docs/report.md.'
