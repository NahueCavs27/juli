import tkinter as tk
from tkinter import ttk, messagebox
from globals import root
from utils import center_window
from globals import tree_telas


def generate_movimientos_menu(event):
    global movimiento_menu
    if movimiento_menu:
        movimiento_menu.unpost()

    movimiento_menu = tk.Menu(root, tearoff=0)
    movimiento_menu.add_command(label="Movimientos de prendas",
                                command=lambda: open_movimiento("Movimientos de prendas"))
    movimiento_menu.add_command(
        label="Movimientos de tela", command=lambda: open_movimiento("Movimientos de tela"))
    movimiento_menu.add_command(label="Movimientos de Avíos",
                                command=lambda: open_movimiento("Movimientos de Avíos"))

    root.bind('<Button-1>', hide_movimientos_menu)
    # Shift 10cm to the left
    movimiento_menu.post(event.x_root - 100, event.y_root)


def hide_movimientos_menu(event):
    global movimiento_menu
    if movimiento_menu:
        movimiento_menu.unpost()


def open_movimiento(name):
    global movimiento_menu
    movimiento_menu.unpost()  # Hide the menu after selection

    movimiento_window = tk.Toplevel(root)
    movimiento_window.title(name)
    movimiento_window.geometry("800x600")
    movimiento_window.attributes("-topmost", True)
    center_window(movimiento_window)

    tree_movimiento = ttk.Treeview(movimiento_window, columns=[
                                   name], show="headings", height=25)
    tree_movimiento.heading(name, text=name)
    tree_movimiento.pack(expand=True, fill="both")

    scrollbar_y_movimiento = ttk.Scrollbar(
        movimiento_window, orient="vertical", command=tree_movimiento.yview)
    scrollbar_y_movimiento.pack(side="right", fill="y")
    tree_movimiento.configure(yscrollcommand=scrollbar_y_movimiento.set)

    scrollbar_x_movimiento = ttk.Scrollbar(
        movimiento_window, orient="horizontal", command=tree_movimiento.xview)
    scrollbar_x_movimiento.pack(side="bottom", fill="x")
    tree_movimiento.configure(xscrollcommand=scrollbar_x_movimiento.set)

    close_button = tk.Button(
        movimiento_window, text="Cerrar", command=movimiento_window.destroy)
    close_button.pack(side="right", padx=5, pady=5)


def filter_sku(tree):
    sku_window = tk.Toplevel(root)
    sku_window.title("Filtrar por SKU")
    sku_window.geometry("400x300")
    sku_window.attributes("-topmost", True)

    tk.Label(sku_window, text="Seleccione la opción de búsqueda para DEPÓSITO:").pack(
        pady=10)

    search_by_sku = tk.BooleanVar()

    tk.Checkbutton(sku_window, text="Búsqueda por SKU",
                   variable=search_by_sku).pack()

    tk.Label(sku_window, text="Ingrese SKU para buscar:").pack(pady=10)
    sku_entry = tk.Entry(sku_window)
    sku_entry.pack(pady=10)

    tk.Label(sku_window, text="Seleccione la opción de búsqueda para TELAS:").pack(
        pady=10)

    tk.Label(sku_window, text="Ingrese SKU tela para buscar:").pack(pady=10)
    sku_entry_telas = tk.Entry(sku_window)
    sku_entry_telas.pack(pady=10)

    def search():
        sku_value = sku_entry.get()
        sku_telas_value = sku_entry_telas.get()
        found = False

        if search_by_sku.get():
            for item in tree.get_children():
                values = tree.item(item, 'values')
                if sku_value == values[3]:
                    tree.selection_set(item)
                    tree.see(item)
                    found = True
                    break

        if sku_telas_value:
            for item in tree_telas.get_children():
                values = tree_telas.item(item, 'values')
                if sku_telas_value == values[4]:
                    tree_telas.selection_set(item)
                    tree_telas.see(item)
                    found = True
                    break

        if not found:
            messagebox.showinfo(
                "Resultado", "No se encontró el SKU", parent=sku_window)
        sku_window.destroy()

    tk.Button(sku_window, text="Buscar", command=search).pack(pady=10)

    center_window(sku_window)
