import servidor
port = '1337'
#servidor.inicio_sig(port)
if servidor.testing_server():
    print("TCX: servidor conectado")
else:
    print("TCX: servidor no conectado")