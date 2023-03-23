import tkinter as tk
from tkinter import messagebox
import threading

class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.serial = None  
        self.init_test = False
        self.title("IPB2 Sequence")
        self.geometry("200x100")
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        self._create_interface()
        self._center_window()
        self.serial_entry.focus()

    def _create_interface(self):
        serial_label = tk.Label(self, text="Serial:")
        serial_label.grid(row=0, column=0, padx=10, pady=10)

        self.serial_entry = tk.Entry(self)
        self.serial_entry.grid(row=0, column=1, padx=10, pady=10)
        self.serial_entry.bind("<Return>", self.process_serial)

        start_test_button = tk.Button(self, text="Start Test", command=self._start_test)
        start_test_button.grid(row=1, column=1, padx=10, pady=10)

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            self.destroy()

    def process_serial(self, event):
        serial = self.serial_entry.get()
        # self.serial_entry.delete(0, tk.END)
        print(serial)  # Replace this with the desired operation

    def _start_test(self):
        self.init_test = True
        self.serial_entry.delete(0, tk.END)
        self.hide()

    def close_main_window(self):
        self.destroy()

    def hide(self):
        self.withdraw()

    def show(self):
        self.init_test = False
        self.deiconify()

    def create_success_window(self):
        def close():
            success_window.destroy()
            self.show()

        self.hide()
        success_window = tk.Toplevel(self)
        success_window.configure(bg="green")
        success_window.geometry("300x100")
        success_label = tk.Label(
            success_window, text="Retire la pieza y\n tome una nueva", bg="green"
        )
        success_label.pack(pady=20)

        ok_button = tk.Button(success_window, text="OK", command=close)
        ok_button.pack(pady=10)

    def create_failure_window(self):
        def close():
            failure_window.destroy()
            self.show()

        self.hide()
        failure_window = tk.Toplevel(self)
        failure_window.configure(bg="red")
        failure_window.geometry("300x100")
        failure_label = tk.Label(
            failure_window, text="PCB con falla, retire la pieza", bg="red"
        )
        failure_label.pack(pady=20)

        ok_button = tk.Button(failure_window, text="OK", command=close)
        ok_button.pack(pady=10)

    def create_serial_failure_window(self):
        def close():
            failure_window.destroy()
            self.show()

        self.hide()
        failure_window = tk.Toplevel(self)
        failure_window.configure(bg="red")
        failure_window.geometry("300x100")
        failure_label = tk.Label(
            failure_window, text="Serial invalido, retire la pieza", bg="red"
        )
        failure_label.pack(pady=20)

        ok_button = tk.Button(failure_window, text="OK", command=close)
        ok_button.pack(pady=10)

    def create_PN_failure_window(self):
        def close():
            failure_window.destroy()
            self.show()

        self.hide()
        failure_window = tk.Toplevel(self)
        failure_window.configure(bg="red")
        failure_window.geometry("300x100")
        failure_label = tk.Label(
            failure_window, text="PartNumber invalido", bg="red"
        )
        failure_label.pack(pady=20)

        ok_button = tk.Button(failure_window, text="OK", command=close)
        ok_button.pack(pady=10)

    def create_backcheck_failure_window(self):
        def close():
            backcheck_failure_window.destroy()
            self.show()

        self.hide()
        backcheck_failure_window = tk.Toplevel(self)
        backcheck_failure_window.configure(bg="red")
        backcheck_failure_window.geometry("300x100")
        backcheck_failure_label = tk.Label(
            backcheck_failure_window, text="Backcheck failure", bg="red"
        )
        backcheck_failure_label.pack(pady=20)

        ok_button = tk.Button(
            backcheck_failure_window, text="OK", command=close
        )
        ok_button.pack(pady=10)

    def update(self):
        def run():
            self.mainloop()

        self.thread = threading.Thread(target=run)
        self.thread.start()

if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()