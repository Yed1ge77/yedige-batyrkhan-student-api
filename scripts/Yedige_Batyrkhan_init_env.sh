#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -e .env ]]; then echo '.env already exists; preserved'; exit 0; fi
umask 077
python3 - <<'PY'
import secrets
from pathlib import Path
Path('.env').write_text('DB_USER=student_api\nDB_PASSWORD='+secrets.token_urlsafe(32)+'\nAPP_PORT=8081\n')
PY
echo '.env created with a random password (not printed)'
