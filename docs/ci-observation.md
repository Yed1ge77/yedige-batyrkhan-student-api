# Наблюдение реального Jenkins CI — Batyrkhan Yedige

Проверка выполнена на отдельном job Yedige_Batyrkhan_Student_API.

- Build #1: main, SUCCESS, 9 тестов; Checkout/Build/Test/Docker Build/Verify прошли.
- Build #2: test/yedige-batyrkhan-ci-failure-repro, FAILURE, 9 passed + 1 failed. StudentNormalizationTest ожидал WRONG-EXPECTED-EMAIL, хотя Student нормализовал адрес в batyrkhan.yedige@example.com. Docker Build и Verify были пропущены, JUnit опубликован.
- Build #3: test/yedige-batyrkhan-ci-recovery, SUCCESS, 10 тестов. Исправлено ожидаемое значение, поведение приложения не менялось.
- Build #4: main, SUCCESS, 9 тестов; baseline для отдельного эксперимента SCM polling.

В CLI проверки Jenkinsfile исправлено поле multipart: validator принимает текстовый параметр jenkinsfile; file upload с filename возвращал No Jenkinsfile specified. Текущий файл успешно проходит встроенный validator.

Этот содержательный commit добавляет фактические наблюдения, evidence и исправление CLI. После его push следующая проверка выполняется только SCM polling; ручной build API не вызывается. У автоматического build нужно проверить SCMTriggerCause и точный SHA этого commit. Результат эксперимента фиксируется отдельно после завершения.
