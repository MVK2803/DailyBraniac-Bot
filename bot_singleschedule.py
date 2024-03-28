#importing required libraries
import json
import random
from telegram.ext import Updater, CommandHandler, PollAnswerHandler,CallbackContext
from datetime import datetime
from telegram import Update,Message,Chat
from dotenv import load_dotenv
import os
import db

with open('count.json', 'r') as file:
    data = json.load(file)
    current_count = data['q_count']



# Load questions from JSON file -replace with the question from ai prompt
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Handler to send a poll with a question
def send_poll(update, context):
    questions = load_questions()
    # question2 = random.choice(questions)  # Select a random question
    #print(question2)
    question=questions[current_count]
    x=context.bot.send_poll(chat_id=update.effective_chat.id,
                        question=question['question'],
                        options=question['options'],
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=question['correct_option']-1) 
    print("Details of the poll")
    print(x)
    print("Question updated")
    new_count = current_count + 1
    data['q_count'] = new_count
    with open('count.json', 'w') as file:
        json.dump(data, file, indent=4)
    #Details of the poll to be stored in the DB
    pollDetails={"pollId":int(x.poll.id),"pollQuestion":x.poll.question,"correctOption":int(x.poll.correct_option_id),"pollTime":x.date.date()}
    #add the poll details to the firebasdb  
    if db.addPollToDB(pollDetails):
        print("Poll details added to the DB")
    
   
#Handler to log the answers to the poll
def answer_poll(update, context):
    message = update.poll_answer
    '''user_id = message.user.username
    answer = message.option_ids'''
    pollDetails=db.getPollDetails(int(message.poll_id))
    correctResponse=int(pollDetails['correctOption']==message.option_ids[0])
    userName=message.user.username
    userPollResponse={"pollId":int(message.poll_id),"userResponse":correctResponse}
    db.addResponseToDB(userName,userPollResponse)
    print(message)


def main():
    print("Runnig Bot")

    updater = Updater("7164481370:AAHBkrULh_e058h5bUh2Jsc23sdeEKBf9MI", use_context=True)
    dp = updater.dispatcher


    #dp.add_handler(PollAnswerHandler(answer_poll))

    # Send a poll as soon as the bot starts
    chat_id = "-4152204929"
    context = CallbackContext.from_update(Update(0), dp)

    send_poll(Update(0, message=Message(0,datetime.now(), chat=Chat(chat_id, ""))), context)

    dp.add_handler(PollAnswerHandler(answer_poll))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()