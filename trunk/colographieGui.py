#!/usr/bin/python
# -*- coding:Utf-8 -*-

# Import pour la GUI 
import wx
# Import pour Gestion d'images
import Image
import ImageDraw

# Fonction de chargement du fichier de configuration
def loadConfig(filename):
	fileCfg = open(filename, 'r')
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


# Fonction de traduction du texte en code couleur
def traductColor(text,squareSize,squareNumPerLine,squareSpace,imgName):
	# image width = borders (squareSpace) + nb squares (size and space included)
	imageWidth = squareSpace + ((int(squareSize)+squareSpace)*squareNumPerLine)
	imageHeight = 300
	squareX = squareY = squareSpace
	im = Image.new("RGB", (imageWidth, imageHeight), 'white')
	draw = ImageDraw.Draw(im)

	# Create Squares
	for i in range(len(text)):
		draw.rectangle([(squareX,squareY), (squareX+squareSize,squareSize+squareY)], tuple(cfg[text.upper()[i]]))
		squareX += squareSize+squareSpace
		if squareX >= imageWidth:
			squareY += squareSize+squareSpace
			squareX = squareSpace

	im.save(imgName, "PNG")


		
# Main Frame including all graphics
class myFrame(wx.Frame):

    #__init__:begin
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
 
        #menubar:begin
        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(1, '&Load File', 'Load File')
        file.Append(2, '&Save File', 'Save File')
        file.Append(99, '&Quit', 'Quit application')
        menubar.Append(file, '&File')
 
        self.Bind(wx.EVT_MENU, self.OnQuit, id=99)
 
        help = wx.Menu()
        help.Append(-1, 'About', 'About')
        menubar.Append(help, '&Help')
    
        self.SetMenuBar(menubar)
        #menubar:end
 
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.GridSizer(2, 2) # taille / nombre
        hbox2 = wx.BoxSizer(wx.HORIZONTAL) # texte
        hbox3 = wx.BoxSizer(wx.HORIZONTAL) # afficher / sauvegarder
        
        self.textSize = wx.StaticText(panel, -1, 'Taille: ')
        self.spinSize = wx.SpinCtrl(panel, -1, '30', min=1)
        self.textNb = wx.StaticText(panel, -1, 'Nombre: ')
        self.spinNb = wx.SpinCtrl(panel, -1, '15', min=1)
        hbox1.Add(self.textSize, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(self.textNb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(self.spinSize, 1, wx.EXPAND)
        hbox1.Add(self.spinNb, 1, wx.EXPAND)
        vbox.Add(hbox1, 0, wx.EXPAND)
 
        self.text = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)

        hbox2.Add(self.text, 1, wx.EXPAND)
 
        vbox.Add(hbox2, 1, wx.EXPAND)

        btnShow = wx.Button(panel, -1, 'Afficher')
        btnSave = wx.Button(panel, -1, 'Sauvegarder')
		
        hbox3.Add(btnShow, 1, wx.EXPAND)
        hbox3.Add(btnSave, 1, wx.EXPAND)
        vbox.Add(hbox3, 0, wx.EXPAND)
 
        panel.SetSizer(vbox)

        #self.Bind(wx.EVT_BUTTON, self.printTxt, btnShow)
        self.Bind(wx.EVT_BUTTON, self.saveImg, btnSave)

        self.Centre()
        self.Show(True)
    #__init__:end        

    #def printTxt(self, event):
    #    traductColor(self.text.GetValue(),self.spinSize.GetValue(),self.spinNb.GetValue(),2,'toto.png')

    def saveImg(self, event):
        dlg = wx.FileDialog(self, message=u"Sauvegarde", defaultDir=".",
        wildcard="Fichiers PNG (*.png)|*.png", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            traductColor(self.text.GetValue(),self.spinSize.GetValue(),self.spinNb.GetValue(),2,dlg.GetPath())
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close()
    

# ici début du programme
loadConfig('couleurs.cfg')
app = wx.App()
myFrame(None, -1, 'myApplication')
app.MainLoop()

