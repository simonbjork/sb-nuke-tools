####################################

'''
bjorkvisuals public tools, a.k.a sb Tools.
autor: simon bjork
simon@bjorkvisuals.com
latest update: 2015-07-25
'''

####################################

'''
Import standard Python modules.
'''
import os
import nuke

####################################

'''
Import Python scripts.
'''
import sb_autoAddGizmos
import sb_autoRender
import sb_backdrop
import sb_bakeWorldPosition
import sb_cardToCamera
import sb_convertCornerPin
import sb_convertFootage
import sb_convertTracker
import sb_dagPosition
import sb_deleteViewers
import sb_distributeObjects
import sb_exportNodesAsScript
import sb_exportNukeSceneToAE
import sb_globalToolSet
import sb_lensReflections_callbacks
import sb_listExternalNodes
import sb_measureDistance
import sb_onOff
import sb_randomTimeOffset
import sb_replacePaths
import sb_revealInFileBrowser
import sb_setExpression
import sb_setKnobValue

####################################

''' 
User variables/Folder paths.
'''
# Auto add gizmos path.
autoAddGizmosPath = "D:/tools/nuke/gizmos"

# Global ToolSets (default path).
globalToolSetsPath = "D:/tools/nuke/ToolSets/"

# Show sb ConvertFootage as Modal/NonModal (True/False).
# Modal: Sets the correct size of the panel, no resizing needed. However, Nuke is locked and you can't select/deselect nodes etc once the panel is shown.
# NonModal: Does not set the size of the panel, meaning it needs to be resized. On the other hand, you have the option to select/deselect nodes etc even when the panel is shown.
convertFootageShowAsModal = False

####################################

'''
Override default backdrop function.
'''
nukescripts.autoBackdrop = sb_backdrop
nuke.toolbar("Nodes").addCommand('Other/Backdrop', 'sb_backdrop.sb_backdrop()','')

####################################

'''
Add to existing menu.
'''
nuke.menu('Nuke').findItem('File').addCommand('Export Nodes As Script (Root)...', "sb_exportNodesAsScript.sb_exportNodesAsScript()", index=9)

####################################

'''
Add gizmos automatically.
'''
sb_autoAddGizmos.sb_autoAddGizmos(autoAddGizmosPath, "MiscTools/Gizmos", addSubFolders=False, menuIcon="gizmos.png")

####################################

'''
Add a sb Tools toolbar.
'''
# Add toolbar.
sb_tools = nuke.toolbar("Nodes").addMenu( "sb_Tools", icon="sb_tools.png" )

# Gizmos.
sb_tools.addCommand("Gizmos/sb AlphaFromMax", "nuke.createNode('sb_alphaFromMax')" )
sb_tools.addCommand("Gizmos/sb CardFromAOV", "nuke.createNode('sb_cardFromAOV')" )
sb_tools.addCommand("Gizmos/sb ChangeFocal", "nuke.createNode('sb_changeFocal')" )
sb_tools.addCommand("Gizmos/sb CompoundBlur", "nuke.createNode('sb_compoundBlur')" )
sb_tools.addCommand("Gizmos/sb EdgeBlend", "nuke.createNode('sb_edgeBlend')" )
sb_tools.addCommand("Gizmos/sb Erode", "nuke.createNode('sb_erode')" )
sb_tools.addCommand("Gizmos/sb ExposureDifference", "nuke.createNode('sb_exposureDifference')" )
sb_tools.addCommand("Gizmos/sb FindPosition", "nuke.createNode('sb_findPosition')" )
sb_tools.addCommand("Gizmos/sb Glow", "nuke.createNode('sb_glow')" )
sb_tools.addCommand("Gizmos/sb Grain", "nuke.createNode('sb_grain2')" )
sb_tools.addCommand("Gizmos/sb Haze", "nuke.createNode('sb_haze')" )
sb_tools.addCommand("Gizmos/sb LensReflections", "nuke.createNode('sb_lensReflections')" )
sb_tools.addCommand("Gizmos/sb LightWrap", "nuke.createNode('sb_lightWrap')" )
sb_tools.addCommand("Gizmos/sb LumaKey", "nuke.createNode('sb_lumaKey')" )
sb_tools.addCommand("Gizmos/sb MatteEdge", "nuke.createNode('sb_matteEdge')" )
sb_tools.addCommand("Gizmos/sb NanInf", "nuke.createNode('sb_nanInf')" )
sb_tools.addCommand("Gizmos/sb PerfectCircle", "nuke.createNode('sb_perfectCircle')" )
sb_tools.addCommand("Gizmos/sb PositionTracker", "nuke.createNode('sb_positionTracker')" )
sb_tools.addCommand("Gizmos/sb SkySetup", "nuke.createNode('sb_skySetup')" )
sb_tools.addCommand("Gizmos/sb Vignette", "nuke.createNode('sb_vignette')" )

# Setup sb AutoRender defaults.
sb_tools.addCommand("Python/sb AutoRender", '''sb_autoRender.sb_autoRenderNode(
	rootFolderMethod="search word",
	rootFolderUserInput="comp", 
	customRenderPath="",
	renderType="main render",
	renderName="script name",
	customName="",
	prefix="",
	suffix="",
	addSubfolder=True,
	addColorspaceSubfolder=False,
	addFileExtensionSubfolder=False,
	addColorToFileName=True,
	useOCIO=False,
	channels="rgb",
	colorspace="Cineon",
	fileType="dpx",
	mainRenderFolder="publish/comp",
	precompRenderFolder="publish/precomp",
	proxyRenderFolder="publish/proxy",
	framePaddingSep=".",
	framePadding="####"
	)''', "shift+w")

sb_tools.addCommand("Python/sb Backdrop", "sb_backdrop.sb_backdrop()", "")
sb_tools.addCommand("Python/sb BakeWorldPosition", "sb_bakeWorldPosition.sb_bakeWorldPosition()", "")
sb_tools.addCommand("Python/sb CardToCamera", "sb_cardToCamera.sb_cardToCamera()", "")
sb_tools.addCommand("Python/sb ConvertCornerPin", "sb_convertCornerPin.sb_convertCornerPin()", "")
sb_tools.addCommand("Python/sb ConvertFootage", "sb_convertFootage.sb_convertFootage(showAsModal=convertFootageShowAsModal)", "")
sb_tools.addCommand("Python/sb ConvertTracker", "sb_convertTracker.sb_convertTracker()", "")

sb_tools.addCommand("Python/sb DAGPosition/sb LoadDAGPosition1", 'sb_dagPosition.sb_loadDagPosition(1)', 'F1')
sb_tools.addCommand("Python/sb DAGPosition/sb LoadDAGPosition2", 'sb_dagPosition.sb_loadDagPosition(2)', 'F2')
sb_tools.addCommand("Python/sb DAGPosition/sb LoadDAGPosition3", 'sb_dagPosition.sb_loadDagPosition(3)', 'F3')
sb_tools.addCommand("Python/sb DAGPosition/sb LoadDAGPosition4", 'sb_dagPosition.sb_loadDagPosition(4)', 'F4')
sb_tools.addCommand("Python/sb DAGPosition/sb LoadDAGPosition5", 'sb_dagPosition.sb_loadDagPosition(5)', 'F5')
sb_tools.addCommand("Python/sb DAGPosition/sb SaveDAGPosition1", 'sb_dagPosition.sb_saveDagPosition(1)', 'shift+F1')
sb_tools.addCommand("Python/sb DAGPosition/sb SaveDAGPosition2", 'sb_dagPosition.sb_saveDagPosition(2)', 'shift+F2')
sb_tools.addCommand("Python/sb DAGPosition/sb SaveDAGPosition3", 'sb_dagPosition.sb_saveDagPosition(3)', 'shift+F3')
sb_tools.addCommand("Python/sb DAGPosition/sb SaveDAGPosition4", 'sb_dagPosition.sb_saveDagPosition(4)', 'shift+F4')
sb_tools.addCommand("Python/sb DAGPosition/sb SaveDAGPosition5", 'sb_dagPosition.sb_saveDagPosition(5)', 'shift+F5')

sb_tools.addCommand("Python/sb DeleteViewers", "sb_deleteViewers.sb_deleteViewers()", "shift+d")
sb_tools.addCommand("Python/sb Distribute Objects", "sb_distributeObjects.sb_distributeObjects()", "")
sb_tools.addCommand("Python/sb ExportNukeSceneToAE", "sb_exportNukeSceneToAE.sb_exportNukeSceneToAE()", "")
sb_tools.addCommand("Python/sb GlobalToolSet", "sb_globalToolSet.sb_globalToolSet(globalToolsetPath)", "")
sb_tools.addCommand("Python/sb ListExternalNodes", "sb_listExternalNodes.sb_listExternalNodes()", "")
sb_tools.addCommand("Python/sb MeasureDistance", "sb_measureDistance.sb_measureDistance()", "")
sb_tools.addCommand("Python/sb OnOff", "sb_onOff.sb_onOff()", "")
sb_tools.addCommand("Python/sb RandomTimeOffset", "sb_randomTimeOffset.sb_randomTimeOffset()", "")
sb_tools.addCommand("Python/sb ReplacePaths", "sb_replacePaths.sb_replacePaths()", "")
sb_tools.addCommand("Python/sb RevealInFileBrowser", "sb_revealInFileBrowser.sb_revealInFileBrowser()", "shift+r")
sb_tools.addCommand("Python/sb SetExpression", "sb_setExpression.sb_setExpression()", "")
sb_tools.addCommand("Python/sb SetKnobValue", "sb_setKnobValue.sb_setKnobValue()", "")

####################################