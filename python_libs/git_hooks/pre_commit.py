#!/usr/bin/env python3
import subprocess
import sys

def get_branch_name():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()

def get_commit_message():
    return subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()

branch_name = get_branch_name()
# Extract the first four letters after the slash
prefix = branch_name.split('/')[-1][:4]

commit_message = get_commit_message()

if not commit_message.startswith(prefix):
    print(f'Error: Commit message should start with the first four letters of the feature branch name ({prefix}).')
    sys.exit(1)