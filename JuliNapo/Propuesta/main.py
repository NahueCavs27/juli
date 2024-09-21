import tkinter as tk
from globals import root
from dashboard import create_dashboard


def create_root():
    global root
    if root is None:  # Solo creamos una instancia si no existe
        root = tk.Tk()
        root.title("Dashboard")
        root.geometry("640x480")
        root.resizable(False, False)
    return root


if __name__ == "__main__":
    root = create_root()
    create_dashboard(root)
    root.mainloop()
