from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        pyautogui.press("volumedown")

    def shutdown(self):
        Output.tts("Volume decreased.")

    def get_identifier(self):
        return "media_volume_down"

    def register_commands(self):
        return [
            "Decrease volume.",
            "Lower volume level.",
            "Turn down the volume.",
            "Reduce audio volume.",
            "Diminish sound output.",
            "Lower audio level.",
            "Make it quieter.",
            "Volume down.",
            "Decrease sound volume.",
            "Lower audio level."
        ]

    def get_description(self):
        return "This plugin decreases the volume using the system's media controls."