"""
Telegram-бот для RAG системы Cyber Nexus с локальной моделью
"""
import os
import logging
import asyncio
from dotenv import load_dotenv

# ВАЖНО: загружаем .env ДО импорта библиотек, которые используют HF_HOME
load_dotenv()

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from rag_bot_local import RAGBot

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация RAG-бота с локальной моделью
rag_bot = RAGBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот базы знаний Cyber Nexus.\n\n"
        "Задай мне любой вопрос о персонажах, планетах, организациях или технологиях!\n\n"
        "Примеры вопросов:\n"
        "- Who is Xarn Velgor?\n"
        "- What is the Synth Flux?\n"
        "- Tell me about the Shadow Order\n\n"
        "Команды:\n"
        "/start - Показать это сообщение\n"
        "/help - Справка"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "ℹ️ Справка по использованию:\n\n"
        "Просто напиши свой вопрос о вселенной Cyber Nexus.\n\n"
        "Я использую:\n"
        "• 🔍 Векторный поиск (FAISS)\n"
        "• 🤖 LLM генерация (Flan-T5)\n"
        "• 💡 Chain-of-Thought рассуждения\n"
        "• 📚 Few-shot примеры\n\n"
        "Если я не знаю ответа, я так и скажу!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    query = update.message.text.strip()
    logger.info(f"Получен запрос: {query}")

    if not query:
        return

    # Отправка статуса и уведомления о долгой обработке
    status_message = await update.message.reply_text("⏳ Генерирую ответ, это может занять ~30-60 секунд...")

    try:
        # Генерация ответа (запускаем в отдельном потоке, чтобы не блокировать event loop)
        logger.info(f"Начинаем генерацию ответа для: {query}")

        # Задача генерации с периодической отправкой typing action
        async def generate_with_typing():
            # Запускаем генерацию в отдельном потоке
            task = asyncio.create_task(asyncio.to_thread(rag_bot.generate_answer, query, top_k=3))

            # Периодически отправляем typing action
            while not task.done():
                try:
                    await update.message.chat.send_action(action="typing")
                except:
                    pass
                await asyncio.sleep(5)

            return await task

        result = await generate_with_typing()
        logger.info(f"Ответ сгенерирован: {len(result.get('answer', ''))} символов")

        # Удаляем статусное сообщение
        await status_message.delete()

        # Формирование сообщения (без Markdown, чтобы избежать ошибок парсинга)
        response = f"📄 Источники: {', '.join(result['sources']) if result['sources'] else 'Нет'}\n\n"
        response += result['answer']

        # Обрезка если слишком длинный
        if len(response) > 4000:
            response = response[:3900] + "\n\n... (ответ обрезан)"

        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}", exc_info=True)
        try:
            await status_message.delete()
        except:
            pass
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке запроса. Попробуйте еще раз."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Запуск бота"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")

    # Создание приложения
    application = Application.builder().token(token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Запуск
    logger.info("🚀 Telegram-бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
