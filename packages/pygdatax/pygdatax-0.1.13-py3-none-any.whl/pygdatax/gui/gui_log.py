from silx.io.specfile import SpecFile
from silx.gui import qt
from silx.math.fit import FitManager, fittheories
from pygdatax.gui import DataView
from pygdatax.icons import getQIcon
import warnings
from matplotlib import mplDeprecation
import os
import numpy as np

CFREE = 0
CPOSITIVE = 1
CQUOTED = 2
CFIXED = 3
CFACTOR = 4
CDELTA = 5
CSUM = 6
CIGNORED = 7


def fit_distance_and_offset(x, distance, offset):
    """
    fitting function for the specular postion
    Args:
        x: goniometer position in degree
        distance: sample to detector distance
        offset: goniometer offset in degree

    Returns:

    """
    # 0.172 is the pixel size in mm
    return np.tan(2*np.deg2rad(x-offset))*distance / 0.172


def zScanLIn(x, height, z0, width):
    y = np.zeros_like(x)
    y[x < (z0 - width/2)] = height
    y[x > (z0 + width/2)] = 0
    index = np.abs(x-z0) <= width / 2
    y[index] = -height / width * (x[index]-z0) + height/2
    return y


def estimate_zScanLin(x, y):
    height = np.max(y)
    z0 = np.mean(x)
    width = np.max(x)-np.min(x)
    cons = np.zeros((3, 3))
    cons[0, 0] = CFREE
    cons[0, 1] = 0
    cons[0, 2] = 0
    cons[1, 0] = CFREE
    cons[1, 1] = 0
    cons[1, 2] = 0
    cons[2, 0] = CPOSITIVE
    cons[2, 1] = 0
    cons[2, 2] = 0
    return [height, z0, width], cons


def estimate_zScanLin(x, y):
    height = np.max(y)
    z0 = np.mean(x)
    width = np.max(x)-np.min(x)
    cons = np.zeros((3, 3))
    cons[0, 0] = CFREE
    cons[0, 1] = 0
    cons[0, 2] = 0
    cons[1, 0] = CFREE
    cons[1, 1] = 0
    cons[1, 2] = 0
    cons[2, 0] = CPOSITIVE
    cons[2, 1] = 0
    cons[2, 2] = 0
    return [height, z0, width], cons


def omScanLin(x, height, om0, width):
    y = np.zeros_like(x)
    index = np.abs(x-om0) <= width/2
    y[index] = 2*-height/width*np.abs(x[index]-om0)+height
    return y

def estimate_omScanLin(x, y):
    height = np.max(y)
    om0 = x[np.argmax(y)]
    width = np.max(x)-np.min(x)
    cons = np.zeros((3, 3))
    cons[0, 0] = CFREE
    cons[0, 1] = 0
    cons[0, 2] = 0
    cons[1, 0] = CFREE
    cons[1, 1] = 0
    cons[1, 2] = 0
    cons[2, 0] = CPOSITIVE
    cons[2, 1] = 0
    cons[2, 2] = 0
    return [height, om0, width], cons


FITMANAGER = FitManager()
FITMANAGER.loadtheories(fittheories)
FITMANAGER.addtheory("z_scan",
                     function=zScanLIn,
                     parameters=["height", "z0", "beam_width"],
                     estimate=estimate_zScanLin)

FITMANAGER.addtheory("om_scan",
                     function=omScanLin,
                     parameters=["height", "om0", "width"],
                     estimate=estimate_omScanLin)



class LogTableModel(qt.QAbstractTableModel):

    def __init__(self):
        super(LogTableModel, self).__init__()
        self._data = None
        self._specfile = None
        self._motorDict = {}
        self._columnHeaders = ['motor', 'start', 'stop', 'interval', 'time','date']

    def data(self, index, role):
        if not self._specfile:
            return
        if role == qt.Qt.DisplayRole:
            if index.column() < 5:
                command = self._data.command(index.row()).split()
                return command[index.column()+1]
            else:
                scanDate = self._data[index.row()].scan_header_dict['D']
                return scanDate

    def columnCount(self, index):
        # command = self._data.command(index.row()).split()
        return len(self._columnHeaders)

    def rowCount(self, index):
        if self._data:
            return len(self._data.keys())
        else:
            return 1

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == qt.Qt.DisplayRole:
            if orientation == qt.Qt.Horizontal:
                return str(self._columnHeaders[section])

            if orientation == qt.Qt.Vertical:
                if self._data:
                    return str(self._data.number(section))

    def loadSpecFile(self, specfile):
        self.layoutAboutToBeChanged.emit()
        self._data = SpecFile(specfile)
        self._specfile = specfile
        self._motorDict = {}
        motor_keys = []
        motor_names = []
        header = self._data.file_header()
        for i in [4, 5, 6]:
            key_line = header[i]
            name_line = header[i + 3]
            motor_keys += key_line.split()[1:]
            motor_names += name_line.split()[1:]
        for key, name in zip(motor_keys, motor_names):
            self._motorDict[key] = name
        self.layoutChanged.emit()

    def refreshSpecFile(self):
        if self._specfile:
            self.layoutAboutToBeChanged.emit()
            self._data = SpecFile(self._specfile)
            self.layoutChanged.emit()

    def getScan(self, index):
        scan_dict = {}
        if self._data:
            scan = self._data[index.row()]
            scan_dict['motor_name'] = self._motorDict[self._data[index.row()].labels[0]]
            scan_dict['command'] = self._data.command(index.row())
            try:
                scan_dict['x'] = scan.data[0]
                scan_dict['roi0'] = scan.data_column_by_name('Pil Roi0')
                scan_dict['ct0'] = scan.data_column_by_name('Pil Ct0')
            except IndexError:
                scan_dict = {}
        return scan_dict


class LogMainWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pygdatax scans log")
        self.setWindowIcon(getQIcon('logo_llb.ico'))
        logfile = '/home/achennev/Documents/xeuss/logfiles/log.log'
        # table
        self.table = qt.QTableView()
        self.table.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.model = LogTableModel()
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(qt.QHeaderView.ResizeToContents)
        # pick log file
        self.fileLineEdit = qt.QLineEdit(parent=self)
        self.filePickerButton = qt.QPushButton()
        self.filePickerButton.setIcon(getQIcon('directory.ico'))
        self.filePickerButton.setToolTip('open log file')
        self.refreshButton = qt.QPushButton()
        self.refreshButton.setIcon(getQIcon('refresh.ico'))
        self.refreshButton.setToolTip('refresh log file')
        # data viewer
        self.plotWindow = DataView(fitmanager=FITMANAGER)


        # layout
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(qt.QLabel('log file :'))
        hlayout.addWidget(self.fileLineEdit)
        hlayout.addWidget(self.filePickerButton)
        hlayout.addWidget(self.refreshButton)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.table)
        layout = qt.QHBoxLayout()
        layout.addLayout(vlayout)
        layout.addWidget(self.plotWindow)
        self.setLayout(layout)

        # connect signal
        self.fileLineEdit.textChanged.connect(self.set_logfile)
        self.filePickerButton.clicked.connect(self.choose_logfile)
        self.refreshButton.clicked.connect(self.refresh)
        selectionModel = self.table.selectionModel()
        selectionModel.selectionChanged.connect(self.plot_scan)
        # self.table.currentChanged.connect(self.plot_scan)
    
    def set_logfile(self):
        text = self.fileLineEdit.text()
        if text.endswith('.log') and os.path.exists(text):
            self.model.loadSpecFile(text)

    def choose_logfile(self):
        basedir = os.path.expanduser("~")
        fname = qt.QFileDialog.getOpenFileName(self, 'Select log file', basedir,
                                               options=qt.QFileDialog.DontUseNativeDialog)
        if fname:
            self.fileLineEdit.setText(fname[0])

    def refresh(self):
        self.model.refreshSpecFile()

    def plot_scan(self, new_item, prev_item):
        indexes = self.table.selectedIndexes()
        self.plotWindow.clear()
        self.plotWindow.setGraphYLabel('counts')
        for index in indexes:
            scan_dict = self.model.getScan(index)
            if scan_dict:
                command = scan_dict['command']
                x = scan_dict['x']
                roi0 = scan_dict['roi0']
                ct0 = scan_dict['ct0']
                self.plotWindow.setGraphXLabel(scan_dict['motor_name'])
                self.plotWindow.addCurve(x, roi0, legend='roi0 ' + '#S' + str(index.row()+1))
                self.plotWindow.addCurve(x, ct0, legend='ct0 ' + '#S' + str(index.row()+1))


def main():
    import sys
    # unlock hdf5 files for file access during plotting
    os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
    warnings.filterwarnings("ignore", category=mplDeprecation)
    app = qt.QApplication([])
    # sys.excepthook = qt.exceptionHandler
    window = LogMainWindow()
    window.show()
    result = app.exec_()
    # remove ending warnings relative to QTimer
    app.deleteLater()
    sys.exit(result)



if __name__ == '__main__':
    main()



if __name__ == '__main__':
    main()



