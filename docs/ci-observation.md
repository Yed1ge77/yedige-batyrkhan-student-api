# Наблюдение реального Jenkins CI — Batyrkhan Yedige

Проверка выполнена на отдельном job Yedige_Batyrkhan_Student_API.

- Build #1: main, SUCCESS, 9 тестов; Checkout/Build/Test/Docker Build/Verify прошли.
- Build #2: test/yedige-batyrkhan-ci-failure-repro, FAILURE, 9 passed + 1 failed. StudentNormalizationTest ожидал WRONG-EXPECTED-EMAIL, хотя Student нормализовал адрес в batyrkhan.yedige@example.com. Docker Build и Verify были пропущены, JUnit опубликован.
- Build #3: test/yedige-batyrkhan-ci-recovery, SUCCESS, 10 тестов. Исправлено ожидаемое значение, поведение приложения не менялось.
- Build #4: main, SUCCESS, 9 тестов; baseline для отдельного эксперимента SCM polling.

В CLI проверки Jenkinsfile исправлено поле multipart: validator принимает текстовый параметр jenkinsfile; file upload с filename возвращал No Jenkinsfile specified. Текущий файл успешно проходит встроенный validator.

Этот содержательный commit добавляет фактические наблюдения, evidence и исправление CLI. После его push следующая проверка выполняется только SCM polling; ручной build API не вызывается. У автоматического build нужно проверить SCMTriggerCause и точный SHA этого commit. Результат эксперимента фиксируется отдельно после завершения.

Polling диагностика: переменная ${BRANCH} в SCM definition возвращала No changes при новом remote main. Job definition закреплён на main; тестовая ветка выбирается явно параметром в Checkout Jenkinsfile. Это делает SCM polling однозначным и сохраняет повторяемость failure/recovery через BRANCH. Исправление проверяется автоматическим запуском, без build API.

Build #5: ручной baseline исправленного main, SUCCESS, 9 тестов. Для Pipeline job poller использовал SCM-снимки последнего выполненного Pipeline, поэтому одного изменения config.xml было недостаточно. После запуска исправленного Jenkinsfile сохранены конкретные SCM branches вместо ${BRANCH}. Следующий commit добавляет этот фактический разбор и исправленный сбор polling log через /scmPollLog/; опубликованный HTML не сохраняется, извлекается только текст лога.

После push данного commit build API не вызывается; следующий запуск должен иметь SCMTriggerCause и SHA этого изменения. Ручные builds #4 и #5 не являются доказательством automation.

Итог: build #6 автоматически стартовал от SCM change и завершился SUCCESS,9 tests passed. SHA 54f3a0e7c6505930c51de5217a1dea39a4c60ec1; cause SCMTriggerCause, UserIdCause отсутствует. Реальные JSON/Console/Polling evidence сохранены.

Финальный автоматический build #7 выявил отдельную инфраструктурную гонку: Unix-socket pg_isready мог увидеть временный init-сервер official PostgreSQL image, который затем останавливался перед запуском основного сервера. Gradle Test ещё не начался, JUnit отсутствовал, Docker Build/Verify пропущены. Readiness в CI и Compose изменена на TCP127.0.0.1: временный init-сервер слушает только Unix socket, поэтому проверка ждёт основной TCP server. Этот незапланированный сбой не заменяет контролируемый test failure #2. Логи #7 сохранены отдельно; исправление проверяет следующий автоматический SCM build.
