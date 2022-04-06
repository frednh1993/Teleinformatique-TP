# Importation de la librairy pour les sockets
import socket

# Attribution du mode datagrame, de l'adresse IP et du numéro de port au socket :
sock_Serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock_Serveur.bind(("127.0.0.1", 22222))

# Réception du message de synchronisation et des coordonnées du client :
while True:
     msg_syn, address = sock_Serveur.recvfrom(4096)

     if msg_syn:
        msg_syn = msg_syn.decode(encoding='utf-8')

        if msg_syn == "Hello Serveur":
           print(f"Message synchronisation : {msg_syn} de {address}")
           sock_Serveur.connect(("127.0.0.1", 5653))

           msg_ack = "Hello Client"
           sock_Serveur.send(str.encode(msg_ack, encoding="utf-8"))
           print("2e message de synchronisation envoyé au client")

        if msg_syn == "Connexion":
           print("Connexion établie entre client-serveur")
           break


while True:
     print("On peut envoyer le datagramme au client !")

     # Ouverture du fichier txt pour lecture :
     
     nom_fichier_txt = "Bla.txt"
     
     fichiertxt = open(nom_fichier_txt, 'r')
     
     fichiertxt.read()

     fichiertxt.close()






     sock_Serveur.shutdown(socket.SHUT_RDWR) 
     sock_Serveur.close()
     break

          

      

    

     
     