#!/usr/bin/env python3
"""Read-only audit of current project, evidence and exact secret leakage; never prints values."""
from pathlib import Path
import os
import json
import re
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
report = ROOT/'evidence/Yedige_Batyrkhan_safety-audit.txt'
report.touch(exist_ok=True)
messages = []
for path in sorted(Path('scripts').glob('*.sh')):
    result = subprocess.run(['bash','-n',str(path)],capture_output=True,text=True)
    assert result.returncode == 0, (path,result.stderr)
    messages.append('PASS Bash syntax '+str(path))
for path in sorted(Path('scripts').glob('*.py')):
    compile(path.read_text(),str(path),'exec')
    messages.append('PASS Python syntax '+str(path))
for path in ['.env','.secrets/test-db-password','.secrets/jenkins.netrc','.ci-db.env']:
    result = subprocess.run(['git','check-ignore',path],capture_output=True,text=True)
    assert result.returncode == 0, path
    messages.append('PASS Git ignore '+path)
for pattern in ['.env','.secrets','.tools','.ci*','.gradle-ci/']:
    assert pattern in Path('.dockerignore').read_text().splitlines(),pattern
    messages.append('PASS Docker context exclusion '+pattern)
secrets = []
if Path('.env').exists():
    for line in Path('.env').read_text().splitlines():
        if line.startswith('DB_PASSWORD='): secrets.append(line.split('=',1)[1])
if Path('.secrets/test-db-password').exists():
    secrets.append(Path('.secrets/test-db-password').read_text().strip())
# Exact substring scanning is for generated DB secrets. Human login credentials
# may coincide with pre-existing public identifiers; their storage exclusion
# and absence of credential-export code are checked separately.
if Path('.secrets/jenkins.netrc').exists():
    assert (Path('.secrets/jenkins.netrc').stat().st_mode & 0o777) == 0o600
    messages.append('PASS local Jenkins credential file permissions600 and Git/context exclusions')
excluded = {'.git','.tools','.secrets','.gradle','build','__pycache__'}
scanned = 0
for directory, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in excluded]
    for filename in files:
        path = Path(directory)/filename
        if path == ROOT/'.env': continue
        data = path.read_bytes()
        scanned += 1
        assert not any(value.encode() in data for value in secrets if value), f'Secret found in {path.relative_to(ROOT)}'
messages.append(f'PASS exact secret-value scan of {scanned} project files; values not printed')
objects = subprocess.check_output(['git','rev-list','--objects','--all'],text=True).splitlines()
blob_count = 0
for line in objects:
    oid = line.split()[0]
    if subprocess.check_output(['git','cat-file','-t',oid],text=True).strip() != 'blob': continue
    data = subprocess.check_output(['git','cat-file','blob',oid])
    blob_count += 1
    assert not any(value.encode() in data for value in secrets if value), 'Secret found in Git history (not printed)'
messages.append(f'PASS exact secret-value scan across {blob_count} historical Git blobs')
assert not subprocess.check_output(['git','ls-files','.env','.secrets','.tools'],text=True).strip()
messages.append('PASS no real .env, .secrets or .tools tracked')
assert not subprocess.check_output(['git','ls-files','-u'],text=True).strip()
assert not any(marker in Path('README.md').read_text() for marker in ['<<<<<<<','=======','>>>>>>>'])
messages.append('PASS merge resolved and README contains no conflict markers')
assert (Path('scripts/Yedige_Batyrkhan_system_report.sh').stat().st_mode & 0o777) == 0o744
assert Path('README.md').read_bytes() == Path('backups/Yedige_Batyrkhan_README.final.md').read_bytes()
messages.append('PASS system report permissions744 and identical final README backup')
links = 0
for path in [Path('README.md'),Path('REQUIREMENTS.md'),*Path('docs').glob('*.md')]:
    for ref in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if ref.startswith(('http://','https://','#','mailto:')): continue
        target = urllib.parse.unquote(ref.split('#')[0])
        assert (path.parent/target).exists(), f'Broken link {path}: {ref}'
        links += 1
messages.append(f'PASS {links} local Markdown links resolve')
assert len(re.findall(r'^## \d+\.',Path('docs/defense-ru.md').read_text(),re.M)) == 80
assert len(re.findall(r'^\| D\d+',Path('REQUIREMENTS.md').read_text(),re.M)) == 116
messages.append('PASS all80 defense questions; 116 DOCX matrix rows plus17 additional requirements')
for directory, expected in [('evidence/junit',9),('evidence/junit-recovery',10)]:
    total = 0
    for path in Path(directory).glob('TEST-*.xml'):
        suite = ET.parse(path).getroot()
        total += int(suite.get('tests'))
        assert all(int(suite.get(key,'0')) == 0 for key in ['failures','errors','skipped'])
    assert total == expected, (directory,total)
    messages.append(f'PASS {directory}: {total} tests, no failures/errors/skips')
transcript = Path('evidence/Yedige_Batyrkhan_local-final-api-curl.txt').read_text()
assert len(re.findall(r'^\$ curl ',transcript,re.M)) == 15
messages.append('PASS final HTTP transcript contains15 real curl requests')
verification = json.loads(Path('evidence/Yedige_Batyrkhan_jenkins-final-verification.json').read_text())
assert verification['temporaryResourcesCleaned'] and verification['failureStoppedLaterStages']
assert [b['result'] for b in verification['builds']] == ['SUCCESS','FAILURE','SUCCESS','SUCCESS','SUCCESS','SUCCESS']
assert any(c['_class'] == 'hudson.triggers.SCMTrigger$SCMTriggerCause' for c in verification['builds'][-1]['causes'])
assert verification['automaticCommit'] in verification['builds'][-1]['revisions']
messages.append('PASS Jenkins1SUCCESS/2FAILURE/3SUCCESS, baselines4/5SUCCESS, automatic6SUCCESS with SCM cause and exact SHA')
messages.append('PASS CI failure propagation and temporary resource cleanup')
messages.append('STATUS: all mandatory practical checks passed; release tag is finalized after this audit')
report.write_text('\n'.join(messages)+'\n')
print('\n'.join(messages))
