import os
from colorama import Style, Fore
import sys


def clear_screen():
    if sys.platform.startswith("linux"):
        os.system("clear")

    elif sys.platform.lower().startswith("win"):
        os.system("cls")


def enter_confirmation(skip_enter_confirmation: bool = False):
    if not skip_enter_confirmation:
        input(f"{Fore.CYAN}Press enter to continue...{Style.RESET_ALL}")