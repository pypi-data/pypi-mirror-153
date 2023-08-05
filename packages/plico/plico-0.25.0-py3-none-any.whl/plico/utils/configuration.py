#!/usr/bin/env python

import os
import re
import configparser
import appdirs
from pkg_resources import resource_filename
from plico.utils.calibration_installer import CalibrationInstaller
from plico.utils.addtree import mkdirp


__version__= "$Id: configuration.py 50 2018-04-26 21:42:20Z lbusoni $"


class LogFolderManager():

    def __init__(self, appDirs):
        self._appdirs= appDirs


    def getLogFolderPath(self):
        return self._appdirs.user_log_dir


    def doesLogFolderExists(self):
        return os.path.isdir(self.getLogFolderPath())


    def createLogFolder(self):
        mkdirp(os.path.dirname(self.getLogFolderPath()))


class Configuration(object):


    def __init__(self):
        NOT_INITIALIZED= None
        self._cfg = configparser.ConfigParser()


    def networkHostName(self, section):
        return self.getValue(section, 'host')


    def calibrationRootDir(self):
        return self._getCalibDir()


    def loggingDir(self):
        return self._getLogDir()


    def deviceModel(self, section):
        return self.getValue(section, 'model')


    def deviceName(self, section):
        return self.getValue(section, 'name')


    def basePort(self, section):
        return self.getValue(section, 'port', getint=True)


    def logLevel(self, section):
        return self.getValue(section, 'log_level')


    def numberedSectionList(self, prefix=''):
        pattern = prefix+'\\d+'
        return list(filter(lambda x: re.search(pattern, x), self._cfg.sections()))


    def _assertSectionExists(self, section):
        if section not in self._cfg.sections():
            raise Exception('Section "%s" not found in configuration file' %
                            section)


    def getValue(self, section, entry, getint=False,
                 getfloat=False, getboolean=False):
        if entry not in list(dict(self._cfg.items(section)).keys()):
            raise KeyError(
                'Section "%s" must contain a "%s" entry. File is %s. Keys %s' %
                (section, entry, self._filename,
                 list(dict(self._cfg.items(section)).keys())))
        if getint:
            try:
                value = self._cfg.getint(section, entry)
            except ValueError:
                raise ValueError(
                    'Value for entry "%s" in section "%s"'
                    ' must be an integer number' % (entry, section))
        elif getfloat:
            try:
                value = self._cfg.getfloat(section, entry)
            except ValueError:
                raise ValueError(
                    'Value for entry "%s" in section "%s"'
                    ' must be a float number' % (entry, section))
        elif getboolean:
            try:
                value = self._cfg.getboolean(section, entry)
            except ValueError:
                raise ValueError(
                    'Value for entry "%s" in section "%s"'
                    ' must be a boolean' % (entry, section))
        else:
            value = self._cfg.get(section, entry)
        return value


    def load(self, filename):
        if not os.path.exists(filename):
            raise Exception('Configuration file not found: %s' % filename)
        self._cfg.read(filename)
        self._filename= filename


    def _getLogDir(self):
        try:
            return self.getValue('global', 'force_log_dir')
        except Exception:
            lfm= LogFolderManager(self._getAppDirs())
            lfm.createLogFolder()
            return lfm.getLogFolderPath()


    def _getCalibDir(self):
        try:
            return self.getValue('global', 'force_calib_folder_dest')
        except Exception:
            calibInst= CalibrationInstaller(
                self._getAppDirs(), self._getPythonPackageName())
            calibInst.installCalibrationFilesFromPackage()
            return calibInst.getCalibrationFolderPath()


    def _getPythonPackageName(self):
            return self.getValue('global', 'python_package_name')


    def _getAppName(self):
            return self.getValue('global', 'app_name')


    def _getAppAuthor(self):
            return self.getValue('global', 'app_author')


    def _getAppDirs(self):
        return appdirs.AppDirs(self._getAppName(),
                               self._getAppAuthor())
