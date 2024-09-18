# -*- coding: utf-8 -*-
"""User interface tools"""

import sys
import os

try:
    from PySide2 import QtWidgets as qw
    from PySide2 import QtGui as qg
    from PySide2 import QtCore as qc
except:  # pylint: disable=bare-except
    from PySide6 import QtWidgets as qw
    from PySide6 import QtGui as qg
    from PySide6 import QtCore as qc

from dumaf.utils import getModulePath
from dumaf.rendering import get_ortho_cameras, get_persp_cameras, get_renderable_cameras
from dumaf.paths import baseName

ICON_PATH = getModulePath() + "/icons/"

def getMayaWindow():
    """Returns the Maya QMainWindow"""
    app = qw.QApplication.instance() #get the qApp instance if it exists.
    if not app:
        app = qw.QApplication(sys.argv)

    try:
        mayaWin = next(w for w in app.topLevelWidgets() if w.objectName()=='MayaWindow')
        return mayaWin
    except: # pylint: disable=bare-except
        return None

def update_cam_combobox(combobox):
    """Sets the list of cameras in the scene in a QComboBox"""
    combobox.clear()

    renderableCameras = get_renderable_cameras()
    perspCameras =  get_persp_cameras()
    orthoCameras = get_ortho_cameras()

    numRenderCam = len(renderableCameras)
    if numRenderCam > 0:
        for camera in renderableCameras:
            cameraName = baseName(camera)
            combobox.addItem( cameraName, camera)
        combobox.insertSeparator( numRenderCam )

    numPerspCam = len( perspCameras )
    if numPerspCam > 0:
        for camera in perspCameras:
            cameraName = baseName(camera)
            combobox.addItem( cameraName, camera)
        combobox.insertSeparator( numRenderCam+numPerspCam+1 )

    for camera in orthoCameras:
        cameraName = baseName(camera)
        combobox.addItem( cameraName, camera)

def icon(name):
    """Gets qg.QIcon for an icon from its name (without extension)"""
    if os.path.isfile( ICON_PATH + name + ".png" ):
        return qg.QIcon( ICON_PATH + name + ".png" )
    else:
        return qg.QIcon( ICON_PATH + name + ".svg" )

class UpdateDialog( qw.QDialog ):
    """The dialog to show details about an update"""

    def __init__(self, updateInfo, toolName, toolVersion, parent=None):
        if not parent:
            parent=getMayaWindow()
        super(UpdateDialog, self).__init__(parent)
        self.__setupUi(updateInfo, toolName, toolVersion)

    def __setupUi(self, updateInfo, toolName, toolVersion):
        self.setModal(True)

        mainLayout = qw.QVBoxLayout()
        mainLayout.setSpacing(3)
        self.setLayout(mainLayout)

        if updateInfo.get("update", False):
            self.setWindowTitle("New " + toolName + " available!" )

            latestVersionLabel = qw.QLabel("version: " + updateInfo.get("version") )
            mainLayout.addWidget(latestVersionLabel)

            descriptionEdit = qw.QTextEdit()
            descriptionEdit.setMarkdown(updateInfo.get("description"))
            descriptionEdit.setReadOnly(True)
            mainLayout.addWidget(descriptionEdit)

            currentVersionLabel = qw.QLabel("Current version: " + toolVersion )
            currentVersionLabel.setEnabled(False)
            mainLayout.addWidget(currentVersionLabel)

            self.__downloadURL = updateInfo.get("downloadURL", "")
            if self.__downloadURL != "":
                self.__ui_downloadButton = qw.QPushButton("Download")
                self.__ui_downloadButton.setIcon(icon("download"))
                mainLayout.addWidget(self.__ui_downloadButton)
                self.__ui_downloadButton.clicked.connect(self.download)

            self.__changelogURL = updateInfo.get("changelogURL", "")
            if self.__changelogURL != "":
                self.__ui_changelogButton = qw.QPushButton("Changelog")
                self.__ui_changelogButton.setIcon(icon("changelog"))
                mainLayout.addWidget(self.__ui_changelogButton)
                self.__ui_changelogButton.clicked.connect(self.changelog)

            self.__donateURL = updateInfo.get("donateURL", "")
            if self.__donateURL != "":
                self.__ui_donateButton = qw.QPushButton("I ♥ " + toolName)
                self.__ui_donateButton.setIcon(icon("donate"))
                mainLayout.addWidget(self.__ui_donateButton)
                self.__ui_donateButton.clicked.connect(self.donate)

            self.__ui_okButton = qw.QPushButton("Close")
            self.__ui_okButton.setIcon(icon("close"))
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        elif updateInfo.get("accepted", False):
            self.setWindowTitle( "Update" )

            versionLabel = qw.QLabel("I'm already up-to-date!" )
            mainLayout.addWidget(versionLabel)

            self.__ui_okButton = qw.QPushButton("Close")
            self.__ui_okButton.setIcon(icon("close"))
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        elif updateInfo.get("success", False):
            self.setWindowTitle( "Server error" )
            label = qw.QLabel("Sorry, the server could not get update information." )
            mainLayout.addWidget(label)

            descriptionEdit = qw.QTextEdit(updateInfo.get("description", ""))
            descriptionEdit.setReadOnly(True)
            mainLayout.addWidget(descriptionEdit)

            self.__ui_okButton = qw.QPushButton("Close")
            self.__ui_okButton.setIcon(icon("close"))
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        else:
            self.setWindowTitle( "Server error" )
            label = qw.QLabel("Sorry, there was a server error." )
            mainLayout.addWidget(label)

            self.__ui_okButton = qw.QPushButton("Close")
            self.__ui_okButton.setIcon(icon("close"))
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)

    @qc.Slot()
    def download(self):
        """Opens the download URL"""
        qg.QDesktopServices.openUrl ( qc.QUrl( self.__downloadURL ) )
        self.close()

    @qc.Slot()
    def changelog(self):
        """Opens the changelog URL"""
        qg.QDesktopServices.openUrl ( qc.QUrl( self.__changelogURL ) )
        self.close()

    @qc.Slot()
    def donate(self):
        """Opens the donate URL"""
        qg.QDesktopServices.openUrl ( qc.QUrl( self.__donateURL ) )
        self.close()
