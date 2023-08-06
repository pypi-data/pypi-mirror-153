from silx.gui import qt, hdf5
from silx.math.fit import fittheories
from silx.math.fit import FitManager, FitTheory
from silx.gui.plot.items.roi import RectangleROI, CrossROI
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser
from pygdatax.icons import getQIcon
import os
from pathlib import Path
import fabio
from pygdatax import nxlib, gui
from pygdatax.instruments import xeussrx
from numpy import tan, deg2rad


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
    return tan(2*deg2rad(x-offset))*distance / 0.172

FITMANAGER = FitManager()
FITMANAGER.loadtheories(fittheories)
FITMANAGER.addtheory("specular position",
                     function=fit_distance_and_offset,
                     parameters=["distance", "offset"])





def get_edf_rx_description(filepath):
    des = []
    if os.path.isfile(filepath):
        if filepath.endswith('.edf'):
            dataObj = fabio.open(filepath)
            try:
                des.append(os.path.basename(filepath))
                des.append(dataObj.header['Comment'])
                des.append(dataObj.header['om'])
                des.append(dataObj.header['count_time'])
            except KeyError:
                des.append(os.path.split(filepath[1]))
                des += 3 * ['']
    return des


class EdfRxFileTable(qt.QTableWidget):
    directory = ''
    file_extension = '.edf'
    fileSelectedChanged = qt.pyqtSignal(str)
    directBeamFile = None

    def __init__(self, parent=None):
        super(EdfRxFileTable, self).__init__(parent=parent)
        self.setColumnCount(4)
        self.setRowCount(4)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.setSelectionMode(qt.QAbstractItemView.SingleSelection)
        self.setHorizontalHeaderLabels(['File', 'comment', 'om (deg))', 'counting time'])
        self.currentItemChanged.connect(self.on_selectionChanged)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)

    def setDirectory(self, directory):
        folderPath = Path(directory)
        if folderPath.is_dir():
            self.directory = folderPath
            self.refresh()

    def refresh(self):
        self.currentItemChanged.disconnect()
        if os.path.isdir(self.directory):
            l = os.listdir(self.directory)
            # l.sort()
            fileList = []
            for item in l:
                if item.endswith(self.file_extension):
                    fileList.append(item)
            # self.clearContents()
            self.setRowCount(len(fileList))
            for i, file in enumerate(fileList):
                description = get_edf_rx_description(os.path.join(self.directory, file))
                for j, des in enumerate(description):
                    item = qt.QTableWidgetItem(des)
                    item.setFlags(qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled)
                    self.setItem(i, j, item)
                # check of the file was current set to parametric file
                filepath = os.path.join(self.directory, file)
                if filepath == self.directBeamFile:
                    self.set_row_bkg(i, qt.QColor("red"))
                    self.item(i, 0).setIcon(getQIcon('beam.ico'))

        self.sortItems(0, qt.Qt.AscendingOrder)
        self.currentItemChanged.connect(self.on_selectionChanged)

    def on_selectionChanged(self):
        row = self.currentRow()
        file = self.item(row, 0).text()
        self.fileSelectedChanged.emit(os.path.join(self.directory, file))

    def generateMenu(self, event):
        current_item = self.itemAt(event)
        # current_item = self.selectedItems()
        menu = qt.QMenu()
        directBeamAction = qt.QAction(getQIcon('beam.ico'), 'direct beam')
        directBeamAction.triggered.connect(self._set_direct_beam)
        sampleAction = qt.QAction('sample')
        sampleAction.triggered.connect(self._set_sample)
        # maskAction = qt.QAction(getQIcon('mask.ico'), 'mask')
        # maskAction.triggered.connect(self._set_mask)
        # build menu
        menu.addAction(directBeamAction)
        menu.addAction(sampleAction)
        # menu.addAction(maskAction)
        action = menu.exec_(self.mapToGlobal(event))

    def set_row_bkg(self, row, color):
        for i in range(self.columnCount()):
            item = self.item(row, i)
            item.setBackground(color)

    def _set_sample(self):
        for current_item in self.selectedItems():
            if current_item is not None:
                row = current_item.row()
                ncol = self.columnCount()
                first_col_item = self.item(row, 0)
                file = first_col_item.text()
                self.set_row_bkg(row, qt.QColor("white"))
                first_col_item.setIcon(qt.QIcon())
                fullfile = os.path.join(self.directory, file)
                # remove double reference
                if fullfile == self.directBeamFile:
                    self.directBeamFile = None
                # elif fullfile == self.maskFile:
                #     self.maskFile = None

    def _set_direct_beam(self):
        current_item = self.currentItem()
        if current_item is not None:
            current_eb_item = self.findItems(os.path.basename(str(self.directBeamFile)), qt.Qt.MatchExactly)
            # remove the previous empty cell icons
            if current_eb_item:
                self.set_row_bkg(current_eb_item[0].row(), qt.QColor("white"))
                filepath = os.path.join(self.directory, current_eb_item[0].text())
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            self.set_row_bkg(row, qt.QColor("red"))
            first_col_item.setIcon(getQIcon('beam.ico'))
            # remove double reference
            fullfile = os.path.join(self.directory, file)
            self.directBeamFile = fullfile
            # if fullfile == self.maskFile:
            #     self.maskFile = None

    def get_sample_files(self):
        sampleList = []
        nRow = self.rowCount()
        for i in range(nRow):
            first_col_item = self.item(i, 0)
            file = first_col_item.text()
            # remove double reference
            fullfile = os.path.join(self.directory, file)
            if fullfile != self.directBeamFile:
                sampleList.append(fullfile)
        return sampleList, self.directBeamFile


class EdfRxTreatmentWidget(qt.QWidget):
    fileSelectedChanged = qt.pyqtSignal(str, list)
    treatementClicked = qt.pyqtSignal()
    treatementPerformed = qt.pyqtSignal()
    roiChanged = qt.pyqtSignal(list)

    def __init__(self, parent=None):
        super(EdfRxTreatmentWidget, self).__init__(parent=parent)
        # directory selector
        self.directoryLineEdit = qt.QLineEdit(parent=self)
        self.directoryPickerButton = qt.QPushButton()
        self.directoryPickerButton.setIcon(getQIcon('directory.ico'))
        self.refreshButton = qt.QPushButton()
        self.refreshButton.setIcon(getQIcon('refresh.ico'))
        # file table
        self.table = EdfRxFileTable(parent=self)
        # beam center coordinates
        self.x0LineEdit = qt.QLineEdit('566')
        self.y0LineEdit = qt.QLineEdit('906')
        # sample to detector distance
        self.distanceLineEdit = qt.QLineEdit('1214')
        # define the angular offset in deg
        self.offsetLineEdit = qt.QLineEdit('0')
        # roi dimension
        self.roiWidthLineEdit = qt.QLineEdit('40')
        self.roiWidthLineEdit.setValidator(qt.QIntValidator())
        self.roiHeightLineEdit = qt.QLineEdit('20')
        self.roiHeightLineEdit.setValidator(qt.QIntValidator())

        # button to treat data
        self.treatButton = qt.QPushButton('treat')
        self.treatButton.setIcon(getQIcon('gear.ico'))
        self.treatButton.setToolTip('Compute reflectivity spectra')
        # parameter form layout
        formLayout = qt.QFormLayout()
        formLayout.addRow('x0 (pixels):', self.x0LineEdit)
        formLayout.addRow('y0 (pixels):', self.y0LineEdit)
        formLayout.addRow('distance (mm):', self.distanceLineEdit)
        formLayout.addRow('offset (°) :', self.offsetLineEdit)
        formLayout.addRow('roi width (pixels):', self.roiWidthLineEdit)
        formLayout.addRow('roi height (pixels):', self.roiHeightLineEdit)
        # general layout
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(qt.QLabel('directory :'))
        hlayout.addWidget(self.directoryLineEdit)
        hlayout.addWidget(self.directoryPickerButton)
        hlayout.addWidget(self.refreshButton)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addLayout(formLayout)
        vlayout.addWidget(self.table)
        vlayout.addWidget(self.treatButton)
        self.setLayout(vlayout)
        # connect signals
        self.directoryLineEdit.textChanged.connect(self.set_directory)
        self.directoryPickerButton.clicked.connect(self.choose_directory)
        self.table.fileSelectedChanged.connect(self.on_selectionChanged)
        self.treatButton.clicked.connect(self.treat)
        # parameter signal
        self.x0LineEdit.textEdited.connect(self.on_parameters_changed)
        self.y0LineEdit.textEdited.connect(self.on_parameters_changed)
        self.distanceLineEdit.textChanged.connect(self.on_parameters_changed)
        self.offsetLineEdit.textChanged.connect(self.on_parameters_changed)
        self.roiWidthLineEdit.textChanged.connect(self.on_parameters_changed)
        self.roiHeightLineEdit.textChanged.connect(self.on_parameters_changed)

    def on_parameters_changed(self):
        row = self.table.currentRow()
        if row >=0:
            params = self.get_parameters()
            file = self.table.item(row, 0).text()
            path = os.path.join(self.table.directory, file)
            if path == self.table.directBeamFile:
                omega = 0
                offset = 0
            else:
                omega = float(self.table.item(row, 2).text())
                offset = params['offset']
            # building roi
            try:
                x1 = params['x0'] - params['roi_width'] / 2
                x2 = params['x0'] + params['roi_width'] / 2
                y1 = params['y0'] - params['roi_height'] / 2
                y2 = params['y0'] + params['roi_height'] / 2
                disp = tan(2 * deg2rad(omega - offset)) * params['distance'] / 0.172
                y1 -= disp
                y2 -= disp
                roi = [x1, y1, x2, y2]
            except TypeError:
                roi = 4 * [None]
            self.roiChanged.emit(roi)

    def treat(self):
        # msg = qt.QMessageBox()
        # msg.setIcon(qt.QMessageBox.Information)
        # msg.setText("treatment running")
        # msg.setStandardButtons(qt.QMessageBox.NoButton)
        # msg.setWindowModality(qt.Qt.NonModal)
        # msg.show()
        self.treatementClicked.emit()
        try:
            x0 = float(self.x0LineEdit.text())
        except ValueError:
            x0 = None
        try:
            y0 = float(self.y0LineEdit.text())
        except ValueError:
            y0 = None
        try:
            offset = float(self.offsetLineEdit.text())
        except ValueError:
            offset = 0
        try:
            distance = float(self.distanceLineEdit.text())
        except ValueError:
            distance = None
        try:
            roi_width = float(self.roiWidthLineEdit.text())
        except ValueError:
            roi_width = None
        try:
            roi_height = float(self.roiHeightLineEdit.text())
        except ValueError:
            roi_height = None

        fileList, directBeamFile = self.table.get_sample_files()
        outputFolder = os.path.abspath(os.path.join(self.table.directory, os.pardir))
        outputFilename = os.path.relpath(self.table.directory, start=outputFolder) + '.nxs'
        outputFullPath = os.path.join(outputFolder, outputFilename)
        nxlib.build_rxnexus_from_edf(fileList, directBeamFile, outputFullPath,
                                     offset=offset)
        xeussrx.set_center(outputFullPath, x0=x0, y0=y0)
        xeussrx.set_roi(outputFullPath, roi_width=roi_width, roi_height=roi_height)
        xeussrx.set_distance(outputFullPath, distance=distance)
        # offset is already set
        xeussrx.compute_ref(outputFullPath)

    def set_directory(self):
        text = self.directoryLineEdit.text()
        self.table.setDirectory(text)
        # if os.path.exists(text):
        #     os.chdir(text)

    def choose_directory(self):
        # if self.table.directory:
        #     if os.path.exists(self.table.directory):
        #         basedir = self.table.directory
        #     else:
        #         basedir = os.path.expanduser("~")
        # else:

        basedir = os.path.expanduser("~")
        fname = qt.QFileDialog.getExistingDirectory(self, 'Select data directory', directory=basedir,
                                                    options=qt.QFileDialog.DontUseNativeDialog)
        if fname:
            self.directoryLineEdit.setText(fname)
            # self.edfTab.table.setDirectory(fname)
            # self.nxsTab.setDirectory(fname)

    def on_selectionChanged(self):
        row = self.table.currentRow()
        if row >= 0:
            params = self.get_parameters()
            file = self.table.item(row, 0).text()
            path = os.path.join(self.table.directory, file)
            if path == self.table.directBeamFile:
                omega = 0
                offset = 0
            else:
                omega = float(self.table.item(row, 2).text())
                offset = params['offset']
            # building roi
            try:
                x1 = params['x0'] - params['roi_width']/2

                x2 = params['x0'] + params['roi_width'] / 2
                y1 = params['y0'] - params['roi_height'] / 2
                y2 = params['y0'] + params['roi_height'] / 2
                disp = tan(2*deg2rad(omega-offset))*params['distance'] / 0.172
                y1 -= disp
                y2 -= disp
                roi = [x1, y1, x2, y2]
            except TypeError:
                roi = 4*[None]
            self.fileSelectedChanged.emit(path, roi)

    def get_parameters(self):
        params = {}
        try:
            params['x0'] = float(self.x0LineEdit.text())
        except ValueError:
            params['x0'] = None
        try:
            params['y0'] = float(self.y0LineEdit.text())
        except ValueError:
            params['y0'] = None
        try:
            params['offset'] = float(self.offsetLineEdit.text())
        except ValueError:
            params['offset'] = 0
        try:
            params['distance'] = float(self.distanceLineEdit.text())
        except ValueError:
            params['distance'] = None
        try:
            params['roi_width'] = float(self.roiWidthLineEdit.text())
        except ValueError:
            params['roi_width'] = None
        try:
            params['roi_height'] = float(self.roiHeightLineEdit.text())
        except ValueError:
            params['roi_height'] = None

        return params


class EdfViewerRX(gui.DataView):

    def __init__(self):
        super(EdfViewerRX, self).__init__(fitmanager=None)

    def displayEdf(self, file):
        dataObj = fabio.open(file)
        data = dataObj.data
        self.addImage(data)

    def displayRoi(self, roi):
        # display roi of interation
        if roi == 4 * [None]:
            return
        self.roiManager.disconnect()
        roisList = self.roiManager.getRois()
        for r in roisList:
            # if not isinstance(r, CrossROI):
            self.roiManager.removeRoi(r)
        currentRoi = RectangleROI()
        currentRoi.setGeometry(origin=[roi[0], roi[1]], size=[roi[2] - roi[0], roi[3] - roi[1]])
        self.roiManager.addRoi(currentRoi)
        self.roiManager.sigRoiAdded.connect(self.updateAddedRegionOfInterest)


class NexusRXTreeWidget(qt.QWidget):
    operationPerformed = qt.pyqtSignal()
    selectedNodeChanged = qt.pyqtSignal(list)

    def __init__(self):
        super(NexusRXTreeWidget, self).__init__()
        """Silx HDF5 TreeView"""
        self.treeview = hdf5.Hdf5TreeView(self)
        treemodel = hdf5.Hdf5TreeModel(self.treeview,
                                       ownFiles=True
                                       )
        # treemodel.sigH5pyObjectLoaded.connect(self.__h5FileLoaded)
        # treemodel.sigH5pyObjectRemoved.connect(self.__h5FileRemoved)
        # treemodel.sigH5pyObjectSynchronized.connect(self.__h5FileSynchonized)
        treemodel.setDatasetDragEnabled(False)
        # self.treeview.setModel(treemodel)
        self.__treeModelSorted = gui.hdf5.NexusSortFilterProxyModel(self.treeview)
        self.__treeModelSorted.setSourceModel(treemodel)
        self.__treeModelSorted.sort(0, qt.Qt.AscendingOrder)
        self.__treeModelSorted.setSortCaseSensitivity(qt.Qt.CaseInsensitive)
        self.treeview.setModel(self.__treeModelSorted)
        self.treeview.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        # layout
        # hlayout.addWidget(self.sync_btn)
        vlayout = qt.QVBoxLayout()
        vlayout.addWidget(self.treeview)
        self.setLayout(vlayout)

        # connect signals
        # self.sync_btn.clicked.connect(self.sync_all)
        self.treeview.selectionModel().selectionChanged.connect(self.on_tree_selection)

    def load_files(self, files):
        model = self.treeview.findHdf5TreeModel()
        model.clear()
        for file in files:
            model.insertFile(file, row=-1)
        self.treeview.expandToDepth(0)

    def sync_all(self):
        model = self.treeview.findHdf5TreeModel()
        nrow = model.rowCount()

        for n in range(nrow):
            index = model.index(n, 0, qt.QModelIndex())
            node = model.nodeFromIndex(index)
            filename = node.obj.filename
            model.removeH5pyObject(node.obj)
            model.insertFile(filename, row=n)
        self.treeview.expandToDepth(0)
        self.operationPerformed.emit()

    def on_tree_selection(self):
        selected = list(self.treeview.selectedH5Nodes())
        self.selectedNodeChanged.emit(selected)


class NexusRxViewer(gui.DataView):

    def __init__(self, parent=None):
        super(NexusRxViewer, self).__init__(fitmanager=FITMANAGER)
        self._browser_label = qt.QLabel("image index :")
        central_widget = self.centralWidget()
        self._browser = HorizontalSliderWithBrowser(self)
        layout = central_widget.layout()
        layout.addWidget(self._browser)
        central_widget.setLayout(layout)
        self._browser.hide()
        self.stack = None

    def displayStack(self, nxstack):
        shape = nxstack.shape
        self.stack = nxstack
        self._browser.setMinimum(0)
        self._browser.setMaximum(shape[2])
        self._browser.setValue(0)
        self._browser.show()
        self.addImage(nxstack.nxsignal[:, :, 0])


class XeussRxMainWindow(qt.QMainWindow):
    """
    This window show an example of use of a Hdf5TreeView.

    The tree is initialized with a list of filenames. A panel allow to play
    with internal property configuration of the widget, and a text screen
    allow to display events.
    """

    def __init__(self):
        super(XeussRxMainWindow, self).__init__()
        self.plotWindow = EdfViewerRX()
        self.edfWidget = EdfRxTreatmentWidget(parent=self)
        # self.nxsWidget = gui.NexusFileTable(parent=self)

        layout = qt.QHBoxLayout()
        layout.addWidget(self.edfWidget)
        layout.addWidget(self.plotWindow)
        main_panel = qt.QWidget(self)
        main_panel.setLayout(layout)
        self.setCentralWidget(main_panel)
        # self.setLayout(layout)
        # connect signals
        self.edfWidget.fileSelectedChanged.connect(self.plot)
        self.edfWidget.roiChanged.connect(self.plotWindow.displayRoi)

    def plot(self, file, roi):
        self.plotWindow.displayEdf(file)
        self.plotWindow.displayRoi(roi)


def main():
    # unlock hdf5 files for file access during plotting
    os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
    # warnings.filterwarnings("ignore", category=mplDeprecation)
    app = qt.QApplication([])
    # sys.excepthook = qt.exceptionHandler
    window = XeussRxMainWindow()
    window.show()
    result = app.exec_()
    # remove ending warnings relative to QTimer
    app.deleteLater()
    sys.exit(result)



if __name__ == '__main__':
    import sys
    import pygdatax.gui
    from silx.math.fit import FitManager
    from silx.gui.fit import FitWidget
    import nexusformat.nexus as nx
    from silx.math.fit import FitManager, FitTheory, fittheories

    def linearfun(x, a, b):
        return a * x + b


    app = qt.QApplication([])
    # w = EdfRxTreatmentWidget()
    # w.directoryLineEdit.setText('/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/TH1_10_1000_pos1')
    w = XeussRxMainWindow()
    w.edfWidget.directoryLineEdit.setText('/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/TH1_10_1000_pos1')
    # w = EdfViewerRX()
    # w = NexusRxViewer()
    w.show()
    result = app.exec_()
    app.deleteLater()
    sys.exit(result)
