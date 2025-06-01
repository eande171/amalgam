from src.speech_recognition.stt_tts import Speech
import os
import importlib

import spacy

# Constants
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(SOURCE_DIR, "..")

PLUGINS_DIR = os.path.join(CORE_DIR, "plugins")
MODEL_DATA_DIR = os.path.join(CORE_DIR, "model_data")
USER_DATA_DIR = os.path.join(CORE_DIR, "user_data")
PLUGIN_CONFIG_DIR = os.path.join(USER_DATA_DIR, "plugin_config")

VOSK_MODEL_DIR = os.path.join(SOURCE_DIR, "speech_recognition", "model")

TRIGGER_PHRASE = ["hey amalgam", "hello amalgam", "hi amalgam", "hey computer", "hello computer", "hi computer", "hey jarvis", "hello jarvis", "hi jarvis", "amalgam", "jarvis", "computer"]

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
    setup()

    # Initialize Speech Recognition and Text-to-Speech
    speech = Speech(VOSK_MODEL_DIR)
    sst = speech.sst
    tts = speech.tts

    # Initialize Plugin Controller
    controller = PluginController()
    controller.load_plugins()

    while True:
        try:
            text = sst(VOSK_MODEL_DIR).lower()
            if not text:
                continue

            found_trigger = None
            for trigger in TRIGGER_PHRASE:
                if trigger in text:
                    found_trigger = trigger
                    break

            if found_trigger:
                trigger_start_index = text.find(found_trigger)
                text = text[trigger_start_index + len(found_trigger):].strip()
                
                print(f"Trigger found: {found_trigger}")
                print(f"Command text: {text}")

                process_command(text, controller)

        except Exception as e:
            print(f"Error during speech recognition: {e}")
            break

    '''controller = PluginController()
    controller.load_plugins()

    controller.set_active_plugin("sample_plugin")
    print(controller.get_active_identifier())
    print(controller.get_active_description())
    controller.active_startup()
    controller.active_execute()
    controller.active_shutdown()
    print(controller.list_identifiers())
    print(controller.list_active_commands())'''

    '''model_path = os.path.join(MODEL_DATA_DIR, "output", "model-last")

    try:
        nlp_trained = spacy.load(model_path)

        doc = nlp_trained("Turn on the lights for me please.")
        print("DOC:", doc)
        print("CATS:", doc.cats)

        confidence = max(doc.cats, key=doc.cats.get)
        print("Confidence:", confidence, "with value:", doc.cats[confidence])

        # print("ENTS:", doc.ents[1].label_)
        # Check if the model is loaded correctly    


    except OSError:
        print(f"Model not found at {model_path}. Please train the model first.")
        return
    pass'''

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
        # return f"Executed command: {identified_command}"
    elif not identified_command == "unknown":
        print(f"No matching plugin found for command: {command}")
        # return f"No matching plugin found for command: {command}"


def identify_command(command: str) -> str:
    model_path = os.path.join(MODEL_DATA_DIR, "output", "model-last")

    nlp_trained = spacy.load(model_path)
    doc = nlp_trained(command)
    confidence = max(doc.cats, key=doc.cats.get)

    print(f"Identified command: {confidence} with confidence value: {doc.cats[confidence]}")
    if doc.cats[confidence] > 0.8:
        return confidence
    else:
        return "unknown"



def setup():
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

    # Train Amalgam if File is Missing
    if not os.path.exists(os.path.join(MODEL_DATA_DIR, "output", "model-last")):
        print("Model not found. Training the model...")
        from src.trainer import train_model, generate_model_data

        generate_model_data()
        train_model()

if __name__ == "__main__":
    main()