"""
This code simply acts as a wrapper around all other codes and runs the
management system

"""

from Menu.menu import Menu # importing menu manager


menu = Menu()
try:
    menu.run() # runs the loop till user exits
except KeyboardInterrupt as e:
    print("Gracefully exiting....")
    exit(0)
