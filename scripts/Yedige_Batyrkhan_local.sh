#!/bin/bash
# Optional native demonstration; Docker validation remains a separate requirement.
set -euo pipefail
cd "$(dirname "$0")/.."
export JAVA_HOME="$PWD/.tools/jdk/root/usr/lib/jvm/java-21-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$PWD/.tools/postgres/root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
pgbin="$PWD/.tools/postgres/root/usr/lib/postgresql/16/bin"
pgsocket="$PWD/.tools/pgsocket"
mkdir -p .secrets .tools/pgsocket evidence
chmod 700 .secrets .tools/pgsocket
start_db() {
  if [[ ! -e .secrets/test-db-password ]]; then
    (umask 077; python3 -c 'import secrets; print(secrets.token_urlsafe(24))' > .secrets/test-db-password)
  fi
  if [[ ! -e .tools/pgdata/PG_VERSION ]]; then
    "$pgbin/initdb" -D "$PWD/.tools/pgdata" -L "$PWD/.tools/postgres/root/usr/share/postgresql/16" \
      --username=student_api --pwfile=.secrets/test-db-password --auth-host=scram-sha-256 --auth-local=trust
  fi
  if ! "$pgbin/pg_ctl" -D .tools/pgdata status >/dev/null 2>&1; then
    "$pgbin/pg_ctl" -D .tools/pgdata -l "$PWD/.tools/postgres/server.log" -o "-h 127.0.0.1 -p 55432 -k $pgsocket" start
  fi
}
stop_app() {
  python3 - <<'PY'
import os,signal,time
from pathlib import Path
p=Path('.tools/app.pid')
if p.exists():
    pid=int(p.read_text()); proc=Path('/proc')/str(pid)
    if proc.exists():
        command=(proc/'cmdline').read_bytes()
        if b'student-api.jar' not in command or (proc/'cwd').resolve()!=Path.cwd():
            raise SystemExit('PID does not match this project; refused to stop')
        os.kill(pid,signal.SIGTERM)
        for _ in range(100):
            if not proc.exists() or (proc/'stat').read_text().split()[2]=='Z': break
            time.sleep(.1)
        else: raise SystemExit('Application did not stop within 10 seconds')
    p.unlink()
PY
}
case "${1:-help}" in
  db-start) start_db ;;
  test)
    start_db
    export DB_USER=student_api DB_URL=jdbc:postgresql://127.0.0.1:55432/student_api_test
    export DB_PASSWORD="$(cat .secrets/test-db-password)"
    # CREATE DATABASE is safe to retry after checking the catalog.
    export PGPASSWORD="$DB_PASSWORD"
    if [[ $("$pgbin/psql" -h 127.0.0.1 -p 55432 -U student_api -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='student_api_test'") != 1 ]]; then
      "$pgbin/createdb" -h 127.0.0.1 -p 55432 -U student_api student_api_test
    fi
    ./gradlew clean test bootJar
    ;;
  start)
    start_db
    export PGPASSWORD="$(cat .secrets/test-db-password)"
    if [[ $("$pgbin/psql" -h 127.0.0.1 -p 55432 -U student_api -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='student_api_demo'") != 1 ]]; then
      "$pgbin/createdb" -h 127.0.0.1 -p 55432 -U student_api student_api_demo
    fi
    stop_app
    python3 - <<'PY'
import os,subprocess
from pathlib import Path
if not Path('build/libs/student-api.jar').exists(): raise SystemExit('Run local.sh test first to build the JAR')
env=dict(os.environ,DB_URL='jdbc:postgresql://127.0.0.1:55432/student_api_demo',DB_USER='student_api',DB_PASSWORD=Path('.secrets/test-db-password').read_text().strip(),SERVER_PORT='8081')
with open('evidence/Yedige_Batyrkhan_local-app.log','a') as f:
    p=subprocess.Popen([str(Path(os.environ['JAVA_HOME'])/'bin/java'),'-Xmx256m','-jar','build/libs/student-api.jar'],env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
Path('.tools/app.pid').write_text(str(p.pid))
PY
    for attempt in {1..60}; do
      if curl -fsS http://127.0.0.1:8081/actuator/health >/dev/null 2>&1; then
        curl -fsS http://127.0.0.1:8081/api/info; printf '\n'; exit 0
      fi
      sleep 1
    done
    echo 'Application readiness timeout; see evidence/Yedige_Batyrkhan_local-app.log' >&2; exit 1
    ;;
  stop)
    stop_app
    if "$pgbin/pg_ctl" -D .tools/pgdata status >/dev/null 2>&1; then
      "$pgbin/pg_ctl" -D .tools/pgdata -m fast stop
    else
      echo 'Native PostgreSQL already stopped; data preserved'
    fi
    ;;
  app-stop) stop_app ;;
  *) echo 'Usage: local.sh db-start|test|start|app-stop|stop'; exit 2 ;;
esac
