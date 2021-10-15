################

"""
	sb ExportNodesAsScript
	Simon Bjork
	October 2014
	Version 1.0
	bjork.simon@gmail.com

	Synopsis: Exports the selected nodes as a script, including the Root node (most knobs).
	OS: Windows/OSX/Linux

	Installation (menu.py):
	nuke.menu('Nuke').findItem('File').addCommand('Export Nodes As Script (Root)...', "sb_exportNodesAsScript.sb_exportNodesAsScript()", index=9)

"""

################

import nuke
import nukescripts
import os

################

def sb_exportNodesAsScript():

	if len(nuke.selectedNodes()) == 0:
		nuke.message("Select nodes to export.")
		return

	filePath = nuke.getClipname("Export nodes as script (including Root node).")

	if not filePath:
		return

	if not filePath.endswith(".nk"):
		filePath = "{0}.nk".format(filePath)

	# Folder path.
	folderPath = "/".join(filePath.split("/")[:-1])

	if not os.path.exists(folderPath):
		try:
			os.makedirs(folderPath)
		except:
			raise Exception ("Can't create folder at:\n{0}".format(folderPath))

	try:
		# Save nodes as script (excluding Root node).
		nuke.nodeCopy(filePath)

		# The Root node isn't saved with nuke.nodeCopy, so it needs to be saved separately.
		# First let's save some knobs manually.
		rootValues = ""
		r = nuke.Root() 
		wantedKnobs = ['inputs', 'frame', 'first_frame', 'last_frame', 'proxy', 'proxy_type', 'proxy_format', 'label']
		for k, v in r.knobs().iteritems(): 
			if not k in wantedKnobs:
				continue
			knobValue = r[k].toScript()
			if not knobValue:
				knobValue = '""'
			if len(knobValue.split(" ")) > 1:
				knobValue = '"' + knobValue + '"'

			rootValues = "{0}\n{1} {2}".format(rootValues, k, knobValue)

		# Add more root knobs via the writeKnobs function.
		# This will add user created knobs as well.
		moreRootKnobs = nuke.root().writeKnobs(nuke.TO_SCRIPT | nuke.WRITE_USER_KNOB_DEFS)
		rootValues = "{0}{1}".format(rootValues, moreRootKnobs)

		# Open saved backup script.
		f = open(filePath,"r")
		savedNodes = f.read()
		f.close()

		# Combine root values with the rest of the nodes.
		allNodes = "Root {0}\n{1}\n{2}\n{3}".format("{", rootValues.strip(), "}", savedNodes)

		f = open(filePath, "w")
		f.write(allNodes)

		print "Nodes exported successfully to {0}".format(filePath)
	except Exception as e:
		raise Exception ("Could not export nodes as script to: {0}\n{1}".format(filePath, e))
