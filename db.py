from firebase import firebase
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
