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

# Running Amalgam
Simple steps to run **Amalgam**:
```batch
cd amalgam
.\venv\Scripts\activate
python -m src.main
```
For a list of current features, information on creating custom plugins / AI tools, check the [wiki](https://github.com/eande171/amalgam/wiki).
