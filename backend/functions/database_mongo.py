from bson import ObjectId
import pymongo
from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi


uri = "mongodb+srv://{dbuser}:{dbpassword}/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.rachel
usersCollection = db.users
messagesCollection = db.messages
#print(client.server_info())

def system_prompt_interview(user_id, session_id):
    learn_instructions = {
        "role": "system",
        "content": "As a Senior Software Engineer, you are interviewing the user for a job. Ask short questions that are relevant to the junior position. Your name is Rachel. Keep your answer to under 30 words.",
        "user_id": user_id,
        "session_id": session_id
    }
    criteria = {
        "role": "system",
        "user_id": user_id,
        "session_id": session_id 
    }
    if messagesCollection.count_documents(criteria) == 0:
        messagesCollection.insert_one(learn_instructions)
    return {"role": learn_instructions["role"], "content": learn_instructions["content"]}

def store_messages(request_message, response_message, user_id, session_id):
    
    system_prompt_interview(user_id, session_id)

    # Crea un documento per il messaggio utente
    user_message = {"role": "user", "content": request_message, "user_id": user_id, "session_id": session_id}
    # Crea un documento per il messaggio assistente
    assistant_message = {"role": "assistant", "content": response_message, "user_id": user_id, "session_id": session_id}

    # Inserisci i documenti nella raccolta MongoDB
    messagesCollection.insert_one(user_message)
    result = messagesCollection.insert_one(assistant_message)
    return result.inserted_id

def store_audio(message_id, audio_data):
    update_data = {"$set": {"audio": audio_data}}

    result = messagesCollection.update_one({"_id": message_id}, update_data)
    return audio_data

def get_audio(message_id):
    message = messagesCollection.find_one({"_id": message_id})
    return message['audio']

def reset_messages(user_id, session_id):
    # Elimina tutti i documenti dalla raccolta MongoDB
    messagesCollection.delete_many({"user_id": user_id, "session_id": session_id})


def get_recent_messages():
    # Recupera le ultime 5 conversazioni dalla raccolta MongoDB
    recent_messages = messagesCollection.find().sort([("_id", ASCENDING)])

    # Restituisci le conversazioni come una lista di dizionari
    return list(recent_messages)

def get_filtered_messages(user_id, session_id):
    # Filtra i messaggi in cui il campo "role" non è "system"
    filter_criteria = {"role": {"$ne": "system"}, "user_id": user_id, "session_id": session_id}
    # Recupera le ultime 5 conversazioni dalla raccolta MongoDB
    recent_messages = messagesCollection.find(filter_criteria).sort([("_id", ASCENDING)])

    # Restituisci le conversazioni come una lista di dizionari
    return list(recent_messages)


###################### USER ###########################

from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from decouple import config
from passlib.context import CryptContext



class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    

class User(UserCreate):
    user_id: str
    _id: str
    

class Token(BaseModel):
    access_token: str
    token_type: str

# Modello per l'oggetto utente in risposta
class UserResponse(User):
    access_token: str
    token_type: str

SECRET_KEY_JWT = config("SECRET_KEY_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funzione per creare un token di accesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)
    return encoded_jwt

# Funzione per autenticare un utente
def authenticate_user(username: str, password: str):
    user = usersCollection.find_one({"username": username})
    email = usersCollection.find_one({"email": username})
    if not user and not email:
        return None
    if not pwd_context.verify(password, user['password']):
        return None
    user['user_id'] = str(user['_id'])
    return user