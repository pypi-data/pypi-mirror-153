import subprocess

def exec_command(cmd):
    return subprocess.getoutput(cmd)


def get_git_name():
    return exec_command("git config user.name")


def get_git_email():
    return exec_command("git config user.email")


def get_name():
    email = get_git_email()
    name = get_git_name()
    if email:
        return email
    else:
        return name
