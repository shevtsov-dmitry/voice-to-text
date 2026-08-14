import os
import tempfile
from pathlib import Path

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from transcriber import Transcriber


TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

transcriber = Transcriber()


# Temporary in-memory storage.
# Later we can replace this with PostgreSQL.
user_languages: dict[int, str] = {}


def language_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🇬🇧 EN", "🇷🇺 RU"],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    await update.message.reply_text(
        "Send me a voice message and I will transcribe it.\n\n"
        "Choose transcription language:",
        reply_markup=language_keyboard(),
    )


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🇬🇧 EN":
        user_languages[user_id] = "en"
        language_name = "English"

    elif text == "🇷🇺 RU":
        user_languages[user_id] = "ru"
        language_name = "Russian"

    else:
        return

    await update.message.reply_text(
        f"Language changed to {language_name}.",
        reply_markup=language_keyboard(),
    )


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    language = user_languages.get(user_id, "ru")

    await update.message.reply_text("🎧 Processing...")

    voice = update.message.voice

    telegram_file = await context.bot.get_file(voice.file_id)

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = Path(temp_dir) / "audio.ogg"

        await telegram_file.download_to_drive(audio_path)

        text = transcriber.transcribe(
            str(audio_path),
            language,
        )

    if not text:
        await update.message.reply_text(
            "I couldn't recognize any speech.",
            reply_markup=language_keyboard(),
        )
        return

    await update.message.reply_text(
        text,
        reply_markup=language_keyboard(),
    )


def main():
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^(🇬🇧 EN|🇷🇺 RU)$"),
            language,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice,
        )
    )

    print("Bot started.")

    application.run_polling()


if __name__ == "__main__":
    main()
