import logging
import openai
import time
import asyncio
import psycopg2
from sqlalchemy.engine.url import make_url
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from config import TELEGRAM_TOKEN, OPENAI_API_KEY, DATABASE_URL

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Парсинг DATABASE_URL
db_url = make_url(DATABASE_URL)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname=db_url.database,
    user=db_url.username,
    password=db_url.password,
    host=db_url.host,
    port=db_url.port
)
cursor = conn.cursor()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправьте мне сообщение, и я отправлю его в OpenAI API.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('/start - начало работы с ботом')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Received message from user: {user_message}")

    # Retry in case of rate limit error
    for attempt in range(3):
        try:
            # Sending message to OpenAI API
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Обновите модель
                prompt=user_message,
                max_tokens=150
            )

            # Getting response from OpenAI API
            ai_response = response.choices[0].text.strip()
            logger.info(f"Response from OpenAI API: {ai_response}")

            # Saving data to the database
            cursor.execute(
                "INSERT INTO user_interactions (user_id, request_text, response_text) VALUES (%s, %s, %s)",
                (user_id, user_message, ai_response)
            )
            conn.commit()
            logger.info(f"Data successfully saved in the database for user {user_id}")

            # Checking if data is indeed saved
            cursor.execute("SELECT * FROM user_interactions WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
            row = cursor.fetchone()
            if row:
                logger.info(f"Last entry for user {user_id}: {row}")
            else:
                logger.error(f"Entry for user {user_id} not found in the database")

            # Sending response to the user
            await update.message.reply_text(ai_response)
            return

        except openai.RateLimitError:
            logger.warning(f"Rate limit exceeded. Attempt {attempt + 1}. Retrying after 10 seconds.")
            if attempt == 2:  # Last attempt
                await update.message.reply_text("Rate limit exceeded. Please try again later.")
                return
            else:
                logger.info(f"Retrying after 10 seconds.")
                time.sleep(10)

        except openai.OpenAIError as e:
            error_message = "Error accessing OpenAI API. Please update your code to use the new API."
            await handle_error(update, error_message, e)

        except psycopg2.Error as e:
            error_message = "Error accessing the database. Please try again later."
            await handle_error(update, error_message, e)

async def handle_error(update: Update, error_message: str, exception: Exception) -> None:
    try:
        await update.message.reply_text(error_message)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю: {e}")
    logger.error(f"Ошибка: {exception}")

def main() -> None:
    # Создание ApplicationBuilder и Application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Создание событийного цикла asyncio и запуск бота
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(application.run_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Программа завершена по запросу пользователя.")
    finally:
        loop.stop()
        loop.run_until_complete(loop.shutdown_asyncgens())
        cursor.close()  # Закрытие курсора
        conn.close()    # Закрытие соединения с базой данных

if __name__ == '__main__':
    main()
