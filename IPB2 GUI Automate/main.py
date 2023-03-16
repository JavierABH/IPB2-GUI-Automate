import tkinter as tk
import configparser
import clr

from utilities.melexishandler import ProgramHandler
from gui.gui import MiAplicacion

settings = configparser.ConfigParser()
settings.read('IPB2 GUI Automate\settings\settings.ini')

app_path = settings["Paths"]["Melexis_app"]

def main():
    print("Open app")
    # Autogui.open_application(app_path)
    # print("Maximize app")
    # Autogui.maximize_window()

if __name__ == "__main__":
    main()
    app = MiAplicacion()
    app.mainloop()
