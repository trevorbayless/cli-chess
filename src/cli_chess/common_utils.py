import os

def is_unix_system():
    """Returns True if on a unix system"""
    return False if os.name == "nt" else True


def clear_screen():
    """Sends a clear command based on operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')
