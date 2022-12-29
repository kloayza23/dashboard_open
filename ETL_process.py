# Importacion de librerias
from pymongo import MongoClient
import pandas as pd
import json

# Conexion con MongoDb
mongClient = MongoClient('127.0.0.1', 27017)
db = mongClient.db_iris
# Fase Extraccion
file_data = 'iris.csv'
iris_dat = pd.read_csv(file_data, sep=',')


# Fase transformacion

## Clasificar la data por su variedad
setosa_data=iris_dat[(iris_dat['variety'] == 'Setosa')]
versicolor_data=iris_dat[(iris_dat['variety'] == 'Versicolor')]
virginica_data=iris_dat[(iris_dat['variety'] == 'Virginica')]

# Cantidades por clase
cant_setosa=len(setosa_data)
cant_versicolor=len(versicolor_data)
cant_virginica=len(virginica_data)

# Totales por variedad
cant_tot_variedad = [cant_setosa, cant_versicolor, cant_virginica]
print(cant_tot_variedad)
label_variedad =['Setosa','Versicolor','Virginica']

df_cant_variedad = pd.DataFrame(cant_tot_variedad,index=label_variedad,columns =['Variedad'])
# Fase Carga (Loading)

setosa_coll = json.loads(setosa_data.T.to_json()).values()
db.setosa.drop()
db.setosa.insert(setosa_coll)
versicolor_coll = json.loads(versicolor_data.T.to_json()).values()
db.versicolor.drop()
db.versicolor.insert(versicolor_coll)
virginica_coll = json.loads(virginica_data.T.to_json()).values()
db.virginica.drop()
db.virginica.insert(virginica_coll)
cant_variedad_coll = json.loads(df_cant_variedad.to_json()).values()
db.cant_variedad.drop()
db.cant_variedad.insert(cant_variedad_coll)

    