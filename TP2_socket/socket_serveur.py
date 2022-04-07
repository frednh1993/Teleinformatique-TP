# Importation de la librairy pour les sockets
import socket
import os


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

     header = 12
     nbrDgm = 1
     oct_init = 0

      # Sélectionner le fichier à transmettre + obtenir sa taille :
     nom_fichier = "Mario.png"
     fichierSize = os.path.getsize(nom_fichier)
     totDgm = (fichierSize/1000)
     print(fichierSize)
     
     # Ouverture du fichier pour lecture et transmission les datagrammes :
     fichier = open(nom_fichier, 'rb')
     fichiertotal = fichier.read()


     while nbrDgm < totDgm:
      datagramme = fichier[oct_init:(nbrDgm*1000)]
      datagramme = f'{{ND}}{nbrDgm}{{TD}}{totDgm}:<20' + datagramme


      oct_init = (nbrDgm*1000)+1
      nbrDgm = nbrDgm + 1






      sock_Serveur.send(str.encode(datagramme, encoding="utf-8"))

      




      fichier.close()

     sock_Serveur.shutdown(socket.SHUT_RDWR) 
     sock_Serveur.close()
     break

          

      

    

     
     