# coopui
 Package dedicated for holding tooling that allows a developer to interact with a user
 

Import the packages that will handle the cli interaction with the user
```
from coopui.cli.CliAtomicUserInteraction import CliAtomicUserInteraction as ui
from coopui.cli.CliMenu import CliMenu
```
 
 The CliAtomicUserInteraction class allows interaction with the user with validation of the input returned, as well as ability to notify user with text
 ```
 
if __name__ == "__main__":
    # yes or no
    ret1 = ui.request_yes_no(prompt="Select Yes or No")

    # from a list
    lst = [x for x in 'abcdefghijklmnop']
    ret2 = ui.request_from_list(lst)

    # from a dict
    dic = {1: "Cat", 2: "Dog", 3: "Turtle", 4: "Frog"}
    ret3 = ui.request_from_dict(dic)

    # notify user
    ui.notify_user(text=f"selected yes: {ret1}")
    ui.notify_user(text=f"selected letter from list: {ret2}")
    ui.notify_user(text=f"selected animal: {ret3}")
``` 
 
 
 First define a custom function to greet a user:
 ```
def greet(ui):
    ui.notify_user("Hello!")
    ret = ui.request_yes_no("Are you having a good day?")

    if ret is None:
        return

    if ret:
        ui.notify_user("Glad to hear it!")
    else:
        ui.notify_user("Im so sorry....")
```

Then, use the CliAtomicUserInteraction class along with the CliMenu class to provide a menu to perform the greeting
```
if __name__ == "__main__":
    ui = CliAtomicUserInteraction()
    menu = CliMenu(menu_header="************* My Menu *************",
                   definition={
                       "G": ("[G]reeting", lambda: greet(ui))
                   },
                   notify_user_provider=ui.notify_user
                   )

    menu.run()
```

A menu will return only if the result of a selection is None. Therefore, always include a definition for returning None
```
if __name__ == "__main__":
    ui = CliAtomicUserInteraction()
    menu = CliMenu(menu_header="************* My Menu *************",
                   definition={
                       "G": ("[G]reeting", lambda: greet(ui)),
                       "X": ("Back", None)
                   },
                   notify_user_provider=ui.notify_user
                   )

    menu.run()
```


Multiple menus can be chained together to define a nested menu selection. 
 
```
if __name__ == "__main__":
    ui = CliAtomicUserInteraction()
    main_menu = CliMenu(menu_header="************* My Menu *************",
                   definition={
                       "G": ("[G]reeting", lambda: greet(ui)),
                       "S": ("[S]ub-menu", lambda: sub_menu.run()),
                       "X": ("E[X]it", None)
                   },
                   notify_user_provider=ui.notify_user
                   )
    sub_menu = CliMenu(menu_header="************* Sub Menu *************",
                   definition={
                       "G": ("[G]reeting", lambda: greet(ui)),
                       "X": ("X -- Back", None)
                   },
                   notify_user_provider=ui.notify_user
                   )

    main_menu.run()
```
