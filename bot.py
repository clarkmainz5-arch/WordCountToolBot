import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WORDS_PER_MINUTE_READING = 200
WORDS_PER_MINUTE_SPEAKING = 130


def analyze_text(text: str) -> dict:
    stripped = text.strip()

    words = re.findall(r"\S+", stripped)
    word_count = len(words)

    char_count = len(stripped)
    char_count_no_spaces = len(re.sub(r"\s", "", stripped))

    sentences = re.findall(r"[^.!?]+[.!?]", stripped)
    if not sentences and stripped:
        sentences = [stripped]
    sentence_count = len(sentences)

    paragraphs = [p for p in re.split(r"\n\s*\n", stripped) if p.strip()]
    paragraph_count = len(paragraphs) if paragraphs else (1 if stripped else 0)

    reading_time = word_count / WORDS_PER_MINUTE_READING
    speaking_time = word_count / WORDS_PER_MINUTE_SPEAKING

    return {
        "words": word_count,
        "chars": char_count,
        "chars_no_spaces": char_count_no_spaces,
        "sentences": sentence_count,
        "paragraphs": paragraph_count,
        "reading_time": reading_time,
        "speaking_time": speaking_time,
    }


def format_time(minutes: float) -> str:
    total_seconds = int(round(minutes * 60))
    m, s = divmod(total_seconds, 60)
    if m == 0:
        return f"{s} sec"
    return f"{m} min {s} sec"


def build_report(text: str) -> str:
    stats = analyze_text(text)
    if stats["words"] == 0:
        return "Send me some text and I'll count it for you."

    return (
        "📊 *Text Stats*\n\n"
        f"📝 Words: `{stats['words']}`\n"
        f"🔤 Characters (with spaces): `{stats['chars']}`\n"
        f"🔡 Characters (no spaces): `{stats['chars_no_spaces']}`\n"
        f"📖 Sentences: `{stats['sentences']}`\n"
        f"📄 Paragraphs: `{stats['paragraphs']}`\n"
        f"⏱ Reading time: `{format_time(stats['reading_time'])}`\n"
        f"🗣 Speaking time: `{format_time(stats['speaking_time'])}`"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm *WordCountTool Bot*.\n\n"
        "Send me any text and I'll count words, characters, sentences, "
        "paragraphs, and estimate reading/speaking time.\n\n"
        "Commands:\n"
        "/count <text> - analyze text directly\n"
        "Or just send text as a normal message.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just paste or type any text and send it to me.\n"
        "You can also use /count followed by your text.\n\n"
        "I'll reply with:\n"
        "- Word count\n"
        "- Character count (with/without spaces)\n"
        "- Sentence count\n"
        "- Paragraph count\n"
        "- Estimated reading & speaking time"
    )


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or ""
    report = build_report(text)
    await update.message.reply_text(report, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    report = build_report(text)
    await update.message.reply_text(report, parse_mode="Markdown")


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it in Railway's Variables tab."
        )

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("count", count_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot starting with polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
