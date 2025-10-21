import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Конфигурация ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = os.getenv("ADMIN_ID", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не задан в Railway Variables.")
if not ADMIN_ID.isdigit():
    raise RuntimeError("❌ ADMIN_ID должен быть числом.")
ADMIN_ID = int(ADMIN_ID)


# === Приветствие ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎟 Добро пожаловать!\n\n"
        "Вы находитесь в официальном боте *Sochi Tech & Web3 Summit 2025* —\n"
        "главного события о технологиях, блокчейне и цифровом маркетинге.\n\n"
        "Напишите количество билетов, которые хотите приобрести, "
        "или задайте вопрос — и наша команда свяжется с вами лично 💬"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# === Пересылка сообщений админу ===
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.message.from_user
    who = user.username or user.full_name or f"id:{user.id}"
    text = update.message.text or "(медиа)"

    print(f"[LOG] Сообщение от @{who}: {text}")

    try:
        # Пересылаем админу сообщение
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

        # Добавляем подпись
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Новое сообщение от @{who} (id: {user.id})"
        )

    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")


# === Запуск бота ===
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print("🤖 Бот запущен. Ожидаю сообщений...")
    app.run_polling()
