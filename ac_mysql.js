/*
MODULO ac_mysql propio del sistema En-Ruta.
la funcion mysql del modulo toma dos argumentos data y socket, data son los datos que llegan del cliente y 
socket son las caracteristicas del servidor. mysql_acceso recibe el dato del cliente, inicia la base de datos 
verifica si el codigo del cliente pertenece a la base de datos. Si el codigo no esta en la base de datos 
regresa el mensaje "usuario no registrado/. codigo erroneo". Si el usuario está registrado el servidor le 
regresara, el nombre del usuario, el perfil del usuario, y saldo actual.
mysql_acceso registrara en la base de datos el saldo anterior y el descuento por el viaje realizado.
*/

var mysql = require("mysql");
var net = require('net');
/*esta funcion recibe data y socket*/
function mysql_acceso (data, socket){
  var table = "data_x1";
  var DataBase = "db_sgserver";
  //mysql_connection activa la conexion a la base de datos.
  var mysql_connection = mysql.createConnection({
    host: "localhost",
    user: "sigri",
    password: "Innova-sigri***2021",
    database: DataBase
  });
  //alerta por irregularidades en la conexion con la DB o de una conexion exitosa
  mysql_connection.connect(function(err){
    if(err){
      console.log("Error connecting to " + DataBase);
      return;
    }
    console.log("Connection established with " + DataBase + " -> " + table);
  });
  //var key = '{"lat": "7654", "log": "36664", "date": "2023-04-12", "time": "19:19:00", "pasajero": 12}';
  var key = JSON.parse(data);  
 
  var query = "INSERT INTO data_x1 (lat, log, date, time, pasajeros) VALUES ("+key.lat+", "+key.log+", '"+key.date+"', '"+key.time+"', "+key.pasajero+")";
  mysql_connection.query(query, function(err, result){
    if (err){
       throw (err);
       console.log("Error \n");
    }
    else{
      console.log("registro exitoso");
    }
  });
 
  function salida(){
    mysql_connection.end(function(err){
      if (err){
        console.log("Error of closure");
        return;
      }
      else{console.log("exit")}
    });
  }
  salida();
}
exports.mysql_acceso = mysql_acceso;
