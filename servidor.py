import json
import puerto
import time
APN = "internet.movistar.com.co"
ServerIP = '54.209.236.227'
Port = '1337'
#revisa la senal
def signal():
    param = 5
    ans = puerto.send_at('AT+CSQ','OK',0.5)
    ans_a = ans.split(',')
    ans_b = ans_a[0].split(':')    
    ans_p = int(ans_b[1].strip())
    if ans_p != None:
        if param <= ans_p <30:
            return "Aceptable"
        if ans_p < param:
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
        puerto.send_at('AT+NETOPEN', '+NETOPEN: 0',2)
        print("red abierta")
        puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+port,'+CIPOPEN: 0,0', 3)
        print("servidor conectado")
        time.sleep(1)
        print("RED OK")
        return False
    else:
        print("Inic: No hay condiciones de red")
def envio(dato, lng):
    lng_json = str(lng)
    puerto.send_at('AT+CIPSEND=0,' + lng_json, '>', 1)
    json_pe = json.dumps(dato)
    puerto.send_at(json_pe, '+CIPSEND: 0,' + lng_json + ',' + lng_json, 1)
    time.sleep(0.5)
def testing_server():
    test = signal()
    if test == "Aceptable":
        #revisar verificar conexion
        net = puerto.send_at('AT+NETOPEN?', '+NETOPEN: 1',0.5)
        #print(net)
        if '+NETOPEN: 1' in net:
            print("Rev: red abierta")
            server = puerto.send_at('AT+CIPOPEN?', '+CIPOPEN: 0,"TCP","54.209.236.227",1337', 0.5)
            #print(server)
            if '+CIPOPEN: 0,"TCP","54.209.236.227",1337' in server:
                print ("Rev: servidor activo")
                return True
            else:
                act = puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 2.5)
                print("Revc: servidor conectado")
                if "Back: command error" in act:
                    return False
                else:
                    return True
        else:
            puerto.send_at('AT+NETOPEN', '+NETOPEN: 0',2)
            print("Revc: red abierta")
            act2 = puerto.send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 2)
            if "Back: command error" in act2:
                return False
            else:
                print("Revc: servidor conectado")
                return True                
    else:
        print("Test: No hay condiciones de red")
        return False