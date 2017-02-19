#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import json
import urllib2
import os
import xlwt
from threading import Thread
from urlparse import urlparse
from os.path import splitext, basename

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass


ApiUrlGetUserInfo = "https://v2api.collaborizm.com/v2/users/"
ApiUrlGetUserProfileImage = "https://res.cloudinary.com/collabizm/image/facebook/c_fill,w_200,h_200,q_auto,g_face,dpr_1,f_auto/v1/"
ApiUrlGetUserList = "https://v2api.collaborizm.com/v2/people/list?page=" #page=0 get page 0 each page contain 16 user

GObject.threads_init()

class Widgets:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("main.glade")
		self.window = self.builder.get_object("window")
		self.liststore_project = self.builder.get_object("liststore_project")
		self.treeview_project = self.builder.get_object("treeview_project")

		#avtar image
		self.avtar = self.builder.get_object("avtar")
		#user name lable
		self.usernameLable = self.builder.get_object("usernameLable")

		#notebook elements
		self.notebook = self.builder.get_object("notebook")
		self.Tab1ScrollView = self.builder.get_object("Tab1ScrollView")
		self.Tab1ListBox = self.builder.get_object("Tab1ListBox")

		#self.Tab1View = self.builder.get_object("Tab1View")
		#self.Tab2View = self.builder.get_object("Tab2View")
		#self.Tab3View = self.builder.get_object("Tab3View")	
		self.processPopUp = self.builder.get_object("processPopUp")
		
		
class Handler:
	def __init__(self,wdgt):
		self.wdgt = wdgt
		
	def updateUserInfo(self,userId):
		response = urllib2.urlopen(ApiUrlGetUserInfo+userId)
		jsonObj = json.loads(response.read())

		fullName = jsonObj["first_name"]+" "
		fullName += jsonObj["last_name"]
		print "Full Name From Thread"+ fullName
		imageUrl = jsonObj["facebook_id"]
		path = "/tmp/"
		fullUrl	= ApiUrlGetUserProfileImage + imageUrl
		disassembled = urlparse(imageUrl)
		imageName = basename(disassembled.path)
		path+=imageName+".jpg"
		try:
			f = open(path,'wb')
			f.write(urllib2.urlopen(fullUrl).read())
			f.close()
			self.wdgt.avtar.set_from_file(path);
		except:
			print "cant download avatar"

		
		self.wdgt.usernameLable.set_text(fullName)	#top user name lable

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def userSelectFronList(self, *args):	  
		treeViewWidget = args[0]
		selectionId = args[1]
		treeViewWidgetColumn = args[2]
		selection = treeViewWidget.get_selection()
		model, treeiter = selection.get_selected()
		if treeiter != None:
			userId = model[treeiter][0:4][3]	#row:column
		Thread(target=self.updateUserInfo,args=(userId,)).start()

class mainGtkClass:
	def __init__(self):
		
		self.wdgt = Widgets()

		self.wdgt.builder.connect_signals(Handler(self.wdgt))
		self.wdgt.window.maximize()		

		renderer = Gtk.CellRendererText()
		self.column1 = Gtk.TreeViewColumn("User", renderer, text=0)

		self.wdgt.treeview_project.append_column(self.column1)

		self.column2 = Gtk.TreeViewColumn("Like", renderer, text=1)
		self.wdgt.treeview_project.append_column(self.column2)
	
		self.column3 = Gtk.TreeViewColumn("Status", renderer, text=2)
		self.wdgt.treeview_project.append_column(self.column3)
		#self.column1.set_sort_column_id(0) #sort column by name
		#create excel file for user list and ID
		self.book = xlwt.Workbook(encoding="utf-8")
		self.sheet1 = self.book.add_sheet("Sheet 1",cell_overwrite_ok=True)
	
		#response = urllib2.urlopen(ApiUrlGetUserInfo+"SJyT86LIl")
		#data = json.loads(response.read())
		#self.setUserName(data)				

		self.getUserList();

		self.wdgt.window.show_all()
		
	def getUserList(self):
		
		index = 0
		response = urllib2.urlopen(ApiUrlGetUserList+str(0))
		jsonObj = json.loads(response.read())
		

		#for item in jsonObj:
		for index in range(len(jsonObj)):
			fullname = jsonObj[index]['first_name']+" "+jsonObj[index]['last_name']
			userId = jsonObj[index]['id']
			userAvtarId = jsonObj[index]['facebook_id']
			print userId+"->"+fullname+"->"+userAvtarId
			#store data in excel file 
			self.sheet1.write(index, 0, userId)
			self.sheet1.write(index, 1, fullname)
			self.sheet1.write(index, 2, userAvtarId)
			self.book.save("/tmp/userlist.xls")

			self.wdgt.liststore_project.append([fullname,0,1,userId])	#add full name to list view
			index = index+1
		

	def setUserName(self,jsonObj):
		value = jsonObj["first_name"]+" "
		value += jsonObj["last_name"]
		self.wdgt.usernameLable.set_text(value)	#top user name lable
		lbl = Gtk.Label(value)
		lbl.set_alignment(xalign=0, yalign=1) 

		lbl1 = Gtk.Label(value)
		lbl1.set_alignment(xalign=0, yalign=1) 

		self.wdgt.Tab1ListBox.add(lbl)


		self.downlodImage(jsonObj)

	def downlodImage(self,jsonObj):	#Download User Profile image
		imageUrl = jsonObj["facebook_id"]
		path = "/tmp/"
		fullUrl	= ApiUrlGetUserProfileImage + imageUrl
		disassembled = urlparse(imageUrl)
		imageName = basename(disassembled.path)
		path+=imageName+".jpg"
		print fullUrl
		print path
		try:
			f = open(path,'wb')
			f.write(urllib2.urlopen(fullUrl).read())
			f.close()
			self.wdgt.avtar.set_from_file(path);
		except:
			print "cant download avatar"


if __name__ == "__main__":
	mgc = mainGtkClass()
	Gtk.main()
