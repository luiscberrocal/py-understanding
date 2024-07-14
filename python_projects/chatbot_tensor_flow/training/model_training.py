from pathlib import Path

import nltk
from nltk import RegexpTokenizer, WordNetLemmatizer

from python_projects.chatbot_tensor_flow import settings
from python_projects.chatbot_tensor_flow.core import get_intents


def train_model(intent_file: Path):
    # nltk.download('punkt')
    nltk.download('wordnet')
    tokenizer = RegexpTokenizer(r'\w+')
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
if __name__ == '__main__':
    f = settings.APP_FOLDER / 'intents.json'
    train_model(f)
