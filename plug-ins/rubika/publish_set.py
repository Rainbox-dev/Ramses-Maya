# -*- coding: utf-8 -*-

import maya.cmds as cmds # pylint: disable=import-error
import ramses as ram # pylint: disable=import-error
import dumaf as maf # pylint: disable=import-error
from .ui_publish_geo import PublishGeoDialog
from .utils_shaders import exportShaders
from .utils_nodes import getPublishNodes
from .utils_attributes import * # pylint: disable=import-error
from .utils_constants import * # pylint: disable=import-error
from .utils_general import * # pylint: disable=import-error
from .utils_items import * # pylint: disable=import-error
from .utils_publish import *

def publishSet(item, step, publishFileInfo, pipeFiles):

    # Options
    # Show dialog
    publishGeoDialog = PublishGeoDialog( maf.UI.getMayaWindow() )
    if not publishGeoDialog.exec_():
        return

    removeHidden = publishGeoDialog.removeHidden()
    removeLocators = publishGeoDialog.removeLocators()
    renameShapes = publishGeoDialog.renameShapes()
    noFreeze = publishGeoDialog.noFreeze()
    noFreezeCaseSensitive = publishGeoDialog.noFreezeCaseSensitive()
    keepCurves = publishGeoDialog.curves()
    keepSurfaces = publishGeoDialog.surfaces()
    keepAnimation = publishGeoDialog.animation()
    keepAnimatedDeformers = publishGeoDialog.animatedDeformers()
    # Prepare options
    # Freeze transform & center pivot
    if not noFreezeCaseSensitive:
        noFreeze = noFreeze.lower()
    # noFreeze contains a comma-separated list
    noFreeze = noFreeze.replace(' ','')
    noFreeze = noFreeze.split(',')

    # Progress
    progressDialog = maf.ProgressDialog()
    progressDialog.show()
    progressDialog.setText("Publishing set")

    tempData = maf.Scene.createTempScene()
    maf.Reference.importAll()
    maf.Namespace.removeAll()
    if not keepAnimation: maf.Animation.removeAll()
    
    nodes = getPublishNodes()

    if len(nodes) == 0:
        endProcess(tempData, progressDialog)
        return

    numNodes = len(nodes)
    progressDialog.setMaximum(numNodes + 2)
    progressDialog.setText("Preparing")
    progressDialog.increment()

    # Publish folder
    ram.log( "I'm publishing the sets in " + os.path.dirname( publishFileInfo.filePath() ) )

    # Publish each set (reversed because we may remove some of them)
    publishedNodes = []
    for node in reversed(nodes):
        progressDialog.setText("Publishing: " + node)
        progressDialog.increment()

        # Get children
        children = cmds.listRelatives(node, ad=True, f=True, type='transform')

        # If there's no child and just an empty group, nothing to publish
        if children is None and maf.Node.isGroup( node ):
            cmds.delete(node)
            continue
        
        # Add the node to the checks run on children
        children.append( node )

        # Move the node we're publishing to zero
        maf.Node.lockTransform( node, False, recursive=True )
        maf.Node.moveToZero( node )

        # Clean all children (reversed because we may remove some of them)
        for child in reversed(children):

            # Remove hidden
            if removeHidden and maf.Node.isHidden( child ):
                cmds.delete( child )
                continue

            typesToKeep = ()
            if not keepAnimatedDeformers and not isRamsesManaged( child ):
                typesToKeep = ['mesh']
                if not removeLocators:
                    typesToKeep.append('locator')
                if keepCurves:
                    typesToKeep.append('bezierCurve')
                    typesToKeep.append('nurbsCurve')
                if keepSurfaces:
                    typesToKeep.append('nurbsSurface')

            if not maf.Node.check( child, True, typesToKeep ):
                continue
           
            if not keepAnimatedDeformers:
                maf.Node.removeExtraShapes( child )
                if renameShapes: maf.Node.renameShapes( child )
                maf.Node.deleteHistory( child )

            freeze = True
            childName = child
            if not noFreezeCaseSensitive: childName = child.lower()
            for no in noFreeze:
                if no in childName:
                    freeze = False
                    break

            if maf.Node.isTransform( child ):
                # If this child is the root of another asset, store its PRS
                if isRamsesManaged( child ):
                    # store the current PRS on the node
                    tx = cmds.getAttr( child + '.tx' )
                    ty = cmds.getAttr( child + '.ty' )
                    tz = cmds.getAttr( child + '.tz' )
                    setRamsesAttr3( child, RamsesAttribute.ORIGIN_POS, tx, ty, tz, 'float3')
                    rx = cmds.getAttr( child + '.rx' )
                    ry = cmds.getAttr( child + '.ry' )
                    rz = cmds.getAttr( child + '.rz' )
                    setRamsesAttr3( child, RamsesAttribute.ORIGIN_ROT, rx, ry, rz, 'float3')
                    sx = cmds.getAttr( child + '.sx' )
                    sy = cmds.getAttr( child + '.sy' )
                    sz = cmds.getAttr( child + '.sz' )
                    setRamsesAttr3( child, RamsesAttribute.ORIGIN_SCA, sx, sy, sz, 'float3')
                # else freeze
                elif not keepAnimation and freeze:
                    maf.Node.freezeTransform( child )
                    maf.Node.lockTransform( child, True )

        # the main node may have been removed (if hidden or empty for example)
        if not cmds.objExists(node):
            continue

        # Remove empty groups
        maf.Node.removeEmptyGroups(node)

        # Get the node name (without any proxy prefix)
        nodeName = maf.Path.baseName(node, True)
        if nodeName.lower().startswith('proxy_'):
            nodeName = nodeName[6:]

        # Create a root controller
        r = maf.Node.createRootCtrl( node, nodeName + '_root_' + SET_PIPE_NAME )
        node = r[0]
        controller = r[1]

        publishedNodes.append(controller)

    # Clean scene:
    # Remove empty groups from the scene
    maf.Node.removeEmptyGroups()

    # Save scene
    extension = getExtension( step, SET_STEP, SET_PIPE_FILE, pipeFiles, ['ma','mb'], 'mb' )
    publishNodesAsMayaScene( publishFileInfo, publishedNodes, SET_PIPE_NAME, extension )
    
    # End and log
    endProcess(tempData, progressDialog)

    ram.log("I've published the set.")
    cmds.inViewMessage( msg="Set published!", pos='midCenterBot', fade=True)
