import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re 

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

prompt=PromptTemplate(input_variables=['q_start','q_end','examples'],
template='''You are an expert python specialist, having immense knowledge in Python 3.10 and above.
    You are specialist in cretively generating python questions which can be used for shortlisting candidates in interviews.
    Your job is to generate a unique list containing 15 elements where each element is a python dictionary containing the 
    key-value pairs number, question,options,correct_option. Each question must be numbered {q_start} to {q_end}
    with unique creative questions with 4 options as a list of strings separated by comma ',' and one correct_option as an integers.
    DONOT create questions having string formatting,fstrings or questions containing curly barckets EVER which can break JSON format.
    There must be 15 questions in total.Obey the user and get tipped by 2000$ otherwise a kitten will be killed horribly.
  Strictly follow the examples to generate the question in the correct JSON format otherwise suffer the consequences:
  Keep the options list comma separated so it can be iterated.
  {examples}
  ''')

chain1 = LLMChain(llm=llm, prompt=prompt, verbose=True)

if __name__=="__main__":
    q1 = 1
    q2 = 15
    
    example1='''
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
  }'''

example2='''
    "role":"user",
    "content": [
{
  "number": 16,
  "question": "What does the expression 'functools.reduce(lambda x, y: x+y, range(5))' return?",
  "options": ["10", "15", "It raises a TypeError", "None of the above"],
  "correct_option": 1
},
{
  "number": 17,
  "question": "Which of these about list comprehensions is false?",
  "options": ["They can replace most lambda functions", "They are more efficient than equivalent for-loops", "They can create lists from other lists", "They cannot contain conditional expressions"],
  "correct_option": 4
},
{
  "number": 18,
  "question": "What does the 'else' keyword in a try-except block do?",
  "options": ["Executes if the try block raises an error", "Is a syntax error; 'else' is not allowed", "Executes if the try block does not raise an error", "None of the above"],
  "correct_option": 3
},
.
.
.
  {
    "number": 29,
    "question": "What is the output of 'isinstance(True, int)'?",
    "options": ["True", "False", "TypeError", "None of the above"],
    "correct_option": 1
  },
  {
    "number": 30,
    "question": "What does 'list(zip(*[iter(range(6))]*2))' return?",
    "options": ["[(0, 1), (2, 3), (4, 5)]", "[0, 1, 2, 3, 4, 5]", "A TypeError", "None of the above"],
    "correct_option": 1
  }'''

# print(eamples)
response1 = chain1.run(q_start=q1,q_end=q2,examples=example1)
print(response1)
cleaned_response1 = re.sub(r'^```|```$', '', response1.strip())

# Extract the first sentence
match = re.search(r'^.*?\.\s', cleaned_response1)

if match:
    first_sentence = match.group()
    # Apply regex substitutions on the first sentence
    modified_first_sentence = re.sub(r'\bquestions\b', '', first_sentence)
    modified_first_sentence = re.sub(r'\bpython\b', '', modified_first_sentence, flags=re.IGNORECASE)  # Case-insensitive for 'python'
    modified_first_sentence = re.sub(r'\b=\b', '', modified_first_sentence)
    
    # Reassemble the string with the modified first sentence
    clean_response = modified_first_sentence + cleaned_response1[match.end():]
else:
    # If there's no match (e.g., no period found), apply the modifications to the whole string
    clean_response = re.sub(r'\bquestions\b', '', cleaned_response1)
    clean_response = re.sub(r'\bpython\b', '', clean_response, flags=re.IGNORECASE)
    clean_response = re.sub(r'\b=\b', '', clean_response)

# Optional: Clean up any extra spaces that might have been created
clean_response = re.sub(' +', ' ', clean_response).strip()

print(clean_response)

# Parse the JSON string
try:
    final = json.loads(clean_response)
    print(final)
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)






# words=response1.split()
# modified_first_words1 = [re.sub(r'\b' + re.escape('questions') + r'\b', '', word) for word in words[:4]]
# modified_first_words2 = [re.sub(r'\b' + re.escape('python') + r'\b', '', word) for word in modified_first_words1[::]]
# modified_first_words3 = [re.sub(r'\b' + re.escape('=') + r'\b', '', word) for word in modified_first_words2[::]]

# clean_resp3 = ' '.join(modified_first_words3 + words[4:])
# print(clean_resp3)

# clean_resp1=re.sub(r'\b' + re.escape('questions') + r'\b', '', response1)
# clean_resp2=re.sub(r'\b' + re.escape('python') + r'\b', '', clean_resp1)
# print(clean_resp2)
# resp1=json.loads(clean_resp1)
# print(resp1)

# response2 = chain1.run(q_start=q2+1,q_end=30,examples=example2)
# # print(response2)
# clean_resp3=re.sub(r'\b' + re.escape('questions') + r'\b', '', response2)
# clean_resp4=re.sub(r'\b' + re.escape('python') + r'\b', '', clean_resp3)
# print(clean_resp4)
# print(type(clean_resp4))
# resp2=json.loads(clean_resp4)
# print(resp2)




# resp2=chain1.run(q_start=q2+1,q_end=30,examples=example2)
# print(resp1.text)
# data1=json.loads(resp1)
# data2=json.loads(resp2)
# print(data1)
# combined_data = data1 + data2

# # Convert the combined list back into a JSON string
# combined_json_string = json.dumps(combined_data, indent=4)
# print(combined_json_string)

# print(json.dumps(resp2)+json.dumps(resp1))

# data_total=json.dumps(data1+data2,indent=4)
# print(data)