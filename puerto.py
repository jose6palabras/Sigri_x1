import serial
import time
#seleccion puerto para comandos AT
ser = serial.Serial('/dev/ttyTHS1',115200)
ser.flushInput()
rec_buff = ''
#funcion para enviar comandos AT
def send_at(command,back,timeout):
    ser.flushInput()
    ser.flushOutput()
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.1 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            ser.flushInput()
            ser.flushOutput()
            return "command error"
        else: 
            result = rec_buff.decode()
            ser.flushInput()
            ser.flushOutput()
            return result
    else:
        print('Device is not connected')
        ser.flushInput()
        ser.flushOutput()
        return "error"
def apagado():
    if ser != None:
        send_at('AT+CGPS=0','OK',1)
        time.sleep(3)
        print('GPS apagado')
        ser.close()
