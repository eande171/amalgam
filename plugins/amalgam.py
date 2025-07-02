import time

from os import path

from src.main import LLM_TOOL_DIR, LLM_PROMPT_DIR, CONVERSATION_LOG_DIR, idenfify_wakeword
from src.llm import LLM
from src.plugin import Plugin, PluginController
from src.speech_recognition.stt_tts import Input, Output
from src.config import Config

def run_plugin_queue(queue):
    for plugin in queue:
        PluginController.set_active_plugin(plugin)
        PluginController.active_startup()
        PluginController.active_execute()
        PluginController.active_shutdown()

using_ai = False

class Stop(Plugin):
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
    
class AIConversation(Plugin):
    def startup(self):
        Output.tts("What would you like to talk about?")

    def execute(self):
        conversation = LLM.construct_chat(path.join(LLM_PROMPT_DIR, "converse.md"))

        log_text = ""

        while True:
            if idenfify_wakeword() or Config.get_data("deafened"):
                text = Input.sst().lower()

                if text in ["exit", "quit", "stop"]:
                    break
                if text == "":
                    continue
                else:
                    conversation.add_user_message(text)
                    response = LLM.query(conversation)
                    conversation.add_assistant_response(response)

                    log_text += f"User: {text}\nAmalgam: {response}\n"

                    Output.tts(str(response))

        if Config.get_nested_data(["ai_config", "log_conversation"]):
            time_value = time.localtime()
            time_string = time.strftime("%Y-%m-%d_%H-%M", time_value)

            file_name = str(LLM.query(LLM.construct_chat(path.join(LLM_PROMPT_DIR, "file_name.md"), log_text)))
            file_name += f"_{time_string}.log"

            with open(path.join(CONVERSATION_LOG_DIR, file_name), "w") as file:
                file.write("# -- Chat Logs -- #\n" + log_text)

            print(f"Output saved to: {file_name}")

    def shutdown(self):
        Output.tts("Our conversation has finished.")

    def get_identifier(self):
        return "ai_conversation"

    def register_commands(self):
        return [
            "I'd like to talk to you",
            "I'd like to start a conversation",
            "Start a conversation",
            "Can I ask you a question?",
            "I have a question.",
            "Let's chat",
            "Talk to me",
            "Open a dialogue",
            "Initiate conversation",
            "Engage in conversation",
            "Speak with you",
            "I need to ask something",
            "Query",
            "Ask a question"
        ]

    def get_description(self):
        return "This plugin allows you to have a conversation with the local LLM"


class UseAI(Plugin):
    def startup(self):
        global using_ai
        using_ai = True
        Output.tts("AI Mode Activated.")
    
    def execute(self):
        global using_ai
        from llm_data.tools.plugins import plugin_queue

        plugin_queue.clear()
        while using_ai:
            try:
                if idenfify_wakeword() or Config.get_data("deafened"):
                    text = Input.sst().lower()
                    if text:
                        # LLM.query_with_tools("For the following input, use a tool to determine what plugin identifier is needed for each command? Then please add the plugin to the queue. Think step by step. Input: " + text, LLM.get_tools(LLM_TOOL_DIR))
                        LLM.query_with_tools(LLM.construct_chat(path.join(LLM_PROMPT_DIR, "default.md"), text), LLM.get_tools(LLM_TOOL_DIR))

                        print(plugin_queue)
                        run_plugin_queue(plugin_queue)

                        plugin_queue.clear()
                    elif text == "":
                        Output.tts("No search query provided.", Output.YELLOW)
            except KeyboardInterrupt:
                Output.tts("Stopping LLM Usage.")
                break

        PluginController.set_active_plugin("use_ai")
    
    def shutdown(self):
        global using_ai
        using_ai = False
    
    def get_identifier(self):
        return "use_ai"
    
    def register_commands(self):
        return [
            "I'd like to use AI.",
            "Start AI mode.",
            "Enable AI for plugins.",
            "Can you enable AI for me?",
            "Please switch to AI-powered plugin execution.",
            "Let's use AI for running plugins.",
            "Turn on AI capabilities.",
            "Use AI from now on.",
            "Use AI",
        ]
    
    def get_description(self):
        return "This plugin will force amalgam to use AI (LLM + tools) to run the plugins from now on."
    
class RetireAI(Plugin):
    def startup(self):
        pass
    
    def execute(self):
        global using_ai
        if using_ai:
            Output.tts("Disabling AI...")
            using_ai = False
        else:
            Output.tts("AI is not active.")
            
    def shutdown(self):
        pass
    
    def get_identifier(self):
        return "retire_ai"
    
    def register_commands(self):
        return [
            "I'd like to stop using AI.",
            "Disable AI mode.",
            "Turn off AI for plugins.",
            "Can you disable AI for me?",
            "Please switch off AI-powered plugin execution.",
            "Let's stop using AI for running plugins.",
            "Turn off AI capabilities."
        ]
    
    def get_description(self):
        return "This plugin will stop amalgam from using AI (LLM + tools) to run the plugins from now on."
