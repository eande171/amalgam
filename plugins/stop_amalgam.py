from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        print("Stopping amalgam...")
        Output.tts("Amalgam is shutting down.")

    def shutdown(self):
        import sys
        sys.exit(0)

    def get_identifier(self):
        return "stop_self"

    def register_commands(self):
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

    def get_description(self):
        return "This plugin stops the amalgam program when triggered"