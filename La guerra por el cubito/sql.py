import sqlite3
def generar_sql():
    with sqlite3.connect("tabla_score.db") as conexion:
        try:
            sentencia = ''' create  table jugadores
            (
            id integer primary key autoincrement,
            nombre text,
            score real
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla personajes")                       
        except sqlite3.OperationalError:
            print("La tabla personajes ya existe")
def ingresar_datos_sql(name:str,score:float):
    with sqlite3.connect("tabla_score.db") as conexion:
        try:
            conexion.execute("insert into jugadores(nombre,score) values (?,?)", (name,score))
            conexion.commit()# Actualiza los datos realmente en la tabla
        except:
            print("Error")
def generar_lista_sql():
    with sqlite3.connect("tabla_score.db") as conexion:
        try:
            tupla_sql = conexion.execute("SELECT * FROM jugadores")
            lista_ranking = []
            for tupla in tupla_sql:
                dic = {}
                dic["name"] = tupla[1]
                dic["score"] = tupla[2]
                lista_ranking.append(dic)
            return lista_ranking
        except:
            print("Error al generar la lista")
