import json
import puerto
import time
APN = "internet.movistar.com.co"
ServerIP = '54.209.236.227'
Port = '1337'
#revisa la senal
def signal():
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
#establecimiento de senal
def inicio_sig(port):
    status = signal()
    if status == "Aceptable":
        puerto.send_at('AT+CGSOCKCONT=1,\"IP\",\"'+APN+'\"','OK',1)
        puerto.send_at('AT+CSOCKSETPN=1', 'OK', 1)
        puerto.send_at('AT+CIPMODE=0', 'OK', 1)
        puerto.send_at('AT+NETOPEN', '+NETOPEN: 0',3)
        print("red abierta")
        puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+port,'+CIPOPEN: 0,0', 3)
        print("servidor conectado")
        time.sleep(1)
        print("RED OK")
        return False
    else:
        print("No hay condiciones de red")
def envio(dato, lng):
    lng_json = str(lng)
    puerto.send_at('AT+CIPSEND=0,' + lng_json, '>', 1)
    json_pe = json.dumps(dato)
    puerto.send_at(json_pe, '+CIPSEND: 0,' + lng_json + ',' + lng_json, 1)
    time.sleep(0.5)
def envio_tr(dato, lng):
    test = signal()
    if test == "Aceptable":
        #revisar verificar conexion
        if puerto.send_at('AT+NETOPEN?', '+NETOPEN: 1',0.5) == '+NETOPEN: 1':
            print("Red abierta")
            if puerto.send_at('AT+CIPOPEN?', '+CIPOPEN: 0,"TCP","54.209.236.227",1337', 0.5) == '+CIPOPEN: 0,"TCP","54.209.236.227",1337':
                print ("servidor activo")
            else:
                puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 3)
                print("servidor conectado")
        else:
            puerto.send_at('AT+NETOPEN', '+NETOPEN: 0',2)
            print("red abierta")
            puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 2)
            print("servidor conectado")
        envio(dato, lng)                
    else:
        print("No hay condiciones de red")