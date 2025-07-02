from src.speech_recognition.stt_tts import Output
from src.main import CONFIG_FILE, hash_check
from src.plugin import Plugin, PluginController
from src.config import Config

class Stop(Plugin):
    def startup():
        pass

    def execute():
        print("Stopping amalgam...")
        Output.tts("Amalgam is shutting down.")

    def shutdown():
        import sys
        sys.exit(0)

    def get_identifier():
        return "stop_self"

    def register_commands():
        return [
            "Stop amalgam.",
            "Terminate amalgam.",
            "Halt amalgam.",
            "End amalgam.",
            "Power off amalgam.",
            "Shut down amalgam.",
            "Stop yourself.",
            "Shut yourself down.",
            "Stop running"
        ]

    def get_description():
        return "This plugin stops the amalgam program when triggered"

class ReloadConfig(Plugin):
    def startup():
        pass

    def execute():
        print("Reloading Config...")
        Config.init(CONFIG_FILE)

    def shutdown():
        Output.tts("Amalgam has reloaded the configuration file.")

    def get_identifier():
        return "reload_config"

    def register_commands():
        return [
            "Reload the config.",
            "Refresh the config.",
            "Apply the changes from the config.",
            "Load the config into memory.",
            "Hot reload the config file."
        ]

    def get_description():
        return "This plugin reloads the configuration file so that changes to the config apply to the whole program."
    
class SaveConfig(Plugin):
    def startup():
        pass

    def execute():
        print("Saving current state to Config...")
        Config.save_data(CONFIG_FILE)

    def shutdown():
        Output.tts("Amalgam has saved the configuration file.")

    def get_identifier():
        return "save_config"

    def register_commands():
        return [
            "Save the config.",
            "Save changes to the config.",
            "Save the changes from the config.",
            "Save the config into memory.",
            "Make these changes permanent.",
        ]

    def get_description():
        return "This plugin saves the configuration file."

class Deafen(Plugin):
    def startup():
        pass

    def execute():
        Config.set_data("deafened", True)

    def shutdown():
        Output.tts("Amalgam has been deafened.")

    def get_identifier():
        return "deafen"

    def register_commands():
        return [
            "Stop listening to me.",
            "I don't want you listening anymore.",
            "Deafen yourself.",
            "Mute microphone.",
            "Turn off mic.",
            "Disable microphone."
            "Go deaf.",
            "Cease listening.",
            "Disable microphone input.",
            "Don't listen.",
            "Block audio input.",
            "Stop picking up my voice."
        ]

    def get_description():
        return "This plugin deafens amalgam so it no longer uses the microphone."

class Undeafen(Plugin):
    def startup():
        pass

    def execute():
        Config.set_data("deafened", False)

    def shutdown():
        Output.tts("Amalgam has been undeafened.")

    def get_identifier():
        return "undeafen"

    def register_commands():
        return [
            "Start listening to me.",
            "I want you listening again.",
            "Undeafen yourself.",
            "Unmute microphone.",
            "Turn on mic.",
            "Enable microphone."
            "Hear me.",
            "Enable microphone input.",
            "Listen again.",
            "Unblock audio input.",
            "Start picking up my voice.",
            "Wake up.",
            "Listen closely.",
            "Enable audio input.",
            "Resume listening.",
            "I'm ready for you to hear me.",
            "Undeafen."
        ]

    def get_description():
        return "This plugin undeafens amalgam so it can use the microphone."
    pass

class Mute(Plugin):
    def startup():
        pass

    def execute():
        Config.set_data("muted", True)

    def shutdown():
        Output.tts("Amalgam has been muted.")

    def get_identifier():
        return "mute"

    def register_commands():
        return [
            "Silence yourself.",
            "Go quiet.",
            "Hold your tongue.",
            "Don't speak.",
            "Cut the audio output.",
            "Mute yourself",
        ]

    def get_description():
        return "This plugin mutes amalgam so it no longer produces sound."

class Unmute(Plugin):
    def startup():
        pass

    def execute():
        Config.set_data("muted", False)

    def shutdown():
        Output.tts("Amalgam has been unmuted.")

    def get_identifier():
        return "unmute"

    def register_commands():
        return [
            "Speak up.",
            "Talk to me.",
            "Make some noise.",
            "Restore audio.",
            "Let me hear you.",
            "Unmute yourself",
        ]

    def get_description():
        return "This plugin unmutes amalgam so it starts producing sound."

class Retrain(Plugin):
    def startup():
        Output.tts("Retraining intent recognition.")

    def execute():
        from src.trainer import train_model, generate_model_data

        hash_check()
        generate_model_data()
        train_model()

    def shutdown():
        Output.tts("Amalgam has been retrained.")

    def get_identifier():
        return "retrain"

    def register_commands():
        return [
            "Retrain the model.",
            "Refresh intent data.",
            "Rebuild intent recognition.",
            "Train again.",
            "Learn from new data.",
            "Recalibrate the intent model.",
            "Initiate intent training.",
        ]

    def get_description():
        return "This plugin retrains amalgam's intent recognition model."

class ReloadPlugins(Plugin):
    def startup():
        Output.tts("Reloading Amalgam's plugins.")

    def execute():
        PluginController.reload_plugins()
        PluginController.set_active_plugin("reload_plugins")

    def shutdown():
        Output.tts("Amalgam's plugins have been reloaded.")

    def get_identifier():
        return "reload_plugins"

    def register_commands():
        return [
            "Reload plugins.",
            "Refresh extensions.",
            "Restart modules.",
            "Update add-ons.",
            "Rescan plugins.",
            "Apply plugin changes.",
            "Scan for new plugins.",
        ]

    def get_description():
        return "This plugin reloads amalgam's plugins. Note that it does not retrain anything."