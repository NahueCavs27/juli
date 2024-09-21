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
    load_sales_data(tree_sales)  # aca el final la invocamos para q las carge

# Te agregé esta función para cargar las entradas guardadas en los txt.


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
            guardar_datos(rutas["ventas"], df.to_csv(index=False))
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
