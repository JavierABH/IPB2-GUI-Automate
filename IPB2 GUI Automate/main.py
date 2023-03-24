#external modules
from tkinter import Tk
import configparser
import clr
import re
import os

from utilities.melexishandler import ProgramHandler
# from gui.gui import MyApplication
from gui.GUI_popups import MainApplication

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

test_start_time = None
test_end_time = None

def main():

    root = Tk()
    root.withdraw()
    gui_app = MainApplication(root)

    # Traceability dll connection
    connector = Connector() #traceability connection

    melexis = ProgramHandler(melexis_path)
    
    if not melexis.opened:
            # App settings for calibration
            melexis.open_application()
            melexis.maximize_window()
            # Open window PTC-04
            melexis.double_click_coordinates(109, 145)
            # Maximize window PTC-04
            melexis.click_coordinates(949, 122)
            # config pull dir
            melexis.click_coordinates(150, 192, 2)
            melexis.press_key("backspace")
            melexis.write_text("1")
            # config AGC_GAIN_MAX [3]
            melexis.click_coordinates(152, 268)
            melexis.press_key("backspace")
            melexis.write_text("4")

    while melexis.opened:
        melexis.freeze(5)
        #se abre ventana que pide escanear la pieza
        askserial_window =  gui_app.ask_serial()

        #se espera hasta que el serial se guarde
        gui_app.wait_window_destroy(askserial_window)
        if gui_app.serial == None:
            continue
        print(gui_app.serial)
        def valid_serial(serial):
            # return True
            if len(serial) != 16:
                msg_window = gui_app.message("SERIAL '{1}' NO VALIDO".format(serial), "orange")
                gui_app.wait_window_destroy(msg_window)
                return False
            else:
                if validate_partnumber_enabled == 'yes':
                    serial_partnumber = ""
                    resp, serial_partnumber = connector.CIMP_PartNumberRef(serial,1, serial_partnumber)
                    print(f"pn: {serial_partnumber}")
                    if expected_part_number != serial_partnumber:
                        msg_window = gui_app.message("NUMERO DE PARTE NO COINCIDE\nExpected: {0}\nReceived: {1}".format(expected_part_number, serial_partnumber), "orange")
                        gui_app.wait_window_destroy(msg_window)

                        #----------------------------------------------------------------------
                        #aqui puede ir mensaje al operador para retirar la pieza del fixture
                        msg_window = gui_app.message("RETIRE LA PIEZA Y\n TOME UNA NUEVA", "blue")
                        gui_app.wait_window_destroy(msg_window)
                        #----------------------------------------------------------------------

                        return False
                    else:
                        return True
                else:
                    return True
                    

        if not valid_serial(gui_app.serial):
            continue

        test_start_time = connector.CIMP_GetDateTimeStr()

        #se hace el backcheck de la pieza
        if backcheck_serial_enabled == 'yes':
            resp = connector.BackCheck_Serial(gui_app.serial, station_name)
            print(f"Bkck: {resp}")
        else:
            resp = "1|TEST FINAL FUNCTIONAL"
        
        #se determina si el backcheck fue aprobatorio
        if not resp == "1|TEST FINAL FUNCTIONAL":
            msg_window = gui_app.message("FALLA EN BACKCHECK\n" + resp, "orange")
            gui_app.wait_window_destroy(msg_window)

            #----------------------------------------------------------------------
            #aqui puede ir mensaje al operador para retirar la pieza del fixture
            msg_window = gui_app.message("RETIRE LA PIEZA Y\n TOME UNA NUEVA", "blue")
            gui_app.wait_window_destroy(msg_window)
            #----------------------------------------------------------------------

            #la palabra reservada continue, descarta el ciclo actual del loop, y continua con el siguiente
            #ciclo desde el principio
            continue

        melexis.freeze(2)
        new_log = "logs\\MLX90510_data.csv" 
        if os.path.exists(new_log):
            os.remove(new_log)

        # Inicia la prueba
        # Power
        melexis.click_coordinates(1517, 126, 1)
        # Connect
        melexis.click_coordinates(1517, 155, 1)
        # Offset
        melexis.click_coordinates(1490, 274, 1)
        # Advertencia
        melexis.click_coordinates(833, 510, 1)
        # ok advertencia
        melexis.freeze(3)
        melexis.press_key("enter")
        # Guardar serial
        # Memory map
        melexis.click_coordinates(148, 52, 1)

        # guardar log
        melexis.click_coordinates(1511, 265)
        melexis.freeze(2)
        melexis.press_key("enter")
        # regresar a menu
        melexis.click_coordinates(21, 53)
        # desconectar pieza
        melexis.click_coordinates(1516, 158)
        # apagar equipo
        melexis.click_coordinates(1517, 126)
        # valida informacion de log
        csv_path = f"logs\\{gui_app.serial}.csv"
        print(new_log)
        if os.path.exists(new_log):
            os.rename(new_log, csv_path)
            print("csv renombrado")

        melexis.freeze(2)
        # lista para almacenar los valores
        numbers = []
        status = 1
        with open(csv_path, mode="r") as csvfile:
            reader = csvfile.read()
            test_search = ['DC01_CONST', 'DC12_CONST', 'DC20_CONST']
            for i in test_search:
                regex = f'"CEE_MAP","\\d+","{i}","[^"]+","RW","(\\d+)"'
                match = re.search(regex, reader)
                if match:
                    numbers.append(int(match.group(1)))
            # valida si no son 0
            if numbers:
                for number in numbers:
                    if number == 0:
                        status = 0
                        break
            else:
                status = 0
        print(numbers)
        # Verifica las pruebas del log    
        if status == 0:
            msg_window = gui_app.message("TEST FUNCTIONAL FAILED", "red", 40)
            gui_app.wait_window_destroy(msg_window)
            msg_window = gui_app.message("PIEZA MALA, RETIRE LA PIEZA Y\n TOME UNA NUEVA", "red")
            gui_app.wait_window_destroy(msg_window)
            continue

        msg_window = gui_app.message("TEST FUNCTIONAL PASSED", "green")
        gui_app.wait_window_destroy(msg_window)
        # Sube a trazabilidad
        test_end_time = connector.CIMP_GetDateTimeStr()
        print(f"serial: {gui_app.serial}, station: S{station_name}, starttime: {test_start_time} ,endtime: {test_end_time}, status: {status}")

        def insert_process_data():
            return connector.InsertProcessDataWithFails(gui_app.serial,
                                                    station_name,
                                                    "TEST FINAL FUNCTIONAL",
                                                    test_start_time,
                                                    test_end_time,
                                                    status,
                                                    "",
                                                    "employee")

        if insertprocess_data_enabled == 'yes':
            reply = insert_process_data()
            print(f"traz rep: {reply}")
        # else:
        #     reply = "OK"
        # print(f"traz rep1: {reply}")
        
        if insertprocess_data_enabled == 'yes':
            reply = insert_process_data()
        else:
            reply = "OK"

        #se determina si los datos se subieron correctamente a traceabilidad
        #dependiendo de la respusta, se mostrara un mensaje indicandolo
        if reply != "OK":
            msg_window = gui_app.message("FALLA AL SUBIR A TRACEABILIDAD: \n"+ reply, "red")
            gui_app.wait_window_destroy(msg_window)
            msg_window = gui_app.message("VUELVA A ESCANEAR LA PIEZA", "green")
            gui_app.wait_window_destroy(msg_window)
            continue

        #----------------------------------------------------------------------
        #aqui puede ir mensaje al operador para retirar la pieza del fixture
        msg_window = gui_app.message("PIEZA BUENA, RETIRE LA PIEZA Y\n TOME UNA NUEVA", "green")
        gui_app.wait_window_destroy(msg_window)
        #----------------------------------------------------------------------


    root.destroy()
    root.mainloop()
    os._exit(1)


if __name__ == "__main__":
    main()