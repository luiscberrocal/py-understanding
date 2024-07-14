import json
import pickle
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import nltk
import numpy as np
from nltk import RegexpTokenizer, WordNetLemmatizer

from python_projects.chatbot_tensor_flow import settings
from python_projects.chatbot_tensor_flow.core import get_intents

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

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
            # print(word_list)
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
        action = "wb"
        dump = pickle.dump
    elif file_type == "json":
        dump = json.dump
        action = "w"
    else:
        raise ValueError(f'Unknown format: {file_type}')
    for key, value in data.items():
        lem_file = folder / f'{key}.{file_type}'
        with open(lem_file, action) as f:  # noqa
            dump(value, f)
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


def training_data(classes: List[str], documents: List[Tuple[List[str], str]],
                  words: List[str]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    lemmatizer = WordNetLemmatizer()
    training = []
    output = []
    output_empty = [0] * len(classes)
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word) for word in pattern_words if word not in settings.IGNORE_WORDS]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append(bag)
        output.append(output_row)
    random.shuffle(training)
    random.shuffle(output)
    training = np.array(training)
    output = np.array(output)
    train_x = list(training)
    train_y = list(output)
    return train_x, train_y


def build_model(train_x: List[np.ndarray], train_y: List[np.ndarray]) -> Sequential:
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    # sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    sgd = SGD(learning_rate=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model


if __name__ == '__main__':
    f = settings.APP_FOLDER / 'intents.json'
    wd = prep_word_data(f)
    ft = "pickle"
    wd_files = save_data(settings.MODEL_FOLDER, wd, file_type=ft)
    for wdf in wd_files:
        print(f'Saved: {wdf}')

    tr_x, tr_y = training_data(**wd)
    model = build_model(tr_x, tr_y)

    model.fit(np.array(tr_x), np.array(tr_y), epochs=200, batch_size=5, verbose=1)

    model.save(settings.MODEL_FOLDER / 'chatbot_model.keras')
