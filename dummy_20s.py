import json

# # Step 1: Load the current value from the file
# with open('count.json', 'r') as file:
#     data = json.load(file)
#     current_count = data['q_count']

# # Step 2: Increment the value
# new_count = current_count + 1

# # Update the dictionary
# data['q_count'] = new_count

# # Step 3: Write the updated value back to the file
# with open('count.json', 'w') as file:
#     json.dump(data, file, indent=4)

# # Optionally, print the new value to confirm it's been updated
# print("Updated q_count:", new_count)

def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

questions = load_questions()
if (questions[0]['number']==1):
    print(questions[0]['question'])