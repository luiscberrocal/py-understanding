import json
import pickle
from pathlib import Path
from typing import Any, Dict, List

import nltk
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
        "classes": sorted(set(classes))
    }
    return results


def save_data(folder: Path, data: Dict[str, Any], format: str = "pickle") -> List[Path]:
    files = []
    if format == "pickle":
        action = "wb"
    elif format == "json":
        action = "w"
    else:
        raise ValueError(f'Unknown format: {format}')
    for key, value in data.items():
        lem_file = folder / f'{key}.{format}'
        with open(lem_file, action) as f:
            eval(f'{format}.dump(value, f)')
        files.append(lem_file)
    return files


if __name__ == '__main__':
    f = settings.APP_FOLDER / 'intents.json'
    wd = prep_word_data(f)
    wd_files = save_data(settings.MODEL_FOLDER, wd, format='json')
    for wdf in wd_files:
        print(f'Saved: {wdf}')
