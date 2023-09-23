from responsive_voice import ResponsiveVoice

def to_speech(text):
    print("Hello")
    engine = ResponsiveVoice()
    file_path = engine.get_mp3(text)
    return file_path

def listen_speech(file):
    print("Trying to listen to audio...")
    engine = ResponsiveVoice()
    engine.play_mp3(file)