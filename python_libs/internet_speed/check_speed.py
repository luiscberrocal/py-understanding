import json
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

import speedtest
from pydantic import BaseModel


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
        print(f"Your Upload speed is {upload_speed:.2f}")
    elapsed_time = time.time() - start_time
    return download_speed, upload_speed, elapsed_time


if __name__ == '__main__':
    o_folder = Path(__file__).parent.parent.parent / "output"
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = o_folder / f"speed_test_{ts}.json"

    # print(o_folder, o_folder.exists())
    test_list = []
    total_runs = 12
    wait_minutes_max = 5
    for i in range(total_runs):
        sleep_seconds = 60 * random.randint(0, wait_minutes_max)
        results = check(verbose=True)
        print(f"{i} Test took: {results[2]:.2f} seconds")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        speed_result = {"machine": "Dell", "download": results[0], "upload": results[1],
                        "elapsed_time": results[2], "date": now}
        test_list.append(speed_result)
        print(f'Sleeping for {sleep_seconds/60:.2f} minutes')
        print('-' * 80)
        if (total_runs-1) != i:
            time.sleep(sleep_seconds)

    with open(json_file, "a") as f:
        json.dump(test_list, f)
    print(f'Finished {json_file}')