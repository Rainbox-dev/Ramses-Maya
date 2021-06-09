import ramses as ram # pylint: disable=import-error
import maya.cmds as cmds
from .utils_constants import  *
import ramses as ram

ramses = ram.Ramses.instance()

def getFileInfo( filePath):
    fileInfo = ram.RamFileManager.decomposeRamsesFilePath( filePath )
    if fileInfo is None:
        ram.log(ram.Log.MalformedName, ram.LogLevel.Fatal)
        cmds.inViewMessage( msg=ram.Log.MalformedName, pos='midCenter', fade=True )
        cmds.error( ram.Log.MalformedName )
        return None
    return fileInfo

def getPublishFolder( item, step):
    publishFolder = item.publishFolderPath( step )
    if publishFolder == '':
        ram.log("I can't find the publish folder for this item, maybe it does not respect the ramses naming scheme or it is out of place.", ram.LogLevel.Fatal)
        cmds.inViewMessage( msg="Can't find the publish folder for this scene, sorry. Check its name and location.", pos='midCenter', fade=True )
        cmds.error( "Can't find publish folder." )
        return ''
    return publishFolder

def getPipes( step, currentSceneFilePath = '' ):
    pipes = step.outputPipes()
    if len( pipes ) == 0:
        # Get defaults
        if step == MOD_STEP:
            pipes = MOD_STEP.outputPipes()
        elif step == SHADE_STEP:
            pipes = SHADE_STEP.outputPipes()
    
    if len( pipes ) == 0: # Let's ask!
        # TODO UI
        return pipes

    if currentSceneFilePath == '':
        return pipes

    scenePipes = []

    # Get the current step if possible
    currentStepShortName = ''
    saveFilePath = ram.RamFileManager.getSaveFilePath( currentSceneFilePath )

    if saveFilePath != '':
        saveFileInfo = ram.RamFileManager.decomposeRamsesFilePath( saveFilePath )
        if saveFileInfo is not None:
            currentProject = ramses.project( saveFileInfo['project'] )
            if currentProject is None:
                currentProject = ramses.currentProject()
            else:
                ramses.setCurrentProject( currentProject )
            if currentProject is not None:
                currentStep = currentProject.step( saveFileInfo['step'] )
                currentStepShortName = currentStep.shortName()

    # Check the pipes
    for pipe in pipes:
        if pipe.inputStepShortName() == currentStepShortName or currentStepShortName == '' or pipe.inputStepShortName() == '':
            scenePipes.append(pipe)

    return scenePipes