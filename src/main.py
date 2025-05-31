from src.speech_recognition.stt_tts import sst, tts
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

    model_path = os.path.join(MODEL_DATA_DIR, "output", "model-last")

    try:
        nlp_trained = spacy.load(model_path)

        doc = nlp_trained("Turn on the lights for me please.")
        print("DOC:", doc)
        print("CATS:", doc.cats)
        # print("ENTS:", doc.ents[1].label_)

        # Check if the model is loaded correctly    


    except OSError:
        print(f"Model not found at {model_path}. Please train the model first.")
        return
    pass



def setup():
    # Create Directories
    os.makedirs(PLUGIN_CONFIG_DIR, exist_ok = True)
    os.makedirs(PLUGINS_DIR, exist_ok = True)
    os.makedirs(MODEL_DATA_DIR, exist_ok = True)

    if not os.path.exists(os.path.join(PLUGINS_DIR, "__init__.py")):
        with open(os.path.join(PLUGINS_DIR, "__init__.py"), "w") as f:
            f.write("# This file is required to treat the plugins directory as a package.\n")

    # Train Amalgam if File is Missing
    if not os.path.exists(os.path.join(MODEL_DATA_DIR, "output", "model-last")):
        print("Model not found. Training the model...")
        from src.trainer import train_model, generate_model_data

        generate_model_data()
        train_model()

if __name__ == "__main__":
    main()