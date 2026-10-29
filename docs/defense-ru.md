# Материалы устной защиты

Batyrkhan Yedige Yerlanuly · IT2-2302 · 38419 · IITU.

Моя работа — Java 21 Spring Boot REST API студентов. Запрос проходит через controller, DTO проверяет данные, service выполняет транзакцию, repository обращается к PostgreSQL. Flyway создаёт схему, Hibernate проверяет её. POST возвращает 201 и Location, GET/PUT — 200, DELETE — 204; ошибки ввода — 400, отсутствие студента — 404, повтор email — 409.

Dockerfile собирает JAR в JDK-стадии, запускает его в JRE от UID 10001. Compose объединяет приложение и db в персональную сеть, данные PostgreSQL хранит named volume. Jenkinsfile получает код, собирает, тестирует с отдельным PostgreSQL, создаёт и проверяет образ. Проверенное выполнение и ещё не выполненные пункты нужно различать по REQUIREMENTS.md и report.md.

Секреты находятся в исключённых .env и .secrets; они не публикуются. Первый запуск показал отсутствие javac при наличии Java Runtime; причина и исправление сохранены в evidence. Это локальная диагностика, её нельзя выдавать за намеренный провал Jenkins.

## 1. What is Docker, and why is it useful in DevOps?

Docker собирает и запускает приложение с зависимостями в изолированных контейнерах. Это делает окружение разработки и CI воспроизводимым.

## 2. What does the git commit command do?

`git commit` записывает подготовленный через `git add` снимок в локальную историю с автором, сообщением и ссылкой на родителя. Он не отправляет код на GitHub.

## 3. What is the purpose of the shebang line #!/bin/bash?

Shebang `#!/bin/bash` сообщает системе, каким интерпретатором запускать исполняемый файл.

## 4. What is a Jenkinsfile?

Jenkinsfile хранит pipeline в репозитории: этапы, команды, credentials bindings, timeout и действия после сборки.

## 5. What is the difference between a Docker image and a Docker container?

Образ — шаблон файловой системы и настроек. Контейнер — экземпляр образа с процессом и собственным изменяемым слоем.

## 6. What is the purpose of the pwd command?

`pwd` показывает абсолютный путь текущего каталога.

## 7. What is Continuous Integration (CI)?

Continuous Integration: изменения регулярно объединяются и автоматически собираются и тестируются. В работе Jenkins проверяет новый commit через SCM polling.

## 8. What is a Git branch, and why do developers use branches?

Ветка — изменяемая ссылка на commit. Она позволяет разрабатывать CRUD отдельно от main и затем объединить изменения.

## 9. What is the difference between RUN and CMD in a Dockerfile?

`RUN` выполняется при сборке образа и создаёт слой; `CMD` задаёт команду или аргументы по умолчанию при запуске контейнера. Здесь запуск Java задан через `ENTRYPOINT`.

## 10. How can you check available disk space in Linux?

`df -h` показывает размер, использование и доступное место файловых систем; `du -sh каталог` — объём каталога.

## 11. What is the difference between Git and GitHub?

Git — локальная распределённая система контроля версий. GitHub — сервис хранения репозиториев и совместной работы.

## 12. What is Docker Compose, and why is it useful for this project?

Compose описывает связанные контейнеры, сеть, volume и настройки в YAML. Здесь он запускает Spring Boot и PostgreSQL одной командой.

## 13. What does the chmod command do?

`chmod` меняет права доступа. `chmod 744` даёт владельцу rwx, группе r и остальным r.

## 14. What is the purpose of the Checkout stage in Jenkins?

Checkout получает выбранную версию исходного кода из репозитория в рабочий каталог агента.

## 15. What is the difference between > and >> in Linux?

`>` создаёт или перезаписывает файл; `>>` создаёт или дописывает в конец. Например `grep Yedige log > result.txt` заменяет прошлый результат, а `date >> result.txt` добавляет строку.

## 16. What is a merge conflict, and why can it happen?

Конфликт возникает, когда Git не может автоматически объединить несовместимые изменения одного участка. Здесь две ветки меняют одну строку README.

## 17. What is a Docker volume, and why is it important for PostgreSQL?

Named volume хранит данные независимо от изменяемого слоя контейнера. PostgreSQL использует его для каталога данных, поэтому пересоздание контейнера сохраняет записи; `down -v` удалит volume.

## 18. What is the difference between Continuous Delivery and Continuous Deployment?

Continuous Delivery автоматически готовит проверенный релиз, но выпуск требует решения человека. Continuous Deployment автоматически выпускает каждое прошедшее проверки изменение.

## 19. How do you make a Bash script executable?

`chmod u+x script.sh` добавляет выполнение владельцу; в задании нужен точный режим `chmod 744 scripts/Yedige_Batyrkhan_system_report.sh`.

## 20. What is the purpose of the FROM instruction in a Dockerfile?

`FROM` задаёт базовый образ и начинает стадию. Здесь JDK нужен для сборки, а JRE — для запуска.

## 21. What is a Jenkins job?

Jenkins job — настроенная задача сборки. Наша отдельная задача называется `Yedige_Batyrkhan_Student_API`.

## 22. What is the difference between git fetch and git pull?

`git fetch` обновляет remote-tracking ссылки без изменения рабочей ветки. `git pull` сначала fetch, затем merge либо rebase по настройке.

## 23. How can you display the last five lines of a log file?

`tail -n 5 logs/Yedige_Batyrkhan_system_report.log`.

## 24. What is a multi-stage Docker build, and what advantage does it provide?

Multi-stage build разделяет сборку и runtime. В финальный образ копируется JAR без Gradle cache и исходников, что уменьшает образ и набор инструментов внутри.

## 25. What is the difference between the working directory, staging area and repository in Git?

Working directory — файлы на диске; staging area — будущий снимок после git add; repository — сохранённые commits и ссылки в .git.

## 26. Why should automated tests run before deploying an application?

Тесты находят регрессии до выпуска. Ошибка должна остановить pipeline, чтобы не продвигать неисправный артефакт.

## 27. What information can the free -h command provide?

`free -h` показывает RAM и swap: total, used, free, shared, buff/cache и available. Available учитывает память, которую ОС может освободить из cache.

## 28. What is the purpose of the WORKDIR instruction in a Dockerfile?

`WORKDIR` задаёт рабочий каталог следующих RUN/COPY и команды запуска; создаёт каталог, если его нет.

## 29. What is the difference between git merge and git rebase?

Merge объединяет истории и может создать merge commit. Rebase переносит commits на новую базу, изменяя их идентификаторы; опубликованную общую историю без согласования не переписывают.

## 30. How can Jenkins retrieve source code from a private GitHub repository?

Нужно сохранить token либо SSH key в Jenkins Credentials и указать credentialsId в SCM. Секрет не записывают в Jenkinsfile. Публичный репозиторий можно читать без credentials.

## 31. What is a Linux process, and how can you list running processes?

Процесс — выполняющаяся программа с PID, памятью и правами пользователя. `ps -ef`, `pgrep -a java`, `top` показывают процессы.

## 32. What is the purpose of the docker build command?

`docker build -t имя:тег .` читает Dockerfile и build context, выполняет стадии и создаёт образ.

## 33. What is the purpose of a .gitignore file?

`.gitignore` исключает подходящие неотслеживаемые файлы из обычного git add. Уже отслеживаемый секрет он не удалит из истории.

## 34. What is the difference between a Jenkins controller and an agent?

Controller хранит конфигурацию и планирует сборки; agent выполняет команды. Docker CLI, daemon access и JDK нужны на исполняющем агенте.

## 35. What is the meaning of the permission mode 755?

755: владелец rwx, группа r-x, остальные r-x. В данной работе требуется 744: группа и остальные могут читать, но не выполнять.

## 36. Why does the Spring Boot container connect to PostgreSQL using the database service name instead of localhost?

`localhost` внутри app означает сам app-контейнер. Имя `db` разрешается Docker DNS в адрес контейнера PostgreSQL в общей сети.

## 37. What does git status display?

`git status` показывает ветку, подготовленные/неподготовленные изменения, неотслеживаемые файлы и состояние слияния.

## 38. What is a Jenkins build trigger, and how can a GitHub webhook trigger a pipeline?

Trigger задаёт условие старта job. Webhook присылает событие GitHub в Jenkins; локальный Jenkins здесь использует polling, периодически проверяя изменения SCM.

## 39. How do you pass arguments to a Bash script?

После имени скрипта: `./script.sh one two`. Внутри `$1`, `$2`, `$#`; `"$@"` сохраняет границы аргументов.

## 40. What is the difference between COPY and ADD in a Dockerfile?

`COPY` копирует файлы из контекста/стадии. `ADD` также умеет распаковывать локальные tar и получать удалённые ресурсы; для обычных файлов предпочтителен COPY.

## 41. What is the difference between docker stop and docker rm?

`docker stop` останавливает процесс, сохраняя контейнер. `docker rm` удаляет контейнер; отдельно подключённый named volume без явной команды остаётся.

## 42. Why should passwords and .env files not be committed to GitHub?

Секреты в истории Git могут попасть к другим людям и сохраняются в старых commits. Их передают через environment/credentials, а .env исключают также из Docker context.

## 43. What happens when a Jenkins pipeline stage fails?

При ненулевом коде обычного sh шага pipeline получает FAILURE и последующие stages пропускаются; post always выполняет уборку и публикацию отчётов. Ошибку нельзя скрывать `|| true`.

## 44. How can you list hidden files in a Linux directory?

`ls -la` показывает скрытые файлы, права и владельцев.

## 45. What is the difference between RUN and CMD in a Dockerfile?

`RUN` работает при docker build, `CMD` — при docker run. Повтор вопроса в исходном документе сохранён.

## 46. How do you resolve a merge conflict in README.md?

Открыть README, осмысленно объединить текст, удалить маркеры `<<<<<<<`, `=======`, `>>>>>>>`, проверить файл, выполнить git add README.md и git commit.

## 47. What is a health check, and how can it help determine whether PostgreSQL is ready?

Healthcheck периодически запускает проверку. `pg_isready` подтверждает, что сервер принимает подключения; Compose service_healthy задерживает старт приложения. Успех pg_isready сам по себе не проверяет CRUD.

## 48. What is the purpose of the git push command?

`git push` отправляет commits и обновляет удалённые ветки/теги в пределах прав пользователя.

## 49. What is the difference between Declarative Pipeline and Scripted Pipeline in Jenkins?

Declarative Pipeline использует `pipeline { stages { ... } }` и стандартную структуру. Scripted Pipeline — Groovy `node { ... }` с более свободным управлением.

## 50. How can you find and terminate a process by its PID?

`pgrep -a java` или `ps -ef` находят PID; `kill -TERM PID` просит завершиться. После проверки владельца и назначения `kill -KILL` используют только как последний шаг.

## 51. What is the purpose of the EXPOSE instruction in a Dockerfile?

`EXPOSE 8080` документирует порт контейнера; он не публикует его на хосте. Для доступа нужен `-p` или Compose ports.

## 52. What are Jenkins Credentials, and why should they be used?

Jenkins Credentials — хранилище секретов с ID и выдачей через binding. Маскирование в логах помогает, но секрет всё равно нельзя echo, передавать Groovy interpolation или публиковать в artifacts.

## 53. What is the difference between an absolute path and a relative path?

Абсолютный путь начинается от `/`; относительный считается от текущего каталога. Скрипт отчёта вычисляет каталог проекта по BASH_SOURCE, поэтому работает из /tmp.

## 54. How can you create and switch to a new Git branch?

`git switch -c feature/yedige-batyrkhan-crud` создаёт ветку и переключается на неё.

## 55. Why does Jenkins need access to a Docker-capable agent to build Docker images?

Для docker build нужны CLI и доступ к daemon. Доступ к Docker socket даёт широкие права, поэтому его предоставляют только доверенному build agent; защиту Jenkins не отключают.

## 56. What is the difference between a Docker network and a Docker volume?

Сеть обеспечивает связь контейнеров и DNS; volume хранит данные. Сеть не заменяет резервную копию БД.

## 57. How can you search for a specific word in a file?

`grep -n 'Yedige' файл` или `rg 'Yedige' файл` ищет совпадения.

## 58. What is the purpose of the git init command?

`git init -b main` создаёт локальный репозиторий и начальную ветку main; commits ещё отсутствуют.

## 59. How can you view the logs of a running Docker container?

`docker compose logs --tail=100 app` или `docker logs имя-контейнера`.

## 60. How can you configure a Jenkins pipeline to stop when automated tests fail?

Выполнять `./gradlew test` обычным sh шагом, не подавлять ненулевой код. JUnit публикуется в post always. Не использовать catchError, превращающий ошибку в успех.

## 61. What is the difference between mkdir and mkdir -p?

`mkdir каталог` создаёт один каталог и ошибается, если родитель отсутствует. `mkdir -p a/b` создаёт цепочку и допускает существующие каталоги.

## 62. What is a Git tag, and how can it be used to identify a project version?

Tag — именованная ссылка на конкретный commit. Annotated tag дополнительно хранит автора, дату и сообщение. Здесь `v1.0-yedige-batyrkhan` создаётся только после итоговых проверок.

## 63. How should database credentials be passed to a Spring Boot container?

Через переменные окружения DB_URL, DB_USER, DB_PASSWORD из локального исключённого .env или хранилища секретов. Не включать пароль в URL, Dockerfile и Git.

## 64. What is the purpose of the Build stage in a Jenkins pipeline?

Build компилирует исходники и собирает JAR через Gradle Wrapper. Отдельный Test проверяет поведение с PostgreSQL.

## 65. What is the difference between cp and mv in Linux?

`cp` копирует, оставляя источник; `mv` перемещает или переименовывает. Для backup README используется cp и сравнение cmp.

## 66. What is the purpose of the git add command?

`git add` переносит текущее содержимое выбранных файлов в staging area для следующего commit.

## 67. What information can you find in the Jenkins console output?

Console Output показывает trigger/cause, выбранный commit, stages, команды, ошибки Gradle, тесты, идентификатор образа и итоговый статус. Секреты там показывать нельзя.

## 68. How do you run a Docker container and map host port 8080 to container port 8080?

`docker run --rm -p 127.0.0.1:8080:8080 image:tag`. Здесь 8080 занят Jenkins, поэтому Compose публикует 8081:8080 и передаёт настройки БД.

## 69. What is Linux, and why is it commonly used in DevOps?

Linux — ядро ОС; Ubuntu — дистрибутив Linux. В DevOps он распространён благодаря серверным инструментам, автоматизации через shell и контейнерам.

## 70. What is the difference between a Git commit and a Git tag?

Commit — снимок проекта и связь с историей; tag — имя конкретного commit для обозначения релиза.

## 71. What is the purpose of the docker-compose.yml file?

Файл описывает сервисы app/db, образы, окружение, published port, зависимость readiness, сеть и persistent volume.

## 72. How can you investigate a failed Gradle build in Jenkins?

Найти первый неуспешный task и корневую причину в Console Output, посмотреть JUnit/Gradle reports, воспроизвести Wrapper с теми же Java и env. Проверить JDK, зависимости, права и БД; при необходимости --stacktrace без вывода секретов.

## 73. How do you create an empty file from the terminal?

`touch файл` создаёт пустой файл, если его нет; `: > файл` также обнуляет уже существующий файл.

## 74. Why should commit messages be meaningful?

Сообщение должно объяснять реальное изменение, чтобы искать регрессии и понимать историю без чтения всей разницы.

## 75. What is the purpose of the Test stage in a Jenkins pipeline?

Test запускает автоматические unit и PostgreSQL integration tests, возвращает ненулевой код при ошибках и создаёт JUnit XML.

## 76. How can you execute a command inside a running Docker container?

`docker compose exec app sh -c 'id; java -version'` выполняет команду в работающем app-контейнере.

## 77. How can you search a log file for your surname and save the results to another file?

`grep 'Yedige' logs/Yedige_Batyrkhan_system_report.log > Yedige_Batyrkhan_log_analysis.txt`. `>` заменяет файл результатом поиска.

## 78. Your local code differs from the code on GitHub. How would you investigate and safely synchronize the changes?

Сначала git status и сохранить работу commit/stash; git fetch origin; сравнить git log --left-right --graph main...origin/main и git diff main..origin/main. Затем осознанно merge/rebase своей ветки, разрешить конфликты, проверить тесты и push без force.

## 79. Your Spring Boot container cannot connect to PostgreSQL. How would you troubleshoot the problem?

Проверить compose ps и logs app/db, pg_isready, DB_URL с host db, одинаковые DB_USER/DB_PASSWORD, общую сеть, readiness и Flyway. Не печатать пароль и не удалять volume: при смене .env существующая БД сама пароль не меняет.

## 80. Your Jenkins pipeline successfully compiles the application but fails during Docker image creation. How would you identify and fix the problem?

Найти ошибку Docker Build: доступ к daemon и права агента, Dockerfile/context, сеть/registry, базовый образ, свободное место и путь JAR. Повторить docker build на том же агенте; менять только новый проект, не делать глобальный prune и не отключать Jenkins security.
