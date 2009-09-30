#!/usr/bin/python
# -*- coding:Utf-8 -*-

# Import pour la GUI 
import wx
# Import pour Gestion d'images
import Image
import ImageDraw
# Gestion des fichiers et repertoires
import os

#-------------------------------------------------------------------------------
# Fonction de chargement du fichier de configuration
#-------------------------------------------------------------------------------
def loadConfig(filename):
    fileCfg = open(filename, 'r')
    global cfg
    cfg = {}
    for line in fileCfg:
        cle, x = line.split('\t', 1)
        x = x.rstrip()
        val = x.split('\t')[:3]
        for i in range(len(val)):
            val[i]=int(val[i])
        cfg[cle] = val
    fileCfg.close()

#-------------------------------------------------------------------------------
# Fonction de traduction du texte en code couleur
#-------------------------------------------------------------------------------
def traducColor(text,squareSize,squareNumPerLine,squareSpace,imgName):
    # image width = borders (squareSpace) + nb squares (size and space included)
    imageWidth = squareSpace + ((int(squareSize)+squareSpace)*squareNumPerLine)
    imageHeight = squareSpace + (len(text) / squareNumPerLine) \
	                * (squareSize + squareSpace)
    if (len(text) % squareNumPerLine) > 0:
        imageHeight += squareSize + squareSpace
    squareX = squareY = squareSpace
    im = Image.new("RGB", (imageWidth, imageHeight), 'white')
    draw = ImageDraw.Draw(im)

    # Create Squares
    for i in range(len(text)):
        draw.rectangle([(squareX,squareY),  
          (squareX+squareSize,squareSize+squareY)], tuple(cfg[text.upper()[i]]))
        squareX += squareSize+squareSpace
        if squareX >= imageWidth:
            squareY += squareSize+squareSpace
            squareX = squareSpace

    im.save(imgName, "PNG")

#-------------------------------------------------------------------------------
# Main Frame including all graphics
#-------------------------------------------------------------------------------
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

        self.Bind(wx.EVT_MENU, self.OnLoad, id=1)
        self.Bind(wx.EVT_MENU, self.OnSave, id=2)
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
        hbox1.Add(self.textSize, 0,
                    wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(self.textNb, 0,
                    wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
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
    #    traducColor(self.text.GetValue(),
    #           self.spinSize.GetValue(),self.spinNb.GetValue(),2,'toto.png')

    def saveImg(self, event):
        dlg = wx.FileDialog(self, "Sauvegardez l'image", defaultDir=".",
        wildcard="Images PNG (*.png)|*.png",
                    style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            traducColor(self.text.GetValue(),
                self.spinSize.GetValue(),self.spinNb.GetValue(),2,dlg.GetPath())
        dlg.Destroy()

    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Selectionnez un fichier", defaultDir=".",
        wildcard="Fichiers Texte (*.txt)|*.txt",
                    style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            self.text.SetValue(filehandle.read())
            filehandle.close()
        dlg.Destroy()

    def OnSave(self, event):
        dlg = wx.FileDialog(self, "Sauvegardez le texte", defaultDir=".",
        wildcard="Fichiers Texte (*.txt)|*.txt",
                    style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(self.text.GetValue())
            filehandle.close()
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close()

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
loadConfig('couleurs.cfg')
app = wx.App()
myFrame(None, -1, 'Colographie')
app.MainLoop()

