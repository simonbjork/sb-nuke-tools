################

"""
	sb AutoAddGizmos
	Simon Bjork
	Version 3.0
	June 2015 (original version May 2013)
	bjork.simon@gmail.com

	Synopsis: Automatically add gizmos to a menu. Make sure the gizmo path is in your Nuke environment.

	NOTE: If you add subfolders, make sure the subfolders are in the Nuke environment aswell.

	To install the script:

	- Add the script to your Nuke pluginPath.
	- Add the following to your menu.py (changing folder path and names):

	import sb_autoAddGizmos
	sb_autoAddGizmos.sb_autoAddGizmos("<folder path>, "<menu name>", <add subfolders at path>, "menu icon (optional)")

	For example:
	sb_autoAddGizmos.sb_autoAddGizmos("D:/tools/nuke/simon/gizmos/", "Gizmos", addSubFolders=False, "menuIcon=GizmosIcon.png")

"""

################

import os
import nuke

################

def sb_autoAddGizmos(gizmoPath, menuName, addSubFolders=False, menuIcon=None):

	if not os.path.exists(gizmoPath):
		return

	# Find gizmos.
	gizmos = []
	for root, dirnames, filenames in os.walk(gizmoPath):
		for filename in filenames:
			if filename.endswith(".gizmo"):
				# Remove the gizmoPath from the string.
				# Subfolders will be kept.
				gizmo_path = os.path.join( root.replace(gizmoPath, ""), os.path.splitext(filename)[0] ).replace("\\", "/").lstrip("/")
				gizmos.append(gizmo_path)
		if not addSubFolders:
			break

	if len(gizmos) == 0:
		print "sb AutoAddGizmos: No gizmos found at {0}.".format(gizmoPath)
		return

	t = nuke.toolbar("Nodes")
	customMenu = t.findItem(menuName)

	if not customMenu:
		# Make a special case if the menu name contains submenus.
		menuNameSplit = menuName.split("/")
		if len(menuNameSplit)>1:
			mainMenu = t.addMenu(menuNameSplit[0], icon = menuIcon)
			customMenu = mainMenu.addMenu("/".join(menuNameSplit[1:]))
		else:
			customMenu = t.addMenu(menuName, icon = menuIcon)

	# Add to menu.
	for i in sorted(gizmos):
		splitPath = i.split("/")
		# Strip away "_" in the menuName.
		# Hey, it's friday...
		if addSubFolders:
			gizmoMenuName = os.path.join( "/".join(splitPath[:-1]).strip(), splitPath[-1].replace("_", " ") ).replace("\\", "/")
		else:
			gizmoMenuName = splitPath[-1].replace("_", " ")
		# Add command.
		customMenu.addCommand(gizmoMenuName, "nuke.createNode(\"" + splitPath[-1] +"\")")