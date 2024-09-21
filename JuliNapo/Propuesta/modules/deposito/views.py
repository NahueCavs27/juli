import tkinter as tk
from tkinter import ttk
from globals import tree, tree_telas, root
from utils import center_window, sort_rows
from .actions import generate_movimientos_menu, filter_sku


def show_deposito():
    global tree, tree_telas
    deposito_window = tk.Toplevel(root)
    deposito_window.title("Depósito")
    deposito_window.geometry(
        f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    deposito_window.attributes("-topmost", True)
    center_window(deposito_window)

    tab_control = ttk.Notebook(deposito_window)
    tab_prendas = ttk.Frame(tab_control)
    tab_telas = ttk.Frame(tab_control)
    tab_avios = ttk.Frame(tab_control)
    tab_registro = ttk.Frame(tab_control)

    tab_control.add(tab_prendas, text="Prendas")
    tab_control.add(tab_telas, text="Telas")
    tab_control.add(tab_avios, text="Avíos")
    tab_control.add(tab_registro, text="Registro de movimiento")
    tab_control.pack(expand=1, fill="both")

    # Avíos Tab

    # Prendas Tab
    columns = ["Rubro", "Nombre", "Género", "SKU", "Color", "Cód. Color", "Fitment",
               "Tela", "SKU Tela", "XS", "S", "M", "L", "XL", "XXL", "XXXL",
               "Cantidad", "Composición", "Descripción"]
    tree = ttk.Treeview(tab_prendas, columns=columns,
                        show="headings", height=25)

    column_widths = {"XS": 9, "S": 9, "M": 9, "L": 9, "XL": 9, "XXL": 9, "XXXL": 9,
                     "Cantidad": 40, "Cód. Color": 40, "SKU": 80, "Género": 50}

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths.get(col, 80), anchor="center")

    tree.pack(expand=True, fill="both")
    scrollbar_y = ttk.Scrollbar(
        tab_prendas, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(
        tab_prendas, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    # Telas Tab
    telas_columns = ["Prov. de tela", "Tela base", "Composición", "Descripción", "SKU tela",
                     "Colores", "Unidades de rollos", "Cantidad MTS", "Cantidad Kilos", "Estado tela"]
    tree_telas = ttk.Treeview(
        tab_telas, columns=telas_columns, show="headings", height=25)

    for col in telas_columns:
        tree_telas.heading(col, text=col)
        tree_telas.column(col, width=100, anchor="center")

    tree_telas.pack(expand=True, fill="both")
    scrollbar_y_telas = ttk.Scrollbar(
        tab_telas, orient="vertical", command=tree_telas.yview)
    scrollbar_y_telas.pack(side="right", fill="y")
    tree_telas.configure(yscrollcommand=scrollbar_y_telas.set)

    scrollbar_x_telas = ttk.Scrollbar(
        tab_telas, orient="horizontal", command=tree_telas.xview)
    scrollbar_x_telas.pack(side="bottom", fill="x")
    tree_telas.configure(xscrollcommand=scrollbar_x_telas.set)

    exit_button = tk.Button(deposito_window, text="Salir",
                            command=deposito_window.destroy)
    exit_button.pack(side="right", padx=5, pady=5)

    filter_button = tk.Button(
        deposito_window, text="Filtrar por SKU", command=lambda: filter_sku(tree))
    filter_button.pack(side="right", padx=5, pady=5)

    deposito_window.bind_all("<Control-plus>", toggle_ingresos)
    deposito_window.bind_all("<Control-braceleft>", toggle_ingresos_telas)

    # Definir correctamente
    tree.bind('<ButtonRelease-1>', lambda event: sort_rows())

    # Movimientos Tab - Adding hover menu
    tab_registro.bind("<Button-1>", generate_movimientos_menu)
