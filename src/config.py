import json
import os

class Config:
    """
    Global configuration data for Amalgam.
    """
    _config_data = {}
    
    _default_config = {
        "ai_enabled": False,            # Can Amalgam use LLMs
        "ai_config": {
            "port": "1234",             # Port to be used
            "model": "",                # Model to be used
            "log_conversation": False,  # Can Amalgam save AI conversations 
        },
        "deafened": False,              # Can Amalgam get input from the microphone 
        "debug_logs": {
            "console": False,           # Are debug logs printed to the console
            "file": True                # Are debug logs saved to the log files
        },
        "ignore_words": [               # Ignore Words Commonly Misdetected During Silence. Only ignores word if it's alone.
            "the"
        ],
        "ignore_plugin_module": [       # Prevents Plugin Modules being Loaded. Ignores LLMs by default
            "llm"
        ], 
        "muted": False,                 # Can amalgam generate sounds
        "plugin_hash": "",              # Hash of Plugins Directory
    }

    @staticmethod
    def _load_config(default: dict, config_path: str) -> dict:
        """Load configuration from config.json or returns default values.
        
            Args:
                default (dict): Default configuration values.
                config_path (str): Path to the configuration file.

            Returns:
                dict: Merged configuration data.
        """

        config = {}

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as file:
                    config = json.load(file)
                    config = Config._merge_config(default, config)

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
    def _merge_config(default: dict, config: dict) -> dict:
        """
        Merges two configuration dictionaries, with the second overriding the first.

        Args:
            default (dict): The default configuration dictionary.
            config (dict): The configuration dictionary to merge with the default.

        Returns:
            dict: The merged configuration dictionary.
        """
        merged = default.copy()
        for key, value in config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = Config._merge_config(merged[key], value)
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
        Config._config_data = Config._load_config(Config._default_config, config_path)

    @staticmethod
    def set_data(key: str, value: dict) -> None:
        """
        Set a specific configuration value by key.
        
        Args:
            key (str): The key for the configuration value.
            value (dict): The value to set for the specified key.
        """
        Config._config_data[key] = value

    @staticmethod
    def save_data(config_path: str) -> None:
        """
        Save the current configuration data to a file.
        
        Args:
            config_path (str): Path to the configuration file where data will be saved.
        """
        try:
            with open(config_path, "w") as file:
                json.dump(Config._config_data, file, indent=4)
        except Exception as e:
            print(f"Error saving configuration data to {config_path}: {e}")

    @staticmethod
    def get_data_full() -> dict:
        """
        Get the full configuration data.
        
        Returns:
            dict: The full configuration data.
        """
        return Config._config_data
    
    @staticmethod
    def get_data(key: str) -> dict:
        """
        Get a specific configuration value by key.
        
        Args:
            key (str): The key for the configuration value.

        Returns:
            dict: The configuration value for the specified key.
        """
        return Config._config_data.get(key, None)
    
    @staticmethod
    def get_nested_data(keys: list) -> dict:
        """
        Get a specific configuration value by a list of keys.
        
        Args:
            keys (list): The list of keys for the configuration value.

        Returns:
            dict: The configuration value for the specified key.
        """
        current_data = Config.get_data_full()
        for key in keys:
            current_data = current_data.get(key, None)

        return current_data

