import json
import random
from telegram.ext import Updater, CommandHandler, Filters, PollAnswerHandler
import datetime
from dotenv import load_dotenv
import os
# Load questions from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Handler to send a poll with a question
def send_poll(update, context):
    questions = load_questions()
    question2 = random.choice(questions)  # Select a random question
    #print(question2)
    x=context.bot.send_poll(chat_id=update.effective_chat.id,
                          question=question2['question'],
                          options=question2['options'],
                          is_anonymous=False,
                          type='quiz',
                          correct_option_id=question2['correct_option']-1) 
    print("Details of the poll")
    #Fetching the details of the poll
    pollDetails={"pollId":x.poll.id,"correctOption":x.poll.correct_option_id,"pollTime":x.date.date()}
    #store the poll in a db with the pollId as the primary key
    print(pollDetails)
#Handler to log the answers to the poll
def answer_poll(update, context):
    message = update.poll_answer
    user_id = message.user.username
    answer = message.option_ids
    # Log the answer
    #Fetch the poll details from the db using the pollID and verify the answer in the db and store whether 1 or 0 in the responses db
    
    print(message)


def main():
    # Load the .env file
    
    # Replace 'YOUR_TOKEN_HERE' with the token given by BotFather
    updater = Updater("7164481370:AAHBkrULh_e058h5bUh2Jsc23sdeEKBf9MI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register a command handler to trigger the poll and log the answers
    dp.add_handler(CommandHandler("start", send_poll))
    dp.add_handler(PollAnswerHandler(answer_poll))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()