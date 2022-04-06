import os

nom_fichier = "Mario.png"
fichierSize = os.path.getsize(nom_fichier)
print(fichierSize)

lngDatagramme = 100


fichiertxt = open(nom_fichier, 'rb')
temp = fichiertxt.read(1024)

print(temp)
fichiertxt.close()

