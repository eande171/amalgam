from src.plugin import PluginController

plugin_queue = []

def add_plugin_to_queue(identifier: str) -> bool:
    """
    Adds a plugin to the queue to be executed next. 

    Args:
        identifier (str): The unique identifier of the plugin to added to the queue.
    Returns:
        bool: A boolean value which returns True if the plugin was successfully added
              and False if it was not added successfully.
    """
    try:
        print("Before:", plugin_queue)
        plugin_queue.append(identifier)
        print("After:", plugin_queue)
        return True
    except Exception:
        return False

def get_all_plugin_information() -> dict:
    """
    Retrieves the description for all registered plugins.

    This function iterates through all identifiers known to the PluginController,
    activates each plugin, and then fetches its description. The descriptions
    are stored in a dictionary where keys are plugin identifiers and values
    are their corresponding descriptions.

    Returns:
        dict: A dictionary where keys are plugin identifiers (str) and values
              are their descriptions (str).
    """
    plugin_dict: dict = {}

    for identifier in PluginController.list_identifiers():
        PluginController.set_active_plugin(identifier)
        plugin_dict[identifier] = PluginController.get_active_description()

    return plugin_dict
    
