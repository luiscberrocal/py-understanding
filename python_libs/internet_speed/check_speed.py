import time
from typing import Tuple

import speedtest

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
    results = check(verbose=True)
    print(f"Test took: {results[2]:.2f} seconds")