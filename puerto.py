import serial
import time
#seleccion puerto para comandos AT
ser = serial.Serial('/dev/ttyUSB2',115200)
ser.flushInput()
rec_buff = ''
#funcion para enviar comandos AT
def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return "error"
        else:
            return rec_buff.decode()
    else:
        print('Device is not connected')
        return "error"
def apagado():
    if ser != None:
        send_at('AT+CGPS=0','OK',1)
        time.sleep(3)
        print('GPS apagado')
        ser.close()