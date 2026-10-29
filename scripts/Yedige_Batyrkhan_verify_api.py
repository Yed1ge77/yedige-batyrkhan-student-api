#!/usr/bin/env python3
"""Real curl requests with assertions. Run only against a demonstration database."""
import json
import os
import subprocess
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get('API_URL', 'http://127.0.0.1:8081').rstrip('/')
OUT = ROOT / 'evidence' / os.environ.get('API_EVIDENCE', 'Yedige_Batyrkhan_api-curl.txt')
records = []


def call(method, path, expected, data=None):
    command = ['curl', '--silent', '--show-error', '--max-time', '20', '-i', '-X', method, BASE + path]
    if data is not None:
        command += ['-H', 'Content-Type: application/json', '--data', json.dumps(data)]
    response = subprocess.run(command, capture_output=True, text=True, check=True).stdout
    records.append(f'$ curl -i -X {method} {BASE}{path}' +
                   (' --data ' + json.dumps(data) if data is not None else '') + '\n' + response)
    OUT.write_text('\n\n'.join(records) + '\n')
    headers, _, body = response.partition('\n\n')
    actual = int(headers.splitlines()[0].split()[1])
    assert actual == expected, f'{method} {path}: expected {expected}, got {actual}'
    return json.loads(body) if body.strip() else None


def main():
    records.append('Started: ' + time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    assert call('GET', '/actuator/health', 200)['status'] == 'UP'
    assert call('GET', '/api/info', 200)['student'] == 'Batyrkhan Yedige Yerlanuly'
    student = {'firstName': 'Batyrkhan', 'lastName': 'Yedige',
               'email': f'yedige.38419.{uuid.uuid4().hex[:8]}@example.com', 'groupName': 'IT2-2302'}
    created = call('POST', '/api/students', 201, student)
    student_id = created['id']
    assert any(s['id'] == student_id for s in call('GET', '/api/students', 200))
    assert call('GET', f'/api/students/{student_id}', 200)['lastName'] == 'Yedige'
    call('POST', '/api/students', 409, student)
    student['groupName'] = 'IT2-2302-UPDATED'
    assert call('PUT', f'/api/students/{student_id}', 200, student)['groupName'] == 'IT2-2302-UPDATED'
    invalid = dict(student, firstName='', email='invalid')
    assert 'email' in call('POST', '/api/students', 400, invalid)['fields']
    assert 'firstName' in call('POST', '/api/students', 400, dict(student, firstName='X' * 101))['fields']
    call('DELETE', f'/api/students/{student_id}', 204)
    call('GET', f'/api/students/{student_id}', 404)
    call('GET', '/api/students/999999999', 404)
    call('PUT', '/api/students/999999999', 404, student)
    call('DELETE', '/api/students/999999999', 404)
    call('GET', '/api/students/not-a-number', 400)
    records.append(f'PASS: {len(records) - 1} real curl requests; CRUD, validation, duplicate email, missing student, health and identity')
    OUT.write_text('\n\n'.join(records) + '\n')
    print(records[-1])
    print('Evidence:', OUT)


if __name__ == '__main__':
    main()
