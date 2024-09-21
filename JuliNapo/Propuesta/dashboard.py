import tkinter as tk
from tkinter import messagebox
from modules.database.views import show_base_de_datos
from modules.deposito.views import show_deposito
from modules.picking_list.views import show_picking_list
from modules.solicitudes.views import show_solicitudes


def show_sector(sector_name):
    if sector_name == "Depósito":
        show_deposito()
    elif sector_name == "Ventas":
        show_solicitudes()
    elif sector_name == "Picking":
        show_picking_list()
    elif sector_name == "Solicitudes":
        show_solicitudes()
    elif sector_name == "Base de datos":
        show_base_de_datos()
    else:
        messagebox.showinfo("Información", f"{sector_name} en proceso")


def create_dashboard(root):
    frame = tk.Frame(root)
    frame.pack(expand=True)

    button_width = 15
    button_height = 6

    for i in range(2):
        for j in range(5):
            sector_name = f"prueba {i * 5 + j + 1}"
            if i * 5 + j == 0:
                sector_name = "Depósito"
            elif i * 5 + j == 1:
                sector_name = "Ventas"
            elif i * 5 + j == 2:
                sector_name = "Picking"
            elif i * 5 + j == 3:
                sector_name = "Onbound"
            elif i * 5 + j == 4:
                sector_name = "Colaboradores"
            elif i * 5 + j == 5:
                sector_name = "Base de datos"
            elif i * 5 + j == 6:
                sector_name = "Solicitudes"
            btn = tk.Button(frame, text=sector_name, width=button_width, height=button_height,
                            command=lambda name=sector_name: show_sector(name))
            btn.grid(row=i, column=j, padx=7, pady=7)
