# Importation des librairies pour les sockets, les fichiers et le random (aléatoire)
import socket
import os
import random
import math

# Attribution du mode UDP, de l'adresse IP et du numéro de port du socket Serveur :
sock_Serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock_Serveur.bind(("127.0.0.1", 22222))
#sock_Serveur.listen(5)



# Réception du message de synchronisation du Client, connexion du Serveur au Client, envoit de message d'acquittement du Serveur et confirmation de connexion :
while True:
   msg_syn, address = sock_Serveur.recvfrom(4096)

   if msg_syn:
      msg_syn = msg_syn.decode(encoding='utf-8')

      if msg_syn == "Hello Serveur":
         print(f"Serveur : Message de synchronisation {msg_syn} reçu du Client {address}. \n")
         sock_Serveur.connect(("127.0.0.1", 5653))

         msg_ack = "Hello Client"
         sock_Serveur.send(str.encode(msg_ack, encoding="utf-8"))
         print("Serveur : Message d'acquittement envoyé au Client. \n")

      if msg_syn == "Connexion":
         print("Serveur : Connexion établie entre Client et Serveur. ")
         print("Serveur : On peut commencer le transfert du fichier. \n")
         break



# nbrDgm : Nombre de datagramme envoyé, 
# oct_init : Représente le début du curseur pour la transmission des datagrammes (ex : Datagramme1 oct_init=0; Datagramme2 oct_init=1001; ...),
# fin : Code de fin de transmission une fois tout le fichier transmis au client.
nbrDgm = 1
oct_init = 0
fin = b'-END-'

# Sélectionner le fichier à transmettre et obtenir sa taille :
nom_fichier = "Mario.png"
fichierSize = os.path.getsize(nom_fichier)
#print(fichierSize)

# Nombre total de datagrammes à transmettre
totDgm = int(math.ceil((fichierSize/1000)))
   
# Ouverture en lecture binaire de la totalité du fichier à transmettre :
fichier = open(nom_fichier, 'rb')
fichierTot = fichier.read()

# Envoit au Client du nom du fichier que l'on transmet : 
sock_Serveur.send(str.encode(nom_fichier, encoding="utf-8"))

# Boucle qui envoit un datagramme tant que tout le fichier n'est pas transmis en totalité (par tranche de 1000 oct. max de données) : (+1 ligne 60)
while nbrDgm <= totDgm:  

   datagramme = fichierTot[oct_init:(nbrDgm*1000)]

   header = f'{{S.HEADER}}{{ND}}{nbrDgm}{{TD}}{totDgm}{{E.HEADER}}'
   header = header.encode()

   # datagramme envoyé = header + datagramme
   datagramme = b''.join([header, datagramme])
   #print(type(datagramme))

   # Afin de 
   fiabilite_reseau = random.randint(0,100)

   if fiabilite_reseau != 20 and fiabilite_reseau != 40 and fiabilite_reseau != 60 and fiabilite_reseau != 80 and fiabilite_reseau != 100:
      # Transmission du datagramme :
      sock_Serveur.send(datagramme)
   else:
      sock_Serveur.send(b"")
           
   # Le client envoit une confirmation (confirmation_dgm) de chaque datagramme reçu :
   confirmation_dgm, address = sock_Serveur.recvfrom(4096)

   # Condition : Si le nombre de datagramme envoyé = totalité du fichier à transmettre = message de fin (+1 ligne 84)
   if nbrDgm == totDgm:
      sock_Serveur.send(fin)
      print("Fin de transmission")

   # Si le Serveur reçoit confirmation_dgm, il va le caster de bytes en int (confirmation_dgm = numéro datagramme reçu par le Client) :
   if confirmation_dgm:
      confirmation_dgm = int(confirmation_dgm)

   # Si on a la confirmation Client de la réception du datagramme, il va y avoir incrémentation de l'oct_init et du nombre de datagramme 
   # (prochain datagramme à transmettre) :
   if confirmation_dgm == nbrDgm:
      oct_init = (nbrDgm*1000)+1
      nbrDgm = (nbrDgm + 1)
   else:
      # S'il n'y a pas de réception du client, on démarre le timer de 3 sec et on regarde encore si nous avons reçu une confirmation :
      sock_Serveur.settimeout(3)
      if confirmation_dgm == nbrDgm:
         oct_init = (nbrDgm*1000)+1
         nbrDgm = (nbrDgm + 1)
# Si aucune confirmation Client, même suite au timer de 3 sec, la boucle va recommancer sans incrémenter vers le prochain datagramme (va donc
# renvoyer le même datagramme) 



# Fermeture du fichier et du socket serveur :
fichier.close()
sock_Serveur.shutdown(socket.SHUT_RDWR) 
sock_Serveur.close()


          

      

    

     
     