/*
PROTIPO servidor TCP/IP para menejo del programa EN-Ruta
funcionamiento: el cliente envia un codigo pertenenciente a un tag personal. El servidor al recibir este tag 
busca en la base de datos que está escrita en mysql si el codigo enviado pertenece o no a un usuario del 
programa En-Ruta. 
Si el usuario no pertenece al programa el servidor le regresara al usuario el mensaje "usuario no registrado/. 
codigo erroneo". Si el usuario está registrado el servidor le regresara al cliente, el nombre del usuario, 
el perfil del usuario, y saldo actual. el servidor en su interior registrara en la base de datos el saldo 
anterior y el descuento por el viaje realizado, también registrara hora y fecha de la lectura.
*/
var net = require('net');//se requiere el modulo net de node.js, en el estan las librerias para manejar las caracteristicas del protocolo TCP/IP.
var mysql = require('mysql');//se requiere el modulo mysql para permitir la conexion entre el servidor y la BD.
var ac_mysql = require("./ac_mysql");//se require el modulo ac_mysql que es un modulo propio del proyecto, para el manejo de la base de datos.
/*
se crea la funcion servidor, esta contiene el inicio del servidor en el puerto 1337 y algunas de sus acciones
*/
function servidor (){
  var registro = {};
  net.createServer(function(socket) {
    socket.name = socket.remoteAddress + ":" + socket.remotePort; //a socket le define el atributo name
    //socket.write("Welcome " + socket.name + " ;\n"); //le regresa al cliente por medio del metodo write un mensaje
    console.log("cliente en linea:" + socket.name); //escribe en la terminal del servidor el mensaje
    //a continuacion se activa el socket para recibir los datos enviados del cliente y se crea una funcion para manejar los datos que lleguen del cliente.
    socket.on('data', function(data){
      console.log(socket.name + ': ' + data);//escribe en la terminal del servidor el mensaje 
      registro.code = data;
      ac_mysql.mysql_acceso(data, socket);//se llama del modulo ac_mysql el metodo mysql_acceso.
    });
    //se define una funcion para cuando el cliente se desconete
    socket.on('end', function(){
      console.log('cliente fuera');
    });
    socket.pipe(socket);
  }).listen(1337, function(){
  console.log("servidor activo");
  });
}
servidor();
