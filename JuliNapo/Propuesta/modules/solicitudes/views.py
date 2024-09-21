import tkinter as tk
from tkinter import ttk
from globals import root
from utils import center_window
from .actions import generate_solicitud_menu


def show_solicitudes():
    solicitudes_window = tk.Toplevel(root)
    solicitudes_window.title("Solicitudes")
    solicitudes_window.geometry("1000x600")
    center_window(solicitudes_window)

    columns = ["Sector", "Fecha de solicitud",
               "Tipo de solicitud", "Solicitud"]

    tree_solicitudes = ttk.Treeview(
        solicitudes_window, columns=columns, show="headings", height=25)

    for col in columns:
        tree_solicitudes.heading(col, text=col)
        tree_solicitudes.column(col, width=200, anchor="center")
    tree_solicitudes.pack(expand=True, fill="both")

    scrollbar_y = ttk.Scrollbar(
        solicitudes_window, orient="vertical", command=tree_solicitudes.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree_solicitudes.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(
        solicitudes_window, orient="horizontal", command=tree_solicitudes.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree_solicitudes.configure(xscrollcommand=scrollbar_x.set)

    # Adding the "Generar solicitud" tab above the columns
    tab_control = ttk.Notebook(solicitudes_window)
    tab_generar_solicitud = ttk.Frame(tab_control)
    tab_control.add(tab_generar_solicitud, text="Generar solicitud")
    tab_control.pack(expand=0, fill="x")

    tab_generar_solicitud.bind("<Button-1>", generate_solicitud_menu)
