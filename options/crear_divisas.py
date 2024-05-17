from modules.manejo_archivos import status_manejo_archivos, obtener_ruta_archivo, obtener_ruta_carpeta, exportar_tupla_txt
from modules.excel import excel_to_df, status_modulo_excel, xls_to_df, agrupar_df, merge_df, operatoria_entre_columnas, df_to_excel, formatear_columna_df, suma_columna_excel, ajustar_ancho_columnas, buscar_filas_df_contiene, filtrar_filas_por_valor, filtrar_filas_por_valores
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


def status_generar_divisas():
    print("Modulo generar Divisas Pendientes funcionando exitosamente")
    return True


def generar_divisas():  
    #status manejo archivos
    if not status_manejo_archivos():
        print("Error en el modulo de manejo de archivos")
        raise Exception("Error en el modulo de manejo de archivos")
    #status modulo excel
    if not status_modulo_excel():
        print("Error en el modulo de manejo de excel")
        raise Exception("Error en el modulo de manejo de excel")
    
    #obtener rutas de archivos
    ruta_reclasif_op = obtener_ruta_archivo("Selecciona el archivo Reclasificacion de Operaciones", "Archivos Excel")
    if not ruta_reclasif_op:
        print("No se seleccionó ningún archivo Reclasificacion de Operaciones")
        raise Exception("No se seleccionó ningún archivo Reclasificacion de Operaciones")

    ruta_corto_plazo = obtener_ruta_archivo("Selecciona el archivo cp", "Archivos Excel")
    if not ruta_corto_plazo:
        print("No se seleccionó ningún archivo cp")
        raise Exception("No se seleccionó ningún archivo cp")
    
    ruta_diccio = obtener_ruta_archivo("Selecciona el archivo Diccionario", "Archivos Excel")
    if not ruta_diccio:
        print("No se seleccionó ningún archivo Diccionario")
        raise Exception("No se seleccionó ningún archivo Diccionario")
    
    print(f"Ambas rutas leidas de manera exitosa {ruta_reclasif_op}, {ruta_corto_plazo} y {ruta_diccio}")

    #carga de archivos en dataframes
    reclasif_op = excel_to_df(ruta_reclasif_op, 1, 'B:K')
   
    try:
        # Lista de columnas que deseas mantener
        columnas_a_mantener = ['CUENTA', 'Mon.', 'No Operación', 'Monto Vigente']
        # Seleccionar solo las columnas deseadas del DataFrame original
        reclas1 = reclasif_op[columnas_a_mantener]
        print(reclas1.head())
    except KeyError as e:
        print(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
        raise Exception(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
    



    corto_plazo = excel_to_df(ruta_corto_plazo, None, None)

    try:
        cp = corto_plazo.iloc[:, :-1]
        cp = cp.drop(columns=['clasificacion_soberano'])
        print(cp.head())
    except KeyError as e:
        print(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
        raise Exception(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
    diccio = excel_to_df(ruta_diccio, None, None)

    #Modificaciones para CP
    cp.rename(columns={'rut': 'RUT'}, inplace=True)

    #Modificaciones para Reclasificacion de Operaciones
    # Lista de cuentas a filtrar:
    cuentas = [2115221002, 2115321168]

    reclas1 = filtrar_filas_por_valores(reclas1, 'CUENTA', cuentas)
    lista_agrupar = ['CUENTA', 'Mon.', 'No Operación']
    lista_sumar = ['Monto Vigente']
    reclas1 = agrupar_df(reclas1, lista_agrupar, lista_sumar)
    print(reclas1.head())

    #objetivo: reemplazar No Operacion por rut
    df_temp = filtrar_filas_por_valores(diccio, 'KGL', reclas1['No Operación'].tolist())
    print(df_temp.head())




