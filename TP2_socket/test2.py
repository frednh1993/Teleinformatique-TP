
import os

print("On peut envoyer le datagramme au client ! \n")

nbrDgm = 1
oct_init = 0
fin = bytes('{{END}}', "utf-8")

# Sélectionner le fichier à transmettre + obtenir sa taille :
nom_fichier = "Mario.png"

fichierSize = os.path.getsize(nom_fichier)
#print(fichierSize)

# Nombre total de datagrammes à transmettre
totDgm = round((fichierSize/1000),0)
totDgm = int(totDgm)

# Dédinition de l'entête d'encapsulation en utf-8 des datagrammes :
#header = f'{{ND}}{nbrDgm}{{TD}}{totDgm}'
#print(type(header))
#header = bytes(header, "utf-8")
    
# Ouverture en lecture de la totalité du fichier :
fichier = open(nom_fichier, 'rb')
fichierTot = fichier.read()




for i in range(0,3):
      datagramme = fichierTot[oct_init:(nbrDgm*1000)]

      header = f'{{ND}}{nbrDgm}{{TD}}{totDgm}'
      header = bytes(header, "utf-8")
      
      #datagramme = bytes(datagramme, "utf-8") 
      #datagramme = header + datagramme
      datagramme = b''.join([header, datagramme])
      print(type(datagramme))

      # Incrémentation de l'oct_init et du nombre de datagramme (prochain datagramme à transmettre) :
      oct_init = (nbrDgm*1000)+1
      nbrDgm = (nbrDgm + 1)

      # Transmission du datagramme :
      print(f'{datagramme} \n')

      if i == 2:
         print("fin")


data = b'salut'
print(data[1:3])
      