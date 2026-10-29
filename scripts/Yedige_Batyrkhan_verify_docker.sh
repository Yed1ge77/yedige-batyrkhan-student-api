#!/bin/bash
# Runs only the dedicated midterm Compose project. Requires Docker access.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence
exec > >(tee evidence/Yedige_Batyrkhan_docker-verification.txt) 2>&1
image=yedige-batyrkhan-student-api:v1.0-yedige-batyrkhan
docker info --format 'Docker server={{.ServerVersion}}'
docker compose config --quiet
APP_VERSION=1.0.0 docker compose build
# Capture the first actual image before rebuilding its application version.
docker image inspect "$image" --format 'Initial ID={{.Id}} Created={{.Created}} Size={{.Size}} User={{.Config.User}}'
docker compose up -d --wait --wait-timeout 120
wait_api() {
  for attempt in {1..90}; do
    if curl -fsS http://127.0.0.1:8081/actuator/health >/dev/null 2>&1; then return 0; fi
    sleep 1
  done
  echo 'Application readiness timed out' >&2
  return 1
}
wait_api
curl -fsS http://127.0.0.1:8081/api/info | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["version"] == "1.0.0", d; print(d)'
docker compose ps
docker compose exec -T app sh -c 'id; java -version; pwd'
app_id=$(docker compose ps -q app)
docker inspect "$app_id" --format 'Image={{.Config.Image}} User={{.Config.User}} Ports={{json .NetworkSettings.Ports}} Networks={{json .NetworkSettings.Networks}}'
docker compose logs --tail=80 app db
docker compose stop app
docker compose start app
wait_api
# A real version change: buildInfo version 1.0.0 -> 1.0.1, reflected by /api/info.
APP_VERSION=1.0.1 docker compose build
docker compose up -d --wait --wait-timeout 120
wait_api
curl -fsS http://127.0.0.1:8081/api/info | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["version"] == "1.0.1", d; print(d)'
docker image inspect "$image" --format 'Rebuilt ID={{.Id}} Created={{.Created}} Size={{.Size}} User={{.Config.User}}'
docker tag "$image" yedige-batyrkhan-student-api:v1.0-yedige-batyrkhan-38419
python3 scripts/Yedige_Batyrkhan_verify_api.py
python3 - <<'PY'
import json,subprocess,time,uuid
from pathlib import Path
p={'firstName':'Batyrkhan','lastName':'Yedige','email':'persist.38419.'+uuid.uuid4().hex[:8]+'@example.com','groupName':'IT2-2302'}
raw=subprocess.check_output(['curl','-fsS','-X','POST','http://127.0.0.1:8081/api/students','-H','Content-Type: application/json','--data',json.dumps(p)],text=True)
created=json.loads(raw)
Path('.tools').mkdir(exist_ok=True)
Path('.tools/persistence-record.json').write_text(raw)
Path('evidence/Yedige_Batyrkhan_docker-persistence.txt').write_text('Before restart: '+raw+'\n')
print('Created persistence record:',created)
PY
# down without -v removes only this project's containers/network, preserving the volume.
docker compose down
docker volume inspect yedige-batyrkhan-student-api_student-data --format 'Volume={{.Name}} Mountpoint={{.Mountpoint}}'
docker compose up -d --wait --wait-timeout 120
wait_api
python3 - <<'PY'
import json,subprocess
from pathlib import Path
before=json.loads(Path('.tools/persistence-record.json').read_text())
raw=subprocess.check_output(['curl','-fsS','http://127.0.0.1:8081/api/students/'+str(before['id'])],text=True)
after=json.loads(raw)
assert before==after,(before,after)
with Path('evidence/Yedige_Batyrkhan_docker-persistence.txt').open('a') as f:f.write('After container recreation: '+raw+'\nPASS: identical record from persistent named volume\n')
print('PASS: PostgreSQL record persisted across container recreation:',after)
PY
docker compose ps
echo 'PASS: Docker audit completed; dedicated app and db remain running'
