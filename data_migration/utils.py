"""Shared functionality of migration scripts."""


def execute_bash_command(command_args):
    print('Executing command:\n {command}\n...'.format(
        command=' '.join(command_args))
    )

    process = subprocess.Popen(
        command_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    if stderr:
        print(
            f'Command returned error information.\n  '
            f'stderr: {stderr.decode()}\n'
        )
    else:
        print('Command successful.\n')

    if stdout:
        print(f'  stdout: {stdout.decode()}')
