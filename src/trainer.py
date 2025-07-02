import os
import sys
import subprocess
import random
import spacy
from spacy.tokens import DocBin
from src.plugin import PluginController
from src.config import Config
import logging

logger = logging.getLogger(__name__)

def generate_model_data():
    spacy_train_data = []
    all_labels = set()

    # Associate Idenfifiers with Commands
    for identifier in PluginController.list_identifiers():
        PluginController.set_active_plugin(identifier)
        commands = PluginController.list_active_commands()

        logger.debug(f"Processing plugin: {identifier} with commands: {commands}")

        for command in commands:
            cats = {label: False for label in all_labels}
            all_labels.add(identifier)
            cats[identifier] = True
            spacy_train_data.append((command, {"cats": cats}))

    # print("Data: ", spacy_train_data)

    updated_spacy_train_data = []
    for text, annotations in spacy_train_data:
        current_cats = annotations["cats"]
        full_cats = {label: current_cats.get(label, False) for label in all_labels}
        updated_spacy_train_data.append((text, {"cats": full_cats}))

    spacy_train_data = updated_spacy_train_data

    # print("Data New: ", spacy_train_data)

    # Prepare Training and Test Data
    random.shuffle(spacy_train_data)

    train_split = int(len(spacy_train_data) * 0.8)
    train_data = spacy_train_data[:train_split]
    test_data = spacy_train_data[train_split:]

    # Load the English NLP model
    model = "en_core_web_md"
    try: 
        nlp = spacy.load(model)
    except OSError:
        spacy.cli.download(model)
        nlp = spacy.load(model)
    except Exception as e:
        logger.critical(f"Unhandled error: {e}")

    # Add Text Categoriser
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    # Add labels to the text categoriser
    for label in all_labels:
        textcat.add_label(label)

    # Convert to DocBin
    def convert_to_docbin(data):
        doc_bin = DocBin()
        for text, annotations in data:
            doc = nlp.make_doc(text)
            doc.cats = annotations["cats"]
            doc_bin.add(doc)
        return doc_bin

    # Save Training and Test Data
    train_doc_bin = convert_to_docbin(train_data)
    train_doc_bin.to_disk(os.path.join("intent_model_data", "train.spacy"))

    test_doc_bin = convert_to_docbin(test_data)
    test_doc_bin.to_disk(os.path.join("intent_model_data", "dev.spacy"))

    logger.info("Training data and test data saved to 'intent_model_data/train.spacy' and 'intent_model_data/dev.spacy' respectively.")

# Train the model
def train_model():
    python_executable = sys.executable

    '''if Config.get_data("efficient_training"):
        optimise = "efficiency"
    else:
        optimise = "accuracy"

        model = "en_core_web_lg"
        try: 
            spacy.load(model)
        except OSError:
            spacy.cli.download(model)
        except Exception as e:
            logger.critical(f"Unhandled error: {e}")

    try:
        subprocess.run([
            python_executable, "-m", "spacy", "init", "config",
            "intent_model_data/config.cfg", "--lang", "en",
            "--pipeline", "textcat",
            "--optimize", optimise, "--force"
        ])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error initializing config: {e}")
        return'''
    

    try:
        subprocess.run([
            python_executable, "-m", "spacy", "train",
            "intent_model_data/config.cfg",
            "--output", "intent_model_data/output",
            "--paths.train", "intent_model_data/train.spacy",
            "--paths.dev", "intent_model_data/dev.spacy"
        ])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error training model: {e}")
        return