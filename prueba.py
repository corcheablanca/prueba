
import pandas as pd
import numpy as np
import urllib.request
import json  
from pandas.io.json import json_normalize  
import sqlalchemy
import time

#iniciamos el tiempo de ejecucion

start_time = time.time()

#descargamos el json
import urllib.request, json 
with urllib.request.urlopen("http://dummy.restapiexample.com/api/v1/employees") as url:
    data = json.loads(url.read().decode())

with open('personal.json', 'w') as json_file:
    json.dump(data, json_file)
    
#abrimos el json con pandas
with open('personal.json') as access_json:   
     read_content =json.load(access_json)

datos= read_content["data"]

df = pd.DataFrame(data=json_normalize(datos[1::]))
df=df.sort_values("employee_salary",ascending=False)

# obtenemos los mejores salarios
df=df.iloc[3:8]

#los escribimos en la base de datos "salarios_sql"
engine =sqlalchemy.create_engine("mysql+pymysql://rooot:@localhost:3306")
df.to_sql("salarios_sql", con=engine, index=False, if_exists="replace")

#luego en el json "salarios_json"
df.to_json("salarios_json")

#impriimimos el tiempo de ejecucion
print("--- %s seconds ---" % (time.time() - start_time))
