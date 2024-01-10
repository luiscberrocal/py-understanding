import time
from csv import DictWriter
from pathlib import Path

from rich.progress import track

from .schemas import SpeedSample


class Observer:

    def __init__(self, file: Path) -> None:
        self.file = file

    def update(self, sample: SpeedSample):
        property_list = [sample.model_dump()]
        if not self.file.exists():
            with open(self.file, 'w') as f:
                writer = DictWriter(f, fieldnames=list(property_list[0].keys()))
                writer.writeheader()
                writer.writerows(property_list)
        else:
            with open(self.file, 'a') as f:
                writer = DictWriter(f, fieldnames=list(property_list[0].keys()))
                writer.writerows(property_list)


if __name__ == '__main__':
    sleep_seconds = int(3 * 60)
    for i in track(range(sleep_seconds), description=f"Sleeping for {sleep_seconds / 60} minutes..."):
        time.sleep(1)  # Simulate work being done
