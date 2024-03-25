import json
import random
from telegram.ext import Updater, CommandHandler, PollAnswerHandler
import os
import db

def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

def get_next_question_index():
    state_file = 'last_q.txt'
    try:
        with open(state_file, 'r') as file:
            last_index = int(file.read().strip())
    except FileNotFoundError:
        last_index = -1  # -1 means no question has been sent yet
    return (last_index + 1) % len(load_questions())  # Cycle through questions

def update_question_index(index):
    state_file = 'last_q.txt'
    with open(state_file, 'w') as file:
        file.write(str(index))

def send_poll(update, context):
    questions = load_questions()
    next_index = get_next_question_index()
    question = questions[next_index]  # Select the next question
    update_question_index(next_index)  # Update the index for the next run

    poll = context.bot.send_poll(chat_id=update.effective_chat.id,
                                 question=question['question'],
                                 options=question['options'],
                                 is_anonymous=False,
                                 type='quiz',
                                 correct_option_id=question['correct_option']-1)
    print("Details of the poll")
    print(poll)
    pollDetails = {"pollId": int(poll.poll.id), "pollQuestion": poll.poll.question, "correctOption": int(poll.poll.correct_option_id), "pollTime": poll.date.date()}
    if db.addPollToDB(pollDetails):
        print("Poll details added to the DB")

def answer_poll(update, context):
    message = update.poll_answer
    pollDetails = db.getPollDetails(int(message.poll_id))
    correctResponse = int(pollDetails['correctOption'] == message.option_ids[0])
    userName = message.user.username
    userPollResponse = {"pollId": int(message.poll_id), "userResponse": correctResponse}
    db.addResponseToDB(userName, userPollResponse)
    print(message)

def main():
    updater = Updater("7164481370:AAHBkrULh_e058h5bUh2Jsc23sdeEKBf9MI", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", send_poll))
    dp.add_handler(PollAnswerHandler(answer_poll))

    send_poll(None, updater)  # Directly send a poll when the script is executed

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
