from firebase import firebase
from datetime import date
#Setting up the connection to the database
firebase_url = 'https://dailybraniac-bot-default-rtdb.firebaseio.com/'
firebase = firebase.FirebaseApplication(firebase_url, None)

def addPollToDB(pollDetails):
    result = firebase.put('/polls', pollDetails["pollId"],pollDetails)
    print(result)
    return result

def getPollDetails(poll_id):
    # Replace this with the URL of your Firebase database
    result = firebase.get('/polls', poll_id)
    print(result)
    return result

def addResponseToDB(userName,responseDetails):
    result = firebase.post(f'/responses/{userName}', responseDetails)
    print(result)
    return result

def getPollResults():
    result = firebase.get('/responses', None)
    monthlyAggregates = {}
    for i in result:
        aggregate=0
        for j in result[i]:
            aggregate+=result[i][j]['userResponse']
        
        monthlyAggregates[i]=aggregate
    monthlyAggregates=({k: v for k, v in sorted(monthlyAggregates.items(), key=lambda item: item[1])})
    monthToppers=[]
    for i in monthlyAggregates:
        monthToppers.append(i)
    currentMonth = date.today().strftime("%B")
    result = firebase.put('/monthToppers', currentMonth,monthToppers)
    return(monthlyAggregates)

def clearDB():
    clearPoll = firebase.delete('/polls', None)
    clearResponse = firebase.delete('/responses', None)
    
# getPollResults()