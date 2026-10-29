# Фактический отчёт по DevOps midterm

**Batyrkhan Yedige Yerlanuly · IT2-2302 · Student ID 38419 · IITU**

Папка: `/home/batyr/devops/yedige-batyrkhan-student-api`. Проверки выполнены 30 октября 2026, локальное время Asia/Qyzylorda (UTC+05). Главный источник — полный DOCX, включая таблицу; [извлечённый текст](../evidence/Yedige_Batyrkhan_assignment.txt). Все пункты: [REQUIREMENTS.md](../REQUIREMENTS.md).

**Остаётся обязательная Jenkins-часть: необходима локальная авторизация.** Docker build/runtime и GitHub publication теперь реально выполнены. Native-экземпляр штатно остановлен с сохранением данных, порт8081 передан контейнерному приложению. Jenkins builds и auto trigger пока не выполнялись.

## Проверенное окружение

| Компонент | Фактическая версия / состояние |
|---|---|
| OS | Ubuntu 24.04.5 LTS, WSL2 |
| Kernel | 6.18.54.1-microsoft-standard-WSL2 |
| Пользователь | batyr, uid1000 |
| Ресурсы | 4 CPU; RAM 3.7 GiB; swap1 GiB; доступно около951 GiB на rootfs при первом замере |
| Git | 2.43.0 |
| OpenJDK | 21.0.12.1, runtime системный, полный JDK распакован в .tools |
| Gradle | Wrapper 8.14.6; distribution SHA-256 закреплён |
| Spring Boot | 3.5.16; dependency-management plugin1.1.7 |
| Native PostgreSQL | 16.15 (Ubuntu16.15-0ubuntu0.24.04.1) |
| Docker CLI | 29.9.1; daemon доступен через sg docker, новая группа batyr подтверждена |
| Compose | v5.6.0 |
| Jenkins | 2.580.1, systemd active, 127.0.0.1:8080; anonymous API403 |
| GitHub CLI | 2.103.3 в .tools; авторизован Yed1ge77 |

Версии совместимы: [Spring Boot 3.5 system requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html) допускает Java21 и Gradle8.x; [официальные Gradle releases](https://gradle.org/releases/) содержат 8.14.6. Boot artifact3.5.16 проверен через Maven Central и успешно собран. Docker base images закреплены реальными registry digests, см. [registry API evidence](../evidence/Yedige_Batyrkhan_registry-digests.json). Образы затем реально собраны и запущены; результат приведён ниже.

Подробная диагностика: [environment](../evidence/Yedige_Batyrkhan_environment.txt), [access blockers](../evidence/Yedige_Batyrkhan_access-blockers.txt).

## Linux

Создана требуемая структура, персональный Bash script и log. Скрипт использует путь от BASH_SOURCE, работает из `/tmp`, выводит ФИО, дату, пользователя, OS/kernel, CPU/RAM, диски и свободное место в stdout и log через tee. Проверены права **744**, initial и final README backups, `cmp`, процессы и Java Jenkins, последние5 строк personal log и syslog, поиск фамилии.

Доказательства: [дерево](../evidence/Yedige_Batyrkhan_project-tree.txt), [реальный запуск](../evidence/Yedige_Batyrkhan_linux-report-run.txt), [первичные проверки](../evidence/Yedige_Batyrkhan_linux-checks.txt), [финальные проверки](../evidence/Yedige_Batyrkhan_final-linux-checks.txt), [результат поиска](../Yedige_Batyrkhan_log_analysis.txt), [backups](../backups/).

## Приложение и тесты

Реализованы Student, request/response DTO, controller/service/repository, транзакции, валидация, JSON errors, уникальность email, info с ФИО/версией и health. БД настраивается DB_URL/DB_USER/DB_PASSWORD. Flyway V1 создаёт таблицу; Hibernate `validate` проверяет схему. Код не содержит пароля по умолчанию.

Первый запуск Gradle выявил установленный JRE без javac: [реальный сбой](../evidence/Yedige_Batyrkhan_gradle-missing-jdk.txt). Полный JDK распакован локально из Ubuntu packages, без sudo и изменения старых сервисов. После исправления сборка успешна.

| Проверка | Фактический результат | Доказательство |
|---|---|---|
| main unit tests | 3 passed, 0 skipped/failures/errors | [JUnit](../evidence/junit/TEST-kz.iitu.yedige.studentapi.StudentServiceTest.xml) |
| main PostgreSQL integration tests | 6 passed, 0 skipped/failures/errors | [JUnit](../evidence/junit/TEST-kz.iitu.yedige.studentapi.StudentApiIntegrationTest.xml) |
| Итоговая сборка версии1.0.1 | BUILD SUCCESSFUL, 9/9 tests, bootJar; 34s | [Gradle output](../evidence/Yedige_Batyrkhan_gradle-final-test.txt) |
| curl API | 15 реальных запросов, HTTP/JSON assertions passed | [полные запросы и ответы](../evidence/Yedige_Batyrkhan_local-final-api-curl.txt) |
| Native persistence | Одинаковая запись id5 до/после остановки и запуска app+PostgreSQL | [результат](../evidence/Yedige_Batyrkhan_local-persistence.txt) |
| Схема PostgreSQL | Реальная таблица/unique/Flyway history | [schema](../evidence/Yedige_Batyrkhan_postgres-schema.txt) |

curl проверяет health/info, создание с Batyrkhan Yedige, list/get, повтор email409, update, пустые/невалидные поля400, длину firstName400, delete204, get удалённого404, get/put/delete отсутствующего404 и нечисловой ID400. Скрипт использует полученный ID и уникальный email. Ранний transcript имел ошибку только в счётчике summary (14 запросов вместо15); к нему добавлена явная поправка, финальный transcript содержит15 и считает их программно. Исходные HTTP responses не подделывались.

## Git

Identity подтверждена через GitHub commit history старой лабораторной и её локальную конфигурацию: `Batyrkhan Yedige Yerlanuly <208401081+Yed1ge77@users.noreply.github.com>`. Применена только локально в новом repo. История создавалась по мере разработки:

- `12b2fdc`: Initial commit: Batyrkhan Yedige Student API.
- `1cf95cc`, `9eaa2ee`, `63b3d98`: реальные CRUD, PostgreSQL tests/Wrapper и Docker/Jenkins изменения на персональной CRUD branch.
- Две documentation branches реально изменили одну строку; git merge вернул CONFLICT. Разрешение редактированием объединило смысл, commit `70883f4`.

[Реальная история и ветки](../evidence/Yedige_Batyrkhan_git-history.txt), [вывод конфликта и маркеры](../evidence/Yedige_Batyrkhan_git-conflict.txt). Источник истины — Git objects и `git log`, текст отчёта лишь поясняет их.

GitHub: [Yed1ge77/yedige-batyrkhan-student-api](https://github.com/Yed1ge77/yedige-batyrkhan-student-api), public repository создан. Origin настроен; main, три feature-ветки и две test-ветки отправлены. [API и remote refs](../evidence/Yedige_Batyrkhan_github-publication.txt). Release tag ещё отсутствует: создаётся после Jenkins и SCM проверки.

## Docker

Написаны multi-stage Dockerfile JDK→JRE, UID10001, .dockerignore, Compose app/db, env, отдельная сеть, named volume, pg_isready, персональный project. `docker compose config --quiet` проходит; [безопасная выборка конфигурации](../evidence/Yedige_Batyrkhan_compose-safe-config.json) не содержит DB_PASSWORD. Настоящий .env имеет mode600 и исключён из Git/context.

Полный [контейнерный аудит](../scripts/Yedige_Batyrkhan_verify_docker.sh) **успешно выполнен через sg docker**: [сырой вывод сборок и всех операций](../evidence/Yedige_Batyrkhan_docker-verification.txt). Первоначальный отказ доступа сохранён отдельно, не выдаётся за текущий результат.

| Проверка | Реальный результат |
|---|---|
| Первая сборка | Версия1.0.0, image1dc83756b87a, размер515970635 bytes, created2026-10-30T02:21:13+05 |
| Пересборка версии | Версия1.0.1, image3e9e2b0a10da, размер515966486 bytes, created2026-10-30T02:22:38+05 |
| Runtime | UID/GID10001:10001; Java21; app работает на8080, опубликован127.0.0.1:8081 |
| Compose | app работает, PostgreSQL16.15 healthy, отдельная сеть и named volume |
| Управление | ps, app/db logs, безопасный inspect, exec id/java/pwd, stop/start app выполнены |
| API | 15/15 curl проверок в контейнерном приложении, [HTTP evidence](../evidence/Yedige_Batyrkhan_api-curl.txt) |
| Persistence | Запись id3 полностью совпала после compose down/up без -v, [доказательство](../evidence/Yedige_Batyrkhan_docker-persistence.txt) |

Создан основной Docker tag v1.0-yedige-batyrkhan и дополнительный alias v1.0-yedige-batyrkhan-38419. Пароли не печатались; inspect выбирал только несекретные поля. Native data сохранены в .tools/pgdata и не смешивались с Docker volume.

## Jenkins и контролируемый сбой

Существующий Jenkins работает на8080. Его конфигурация и старый job не менялись. Написаны Jenkinsfile и API CLI для отдельного job, credentials, validation, build/collect и polling log. Pipeline содержит Checkout → Build → Test → Docker Build → Verify, timeout30min, junit post, fail-fast и уборку только персональных временных контейнеров/сети. Polling задан раз в минуту.

Тестовая branch isolation подготовлена и **проверена локально**:

| Ref | Результат native Gradle |
|---|---|
| test/yedige-batyrkhan-ci-failure-repro, commit3d25172 | 1 failed normalization test: WRONG-EXPECTED-EMAIL вместо реально нормализованного email; BUILD FAILED |
| test/yedige-batyrkhan-ci-recovery, commite1bfd8b | Исправлен ожидаемый email; полный suite10/10 passed |
| main | Намеренный сбой не включался; 9/9 passed |

[Failure log](../evidence/Yedige_Batyrkhan_controlled-local-failure.txt), [recovery log](../evidence/Yedige_Batyrkhan_controlled-local-recovery.txt), [recovery JUnit](../evidence/junit-recovery/).

**Jenkins job ещё не создан. Build numbers и результаты Jenkins отсутствуют. Auto SCM build не выполнен и не доказан.** Наличие pollSCM в файле не является доказательством зарегистрированного trigger. После доступа нужны реальный success/failure/recovery, main baseline, содержательный commit+push и запуск без build API с cause `hudson.triggers.SCMTrigger$SCMTriggerCause` и новым SHA. [Точный сценарий](demo-checklist.md).

## Внешние блокеры и локальные действия владельца

Docker/GitHub блокеры устранены. Осталось выполнить в вашем локальном терминале:

```bash
cd ~/devops/yedige-batyrkhan-student-api
bash scripts/Yedige_Batyrkhan_jenkins_login.sh
```

Скрипт принимает Jenkins username и скрыто пароль/API token, сохраняет .secrets/jenkins.netrc с mode600 и проверяет whoAmI. Ожидается authenticated:true. Секреты в чат не отправлять. Затем можно создать только персональный job/credential, проверить agent и выполнить SUCCESS → FAILURE → SUCCESS и polling. Текущий процесс использует sg docker, поскольку его первоначальный список групп не обновился.

Полный перечень команд после доступа — README. После реальных Docker/Jenkins/SCM результатов необходимо обновить этот отчёт и матрицу, затем создать и push release tag.

## Что осталось запущено

На момент аудита работают **два новых Compose-контейнера**: app1.0.1 на127.0.0.1:8081 и PostgreSQL16.15 с persistent named volume. Native app и native PostgreSQL штатно остановлены; данные .tools/pgdata сохранены. Существующий Jenkins на8080 и прежняя лабораторная не изменялись.

Запуск: `sg docker -c 'docker compose up -d --build --wait --wait-timeout 120'`. Проверка: `python3 scripts/Yedige_Batyrkhan_verify_api.py`. Остановка: `sg docker -c 'docker compose stop'` либо `down` без -v. В новом login shell с группой docker префикс sg не нужен.

Отчёт подготовлен в Markdown. Надёжный PDF renderer в окружении не найден; PDF не создавался. [Список реальных screenshots](screenshots.md) подготовлен, имитации не создавались. [Русская защита со всеми80 ответами](defense-ru.md), [архитектура](architecture.md).
