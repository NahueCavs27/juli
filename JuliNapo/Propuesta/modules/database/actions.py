import os
import pandas as pd


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
