#!/usr/bin/python
# -*- coding:Utf-8 -*- 

# Import pour Gestion d'images
import Image
import ImageDraw

# Fonction de chargement du fichier de configuration
def loadConfig():
	fileCfg = open('couleurs.cfg', 'r')
	global cfg
	cfg = {} # On cree un dictionnaire vide
	for line in fileCfg:
		cle, x = line.split('\t', 1) # On isole la cle
		x = x.rstrip() # On enleve les caracteres d espacement superflus a la fin
		val = x.split('\t')[:3] # On separe les valeurs on ne garde que les 3 premieres
		for i in range(len(val)): val[i]=int(val[i])
		#print cle, val
		cfg[cle] = val #On ajoute la ligne au dico
	fileCfg.close()
	# Affichage du 3eme element de la valeur correspondant a la clé 'A'
	#print cfg['A'][2]

# Fonction de traduction du texte en code couleur
def traductColor(text,squareSize,squareNumPerLine,squareSpace,imgName):
	# image width = borders (squareSpace) + nb squares (size and space included)
	imageWidth = squareSpace + ((int(squareSize)+squareSpace)*squareNumPerLine)
	print imageWidth 
	imageHeight = 300
	squareX = squareY = squareSpace
	im = Image.new("RGB", (imageWidth, imageHeight), 'white')
	draw = ImageDraw.Draw(im)

	# Create Squares	
	for i in range(len(text)):
		draw.rectangle([(squareX,squareY), (squareX+squareSize,squareSize+squareY)], tuple(cfg[text.upper()[i]]))
		squareX += squareSize+squareSpace
	
	im.save(imgName, "PNG")
		
def menu():								 
	print"----------------Menu principal-------------------------------"
	squareSize=raw_input("> Entrez la taille des carres: ", )
	squareNumPerLine=raw_input("> Entrez le nombre de carres par ligne: ", )
	squareSpace=raw_input("> Entrez l'espacement entre les carres: ", )
	imgName=raw_input("> Entrez le nom de l'image a generer (.png): ",)	
	text=raw_input("> Entrez le texte a traduire:\n", )
	traductColor(text,float(squareSize),int(squareNumPerLine),int(squareSpace),imgName)

#ici début du programme
loadConfig()
menu()
