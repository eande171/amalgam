
<img src="./amalgam.svg" width="25%">

# AMALGAM
**A**utonomous
**M**odular 
**A**gent for 
**L**anguage based 
**G**lobal 
**A**ctions and 
**M**anagement

## Amalgam's Principle
**Amalgam** is a fully local AI Assistant. From speech recognition to using LLMs, it all happens privately on your machine.  The entire system is designed to be modular, and mostly automated, requiring little setup or downloads. 

# Installation and Setup
## Requirements
**NOTE: Amalgam**, whilst being fully local, ***DOES***, download important files when starting for the first time. Requirements also need to be installed. Internet access **will** be required for both.

---

**Amalgam** has been built using [Python version **3.13.3**](https://www.python.org/downloads/release/python-3133/), so it is recommended to download or update to this version to ensure the most reliable experience.

## Download Amalgam
Download the most recent release [here](https://github.com/eande171/amalgam/releases/)

## Create Virtual Environment 
It is **HIGHLY** recommended you setup and run a virtual environment (venv):
```batch
cd amalgam
python -m venv venv
```
Activate the venv by running: `.\venv\Scripts\activate`, you should see (venv) in the terminal. 

## Install Dependencies
After activating the virtual environment, run the following: 
```batch
cd amalgam
python -m pip install -r .\requirements.txt
```
## Setup Amalgam
Running **Amalgam** for the first time requires an internet connection. This will:
- Download the required models **(requires internet)**
- Generate default folders & config
- Train the intent recognition model

**Optional for running, but required for all speech recognition:**
- Prompt you to install **(requires internet)** a VOSK (speech recognition) model

## Selecting a VOSK Model
**NOTE:** Installing a VOSK model is *"optional"* but highly recommended as it allows you to use plugins with just your voice. 
 
**Amalgam** requires you to have a VOSK model installed in the `src/speech_recognition/model` directory. VOSK models can be obtained [here](https://alphacephei.com/vosk/models). I recommend at least: [vosk-model-en-us-0.22-lgraph](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) which can be understood by **Amalgam** with decent accuracy. Obviously, the higher the model, the more accurate speech recognition, at the cost of higher RAM usage. 

# Using LLMs 
**NOTE:** Using (local) Large Language Models is **entirely optional** and not required for **Amalgam** to function. They can, however, improve the quality of the program/your experience.

**Amalgam** uses [LM Studio](https://lmstudio.ai/) as the backend and requires models to be installed either through their (LM Studio's) CLI or through the desktop application. For amalgam to load the model you'd like to use, you need to include it in `user_data/config.json`. My config for AI looks similar to the following (without comments):
```python
"ai_enabled": true,                   # This must be enabled for any AI usage (IMPORTANT)
"ai_config": {
    "port": "1234",                   # The localhost port running the LLM server
    "model": "qwen2.5-7b-instruct",   # The default identifier used by LM Studio (IMPORTANT)
    "log_conversation": true          # Can a conversation be saved to a file
    "llm_recognition": true           # Can the LLM be used if intent recognition fails
}
```
You can choose whichever model you like, making sure to update the config to use the model, although I recommend one with at least 7 billion parameters. The server will start automatically if AI is invoked and will close after it is no longer required. Occasionally, the server may fail to close. If AI is used again, it should resolve this issue. Otherwise, the server can be closed through the LM Studio GUI or by running `lms server stop`.

There are also some LLM plugins which have been disabled by default. This includes both a conversation plugin  and "Use AI" plugin. The conversation plugin allows you to have a conversation with it, just like any other LLM. The output will be saved to `user_data/conversation_log` if `"log_conversation"` is set to True. 

The "Use AI" plugin skips the default intent recognition and uses AI for everything. I don't personally recommend it as it is generally unnecessary but the option to enable it is there. **NOTE:** The "Use AI" plugin requires you have an LLM that is trained for tools. It **will NOT** work correctly without it. 

To enable the LLM module, go to `user_data/config.json` and remove `"llm"` from `"ignore_plugin_module"`

# Running Amalgam
Simple steps to run **Amalgam**:
```batch
cd amalgam
.\venv\Scripts\activate
python -m src.main
```

# Using Amalgam
1. Say the wake word `hey jarvis` (just like "hey google" or "hey siri"), Amalgam will indicate it is listening.
2. Give it an instruction like: `play me some music` or `search the web`.

That's it! 

For a list of current features, information on creating custom plugins / AI tools, check the [wiki](https://github.com/eande171/amalgam/wiki).
