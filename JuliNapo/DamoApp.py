import tkinter as tk
from tkinter import messagebox, ttk
import os
import pandas as pd

root = tk.Tk()  # Definimos root al inicio del script
root.title("Dashboard")
root.geometry("640x480")
root.resizable(False, False)

selected_item = None  # Inicializamos selected_item al inicio
selected_item_telas = None
movimiento_menu = None  # Initialize movimiento_menu

# Funciones para manejar archivos .txt


def guardar_datos(ruta, datos):
    with open(ruta, 'a') as archivo:
        archivo.write(datos)


def eliminar_datos(ruta):
    if os.path.exists(ruta):
        os.remove(ruta)


def cargar_datos(ruta):
    if os.path.exists(ruta):
        # Cambiar a coma como delimitador
        return pd.read_csv(ruta, sep=",", header=None)
    else:
        return pd.DataFrame()


def poblar_treeview(tree, datos, columns):
    for i in tree.get_children():
        tree.delete(i)
    print(datos)  # Verifica qué datos se están cargando
    for _, row in datos.iterrows():
        tree.insert("", "end", values=row.tolist())


# Rutas de los archivos de datos
rutas = {
    "prendas": os.path.join("database", "prendas.txt"),
    "telas": os.path.join("database", "telas.txt"),
    "avios": os.path.join("database", "avios.txt"),
    "registros_movimiento": os.path.join("database", "registros de movimiento.txt"),
    "ventas": os.path.join("database", "ventas.txt")
}


def on_click(sector_name):
    if sector_name == "Depósito":
        show_deposito()
    elif sector_name == "Ventas":
        show_sales()
    elif sector_name == "Picking":
        show_picking_list()
    elif sector_name == "Solicitudes":
        show_solicitudes()
    elif sector_name == "Base de datos":
        show_base_de_datos()
    else:
        messagebox.showinfo("Información", f"{sector_name} en proceso")


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def show_deposito():
    global tree, tree_telas, current_row, Ingresos, selected_item, movimiento_menu
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

# Función para ordenar filas por columna


def sort_rows():
    items = tree.get_children()
    sorted_items = sorted(items, key=lambda item: tree.item(item)["values"])
    for idx, item in enumerate(sorted_items):
        tree.move(item, '', idx)


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

# Continua con los botones del dashboard


def show_sales():
    global tree_sales
    sales_window = tk.Toplevel(root)
    sales_window.title("Ventas")
    sales_window.geometry("1200x600")
    center_window(sales_window)

    columns = ["Fecha", "Usuario", "Nombre", "Email", "Teléfono", "Punto de envío", "Dirección", "CP",
               "Localidad", "Partido", "Zona", "Banco", "Monto", "Tipo de compra", "Peso (gramos)",
               "Código de prenda", "Especificación de prenda", "Talle", "Unidades", "N° de pedido",
               "Realizado a las", "Número en orden"]

    tree_sales = ttk.Treeview(
        sales_window, columns=columns, show="headings", height=25)
    for col in columns:
        tree_sales.heading(col, text=col)
        tree_sales.column(col, width=120, anchor="center")
    tree_sales.pack(expand=True, fill="both")

    scrollbar_y = ttk.Scrollbar(
        sales_window, orient="vertical", command=tree_sales.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree_sales.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(
        sales_window, orient="horizontal", command=tree_sales.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree_sales.configure(xscrollcommand=scrollbar_x.set)

    close_button = tk.Button(sales_window, text="Cerrar",
                             command=sales_window.destroy)
    close_button.pack(side="right", padx=5, pady=5)

    new_button = tk.Button(
        sales_window, text="Nueva venta", command=add_new_sale)
    new_button.pack(side="right", padx=5, pady=5)

    edit_button = tk.Button(
        sales_window, text="Editar venta", command=edit_sale)
    edit_button.pack(side="right", padx=5, pady=5)

    delete_button = tk.Button(
        sales_window, text="Eliminar venta", command=delete_sale)
    delete_button.pack(side="right", padx=5, pady=5)

    filter_button = tk.Button(
        sales_window, text="Filtrar búsqueda", command=filter_sales_search)
    filter_button.pack(side="right", padx=5, pady=5)
    load_sales_data(tree_sales)


def load_sales_data(tree_sales: ttk.Treeview):
    datos = cargar_datos(rutas["ventas"])
    for _, row in datos.iterrows():
        tree_sales.insert("", "end", values=row.tolist())


def add_new_sale():
    sales_form("Nueva venta", "Desea sumar una venta?")


def edit_sale():
    selected_item = tree_sales.selection()
    if not selected_item:
        messagebox.showwarning(
            "Advertencia", "Por favor, seleccione una venta para editar.")
        return
    sales_form("Editar venta", "Desea editar la venta?", edit=True)


def delete_sale():
    selected_item = tree_sales.selection()
    if not selected_item:
        messagebox.showwarning(
            "Advertencia", "Por favor, seleccione una venta para eliminar.")
        return
    confirm = messagebox.askquestion(
        "Confirmación", "¿Desea eliminar la venta?")
    if confirm == 'yes':
        tree_sales.delete(selected_item)


def sales_form(title, confirm_message, edit=False):
    form_window = tk.Toplevel(root)
    form_window.title(title)
    form_window.geometry("600x600")
    center_window(form_window)

    labels = ["Fecha", "Usuario", "Nombre", "Email", "Teléfono", "Punto de envío", "Dirección", "CP",
              "Localidad", "Partido", "Zona", "Banco", "Monto", "Tipo de compra", "Peso (gramos)",
              "Código de prenda", "Especificación de prenda", "Talle", "Unidades", "N° de pedido"]

    entries = {}
    for idx, label in enumerate(labels):
        lbl = tk.Label(form_window, text=label)
        lbl.grid(row=idx//2, column=(idx % 2) * 2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_window)
        entry.grid(row=idx//2, column=(idx % 2) *
                   2 + 1, padx=5, pady=5, sticky="w")
        entries[label] = entry

    if edit:
        selected_item = tree_sales.selection()[0]
        values = tree_sales.item(selected_item, 'values')
        for idx, label in enumerate(labels):
            entries[label].insert(0, values[idx])

    def save_sale():
        if messagebox.askquestion("Confirmación", confirm_message) == 'yes':
            values = [entries[label].get() for label in labels]
            df = pd.DataFrame([values], columns=labels)
            guardar_datos(rutas["ventas"], df.to_csv(
                index=False, header=False))
            if edit:
                tree_sales.item(selected_item, values=values)
            else:
                tree_sales.insert("", "end", values=values)
            form_window.destroy()

    save_button = tk.Button(form_window, text="Guardar", command=save_sale)
    save_button.grid(row=(len(labels)//2) + 1, column=0, padx=5, pady=10)

    cancel_button = tk.Button(
        form_window, text="Cancelar", command=form_window.destroy)
    cancel_button.grid(row=(len(labels)//2) + 1, column=1, padx=5, pady=10)


def filter_sales_search():
    filter_window = tk.Toplevel(root)
    filter_window.title("Filtrar búsqueda")
    filter_window.geometry("400x200")
    center_window(filter_window)

    tk.Label(filter_window, text="Usuario:").grid(
        row=0, column=0, padx=5, pady=5, sticky="e")
    user_entry = tk.Entry(filter_window)
    user_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(filter_window, text="Fecha:").grid(
        row=1, column=0, padx=5, pady=5, sticky="e")
    date_entry = tk.Entry(filter_window)
    date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def search():
        user = user_entry.get()
        date = date_entry.get()
        if not user or not date:
            messagebox.showwarning(
                "Advertencia", "Por favor, complete ambos campos para buscar.")
            return

        found = False
        for item in tree_sales.get_children():
            values = tree_sales.item(item, 'values')
            if user == values[1] and date == values[0]:
                tree_sales.selection_set(item)
                tree_sales.see(item)
                found = True
                break

        if not found:
            messagebox.showinfo(
                "Resultado", "No se encontraron coincidencias.")
        filter_window.destroy()

    tk.Button(filter_window, text="Buscar", command=search).grid(
        row=2, column=0, columnspan=2, pady=10)


def create_ingresos():
    global Ingresos, entries, selected_item
    Ingresos = tk.Toplevel(root)
    Ingresos.title("Ingresos")
    Ingresos.geometry("600x400")
    Ingresos.resizable(False, False)
    Ingresos.attributes("-topmost", True)

    center_window(Ingresos)

    labels = ["Rubro", "Nombre", "Género", "SKU", "Color", "Cód. Color", "Fitment",
              "Tela", "SKU Tela", "XS", "S", "M", "L", "XL", "XXL", "XXXL",
              "Composición", "Descripción"]

    entries = {}

    for idx, label in enumerate(labels):
        lbl = tk.Label(Ingresos, text=label)
        lbl.grid(row=idx // 2, column=(idx % 2)
                 * 2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(Ingresos)
        entry.grid(row=idx // 2, column=(idx % 2) *
                   2 + 1, padx=5, pady=5, sticky="w")
        entries[label] = entry

    def show_confirmation_message(message):
        msg_box = tk.Toplevel(Ingresos)
        msg_box.title("Confirmación")
        msg_box.attributes("-topmost", True)
        tk.Label(msg_box, text=message).pack(padx=20, pady=20)
        tk.Button(msg_box, text="Aceptar",
                  command=msg_box.destroy).pack(pady=10)
        center_window(msg_box)

    def save_data():
        global selected_item
        values = [entries[label].get() for label in labels]

        # Calcula la cantidad total y actualiza el campo correspondiente
        tallas = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        total_cantidad = sum(int(entries[talla].get())
                             for talla in tallas if entries[talla].get().isdigit())
        # Asegúrate de que el índice coincide con "Cantidad"
        values[16] = str(total_cantidad)

        df = pd.DataFrame([values], columns=labels)
        guardar_datos(rutas["prendas"], df.to_csv(index=False))

        if selected_item:
            tree.item(selected_item, values=values)
            selected_item = None
            show_confirmation_message("¡Datos editados con éxito!")
        else:
            tree.insert("", "end", values=values)
            show_confirmation_message("¡Datos guardados con éxito!")

        clear_entries()

    def clear_entries():
        for label in labels:
            entries[label].delete(0, tk.END)

    def cancel():
        clear_entries()
        Ingresos.withdraw()

    def edit_data():
        global selected_item
        if tree.selection():
            selected_item = tree.selection()[0]
            values = tree.item(selected_item, 'values')
            for idx, label in enumerate(labels):
                entries[label].delete(0, tk.END)
                entries[label].insert(0, values[idx])
            show_confirmation_message("¡Listo para editar!")

    def delete_data():
        global selected_item
        if tree.selection():
            selected_item = tree.selection()[0]
            confirm = messagebox.askquestion(
                "Confirmación", "¿Confirmas que deseas eliminar?", parent=Ingresos)
            if confirm == 'yes':
                tree.delete(selected_item)
                selected_item = None
                show_confirmation_message("¡Datos eliminados con éxito!")

    btn_save = tk.Button(Ingresos, text="Guardar", command=save_data)
    btn_save.grid(row=(len(labels) // 2) + 1, column=0, padx=5, pady=5)

    btn_cancel = tk.Button(Ingresos, text="Cancelar", command=cancel)
    btn_cancel.grid(row=(len(labels) // 2) + 1, column=1, padx=5, pady=5)

    btn_edit = tk.Button(Ingresos, text="Editar", command=edit_data)
    btn_edit.grid(row=(len(labels) // 2) + 2, column=0, padx=5, pady=5)

    btn_delete = tk.Button(
        Ingresos, text="Eliminar Datos", command=delete_data)
    btn_delete.grid(row=(len(labels) // 2) + 2, column=1, padx=5, pady=5)


def create_ingresos_telas():
    global Ingresos_telas, entries_telas, selected_item_telas
    Ingresos_telas = tk.Toplevel(root)
    Ingresos_telas.title("Ingresos Telas")
    Ingresos_telas.geometry("600x400")
    Ingresos_telas.resizable(False, False)
    Ingresos_telas.attributes("-topmost", True)

    center_window(Ingresos_telas)

    labels_telas = ["Prov. de tela", "Tela base", "Composición", "Descripción", "SKU tela",
                    "Colores", "Unidades de rollos", "Cantidad MTS", "Cantidad Kilos", "Estado tela"]

    entries_telas = {}

    for idx, label in enumerate(labels_telas):
        lbl = tk.Label(Ingresos_telas, text=label)
        lbl.grid(row=idx // 2, column=(idx % 2)
                 * 2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(Ingresos_telas)
        entry.grid(row=idx // 2, column=(idx % 2) *
                   2 + 1, padx=5, pady=5, sticky="w")
        entries_telas[label] = entry

    def show_confirmation_message(message):
        msg_box = tk.Toplevel(Ingresos_telas)
        msg_box.title("Confirmación")
        msg_box.attributes("-topmost", True)
        tk.Label(msg_box, text=message).pack(padx=20, pady=20)
        tk.Button(msg_box, text="Aceptar",
                  command=msg_box.destroy).pack(pady=10)
        center_window(msg_box)

    def save_data_telas():
        global selected_item_telas
        values = [entries_telas[label].get() for label in labels_telas]

        df = pd.DataFrame([values], columns=labels_telas)
        guardar_datos(rutas["telas"], df.to_csv(index=False))

        if selected_item_telas:
            tree_telas.item(selected_item_telas, values=values)
            selected_item_telas = None
            show_confirmation_message("¡Datos editados con éxito!")
        else:
            tree_telas.insert("", "end", values=values)
            show_confirmation_message("¡Datos guardados con éxito!")

        clear_entries_telas()

    def clear_entries_telas():
        for label in labels_telas:
            entries_telas[label].delete(0, tk.END)

    def cancel_telas():
        clear_entries_telas()
        Ingresos_telas.withdraw()

    def edit_data_telas():
        global selected_item_telas
        if tree_telas.selection():
            selected_item_telas = tree_telas.selection()[0]
            values = tree_telas.item(selected_item_telas, 'values')
            for idx, label in enumerate(labels_telas):
                entries_telas[label].delete(0, tk.END)
                entries_telas[label].insert(0, values[idx])
            show_confirmation_message("¡Listo para editar!")

    def delete_data_telas():
        global selected_item_telas
        if tree_telas.selection():
            selected_item_telas = tree_telas.selection()[0]
            confirm = messagebox.askquestion(
                "Confirmación", "¿Confirmas que deseas eliminar?", parent=Ingresos_telas)
            if confirm == 'yes':
                tree_telas.delete(selected_item_telas)
                selected_item_telas = None
                show_confirmation_message("¡Datos eliminados con éxito!")

    btn_save_telas = tk.Button(
        Ingresos_telas, text="Guardar", command=save_data_telas)
    btn_save_telas.grid(row=(len(labels_telas) // 2) +
                        1, column=0, padx=5, pady=5)

    btn_cancel_telas = tk.Button(
        Ingresos_telas, text="Cancelar", command=cancel_telas)
    btn_cancel_telas.grid(row=(len(labels_telas) // 2) +
                          1, column=1, padx=5, pady=5)

    btn_edit_telas = tk.Button(
        Ingresos_telas, text="Editar", command=edit_data_telas)
    btn_edit_telas.grid(row=(len(labels_telas) // 2) +
                        2, column=0, padx=5, pady=5)

    btn_delete_telas = tk.Button(
        Ingresos_telas, text="Eliminar Datos", command=delete_data_telas)
    btn_delete_telas.grid(row=(len(labels_telas) // 2) +
                          2, column=1, padx=5, pady=5)

    # Add the "Ordenar por" button and its functionality
    btn_ordenar = tk.Button(
        Ingresos_telas, text="Ordenar por", command=open_ordenar_por)
    btn_ordenar.grid(row=(len(labels_telas) // 2) + 3,
                     column=0, columnspan=2, pady=10)


def open_ordenar_por():
    ordenar_window = tk.Toplevel(root)
    ordenar_window.title("Ordenar por")
    ordenar_window.geometry("600x400")
    ordenar_window.resizable(False, False)
    # Ensure the window is always on top
    ordenar_window.attributes("-topmost", True)
    center_window(ordenar_window)

    left_listbox = tk.Listbox(ordenar_window)
    right_listbox = tk.Listbox(ordenar_window)
    left_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    right_listbox.pack(side="right", fill="both",
                       expand=True, padx=10, pady=10)

    def add_param():
        add_window = tk.Toplevel(root)
        add_window.title("Agregar parámetro")
        add_window.geometry("300x150")
        # Ensure the window is always on top
        add_window.attributes("-topmost", True)
        center_window(add_window)

        tk.Label(add_window, text="Indique parámetro:").pack(pady=10)
        param_entry = tk.Entry(add_window)
        param_entry.pack(pady=10)

        def save_param():
            param = param_entry.get()
            if param:
                left_listbox.insert(tk.END, param)
                add_window.destroy()

        tk.Button(add_window, text="Guardar", command=save_param).pack(pady=10)

    def edit_param():
        selected = left_listbox.curselection()
        if not selected:
            messagebox.showwarning(
                "Advertencia", "Seleccione un parámetro para editar.")
            return

        edit_window = tk.Toplevel(root)
        edit_window.title("Editar parámetro")
        edit_window.geometry("300x150")
        # Ensure the window is always on top
        edit_window.attributes("-topmost", True)
        center_window(edit_window)

        tk.Label(edit_window, text="Editar parámetro:").pack(pady=10)
        param_entry = tk.Entry(edit_window)
        param_entry.pack(pady=10)
        param_entry.insert(0, left_listbox.get(selected))

        def save_edit():
            param = param_entry.get()
            if param:
                left_listbox.delete(selected)
                left_listbox.insert(selected, param)
                edit_window.destroy()

        tk.Button(edit_window, text="Guardar", command=save_edit).pack(pady=10)

    def delete_param():
        selected = left_listbox.curselection()
        if selected:
            if messagebox.askquestion("Confirmación", "¿Desea eliminar la información?") == 'yes':
                left_listbox.delete(selected)
        else:
            messagebox.showwarning(
                "Advertencia", "Seleccione un parámetro para eliminar.")

    def move_param():
        selected_left = left_listbox.curselection()
        selected_right = right_listbox.curselection()
        if selected_left:
            param = left_listbox.get(selected_left)
            left_listbox.delete(selected_left)
            right_listbox.insert(tk.END, param)
            # Add sorting functionality here
            sort_telas_by(right_listbox.get(0, tk.END))
        elif selected_right:
            param = right_listbox.get(selected_right)
            right_listbox.delete(selected_right)
            left_listbox.insert(tk.END, param)
            # Add sorting functionality here
            sort_telas_by(right_listbox.get(0, tk.END))
        else:
            messagebox.showwarning(
                "Advertencia", "No has seleccionado ninguna fila.")

    tk.Button(ordenar_window, text="Agregar",
              command=add_param).pack(side="top", pady=5)
    tk.Button(ordenar_window, text="Editar",
              command=edit_param).pack(side="top", pady=5)
    tk.Button(ordenar_window, text="Eliminar",
              command=delete_param).pack(side="top", pady=5)
    tk.Button(ordenar_window, text="Mover",
              command=move_param).pack(side="top", pady=5)


def sort_telas_by(order_params):
    def get_sort_key(item):
        values = tree_telas.item(item, 'values')
        sort_value = order_params.index(
            values[0]) if values[0] in order_params else float('inf')
        return sort_value

    items = list(tree_telas.get_children())
    items.sort(key=get_sort_key)

    for index, item in enumerate(items):
        tree_telas.move(item, '', index)


def toggle_ingresos(event=None):
    global Ingresos
    try:
        if Ingresos.state() == "normal":
            Ingresos.withdraw()
        else:
            Ingresos.deiconify()
    except:
        create_ingresos()


def toggle_ingresos_telas(event=None):
    global Ingresos_telas
    try:
        if Ingresos_telas.state() == "normal":
            Ingresos_telas.withdraw()
        else:
            Ingresos_telas.deiconify()
    except:
        create_ingresos_telas()


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

    def generate_solicitud_menu(event):
        solicitud_menu = tk.Menu(root, tearoff=0)
        solicitud_menu.add_command(label="Solicitud de insumos", command=lambda: messagebox.showinfo(
            "Solicitud", "Generando solicitud de insumos"))
        solicitud_menu.add_command(label="Solicitud de producción", command=lambda: messagebox.showinfo(
            "Solicitud", "Generando solicitud de producción"))
        solicitud_menu.post(event.x_root, event.y_root)

    tab_generar_solicitud.bind("<Button-1>", generate_solicitud_menu)


def show_base_de_datos():
    base_datos_window = tk.Toplevel(root)
    base_datos_window.title("Base de datos")
    base_datos_window.geometry("800x200")
    center_window(base_datos_window)

    # Create buttons
    botones = [
        ("Imágenes", lambda: messagebox.showinfo(
            "Imágenes", "Función de Imágenes en desarrollo")),
        ("Colaboradores", lambda: messagebox.showinfo(
            "Colaboradores", "Función de Usuarios en desarrollo")),
        ("Ventas", lambda: messagebox.showinfo(
            "Ventas", "Función de Ventas en desarrollo")),
        ("Compras", lambda: messagebox.showinfo(
            "Compras", "Función de Compras en desarrollo")),
    ]

    for idx, (text, command) in enumerate(botones):
        btn = tk.Button(base_datos_window, text=text,
                        width=20, command=command)
        btn.grid(row=0, column=idx, padx=5, pady=5)

    close_button = tk.Button(
        base_datos_window, text="Cerrar", command=base_datos_window.destroy)
    close_button.grid(row=1, column=2, pady=10)


# Main Dashboard
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
                        command=lambda name=sector_name: on_click(name))
        btn.grid(row=i, column=j, padx=7, pady=7)

root.mainloop()
