pipeline {
    agent any
    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timestamps()
    }
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Personal repository branch to verify')
    }
    triggers { pollSCM('* * * * *') }
    environment {
        IMAGE = 'yedige-batyrkhan-student-api:v1.0-yedige-batyrkhan'
        CI_DB = "yedige-batyrkhan-ci-${BUILD_NUMBER}"
        CI_NETWORK = "yedige-batyrkhan-ci-network-${BUILD_NUMBER}"
        DB_USER = 'student_api'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: params.BRANCH]],
                    userRemoteConfigs: [[url: 'https://github.com/Yed1ge77/yedige-batyrkhan-student-api.git']]])
                echo 'Batyrkhan Yedige Yerlanuly | IT2-2302 | 38419 | IITU'
                sh 'java -version && docker version --format "{{.Server.Version}}" && chmod +x gradlew'
            }
        }
        stage('Build') {
            steps {
                sh 'docker run --rm --name "${CI_DB}-build" -u "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace -e GRADLE_USER_HOME=/workspace/.gradle-ci eclipse-temurin:21-jdk-jammy@sha256:4b1a74fbffbe6b4e7b6f0171a472478282fb463790a51edf10e465d578f22b69 ./gradlew --no-daemon clean assemble'
            }
        }
        stage('Test') {
            steps {
                withCredentials([string(credentialsId: 'Yedige_Batyrkhan_CI_DB_PASSWORD', variable: 'DB_PASSWORD')]) {
                    sh '''#!/bin/bash
set -euo pipefail
set +x
export POSTGRES_PASSWORD="$DB_PASSWORD"
docker network create --label owner=yedige-batyrkhan-student-api "$CI_NETWORK" >/dev/null
docker run -d --name "$CI_DB" --network "$CI_NETWORK" --network-alias db \
  --label owner=yedige-batyrkhan-student-api -e POSTGRES_PASSWORD \
  -e POSTGRES_USER="$DB_USER" -e POSTGRES_DB=student_api_test postgres:16.15-bookworm@sha256:e8a07d2c7579b038938cdba6c539e580e5001caf9ea203d397b5cc83e76bd938 >/dev/null
for attempt in {1..60}; do
  if docker exec "$CI_DB" pg_isready -h 127.0.0.1 -U "$DB_USER" -d student_api_test >/dev/null 2>&1; then break; fi
  sleep 1
done
docker exec "$CI_DB" pg_isready -h 127.0.0.1 -U "$DB_USER" -d student_api_test
docker run --rm --name "${CI_DB}-test" --network "$CI_NETWORK" -u "$(id -u):$(id -g)" \
  -v "$PWD:/workspace" -w /workspace -e GRADLE_USER_HOME=/workspace/.gradle-ci \
  -e DB_PASSWORD -e DB_USER -e DB_URL=jdbc:postgresql://db:5432/student_api_test \
  eclipse-temurin:21-jdk-jammy@sha256:4b1a74fbffbe6b4e7b6f0171a472478282fb463790a51edf10e465d578f22b69 ./gradlew --no-daemon test
'''
                }
            }
            post { always { junit testResults: 'build/test-results/test/*.xml', allowEmptyResults: false } }
        }
        stage('Docker Build') {
            steps { sh 'docker build --label owner=yedige-batyrkhan-student-api -t "$IMAGE" .' }
        }
        stage('Verify') {
            steps {
                sh 'docker image inspect "$IMAGE" --format "Image={{.Id}} Created={{.Created}} Size={{.Size}} User={{.Config.User}}"'
                echo 'Verified personalized image for Batyrkhan Yedige Yerlanuly'
            }
        }
    }
    post {
        always {
            sh '''#!/bin/bash
set -euo pipefail
for container in "${CI_DB}-build" "${CI_DB}-test" "$CI_DB"; do
    if docker container inspect "$container" >/dev/null 2>&1; then
        docker rm -fv "$container" >/dev/null
    fi
done
if docker network inspect "$CI_NETWORK" >/dev/null 2>&1; then
    docker network rm "$CI_NETWORK" >/dev/null
fi
'''
        }
    }
}
