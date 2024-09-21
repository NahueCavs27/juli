# Centrar pantalla
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Ordenar filas por columna


def sort_rows(tree):
    items = tree.get_children()
    sorted_items = sorted(items, key=lambda item: tree.item(item)["values"])
    for idx, item in enumerate(sorted_items):
        tree.move(item, '', idx)
