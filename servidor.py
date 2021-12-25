import json
import puerto
import mysql.connector
import time
APN = "internet.movistar.com.co"
#establecimiento de senal
def inicio_sig():
    puerto.send_at('AT+CREG?','+CREG: 0,1',1)
    puerto.send_at('AT+CPSI?','OK',1)
    puerto.send_at('AT+CGREG?','+CGREG: 0,1',0.5)
    puerto.send_at('AT+CGSOCKCONT=1,\"IP\",\"'+APN+'\"','OK',1)
    puerto.send_at('AT+CSOCKSETPN=1', 'OK', 1)
    puerto.send_at('AT+CIPMODE=0', 'OK', 1)
    print("inicio ok")
#conexion base de datos mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="sigri",
  password="Innova-sigri***2021",
  database="db_sgcp"
)
#revisa la senal
def signal ():
    ans = puerto.send_at('AT+CSQ','OK',1)
    ans_a = ans.split(',')
    ans_b = ans_a[0].split(':')    
    ans_p = int(ans_b[1].strip())
    if ans_p != None:
        if 10<=ans_p<30:
            return "Aceptable"
        if ans_p<9:
            return "Mala"
    else:
        print ("error signal")
        return "no"
def envio(dato):
    ServerIP = '54.209.236.227'
    Port = '1337'
    puerto.send_at('AT+NETOPEN', '+NETOPEN: 0',3)
    print("red abierta")
    puerto.send_at('AT+IPADDR', '+IPADDR:', 1)
    puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 3)
    time.sleep(3)
    puerto.send_at('AT+CIPSEND=0,101', '>', 1)
    json_pe = json.dumps(dato)
    #print(json_pe)
    print(puerto.send_at(json_pe, '+CIPSEND: 0,101,101', 1))
    time.sleep(2)    
    puerto.send_at('AT+CIPCLOSE=0','+CIPCLOSE: 0,0',5)
    puerto.send_at('AT+NETCLOSE', '+NETCLOSE: 0', 2)
try:
    #inicio_sig()
    #peticiones base de datos
    mycursor = mydb.cursor()
    sesion = True
    while sesion:
        #peticion id sin enviar
        sql_1 = "select id_dato from tbl_datos_gps where Envio = 0"
        mycursor.execute(sql_1)
        rsl = mycursor.fetchall()
        for i in rsl:
            print (len(rsl))
            if len(rsl) != 0:
                test = signal()
                if test == "Aceptable":
                    #obtiene datos para los id que no han sido enviados
                    sql_2 = "select Latitud, Longitud, Fecha, Hora, recorrido from tbl_datos_gps where id_dato = " + str(i[0])
                    mycursor.execute(sql_2)
                    rsl_1 = mycursor.fetchall()
                    #print(rsl_1[0][0])
                    json_fpe = {"lat": rsl_1[0][0], "log": rsl_1[0][1], "date": rsl_1[0][2], "time": rsl_1[0][3], "pasajero": 60}
                    envio(json_fpe)
                    print("envio exitoso")
                else:
                    print("no hay condiciones")
            else:
                print("No hay datos para enviar")
except KeyboardInterrupt:
    puerto.apagado()
    mydb.close()
