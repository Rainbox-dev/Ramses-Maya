import sys, os

import maya.api.OpenMaya as om # pylint: disable=import-error
import maya.cmds as cmds # pylint: disable=import-error

from dumaf import ( # pylint: disable=import-error,no-name-in-module
    registerCommands,
    unregisterCommands,
    getMayaWindow
)

from ui_settings import SettingsDialog # pylint: disable=import-error,no-name-in-module

import ramses as ram
# Keep the ramses and the settings instances at hand
ramses = ram.Ramses.instance()
settings = ram.RamSettings.instance()

def checkDaemon():
    """Checks if the Daemon is available (if the settings tell we have to work with it)"""
    if settings.online:
        if not ramses.connect():
            cmds.confirmDialog(
                title="No User",
                message="You must log in Ramses first!",
                button=["OK"],
                icon="warning"
                )
            ramses.showClient()
            cmds.error( "User not available: You must log in Ramses first!" )
            return False

    return True

def getSaveFilePath( filePath ):
    # Ramses will check if the current file has to be renamed to respect the Ramses Tree and Naming Scheme
    saveFilePath = ram.RamFileManager.getSaveFilePath( filePath )
    if not saveFilePath: # Ramses may return None if the current file name does not respeect the Ramses Naming Scheme
        cmds.warning( ram.Log.MalformedName )
        # Set file to be renamed
        cmds.file( renameToSave = True )
        cmds.inViewMessage( msg='Malformed Ramses file name! <hl>Please save with a correct name first</hl>.', pos='midCenter', fade=True )
        return None

    return saveFilePath

class RamOpenCmd( om.MPxCommand ):
    name = "ramOpen"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamOpenCmd()

    def doIt(self, args):
        ram.log("Command 'open' is not implemented yet!")

class RamSaveCmd( om.MPxCommand ):
    name = "ramSave"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamSaveCmd()

    def doIt(self, args):
        ram.log("Saving file...")

        # The current maya file
        currentFilePath = cmds.file( q=True, sn=True )
        ram.log("Saving file: " + currentFilePath)
        
        # Check if the Daemon is available if Ramses is set to be used "online"
        if not checkDaemon():
            return

        # Get the save path 
        saveFilePath = getSaveFilePath( currentFilePath )
        if not saveFilePath:
            return

        # If the current Maya file is inside a preview/publish/version subfolder, we're going to increment
        # to be sure to not lose the previous working file.
        increment = False
        if ram.RamFileManager.inReservedFolder( currentFilePath ):
            increment = True
            cmds.warning( "Incremented and Saved as " + saveFilePath )

        # Set the save name and save
        cmds.file( rename = saveFilePath )
        cmds.file( save=True, options="v=1;" )
        # Backup / Increment
        backupFilePath = ram.RamFileManager.copyToVersion( saveFilePath, increment=increment )
        backupFileName = os.path.basename( backupFilePath )
        decomposedFileName = ram.RamFileManager.decomposeRamsesFileName( backupFileName )
        newVersion = str( decomposedFileName['version'] )
        ram.log( "Scene saved! Current version is: " + newVersion )
        cmds.inViewMessage( msg='Scene saved! <hl>v' + newVersion + '</hl>', pos='midCenter', fade=True )

class RamSaveVersionCmd( om.MPxCommand ):
    name = "ramSaveVersion"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamSaveVersionCmd()

    def doIt(self, args):
        # The current maya file
        currentFilePath = cmds.file( q=True, sn=True )
        ram.log("Saving file: " + currentFilePath)
        
        # Check if the Daemon is available if Ramses is set to be used "online"
        if not checkDaemon():
            return

        # Get the save path 
        saveFilePath = getSaveFilePath( currentFilePath )
        if not saveFilePath:
            return

        # Set the save name and save
        cmds.file( rename = saveFilePath )
        cmds.file( save=True, options="v=1;" )
        # Backup / Increment
        backupFilePath = ram.RamFileManager.copyToVersion( saveFilePath, increment=True )
        backupFileName = os.path.basename( backupFilePath )
        decomposedFileName = ram.RamFileManager.decomposeRamsesFileName( backupFileName )
        newVersion = str( decomposedFileName['version'] )
        ram.log( "Incremental save, scene saved! New version is: " + newVersion )
        cmds.inViewMessage( msg='Incremental save! New version: <hl>v' + newVersion + '</hl>', pos='midCenter', fade=True )

class RamPublishCmd( om.MPxCommand ):
    name = "ramPublish"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamPublishCmd()

    def doIt(self, args):
        ram.log("Command 'publish' is not implemented yet!")

class RamRetrieveVersionCmd( om.MPxCommand ):
    name = "ramRetriveVersion"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamRetrieveVersionCmd()

    def doIt(self, args):
        ram.log("Command 'retrieve version' is not implemented yet!")

class RamPublishTemplateCmd( om.MPxCommand ):
    name = "ramPulbishTemplate"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamPublishTemplateCmd()

    def doIt(self, args):
        ram.log("Command 'publish as template' is not implemented yet!")

class RamOpenTemplateCmd( om.MPxCommand ):
    name = "ramOpenTemplate"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamOpenTemplateCmd()

    def doIt(self, args):
        ram.log("Command 'open template' is not implemented yet!")

class RamImportTemplateCmd( om.MPxCommand ):
    name = "ramImportTemplate"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamImportTemplateCmd()

    def doIt(self, args):
        ram.log("Command 'import template' is not implemented yet!")

class RamSettingsCmd( om.MPxCommand ):
    name = "ramSettings"
    settingsDialog = SettingsDialog( getMayaWindow() )

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamSettingsCmd()

    def doIt(self, args):
        ram.log("Opening settings...")  
        self.settingsDialog.show()

class RamOpenRamsesCmd( om.MPxCommand ):
    name = "ramOpenRamses"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def createCommand():
        return RamOpenRamsesCmd()

    def doIt(self, args):
        ram.log("Opening the Ramses client...")
        ramses.showClient()
        
cmds_classes = (
    RamOpenCmd,
    RamSaveCmd,
    RamSaveVersionCmd,
    RamPublishCmd,
    RamRetrieveVersionCmd,
    RamPublishTemplateCmd,
    RamOpenTemplateCmd,
    RamImportTemplateCmd,
    RamSettingsCmd,
    RamOpenRamsesCmd,
)

cmds_menuItems = []

def maya_useNewAPI():
    pass

def initializePlugin(obj):
    # Register all commands
    registerCommands( obj, cmds_classes )

    # Add Menu Items
    cmds_menuItems.append( [
        cmds.menuItem(
            parent='MayaWindow|mainWindowMenu',
            divider=True
            ),
        cmds.menuItem(
            parent='MayaWindow|mainWindowMenu',
            label='Ramses Settings',
            command=cmds.ramSettings
            ) ]
    )

def uninitializePlugin(obj):
    # Unregister all commands
    unregisterCommands( obj, cmds_classes )

    # Remove menu items
    for menuItem in cmds_menuItems:
        cmds.deleteUI( menuItem, menuItem = True )
