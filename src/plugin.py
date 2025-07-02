import logging
from src.speech_recognition.stt_tts import Output

from abc import ABC, abstractmethod
from os import path, listdir
from importlib import import_module
import inspect

logger = logging.getLogger(__name__)

# Plugin Class
class Plugin(ABC):
    @abstractmethod
    def startup():
        """Runs when the plugin is loaded."""
        raise NotImplementedError("Plugin initialization not implemented.")

    @abstractmethod
    def execute():
        """Runs when the plugin is executed."""
        raise NotImplementedError("Plugin execution not implemented.")

    @abstractmethod
    def shutdown():
        """Runs when the plugin is stopped/program is shutdown."""
        raise NotImplementedError("Plugin shutdown not implemented.")

    @abstractmethod
    def get_identifier() -> str:
        """Returns the unique identifier for the plugin."""
        raise NotImplementedError("Plugin identifier not implemented.")

    @abstractmethod
    def register_commands() -> list[str]:
        """Returns a list of commands that the program registers ON TRAINING."""
        raise NotImplementedError("Plugin command registration not implemented.")

    @abstractmethod
    def get_description() -> str:
        """Returns a human-readable/AI-readable description of the plugin."""
        raise NotImplementedError("Plugin description not implemented.")

class PluginController:
    active_plugin: Plugin = None
    identifiers = []
    plugins = {}

    @staticmethod
    def load_plugins():
        from src.main import PLUGINS_DIR
        from src.config import Config

        if not path.exists(PLUGINS_DIR):
            logger.critical("Plugins directory is missing. Cannot load plugins.")
            raise FileNotFoundError(f"Plugins directory '{PLUGINS_DIR}' does not exist.")
        
        for file in listdir(PLUGINS_DIR):
            if file.endswith(".py") and not file == "__init__.py":
                plugin_name = file[:-3]
                
                if plugin_name in Config.get_data("ignore_plugin_module"):
                    continue
                
                logger.info(f"Loading plugin: {Output.BLUE} {plugin_name}")

                module = import_module(f"plugins.{plugin_name}")

                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        if issubclass(obj, Plugin) and obj is not Plugin:
                            logger.info(f"Loading plugin:   {Output.BLUE} {name}{Output.RESET} from {obj}")

                            PluginController.plugins[obj.get_identifier()] = obj

                            PluginController.identifiers.append(obj.get_identifier())

    @staticmethod
    def set_active_plugin(identifier):
        if identifier in PluginController.plugins:
            PluginController.active_plugin = PluginController.get_plugin(identifier)
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")

    @staticmethod    
    def get_active_identifier():
        if PluginController.active_plugin:
            return PluginController.active_plugin.get_identifier()
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def get_active_description():
        if PluginController.active_plugin:
            return PluginController.active_plugin.get_description()
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_startup():
        if PluginController.active_plugin:
            PluginController.active_plugin.startup()
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_execute():
        if PluginController.active_plugin:
            PluginController.active_plugin.execute()
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_shutdown():
        if PluginController.active_plugin:
            PluginController.active_plugin.shutdown()
        else:
            raise ValueError("No active plugin set.")

    @staticmethod
    def get_plugin(identifier):
        if identifier in PluginController.plugins:
            return PluginController.plugins[identifier]
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")

    @staticmethod
    def list_identifiers():
        return PluginController.identifiers

    @staticmethod
    def list_active_commands():
        if PluginController.active_plugin:
            return PluginController.active_plugin.register_commands()
        else:
            raise ValueError("No active plugin set.")
        
    @staticmethod
    def reload_plugins():
        PluginController.active_plugin = None
        PluginController.identifiers.clear()
        PluginController.plugins.clear()

        PluginController.load_plugins()

