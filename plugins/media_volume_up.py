from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        pyautogui.press("volumeup")

    def shutdown(self):
        Output.tts("Volume increased.")

    def get_identifier(self):
        return "media_volume_up"

    def register_commands(self):
        return [
            "Increase volume.",
            "Raise volume level.",
            "Turn up the volume.",
            "Boost audio volume.",
            "Amplify sound output.",
            "Enhance audio level.",
            "Make it louder.",
            "Volume up.",
            "Increase sound volume.",
            "Raise audio level."
        ]

    def get_description(self):
        return "This plugin increases the volume using the system's media controls."