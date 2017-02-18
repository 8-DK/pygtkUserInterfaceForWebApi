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
		self.ApiUrlGetUserBaseUserInfo = "https://res.cloudinary.com/collabizm/image/facebook/c_fill,w_200,h_200,q_auto,g_face,dpr_1,f_auto/v1/"
		self.apiUrlGetUserList = "https://v2api.collaborizm.com/v2/people/list?page=" #page=0 get page 0 each page contain 16 user
		builder = Gtk.Builder()
		builder.add_from_file("main.glade")	
		builder.connect_signals(Handler())

		self.window = builder.get_object("window")
		self.liststore_project = builder.get_object("liststore_project")
		self.treeview_project = builder.get_object("treeview_project")

		#avtar image
		self.avtar = builder.get_object("avtar")
		#user name lable
		self.usernameLable = builder.get_object("usernameLable")

		#notebook elements
		self.notebook = builder.get_object("notebook")
		self.Tab1ScrollView = builder.get_object("Tab1ScrollView")
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

		lbl1 = Gtk.Label(value)
		lbl1.set_alignment(xalign=0, yalign=1) 
		lbl2 = Gtk.Label(value)
		lbl2.set_alignment(xalign=0, yalign=1) 
		lbl3 = Gtk.Label(value)
		lbl3.set_alignment(xalign=0, yalign=1) 
		lbl4 = Gtk.Label(value)
		lbl4.set_alignment(xalign=0, yalign=1) 
		lbl5 = Gtk.Label(value)
		lbl5.set_alignment(xalign=0, yalign=1) 
		lbl6 = Gtk.Label(value)
		lbl6.set_alignment(xalign=0, yalign=1) 
		lbl7 = Gtk.Label(value)
		lbl7.set_alignment(xalign=0, yalign=1) 
		lbl8 = Gtk.Label(value)
		lbl8.set_alignment(xalign=0, yalign=1) 
		lbl9 = Gtk.Label(value)
		lbl9.set_alignment(xalign=0, yalign=1) 
		lbl10 = Gtk.Label(value)
		lbl10.set_alignment(xalign=0, yalign=1) 
		lbl11 = Gtk.Label(value)
		lbl11.set_alignment(xalign=0, yalign=1) 
		lbl12 = Gtk.Label(value)
		lbl12.set_alignment(xalign=0, yalign=1) 
		lbl13 = Gtk.Label(value)
		lbl13.set_alignment(xalign=0, yalign=1) 
		lbl14 = Gtk.Label(value)
		lbl14.set_alignment(xalign=0, yalign=1) 
		lbl15 = Gtk.Label(value)
		lbl15.set_alignment(xalign=0, yalign=1) 
		lbl16 = Gtk.Label(value)
		lbl16.set_alignment(xalign=0, yalign=1) 
		lbl17 = Gtk.Label(value)
		lbl17.set_alignment(xalign=0, yalign=1) 
		lbl18 = Gtk.Label(value)
		lbl18.set_alignment(xalign=0, yalign=1) 
		lbl19 = Gtk.Label(value)
		lbl19.set_alignment(xalign=0, yalign=1) 
		

		self.Tab1ListBox.add(lbl)
		self.Tab1ListBox.add(lbl1)
		self.Tab1ListBox.add(lbl2)
		self.Tab1ListBox.add(lbl3)
		self.Tab1ListBox.add(lbl4)
		self.Tab1ListBox.add(lbl5)
		self.Tab1ListBox.add(lbl6)
		self.Tab1ListBox.add(lbl7)
		self.Tab1ListBox.add(lbl8)
		self.Tab1ListBox.add(lbl9)
		self.Tab1ListBox.add(lbl10)
		self.Tab1ListBox.add(lbl11)
		self.Tab1ListBox.add(lbl12)
		self.Tab1ListBox.add(lbl13)
		self.Tab1ListBox.add(lbl14)
		self.Tab1ListBox.add(lbl15)
		self.Tab1ListBox.add(lbl16)
		self.Tab1ListBox.add(lbl17)
		self.Tab1ListBox.add(lbl18)
		self.Tab1ListBox.add(lbl19)

		self.downlodImage(jsonObj["facebook_id"],"/tmp/")

	def downlodImage(self,imageUrl,path):
		
		fullUrl	= self.ApiUrlGetUserBaseUserInfo + imageUrl
		disassembled = urlparse(imageUrl)
		imageName = basename(disassembled.path)
		path+=imageName+".jpg"
		print fullUrl
		print path
		try:
			f = open(path,'wb')
			f.write(urllib2.urlopen(fullUrl).read())
			f.close()
			self.avtar.set_from_file(path);
		except:
			print "cant download avatar"


if __name__ == "__main__":
	mgc = mainGtkClass()
	Gtk.main()
