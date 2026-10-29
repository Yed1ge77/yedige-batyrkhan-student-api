# Архитектура

```mermaid
flowchart LR
    Client["curl / преподаватель"] -->|"127.0.0.1:8081 → 8080"| Controller["StudentController + DTO validation"]
    Controller --> Service["StudentService: transactions"]
    Service --> Repository["StudentRepository: JPA"]
    Repository -->|"jdbc:postgresql://db:5432/student_api"| DB[("PostgreSQL 16")]
    Flyway["Flyway V1 schema"] --> DB
    DB --> Volume["student-data named volume"]
    GitHub["GitHub: Yed1ge77 repository"] -->|"SCM polling"| Jenkins["Jenkins personal job"]
    Jenkins --> Checkout[Checkout] --> Build["Build: Gradle Wrapper"] --> Test["Test: temporary PostgreSQL"] --> Docker["Docker Build: JDK → JRE"] --> Verify["Verify image"]
```

Compose project: `yedige-batyrkhan-student-api`. Сервисы app/db используют отдельную сеть student-network. PostgreSQL не публикует порт на хосте; API публикуется только на loopback. Jenkins остаётся на 8080. Runtime приложения работает от UID/GID 10001. Flyway — единственный источник изменения схемы, `ddl-auto=validate` запрещает неявное изменение Hibernate.

Локальные integration tests используют отдельную БД student_api_test на 127.0.0.1:55432. Jenkins создаёт PostgreSQL-контейнер с уникальным именем по BUILD_NUMBER и отдельной сетью без опубликованных портов, затем удаляет только его. Тесты очищают свою таблицу students, поэтому тестовую БД нельзя подменять демонстрационной/рабочей.

Пределы: это учебный API без авторизации, пагинации и внешнего deployment. Секреты передаются через окружение; Docker environment доступен администраторам daemon. Named volume обеспечивает сохранение при restart/recreate, но не заменяет резервное копирование PostgreSQL.
