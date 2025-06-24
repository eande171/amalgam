import json
import os

default_config = {
    "plugin_hash": "",
}

def load_config(config_path):
    """Load configuration from config.json or returns default values."""

    config = {}

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as file:
                config = json.load(file)
                config = merge_config(default_config, config)

            with open(config_path, "w") as file:
                file.write(json.dumps(config))
        
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {config_path}. File may be corrupt or invalid. Using default configuration.")
            config = default_config
        except Exception as e:
            print(f"Error reading configuration file {config_path}: {e}. Using default configuration.")
            config = default_config
    
    return config

def merge_config(default, config):
    merged = default.copy()
    for key, value in config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged