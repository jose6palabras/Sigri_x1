#!/usr/bin/python
#+CGPSINFO: [<lat>],[<N/S>],[<log>],[<E/W>],[<date>],[<UTC time>],[<alt>],[<speed>],[<course>]
import mysql.connector
import gps
import puerto
import servidor
#variables y listas globales
Port = '1337'
#conexion base de datos mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="sigri",
  password="Innova-sigri***2021",
  database="db_sgcp"
)
servidor.inicio_sig(Port)
try:
    inicio = True
    while inicio:
        inicio = gps.gps_inicio()
    sesion = True
    mycursor = mydb.cursor()
    while sesion:
        inf_gps = gps.gps_data()        
        sql = "INSERT INTO tbl_datos_gps (Latitud, Longitud, Fecha, Hora, recorrido, Envio) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (inf_gps["lat"], inf_gps["log"], inf_gps["date"], inf_gps["time"], inf_gps["distancia"], False)
        mycursor.execute(sql, val)
        mydb.commit()
        json_tr = {"lat": inf_gps["lat"], "log": inf_gps["log"], "date": inf_gps["date"], "time": inf_gps["time"], "pasajero": 60}
        lng_json_tr = len(json_tr)
        servidor.envio_tr(json_tr, lng_json_tr)
except KeyboardInterrupt:
    puerto.apagado()
    mydb.close()



