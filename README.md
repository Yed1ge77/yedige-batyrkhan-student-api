# Yedige Batyrkhan Student API

**Batyrkhan Yedige Yerlanuly · IT2-2302 · Student ID 38419 · IITU**

Spring Boot CRUD API студентов: Java 21, Spring Boot 3.5.16, Gradle Wrapper 8.14.6, PostgreSQL 16.15. Версия приложения 1.0.1; Docker/Git release name: `v1.0-yedige-batyrkhan`. Базовые Docker images закреплены digest, Gradle distribution — SHA-256.

Documentation status: reproducible API demonstration, Russian oral defense and architecture prepared by Yedige Batyrkhan.

CRUD change by Batyrkhan Yedige: transactional Student service, DTO validation, Flyway schema and REST controller; PostgreSQL tests cover create/read/update/delete and errors.

Проверено: 9 тестов main с настоящим PostgreSQL,15 curl-запросов native и15 в Docker, persistence после пересоздания контейнеров без удаления volume, Linux и настоящий Git merge conflict. Docker версии1.0.0→1.0.1, UID/GID10001. GitHub опубликован. **Jenkins: #1 SUCCESS → #2 ожидаемый FAILURE → #3 SUCCESS; #4/#5 baseline SUCCESS; #6 автоматически от SCM — SUCCESS.** Автоматический commit54f3a0e подтверждён SCMTriggerCause и точным SHA. Все обязательные требования закрыты; [полный отчёт](docs/report.md), [матрица](REQUIREMENTS.md). Release tag: [v1.0-yedige-batyrkhan](https://github.com/Yed1ge77/yedige-batyrkhan-student-api/tree/v1.0-yedige-batyrkhan).

## Запуск через Docker Compose

Нужны Docker Engine + Compose и доступ пользователя к daemon. Если текущий shell ещё не видит новую группу docker, выполнять команды через `sg docker -c 'docker compose ...'` либо открыть новый login shell. Порт 8080 занят существующим Jenkins; API публикуется только на `127.0.0.1:8081`. PostgreSQL не публикует порт на хосте.

```bash
cd ~/devops/yedige-batyrkhan-student-api
bash scripts/Yedige_Batyrkhan_init_env.sh
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 120
curl --fail http://127.0.0.1:8081/actuator/health
curl --fail http://127.0.0.1:8081/api/info
python3 scripts/Yedige_Batyrkhan_verify_api.py
docker compose ps
docker compose logs --tail=100 app db
```

Скрипт init_env создаёт `.env` с random password, права 600, существующий файл сохраняет. Можно вместо него скопировать `.env.example` и заменить пароль локально. Не показывайте `docker compose config` без `--quiet`: раскрытая конфигурация содержит пароль. При смене `.env` пароль существующей PostgreSQL автоматически не меняется.

Остановка с сохранением данных:

```bash
docker compose stop
# Или удаление только контейнеров и сети этого проекта, с сохранением named volume:
docker compose down
# Повторный запуск:
docker compose up -d --wait --wait-timeout 120
```

`down -v` удаляет данные и для демонстрации сохранности не применяется. Не выполнять глобальный Docker prune.

Полный контейнерный аудит успешно пройден; повторный запуск занимает 8081, сначала остановить native-демонстрацию:

```bash
bash scripts/Yedige_Batyrkhan_local.sh stop
bash scripts/Yedige_Batyrkhan_verify_docker.sh
```

Аудит реально собирает версии 1.0.0 и 1.0.1 через APP_VERSION, запускает сервисы, выполняет exec/inspect/logs/stop/start, CRUD и пересоздаёт контейнеры без удаления volume. Сохраняет реальные результаты в evidence. Дополнительный Docker alias `v1.0-yedige-batyrkhan-38419` удовлетворяет табличному требованию включить Student ID; основной тег остаётся заданным пользователем. При ошибке скрипт завершается без отметки PASS.

## Локальные тесты и демонстрация без Docker

Это проверенный fallback для Ubuntu 24.04 / WSL2, он не заменяет Docker-часть задания. Пакеты распаковываются в `.tools/`, системные сервисы не изменяются. Bootstrap использует доступные в Ubuntu репозитории patch-версии JDK 21 и PostgreSQL 16; фактически проверенные версии указаны в отчёте.

```bash
bash scripts/Yedige_Batyrkhan_bootstrap_local.sh
bash scripts/Yedige_Batyrkhan_local.sh test
bash scripts/Yedige_Batyrkhan_local.sh start
API_EVIDENCE=Yedige_Batyrkhan_local-final-api-curl.txt python3 scripts/Yedige_Batyrkhan_verify_api.py
# Остановить только локальное приложение:
bash scripts/Yedige_Batyrkhan_local.sh app-stop
# Остановить и native PostgreSQL этого проекта:
bash scripts/Yedige_Batyrkhan_local.sh stop
```

Native PostgreSQL использует 127.0.0.1:55432, каталог `.tools/pgdata`, закрытый Unix socket и пароль `.secrets/test-db-password`. `student_api_test` очищается тестами; `student_api_demo` хранит демонстрационные записи. Никогда не направлять integration tests на рабочую БД.

С установленным JDK 21 и отдельно подготовленной **тестовой** PostgreSQL можно запускать `./gradlew clean test bootJar`, передав DB_URL, DB_USER, DB_PASSWORD через окружение. Обязательное свойство DB_PASSWORD не имеет встроенного пароля. Gradle скачивается Wrapper автоматически; архив проверяется SHA-256. Тесты не пропускаются при недоступной БД и не используют H2.

## API

| Метод | Путь | Успех |
|---|---|---|
| POST | /api/students | 201 + Location |
| GET | /api/students | 200, массив |
| GET | /api/students/{id} | 200 |
| PUT | /api/students/{id} | 200 |
| DELETE | /api/students/{id} | 204, пустое тело |
| GET | /api/info | ФИО, группа, Student ID, университет, версия |
| GET | /actuator/health | 200, UP при доступной БД |

Входные поля: firstName/lastName до 100 символов, email до 254, groupName до 50; все обязательны. Email приводится к lowercase, пробелы по краям удаляются при сохранении; DTO проверяет исходное значение. Email уникален. Ошибки: 400 при невалидных полях/JSON/ID; 404 при отсутствующем студенте; 409 при повторном email. JSON ошибки содержит timestamp, status, error, message, path, fields; пароль и SQL не возвращаются клиенту.

```bash
curl -i -X POST http://127.0.0.1:8081/api/students \
  -H 'Content-Type: application/json' \
  --data '{"firstName":"Batyrkhan","lastName":"Yedige","email":"38419@example.com","groupName":"IT2-2302"}'
curl -i http://127.0.0.1:8081/api/students
# Подставить id из POST, не предполагать, что он равен 1:
curl -i http://127.0.0.1:8081/api/students/1
curl -i -X PUT http://127.0.0.1:8081/api/students/1 \
  -H 'Content-Type: application/json' \
  --data '{"firstName":"Batyrkhan","lastName":"Yedige","email":"38419@example.com","groupName":"IT2-2302-UPDATED"}'
curl -i -X DELETE http://127.0.0.1:8081/api/students/1
curl -i http://127.0.0.1:8081/api/students/999999999
```

Для автоматической демонстрации с фактическим ID и уникальным email используйте verify_api.py.

## Jenkins и GitHub

Имя job: `Yedige_Batyrkhan_Student_API`. Опубликованный репозиторий: `https://github.com/Yed1ge77/yedige-batyrkhan-student-api`. Jenkinsfile: Checkout → Build → Test → Docker Build → Verify, timeout 30 min, публикация JUnit, запрет параллельных запусков job. Build/Test выполняют Gradle Wrapper внутри закреплённого JDK Docker image, поэтому host javac не нужен. Агент должен иметь Docker CLI, доступ к daemon и общий с daemon путь workspace; `agent any` требует подходящий единственный агент либо ограничения job на подготовленный узел. Built-In Node проверен реальными сборками: Java21, Docker29.9.1, доступ к daemon и общий путь workspace подтверждены.

В локальном терминале после выдачи доступов:

```bash
.tools/gh auth login --hostname github.com --git-protocol https
bash scripts/Yedige_Batyrkhan_jenkins_login.sh
# Новый public repository уже создан; старую лабораторную не изменять.
# Push только явно перечисленных веток:
git push -u origin main feature/yedige-batyrkhan-crud feature/yedige-batyrkhan-documentation feature/yedige-batyrkhan-readme-review test/yedige-batyrkhan-ci-failure-repro test/yedige-batyrkhan-ci-recovery
python3 scripts/Yedige_Batyrkhan_configure_jenkins.py
python3 scripts/Yedige_Batyrkhan_jenkins_api.py validate
python3 scripts/Yedige_Batyrkhan_jenkins_api.py build --branch main
# Ожидаемый FAILURE; ненулевой exit code CLI здесь означает ожидаемый провал:
python3 scripts/Yedige_Batyrkhan_jenkins_api.py build --branch test/yedige-batyrkhan-ci-failure-repro
python3 scripts/Yedige_Batyrkhan_jenkins_api.py build --branch test/yedige-batyrkhan-ci-recovery
# Вернуть default main и выполнить baseline перед проверкой polling:
python3 scripts/Yedige_Batyrkhan_jenkins_api.py build --branch main
python3 scripts/Yedige_Batyrkhan_jenkins_api.py status
```

Configure script создаёт только персональный job и Secret text `Yedige_Batyrkhan_CI_DB_PASSWORD`; существующий job/credential сохраняет. Требуются установленные Jenkins Pipeline, Git, Credentials Binding, Plain Credentials, JUnit и Timestamper plugins; доступ и состав plugins подтверждены, см. evidence/Yedige_Batyrkhan_jenkins-plugins.json. Public GitHub checkout не требует token. Секрет тестовой PostgreSQL создаётся случайно в Jenkins Credentials и передаётся через binding; временные контейнеры и сеть имеют уникальное имя по BUILD_NUMBER. Уборка не затрагивает Compose DB.

Polling `* * * * *` регистрируется после первого запуска Jenkinsfile. Для доказательства automation нужен **новый содержательный commit после успешного baseline main**, push и ожидание без build API. Проверить build cause `hudson.triggers.SCMTrigger$SCMTriggerCause`, SHA и Console Output, сохранить polling log. Доказательство получено в build#6: SCMTriggerCause, Changes found и SHA54f3a0e; JSON, Console Output и polling log находятся в evidence/. Definition job закреплён на main, а параметр тестовой ветки применяется в Checkout; это исправило первоначальный No changes. Последовательность: [demo-checklist](docs/demo-checklist.md).

Release tag `v1.0-yedige-batyrkhan` фиксирует итоговое состояние после Docker/Jenkins/SCM проверок. `git show v1.0-yedige-batyrkhan` и `git ls-remote --tags origin` показывают release. Для повторной демонстрации не перемещать этот tag.

## Linux, Git и материалы

```bash
bash scripts/Yedige_Batyrkhan_system_report.sh
ls -l scripts/Yedige_Batyrkhan_system_report.sh
stat -c '%a %n' scripts/Yedige_Batyrkhan_system_report.sh
tail -5 logs/Yedige_Batyrkhan_system_report.log
grep Yedige logs/Yedige_Batyrkhan_system_report.log > Yedige_Batyrkhan_log_analysis.txt
git log --graph --decorate --oneline --all
git branch -a
```

Скрипт имеет права 744: владелец rwx, остальные только r. Git хранит executable bit, но не точный режим 744; после clone при необходимости повторить `chmod 744 scripts/Yedige_Batyrkhan_system_report.sh`. Backup исходного README соответствует первому commit; финальный backup — текущему README на момент итогового аудита. История настоящего конфликта: [evidence](evidence/Yedige_Batyrkhan_git-conflict.txt).

- [REQUIREMENTS.md](REQUIREMENTS.md): каждый пункт DOCX и дополнительные требования.
- [docs/report.md](docs/report.md): реальные результаты и блокеры, Markdown.
- [docs/defense-ru.md](docs/defense-ru.md): объяснение и ответы на все 80 вопросов.
- [docs/architecture.md](docs/architecture.md): Mermaid.
- [docs/demo-checklist.md](docs/demo-checklist.md): последовательность защиты.
- [docs/screenshots.md](docs/screenshots.md): что снять вручную при необходимости.
- [evidence/](evidence/): сырые результаты без секретов.

Не коммитить `.env`, `.secrets`, пароли и credentials; они также исключены из Docker context. Старый проект `yedige_batyrkhan`, его Git-история и Jenkins job не изменялись.
