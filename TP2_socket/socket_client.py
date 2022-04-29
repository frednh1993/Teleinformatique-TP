# Explication : Ceci est le socket Client qui va effectuer une connexion avec un socket Serveur et qui va recevoir une copie d'un fichier quelconque (réception d'information).

# Importation des librairies.
import socket
import os
import re
# Attribution du mode UDP, de l'adresse IP et du numéro de port du socket Client.
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

# Le Client va écouter le message d'acquittement du Serveur (msg_ack). 
while True:
    msg_ack, address = sock_Client.recvfrom(1100)

    if msg_ack:
        msg_ack = msg_ack.decode(encoding='utf-8') 

        # Si le Client reçoit le bon message d'acquittement, il va envoyer le message final (via msg_con) qui confirme la connexion.
        if msg_ack == "Hello Client":
            print(f"Client : Message d'acquittement {msg_ack} reçu du Serveur {address}. \n")

            msg_con = "Connexion"
            sock_Client.send(str.encode(msg_con, encoding="utf-8"))
            print("Client : Message de confirmation de connexion envoyé au Serveur. \n")
            break



# info_fichier_Serveur := nom du fichier copié + sa taille.
info_fichier_Serveur, address = sock_Client.recvfrom(1100)
info_fichier_Serveur = info_fichier_Serveur.decode(encoding='utf-8')
# Permet de séparer l'information.
info_fichier_Serveur = info_fichier_Serveur.split(' ')
nom_fichier_Serveur = info_fichier_Serveur[0]
taille_fichier_Serveur = info_fichier_Serveur[1]

# Ouverture d'un fichier pour recevoir les données.
fichier = open(f"Copie_{nom_fichier_Serveur}", "wb")
# checksum := contient tous les datagrammes reçus et leur ordre.
checksum = ""
 

# Boucle de réception et d'écriture des données du fichier à copier.
while True:

    # data = Header + datagramme de données.
    # 1100 oct. de réception pour avoir une sécurité avec l'entête qui est attachée aux données.
    data, address = sock_Client.recvfrom(1100)

    # Fin de la transcription du fichier de copie.
    if data == b'-END-':
        # Fermeture du socket Client et du fichier en cours.
        sock_Client.shutdown(socket.SHUT_RDWR) 
        sock_Client.close() 
        fichier.close()    
        break

    # Sécurité : data doit avoir un contenu pour entrer ici.
    if data is not None:
        # substring := va contenir l'entête du datagramme. 
        start = data.find(b'{S.HEADER}') 
        end = data.find(b'{E.HEADER}') + len(b'{E.HEADER}')
        substring = data[start:end]

        # data conserve uniquement les données.
        data = data.replace(substring, b'')

        substring = substring.decode()
        début = substring.find(f"{{ND}}") + len(f"{{ND}}")
        fin = substring.find(f"{{TD}}") 
        substring = substring[début:fin]

        # Client envoit le numéro du datagramme lu au Serveur comme confirmation.
        sock_Client.send(substring.encode())

        checksum += substring + ";"

        # Écriture de chaque segement de données reçus (datagramme de données) dans fichier.
        fichier.write(data)



taille_fichier_Serveur = int(taille_fichier_Serveur)
taille_fichier_Client = os.path.getsize(f"Copie_{nom_fichier_Serveur}")

# Si la taille du fichier copié == taille du fichier original = bonne transmission de données.
if taille_fichier_Serveur == taille_fichier_Client:
    print(f"Client : Le fichier {nom_fichier_Serveur} a été copié sans erreur et se nomme Copie_{nom_fichier_Serveur}.")
else:
    print(f"Client : Le fichier {nom_fichier_Serveur} présente des erreurs de copie.")



# Information de validation (moi) :

#print('Taille du fichier copié : ', end='')
#print(os.path.getsize(f"Copie_{nom_fichier_Serveur}"))

#print('Datagrammes reçus : ', end='')
#print(checksum)






    










