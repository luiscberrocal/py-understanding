import random
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

import click
import speedtest
from pydantic import BaseModel
from rich.progress import track

from python_libs.internet_speed.events import Observer
from python_libs.internet_speed.schemas import SpeedSample


class SpeedTestResult(BaseModel):
    pass


def bytes_to_mb(bytes: float) -> float:
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return bytes / MB


def check(verbose: bool) -> Tuple[float, float, float]:
    start_time = time.time()
    speed_test = speedtest.Speedtest()

    download_speed = bytes_to_mb(speed_test.download())
    if verbose:
        print(f"Your Download speed is {download_speed:.2f}")

    upload_speed = bytes_to_mb(speed_test.upload())
    if verbose:
        print(f"Your Upload speed is    {upload_speed:.2f}")
    elapsed_time = time.time() - start_time
    return download_speed, upload_speed, elapsed_time


if __name__ == '__main__':
    o_folder = Path(__file__).parent.parent.parent / "output"
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = o_folder / f"speed_test_{ts}.json"

    csv_file = o_folder / f"speed_test_{ts}.csv"
    observer = Observer(csv_file)
    # print(o_folder, o_folder.exists())

    total_runs = 12
    wait_minutes_max = 5
    for i in range(total_runs):
        sleep_seconds = int(60 * random.random() * wait_minutes_max)
        try:
            results = check(verbose=True)
            print(f"{i} Test took: {results[2]:.2f} seconds")

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            speed_result = {"machine": "Dell", "download": results[0], "upload": results[1],
                            "elapsed_time": results[2], "date": now}
            speed_sample = SpeedSample(**speed_result)
            observer.update(speed_sample)
            print('-' * 80)
            for _ in track(range(sleep_seconds), description=f"Sleeping for {sleep_seconds/60:.2f} minutes..."):
                time.sleep(1)  # Simulate work being done
        except speedtest.SpeedtestBestServerFailure as e:
            click.secho(f'Skipped {i} {e}', fg='red')
    # with open(json_file, "a") as f:
    #    json.dump(test_list, f)
    print(f'Finished')
