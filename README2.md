# Tarea 3 
## Consideraciones
- Al abrir el archivo .pkt el *Laptop Ruzpedia* puede que no se conecte automáticamente al dispositivo inalámbrico correspondiente, por lo que hay que ver en las redes disponibles del laptop y conectarlo al *Access Point Ruzpedia* (generalmente es el que tiene menos señal).
- Debido a lo anterior, a veces se desconfigura el *Laptop Ruzpedia*. En caso de que esto ocurra, hay que configurarlo de nuevo (perdón por esto pero se nos desconfiguraba solo). En *settings* hay que poner la dirección en estática, donde la *default gateway* sería 172.67.7.1 y el servidor DNS es 3.3.0.2. Luego en la configuración inalámbrica (*wireless*), la dirección IPv4 es 172.67.7.3.
- No sabíamos si el paquete TCP era necesario considerarlo, pero de todas formas está descrito en la segunda simulación. 

## Paquete ICMP: Casa Alumno a DNS Server

1. Largo en bits de la dirección IP de destino: 32 bits.
2. Dirección IP de origen: 192.168.3.2
3. Dirección IP de origen: 3.3.0.2
4. A continuación se muestran las etapas separadas por capas:
### In Layers

#### Layer 1
1. FastEthernet0 receives the frame. En esta capa el puerto *Fast Ethernet 0* recibe el marco de información entregado por el *Switch DNS*. Esto es parte de la capa física del sistema.
#### Layer 2
1. The frame's destination MAC address matches the receiving port's MAC address, the broadcast address, or a multicast address. En este paso se utiliza un proceso de Address Resolution Protocol (ARP), lo cual es parte del internet protocol, para poder comparar direcciones MAC y que estas coincidan entre ellas. En caso de que no coincidan no se pasa a la tercera capa. Si no se estuviese en el servidor, no se pasaría a la tercera capa y el paquete simplemente se sigue transmitiendo por la línea.
2. The device decapsulates the PDU from the Ethernet frame. Dado que las direcciones comparadas en el paso anterior calzan, se procede a abrir la información contenida en el puerto *Fast Ethernet 0* y se pasa a la tercera capa (*Network Layer*).
#### Layer 3
1. The packet's destination IP address matches the device's IP address or the broadcast address. The device de-encapsulates the packet. Luego de que las direcciones MAC fuesen comparadas en la *Data Link Layer*, se procede a verificar las direcciones de Internet Protocol que trae el mensaje encapsulado, comparando la que viene acá dentro con la del servidor.
2. The packet is an ICMP packet. The ICMP process processes it. Acá se revisa qué tipo de paquete es el que se desencapsulo, y dado que es uno ICMP se procesa, ya que el protocolo ICMP es parte de la tercera capa.
3. The ICMP process received an Echo Request message. Se revisa cuál es el mensaje encapsulado por el paquete ICMP. En resumen, en la capa 2 se trabaja con la información que trae el cuerpo de la IP, mientras que en la tercera capa se revisa ya el paquete ICMP en sí. 

### Out Layers

#### Layer 1
1. FastEthernet0 sends out the frame. En esta capa el puerto *Fast Ethernet 0* envía devuelta el marco de información a *Switch DNS*. Esto es parte de la capa física del sistema.
#### Layer 2
1. The next-hop IP address is a unicast. The ARP process looks it up in the ARP table.
2. The next-hop IP address is in the ARP table. The ARP process sets the frame's destination MAC address to the one found in the table.
3. The device encapsulates the PDU into an Ethernet frame.
#### Layer 3
1. The ICMP process replies to the Echo Request by setting ICMP type to Echo Reply.
2. The ICMP process sends an Echo Reply.
3. The destination IP address 192.168.3.2 is not in the same subnet and is not the broadcast address.
4. The default gateway is set. The device sets the next-hop to default gateway.

## Conexión a www.ruzpedia.com desde Laptop Ruzpedia:

1. Largo en bytes del HTTP Request del paquete HTTP: 4 Bytes (32 bits)
2. Paquetes que se utilizan en la conexión:
    - **DNS**: Este paquete permite obtener la dirección IP de un dominio respectivo al cual se quiere acceder. Esto permite que el acceso a un dominio web sea más fácil, ya que al querer acceder a *www.ruzpedia.com*, el paquere DNS entregará la dirección adecuada, que en este caso sería *172.67.7.2*. Este paquete debe contener una query con la question que se realiza, una query con la answer respectiva a la IP que se solicitó, un DNS Message, un datagrama de usuario (UDP) como capa de transporte, y las IPs de origen y destino del paquete.
    - **TCP**: Es un protocolo de control de transporte que permite establecer la conexión entre dos puntos de una red, en este caso del Laptop y el Servidor (ambos de la subred *Ruzpedia*). Teniendo la dirección del dominio (entegada por el paquete DNS) se intenta establecer esta conexión entre ambos puntos, para luego enviar el paquete HTTP con la request respectiva. El paquete TCP debe contener las direcciones de IP tanto del dispositivo de origen como la del destino (un dominio web en este caso). Además, debe contener el resto de la información ("payload) de un protocolo TCP estructurada en un header que contiene los puertos de origen y destino, número de confirmación, etc. Esta sería la información del control de un paquete TCP.
    - **HTTP**: Este paquete se utiliza para realizar un intercambio de datos/información entre un cliente que hace una request (*Laptop Ruzpedia*) y un servidor (*Server Ruzpedia*) que emitirá dicha información. Este paquete debe contener la HTTP request realizada por el cliente a la ida y la HTTP response del servidor a la vuelta. Además de esto, contiene los datos del protocolo TCP junto con las IPs tanto de destino como de origen.
    - **STP**: Este protocolo es de segunda capa, y permite tener enlaces redundantes en dispositivos de interconexión, lo que quiere decir que se puede mantener funcionando la red aun cuando un enlace o swithc falla. Este protocolo se da cuando hay rutas alternativas para un mismo destino. En nuestro caso es importante que exista este paquete, ya que al servidor *ruzpedia* también se puede llegar desde la subred *DNS* o *Casa Alumno*, y si por ejemplo esta útima falla, el *laptop de ruzpedia* seguirá bien porque el paquete hace que la conexión no se interrumpa.
3. Envío de paquetes:
    - El primer paquete que se envía es el DNS, el cual comienza en el *Laptop Ruzpedia*, luego pasa por el *Access Point*, se dirige al *switch de Ruzpedia*, luego al *Router gateway Ruzpedia*, llega al *router central*, entra al *Router DNS*, pasa por el *Switch DNS* y llega finalmente al *servidor DNS* donde establece la conexión. Luego realiza el mismo camino anterior pero en sentido contrario hasta llegar al *Laptop Ruzpedia*.
    - El segundo paquete que se envía es el TCP, el cual comienza en el *Laptop Ruzpedia*, pasa por el *Access Point Ruzpedia*, llega al *Switch Ruzpedia* y desde aquí se dirige al *Server Ruzpedia*. Luego se devuelve por la misma ruta hasta el *Laptop Ruzpedia*.
    - El tercer paquete es el HTTP y sigue la misma ruta que el paquete anterior, partiendo en el *Laptop Ruzpedia*, luego llega al *Access Point Ruzpedia*, pasa al *Switch Ruzpedia* y desde aquí se dirige al *Server Ruzpedia*. Luego se devuelve por la misma ruta hasta el *Laptop Ruzpedia*. Cabe destacar que, al igual que como se vió en clases y en los videos, para una request HTTP se envía más de un paquete TCP, y es por esto que en la simulación se pueden ver varios que siguen la ruta detallada anteriormente.
    - El cuarto paquete es STP, y este tiene múltiples caminos. Este paquete comienza en el primer dispositivo en el cual se ven caminos alternativos para llegar al Servidor de Ruzpedia, es decir, en el *Switch Ruzpedia*. De acá se divide hacia el *Access Point Ruzpedia* (donde luego pasa al Laptop), otro al *Server Ruzpedia* y un tercero a *Router Gateway Ruzpedia*. Al mismo tiempo, se generan protocolos STP en los otros 2 switch de la red completa. En el *Switch Casa Alumno* el paquete se envía al *Router Gateway Casa Alumno* y al *Router WRT300N Casa Alumno*, y de este último pasa tanto al Laptop como al PC. Por otra parte, del *Switch DNS* pasa tanto al *Server DNS* y al *Router DNS*. Esto ocurre todo el rato mientras la conexión persista.

## Referencias y material adicional
- https://computernetworking747640215.wordpress.com/2018/07/05/dns-server-configuration-in-packet-tracer/
- https://www.itesa.edu.mx/netacad/introduccion/course/files/7.2.3.5%20Lab%20-%20Using%20Wireshark%20to%20Examine%20a%20UDP%20DNS%20Capture.pdf
- https://developer.mozilla.org/es/docs/Web/HTTP/Overview
- https://ccnadesdecero.com/curso/stp/
