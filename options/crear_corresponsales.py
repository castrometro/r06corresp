from modules.manejo_archivos import status_manejo_archivos, obtener_ruta_archivo, obtener_ruta_carpeta, exportar_tupla_txt
from modules.excel import excel_to_df, status_modulo_excel, xls_to_df, agrupar_df, merge_df, operatoria_entre_columnas, df_to_excel, formatear_columna_df, suma_columna_excel, ajustar_ancho_columnas, buscar_filas_df_contiene
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def status_generar_corresponsales():
    print("Modulo generar corresponsales funcionando exitosamente")
    return True

def generar_corresponsales():  

    #status manejo archivos
    if not status_manejo_archivos():
        print("Error en el modulo de manejo de archivos")
        raise Exception("Error en el modulo de manejo de archivos")
    #status modulo excel
    if not status_modulo_excel():
        print("Error en el modulo de manejo de excel")
        raise Exception("Error en el modulo de manejo de excel")
    
    #obtener rutas de archivos
    ruta_dap = obtener_ruta_archivo("Selecciona el archivo DAP", "Archivos Excel")
    if not ruta_dap:
        print("No se seleccionó ningún archivo DAP")
        raise Exception("No se seleccionó ningún archivo DAP")

    ruta_cp = obtener_ruta_archivo("Selecciona el archivo CP", "Archivos Excel")
    if not ruta_cp:
        print("No se seleccionó ningún archivo CP")
        raise Exception("No se seleccionó ningún archivo CP")
    
    print(f"Ambas rutas leidas de manera exitosa {ruta_dap} y {ruta_cp}")
    
    #carga de archivos en dataframes
    dap_original = xls_to_df(ruta_dap)
    try:
        columnas_a_eliminar = ['fecha', 'COD BANCO', 'MATRIZ', 'PAIS', 'DESCRIPCION', 'PRODUCTO', 'Saldo Financiero MO', 'sdo_orig', 'CUENTA']
        dap = dap_original.drop(columns=columnas_a_eliminar)
        print(dap.head())
    except KeyError as e:
        print(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
        raise Exception(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
    
    cp_original = excel_to_df(ruta_cp, None, None)
    try:
        cp = cp_original.iloc[:, :-1]
        cp= cp.drop(columns=['clasificacion_soberano'])
        print(cp.head())
    except KeyError as e:
        print(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
        raise Exception(f"Error: una o más columnas no se encontraron en el DataFrame. {e}")
    #print("Dataframes creados exitosamente")

    #Modificaciones para DAP
    lista_agrupar = ['RUT', 'MONED']
    lista_sumar = ['sdo_peso']
    dap = agrupar_df(dap, lista_agrupar, lista_sumar)
    print(dap.head())

    #Modificaciones para CP
    cp.rename(columns={'rut': 'RUT'}, inplace=True)

    #Merge de dataframes
    cp_dap, unique_cp, unique_dap = merge_df(cp, dap, 'RUT')   
    #unique_cp son los rut que estan en cp pero no en dap
    #unique_dap son los rut que estan en dap pero no en cp
    #print(cp_dap.head())
    df_temp = buscar_filas_df_contiene(cp_dap, 'RUT', unique_dap)
    print(df_temp.head())
    #tengo ahora en df temp los datos de dap que no se encontraron en cp
    # while len(unique_dap) > 0:



    #Funcion para analizar los unique_dap con tkinter
    #1. Pasar a un df los unique_dap (rut, entidad, pais)
    #   Mientras cantidad de filas en unique_dap > 0
    #2. Mostrar df: No se encontraron los siguientes rut: (rut::entidad::pais)
    #3. Mostrar menú de opciones: ¿Que desea hacer?
    #4. op1, 2, 3
    #4.1. Opcion 1: Ignorar y no colocar en r06
    #4.2. Opcion 2: Buscar coincidencias en prc por NOMBRE, PAIS 
    #4.2.1 Mostrar coincidencias en un menú desplegable
    #4.2.2 Elegir una fila o cancelar. (Cancelar -> menu anterior) (Elegir -> hacer el merge denuevo pero solo con ese dato que no se habia encontrado)
                                        # Repetir




    #calculo de RWA (monto x factor de riesgo)
    cp_dap = operatoria_entre_columnas(cp_dap, 'sdo_peso', 'prc_cortoplazo', '*', 'RWA')

    #expotar dataframe a excel
    ruta_carpeta = obtener_ruta_carpeta('Selecciona la carpeta donde guardar el archivo')
    if not ruta_carpeta:
        print("No se seleccionó ninguna carpeta")
        raise Exception("No se seleccionó ninguna carpeta")
    ruta_excel = df_to_excel(cp_dap, 'Corresponsales', ruta_carpeta)  

    #formatear columnas
    suma_columna_excel(ruta_excel, None, 'sdo_peso')
    formatear_columna_df(ruta_excel,None,'RWA','numero')
    formatear_columna_df(ruta_excel,None,'sdo_peso','numero')
    formatear_columna_df(ruta_excel,None,'prc_cortoplazo','porcentaje')

    #analisis de datos
    cantidad_unique_cp = len(unique_cp)
    cantidad_unique_dap = len(unique_dap)
    sdo_peso_dap = dap['sdo_peso'].sum()
    sdo_peso_r06 = cp_dap['sdo_peso'].sum()

    #formato
    ajustar_ancho_columnas(ruta_excel, 40, None)


    messagebox.showinfo("Estado RUT", "RUT en DAP faltantes: " + str(cantidad_unique_dap))
    messagebox.showinfo("Estado", "Sumas sdo_peso_dap: " + str(dap['sdo_peso'].sum()) + '\n' + "Sumas sdo_peso_r06: " + str(cp_dap['sdo_peso'].sum()))

    #exportar informacion a txt
    informacion = [
        ("RUT en DAP faltantes:", cantidad_unique_dap),
        ("Sumas sdo_peso_dap:", sdo_peso_dap),
        ("Sumas sdo_peso_r06:", sdo_peso_r06)
    ]
    for i in range(len(unique_dap)):
        informacion.append(("RUT" + str(i) + " en DAP faltante:", str(unique_dap[i]).replace('.0','')))
    exportar_tupla_txt(informacion, ruta_carpeta, 'informacion')
    
    #print (dap.head()) 
    #print (cp.head())
    return None
    

 
    



