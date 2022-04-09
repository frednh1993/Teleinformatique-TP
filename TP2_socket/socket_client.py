# Importation de la librairy pour les sockets
import socket
import os
#from turtle import clear
longueurEntete = 10

# Attribution du mode datagrame, de l'adresse IP et du numéro de port au socket :
sock_Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_Client.bind(("127.0.0.1", 5653))




# Le client se connect au port du serveur et envoit un premier message de synchronisation :
try:
    sock_Client.connect(("127.0.0.1", 22222))
    msg_syn = "Hello Serveur"
    sock_Client.send(str.encode(msg_syn, encoding="utf-8"))
    print("1er message de synchronisation envoyé au serveur \n")
except:
    print("Erreur pas de connexion au serveur possible \n")
    exit()




while True:
    msg_ack, address = sock_Client.recvfrom(4096)

    if msg_ack:
        msg_ack = msg_ack.decode(encoding='utf-8') 

        if msg_ack == "Hello Client":
            print(f"Message synchronisation 2 : {msg_ack} de {address} \n")

            msg_syn = "Connexion"
            sock_Client.send(str.encode(msg_syn, encoding="utf-8"))
            break




fichier = open("Copie_fichier", "wb")
HeaderNumbers = []
checksum = ""
 
while True:

    # Réception dans la variable data de chaque d'atagramme transmis par le serveur (data = Header + datagramme)
    data, address = sock_Client.recvfrom(1036)

    # Suite à la réception du dernier datagramme de données, le serveur envoit le segment -END- au client qui va mettre fin à la transcription du fichier de copie
    if data == b'-END-':
        print("Encore la fin")
        # Fermeture du socket client et du fichier de copie
        sock_Client.shutdown(socket.SHUT_RDWR) 
        sock_Client.close() 
        fichier.close()    
        break

    # Variable substring qui va contenir l'entête du datagramme 
    start = data.find(b'{S.HEADER}') 
    end = data.find(b'{E.HEADER}') + len(b'{E.HEADER}')
    substring = data[start:end]

    # Retrait de l'entête de la variable data
    data = data.replace(substring, b'')

    # Stockage de lentête complète dans la variable (str) substring 
    substring = substring.decode()
        
    # Pour la vérification de transmission de chaque datagramme, on stocke seulement le numéro de chaque datagramme reçu dans la variable checksum
    début = substring.find(f"{{ND}}") + len(f"{{ND}}")
    fin = substring.find(f"{{TD}}") 
    substring = substring[début:fin]
    checksum += substring + ";"

    # Écriture de chaque segement de données des datagrammes reçus dans la variable fichier
    fichier.write(data)


print(checksum)
# if fichier:
#     os.remove("Copie_fichier")





    










