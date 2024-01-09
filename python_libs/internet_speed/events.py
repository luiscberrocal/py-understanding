import time
from csv import DictWriter
from datetime import datetime
from pathlib import Path

from python_libs.internet_speed.schemas import SpeedSample


class Subject:
    """Represents what is being observed"""

    def __init__(self):

        """create an empty observer list"""

        self._observers = []

    def notify(self, modifier=None):

        """Alert the observers"""

        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

    def attach(self, observer):

        """If the observer is not in the list,
        append it into the list"""

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):

        """Remove the observer from the observer list"""

        try:
            self._observers.remove(observer)
        except ValueError:
            pass


class Observer:

    def __init__(self, file: Path) -> None:
        self.file = file

    def update(self, sample: SpeedSample):
        property_list = [sample.model_dump()]
        if self.file.exists():
            with open(self.file, 'w') as f:
                writer = DictWriter(f, fieldnames=list(property_list[0].keys()))
                writer.writeheader()
                writer.writerows(property_list)
        else:
            with open(self.file, 'a') as f:
                writer = DictWriter(f, fieldnames=list(property_list[0].keys()))
                writer.writerows(property_list)


if __name__ == '__main__':
    o_folder = Path(__file__).parent.parent.parent / "output"
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = o_folder / f"speed_test_{ts}.csv"

    now = datetime.now()
    sample: SpeedSample = SpeedSample(machine='Dell', download=120, upload=12, elapsed_time=30, date=now)
    sample1: SpeedSample = SpeedSample(machine='Dell', download=124, upload=13, elapsed_time=32, date=now)

    observer = Observer(json_file)
    observer.update(sample1)
    time.sleep(60)
    observer.update(sample)
