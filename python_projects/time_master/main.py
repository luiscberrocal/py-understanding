#!/usr/bin/env python3

import csv
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Any


def fetch_data(command: list[str]) -> list[dict[str, Any]]:
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return json.loads(output)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching data with command {command}: {e}")
        sys.exit(1)


def convert_to_datetime(date_str: str) -> datetime:
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date string {date_str} is not in a recognized format")


def parse_task_entries(time_data: list[dict[str, Any]], task_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    time_data_with_tasks = []
    for task in task_data:
        for interval in time_data:
            try:
                if task["project"] in interval.get("tags", []) and interval.get("duration") is None:
                    start_time = convert_to_datetime(interval["start"])
                    end_time = convert_to_datetime(interval["end"]) if interval.get("end") else None
                    duration = (end_time - start_time) if end_time else None

                    interval.update({
                        "project": task["project"],
                        "description": task["description"],
                        "uuid": task["uuid"],
                        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end": end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None,
                        "duration": str(duration) if duration else None,
                        "user": os.getenv("USER")
                    })

                    if duration:
                        time_data_with_tasks.append(interval)
                    else:
                        print(f">>> Skipping entry without end time: {interval}")
            except Exception as e:
                print(f"Error parsing task entries: {e}, {interval} task: {task}")
                sys.exit(1)
    return time_data_with_tasks


def write_csv(time_entries: list[dict[str, Any]], filename: str = "timew_taskw_report.csv"):
    fieldnames = time_entries[0].keys()
    try:
        with open(filename, mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(time_entries)
        print(f"Report successfully written to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)


def main():
    timew_data = fetch_data(["timew", "export"])
    task_data = fetch_data(["task", "export"])
    entries = parse_task_entries(time_data=timew_data, task_data=task_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"timew_taskw_report_{timestamp}.csv"
    if entries:
        write_csv(entries, filename=report_file)
    else:
        print("No matching entries found between TimeWarrior and TaskWarrior.")


if __name__ == "__main__":
    main()