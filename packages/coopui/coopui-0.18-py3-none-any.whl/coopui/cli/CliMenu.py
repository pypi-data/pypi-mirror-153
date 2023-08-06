from typing import Callable, Dict, Tuple
import logging
import traceback
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

MENU = logging.INFO + 1
logging.addLevelName(MENU, 'MENU')
logger = logging.getLogger('CLIMENU')

def _try_action(action):
    try:
        action()
    except Exception as e:
        stack = traceback.format_exc()
        logger.error(f"{e}"
                     f"\n{stack}")


class CliMenu:
    def __init__(self, menu_header: str,
                 definition: Dict[str,
                                  Tuple[str,
                                         Callable[[], None]
                                        ]
                                ],
                 notify_user_provider: Callable[[str], None]):
        self.notify_user_provider = notify_user_provider

        self.menu_header = menu_header
        self.menu_items = definition

    def register(self, menu_text, user_entry, action):
        self.menu_items[user_entry] = (menu_text, action)

    def loop(self, switch, request):
        while True:
            inp = request()
            logger.log(level=MENU, msg=f"User entered {inp}")
            action = switch(inp)
            if action is None:
                return
            elif action == "INVALID":
                self.notify_user_provider("Invalid Entry...")
            elif action is not None:
                _try_action(action)
            else:
                raise NotImplementedError("Unhandled response type")


    def print_menu(self):
        menu = f"{self.menu_header}" \
              f"\nPlease select option\n"

        logger.log(level=MENU, msg=f"Menu Displayed:"
                                   f"\n{menu}")


        print(f"\n{menu}")


        for item, tup in self.menu_items.items():
            print(tup[0])

    def get_input_from_user(self):
        self.print_menu()
        return input("").upper()

    def run(self):
        switch = lambda x: {item: tup[1] for item, tup in self.menu_items.items()}.get(x, "INVALID")
        self.loop(switch, self.get_input_from_user)