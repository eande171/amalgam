from abc import ABC, abstractmethod
from os import path, listdir
from importlib import import_module

# Plugin Class
class Plugin(ABC):
    @abstractmethod
    def startup(self):
        """Runs when the plugin is loaded."""
        raise NotImplementedError("Plugin initialization not implemented.")

    @abstractmethod
    def execute(self):
        """Runs when the plugin is executed."""
        raise NotImplementedError("Plugin execution not implemented.")

    @abstractmethod
    def shutdown(self):
        """Runs when the plugin is stopped/program is shutdown."""
        raise NotImplementedError("Plugin shutdown not implemented.")

    @abstractmethod
    def get_identifier(self) -> str:
        """Returns the unique identifier for the plugin."""
        raise NotImplementedError("Plugin identifier not implemented.")

    @abstractmethod
    def register_commands(self) -> list[str]:
        """Returns a list of commands that the program registers ON TRAINING."""
        raise NotImplementedError("Plugin command registration not implemented.")

    @abstractmethod
    def get_description(self) -> str:
        """Returns a human-readable/AI-readable description of the plugin."""
        raise NotImplementedError("Plugin description not implemented.")

class PluginController:
    active_plugin = None
    identifiers = []
    plugins = {}

    @staticmethod
    def load_plugins():
        from src.main import PLUGINS_DIR

        if not path.exists(PLUGINS_DIR):
            raise FileNotFoundError(f"Plugins directory '{PLUGINS_DIR}' does not exist.")
        
        for file in listdir(PLUGINS_DIR):
            if file.endswith(".py") and not file == "__init__.py":
                plugin_name = file[:-3]
                print(f"Loading plugin: {plugin_name}")

                # Import the Plugin Class
                plugin = import_module(f"plugins.{plugin_name}")
                plugin_class = getattr(plugin, "Plugin", None)

                print(f"Plugin Name: {plugin_class.get_identifier(plugin_class)}")
                PluginController.plugins[plugin_class.get_identifier(plugin_class)] = plugin_class

                PluginController.identifiers.append(plugin_class.get_identifier(plugin_class))

    @staticmethod
    def set_active_plugin(identifier):
        if identifier in PluginController.plugins:
            PluginController.active_plugin = PluginController.get_plugin(identifier)
        else:
            raise ValueError(f"Plugin with identifier '{identifier}' not found.")

    @staticmethod    
    def get_active_identifier():
        if PluginController.active_plugin:
            return PluginController.active_plugin.get_identifier(PluginController.active_plugin)
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def get_active_description():
        if PluginController.active_plugin:
            return PluginController.active_plugin.get_description(PluginController.active_plugin)
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_startup():
        if PluginController.active_plugin:
            PluginController.active_plugin.startup(PluginController.active_plugin)
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_execute():
        if PluginController.active_plugin:
            PluginController.active_plugin.execute(PluginController.active_plugin)
        else:
            raise ValueError("No active plugin set.")

    @staticmethod    
    def active_shutdown():
        if PluginController.active_plugin:
            PluginController.active_plugin.shutdown(PluginController.active_plugin)
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
            return PluginController.active_plugin.register_commands(PluginController.active_plugin)
        else:
            raise ValueError("No active plugin set.")
