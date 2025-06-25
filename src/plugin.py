from abc import ABC, abstractmethod

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

# Plugin API

