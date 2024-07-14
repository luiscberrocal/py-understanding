import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path

APP_FOLDER = Path(__file__).parent

MODEL_FOLDER = APP_FOLDER / 'model'
