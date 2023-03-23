from utilities.melexishandler import ProgramHandler

melexis_path = r"C:\Program Files (x86)\Melexis\MPT\MPTApp.exe"
melexis = ProgramHandler(melexis_path)
print(len("G583810800005S10"))
coordinates = melexis.mouse_position_on_key_press()
print(coordinates)                             