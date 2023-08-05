import os

__version__= "$Id: fits_file_based_calibration_manager.py 25 2018-01-26 19:00:40Z lbusoni $"


class FitsFileBasedCalibrationManager(object):
    def _createFoldersIfMissing(self, filename):
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
