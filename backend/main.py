# uvicorn main:app --reload

#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from decouple import config 
import openai
from functions.openai_requests import get_chat_response
from bson import json_util
from datetime import datetime, timedelta




#Custom Function imports
from functions.database_mongo import *
from functions.openai_requests import convert_audio_to_text
from functions.text_to_speech import convert_text_to_speech
from functions.text_to_speech_rv import to_speech

#Initiate App
app = FastAPI()

#CORS - Origins

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

#CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Check Health
@app.get("/health")
async def check_health():
    return {"message":"healthy"}

@app.get("/reset")
async def reset_conversation(user_id: str, session_id: str):
    reset_messages(user_id, session_id)
    return {"message":"conversation reset"}


@app.get("/conversations", include_in_schema=False)
async def get_conversations(user_id: str, session_id: str):
    conversations = get_filtered_messages(user_id, session_id)
    #conversation_list = [json_util.dumps(conversation, default=json_util.default) for conversation in conversations]
    # Converti ObjectId in stringhe
    for conversation in conversations:
        conversation['_id'] = str(conversation['_id'])
    print(conversations)
    return JSONResponse(content=conversations)
@app.get("/speech")
async def get_speech(audio_file: str):
    #audio_output = to_speech(text)
    #audio_output = get_audio(message_id)
    return FileResponse(audio_file, media_type="audio/mpeg")

#Get Audio
@app.post("/post-audio/")
async def post_audio(user_id: str, session_id: str, file: UploadFile = File(...)):
    #Get saved audio
    #audio_input = open("voice.mp3", "rb")
    
    #Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")


    #Decode Audio
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    #Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    #Get ChatGPT Response
    chat_response = get_chat_response(message_decoded, user_id, session_id)

    #Guard: Ensure message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    #Store messages
    message_id = store_messages(message_decoded, chat_response, user_id, session_id)

    #Convert chat response to audio
    #####audio_output = convert_text_to_speech(chat_response)
    audio_output = to_speech(chat_response)
        #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Responsive Voice audio response") #Eleven Labs audio response")

    store_audio(message_id, audio_output)

    #Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #Return audio file 
    ####return StreamingResponse(iterfile(), media_type="application/octet-stream" )
    return FileResponse(audio_output, media_type="audio/mpeg")

# Post bot response 
# Note: Not playing in browser when using post request
#@app.post("/post-audio/")
#async def post_audio(file: UploadFile = File(...)):


# API per la registrazione di un nuovo utente
@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Assicurati che l'utente non esista già
    existing_user = usersCollection.find_one({"username": user.username})
    existing_email = usersCollection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash della password prima di salvarla nel database
    hashed_password = pwd_context.hash(user.password)
    
    # Simulazione di salvataggio in database (sostituisci con la tua logica)
    new_user = {"email": user.email, "username": user.username, "password": hashed_password}
    result = usersCollection.insert_one(new_user)
    
    # Creazione del token di accesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return UserResponse(**user.dict(), access_token=access_token, token_type="bearer")

# API per l'accesso di un utente
@app.post("/login", response_model=UserResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Creazione del token di accesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    
    return UserResponse(**user, access_token=access_token, token_type="bearer")