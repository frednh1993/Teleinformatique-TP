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
         print(f"Message synchronisation : {msg_syn} de {address} \n")
         sock_Serveur.connect(("127.0.0.1", 5653))

         msg_ack = "Hello Client"
         sock_Serveur.send(str.encode(msg_ack, encoding="utf-8"))
         print("2e message de synchronisation envoyé au client \n")

      if msg_syn == "Connexion":
         print("Connexion établie entre client-serveur")
         break





print("On peut envoyer le datagramme au client ! \n")

nbrDgm = 1
oct_init = 0
fin = b'-END-'

# Sélectionner le fichier à transmettre + obtenir sa taille :
nom_fichier = "Mario.png"

fichierSize = os.path.getsize(nom_fichier)
#print(fichierSize)

# Nombre total de datagrammes à transmettre
totDgm = round((fichierSize/1000),0)
totDgm = int(totDgm)

# Dédinition de l'entête d'encapsulation en utf-8 des datagrammes :
#header = b'{{ND}}{nbrDgm}{{TD}}{totDgm}'
#print(type(header))
   
# Ouverture en lecture de la totalité du fichier :
fichier = open(nom_fichier, 'rb')
fichierTot = fichier.read()


# Boucle qui envoit un datagramme tant que tout le fichier n'est pas transmis en totalité (toutes les tranches de 1000 oct de données) :
while nbrDgm <= totDgm:
   datagramme = fichierTot[oct_init:(nbrDgm*1000)]

   header = f'{{S.HEADER}}{{TD}}{nbrDgm}{{TD}}{totDgm}{{E.HEADER}}'
   header = header = bytes(header, "utf-8")
    
   #datagramme = header + datagramme
   datagramme = b''.join([header, datagramme])
   #print(type(datagramme))

   # Incrémentation de l'oct_init et du nombre de datagramme (prochain datagramme à transmettre) :
   oct_init = (nbrDgm*1000)+1
   nbrDgm = (nbrDgm + 1)

   # Transmission du datagramme :
   sock_Serveur.send(datagramme)

   if nbrDgm == totDgm:
      sock_Serveur.send(fin)
      print("Fin de transmission")




# Fermeture du fichier et du socket serveur :
fichier.close()
sock_Serveur.shutdown(socket.SHUT_RDWR) 
sock_Serveur.close()


          

      

    

     
     