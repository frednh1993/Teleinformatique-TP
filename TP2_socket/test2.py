import os

nom_fichier = "Mario.png"
fichierSize = os.path.getsize(nom_fichier)
print(fichierSize)


fichier = open(nom_fichier, 'rb')

temp = fichier.read(100)
print(temp)

nbrDgm = 50
totDgm = 250

temp2 = temp[0:10]
datagramme = f'{{ND}}{nbrDgm}{{TD}}{totDgm}'

print(type(datagramme))

bytes(datagramme, "utf-8")



print(datagramme)

fichier.close()

