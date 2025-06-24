import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel

from threading import Thread
from queue import Queue

import json
import os

import pyttsx3 as ttsx
tts_engine = ttsx.init()

r = sr.Recognizer()

print("Adjusting for ambient noise... Please be quiet.")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise

r.pause_threshold += 0.8
r.non_speaking_duration += 0.8
SetLogLevel(-1)

class Speech():
    def __init__(self, model_path: str = "model"):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please download the model from https://alphacephei.com/vosk/models and place the model there.")

        self.model = Model(self.model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

    def recognise_vosk(self, audio):
        """Recognize speech using Vosk"""
        self.rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        result = self.rec.FinalResult()

        # print(f"Vosk Result: {result}")
        return json.loads(result)["text"]

    def sst(self) -> str:
        """Speech to Text"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print("Not Listening...")
            try:
                text = self.recognise_vosk(audio)
                print(f"You: {text}")
                return text
            except sr.UnknownValueError:
                Output.tts("Sorry, I did not understand that.")
                return ""
            
class Output():
    GREEN = "\033[92m"   # Success
    YELLOW = "\033[93m"  # Warning
    RED = "\033[91m"     # Error
    BLUE = "\033[94m"    # Information
    RESET = "\033[0m"    # Reset to default color

    @staticmethod
    def tts(text: str, colour: str = "\033[0m"):
        """Text to Speech"""
        print(f"Amalgam: {colour} {text}\033[0m")
        tts_engine.say(text)
        tts_engine.runAndWait()