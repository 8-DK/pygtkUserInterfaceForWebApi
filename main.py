#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import json
import urllib2

import os
from urlparse import urlparse
from os.path import splitext, basename

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass



class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

class mainGtkClass:
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("main.glade")	
		builder.connect_signals(Handler())

		self.window = builder.get_object("window")
		self.liststore_project = builder.get_object("liststore_project")
		self.treeview_project = builder.get_object("treeview_project")
		#user name elements 
		self.usernameLable = builder.get_object("usernameLable")

		#notebook elements
		self.notebook = builder.get_object("notebook")
		self.Tab1ViewPort = builder.get_object("Tab1ViewPort")
		self.Tab1ListBox = builder.get_object("Tab1ListBox")

		#self.Tab1View = builder.get_object("Tab1View")
		#self.Tab2View = builder.get_object("Tab2View")
		#self.Tab3View = builder.get_object("Tab3View")
		
		self.window.maximize()

		self.liststore_project.append(["Tiny Wifi Server",1000,1])
		self.liststore_project.append(["TIme Pass",0,0])
		self.liststore_project.append(["sfdads",56,0])

		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Project", renderer, text=0)
		self.treeview_project.append_column(column)

		column = Gtk.TreeViewColumn("Like", renderer, text=1)
		self.treeview_project.append_column(column)
	
		column = Gtk.TreeViewColumn("Status", renderer, text=2)
		self.treeview_project.append_column(column)
		
		url = "https://v2api.collaborizm.com/v2/users/21339"
		response = urllib2.urlopen(url)
		data = json.loads(response.read())

		self.setUserName(data)		
		self.window.show_all()

	def setUserName(self,jsonObj):
		value = jsonObj["first_name"]+" "
		value += jsonObj["last_name"]
		self.usernameLable.set_text(value)
		lbl = Gtk.Label(value)
		lbl.set_alignment(xalign=0, yalign=1) 
		self.Tab1ListBox.add(lbl)
		self.downlodImage(jsonObj["avatar"],"/tmp/")

	def downlodImage(self,imageUrl,path):
		userApi = "https://v2api.collaborizm.com/v2/users/21339/"
		fullUrl	= userApi + imageUrl
		disassembled = urlparse(imageUrl)
		imageName = basename(disassembled.path)
		path+=imageName
		print fullUrl
		print path
		try:
			f = open(path,'wb')
			f.write(urllib2.urlopen(fullUrl).read())
			f.close()
		except:
			print "cant download avatar"


if __name__ == "__main__":
	mgc = mainGtkClass()
	Gtk.main()
