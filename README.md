# Telegram Бот с Интеграцией OpenAI

Этот проект представляет собой Telegram бота, который интегрируется с API OpenAI для генерации ответов на сообщения пользователей. Бот сохраняет взаимодействия пользователей в базе данных PostgreSQL.

## Функции

- Интеграция с API OpenAI для генерации ответов.
- Хранение взаимодействий пользователей в базе данных PostgreSQL.
- Асинхронная обработка сообщений пользователей.

## Предварительные требования

- Docker
- Docker Compose


## Структура базы данных

### Таблица `user_interactions`

Таблица `user_interactions` хранит информацию о взаимодействиях пользователей с ботом. Каждое взаимодействие включает в себя запрос пользователя и ответ, полученный от API OpenAI.

#### Структура таблицы

| Столбец       | Тип                         | Правило сортировки | Допустимость NULL | По умолчанию                                  |
|---------------|-----------------------------|--------------------|-------------------|-----------------------------------------------|
| id            | integer                     |                    | not null          | nextval('user_interactions_id_seq'::regclass) |
| user_id       | bigint                      |                    | not null          |                                               |
| request_text  | text                        |                    | not null          |                                               |
| response_text | text                        |                    | not null          |                                               |
| timestamp     | timestamp without time zone |                    |                   | CURRENT_TIMESTAMP                             |

#### Описание столбцов

1. **id**
   - **Тип:** integer
   - **Описание:** Уникальный идентификатор записи. Автоматически генерируется с помощью последовательности `user_interactions_id_seq`.
   - **Допустимость NULL:** нет
   - **По умолчанию:** nextval('user_interactions_id_seq'::regclass)

2. **user_id**
   - **Тип:** bigint
   - **Описание:** Уникальный идентификатор пользователя, отправившего запрос.
   - **Допустимость NULL:** нет
   - **По умолчанию:** нет

3. **request_text**
   - **Тип:** text
   - **Описание:** Текст запроса, отправленного пользователем.
   - **Допустимость NULL:** нет
   - **По умолчанию:** нет

4. **response_text**
   - **Тип:** text
   - **Описание:** Текст ответа, полученного от API OpenAI.
   - **Допустимость NULL:** нет
   - **По умолчанию:** нет

5. **timestamp**
   - **Тип:** timestamp without time zone
   - **Описание:** Время, когда было записано взаимодействие.
   - **Допустимость NULL:** да
   - **По умолчанию:** CURRENT_TIMESTAMP

#### Пример данных

INSERT INTO user_interactions (user_id, request_text, response_text)
VALUES (123456789, 'Как сделать оригами лягушки?', 'Для создания оригами лягушки...');


## Установка
### Клонируйте репозиторий:

- git clone https://github.com/anyviewww/Bot_testovoe.git
- cd your_project

### Создайте файл .env в корневой директории проекта
- cp .env.example .env

### c переменными:
- TELEGRAM_TOKEN=your_telegram_token
- OPENAI_API_KEY=your_openai_api_key
- DATABASE_URL=postgres://tat:123@db:5432/telebot
#### В docker-compose.yml указаны данные для такой базы данных, для своей б.д. измените DATABASE_URL и docker-compose.yml



## Запуск приложения

### Соберите Docker-образ:
- docker-compose build

### Запустите контейнеры:
- docker-compose up

### Остановите контейнеры:
- docker-compose down

