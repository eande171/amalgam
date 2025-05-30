import spacy
import spacy.cli
import spacy.cli.download
import spacy.cli.init_config
from spacy.tokens import DocBin
import random
from src.main import PluginController
import os

# Get Sentence Data
plugin_controller = PluginController()
plugin_controller.load_plugins()

spacy_train_data = []
all_labels = set()

# Associate Idenfifiers with Commands
for identifier in plugin_controller.list_identifiers():
    plugin_controller.set_active_plugin(identifier)
    commands = plugin_controller.list_active_commands()

    print(f"Processing plugin: {identifier} with commands: {commands}")

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
#if not os.path.exists("en_core_web_sm"):
#spacy.cli.download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

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
train_doc_bin.to_disk(os.path.join("model_data", "train.spacy")) 

test_doc_bin = convert_to_docbin(test_data)
test_doc_bin.to_disk(os.path.join("model_data", "dev.spacy"))

print("Training data and test data saved to 'model_data/train.spacy' and 'model_data/dev.spacy' respectively.")

# Train the model