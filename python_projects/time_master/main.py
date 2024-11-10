#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
from datetime import datetime
from typing import Any


def fetch_timewarrior_data():
    try:
        timew_output = subprocess.check_output(
            ["timew", "export"], universal_newlines=True
        )
        timew_data = json.loads(timew_output)
        return timew_data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching TimeWarrior data: {e}")
        sys.exit(1)


def fetch_taskwarrior_data():
    try:
        task_output = subprocess.check_output(
            ["task", "export"], universal_newlines=True
        )
        task_data = json.loads(task_output)
        return task_data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching TaskWarrior data: {e}")
        sys.exit(1)


def convert_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


# Example usage


def parse_task_entries(
        *, time_data: list[dict[str, Any]], task_data: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    time_data_with_tasks = []
    for task in task_data:
        for interval in time_data:
            try:
                if (
                        task["project"] in interval.get("tags", [])
                        and interval.get("duration") is None
                ):
                    start_time = convert_to_datetime(interval["start"])
                    if interval.get("end"):
                        end_time = convert_to_datetime(interval["end"])
                        duration = end_time - start_time
                    else:
                        end_time = None
                        duration = None

                    interval["project"] = task["project"]
                    interval["description"] = task["description"]
                    interval["uuid"] = task["uuid"]
                    interval["start"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
                    if end_time is not None:
                        interval["end"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
                    interval["duration"] = str(duration)
                    print(interval)
                    print("-" * 120)
                    if duration is not None:
                        time_data_with_tasks.append(interval)
                    else:
                        print(f">>> Skipping entry without end time: {interval}")
            except Exception as e:
                print(f"Error parsing task entries: {e}, {interval} task: {task}")
                sys.exit(1)
    return time_data_with_tasks


def write_csv(
        time_entries: list[dict[str, Any]], filename: str = "timew_taskw_report.csv"
):
    fieldnames = ["Task UUID", "Description", "Start", "End", "Duration (HH:MM:SS)"]
    fieldnames = time_entries[0].keys()
    try:
        with open(filename, mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in time_entries:
                writer.writerow(entry)
        print(f"Report successfully written to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)


def main():
    timew_data = fetch_timewarrior_data()
    task_data = fetch_taskwarrior_data()
    entries = parse_task_entries(time_data=timew_data, task_data=task_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"timew_taskw_report_{timestamp}.csv"
    if entries:
        write_csv(entries, filename=report_file)
    else:
        print("No matching entries found between TimeWarrior and TaskWarrior.")


if __name__ == "__main__":
    main()
