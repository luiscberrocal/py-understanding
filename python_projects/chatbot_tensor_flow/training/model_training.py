from pathlib import Path

from python_projects.chatbot_tensor_flow import settings
from python_projects.chatbot_tensor_flow.core import get_intents


def train_model(intent_file: Path):
    intents = get_intents(intent_file)
    print(intents)


if __name__ == '__main__':
    f = settings.APP_FOLDER / 'intents.json'
    train_model(f)
