from os import path, makedirs
from time import sleep
from dirhash import dirhash
import logging

from openwakeword.model import Model
from openwakeword.utils import download_models

import pyaudio
import numpy as np

import spacy

from src.speech_recognition.stt_tts import Input, Output
from src.config import Config
from src.logger import setup_logging

# Constants
SOURCE_DIR = path.dirname(path.abspath(__file__))
CORE_DIR = path.join(SOURCE_DIR, "..")

MODEL_DATA_DIR = path.join(CORE_DIR, "intent_model_data")
USER_DATA_DIR = path.join(CORE_DIR, "user_data")
LLM_DATA_DIR = path.join(CORE_DIR, "llm_data")
PLUGINS_DIR = path.join(CORE_DIR, "plugins")

VOSK_MODEL_DIR = path.join(SOURCE_DIR, "speech_recognition", "model")

PLUGIN_CONFIG_DIR = path.join(USER_DATA_DIR, "plugin_config")
CONFIG_FILE = path.join(USER_DATA_DIR, "config.json")
LOG_DIR = path.join(USER_DATA_DIR, "logs")

download_models(["hey_jarvis"])
model = Model(["hey_jarvis"], inference_framework="onnx", vad_threshold=0.5)

from src.plugin import PluginController

logger = logging.getLogger(__name__)

def main():
    """
    Main Amalgam Loop. Configures Setup and SST. Processes Commands after Hearing Wakeword.
    """
    setup_logging()

    setup()

    if not Config.get_data("deafened"):
        Input.setup()

    Output.tts("Amalgam is ready to receive commands.", Output.GREEN)

    while True:
        try:
            if idenfify_wakeword() or Config.get_data("deafened"):
                command = Input.sst().lower()
                try:
                    process_command(command)
                except Exception as e: 
                    logger.error(f"Error processing command: {e}")
                    Output.tts("An error occurred while processing your command.", Output.RED)
        except Exception as e:
            logger.error(f"Error during wake word detection: {e}")

def idenfify_wakeword() -> bool:
    """
    Returns True if the wake word "hey jarvis" is detected. Will run indefinitely until the wake word is detected.
    """
    if Config.get_data("deafened"):
        return False

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

            prediction = model.predict(audio_array,
                                       threshold={"hey_jarvis": 0.5},
                                       debounce_time=0.75)
            if prediction["hey_jarvis"] > 0.5:
                return True
            else:
                sleep(0.1)
    except KeyboardInterrupt:
        Output.tts("Exiting amalgam.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        exit(0)

def process_command(command: str):
    """
    Process the command and execute the corresponding plugin action.
    """
    # Identify the command using the trained model
    identified_command = identify_command(command)

    # Check if the identified command matches any plugin identifier
    if identified_command in PluginController.list_identifiers():
        PluginController.set_active_plugin(identified_command)
        PluginController.active_startup()
        PluginController.active_execute()
        PluginController.active_shutdown()
    elif identified_command == "unknown":
        logger.info(f"No matching plugin found for command: {command}")

def identify_command(command: str) -> str:
    """
    Identify the command using the trained model.
    """
    model_path = path.join(MODEL_DATA_DIR, "output", "model-last")

    nlp_trained = spacy.load(model_path)
    doc = nlp_trained(command)
    confidence = max(doc.cats, key=doc.cats.get)

    logger.info(f"Identified command: {confidence} with confidence value: {doc.cats[confidence]}")
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
    computed_hash = dirhash(PLUGINS_DIR, "sha256", match="*.py", ignore = ["__pycache__", "__init__.py"]) 

    logger.debug(f"Config Data: {Config.get_data_full()}")
    logger.debug(f"Plugins Directory Hash: {computed_hash}")

    if not Config.get_data("plugin_hash") == computed_hash:
        logger.info("Plugin hash mismatch. Reinitializing plugins...")

        Config.set_data("plugin_hash", computed_hash)
        Config.save_data(CONFIG_FILE)

        return False
    
    return True

def setup():
    """
    Setup function to initialize directories, load configuration, and train the model if necessary.
    """
    
    # Create Directories
    makedirs(PLUGIN_CONFIG_DIR, exist_ok = True)
    makedirs(PLUGINS_DIR, exist_ok = True)
    makedirs(MODEL_DATA_DIR, exist_ok = True)
    makedirs(LLM_DATA_DIR, exist_ok = True)

    # Create Required Files
    if not path.exists(path.join(PLUGINS_DIR, "__init__.py")):
        with open(path.join(PLUGINS_DIR, "__init__.py"), "w") as f:
            f.write("# This file is required to treat the plugins directory as a package.\n")

    if not path.exists(path.join(LLM_DATA_DIR, "__init__.py")):
        with open(path.join(LLM_DATA_DIR, "__init__.py"), "w") as f:
            f.write("# This file is required to treat the plugins directory as a package.\n")

    if not path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            f.write("{}")
    
    Config.init(CONFIG_FILE)
    PluginController.load_plugins()

    # Train Amalgam if File is Invalid or does not exist
    if not path.exists(path.join(MODEL_DATA_DIR, "output", "model-last")) or not hash_check():
        logger.info("Current Model Invalid. Training the model...")
        from src.trainer import train_model, generate_model_data

        generate_model_data()
        train_model()

if __name__ == "__main__":
    main()


