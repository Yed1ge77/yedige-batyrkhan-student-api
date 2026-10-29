# Скриншоты при требовании преподавателя

DOCX допускает терминальную демонстрацию и исходники; отдельного обязательного формата скриншотов не указано. GUI не использовался, изображения работы не создавались. Если преподаватель потребует скриншоты, снять реальные состояния локально, закрыв секреты:

1. Терминал: pwd + дерево проекта + ФИО README.
2. Скрипт отчёта, его реальный вывод, ls -l и stat с 744, backup/cmp.
3. Git graph, ветки и сохранённый настоящий конфликт README; после публикации remote и release tag.
4. Успешный main Gradle run, итоги 9 тестов и JUnit.
5. Docker Compose ps, created/size image, exec id=10001; получать только после реальной проверки.
6. curl POST/GET/PUT/DELETE/404/400; API info с ФИО и версией.
7. Одинаковая запись до и после пересоздания Docker контейнеров без удаления named volume; получать после доступа.
8. Jenkins SUCCESS main, FAILURE Test и исправленный SUCCESS; видны job, номера и stages.
9. Автоматический Jenkins build: Console Output «Started by an SCM change», SHA нового commit и история сборок; получать только после реального polling trigger.

Нельзя снимать `.env`, `.secrets`, раскрытый `docker compose config`, полный Docker inspect environment или Credentials values. Текстовые evidence уже сохранены и не заменяются имитациями скриншотов.
