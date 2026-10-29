# Итоговый отчёт DevOps midterm

**Batyrkhan Yedige Yerlanuly · IT2-2302 · Student ID 38419 · IITU**

Проект: `/home/batyr/devops/yedige-batyrkhan-student-api`.
GitHub: [Yed1ge77/yedige-batyrkhan-student-api](https://github.com/Yed1ge77/yedige-batyrkhan-student-api).
Release: [v1.0-yedige-batyrkhan](https://github.com/Yed1ge77/yedige-batyrkhan-student-api/tree/v1.0-yedige-batyrkhan).
Проверки: 30 октября 2026, Asia/Qyzylorda, UTC+05. В Jenkins Console timestamps могут быть UTC.

**Все обязательные пункты DOCX и дополнительные практические требования пользователя выполнены. Внешних блокеров нет.** Намеренный FAILURE сохранён только в изолированной тестовой ветке; main исправен. Исходная лабораторная не изменялась. Полный аудит: [REQUIREMENTS.md](../REQUIREMENTS.md), [дословная XML-выгрузка всего DOCX с таблицей](../evidence/Yedige_Batyrkhan_assignment.txt).

## Версии и окружение

| Компонент | Фактическая версия |
|---|---|
| OS / kernel | Ubuntu24.04.5 LTS, WSL2, 6.18.54.1-microsoft-standard-WSL2 |
| Пользователь / ресурсы при диагностике | batyr uid1000; 4 CPU; RAM3.7GiB; swap1GiB |
| Git / GitHub CLI | 2.43.0 / 2.103.3; GitHub account Yed1ge77 |
| Java | OpenJDK21.0.12.1; JDK21 в Docker Build/Test |
| Spring Boot / Gradle Wrapper | 3.5.16 / 8.14.6, distribution SHA-256 закреплён |
| PostgreSQL | 16.15; Docker postgres16.15-bookworm закреплён digest |
| Docker / Compose | 29.9.1 / v5.6.0; текущий процесс использует sg docker |
| Jenkins | 2.580.1, 127.0.0.1:8080; аутентифицированный пользователь batyr |
| Приложение | 1.0.1; Docker/Git release name v1.0-yedige-batyrkhan |

Совместимость подтверждена реальными сборками и [Spring Boot requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html). [Официальные Gradle releases](https://gradle.org/releases/) содержат8.14.6. [Registry digests](../evidence/Yedige_Batyrkhan_registry-digests.json), [environment](../evidence/Yedige_Batyrkhan_environment.txt), [Jenkins plugins](../evidence/Yedige_Batyrkhan_jenkins-plugins.json).

## Linux

Структура создана терминалом. Персональный script выводит и сохраняет через tee ФИО, дату, пользователя, OS/kernel, CPU/RAM и диски. Реально запущен из /tmp; права744 проверены через ls/stat. Созданы initial и final backups README, содержимое сверено cmp. Показаны процессы/Java, последние5 строк personal log и syslog, grep по фамилии с сохранением результата. Разница > и >> объяснена в защите.

Доказательства: [дерево](../evidence/Yedige_Batyrkhan_project-tree.txt), [запуск](../evidence/Yedige_Batyrkhan_linux-report-run.txt), [Linux checks](../evidence/Yedige_Batyrkhan_linux-checks.txt), [final checks](../evidence/Yedige_Batyrkhan_final-linux-checks.txt), [analysis](../Yedige_Batyrkhan_log_analysis.txt), [backup](../backups/Yedige_Batyrkhan_README.final.md).

## Spring Boot API и тесты

Student: id, firstName, lastName, email, groupName. Controller/service/repository, DTO request/response, транзакции, валидация и JSON errors. POST201+Location, GET/PUT200, DELETE204, invalid400, missing404, duplicate email409. Персональные info и health endpoints. DB_URL/DB_USER/DB_PASSWORD через environment. Flyway V1 создаёт схему; Hibernate validate проверяет её. Пароля по умолчанию в коде нет.

| Проверка | Результат | Доказательство |
|---|---|---|
| main unit | 3 passed, 0 failures/errors/skips | [JUnit](../evidence/junit/TEST-kz.iitu.yedige.studentapi.StudentServiceTest.xml) |
| main integration с настоящим PostgreSQL | 6 passed, 0 failures/errors/skips | [JUnit](../evidence/junit/TEST-kz.iitu.yedige.studentapi.StudentApiIntegrationTest.xml) |
| native итоговый Gradle | 9/9, BUILD SUCCESSFUL, bootJar1.0.1 | [Gradle](../evidence/Yedige_Batyrkhan_gradle-final-test.txt) |
| native curl | 15/15 HTTP/JSON assertions | [HTTP](../evidence/Yedige_Batyrkhan_local-final-api-curl.txt) |
| Docker curl | 15/15 HTTP/JSON assertions | [HTTP](../evidence/Yedige_Batyrkhan_api-curl.txt) |
| native persistence | Одинаковый row после app+PostgreSQL restart | [evidence](../evidence/Yedige_Batyrkhan_local-persistence.txt) |
| Docker persistence | Одинаковый row после удаления/создания контейнеров без удаления volume | [evidence](../evidence/Yedige_Batyrkhan_docker-persistence.txt) |

Тесты не используют H2 и не пропускаются при недоступной PostgreSQL. Проверены CRUD, validation, malformed JSON/ID, missing get/put/delete, duplicate409, health и ФИО/версия. [Реальная схема и Flyway history](../evidence/Yedige_Batyrkhan_postgres-schema.txt).

Ранняя диагностика выявила установленный JRE без javac; локальный JDK распакован в .tools, [исходный сбой](../evidence/Yedige_Batyrkhan_gradle-missing-jdk.txt) сохранён. Ранний HTTP transcript имел ошибку только в счётчике summary14/15; поправка явно записана, финальный transcript содержит15 реально сохранённых запросов. Это не Jenkins failure demonstration.

## Git и GitHub

Identity подтверждена старой GitHub history и локальным config старого проекта, применена только к новому repo: Batyrkhan Yedige Yerlanuly, 208401081+Yed1ge77@users.noreply.github.com. Первый commit12b2fdc — Initial commit: Batyrkhan Yedige Student API. В CRUD branch сделаны реальные commits реализации, тестов/Wrapper и контейнеризации, затем merge main.

Две персональные documentation branches изменили одну строку README. Получен настоящий CONFLICT, разрешён редактированием с сохранением обоих смыслов, commit70883f4. [Conflict output](../evidence/Yedige_Batyrkhan_git-conflict.txt), [history](../evidence/Yedige_Batyrkhan_git-history.txt).

Новый public repository создан; main, три feature и две test branches опубликованы, [remote refs](../evidence/Yedige_Batyrkhan_github-publication.txt). Annotated release tag v1.0-yedige-batyrkhan создаётся последним шагом финализации после этого аудита; его наличие проверяется непосредственно через git ls-remote и GitHub tag link выше. Force push не выполнялся, пустых commits и AI co-author нет.

## Docker и Compose

Multi-stage JDK→JRE, Gradle build, COPY JAR, EXPOSE8080, USER10001:10001. Base images закреплены digest. Compose app/db, environment, PostgreSQL healthcheck, named volume и отдельная сеть; DB host db вместо localhost. Project yedige-batyrkhan-student-api; DB port не опубликован; API127.0.0.1:8081. .env имеет mode600 и исключён из Git/build context.

Реально собраны версии1.0.0 и1.0.1. Первая image size515970635 bytes, пересобранная515966486 bytes; Jenkins image с дополнительным CI label515966393 bytes. Created/ID и UID выводятся прямо в [Docker audit](../evidence/Yedige_Batyrkhan_docker-verification.txt) и Jenkins Console. Выполнены ps/logs/безопасный inspect/exec id/java/pwd, stop/start, rebuild и полный curl. Основной tag v1.0-yedige-batyrkhan, дополнительный alias v1.0-yedige-batyrkhan-38419.

Запись id3 сохранена после compose down/up без -v, сравнен весь JSON. Native экземпляр до Docker запуска штатно остановлен с сохранением .tools/pgdata. Старые Docker ресурсы не удалялись, prune не использовался. [Финальное состояние](../evidence/Yedige_Batyrkhan_docker-final-state.txt).

## Реальный Jenkins CI

Отдельный job [Yedige_Batyrkhan_Student_API](http://127.0.0.1:8080/job/Yedige_Batyrkhan_Student_API/). Existing security и старая job не менялись. [SCM config](../evidence/Yedige_Batyrkhan_jenkins-job-config.xml), [validator](../evidence/Yedige_Batyrkhan_jenkins-validation.txt), [credential ID без значения](../evidence/Yedige_Batyrkhan_jenkins-auth-and-credential.json).

Checkout → Build → Test → Docker Build → Verify. Docker-capable Built-In Node реально проверен. Gradle Wrapper запускается в JDK container с UID агента. PostgreSQL для тестов — отдельный временный контейнер/сеть каждого BUILD_NUMBER. Jenkins Secret text binding маскируется. Timeout30min, disableConcurrentBuilds, JUnit post always, fail-fast; cleanup удаляет только свои временные ресурсы. Внешний deployment не требовался и не выполнялся.

| Build | Ref / trigger | Итог | Тесты | Console |
|---|---|---|---|---|
| #1 | main, manual | SUCCESS | 9 passed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-1-console.txt) |
| #2 | test/yedige-batyrkhan-ci-failure-repro, manual | FAILURE ожидаемый | 9 passed + 1 failed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-2-console.txt) |
| #3 | test/yedige-batyrkhan-ci-recovery, manual | SUCCESS | 10 passed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-3-console.txt) |
| #4 | main, исходный baseline | SUCCESS | 9 passed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-4-console.txt) |
| #5 | main, baseline исправленного SCM | SUCCESS | 9 passed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-5-console.txt) |
| #6 | main, **SCM polling** | **SUCCESS** | 9 passed | [log](../evidence/Yedige_Batyrkhan_jenkins-build-6-console.txt) |

Контролируемый failure: тест ожидал WRONG-EXPECTED-EMAIL вместо реально нормализованного batyrkhan.yedige@example.com. [Реальная разница failure→fix](../evidence/Yedige_Batyrkhan_ci-failure-fix-diff.txt). Build2 опубликовал JUnit и пропустил Docker Build/Verify; Build3 подтвердил исправление. Main намеренно не ломался.

Polling первоначально не выбирал ветку из переменной ${BRANCH} в сохранённом SCM. Definition закреплён на main, параметр BRANCH разрешается явно в Checkout. Для смены сохранённых SCM выполнен честно обозначенный ручной baseline5; ручные4/5 не засчитываются за automation. [Диагностический No changes](../evidence/Yedige_Batyrkhan_jenkins-scm-parameter-diagnostic.txt), [разбор](ci-observation.md).

**Automation доказан:** новый содержательный commit **54f3a0e7c6505930c51de5217a1dea39a4c60ec1**, git push, затем только GET-наблюдение. Poll log содержит Changes found и этот SHA. Build6 имеет **hudson.triggers.SCMTrigger$SCMTriggerCause**, Started by an SCM change; checkout SHA совпадает; UserIdCause отсутствует. [Polling log](../evidence/Yedige_Batyrkhan_jenkins-scm-polling.txt), [build6 JSON](../evidence/Yedige_Batyrkhan_jenkins-build-6.json), [test summary](../evidence/Yedige_Batyrkhan_jenkins-build-6-tests.json), [итоговые assertions](../evidence/Yedige_Batyrkhan_jenkins-final-verification.json), [история](../evidence/Yedige_Batyrkhan_jenkins-history.json).

## Финальный контроль и материалы

Все116 строк матрицы DOCX и17 дополнительных требований сверены;80 вопросов защиты имеют русские ответы. Ссылки материалов проверены; backups соответствуют README. Generated DB secrets не найдены в публикуемых файлах и Git blobs; human credential хранится только в .secrets, mode600, не экспортируется. CI temporary containers/networks после сборок отсутствуют. [Safety audit](../evidence/Yedige_Batyrkhan_safety-audit.txt).

Работают Compose app1.0.1 на127.0.0.1:8081 и PostgreSQL16.15 с persistent volume. Jenkins8080 и polling остаются активны; после новых commits могут появляться дополнительные штатные SCM builds. Native app/PostgreSQL остановлены, их данные сохранены.

```bash
cd ~/devops/yedige-batyrkhan-student-api
sg docker -c 'docker compose up -d --build --wait --wait-timeout 120'
curl --fail http://127.0.0.1:8081/actuator/health
python3 scripts/Yedige_Batyrkhan_verify_api.py
sg docker -c 'docker compose stop'
```

В новом login shell с группой docker префикс sg не нужен. Не использовать down -v для сохранения данных.

[README](../README.md), [архитектура с Mermaid](architecture.md), [80 ответов защиты](defense-ru.md), [демонстрация](demo-checklist.md), [что снять на screenshots](screenshots.md). Отчёт — Markdown: PDF renderer не установлен, PDF и имитирующие работу screenshots не создавались. PDF/screenshots не являются обязательным форматом DOCX; реальные terminal/API evidence сохранены.
