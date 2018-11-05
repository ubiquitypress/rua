# -*- coding: utf-8 -*-
"""Script for copying Rua instances' files and media from servers to AWS s3."""
import os
import sys

from utils import execute_bash_command


REMOTE_DATABASE_USER = os.getenv('REMOTE_DATABASE_USER')
REMOTE_DATABASE_PASS = os.getenv('REMOTE_DATABASE_PASS')
REMOTE_DATABASE_HOST = os.getenv('REMOTE_DATABASE_HOST')
REMOTE_SERVER_SSH_USER = os.getenv('REMOTE_SERVER_SSH_USER')
USER_SSH_KEY_PATH = os.getenv('USER_SSH_KEY_PATH')
LOCAL_FILES_DIRECTORY = os.getenv('LOCAL_FILES_DIRECTORY')
REMOTE_FILES_DIRECTORY = os.getenv('REMOTE_FILES_DIRECTORY')


def copy_press_files_to_local(press_code):
    remote_files_subdirectory = os.path.join(REMOTE_FILES_DIRECTORY, press_code)
    copy_files_command_args = [
        'scp',
        '-r',
        '-i',
        USER_SSH_KEY_PATH,
        f'{REMOTE_SERVER_SSH_USER}@{REMOTE_DATABASE_HOST}'
        f':{remote_files_subdirectory}',
        LOCAL_FILES_DIRECTORY,
    ]
    print('Copying remote files to local machine.\n')
    execute_bash_command(copy_files_command_args)


def migrate_press_files_to_s3(press_code):
    copy_press_files_to_local(press_code)


def migrate_presses_files_to_s3(press_codes):
    for press_code in press_codes:
        migrate_press_files_to_s3(press_code)


if __name__ == '__main__':
    migrate_presses_files_to_s3(sys.argv[1:])
