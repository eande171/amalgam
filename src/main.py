from src.speech_recognition.stt_tts import sst, tts
import os
import json

# Constants
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(SOURCE_DIR, "..")

PLUGINS_DIR = os.path.join(CORE_DIR, "plugins")
USER_DATA_DIR = os.path.join(CORE_DIR, "user_data")
PLUGIN_CONFIG_DIR = os.path.join(USER_DATA_DIR, "plugin_config")


def main():
    setup()
    pass

def load_plugins():
    """Loads all plugins"""


def setup():
    # Create Directories
    os.makedirs(PLUGIN_CONFIG_DIR, exist_ok = True)
    os.makedirs(PLUGINS_DIR, exist_ok = True)

    if not os.path.exists(os.path.join(PLUGINS_DIR, "__init__.py")):
        with open(os.path.join(PLUGINS_DIR, "__init__.py"), "w") as f:
            f.write("# This file is required to treat the plugins directory as a package.\n")


    # # Train Amalgam if File is Missing

if __name__ == "__main__":
    main()