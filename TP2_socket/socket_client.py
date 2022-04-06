# Importation de la librairy pour les sockets
import socket

# Attribution du mode datagrame, de l'adresse IP et du numéro de port au socket :
sock_Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_Client.bind(("127.0.0.1", 5653))

# Le client se connect au port du serveur et envoit un premier message de synchronisation :
try:
    sock_Client.connect(("127.0.0.1", 22222))
    msg_syn = "Hello Serveur"
    sock_Client.send(str.encode(msg_syn, encoding="utf-8"))
    print("1er message de synchronisation envoyé au serveur")
except:
    print("Erreur pas de connexion au serveur possible")
    exit()


while True:
     msg_ack, address = sock_Client.recvfrom(4096)

     if msg_ack:
       msg_ack = msg_ack.decode(encoding='utf-8') 

       if msg_ack == "Hello Client":
          print(f"Message synchronisation 2 : {msg_ack} de {address}")

          msg_syn = "Connexion"
          sock_Client.send(str.encode(msg_syn, encoding="utf-8"))
          break


sock_Client.shutdown(socket.SHUT_RDWR) 
sock_Client.close()









