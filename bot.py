import json
import random
from telegram.ext import Updater, CommandHandler

# Load questions from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Handler to send a poll with a question
def send_poll(update, context):
    questions = load_questions()
    question2 = random.choice(questions)  # Select a random question
    print(question2)
    context.bot.send_poll(chat_id=update.effective_chat.id,
                          question=question2['question'],
                          options=question2['options'],
                          is_anonymous=False,
                          type='quiz',
                          correct_option_id=question2['correct_option']-1)  # Replace "8" with the correct answer for your question

def main():
    # Replace 'YOUR_TOKEN_HERE' with the token given by BotFather
    updater = Updater("7164481370:AAH8UHyiHjVj89lSrXo4MQNdf1Zrt7F-QYE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register a command handler to trigger the poll
    dp.add_handler(CommandHandler("start", send_poll))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
