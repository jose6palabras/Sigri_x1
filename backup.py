import mysql.connector
import puerto
import servidor
import time
import json
Port = '1337'
ServerIP = servidor.ServerIP
#conexion base de datos mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="sigri",
  password="Innova-sigri***2021",
  database="db_sgcp"
)
try:
    start_s = True
    while start_s:
        start_s = servidor.inicio_sig(Port)
    #peticiones base de datos
    mycursor = mydb.cursor()
    sesion = True
    while sesion:
        #peticion id sin enviar
        sql_1 = "select id_dato from tbl_datos_gps where Envio = 0"
        mycursor.execute(sql_1)
        rsl = mycursor.fetchall()
        if len(rsl) != 0:
            test = servidor.signal()
            if test == "Aceptable":                
                for i in rsl:
                    #obtiene datos para los id que no han sido enviados
                    sql_2 = "select Latitud, Longitud, Fecha, Hora, recorrido from tbl_datos_gps where id_dato = " + str(i[0])
                    mycursor.execute(sql_2)
                    rsl_1 = mycursor.fetchall()
                    json_fpe = {"lat": rsl_1[0][0], "log": rsl_1[0][1], "date": rsl_1[0][2], "time": rsl_1[0][3], "pasajero": 60}
                    len_json = len(json.dumps(json_fpe))
                    print(json_fpe)
                    servidor.envio(json_fpe, len_json)
                    print("envio exitoso")
                    slq_3 = "update tbl_datos_gps set Envio = true where id_dato = " + str(i[0])
                    mycursor.execute(slq_3)
                    mydb.commit()
            else:
                print("No hay condiciones")
        else:
            print("No hay datos para enviar")
except KeyboardInterrupt:
    puerto.send_at('AT+CIPCLOSE=0','+CIPCLOSE: 0,0',5)
    puerto.send_at('AT+NETCLOSE', '+NETCLOSE: 0', 2)
    puerto.apagado()
    mydb.close()
