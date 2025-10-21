from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === Настройки ===
BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"
ADMIN_USERNAME = "AdSochi"

# === Пересылка сообщений ===
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.message.from_user
    name = user.username or user.full_name or "Без имени"

    try:
        # Пересылаем оригинальное сообщение админу
        await context.bot.forward_message(
            chat_id=f"@{ADMIN_USERNAME}",
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

        # Добавляем подпись
        await context.bot.send_message(
            chat_id=f"@{ADMIN_USERNAME}",
            text=f"📩 Сообщение от @{name} (id: {user.id})"
        )

        # Отвечаем пользователю
        await update.message.reply_text(
            "✅ Спасибо! Ваше сообщение отправлено организаторам Sochi Summit."
        )

    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")

# === Запуск бота ===
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print("🤖 Бот запущен и ждёт сообщений...")
    app.run_polling()
