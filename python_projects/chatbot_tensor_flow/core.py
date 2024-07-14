import json
import pickle
import random
from pathlib import Path
from typing import Dict, Any, List

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from python_projects.chatbot_tensor_flow import settings


def get_intents(file_path: Path) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def clean_up_sentence(sentence: str) -> List[str]:
    lemmatizer = WordNetLemmatizer()

    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

    return sentence_words


def bag_of_words(sentence: str, source_file: Path):
    with open(source_file, 'rb') as file:
        words = pickle.load(file)

    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence, model_file: Path, classes_file: Path, words_file: Path):
    with open(classes_file, 'rb') as file:
        classes = pickle.load(file)

    model = load_model(model_file)

    bow = bag_of_words(sentence, source_file=words_file)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []

    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list




def main():
    model_file = settings.MODEL_FOLDER / 'chatbot_model.keras'
    classes_file = settings.MODEL_FOLDER / 'classes.pickle'
    words_file = settings.MODEL_FOLDER / 'words.pickle'
    intents_file = settings.APP_FOLDER / 'intents.json'

    sentence = "How many gun models do you sell?"
    intents = predict_class(sentence, model_file, classes_file, words_file)
    print(intents)


if __name__ == '__main__':
    main()
