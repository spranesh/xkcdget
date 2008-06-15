 What is XKCDGet?
 ================
	 Gets Comics from http://www.xkcd.com Uses $HOME/.xkcdrc to record when the user
	 last accessed xkcd using the program. Outputs results in a simple html file.

	 Program is structured in a way so that only the functions and global variables
	 have to be changed for minor modifications of http://www.xkcd.com

	 Program Authors:
	 Name                  Gmail Username
	 ====		        ==============
	 Naveen Kumar Molleti  <nerd.naveen>
	 Pranesh Srinivasan    <spranesh>
	 Samhita Reddy Kasula  <samhita.kasula>





 What's new?
 ===========
			 Version 1.1.4
			 --------------
 Date : June 8th 2008. 
	  The structure of the program has been split into the main script, and 2 other modules
	  - a module with functions and variables that defines the user interface
	  - a module with functions and variables that defines how the XKCD html file is parsed.
	  The modules are given the name XKCDUI and XKCDParse respectively.
	  They each contain a single class
	  XKCDUI : UI		
	  XKCDParse : Parse
	  Any changes to the XKCD site by Randall Munroe will now have to be implemented 
	  only in the Parse module. Any change to the program's UI will be made only in the 
	  UI module.

	  The program history will be in the Readme only.

	  quit() has been replaced by sys.exit() everywhere to standardise everything

	  Replaced all Single Quotes in XKCD Image tags, with Double quotes, to prevent interfering with shell
 

 Program History
 ===============
			 Version 1.1.3
			 --------------
	 The program has been restructured into classes

			 Version 1.1.2
			 --------------
	 New Features :
	 Gui Support with -g flag and command line support with -c flag
	 Also added defaults for operating systems
	 Opens comic automatically in web browser.
	 Now accesses home directory through user module
	 Added Zenity for linux systems supporting it for native look and feel
	 Changed HTTPError u2.HTTPError
	 
	 To Do :
	 Arrange the Code into a neat Class 
	 of functions, to avoid global variables

