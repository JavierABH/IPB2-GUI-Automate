from utilities.melexishandler import ProgramHandler
import re
import clr
import configparser

settings = configparser.ConfigParser()
settings.read('IPB2 GUI Automate\settings\settings.ini')

melexis_path = settings["Paths"]["Melexis_app"]
OutputLogs_path = settings["Paths"]["OutputLogs"]
newtonsoftjson_path = settings["Paths"]["Newtonsoft.Json.Dll"]
wsconnector_path = settings["Paths"]["WSConnector.Dll"]

clr.AddReference(newtonsoftjson_path)
clr.AddReference(wsconnector_path)
from WSConnector import Connector

#imported info from .ini settings file
station_name = settings['Process']['StationName']

connector = Connector()

##################### coordenadas ###############################

# melexis_path = r"C:\Program Files (x86)\Melexis\MPT\MPTApp.exe"
# melexis = ProgramHandler(melexis_path)
# print(len("G583810800005S10"))
# coordinates = melexis.mouse_position_on_key_press()
# print(coordinates)                             

##################### coordenadas ###############################

################### info de logs ################################

# with open("logs\G583810810025Z12.csv", 'r') as csvfile:
#     contenido = csvfile.read()
#     constantes = ['DC01_CONST', 'DC12_CONST', 'DC20_CONST']
#     valores = []

#     for constante in constantes:
#         regex = f'"CEE_MAP","\\d+","{constante}","[^"]+","RW","(\\d+)"'
#         match = re.search(regex, contenido)

#         if match:
#             valores.append(int(match.group(1)))

#     print(valores)

################### info de logs ################################

######################## traceabilidad ##########################
serial = "G583810810025Z12"
serial_partnumber = ""
resp, serial_partnumber = connector.CIMP_PartNumberRef(serial,1, serial_partnumber)
print(f"pn: {serial_partnumber}")
bk = connector.BackCheck_Serial(serial, station_name)
print(bk)
test_start_time = connector.CIMP_GetDateTimeStr()
test_end_time = connector.CIMP_GetDateTimeStr()
status = 1
# reply_traz = connector.InsertProcessDataWithFails(serial,
#                                                     station_name,
#                                                     "TEST FINAL FUNCTIONAL",
#                                                     test_start_time,
#                                                     test_end_time,
#                                                     status,
#                                                     "",
#                                                     "employee")
# print(reply_traz)