"""
This code simply acts as a wrapped around all other codes and runs the
management system

"""

from Menu.menu import Menu # importing menu manager


menu = Menu()
menu.run() # runs the loop till user exits
