from src.speech_recognition.stt_tts import sst, tts
import os
import json
import importlib.util
import plugins.test as test_plugin

# Constants
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(SOURCE_DIR, "..")

PLUGINS_DIR = os.path.join(CORE_DIR, "plugins")
USER_DATA_DIR = os.path.join(CORE_DIR, "user_data")
PLUGIN_CONFIG_DIR = os.path.join(USER_DATA_DIR, "plugin_config")

class PluginController:
    def __init__(self):
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

    def get_plugin(self, identifier):
        if identifier in self.plugins:
            return self.plugins[identifier]
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")

def main():
    setup()

    controller = PluginController()
    controller.load_plugins()

    sample = controller.get_plugin("sample_plugin")
    
    print(sample.get_identifier(sample))
    print(sample.get_description(sample))
    sample.startup(sample)
    sample.execute(sample)
    sample.shutdown(sample)

    pass



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