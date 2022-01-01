import puerto
import time
#variables y listas globales
distancia = []
#inicio GPS
def gps_inicio():
    puerto.send_at('AT+CGPS=1','OK',1)
    print('Inciando GPS')
    time.sleep(10)
    print('Probando señal GPS')
    rec_null = True
    answer = ''
    while rec_null:
        answer = puerto.send_at('AT+CGPSINFO','+CGPSINFO: ',1)
        if answer != None:
            if ',,,,,,' in answer:
                print('GPS is not ready')
            else:
                rec_null = False
                print("GPS is ready")
                return False
        else:
            print('error %d'%answer)            
            rec_null = False
            return False

#peticion trama gps
def get_gps_position():
    rec_null = True
    answer = ''
    while rec_null:
        answer = puerto.send_at('AT+CGPSINFO','+CGPSINFO: ',1)
        if answer != None:
            if ',,,,,,' in answer:
                print('GPS is not ready')
            else:
                rec_null = False
                return answer
        else:
            print('error %d'%answer)            
            rec_null = False
#Organiza la trama gps por datos
def gps_data():
    trama_1 = get_gps_position()
    print(trama_1)
    trama = trama_1.split(",")
    fecha_s = str(trama[4])
    temp_s = str(trama[5])
    vel_s = float(trama[7])*1.852# rapidez m/s
    log_s = str(trama[2])
    lat_f = trama[0].split(":")
    lat_s = lat_f[1].strip()
    #calcula la distancia instantanea
    x_ins = vel_s*0.000694444444
    distancia.append(abs(x_ins))
    #calcula la distancia total recorrida
    dist_tri = str(sum(distancia))
    gps_dictionary = {"lat":lat_s, "log":log_s, "date":fecha_s, "time":temp_s, "distancia": dist_tri}
    return gps_dictionary
