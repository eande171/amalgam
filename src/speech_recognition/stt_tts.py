from os import path
import json
import logging

from vosk import Model, KaldiRecognizer, SetLogLevel
import numpy as np
import pyttsx3 as ttsx
import pyaudio

import speech_recognition as sr

from src.config import Config 

logger = logging.getLogger(__name__)

class Input():
    _r = sr.Recognizer()
    _vosk_model = None
    _kaldi = None

    @staticmethod
    def setup():
        """
        Sets up the Speech To Text. Meant to be called once at the beginning of execution, before any STT is attempted. 
        """
        from src.main import VOSK_MODEL_DIR

        if not path.exists(VOSK_MODEL_DIR):
            logger.critical("Vosk model is missing. Cannot start Amalgam speech recognition. Consider changing 'deafened' to True to disable speech recognition.")
            raise FileNotFoundError(f"Vosk model not found at {VOSK_MODEL_DIR}. Please download the model from https://alphacephei.com/vosk/models and place the model there.")

        SetLogLevel(-1)
        
        logger.info("Initialising Vosk Model...")

        Input._vosk_model = Model(VOSK_MODEL_DIR)
        Input._kaldi = KaldiRecognizer(Input._vosk_model, 16000)

        logger.info("Adjusting for ambient noise... Please be quiet.")

        try:
            with sr.Microphone() as source:
                Input._r.adjust_for_ambient_noise(source, duration=0.5)
        except OSError as e:
            Config.set_data("deafened", True)
            logger.warning(f"Microphone is not detected. Amalgam has been set to deafened (text only mode): {e}")

        Input._r.pause_threshold += 0.8
        Input._r.non_speaking_duration += 0.8


    @staticmethod
    def recognise_vosk(audio) -> str:
        """Recognize speech using Vosk"""
        Input._kaldi.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        result = Input._kaldi.FinalResult()

        # print(f"Vosk Result: {result}")
        return json.loads(result)["text"]
    
    @staticmethod
    def sst() -> str:
        """Speech To Text"""
        if Config.get_data("deafened"):
            text = input("You: ")
            return text

        with sr.Microphone() as source:
            print("Listening...")
            Output.play_blip()

            audio = Input._r.listen(source)
            print("Not Listening...")
            Output.play_blip(2)
            try:
                text = Input.recognise_vosk(audio)
                logger.info(f"You: {text}")

                for word in Config.get_data("ignore_words"):
                    if text.lower() == word:
                        logger.info("Word Ignored")
                        return ""

                return text
            except sr.UnknownValueError:
                logger.error("Unclear audio input. Amalgam does not know what was said.")
                Output.tts("Sorry, I did not understand that.")
                return ""

class Output():
    GREEN = "\033[92m"   # Success
    YELLOW = "\033[93m"  # Warning
    RED = "\033[91m"     # Error
    BLUE = "\033[94m"    # Information
    RESET = "\033[0m"    # Reset to default color

    _tts_engine = ttsx.init()

    @staticmethod
    def tts(text: str, colour: str = "\033[0m"):
        """Text to Speech"""
        if Config.get_data("muted"):
            return

        logger.info(f"Amalgam: {colour} {text}\033[0m")
        Output._tts_engine.say(text)
        Output._tts_engine.runAndWait()

    @staticmethod
    def generate_blip(
        duration=0.1,  # very short duration in seconds
        start_freq=1000, # starting frequency for the blip
        end_freq=1500,   # ending frequency (can be same as start_freq for a pure tone blip)
        volume=0.6,    # overall volume (0.0 to 1.0)
        rate=44100,    # samples per second
        decay_factor=50 # Controls how fast the sound decays. Higher = faster decay.
    ):
        """
        Generates a simple "blip" sound.
        Can be a very short, quick frequency sweep or a single tone with fast decay.
        """
        t = np.linspace(0, duration, int(rate * duration), endpoint=False)

        # 1. Frequency Generation (linear sweep for a tiny "chirp")
        # If start_freq == end_freq, it will be a constant frequency blip.
        frequencies = np.linspace(start_freq, end_freq, len(t))
        phase = 2 * np.pi * np.cumsum(frequencies / rate)
        
        # 2. Envelope (fast attack, very fast decay)
        # A simple exponential decay works well for blips.
        # The decay_factor controls the speed of the decay.
        envelope = np.exp(-decay_factor * t)
        
        # 3. Generate the sound wave
        samples = volume * np.sin(phase) * envelope

        # Ensure samples are within the valid float32 range (-1.0 to 1.0)
        # This normalization helps prevent clipping if volume is too high or decay_factor is too low
        max_amp = np.max(np.abs(samples))
        if max_amp > 0:
            samples /= max_amp
        
        return samples.astype(np.float32).tobytes()

    @staticmethod
    def play_sound(sound_data):
        """Play sound data using PyAudio"""
        if Config.get_data("muted"):
            return

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        stream.write(sound_data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    @staticmethod
    def play_blip(count: int = 1):
        """Generate and play a blip sound"""
        for _ in range(count):
            Output.play_sound(Output.generate_blip())