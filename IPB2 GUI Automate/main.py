import tkinter as tk
import configparser
import clr

from utilities.melexishandler import ProgramHandler
from gui.gui import MyApplication

settings = configparser.ConfigParser()
settings.read('IPB2 GUI Automate\settings\settings.ini')

melexis_path = settings["Paths"]["Melexis_app"]
newtonsoftjson_path = settings["Paths"]["Newtonsoft.Json.Dll"]
wsconnector_path = settings["Paths"]["WSConnector.Dll"]

clr.AddReference(newtonsoftjson_path)
clr.AddReference(wsconnector_path)
from WSConnector import Connector

#imported info from .ini settings file
station_name = settings['Process']['StationName']
expected_part_number = settings['Process']['PartNumber']

backcheck_serial_enabled = settings["Default"]["BackcheckSerial"]
validate_partnumber_enabled = settings["Default"]["ValidatePartNumber"]
insertprocess_data_enabled = settings["Default"]["InsertProcessData"]
only_pass_enabled = settings["Default"]["OnlyInsertPass"]

def main():
    gui_app = MyApplication()
    # Traceability dll connection
    connector = Connector() #traceability connection

    melexis = ProgramHandler(melexis_path)
    
    if not melexis.opened:
        # App settings for calibration
        melexis.open_application()
        print("Maximize app")
        melexis.maximize_window()
        # Open window PTC-04
        melexis.double_click_coordinates(93,144, 1)
        # Maximize window PTC-04
        melexis.click_coordinates(953, 125, 2)
        # config pull dir
        melexis.click_coordinates(152, 192, 5)
        melexis.press_key("backspace")
        melexis.write_text("1")
        # config AGC_GAIN_MAX [3]
        melexis.click_coordinates(148, 269, 5)
        melexis.press_key("backspace")
        melexis.write_text("4")

    while melexis.opened:
        # se muestra gui en primer plano
        gui_app.show()
        # se espera hasta que se presione el boton Iniciar prueba que indica que ya se puede iniciar el proceso
        if gui_app.init_test:            

            if gui_app.serial == None:
                continue
        
            def valid_serial(serial):
                
                if len(serial) != 16:
                    gui_app.create_serial_failure_window()
                    return False
                else:
                    if validate_partnumber_enabled == 'yes':
                        serial_partnumber = ""
                        resp, serial_partnumber = connector.CIMP_PartNumberRef(serial,1, serial_partnumber)
                        if expected_part_number != serial_partnumber:
                            gui_app.create_PN_failure_window()
                            gui_app.create_failure_window()
                            return False
                        else:
                            return True
                    else:
                        return True

            if not valid_serial(gui_app.serial):
                continue

            #se hace el backcheck de la pieza
            if backcheck_serial_enabled == 'yes':
                resp = connector.BackCheck_Serial(gui_app.serial, station_name)
            else:
                resp = "1|TEST FINAL FUNCTIONAL"
            
            #se determina si el backcheck fue aprobatorio
            if not resp == "1|TEST FINAL FUNCTIONAL":
                gui_app.create_backcheck_failure_window()
                continue

            melexis.freeze(2)

            # realiza la prueba
            print("HOLA")


if __name__ == "__main__":
    main()