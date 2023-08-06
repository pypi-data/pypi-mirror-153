import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_content(content: str) -> None:
    clear_screen()
    print(content)
