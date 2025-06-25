import os
import importlib
import json
import time

from openwakeword.model import Model
from openwakeword.utils import download_models

import pyaudio
import numpy as np

import spacy

from src.speech_recognition.stt_tts import Speech, Output
from src.config import load_config

# Constants
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(SOURCE_DIR, "..")

PLUGINS_DIR = os.path.join(CORE_DIR, "plugins")
MODEL_DATA_DIR = os.path.join(CORE_DIR, "model_data")
USER_DATA_DIR = os.path.join(CORE_DIR, "user_data")
PLUGIN_CONFIG_DIR = os.path.join(USER_DATA_DIR, "plugin_config")

VOSK_MODEL_DIR = os.path.join(SOURCE_DIR, "speech_recognition", "model")

download_models(["hey_jarvis"])
model = Model(["hey_jarvis"], inference_framework="onnx", vad_threshold=0.5)

# Global Variables
config_data = {}
active_application = "Spotify"

class PluginController:
    def __init__(self):
        self.active_plugin = None
        self.identifiers = []
        self.plugins = {}

    def load_plugins(self):
        if not os.path.exists(PLUGINS_DIR):
            raise FileNotFoundError(f"Plugins directory '{PLUGINS_DIR}' does not exist.")
        
        for file in os.listdir(PLUGINS_DIR):
            if file.endswith(".py") and not file == "__init__.py":
                plugin_name = file[:-3]
                print(f"Loading plugin: {plugin_name}")

                # Import the Plugin Class
                plugin = importlib.import_module(f"plugins.{plugin_name}")
                plugin_class = getattr(plugin, "Plugin", None)

                print(f"Plugin Name: {plugin_class.get_identifier(plugin_class)}")
                self.plugins[plugin_class.get_identifier(plugin_class)] = plugin_class

                self.identifiers.append(plugin_class.get_identifier(plugin_class))

    def set_active_plugin(self, identifier):
        if identifier in self.plugins:
            self.active_plugin = self.plugins[identifier]
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")
        
    def get_active_identifier(self):
        if self.active_plugin:
            return self.active_plugin.get_identifier(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")
        
    def get_active_description(self):
        if self.active_plugin:
            return self.active_plugin.get_description(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")
        
    def active_startup(self):
        if self.active_plugin:
            self.active_plugin.startup(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")
        
    def active_execute(self):
        if self.active_plugin:
            self.active_plugin.execute(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")
        
    def active_shutdown(self):
        if self.active_plugin:
            self.active_plugin.shutdown(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")

    def get_plugin(self, identifier):
        if identifier in self.plugins:
            return self.plugins[identifier]
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")

    def list_identifiers(self):
        return self.identifiers

    def list_active_commands(self):
        if self.active_plugin:
            return self.active_plugin.register_commands(self.active_plugin)
        else:
            raise ValueError("No active plugin set.")

def main():
    """
    Main Amalgam Loop. Configures Setup and SST. Processes Commands after Hearing Wakeword.
    """
    setup()

    # Initialize Speech Recognition and Text-to-Speech
    speech = Speech(VOSK_MODEL_DIR)
    sst = speech.sst

    # Initialize Plugin Controller
    controller = PluginController()
    controller.load_plugins()

    Output.tts("Amalgam is ready to receive commands.", Output.BLUE)

    while True:
        try:
            if idenfify_wakeword():
                command = sst().lower()
                process_command(command, controller)
        except Exception as e:
            print(f"Error during wake word detection: {e}")

def idenfify_wakeword() -> bool:
    """
    Returns True if the wake word "hey jarvis" is detected. Will run indefinitely until the wake word is detected.
    """
    # Config
    RATE = 16000  # openWakeWord and SpeechRecognition typically use 16kHz
    CHUNK_SIZE_WW = 1280 # Frame length for openWakeWord (16000 * 0.080s)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()

    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE_WW)

    stream.start_stream()

    try:
        while True:
            audio_data = stream.read(CHUNK_SIZE_WW, exception_on_overflow=False)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            # print("Model Prediction: ", model.predict(audio_array))

            prediction = model.predict(audio_array,
                                       threshold={"hey_jarvis": 0.5},
                                       debounce_time=0.75)
            if prediction["hey_jarvis"] > 0.5:
                return True
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        Output.tts("Exiting amalgam.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        exit(0)

def process_command(command: str, plugin_controller: PluginController):
    """
    Process the command and execute the corresponding plugin action.
    """
    # Identify the command using the trained model
    identified_command = identify_command(command)

    # Check if the identified command matches any plugin identifier
    if identified_command in plugin_controller.list_identifiers():
        plugin_controller.set_active_plugin(identified_command)
        plugin_controller.active_startup()
        plugin_controller.active_execute()
        plugin_controller.active_shutdown()
    elif not identified_command == "unknown":
        print(f"No matching plugin found for command: {command}")

def identify_command(command: str) -> str:
    """
    Identify the command using the trained model.
    """
    model_path = os.path.join(MODEL_DATA_DIR, "output", "model-last")

    nlp_trained = spacy.load(model_path)
    doc = nlp_trained(command)
    confidence = max(doc.cats, key=doc.cats.get)

    print(f"Identified command: {confidence} with confidence value: {doc.cats[confidence]}")
    if doc.cats[confidence] > 0.5:
        return confidence
    else:
        return "unknown"

# Setup and Configuration
def hash_check() -> bool:
    """
    Compares the current hash of the plugins directory with the stored hash in config_data.
    In the event of a mismatch, it updates the config_data with the new hash.
    """
    global config_data
    from dirhash import dirhash

    computed_hash = dirhash(PLUGINS_DIR, "sha256", match="*.py", ignore = ["__pycache__", "__init__.py"]) 

    print("Config Data: ", config_data)
    print("Plugins Directory Hash: ", computed_hash)

    if not config_data["plugin_hash"] == computed_hash:
        print("Plugin hash mismatch. Reinitializing plugins...")
        config_data["plugin_hash"] = computed_hash
        with open(os.path.join(USER_DATA_DIR, "config.json"), "w") as f:
            f.write(json.dumps(config_data))
        return False
    
    return True

def setup():
    """
    Setup function to initialize directories, load configuration, and train the model if necessary.
    """
    global config_data
    
    # Create Directories
    os.makedirs(PLUGIN_CONFIG_DIR, exist_ok = True)
    os.makedirs(PLUGINS_DIR, exist_ok = True)
    os.makedirs(MODEL_DATA_DIR, exist_ok = True)

    if not os.path.exists(os.path.join(PLUGINS_DIR, "__init__.py")):
        with open(os.path.join(PLUGINS_DIR, "__init__.py"), "w") as f:
            f.write("# This file is required to treat the plugins directory as a package.\n")

    if not os.path.exists(os.path.join(USER_DATA_DIR, "config.json")):
        with open(os.path.join(USER_DATA_DIR, "config.json"), "w") as f:
            f.write("{}")
 
    config_data = load_config(os.path.join(USER_DATA_DIR, "config.json"))
    
    # Train Amalgam if File is Missing
    if not os.path.exists(os.path.join(MODEL_DATA_DIR, "output", "model-last")) or not hash_check():
        print("Current Model Invalid. Training the model...")
        from src.trainer import train_model, generate_model_data

        generate_model_data()
        train_model()

if __name__ == "__main__":
    main()
