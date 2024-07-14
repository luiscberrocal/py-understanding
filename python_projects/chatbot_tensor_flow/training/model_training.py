import importlib
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import nltk
import numpy as np
from nltk import RegexpTokenizer, WordNetLemmatizer

from python_projects.chatbot_tensor_flow import settings
from python_projects.chatbot_tensor_flow.core import get_intents


def install_nltk():
    nltk.download('punkt')
    nltk.download('wordnet')


def prep_word_data(intent_file: Path) -> Dict[str, List[Any]]:
    tokenizer = RegexpTokenizer(r'\w+')
    # tokenizer = WhitespaceTokenizer()
    words = []
    classes = []
    documents = []
    intents = get_intents(intent_file)
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            # word_list = nltk.word_tokenize(pattern)
            word_list = tokenizer.tokenize(pattern)
            words.extend(word_list)
            print(word_list)
            documents.append((word_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in settings.IGNORE_WORDS]
    results = {
        "words": sorted(set(words)),
        "classes": sorted(set(classes)),
        "documents": documents
    }
    return results


def save_data(folder: Path, data: Dict[str, Any], file_type: str = "pickle") -> List[Path]:
    files = []
    if file_type == "pickle":
        import pickle
        eval(f'import pickle')
        action = "wb"
    elif file_type == "json":
        import json
        importlib.import_module('json')
        action = "w"
    else:
        raise ValueError(f'Unknown format: {file_type}')
    for key, value in data.items():
        lem_file = folder / f'{key}.{file_type}'
        with open(lem_file, action) as f: # noqa
            eval(f'{file_type}.dump(value, f)')
        files.append(lem_file)
    return files


def training_data2(classes: List[str], documents: List[Tuple[List[str], str]], words: List[str]):
    lemmatizer = WordNetLemmatizer()
    training = []
    output_empty = [0] * len(classes)
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word) for word in pattern_words if word not in settings.IGNORE_WORDS]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])
    random.shuffle(training)
    training = np.array(training)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    return train_x, train_y

def training_data(classes: List[str], documents: List[Tuple[List[str], str]], words: List[str]):
    lemmatizer = WordNetLemmatizer()
    training = []
    output_empty = [0] * len(classes)
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word) for word in pattern_words if word not in settings.IGNORE_WORDS]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # Pad the bag list with zeros
        while len(bag) < len(output_empty):
            bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])
    random.shuffle(training)
    training = np.array(training)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    return train_x, train_y

if __name__ == '__main__':
    f = settings.APP_FOLDER / 'intents.json'
    wd = prep_word_data(f)
    ft = "json"
    wd_files = save_data(settings.MODEL_FOLDER, wd, file_type=ft)
    for wdf in wd_files:
        print(f'Saved: {wdf}')

    train_x, train_y = training_data(**wd)
    print(train_x)
