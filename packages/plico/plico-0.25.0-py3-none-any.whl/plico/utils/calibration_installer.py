import os
import appdirs
from pkg_resources import Requirement, resource_filename
from plico.utils.constants import Constants
from plico.utils.addtree import addtree, mkdirp




__version__= "$Id: calibration_installer.py 50 2018-04-26 21:42:20Z lbusoni $"



class CalibrationInstaller():

    def __init__(self, appDirs, packageName, src=None, dest=None):
        if src is None:
            self._sourcePath= self._getCalibPathInPackage(packageName)
        else:
            self._sourcePath= src
        if dest is None:
            self._destPath= self._getDestinationPathFromAppDirs(appDirs)
        else:
            self._destPath= dest


    def _getDestinationPathFromAppDirs(self, appDirs):
        calibFolderBaseName= 'calib'
        return os.path.join(appDirs.user_data_dir,
                            calibFolderBaseName)


    def getCalibrationFolderPath(self):
        return self._destPath


    def doesCalibrationFolderExists(self):
        return os.path.isdir(self.getCalibrationFolderPath())


    def _createCalibrationFolder(self):
        mkdirp(os.path.dirname(self.getCalibrationFolderPath()))


    def _getCalibPathInPackage(self, packageName):
        return resource_filename(Requirement(packageName),
                                 "%s/calib" % packageName)


    def installCalibrationFilesFromPackage(self):
        self._createCalibrationFolder()
        dest= self.getCalibrationFolderPath()
        addtree(self._sourcePath, dest)
