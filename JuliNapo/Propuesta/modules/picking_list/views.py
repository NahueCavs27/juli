import tkinter as tk
from tkinter import ttk
from globals import root
from utils import center_window


def show_picking_list():
    picking_window = tk.Toplevel(root)
    picking_window.title("Picking list")
    picking_window.geometry("1000x600")
    center_window(picking_window)

    columns = ["Hecho a las", "N° de pedido", "Usuario", "Especificación de prenda",
               "Unidades", "Código pickeado", "Código de prenda", "N° en orden", "Tipo de compra"]

    tree_picking = ttk.Treeview(
        picking_window, columns=columns, show="headings", height=25)

    for col in columns:
        tree_picking.heading(col, text=col)
        tree_picking.column(col, width=120, anchor="center")
    tree_picking.pack(expand=True, fill="both")

    scrollbar_y = ttk.Scrollbar(
        picking_window, orient="vertical", command=tree_picking.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree_picking.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(
        picking_window, orient="horizontal", command=tree_picking.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree_picking.configure(xscrollcommand=scrollbar_x.set)
