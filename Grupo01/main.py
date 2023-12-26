import funciones as f

# Solicitar al usuario las rutas de los archivos CSV
rutas_csv = {}

nombre_archivo = input("Introduce el nombre del archivo: ")
    
ruta_archivo = input(f"Introduce la ruta del archivo {nombre_archivo}: ")
rutas_csv[nombre_archivo] = ruta_archivo

# Cargar los archivos CSV utilizando la función del módulo funciones
dataframe = f.cargar_archivo_csv(rutas_csv)

# Realizar otras operaciones o análisis con los dataframes si es necesario
print(f"\nInformación de {nombre_archivo}:\n")
f.detectar_caracteres_especiales(dataframe)

print(f"\nAnálisis de datos para {nombre_archivo}:\n")
f.analizar_datos(dataframe)

print("\nVerificación de columnas de fecha:\n")
f.verificar_columnas_de_fecha(dataframe)

print("\nEvaluación de la calidad del archivo:\n")
f.evaluar_calidad_archivo(dataframe)