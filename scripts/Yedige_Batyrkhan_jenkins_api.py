#!/usr/bin/env python3
"""Authenticated CLI for this job only. Credentials stay in .secrets/jenkins.netrc."""
import argparse
import base64
import http.cookiejar
import json
import html
import re
import netrc
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = 'http://127.0.0.1:8080'
JOB = '/job/Yedige_Batyrkhan_Student_API'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['status', 'build', 'collect', 'poll-log', 'validate'])
    parser.add_argument('--branch', default='main')
    parser.add_argument('--number', type=int)
    args = parser.parse_args()
    login, _, password = netrc.netrc(str(ROOT / '.secrets/jenkins.netrc')).authenticators('127.0.0.1')
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{login}:{password}'.encode()).decode()}
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def call(path, data=None, content_type=None):
        h = dict(headers)
        if content_type: h['Content-Type'] = content_type
        with opener.open(urllib.request.Request(URL + path, data=data, headers=h), timeout=60) as r:
            return r.read(), dict(r.headers)
    crumb = json.loads(call('/crumbIssuer/api/json')[0])
    headers[crumb['crumbRequestField']] = crumb['crumb']
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    if args.action == 'validate':
        boundary = 'YedigeBatyrkhanPipelineBoundary38419'
        body = ('--'+boundary+'\r\nContent-Disposition: form-data; name="jenkinsfile"\r\nContent-Type: text/plain\r\n\r\n').encode() + (ROOT/'Jenkinsfile').read_bytes() + ('\r\n--'+boundary+'--\r\n').encode()
        result = call('/pipeline-model-converter/validate', body, 'multipart/form-data; boundary='+boundary)[0].decode()
        (evidence/'Yedige_Batyrkhan_jenkins-validation.txt').write_text(result)
        print(result)
        if 'successfully validated' not in result: raise SystemExit(1)
        return
    if args.action == 'status':
        result = call(JOB+'/api/json?tree=name,builds[number,result,building,actions[causes[*]]],lastBuild[number],nextBuildNumber')[0]
        (evidence/'Yedige_Batyrkhan_jenkins-history.json').write_bytes(result)
        print(result.decode())
        return
    if args.action == 'poll-log':
        page = call(JOB+'/scmPollLog/')[0].decode()
        match = re.search(r'<pre[^>]*>(.*?)</pre>', page, re.S)
        if not match: raise SystemExit('Jenkins polling log was not found in the response')
        result = html.unescape(re.sub(r'<[^>]+>', '', match.group(1)))
        (evidence/'Yedige_Batyrkhan_jenkins-scm-polling.txt').write_text(result)
        print(result)
        return
    number = args.number
    if args.action == 'build':
        _, response_headers = call(JOB+'/buildWithParameters', urllib.parse.urlencode({'BRANCH':args.branch}).encode(), 'application/x-www-form-urlencoded')
        location = response_headers.get('Location', '')
        if not location.startswith(URL+'/queue/item/'): raise SystemExit('Unexpected queue location')
        queue_path = location[len(URL):].rstrip('/')+'/api/json'
        print('Queued branch/revision:', args.branch)
        # The CLI yields updates every 10s; no secret-bearing request data is printed.
        deadline=time.monotonic()+1800
        while time.monotonic()<deadline:
            item=json.loads(call(queue_path)[0])
            if item.get('cancelled'): raise SystemExit('Build cancelled')
            if item.get('executable'):
                number=item['executable']['number']; break
            print('Waiting for Jenkins executor...',flush=True);time.sleep(10)
        else: raise SystemExit('Jenkins queue timed out')
    if not number: raise SystemExit('--number is required for collect')
    deadline=time.monotonic()+2100
    while time.monotonic()<deadline:
        result=call(JOB+f'/{number}/api/json')[0];build=json.loads(result)
        if not build['building']:break
        print(f'Build #{number} running...',flush=True);time.sleep(10)
    else:raise SystemExit('Build wait timed out')
    (evidence/f'Yedige_Batyrkhan_jenkins-build-{number}.json').write_bytes(result)
    console=call(JOB+f'/{number}/consoleText')[0]
    # Jenkins masks credential bindings. Additionally redact the exact local API credential.
    console=console.replace(password.encode(), b'***REDACTED***')
    (evidence/f'Yedige_Batyrkhan_jenkins-build-{number}-console.txt').write_bytes(console)
    print(f'Build #{number}: {build["result"]}')
    print('Causes:',json.dumps([a.get('causes') for a in build.get('actions',[]) if 'causes' in a]))
    raise SystemExit(0 if build['result']=='SUCCESS' else 1)


if __name__=='__main__':main()
