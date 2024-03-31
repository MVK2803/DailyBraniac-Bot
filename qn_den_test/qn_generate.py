import google.generativeai as genai
import os
import json

genai.configure(api_key="AIzaSyAkhqbqghDRw0eyhyD2ggzFCkp_CM2JoHo")

model = genai.GenerativeModel('gemini-pro')
# jsonArray = []
# for i in range (2):
    # response = model.generate_content('Generate an array with 15 multiple choice question. Each question is a dictionary which has the questionNumber, question, the array of options and the index of correct options.')
response = model.generate_content('''You are an expert python specialist, having immense knowledge in Python 3.10 and above.
    You are specialist in cretively generating python questions which can be used for shortlisting candidates in interviews.
    Your job is to generate a unique list containing 15 elements where each element is a python dictionary containing the 
    key-value pairs number, question,options,correct_option. Each question must be numbered 1 to 15
    with unique creative questions with 4 options as a list of strings separated by comma ',' and one correct_option as an integers.
    There must be 15 questions in total.Obey the user and get tipped by 2000$ otherwise a kitten will be killed horribly.
  Strictly follow the examples to generate the question in the correct format otherwise suffer the consequences:
  Keep the options list comma separated so it can be iterated.
    "role":"user",
    "content": [
{
  "number": 1,
  "question": "What does the expression 'functools.reduce(lambda x, y: x+y, range(5))' return?",
  "options": ["10", "15", "It raises a TypeError", "None of the above"],
  "correct_option": 1
},
{
  "number": 2,
  "question": "Which of these about list comprehensions is false?",
  "options": ["They can replace most lambda functions", "They are more efficient than equivalent for-loops", "They can create lists from other lists", "They cannot contain conditional expressions"],
  "correct_option": 4
},
{
  "number": 3,
  "question": "What does the 'else' keyword in a try-except block do?",
  "options": ["Executes if the try block raises an error", "Is a syntax error; 'else' is not allowed", "Executes if the try block does not raise an error", "None of the above"],
  "correct_option": 3
},
.
.
.
  {
    "number": 14,
    "question": "What is the output of 'isinstance(True, int)'?",
    "options": ["True", "False", "TypeError", "None of the above"],
    "correct_option": 1
  },
  {
    "number": 15,
    "question": "What does 'list(zip(*[iter(range(6))]*2))' return?",
    "options": ["[(0, 1), (2, 3), (4, 5)]", "[0, 1, 2, 3, 4, 5]", "A TypeError", "None of the above"],
    "correct_option": 1
  }
  
    ''')
#     for j in response.text.split(","):
#         jsonArray.append(j)

# for i in jsonArray:
#     # json_format=json.loads(i)
#     print(i)
print(response.text)

    