import json
import random


# Get recent messages
def get_recent_messages():

    # Define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instructions = {
        "role": "system",
        "content": "You are interviewing the user for a job as a Senior Software Engineer. Ask short questions that are relevant to the junior position. Your name is Rachel. Keep your answer to under 30 words."
    }

    # Initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instructions["content"] = learn_instructions["content"] + " Your response will include some light dry humour."
    else:
        learn_instructions["content"] = learn_instructions["content"] + " Your response will include a rather challenging question."

    # Append instruction to message 
    messages.append(learn_instructions)

    # Get last messages 
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append the last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    # Return
    return messages


# Store messages

def store_messages(request_message, response_message):
    
    # Define the file name
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to data
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)

# Reset messages
def reset_messages():
    open("stored_data.json", "w")


def get_conversation():
    # Define the file name
    file_name = "stored_data.json"

    with open(file_name, "r") as f:
        data = json.load(f)
    
    return data