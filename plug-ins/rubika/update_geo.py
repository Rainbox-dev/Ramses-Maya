# -*- coding: utf-8 -*-

from .utils_update import update
from .import_geo import importGeo
import maya.cmds as cmds # pylint: disable=import-error

def updateGeo( node, filePath, item, step):

    # Re-import
    newRootCtrls = importGeo( item, filePath, step )

    # Snap and re-apply sets
    newRootCtrls = update(node, newRootCtrls)

    # Delete the old hierarchy and the locator
    cmds.delete( node )

    return newRootCtrls