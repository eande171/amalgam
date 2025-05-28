import speech_recognition as sr
import pyttsx3 as tts
import json

r = sr.Recognizer()
tts_engine = tts.init()

def sst() -> str:
    """Speech to Text"""
    with sr.Microphone() as source:
        audio = r.listen(source)    
        try:
            text = json.loads(r.recognize_vosk(audio))
            text = text["text"]

            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            tts("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            tts(f"Could not request results; {e}")    
            return ""

def tts(text: str):
    """Text to Speech"""
    print(f"Amalgam: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()