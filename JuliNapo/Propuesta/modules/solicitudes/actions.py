import tkinter as tk
from tkinter import messagebox
from globals import root


def generate_solicitud_menu(event):
    solicitud_menu = tk.Menu(root, tearoff=0)
    solicitud_menu.add_command(label="Solicitud de insumos", command=lambda: messagebox.showinfo(
        "Solicitud", "Generando solicitud de insumos"))
    solicitud_menu.add_command(label="Solicitud de producción", command=lambda: messagebox.showinfo(
        "Solicitud", "Generando solicitud de producción"))
    solicitud_menu.post(event.x_root, event.y_root)
