import json
import random
from telegram.ext import Updater, CommandHandler, PollAnswerHandler
import datetime
import calendar
import time
from apscheduler.schedulers.background import BackgroundScheduler
import db
import pytz

# Load questions from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Function to send polls one by one
def send_poll(update, context, job_queue):
    questions = load_questions()
    for question in questions:
        x = context.bot.send_poll(chat_id=update.effective_chat.id,
                                   question=question['question'],
                                   options=question['options'],
                                   is_anonymous=False,
                                   type='quiz',
                                   correct_option_id=question['correct_option']-1)
        print("Details of the poll")
        print(x)
        # Details of the poll to be stored in the DB
        pollDetails = {"pollId": int(x.poll.id), "pollQuestion": x.poll.question, "correctOption": int(x.poll.correct_option_id), "pollTime": x.date.date()}
        # Add the poll details to the database
        if db.addPollToDB(pollDetails):
            print("Poll details added to the DB")
        # Wait for 20 seconds before sending the next question
        time.sleep(20)

# Handler to log the answers to the poll
def answer_poll(update, context):
    message = update.poll_answer
    pollDetails = db.getPollDetails(int(message.poll_id))
    correctResponse = int(pollDetails['correctOption'] == message.option_ids[0])
    userName = message.user.username
    userPollResponse = {"pollId": int(message.poll_id), "userResponse": correctResponse}
    db.addResponseToDB(userName, userPollResponse)
    print(message)

def setup_scheduler(bot_token, schedule_hour, schedule_minute, schedule_end_date):
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", send_poll, pass_job_queue=True))
    dp.add_handler(PollAnswerHandler(answer_poll))
    updater.start_polling()

    scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Calcutta'))  # Replace 'YOUR_TIMEZONE' with your desired timezone
    scheduler.start()

    job = scheduler.add_job(send_poll, 'cron', hour=schedule_hour, minute=schedule_minute, end_date=schedule_end_date, args=[updater.job_queue])

    updater.idle()

def main():
    # Bot token
    BOT_TOKEN = "7164481370:AAHBkrULh_e058h5bUh2Jsc23sdeEKBf9MI"

    # Schedule details
    SCHEDULE_HOUR = 8  # Hour of the day to send the polls (24-hour format)
    SCHEDULE_MINUTE = 0  # Minute of the hour to send the polls
    SCHEDULE_END_DATE = datetime.datetime(datetime.date.today().year, datetime.date.today().month, calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1], SCHEDULE_HOUR, SCHEDULE_MINUTE, tzinfo=pytz.timezone('Asia/Calcutta'))  # End date and time for the schedule (last day of the current month)

    setup_scheduler(BOT_TOKEN, SCHEDULE_HOUR, SCHEDULE_MINUTE, SCHEDULE_END_DATE)

if __name__ == '__main__':
    main()