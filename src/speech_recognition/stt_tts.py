import speech_recognition as sr
import pyttsx3 as ttsx
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import os

r = sr.Recognizer()
tts_engine = ttsx.init() # Path to the Vosk model directory

print("Adjusting for ambient noise... Please be quiet.")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise

r.pause_threshold += 0.8
r.non_speaking_duration = 0.8
SetLogLevel(-1)

class Speech():
    def __init__(self, model_path: str = "model"):
        self.model_path = model_path

    def recognise_vosk(self, audio, model_path):
        """Recognize speech using Vosk"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at {model_path}. Please download the model from https://alphacephei.com/vosk/models and place the model there.")
        model = Model(model_path)
        rec = KaldiRecognizer(model, 16000)
        rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        result = rec.FinalResult()

        # print(f"Vosk Result: {result}")
        return json.loads(result)["text"]

    def sst(self, model_path) -> str:
        """Speech to Text"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                text = self.recognise_vosk(audio, model_path)
                print(f"You: {text}")
                return text
            except sr.UnknownValueError:
                self.tts("Sorry, I did not understand that.")
                return ""

    def tts(self, text: str):
        """Text to Speech"""
        print(f"Amalgam: {text}")
        tts_engine.say(text)
        tts_engine.runAndWait()