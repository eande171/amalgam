import json
import os

class Config:
    """
    Global configuration data for Amalgam.
    """
    config_data = {}
    
    default_config = {
        "plugin_hash": "",
    }

    @staticmethod
    def load_config(default: object, config_path: str) -> object:
        """Load configuration from config.json or returns default values.
        
            Args:
                default (object): Default configuration values.
                config_path (str): Path to the configuration file.

            Returns:
                object: Merged configuration data.
        """

        config = {}

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as file:
                    config = json.load(file)
                    config = Config.merge_config(default, config)

                with open(config_path, "w") as file:
                    file.write(json.dumps(config))

            except json.JSONDecodeError:
                print(f"Error decoding JSON from {config_path}. File may be corrupt or invalid. Using default configuration.")
                config = default
            except Exception as e:
                print(f"Error reading configuration file {config_path}: {e}. Using default configuration.")
                config = default

        return config

    @staticmethod
    def merge_config(default: object, config: object) -> object:
        """
        Merges two configuration dictionaries, with the second overriding the first.

        Args:
            default (object): The default configuration dictionary.
            config (object): The configuration dictionary to merge with the default.

        Returns:
            object: The merged configuration dictionary.
        """
        merged = default.copy()
        for key, value in config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = Config.merge_config(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    @staticmethod
    def init(config_path: str) -> None:
        """
        Initialize the configuration by loading it from a file or using default values.
        
        Args:
            config_path (str): Path to the configuration file.
        """
        Config.config_data = Config.load_config(Config.default_config, config_path)

    @staticmethod
    def set_data(key: str, value: object) -> None:
        """
        Set a specific configuration value by key.
        
        Args:
            key (str): The key for the configuration value.
            value (object): The value to set for the specified key.
        """
        Config.config_data[key] = value

    @staticmethod
    def save_data(config_path: str) -> None:
        """
        Save the current configuration data to a file.
        
        Args:
            config_path (str): Path to the configuration file where data will be saved.
        """
        try:
            with open(config_path, "w") as file:
                json.dump(Config.config_data, file, indent=4)
        except Exception as e:
            print(f"Error saving configuration data to {config_path}: {e}")

    @staticmethod
    def get_data_full() -> object:
        """
        Get the full configuration data.
        
        Returns:
            object: The full configuration data.
        """
        return Config.config_data
    
    @staticmethod
    def get_data(key: str) -> object:
        """
        Get a specific configuration value by key.
        
        Args:
            key (str): The key for the configuration value.

        Returns:
            object: The configuration value for the specified key.
        """
        return Config.config_data.get(key, None)