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
            "Stop running.",
            "Go offline.",
            "Cease operations.",
            "Turn yourself off.",
            "I need you to shut down.",
            "Prepare for shutdown.",
            "Initiate shutdown sequence.",
            "Are you able to stop?",
            "Power down now.",
            "Completely shut down.",
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
            "Reload Amalgam's config.",
            "Refresh Amalgam's settings.",
            "Update Amalgam's configuration.",
            "Apply changes to Amalgam.",
            "Please reload the config.",
            "Can you refresh the configuration?",
            "I need you to update the settings.",
            "Make the config changes apply.",
            "Bring in the new settings.",
            "Load the latest configuration.",
            "Rescan the config file.",
            "Sync config from file.",
            "Process config file.",
            "Reinitialize config.",
            "Reread the configuration file.",
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
            "Save config file.",
            "Save the settings.",
            "Store the settings.",
            "Write settings to file.",
            "Save the current settings.",
            "Please save the config.",
            "Can you save the configuration?",
            "Make sure to save the settings.",
            "Put these changes into effect permanently.",
            "Ensure these settings are permanent.",
            "Save configuration.",
            "Write the config.",
            "Persist the config.",
            "Store the configuration.",
            "Write settings.",
            "Save the current state.",
            "I need to save the config.",
            "Don't lose these changes.",
            "Make sure to save everything.",
            "Can you write the configuration?",
        ]

    def get_description():
        return "This plugin saves the configuration file."

'''
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
            "Stop picking up my voice.",
            "Stop listening.",
            "Deafen Amalgam.",
            "Stop Amalgam from listening.",
            "Turn off speech recognition.",
            "Could you disable audio input?",
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
            "Undeafen.",
            "Turn on speech recognition.",
            "Start recognizing my voice.",
            "Listen for my commands.",
            "Come online.",
        ]

    def get_description():
        return "This plugin undeafens amalgam so it can use the microphone."

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
            "Mute Amalgam.",
            "Please be silent.",
            "Stop talking.",
            "Shut up.",
            "Turn off your voice.",
            "Disable your sound.",
            "Can you go silent?",
            "I need you to be quiet.",
            "Silence the output.",
            "No more sound.",
            "Mute the audio.",
            "Disable voice output.",
            "Stop voice playback.",
            "Turn off Amalgam's sound.",
            "Disable Amalgam's audio.",
            "Amalgam, be quiet.",
            "Amalgam, shut up.",
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
            "Unmute Amalgam.",
            "Please speak again.",
            "Start talking.",
            "Enable your voice.",
            "Turn your sound back on.",
            "Can you talk now?",
            "I want to hear you.",
            "Restore the audio output.",
            "Allow sound.",
            "Turn on your speech.",
            "Enable voice output.",
            "Begin voice playback.",
            "Bring the sound back.",
        ]

    def get_description():
        return "This plugin unmutes amalgam so it starts producing sound."
'''


class Retrain(Plugin):
    def startup():
        Output.tts("Retraining intent recognition.")

    def execute():
        from src.trainer import train_model, generate_model_data

        hash_check()
        generate_model_data()
        train_model()

    def shutdown():
        pass

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
            "Train the model.",
            "Retrain Amalgam's model.",
            "Update the intent model.",
            "Re-train the intent classifier.",
            "Update the recognition model.",
            "Refresh the recognition engine.",
            "Can you retrain the model?",
            "Please train the model again.",
            "Redo the training"
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
            "Reload all plugins.",
            "Refresh all extensions.",
            "Update all add-ons.",
            "Re-read plugins.",
            "Force plugin reload.",
            "Initiate plugin reload.",
            "Can you reload the plugins?",
            "Please refresh the extensions.",
        ]

    def get_description():
        return "This plugin reloads amalgam's plugins. Note that it does not retrain anything."