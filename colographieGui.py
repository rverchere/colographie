#!/usr/bin/python
# simple.py
 
import wx
 
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
        
        textSize = wx.StaticText(panel, -1, 'Taille: ')
        spinSize = wx.SpinCtrl(panel, -1, '30', min=1)
        textNb = wx.StaticText(panel, -1, 'Nombre: ')
        spinNb = wx.SpinCtrl(panel, -1, '15', min=1)
        hbox1.Add(textSize, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(textNb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hbox1.Add(spinSize, 1, wx.EXPAND)
        hbox1.Add(spinNb, 1, wx.EXPAND)
        vbox.Add(hbox1, 0, wx.EXPAND)
 
        text = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)
 
        hbox2.Add(text, 1, wx.EXPAND)
 
        vbox.Add(hbox2, 1, wx.EXPAND)
 
        btnShow = wx.Button(panel, -1, 'Afficher')
        btnSave = wx.Button(panel, -1, 'Sauvegarder')
        hbox3.Add(btnShow, 1, wx.EXPAND)
        hbox3.Add(btnSave, 1, wx.EXPAND)
        vbox.Add(hbox3, 0, wx.EXPAND)
 
        panel.SetSizer(vbox)
 
        self.Centre()
        self.Show(True)
    #__init__:end        
 
    def OnQuit(self, event):
        self.Close()
    
app = wx.App()
myFrame(None, -1, 'myApplication')
app.MainLoop()

