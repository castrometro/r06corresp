import tkinter as tk
from tkinter import filedialog, messagebox
import os

def status_manejo_archivos():
    print("Modulo de manejo de archivos funcionando exitosamente")
    return True

def obtener_ruta_archivo(titulo,tipo_archivo):
    #"*.xlsx" para xlsx
    if tipo_archivo == "Archivos Excel":
        ruta_archivo = filedialog.askopenfilename(title=titulo, filetypes=[(tipo_archivo, '*.xls'), (tipo_archivo, '*.xlsx')])
    else:
        ruta_archivo = filedialog.askopenfilename(title=titulo, filetypes=[(tipo_archivo, '*')])
    if not ruta_archivo:
        return None
    return ruta_archivo

def obtener_ruta_carpeta(titulo):
    ruta_carpeta = filedialog.askdirectory(title=titulo)
    if not ruta_carpeta:
        return None
    return ruta_carpeta

def list_to_txt(nombre_lista,lista, nombre, path):
    full_path = os.path.join(path, nombre + '.txt')
    with open(full_path, 'w') as f:
        f.write(nombre_lista + '\n')
        for item in lista:
            f.write("%s\n" % item)
    return full_path

def exportar_tupla_txt(data, ruta_carpeta, nombre_archivo):
    # Abrir un archivo en modo de escritura en la ruta especificada
    with open(os.path.join(ruta_carpeta, nombre_archivo + '.txt'), 'w') as f:
        # Iterar sobre los elementos de la tupla
        for message, value in data:
            # Escribir cada elemento en una línea del archivo
            formatted_message = f"{message} {value}"
            f.write(formatted_message + '\n')

        

    