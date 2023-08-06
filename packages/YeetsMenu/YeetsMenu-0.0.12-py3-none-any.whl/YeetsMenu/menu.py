import typing

from colorama import Style, Fore
from YeetsMenu.generics.selectable import Selectable
from YeetsMenu.utils import utils
from YeetsMenu.option import Option


class Menu(Selectable):
    def __init__(self, title, colors: list = None):
        super().__init__(title)

        self.options: typing.Dict[int, Selectable] = {0: Option("Exit this menu", exec, "return", skip_enter_confirmation=True)}
        self.colors: typing.List

        if colors is None:
            self.colors = [Fore.BLUE, Fore.MAGENTA]
        else:
            self.colors = colors

    def add_selectable(self, selectable: Selectable):
        self.options[len(self.options)] = selectable

    def __invalid__input__(self):
        print(f"{Fore.RED}Invalid input, retry!{Style.RESET_ALL}")
        utils.enter_confirmation()

    def run(self):
        while True:
            utils.clear_screen()
            options: typing.List[typing.AnyStr] = []
            counter = 0
            for key, value in self.options.items():
                value: Selectable

                if counter % 2 == 0:
                    color_to_show = self.colors[0]
                else:
                    color_to_show = self.colors[1]

                options.append(f"    {Fore.CYAN}{key}{Fore.LIGHTMAGENTA_EX}){color_to_show} {value.name}{Style.RESET_ALL}")
                counter += 1

            menu_string = "\n".join(options)

            print(f"""{Fore.LIGHTMAGENTA_EX}{self.name}{Style.RESET_ALL}
        
{Fore.CYAN}Options:{Style.RESET_ALL}
{menu_string}
                  """)

            print()
            option_selected = input(f"{Fore.LIGHTMAGENTA_EX}Select a option: {Fore.CYAN}")
            print(Style.RESET_ALL)

            try:
                if len(option_selected) == 0:
                    raise KeyError("Internal_error")

                try:
                    option_selected = int(option_selected)
                except ValueError:
                    self.__invalid__input__()
                    continue

                if option_selected == 0:
                    return

                real_option: Selectable = self.options[option_selected]
            except KeyError:
                self.__invalid__input__()
                continue
            utils.clear_screen()

            real_option.run()

            if isinstance(real_option, Option):
                option: Option = real_option
                if option.return_after_execution:
                    return

