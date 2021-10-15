################

"""
	sb_SetExpression
	Simon Bjork
	January 2015
	Version 1.0
	bjork.simon@gmail.com

	Synopsis: Set expression on multiple nodes/knobs.
	OS: Windows/OSX/Linux

	To install the script:
	- Add the script to your Nuke pluginPath.
	- Add the following to your init.py/menu.py:

	import sb_setExpression
	sb_tools = nuke.toolbar("Nodes").addMenu( "sb_Tools", icon = "sb_tools.png" )
	sb_tools.addCommand('Python/sb setExpression', 'sb_setExpression.sb_setExpression()', "")

"""
################

from __future__ import with_statement
import nuke
import nukescripts

################

def sb_setExpression_Data():

	data = {}
	data["scriptName"] = "sb SetExpression"
	data["scriptVersion"] = "1.0"
	return data

def sb_setExpression_Help():

	si = sb_setExpression_Data()

	helpStr = ("<b>{0} {1}</b>\n\n"

	"Set expressions on multiple nodes/knobs.\n\n"
	"Hover the mouse cursor over a knob to see it's name.\n\n"
	"Option to filter by node class (hit i when a node is selected to get it's class).\n\n"
	"Option to edit expressions (replace part of string). Useful when a node is renamed for example.\n\n".format(si["scriptName"], si["scriptVersion"] ))
	
	return helpStr.lstrip()

class sb_setExpression_Panel(nukescripts.PythonPanel):

	def __init__(self):
		scriptData = sb_setExpression_Data()
		nukescripts.PythonPanel.__init__(self, '{0} v{1}'.format(scriptData["scriptName"], scriptData["scriptVersion"]))
		self.nodes = nuke.Enumeration_Knob("nodes", "nodes", ["selected nodes", "all nodes", "all nodes (incl groups)"])
		self.action = nuke.Enumeration_Knob("action", "action", ["set expression", "edit expression"])
		self.div1 = nuke.Text_Knob("divider1", "")
		self.classFilter = nuke.String_Knob("classFilter", "class filter (optional)")
		self.div2 = nuke.Text_Knob("divider2", "")
		self.knobs = nuke.Enumeration_Knob("knobs", "knobs", ["specify knob name", "all knobs (potentially very slow)"])
		self.div3 = nuke.Text_Knob("divider3", "")
		self.kName = nuke.String_Knob("kName", "knob name")
		self.expr = nuke.String_Knob("expression", "expression")
		self.replaceSrc = nuke.String_Knob("replaceSrc", "replace:")
		self.div4 = nuke.Text_Knob("divider4", "")
		self.replaceDst = nuke.String_Knob("replaceDst", "with:", "")
		self.help = nuke.PyScript_Knob("help", " ? ")
		self.help.setFlag(nuke.STARTLINE)
		self.div5 = nuke.Text_Knob("divider5", "")
		self.setVal = nuke.PyScript_Knob("setVal", "set value")

		for i in [self.nodes, self.action, self.div1, self.classFilter, self.div2, self.knobs, self.kName, self.div3, self.expr, self.replaceSrc, self.replaceDst, self.div4, self.help, self.div5, self.setVal]:
			self.addKnob(i)

		self.knobs.setVisible(False)
		self.div3.setVisible(False)
		self.replaceSrc.setVisible(False)
		self.replaceDst.setVisible(False)

	# Set knobChanged commands.
	def knobChanged(self, knob):
		if knob is self.setVal:
			self.setExpressionToKnobs()
		elif knob is self.action:
			if self.action.value() == "set expression":
				self.expr.setVisible(True)
				self.knobs.setVisible(False)
				self.div3.setVisible(False)
				self.replaceSrc.setVisible(False)
				self.replaceDst.setVisible(False)
				self.kName.setVisible(True)
			else:
				self.expr.setVisible(False)
				self.knobs.setVisible(True)
				self.div3.setVisible(True)
				self.replaceSrc.setVisible(True)
				self.replaceDst.setVisible(True)
				if self.knobs.value() == "specify knob name":
					self.kName.setVisible(True)
				else:
					self.kName.setVisible(False)
		elif knob is self.knobs:
			if self.knobs.value() == "specify knob name":
				self.kName.setVisible(True)
			else:
				self.kName.setVisible(False)
		elif knob is self.help:
			nuke.message(sb_setExpression_Help())

	# Main function.
	def setExpressionToKnobs(self):

		nodes = self.nodes.value()
		action = self.action.value()
		kName = self.kName.value()
		expr = self.expr.value()
		knobs = self.knobs.value()
		classFilter = self.classFilter.value()
		replaceSrc = self.replaceSrc.value()
		replaceDst = self.replaceDst.value()


		if nodes == "selected nodes":
			if classFilter:
				nodeList = nuke.selectedNodes(classFilter)
			else:
				nodeList = nuke.selectedNodes()
		elif nodes == "all nodes":
			if classFilter:
				nodeList = nuke.allNodes(classFilter)
			else:
				nodeList = nuke.allNodes()
		else:
			if classFilter:
				nodeList = nuke.allNodes(classFilter, recurseGroups=True)
			else:
				nodeList = nuke.allNodes(recurseGroups=True)

		# Error checking.
		if action == "set expression":
			if not kName or not expr:
				nuke.message("Set both knob name and expression string.")
				return
		elif action == "edit expression":
			if knobs == "specify knob name" and not kName:
				nuke.message("Set knob name.")
				return
			if not replaceSrc or not replaceDst:
				nuke.message("Set both source/replacement string.")
				return

		# Counters.
		updatedKnobs = 0

		# Begin undo command.
		undo = nuke.Undo() 
		undo.begin(sb_setExpression_Data()["scriptName"])

		for i in nodeList:

			if action == "set expression":			
				try:
					i[kName].setExpression(expr)
					updatedKnobs+=1
				except:
					continue
			
			elif action == "edit expression":
				try:
					if knobs == "specify knob name":
						# Create a list with the single knob name. That way we can use same code.
						knobsToLoop = [i[kName]]
					else:
						# Note the allKnobs() function. It returns the actual knob object.
						knobsToLoop = i.allKnobs()

					
					for knob in knobsToLoop:
						if knob.hasExpression():
							for index, anim in enumerate( knob.animations() ): 
								old = anim.expression()
								if replaceSrc in old:
									new = old.replace(replaceSrc, replaceDst)
									anim.setExpression(new)
									if index == len(knob.animations())-1:
										updatedKnobs+=1
				except:
					continue


		nuke.message( "Updated knobs: {0}".format(updatedKnobs) )

		# End undo command.
		undo.end()

# Run main script.
def sb_setExpression():
	sb_setExpression_Panel().show()