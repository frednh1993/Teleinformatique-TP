# Explication : Ceci est le socket Serveur qui va effectuer une connexion avec un socket Client et qui va copier et transmettre un fichier quelconque au Client.
# INSTRUCTION : Entrez le nom du fichier à transmettre à la ligne 45 : nom_fichier = "". Votre fichier doit se trouver à l'intérieur du document TP2_socket.



# Importation des librairies.
import socket
import os
import random
import math
# Attribution du mode UDP, de l'adresse IP et du numéro de port du socket Serveur.
sock_Serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock_Serveur.bind(("127.0.0.1", 22222))



# Processus de connexion Three-Way Handshake.
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



# nbrDgm := nombre de datagrammes envoyés, 
# fin := code de fin de transmission du fichier.
nbrDgm = 1
fin = b'-END-'

# Sélectionne le fichier à transmettre et obtient sa taille. (Inscrire le nom de votre fichier à la ligne suivante)
nom_fichier = "Mario.png"
fichierSize = os.path.getsize(nom_fichier)

# info_fichier renseigne le Client sur le nom du fichier transmis + sa taille.
info_fichier = nom_fichier + f" {fichierSize}"
# totDgm := Nombre total de datagrammes à transmettre.
totDgm = int(math.ceil((fichierSize/1000)))
# Ouverture fichier à transmettre.
fichier = open(nom_fichier, 'rb')
# Envoit info_fichier au Client. 
sock_Serveur.send(str.encode(info_fichier, encoding="utf-8"))



# Boucle d'envoi des datagrammes.
while nbrDgm <= totDgm:  

   #if nbrDgm <= totDgm:
   datagramme = fichier.read(1000) 
              
   # header := entête d'un datagramme.           
   header = f'{{S.HEADER}}{{ND}}{nbrDgm}{{TD}}{totDgm}{{E.HEADER}}'
   header = header.encode()

   # datagramme envoyé = header( # datagramme & nombre total de datagrammes à transmettre) + données (1000 oct.).
   datagramme = b''.join([header, datagramme])

   # Simulation des erreurs d'envoi de datagramme avec la fonction random qui envoit un message vide 5% du temps.
   fiabilite_reseau = random.randint(0,100)
   if fiabilite_reseau != 20 and fiabilite_reseau != 40 and fiabilite_reseau != 60 and fiabilite_reseau != 80 and fiabilite_reseau != 100:
      # Transmission du datagramme.
      sock_Serveur.send(datagramme)
   else:
      sock_Serveur.send(b'')

   # confirmation_dgm := confirmation de datagramme reçu.
   confirmation_dgm, address = sock_Serveur.recvfrom(1100)

   # Message de fin de transmission.
   if nbrDgm == totDgm:
      sock_Serveur.send(fin)
      print("Serveur : Fin de transmission")
   # Si le Serveur reçoit confirmation_dgm, il va le caster en int (compatibilité).
   if confirmation_dgm:
      confirmation_dgm = int(confirmation_dgm)

   # Protocole d'envoi du même datagramme en cas de non réception de confirmation.
   while confirmation_dgm != nbrDgm:
      sock_Serveur.send(datagramme)
      confirmation_dgm, address = sock_Serveur.recvfrom(1100)
      sock_Serveur.settimeout(3)

      if confirmation_dgm:
         confirmation_dgm = int(confirmation_dgm)
   
   #print(f"{nbrDgm}")
   # Incrémentation des datagrammes.
   nbrDgm = (nbrDgm + 1)



# Fermeture du fichier et du socket Serveur.
fichier.close()
sock_Serveur.shutdown(socket.SHUT_RDWR) 
sock_Serveur.close()


          

      

    

     
     