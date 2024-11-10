#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
from datetime import datetime
from typing import Any


def fetch_timewarrior_data():
    try:
        timew_output = subprocess.check_output(['timew', 'export'], universal_newlines=True)
        timew_data = json.loads(timew_output)
        return timew_data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching TimeWarrior data: {e}")
        sys.exit(1)


def fetch_taskwarrior_data():
    try:
        task_output = subprocess.check_output(['task', 'export'], universal_newlines=True)
        task_data = json.loads(task_output)
        return task_data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching TaskWarrior data: {e}")
        sys.exit(1)


def parse_time_entries(timew_data, task_data):
    tasks = {task['uuid']: task for task in task_data}
    entries = []
    for interval in timew_data:
        tags = interval.get('tags', [])
        task_uuids = [tag[5:] for tag in tags if tag.startswith('task:')]
        for uuid in task_uuids:
            task = tasks.get(uuid)
            if task:
                start_time = datetime.fromisoformat(interval['start'])
                end_time = datetime.fromisoformat(interval.get('end', datetime.now().isoformat()))
                duration = end_time - start_time
                entries.append({
                    'Task UUID': uuid,
                    'Description': task.get('description', 'No Description'),
                    'Start': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'End': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Duration (HH:MM:SS)': str(duration)
                })
    return entries

def convert_to_datetime(date_str):
    return datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')

# Example usage

def parse_task_entries(*, time_data: list[dict[str, Any]], task_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    time_data_with_tasks = []
    for task in task_data:
        for interval in time_data:
            # print(interval)
            try:
                if task["project"] in interval.get("tags", []) and interval.get("project") is None:
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
                    interval["start"] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    interval["end"] = end_time.strftime('%Y-%m-%d %H:%M:%S')
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


def write_csv(time_entries: list[dict[str, Any]], filename: str='timew_taskw_report.csv'):
    fieldnames = ['Task UUID', 'Description', 'Start', 'End', 'Duration (HH:MM:SS)']
    fieldnames = time_entries[0].keys()
    try:
        with open(filename, mode='w', newline='') as csv_file:
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
    # entries = parse_time_entries(timew_data, task_data)
    if entries:
        write_csv(entries)
    else:
        print("No matching entries found between TimeWarrior and TaskWarrior.")


if __name__ == '__main__':
    main()
