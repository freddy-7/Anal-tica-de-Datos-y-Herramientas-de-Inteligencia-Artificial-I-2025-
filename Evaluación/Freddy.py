###################### Función para cargar un archivo como un dataframe################################

def cargar_dataset(archivo):  #La entrada es un archivo
    import pandas as pd
    import os
    #Si se desea agregar un input se coloca:
#   archivo=input("Por favor, ingresa el nombre del archivo: ")
    extension = os.path.splitext(archivo)[1].lower()
# Cargar el archivo según su extensión
    if extension == '.csv':
        df= pd.read_csv(archivo)
        return (df)
    elif extension == '.xlsx':
        df= pd.read_excel(archivo)
        return (df)
    else:
            raise ValueError(f"Este formato no esta soportado para esta función: {extension}")
        
######################Función_Contar_Nulos############################################
def cuenta_nulos(df):
    #Valores nulos por columna
    valores_nulos_cols = df.isnull().sum()
    #Valores nulos por dataframe
    valores_nulos_df = df.isnull().sum().sum()
    
    return("Valores nulos por columna", valores_nulos_cols,
            "Valores nulos por dataframe", valores_nulos_df)
    
#######################Función_Nulos########################################
def limpieza_nulos(df):
    import pandas as pd
    #Separo las columnas impares
    impares = df.iloc[:, 1::2] 
    #Separo las columnas pares
    pares = df.iloc[:, 0::2]
    
    #Separo columnas cuantitativas impares del dataframe
    cuantitativas_impares= impares.select_dtypes(include=['float64', 'int64','float','int'])
    #Sustituir valores nulos por un valor numérico en  concreto 
    cuantitativas_impares= cuantitativas_impares.fillna(99) 
    
    #Separo columnas cuantitativas pares del dataframe
    cuantitativas_pares= pares.select_dtypes(include=['float64', 'int64','float','int'])
    #Sustituir valores nulos con promedio o media
    cuantitativas_pares=cuantitativas_pares.fillna(round(cuantitativas_pares.mean(),1))
    
    #Separo columnas cualitativas impares del dataframe 
    cualitativas_impares= impares.select_dtypes(include=['object', 'datetime','category'])
    #Sustituir valores nulos por un string en  concreto
    cualitativas_impares =cualitativas_impares.fillna("Este_es_un_valor_nulo") 
        
    #Separo columnas cualitativas pares del dataframe 
    cualitativas_pares= pares.select_dtypes(include=['object', 'datetime','category'])
    #Sustituir valores nulos por un string en  concreto 
    cualitativas_pares =cualitativas_pares.fillna("Este_es_un_valor_nulo") 
    
    # Unimos el dataframe cuantitativo limpio con el dataframe cualitativo
    df = pd.concat([cuantitativas_impares, cuantitativas_pares, cualitativas_impares,
                    cualitativas_pares], axis=1)
    return(df)
    
#######################Función_Atipicos########################################
def limpieza_atipicos(df):
    import pandas as pd
    #Separo columnas cuantitativas del dataframe
    cuantitativas= df.select_dtypes(include=['float64', 'int64','float','int'])
    #Separo columnas cualitativas del dataframe
    cualitativas = df.select_dtypes(include=['object', 'datetime','category'])
    
    #Método aplicando Cuartiles. Encuentro cuartiles 0.25 y 0.75
    y=cuantitativas

    percentile25=y.quantile(0.25) #Q1
    percentile75=y.quantile(0.75) #Q3
    iqr= percentile75 - percentile25

    Limite_Superior_iqr= percentile75 + 1.5*iqr
    Limite_Inferior_iqr= percentile25 - 1.5*iqr

    #Obtenemos datos limpios del Dataframe
    data_iqr= cuantitativas[(y<=Limite_Superior_iqr)&(y>=Limite_Inferior_iqr)]
    data_iqr
    
    #Reemplazamos valores atípicos (nulos) del dataframe con "mean"
    #Realizamos una copia del dataframe
    data_iqr=data_iqr.fillna(round(data_iqr.mean(),1))
    data_iqr
    
    # Unimos el dataframe cuantitativo limpio con el dataframe cualitativo

    Datos_limpios= pd.concat([cualitativas, data_iqr], axis=1)
    Datos_limpios
    
    return(Datos_limpios)