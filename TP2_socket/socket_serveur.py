# Importation de la librairy pour les sockets
import socket
import os

# Attribution du mode datagrame, de l'adresse IP et du numéro de port au socket :
sock_Serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock_Serveur.bind(("127.0.0.1", 22222))

#sock_Serveur.listen(5)




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
nom_fichier = "Lorem.txt"

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

sock_Serveur.send(str.encode(nom_fichier, encoding="utf-8"))
# Boucle qui envoit un datagramme tant que tout le fichier n'est pas transmis en totalité (toutes les tranches de 1000 oct de données) :
while nbrDgm <= totDgm+1:

   datagramme = fichierTot[oct_init:(nbrDgm*1000)]

   header = f'{{S.HEADER}}{{ND}}{nbrDgm}{{TD}}{totDgm}{{E.HEADER}}'
   header = header.encode()

   
   #datagramme = header + datagramme
   datagramme = b''.join([header, datagramme])
   #print(type(datagramme))

     
   #oct_init = (nbrDgm*1000)+1
   #nbrDgm = (nbrDgm + 1)


   # Transmission du datagramme :
   sock_Serveur.send(datagramme)

   msg, address = sock_Serveur.recvfrom(4096)

   if nbrDgm == totDgm+1:
      sock_Serveur.send(fin)
      print("Fin de transmission")

   #msg_syn, address = sock_Serveur.recvfrom(4096)

   if msg:
      msg = int(msg)


   if msg == nbrDgm:
      # Incrémentation de l'oct_init et du nombre de datagramme (prochain datagramme à transmettre) :
      oct_init = (nbrDgm*1000)+1
      nbrDgm = (nbrDgm + 1)
   else:
      sock_Serveur.settimeout(3)
      if msg == nbrDgm:
         oct_init = (nbrDgm*1000)+1
         nbrDgm = (nbrDgm + 1)
   
   


# Fermeture du fichier et du socket serveur :
fichier.close()
sock_Serveur.shutdown(socket.SHUT_RDWR) 
sock_Serveur.close()


          

      

    

     
     