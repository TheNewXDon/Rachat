import openai
from decouple import config 

from functions.database_mongo import get_recent_messages, system_prompt_interview

# Retrieve Environment Variables 
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# Open AI - Whisper
# Convert Audio to Text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return

# Open AI - ChatGPT
# Get response our message

def get_chat_response(message_input, user_id, session_id):
    system_prompt = system_prompt_interview(user_id, session_id)
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input, "user_id": user_id, "session_id": session_id}
    messages.append(user_message)
    print(messages)

    try:
        formatted_messages = [{"role": message["role"], "content": message["content"]} for message in messages]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [system_prompt] + formatted_messages[-3:]
        )
        print(response)
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(e)
        return