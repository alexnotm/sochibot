from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"
ADMIN_ID = 294491997  # твой Telegram ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает любое сообщение админу"""
    if not update.message:
        return

    user = update.message.from_user
    text = update.message.text or "(медиа)"
    print(f"📩 Сообщение от {user.username or user.full_name}: {text}")

    try:
        # Пересылаем админу
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        # Подпись
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📨 Сообщение от @{user.username or user.full_name} (ID: {user.id})"
        )
        # Ответ пользователю
        await update.message.reply_text("✅ Ваше сообщение передано организаторам Sochi Summit.")

    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        await update.message.reply_text("⚠️ Ошибка отправки, попробуйте позже.")

if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("🤖 Бот запущен. Ожидаю сообщения...")
    app.run_polling()
