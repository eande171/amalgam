import logging
import subprocess
import importlib
import inspect

from os import path, listdir

import lmstudio as lms

from src.config import Config
from src.speech_recognition.stt_tts import Output


logger = logging.getLogger(__name__)

def lm_server_handler(func):
    def wrapper(*args, **kwargs):
        if not Config.get_data("ai_enabled"):
            logger.info("LLM Usage has been disabled.")
            return

        LLM._start_server()
        result = func(*args, **kwargs)
        LLM._stop_server()
        return result

    return wrapper

class LLM:
    ai_data = Config.get_data("ai_config")
    local_address = "localhost:" + ai_data["port"]

    @staticmethod
    def _silent_run(command, shell=False):
        """
        Runs a command, hiding output unless an error occurs.

        Args:
            command (list or str): The command to run.
                                    If shell=True, this should be a string.
                                    If shell=False, this should be a list of strings.
            shell (bool): Whether to execute the command through the shell.
        """
        try: 
            result = subprocess.run(
                command, 
                capture_output=True,  # Capture stdout and stderr
                text=True,            # Decode stdout and stderr as text
                check=False,          # Do not raise CalledProcessError
                shell=shell           # Whether to use the shell
            )

            if result.returncode != 0:
                logger.error(f"Error executing command: {' '.join(command) if isinstance(command, list) else command}")
                logger.error(f"Standard Output:\n{result.stdout}")
                logger.error(f"Standard Error:\n{result.stderr}")
        except FileNotFoundError:
            print(f"Error: Command not found: {' '.join(command) if isinstance(command, list) else command}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def _start_server():
        logger.debug("Starting LMS Server...")
        LLM._silent_run(["lms", "server", "start", "--port", LLM.ai_data["port"]])

    @staticmethod
    def _stop_server():
        logger.debug("Stopping LMS Server...")
        LLM._silent_run(["lms", "server", "stop"])

    @staticmethod
    def get_tools(directory: str) -> list:
        if not path.exists(directory):
            logger.error(f"{directory} is missing. Cannot load tools.")
            raise FileNotFoundError(f"Directory '{directory}' does not exist.")
        
        tools = []

        for file in listdir(directory):
            if file.endswith(".py") and not file == "__init__.py":
                tool_name = file[:-3]
                logger.debug(f"Loading tool: {tool_name}")

                module = importlib.import_module(f"llm_data.tools.{tool_name}")

                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj) and not name.startswith('_'):
                        tools.append(obj)

        return tools

    @staticmethod
    def construct_chat(system_dir: str, user_text: str = "") -> lms.Chat:
        """
        Constructs an LM Studio chat object with a system message loaded from a file
        and an initial user message. In the event the file is missing, the default will be used.

        Args:
            system_dir (str): The file path to the text file containing the system prompt.
                              This prompt sets the initial behavior or persona for the AI.
            user_text (str): The initial message from the user to start the conversation.

        Returns:
            lms.Chat: A configured LM Studio chat object ready for interaction,
                    containing both the system message and the first user message.
        """
        default_prompt = "# Purpose \
                            You are Amalgam, an assistant similar to JARVIS. Your job is to use the tools you have available to you to assist the user as best as possible. \
                            You must follow the rules at all times. Under no condition are you to break these rules. \
                            # Rules \
                            - You must not, under any circumstance, attempt to create or use a plugin that does not exist. \
                            - You should use a tool to determine what plugin identifier is needed for each command, then please add the plugin to the queue. \
                            - Think step by step. \
                            # Advice \
                            Use the get_all_plugin_information tool to find out more about what you can control. \
                            If someone requests you \"shut yourself down\", they are most likely asking you to run stop_self."

        system_text: str = ""
        try:
            with open(system_dir, "r") as file:
                system_text = file.read()
        except FileNotFoundError:
            logger.warning(f"File not found: {system_dir}, using default prompt.")
            system_text = default_prompt
        except Exception as e:
            logger.error(f"An unhandled exception has occurred: {e}, using default prompt.")
            system_text = default_prompt
            
        chat = lms.Chat(system_text)
        chat.add_user_message(user_text)
        return chat

    @staticmethod
    @lm_server_handler
    def query(query, format = None) -> str:
        with lms.Client(LLM.local_address) as client:
            model = client.llm.model(LLM.ai_data["model"])
            return model.respond(query, response_format=format)

    @staticmethod
    @lm_server_handler
    def query_with_tools(query, tools) -> str:
        with lms.Client(LLM.local_address) as client:
            model = client.llm.model(LLM.ai_data["model"])
            model.act(
                query,
                tools,
                on_prediction_completed=logger.debug
            )
