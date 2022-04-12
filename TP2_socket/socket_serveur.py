# INSTRUCTION : Entrez le nom du fichier à transmettre à la ligne 45 : nom_fichier = "". Votre fichier doit se trouver à l'intérieur du document TP2_socket

# Importation des librairies pour les sockets, les options de fichier, le random (aléatoire) ainsi que les fonctions mathématiques.
import socket
import os
import random
import math

# Attribution du mode UDP, de l'adresse IP et du numéro de port du socket Serveur.
sock_Serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock_Serveur.bind(("127.0.0.1", 22222))



# Réception du message de synchronisation du Client, connexion du Serveur au Client, envoit du message d'acquittement au Client et confirmation de connexion.
while True:
   msg_syn, address = sock_Serveur.recvfrom(1100)

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



# nbrDgm : Nombre de datagrammes envoyés, 
# oct_init : Représente le début du curseur pour la transmission des datagrammes (ex : Datagramme1 oct_init=0; Datagramme2 oct_init=1001; ...),
# fin : Code de fin de transmission du fichier envoyé au Client une fois tout le fichier transmis.
nbrDgm = 1
oct_init = 0
fin = b'-END-'

# Sélectionne le fichier à transmettre et obtient sa taille.
nom_fichier = "Mario.png"
fichierSize = os.path.getsize(nom_fichier)
#print(fichierSize)
# info_fichier renseigne le Client sur le nom du fichier transmis avec sa taille.
info_fichier = nom_fichier + f" {fichierSize}"

# totDgm : Nombre total de datagrammes à transmettre.
totDgm = int(math.ceil((fichierSize/1000)))
   
# Ouverture en lecture binaire de la totalité du fichier à transmettre.
fichier = open(nom_fichier, 'rb')
fichierTot = fichier.read()

# Envoit au Client du nom du fichier que l'on transmet.
sock_Serveur.send(str.encode(info_fichier, encoding="utf-8"))



# Boucle qui envoit un datagramme de données tant que tout le fichier n'est pas transmis (par tranche de 1000 oct. de données max).
while nbrDgm <= totDgm:  

   if nbrDgm != totDgm:
      datagramme = fichierTot[oct_init:(nbrDgm*1000)]
   else:
      datagramme = fichierTot[oct_init:fichierSize]

   header = f'{{S.HEADER}}{{ND}}{nbrDgm}{{TD}}{totDgm}{{E.HEADER}}'
   header = header.encode()

   # datagramme envoyé = header(entête indiquant le datagramme transmis par son numéro d'ordre ET le nombre total de datagrammes à transmettre) + datagramme 1000 oct. max de données.
   datagramme = b''.join([header, datagramme])

   # Afin de simuler des erreurs d'envoi de datagramme, on utilise la fonction random 0-100 et 5 valeurs qui font envoyer un message vide (donc aucun message).
   fiabilite_reseau = random.randint(0,100)

   if fiabilite_reseau != 20 and fiabilite_reseau != 40 and fiabilite_reseau != 60 and fiabilite_reseau != 80 and fiabilite_reseau != 100:
      # Transmission du datagramme.
      sock_Serveur.send(datagramme)
   else:
      sock_Serveur.send(b'')
           
   # Le client envoit une confirmation (confirmation_dgm) de chaque datagramme reçu.
   confirmation_dgm, address = sock_Serveur.recvfrom(1100)

   # Condition : Si le nombre de datagramme envoyé = totalité des datagrammes du fichier à transmettre, on envoit le message de fin de transmission.
   if nbrDgm == totDgm:
      sock_Serveur.send(fin)
      print("Serveur : Fin de transmission")

   # Si le Serveur reçoit confirmation_dgm, il va le caster en int.
   if confirmation_dgm:
      confirmation_dgm = int(confirmation_dgm)

   # Si on a la confirmation Client de la réception du datagramme, il va y avoir incrémentation de oct_init et nbrDgm afin de transmettre le prochain datagramme dans la file.
   if confirmation_dgm == nbrDgm:
      oct_init = (nbrDgm*1000)+1
      nbrDgm = (nbrDgm + 1)
   else:
      # S'il n'y a pas de confirmation du Client, le timer de 3 sec est amorcé et la confirmation client est vérifiée de nouveau.
      sock_Serveur.settimeout(3)
      if confirmation_dgm == nbrDgm:
         oct_init = (nbrDgm*1000)+1
         nbrDgm = (nbrDgm + 1)
# Si aucune confirmation Client n'est reçue (même suite au timer de 3 sec), la boucle va recommancer sans incrémenter vers le prochain datagramme (va donc renvoyer le même datagramme) 






# Fermeture du fichier et du socket Serveur :
fichier.close()
sock_Serveur.shutdown(socket.SHUT_RDWR) 
sock_Serveur.close()


          

      

    

     
     