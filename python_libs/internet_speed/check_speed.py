import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

import click
from pydantic import BaseModel
from rich.live import Live
from rich.progress import track
from rich.spinner import Spinner
from rich.text import Text
from speedtest import Speedtest, SpeedtestBestServerFailure

from .events import Observer
from .schemas import SpeedSample


class SpeedTestResult(BaseModel):
    pass


def bytes_to_mb(size_bytes: float) -> float:
    kb = 1024  # One Kilobyte is 1024 bytes
    mb = kb * 1024  # One MB is 1024 KB
    return size_bytes / mb


def check(speed_test: Speedtest, verbose: bool) -> Tuple[float, float, float]:
    start_time = time.time()

    spinner = Spinner('dots3', text=Text('Checking download speed...', style='green'))
    with Live(spinner, transient=True):
        download_speed = bytes_to_mb(speed_test.download())
    if verbose:
        print(f"Your Download speed is {download_speed:.2f}")

    spinner = Spinner('dots3', text=Text('Checking upload speed...', style='green'))
    with Live(spinner, transient=True):
        upload_speed = bytes_to_mb(speed_test.upload())
    if verbose:
        print(f"Your Upload speed is    {upload_speed:.2f}")
    elapsed_time = time.time() - start_time
    return download_speed, upload_speed, elapsed_time


def load_environment_variables(environment_filename: str):
    from dotenv import load_dotenv
    from pathlib import Path

    def find_envs_folder(current_dir: Path):
        env_folder = current_dir / '.envs'
        if env_folder.exists():
            return env_folder
        else:
            return find_envs_folder(current_dir.parent)

    environment_folder = find_envs_folder(Path(__file__).parent)
    environment_file = environment_folder / environment_filename
    load_dotenv(dotenv_path=environment_file)


def getting_best_server():
    spinner = Spinner('dots3', text=Text('Instantiating test...', style='green'))
    with Live(spinner, transient=True):
        speed_test = Speedtest()
    spinner = Spinner('dots3', text=Text('Checking best server...', style='green'))
    with Live(spinner, transient=True):
        best = speed_test.best
    print(f'Sponsor: {best["sponsor"]}')
    print(f'Latency: {best["latency"]}')

    return speed_test


if __name__ == '__main__':
    load_environment_variables('internet_speed_vars.txt')

    sp_test = getting_best_server()

    o_folder = Path(__file__).parent.parent.parent / "output"
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = o_folder / f"speed_test_{ts}.json"

    csv_file = o_folder / f"speed_test_{ts}.csv"
    observer = Observer(csv_file)
    # print(o_folder, o_folder.exists())

    total_runs = int(os.getenv('INTERNET_SPEED_RUNS'))
    wait_minutes_max = int(os.getenv('INTERNET_SPEED_WAIT_MAX'))
    machine_name = os.getenv('INTERNET_SPEED_MACHINE')
    for i in range(total_runs):
        sleep_seconds = int(60 * random.random() * wait_minutes_max)
        try:
            results = check(speed_test=sp_test, verbose=True)
            print(f"{i} Test took: {results[2]:.2f} seconds")

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            speed_result = {"machine": machine_name, "download": results[0], "upload": results[1],
                            "elapsed_time": results[2], "date": now}
            speed_sample = SpeedSample(**speed_result)
            observer.update(speed_sample)
            print('-' * 80)
            for _ in track(range(sleep_seconds), description=f"Sleeping for {sleep_seconds / 60:.2f} minutes...",
                           transient=True):
                time.sleep(1)  # Simulate work being done
        except SpeedtestBestServerFailure as e:
            click.secho(f'Skipped {i} {e}', fg='red')
    # with open(json_file, "a") as f:
    #    json.dump(test_list, f)
    print(f'Finished')
