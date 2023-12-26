import os
import pandas as pd
import unicodedata

def cargar_archivo_csv(rutas):
    """
    Carga archivos CSV y trata de convertir columnas con fechas en formato 'yyyy-mm-dd' a objetos de fecha.

    Parámetros:
    - rutas (dict): Diccionario con nombres y rutas de archivos CSV.

    Retorna:
    - pd.DataFrame: DataFrame cargado.
    """
    for nombre_archivo, ruta_archivo in rutas.items():
        if os.path.exists(ruta_archivo):
            df = pd.read_csv(ruta_archivo, delimiter=';')

            # Inspeccionar cada columna
            for columna in df.columns:
                # Intentar convertir la columna a datetime si contiene datos en formato yyyy-mm-dd
                try:
                    df[columna] = pd.to_datetime(df[columna], errors='raise', format='%Y-%m-%d')
                except (TypeError, ValueError):
                    # Ignorar errores, ya que no todos los datos pueden ser fechas
                    pass
        else:
            print(f"Advertencia: El archivo {nombre_archivo} no existe en la ruta {ruta_archivo}")
    return df

def contar_caracteres_especiales(texto):
    """
    Cuenta el número de mayúsculas y letras especiales en un texto.

    Parámetros:
    - texto (str): Texto a analizar.

    Retorna:
    - dict: Diccionario con el recuento de mayúsculas y letras especiales.
    """
    if isinstance(texto, str):
        return {
            'mayusculas': sum(1 for char in texto if char.isupper()),
            'letras_especiales': sum(1 for char in texto if unicodedata.category(char).startswith('L'))
        }
    else:
        return {'mayusculas': 0, 'letras_especiales': 0}

def detectar_caracteres_especiales(df):
    """
    Detecta y cuenta el número total de mayúsculas y letras especiales en columnas de tipo objeto en un DataFrame.

    Parámetros:
    - df (pd.DataFrame): DataFrame a analizar.

    Retorna:
    - tuple: Total de mayúsculas y letras especiales.
    """
    total_mayusculas = 0
    total_letras_especiales = 0

    for col in df.select_dtypes(include='object').columns:
        recuento_col = df[col].apply(contar_caracteres_especiales)
        total_mayusculas += recuento_col.apply(lambda x: x['mayusculas']).sum()
        total_letras_especiales += recuento_col.apply(lambda x: x['letras_especiales']).sum()

    print(f"Mayúsculas totales: {total_mayusculas}")
    print(f"Letras especiales totales: {total_letras_especiales}") 

    return total_mayusculas, total_letras_especiales 

def analizar_datos(df):
    """
    Realiza un análisis básico de los datos, incluyendo el conteo de nulos, duplicados y muestra algunos datos sin espacios.

    Parámetros:
    - df (pd.DataFrame): DataFrame a analizar.
    """
    nulos = df.isnull().sum()
    duplicados = df.duplicated().sum()
    datos_sin_espacios = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    total_filas = len(df)
    porcentaje_nulos = (nulos / total_filas) * 100
    porcentaje_duplicados = (duplicados / total_filas) * 100

    print(f"Nulos por columna:\n{nulos}\n")
    print(f"Duplicados en el conjunto de datos: {duplicados}\n")
    
    print(datos_sin_espacios.head())

    resultados = pd.DataFrame({
        "Porcentaje de Nulos": porcentaje_nulos,
        "Duplicados": duplicados,
        "Porcentaje de Duplicados": porcentaje_duplicados
    })

    print("\nResultados finales:")
    print(resultados)

def verificar_columnas_de_fecha(df):
    """
    Verifica columnas que contienen fechas y trata de convertirlas a objetos de fecha.

    Parámetros:
    - df (pd.DataFrame): DataFrame a analizar.
    """
    errores_formato = []
    errores_rango = []
    columnas_fecha = []

    for columna in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[columna]):
            columnas_fecha.append(columna)
            try:
                df[columna] = pd.to_datetime(df[columna], errors='raise')
            except pd.errors.OutOfBoundsDatetime:
                errores_rango.append(f"Error de rango en la columna '{columna}'")
            except pd.errors.OutOfBoundsTimedelta:
                errores_rango.append(f"Error de rango en la columna '{columna}'")
            except pd.errors.ParsingError:
                errores_formato.append(f"Error de formato en la columna '{columna}'")

    if columnas_fecha:
        print("Columnas de fecha detectadas:")
        print(columnas_fecha)
    else:
        print("No se encontraron columnas de fecha en el DataFrame.")

    if errores_formato:
        print("\nErrores de formato en fechas:")
        for error in errores_formato:
            print(error)

    if errores_rango:
        print("\nErrores de rango en fechas:")
        for error in errores_rango:
            print(error)

    if not errores_formato and not errores_rango:
        print("\nNo se encontraron errores en las columnas de fecha.")

def evaluar_calidad_archivo(df):
    """
    Evalúa la calidad del archivo basándose en diferentes factores como nulos, duplicados y otros.

    Parámetros:
    - df (pd.DataFrame): DataFrame a evaluar.
    """
    nulos = df.isnull().sum().sum()
    duplicados = df.duplicated().sum()

    total_filas = df.size
    porcentaje_nulos = (nulos / total_filas) * 100
    porcentaje_duplicados = (duplicados / total_filas) * 100

    calidad_global = 10

    calidad_global -= porcentaje_nulos / 2
    calidad_global -= porcentaje_duplicados / 2

    umbral_bueno = 7
    umbral_regular = 5

    if calidad_global >= umbral_bueno:
        resultado = "¡Archivo excelente!"
    elif umbral_regular <= calidad_global < umbral_bueno:
        resultado = "Archivo aceptable, pero podría mejorar."
    else:
        resultado = "¡Archivo necesita limpieza urgente!"

    print(f"Calidad Global del Archivo: {calidad_global:.2f}")
    print(resultado)
