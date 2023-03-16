import tkinter as tk

class MiAplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.serial = None

        self.title("IPB2 Secuencia")
        self.geometry("300x100")

        self._crear_interfaz()

    def _crear_interfaz(self):
        etiqueta_serial = tk.Label(self, text="Serial:")
        etiqueta_serial.grid(row=0, column=0, padx=10, pady=10)

        self.entrada_serial = tk.Entry(self)
        self.entrada_serial.grid(row=0, column=1, padx=10, pady=10)

        # boton_guardar = tk.Button(self, text="Guardar", command=self._guardar_serial)
        # boton_guardar.grid(row=1, columnspan=2, pady=10)

    def _guardar_serial(self):
        self.serial = self.entrada_serial.get()
        print(f"Serial guardado: {self.serial}")
        # Aquí puedes llamar a otras funciones que requieran el serial