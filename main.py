import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Настройки ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = os.getenv("ADMIN_ID", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не задан в Railway Variables.")
if not ADMIN_ID.isdigit():
    raise RuntimeError("❌ ADMIN_ID должен быть числом.")
ADMIN_ID = int(ADMIN_ID)

# Память соответствий: { message_id_админа: user_id_пользователя }
reply_map = {}

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


# === Основной обработчик ===
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    user = msg.from_user

    # --- 1️⃣ Пользователь пишет админу
    if user.id != ADMIN_ID:
        who = user.username or user.full_name or f"id:{user.id}"
        text = msg.text or "(медиа)"
        print(f"[LOG] Сообщение от @{who}: {text}")

        try:
            # пересылаем админу оригинал
            forwarded = await context.bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )

            # подпись
            caption = f"📩 Сообщение от @{who} (id: {user.id})"
            note = await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=caption,
                reply_to_message_id=forwarded.message_id
            )

            # сохраняем связь (ответ админу -> исходный пользователь)
            reply_map[note.message_id] = user.id
            reply_map[forwarded.message_id] = user.id

        except Exception as e:
            print(f"⚠️ Ошибка при пересылке: {e}")

    # --- 2️⃣ Админ отвечает пользователю
    elif msg.reply_to_message:
        target_id = None

        # пробуем определить ID через карту
        if msg.reply_to_message.message_id in reply_map:
            target_id = reply_map[msg.reply_to_message.message_id]

        # пробуем достать напрямую (если forward_origin есть)
        elif msg.reply_to_message.forward_origin and msg.reply_to_message.forward_origin.sender_user:
            target_id = msg.reply_to_message.forward_origin.sender_user.id

        if target_id:
            try:
                await context.bot.send_message(chat_id=target_id, text=msg.text)
                print(f"[LOG] Ответ от админа → пользователю {target_id}: {msg.text}")
            except Exception as e:
                print(f"⚠️ Ошибка при ответе пользователю {target_id}: {e}")
        else:
            print("⚠️ Не удалось определить, кому отправить ответ.")


# === Запуск ===
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handler))
    print("🤖 Бот запущен и готов к работе.")
    app.run_polling()
