import tkinter as tk
from tkinter import messagebox
from utils import center_window
from globals import root


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
