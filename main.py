from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = '7863179997:AAENFnmUnV45j5bZufypTfbFAuPEWr8mEug'
GROUP_CHAT_ID = -1007024135974

(ASK_NAME, ASK_AGE, ASK_GRADE, ASK_SUBJECT, ASK_FEEDBACK) = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Let's begin the survey.\nWhat is your name?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(f"Thanks, {name}. How old are you?")
    return ASK_AGE

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    name = context.user_data["name"]
    await update.message.reply_text(f"{name}, what grade are you in?")
    return ASK_GRADE

async def ask_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["grade"] = update.message.text
    name = context.user_data["name"]
    await update.message.reply_text(f"Great. What's your favorite subject, {name}?")
    return ASK_SUBJECT

async def ask_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["subject"] = update.message.text
    name = context.user_data["name"]
    await update.message.reply_text(f"Got it. Any comments or feedback?")
    return ASK_FEEDBACK

async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["feedback"] = update.message.text
    name = context.user_data["name"]
    age = context.user_data["age"]
    grade = context.user_data["grade"]
    subject = context.user_data["subject"]
    feedback = context.user_data["feedback"]

    message = f"New Survey Response:\nName: {name}\nAge: {age}\nGrade: {grade}\nSubject: {subject}\nFeedback: {feedback}"
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)

    await update.message.reply_text(f"Thank you, {name}. Your responses have been submitted.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Survey cancelled.")
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
        ASK_GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_grade)],
        ASK_SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_subject)],
        ASK_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_feedback)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

app.add_handler(conv_handler)

# Keep-alive trick
from flask import Flask
from threading import Thread

web_app = Flask('')

@web_app.route('/')
def home():
    return "Running"

def run():
    web_app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# Start polling
app.run_polling()
