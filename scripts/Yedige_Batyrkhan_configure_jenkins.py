#!/usr/bin/env python3
"""Create only this project's credential/job using an authenticated Jenkins API."""
import base64
import json
import http.cookiejar
import netrc
import secrets
import urllib.parse
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
URL = 'http://127.0.0.1:8080'
JOB = 'Yedige_Batyrkhan_Student_API'
CREDENTIAL_ID = 'Yedige_Batyrkhan_CI_DB_PASSWORD'


def main():
    login, _, password = netrc.netrc(str(ROOT / '.secrets/jenkins.netrc')).authenticators('127.0.0.1')
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{login}:{password}'.encode()).decode()}
    def request(path, data=None, content_type=None):
        h = dict(headers)
        if content_type:
            h['Content-Type'] = content_type
        with opener.open(urllib.request.Request(URL + path, data=data, headers=h), timeout=60) as response:
            return response.read()
    crumb = json.loads(request('/crumbIssuer/api/json'))
    headers[crumb['crumbRequestField']] = crumb['crumb']
    # Preserve existing project credentials if re-running. Never print or export credential values.
    creds = json.loads(request('/credentials/store/system/domain/_/api/json?tree=credentials[id]'))
    if not any(c['id'] == CREDENTIAL_ID for c in creds.get('credentials', [])):
        payload = {'credentials': {'scope': 'GLOBAL', 'id': CREDENTIAL_ID,
            'description': 'Temporary PostgreSQL tests for Yedige Batyrkhan Student API only',
            'secret': secrets.token_urlsafe(32), '$class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl'}}
        request('/credentials/store/system/domain/_/createCredentials',
                urllib.parse.urlencode({'json': json.dumps(payload)}).encode(), 'application/x-www-form-urlencoded')
        print('Created project Secret text credential')
    root = ET.Element('flow-definition', {'plugin': 'workflow-job'})
    ET.SubElement(root, 'description').text = 'Batyrkhan Yedige Yerlanuly | IT2-2302 | 38419 | IITU. Dedicated midterm job.'
    ET.SubElement(root, 'keepDependencies').text = 'false'
    props = ET.SubElement(root, 'properties')
    params = ET.SubElement(ET.SubElement(props, 'hudson.model.ParametersDefinitionProperty'), 'parameterDefinitions')
    param = ET.SubElement(params, 'hudson.model.StringParameterDefinition')
    ET.SubElement(param, 'name').text = 'BRANCH'
    ET.SubElement(param, 'defaultValue').text = 'main'
    ET.SubElement(param, 'trim').text = 'true'
    definition = ET.SubElement(root, 'definition', {'class': 'org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition', 'plugin': 'workflow-cps'})
    scm = ET.SubElement(definition, 'scm', {'class': 'hudson.plugins.git.GitSCM', 'plugin': 'git'})
    ET.SubElement(scm, 'configVersion').text = '2'
    remote = ET.SubElement(ET.SubElement(scm, 'userRemoteConfigs'), 'hudson.plugins.git.UserRemoteConfig')
    ET.SubElement(remote, 'url').text = 'https://github.com/Yed1ge77/yedige-batyrkhan-student-api.git'
    branch = ET.SubElement(ET.SubElement(scm, 'branches'), 'hudson.plugins.git.BranchSpec')
    ET.SubElement(branch, 'name').text = '${BRANCH}'
    ET.SubElement(scm, 'doGenerateSubmoduleConfigurations').text = 'false'
    ET.SubElement(scm, 'submoduleCfg', {'class': 'empty-list'})
    ET.SubElement(scm, 'extensions')
    ET.SubElement(definition, 'scriptPath').text = 'Jenkinsfile'
    ET.SubElement(definition, 'lightweight').text = 'false'
    ET.SubElement(root, 'disabled').text = 'false'
    # Refuse to overwrite an existing job: modification must be deliberate.
    jobs = json.loads(request('/api/json?tree=jobs[name]'))
    if any(j['name'] == JOB for j in jobs['jobs']):
        print('Project job already exists; preserved')
    else:
        request('/createItem?name=' + JOB, ET.tostring(root, encoding='utf-8'), 'application/xml')
        print('Created ' + URL + '/job/' + JOB + '/')


if __name__ == '__main__':
    main()
