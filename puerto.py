import serial
import time
#seleccion puerto para comandos AT
puerto1 = '/dev/ttyUSB2'
puerto2 = '/dev/ttyTHS1'
ser = serial.Serial(puerto1,115200)
ser.flushInput()
rec_buff = ''
def clean_buffer():
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
#funcion para enviar comandos AT
def send_at(command,back,timeout):
    clean_buffer()
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.1 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            #print(command + ' ERROR')
            #print(command + ' back:\t' + rec_buff.decode())
            clean_buffer()
            return "Back: command error"
        else: 
            result = rec_buff.decode()
            clean_buffer()
            return result
    else:
        print('Device is not connected')
        clean_buffer()
        return "error"
def apagado():
    if ser != None:
        send_at('AT+CGPS=0','OK',1)
        time.sleep(3)
        print('GPS apagado')
        ser.close()
