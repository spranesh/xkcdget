#!/usr/bin/env python

	# Gets Comics from http://www.xkcd.com Uses $HOME/.xkcdrc to record when the user
	# last accessed xkcd using the program. Outputs results in a simple html file.

	# Program is structured in a way so that only the functions and global variables
	# have to be changed for minor modifications of http://www.xkcd.com

	# Program Authors:
	# Name                  Gmail Username
	# ====		        ==============
	# Naveen Kumar Molleti  <nerd.naveen>
	# Pranesh Srinivasan    <spranesh>
	# Samhita Reddy Kasula  <samhita.kasula>


	#			  What's new?
	#			  ===========
	# Version 1.1.4
	# Date : June 8th 2008. 
	#	  The structure of the program has been split into the main script, and 2 other modules
	#	  - a module with functions and variables that defines the user interface
	#	  - a module with functions and variables that defines how the XKCD html file is parsed.
	#	  The modules are given the name XKCDUI and XKCDParse respectively.
	#	  They each contain a single class
	#	  XKCDUI : UI		
	#	  XKCDParse : Parse
	#	  Any changes to the XKCD site by Randall Munroe will now have to be implemented 
	#	  only in the Parse module. Any change to the program's UI will be made only in the 
	#	  UI module.
	#
	#	  The program history will be in the Readme only.
	#
	#	  quit() has been replaced by sys.exit() everywhere to standardise everything
	#
	#	  Replaced all Single Quotes in XKCD Image tags, with Double quotes, to prevent interfering with shell
			 


''' This file is the main module'''


import sys
import os
import urllib as u1
import urllib2 as u2
import BeautifulSoup as BS
import webbrowser
import user

import XKCDParse
import XKCDUI


#A few functions are defined first
def getConfigFileName():
	'''This function returns the path to the config file, depending on the Operating System.'''
	try:
		config_file = os.path.join(user.home, ".xkcdrc")
	except KeyError:
		display("XKCDGet is not available for your OS yet.\n", zenity)
		quit()
	return config_file

def write_to_file(filename, filecontent):
	f = open(filename, "w")
	f.write(filecontent)
	f.close()



#we define a few global variables in the lines to follow
config_file 	= getConfigFileName()
ImageFolder 	= 'images'
thanks 		= "Thanks for using NPS XKCDGet\n"
xkcd 		= "http://www.xkcd.com"

#parameters to be passed in order are image_title, title(again), image_filename, image_mouseOver
html_markup 	= "<html><head><title>%s</title></head><body><center><h3>%s</h3><hr /><br /><img src='%s' /> <br />%s<hr /><br />%s</center></body></html>"



# --------------------------------------------------
# The main program starts here
# --------------------------------------------------
if __name__ == '__main__':
	UI = XKCDUI.UI(sys.argv) 

	try:
		f = open(config_file, "r")
		#the last accessed strip
		lAcc = int(f.readline().strip()) 
		f.close()
	except IOError, OSError:
		s = "ERROR: Some error in looking up last accessed file has occured. We will assume whatever we fetch is the latest one. If this is the first time you are running the program there is no cause for worry. This is perfectly alright. \n"
		UI.display(s)

		lAcc = 0

	try:
		f = u2.urlopen(xkcd)
		page = f.read()
		f.close()
	except u2.HTTPError, e:
		UI.display("Error code "+ e+ ". Site could not be openend \n", error=1)
		quit()
	except IOError:
		UI.display("For some vague reason that even we do not understand, we could not read from /tmp \n",  error = 1)
		quit()

	Parser = XKCDParse.Parse(BS.BeautifulSoup(page), UI)

#we now parse the soup for the PrevTag
	CCno = Parser.getComicNumber()

	if CCno > lAcc :
		UI.display("A new comic is out. Downloading to current directory. \n")
		img_url, img_title, img_mouseOver = Parser.getImgAttr()		

		if not os.path.isdir(ImageFolder):
			os.mkdir(ImageFolder)
		
		#In case there is an error (the dir already exists), we do nothing.
		
		try:
			img_naming_scheme = "%d_%s"%(CCno, img_title.replace(' ', '_'))
			img_save = os.path.join(ImageFolder,img_naming_scheme+'.png')
			u1.urlretrieve(img_url, img_save)
		except:
			#We did not mention error code, since urllib1 does not have HTTPError Code defined
			XKCDParse.layoutChanged()

		#the following 2 lines, save the html file markup
		page_source = BS.BeautifulSoup(html_markup%(img_title, img_title, img_save, img_mouseOver, thanks)).prettify()
		write_to_file(img_naming_scheme +'.html', page_source)


		s1 = "Image downloaded"
		s2 = "\n"*3
		s3 = " Comic title       : %s\n"%img_title
		s4 = " Comic number      : %d\n"%CCno
		s5 = " Comic Mouse Over  : %s\n"%img_mouseOver
		s6 = " Saved HTML File   : %s\n"%(img_naming_scheme+'.html')

		UI.display(s1+s2+s3+s4+s5+s6)
		
		try :
			webbrowser.open(img_naming_scheme+'.html')
		except:
			pass

		write_to_file(config_file, str(CCno))

		if not UI.gui:
			UI.display("\n"*3)

	else :
		UI.display("No new comic. You are up to date \n")
