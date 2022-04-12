# Importation des librairies pour les sockets, les options de fichier et pour la fonction split (via re)
import socket
import os
import re

# Attribution du mode UDP, de l'adresse IP et du numéro de port du socket Client :
sock_Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_Client.bind(("127.0.0.1", 5653))



# Le Client se connect au port du Serveur et envoit un premier message de synchronisation (msg_syn).
try:
    sock_Client.connect(("127.0.0.1", 22222))
    msg_syn = "Hello Serveur"
    sock_Client.send(str.encode(msg_syn, encoding="utf-8"))
    print("Client : Message de synchronisation envoyé au Serveur. \n")
except:
    print("Erreur : Pas de connexion au Serveur possible ! \n")
    exit()



# Le Client va écouter le message d'acquittement du Serveur (msg_ack) : 
while True:
    msg_ack, address = sock_Client.recvfrom(1100)

    if msg_ack:
        msg_ack = msg_ack.decode(encoding='utf-8') 

        # Si le Client reçoit le bon message d'acquittement, il va envoyer le message final (via msg_con) qui confirme la connexion (Three-way handshake) : 
        if msg_ack == "Hello Client":
            print(f"Client : Message d'acquittement {msg_ack} reçu du Serveur {address}. \n")

            msg_con = "Connexion"
            sock_Client.send(str.encode(msg_con, encoding="utf-8"))
            print("Client : Message de confirmation de connexion envoyé au Serveur. \n")
            break



# 1100 oct. de réception pour avoir une sécurité avec l'entête qui est attachée aux données.
info_fichier_Serveur, address = sock_Client.recvfrom(1100)
info_fichier_Serveur = info_fichier_Serveur.decode(encoding='utf-8')
#
info_fichier_Serveur = info_fichier_Serveur.split(' ')
nom_fichier_Serveur = info_fichier_Serveur[0]
taille_fichier_Serveur = info_fichier_Serveur[1]

#print(nom_fichier_Serveur)
#print(taille_fichier_Serveur)

# Ouverture du fichier de copie en écriture binaire.
fichier = open(f"Copie_{nom_fichier_Serveur}", "wb")
# checksum : variable qui donne l'ordre des datagrammes pour la vérification de similarité du fichier transmis.
checksum = ""
 
while True:

    # Réception, dans la variable data, de chaque datagramme transmis par le Serveur (data = Header + datagramme de données)
    data, address = sock_Client.recvfrom(1100)

    # Suite à la réception du dernier datagramme de données, le Serveur envoit le segment -END- au client pour mettre fin à la transcription du fichier de copie.
    if data == b'-END-':
        # Fermeture du socket Client et du fichier en cours.
        sock_Client.shutdown(socket.SHUT_RDWR) 
        sock_Client.close() 
        fichier.close()    
        break

    # Si data est null, il n'y aura pas de Header.
    if data is not None:
        # Variable substring qui va contenir l'entête du datagramme. 
        start = data.find(b'{S.HEADER}') 
        end = data.find(b'{E.HEADER}') + len(b'{E.HEADER}')
        substring = data[start:end]

        # Retrait de l'entête des données de data.
        data = data.replace(substring, b'')

        # Stockage de lentête dans la variable (str) substring. 
        substring = substring.decode()
        
        # Pour la vérification de transmission de chaque datagramme, on stocke seulement le numéro de chaque datagramme reçu dans la variable checksum.
        début = substring.find(f"{{ND}}") + len(f"{{ND}}")
        fin = substring.find(f"{{TD}}") 
        substring = substring[début:fin]

        # Client envoit le numéro du datagramme lu au Serveur comme confirmation.
        sock_Client.send(substring.encode())

        checksum += substring + ";"

        # Écriture de chaque segement de données reçus (datagramme de données) dans la variable fichier.
        fichier.write(data)
    

# Taille du fichier copier.
#print(os.path.getsize(f"Copie_{nom_fichier_Serveur}"))
# Pour voir l'ordre des datagrammes reçus.
#print(checksum)

# Si la taille du fichier copier = taille du fichier Serveur = bonne transmission de données.
# Petite ERREUR : nous avons toujour une taille de fichier copiée légèrement inférieur au fichier Serveur !?
if taille_fichier_Serveur == os.path.getsize(f"Copie_{nom_fichier_Serveur}"):
    print(f"Client : Le fichier {nom_fichier_Serveur} a été copié côté Client sans Erreur.")

print(f"Client : Le fichier {nom_fichier_Serveur} a été copié côté Client.")








    










