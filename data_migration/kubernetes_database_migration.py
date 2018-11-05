from datetime import date
import os
import subprocess

from .mysql_to_postgresql import copy_from_mysqldb_to_postgresdb

FROM_DATABASE_USER = os.getenv('FROM_DATABASE_USER'),
FROM_DATABASE_PASS = os.getenv('FROM_DATABASE_PASS'),
FROM_DATABASE_HOST = os.getenv('FROM_DATABASE_HOST'),
TO_DATABASE_USER = os.getenv('TO_DATABASE_USER'),
TO_DATABASE_PASS = os.getenv('TO_DATABASE_PASS'),
TO_DATABASE_HOST = os.getenv('TO_DATABASE_HOST'),
REMOTE_DATABASE_USER = os.getenv('REMOTE_DATABASE_USER'),
REMOTE_DATABASE_PASS = os.getenv('REMOTE_DATABASE_PASS'),
REMOTE_DATABASE_HOST = os.getenv('REMOTE_DATABASE_HOST'),
DATABASE_DUMP_DIRECTORY = os.getenv('DATABASE_DUMP_DIRECTORY')


def migrate_rua_database(press_code):
    copy_from_mysqldb_to_postgresdb(
        mysql_db_name=f'rua_{press_code}',
        mysql_user=FROM_DATABASE_USER,
        mysql_pass=FROM_DATABASE_PASS,
        mysql_host=FROM_DATABASE_HOST,
        postgres_db_name=press_code,
        postgres_user=TO_DATABASE_USER,
        postgres_pass=TO_DATABASE_PASS,
        postgres_host=TO_DATABASE_HOST,
    )


def dump_remote_database(press_code):
    """Runs a bash command run copy the databases from a remote host via ssl."""

    subprocess.run(
        [
            'ssh',
            REMOTE_DATABASE_HOST,
            'mysqldump',
            press_code,
            '>',
            f'{str(date.today())}_{press_code}.sql',
            '--single-transaction',
            '-u',
            REMOTE_DATABASE_USER,
            f'-p{REMOTE_DATABASE_PASS}'
        ]
    )

