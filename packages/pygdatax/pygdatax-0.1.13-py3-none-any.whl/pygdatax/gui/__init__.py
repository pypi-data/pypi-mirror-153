import sys
import os
import shutil
import warnings

from matplotlib import mplDeprecation
import numpy as np
import fabio
import silx.gui.hdf5
from silx.gui import qt, colors
from silx.gui.plot import PlotWindow, Profile, PlotWidget
from silx .gui.plot.tools.roi import RegionOfInterestManager
from silx.gui.plot.items.roi import RectangleROI, CrossROI, VerticalLineROI
from silx.gui.plot.actions.fit import FitAction
from silx.gui.fit import FitWidget
from silx.math.fit import FitManager, fittheories
import silx.io as sio
from silx.io.utils import is_group, is_dataset, is_file
from silx.io.nxdata import is_NXroot_with_default_NXdata, get_default
import nexusformat.nexus as nx
from numpy.random import randint
from scipy.ndimage.measurements import center_of_mass
from pathlib import Path
import yaml
from pygdatax.icons import getQIcon
from pygdatax import nxlib, moduledescription
from pygdatax.instruments import xeuss
from silx.gui.widgets.WaitingPushButton import WaitingPushButton


def get_edf_description(edf_filepath):
    des = []
    if os.path.isfile(edf_filepath):
        if edf_filepath.endswith('.edf'):
            dataObj = fabio.open(edf_filepath)
            try:
                des.append(os.path.basename(edf_filepath))
                des.append(dataObj.header['Comment'])
                des.append(str(1.5))
                des.append(dataObj.header['pilroi1'])
                distance = float(dataObj.header['SampleDistance'])
                # convert to mm
                distance *= 1000.0
                des.append(str(distance))
                des.append(dataObj.header['count_time'])
                des.append(dataObj.header['Date'])
            except KeyError:
                des.append(os.path.split(edf_filepath)[1])
                des += 5 * ['']
    return des


def get_nxs_description(nxs_filepath):
    if os.path.isfile(nxs_filepath):
        if nxs_filepath.endswith('.nxs'):
            try:
                des = []
                root = nx.nxload(nxs_filepath, mode='r')
                entry = root[nxlib.get_last_entry_key(root)]
                des.append(os.path.basename(nxs_filepath))
                des.append(str(entry.sample.sample_name.nxdata.decode()))
                des.append(str(str(entry.sample.thickness.nxdata)))
                des.append(str(entry.sample.transmission.nxdata))
                des.append(str(entry.instrument.detector.distance.nxdata))
                des.append(str(entry.sample.count_time.nxdata))
                des.append(root.attrs['file_time'])
                root.close()
            except (KeyError, nx.NeXusError, ValueError):
                des = []
                des.append(os.path.split(nxs_filepath)[1])
                des += 5 * ['']
            # compatibility with windows
            except AttributeError:
                des = []
                root = nx.nxload(nxs_filepath, mode='r')
                entry = root[nxlib.get_last_entry_key(root)]
                des.append(os.path.basename(nxs_filepath))
                des.append(str(entry.sample.sample_name.nxdata))
                des.append(str(str(entry.sample.thickness.nxdata)))
                des.append(str(entry.sample.transmission.nxdata))
                des.append(str(entry.instrument.detector.distance.nxdata))
                des.append(str(entry.sample.count_time.nxdata))
                des.append(root.attrs['file_time'])
                root.close()
    return des


class EdfFileTable(qt.QTableWidget):
    directory = ''
    file_extension = '.edf'
    fileSelectedChanged = qt.pyqtSignal(str)
    emptyCellFile = None
    darkFile = None
    emptyBeamFile = None
    maskFile = None
    trashFiles = []
    treatedFiles = []

    def __init__(self):
        super(EdfFileTable, self).__init__()
        self.setColumnCount(6)
        self.setRowCount(3)
        self.setRowCount(4)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(['File', 'comment', 'e (mm)','tr', 'distance',  'counting time', ' date'])
        self.currentItemChanged.connect(self.on_selectionChanged)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)
        self.cellChanged.connect(self.on_cellChanged)

    def setDirectory(self, directory):
        folderPath = Path(directory)
        if folderPath.is_dir():
            self.directory = folderPath
            self.refresh()

    def refresh(self):
        self.currentItemChanged.disconnect()
        self.cellChanged.disconnect()
        if os.path.isdir(self.directory):
            l = os.listdir(self.directory)
            # l.sort()
            fileList = []
            for item in l:
                if os.path.splitext(item)[1] == self.file_extension:
                    fileList.append(item)
            # self.clearContents()
            self.setRowCount(len(fileList))
            for i, file in enumerate(fileList):
                description = get_edf_description(os.path.join(self.directory, file))
                for j, des in enumerate(description):
                    item = qt.QTableWidgetItem(des)
                    if j == 2 or j == 3:
                        item.setFlags(qt.Qt.ItemIsEditable | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                    else:
                        item.setFlags(qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled)
                    self.setItem(i, j, item)
                # check of the file was current set to parametric file
                filepath = os.path.join(self.directory, file)
                if filepath == self.darkFile:
                    self.set_row_bkg(i, qt.QColor("blue"))
                    self.item(i, 0).setIcon(getQIcon('dark.ico'))
                elif filepath == self.emptyCellFile:
                    self.set_row_bkg(i, qt.QColor("cyan"))
                    self.item(i, 0).setIcon(getQIcon('empty_cell.ico'))
                elif filepath == self.emptyBeamFile:
                    self.set_row_bkg(i, qt.QColor("red"))
                    self.item(i, 0).setIcon(getQIcon('beam.ico'))
                # elif filepath in self.trashFiles:
                #     self.set_row_bkg(i, qt.QColor("grey"))
                #     self.item(i, 0).setIcon(getQIcon('cross.ico'))
                elif filepath == self.maskFile:
                    self.set_row_bkg(i, qt.QColor("white"))
                    self.item(i, 0).setIcon(getQIcon('mask.ico'))
                elif os.path.exists(os.path.splitext(filepath)[0]+'.nxs'):
                    self.item(i, 0).setIcon(getQIcon('check.ico'))

        self.sortItems(0, qt.Qt.AscendingOrder)
        self.currentItemChanged.connect(self.on_selectionChanged)
        self.cellChanged.connect(self.on_cellChanged)

    def on_selectionChanged(self):
        row = self.currentRow()
        file = self.item(row, 0).text()
        self.fileSelectedChanged.emit(os.path.join(self.directory, file))

    def on_cellChanged(self, row, col):
        item = self.item(row, col)
        item.setForeground(qt.QBrush(qt.QColor(138, 43, 226)))
        font = qt.QFont()
        font.setBold(True)
        font.setWeight(100)
        item.setFont(font)

    def generateMenu(self, event):
        current_item = self.itemAt(event)
        # current_item = self.selectedItems()
        menu = qt.QMenu()
        # emptyCellAction = qt.QAction(qt.QIcon(qt.QPixmap('../ressources/empty_cell.ico')), 'empty cell')
        emptyCellAction = qt.QAction(getQIcon('empty_cell.ico'), 'empty cell')
        emptyCellAction.triggered.connect(self._set_empty_cell)
        darkAction = qt.QAction(getQIcon('dark.ico'), 'dark')
        darkAction.triggered.connect(self._set_dark)
        emptyBeamAction = qt.QAction(getQIcon('beam.ico'), 'empty beam')
        emptyBeamAction.triggered.connect(self._set_empty_beam)
        # trashAction = qt.QAction(getQIcon('cross.ico'), 'trash')
        # trashAction.triggered.connect(self._set_trash)
        sampleAction = qt.QAction('sample')
        sampleAction.triggered.connect(self._set_sample)
        maskAction = qt.QAction(getQIcon('mask.ico'), 'mask')
        maskAction.triggered.connect(self._set_mask)
        # build menu
        menu.addAction(darkAction)
        menu.addAction(emptyCellAction)
        menu.addAction(emptyBeamAction)
        # menu.addAction(trashAction)
        menu.addAction(sampleAction)
        menu.addAction(maskAction)
        action = menu.exec_(self.mapToGlobal(event))
        # print('###################################### \n')
        # print(('dark : %s \n '
        #        'empty cell: %s \n'
        #        'empty beam %s') %
        #       (self.darkFile, self.emptyCellFile, self.emptyBeamFile))

    def set_row_bkg(self, row, color):
        for i in range(self.columnCount()):
            item = self.item(row, i)
            item.setBackground(color)

    def _set_empty_cell(self):
        current_item = self.currentItem()
        self.cellChanged.disconnect()
        if current_item is not None:
            current_ec_item = self.findItems(os.path.basename(str(self.emptyCellFile)), qt.Qt.MatchExactly)
            # remove the previous empty cell icons
            if current_ec_item:
                self.set_row_bkg(current_ec_item[0].row(), qt.QColor("white"))
                filepath = os.path.join(self.directory, current_ec_item[0].text())
                if os.path.exists(os.path.splitext(filepath)[0] + '.nxs'):
                    current_ec_item[0].setIcon(getQIcon('check.ico'))
                else:
                    current_ec_item[0].setIcon(qt.QIcon())
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            first_col_item.setIcon(getQIcon('empty_cell.ico'))
            self.set_row_bkg(row, qt.QColor("cyan"))
            fullfile = os.path.join(self.directory, file)
            self.emptyCellFile = fullfile
            # remove double reference
            if fullfile == self.darkFile:
                self.darkFile = None
            elif fullfile == self.emptyBeamFile:
                self.emptyBeamFile = None
            elif fullfile == self.maskFile:
                self.maskFile = None
            else:
                pass
        self.cellChanged.connect(self.on_cellChanged)

    def _set_sample(self):
        self.cellChanged.disconnect()
        for current_item in self.selectedItems():
            if current_item is not None:
                row = current_item.row()
                ncol = self.columnCount()
                first_col_item = self.item(row, 0)
                file = first_col_item.text()
                self.set_row_bkg(row, qt.QColor("white"))
                first_col_item.setIcon(qt.QIcon())
                fullfile = os.path.join(self.directory, file)
                if os.path.exists(os.path.splitext(fullfile)[0] + '.nxs'):
                    first_col_item.setIcon(getQIcon('check.ico'))
                else:
                    first_col_item.setIcon(qt.QIcon())
                # remove double reference
                if fullfile == self.emptyCellFile:
                    self.emptyCellFile = None
                elif fullfile == self.darkFile:
                    self.darkFile = None
                elif fullfile == self.emptyBeamFile:
                    self.emptyBeamFile = None
                elif fullfile == self.maskFile:
                    self.maskFile = None
                # elif fullfile in self.trashFiles:
                #     self.trashFiles.remove(fullfile)
        self.cellChanged.connect(self.on_cellChanged)

    def _set_dark(self, event):
        self.cellChanged.disconnect()
        current_item = self.currentItem()
        if current_item is not None:
            current_dark_item = self.findItems(os.path.basename(str(self.darkFile)), qt.Qt.MatchExactly)
            # remove the previous empty cell icons
            if current_dark_item:
                self.set_row_bkg(current_dark_item[0].row(), qt.QColor("white"))
                filepath = os.path.join(self.directory, current_dark_item[0].text())
                if os.path.exists(os.path.splitext(filepath)[0] + '.nxs'):
                    current_dark_item[0].setIcon(getQIcon('check.ico'))
                else:
                    current_dark_item[0].setIcon(qt.QIcon())
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            self.set_row_bkg(row, qt.QColor("blue"))
            first_col_item.setIcon(getQIcon('dark.ico'))
            # remove double reference
            fullfile = os.path.join(self.directory, file)
            self.darkFile = fullfile
            if fullfile == self.emptyCellFile:
                self.emptyCellFile = None
            elif fullfile == self.emptyBeamFile:
                self.emptyBeamFile = None
            elif fullfile == self.maskFile:
                self.maskFile = None
            else:
                pass
            self.cellChanged.connect(self.on_cellChanged)

    def _set_empty_beam(self):
        self.cellChanged.disconnect()
        current_item = self.currentItem()
        if current_item is not None:
            current_eb_item = self.findItems(os.path.basename(str(self.emptyBeamFile)), qt.Qt.MatchExactly)
            # remove the previous empty cell icons
            if current_eb_item:
                self.set_row_bkg(current_eb_item[0].row(), qt.QColor("white"))
                filepath = os.path.join(self.directory, current_eb_item[0].text())
                if os.path.exists(os.path.splitext(filepath)[0] + '.nxs'):
                    current_eb_item[0].setIcon(getQIcon('check.ico'))
                else:
                    current_eb_item[0].setIcon(qt.QIcon())
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            self.set_row_bkg(row, qt.QColor("red"))
            first_col_item.setIcon(getQIcon('beam.ico'))
            # remove double reference
            fullfile = os.path.join(self.directory, file)
            self.emptyBeamFile = fullfile
            if fullfile == self.emptyCellFile:
                self.emptyCellFile = None
            elif fullfile == self.darkFile:
                self.darkFile = None
            elif fullfile == self.maskFile:
                self.maskFile = None
            else:
                pass
            self.cellChanged.connect(self.on_cellChanged)

    # def _set_trash(self):
    #     # can be applied to the overall selection
    #     for current_item in self.selectedItems():
    #         if current_item is not None:
    #             row = current_item.row()
    #             ncol = self.columnCount()
    #             first_col_item = self.item(row, 0)
    #             file = first_col_item.text()
    #             self.set_row_bkg(row, qt.QColor("grey"))
    #             first_col_item.setIcon(getQIcon('cross.ico'))
    #             # remove double reference
    #             fullfile = os.path.join(self.directory, file)
    #             self.trashFiles.append(fullfile)
    #             if fullfile == self.emptyCellFile:
    #                 self.emptyCellFile = None
    #             elif fullfile == self.darkFile:
    #                 self.darkFile = None
    #             elif fullfile == self.emptyBeamFile:
    #                 self.emptyBeamFile = None
    #             elif fullfile == self.maskFile:
    #                 self.maskFile = None
    #             else:
    #                 pass

    def _set_mask(self):
        self.cellChanged.disconnect()
        current_item = self.currentItem()
        if current_item is not None:
            current_mask_item = self.findItems(os.path.basename(str(self.maskFile)), qt.Qt.MatchExactly)
            # remove the previous empty cell icons
            if current_mask_item:
                self.set_row_bkg(current_mask_item[0].row(), qt.QColor("white"))
                filepath = os.path.join(self.directory, current_mask_item[0].text())
                if os.path.exists(os.path.splitext(filepath)[0] + '.nxs'):
                    current_mask_item[0].setIcon(getQIcon('check.ico'))
                else:
                    current_mask_item[0].setIcon(qt.QIcon())
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            first_col_item.setIcon(getQIcon('mask.ico'))
            # self.set_row_bkg(row, qt.QColor("cyan"))

            fullfile = os.path.join(self.directory, file)
            self.maskFile = fullfile
            # remove double reference
            if fullfile == self.darkFile:
                self.darkFile = None
            elif fullfile == self.emptyBeamFile:
                self.emptyBeamFile = None
            elif fullfile == self.emptyCellFile:
                self.maskFile = None
            else:
                pass
        self.cellChanged.connect(self.on_cellChanged)

    def get_sample_files(self):
        sampleList = []
        thicknessList = []
        transmissionList = []
        for current_item in self.selectedItems():
            row = current_item.row()
            ncol = self.columnCount()
            first_col_item = self.item(row, 0)
            file = first_col_item.text()
            # remove double reference
            fullfile = os.path.join(self.directory, file)
            self.trashFiles.append(fullfile)
            if fullfile not in [self.emptyCellFile, self.darkFile, self.emptyBeamFile]:
                sampleList.append(fullfile)
                try:
                    thicknessList.append(float(self.item(row, 2).text()))
                except ValueError:
                    thicknessList.append(1.5)
                try:
                    transmissionList.append(float(self.item(row, 3).text()))
                except ValueError:
                    transmissionList.append(None)

        return sampleList, thicknessList, transmissionList

    def get_standards_transmission(self):
        stantards = [self.darkFile, self.emptyCellFile, self.emptyBeamFile]
        trasnmissionList = []
        for st in stantards:
            if st:
                basename = os.path.basename(st)
                item = self.findItems(basename, qt.Qt.MatchExactly)[0]
                try:
                    tr = float(self.item(item.row(), 3).text())
                except ValueError:
                    tr = None
                trasnmissionList.append(tr)
            else:
                trasnmissionList.append(None)
        print(trasnmissionList)
        return trasnmissionList


class EdfTreatmentWidget(qt.QWidget):
    edfSelectionChanged = qt.pyqtSignal(str)
    edfTreatmentClicked = qt.pyqtSignal()

    def __init__(self, parent=None):
        super(EdfTreatmentWidget, self).__init__()
        # self.directoryLineEdit = qt.QLineEdit(parent=self)
        # self.directoryPickerButton = qt.QPushButton()
        # self.directoryPickerButton.setIcon(qt.QIcon(qt.QPixmap('../ressources/directory.ico')))
        # self.refreshButton = qt.QPushButton()
        # self.refreshButton.setIcon(qt.QIcon(qt.QPixmap('../ressources/refresh.ico')))
        self.table = EdfFileTable()
        # beam center coordinates
        self.x0LineEdit = qt.QLineEdit()
        # self.x0LineEdit.setValidator(qt.QDoubleValidator())
        self.y0LineEdit = qt.QLineEdit()
        # self.y0LineEdit.setValidator(qt.QDoubleValidator())
        # sample to detector distance
        self.distanceLineEdit = qt.QLineEdit()
        # self.distanceLineEdit.setValidator(qt.QDoubleValidator())
        # define the number of bins for azimutal averaging
        self.binsLineEdit = qt.QLineEdit('900')
        self.binsLineEdit.setValidator(qt.QIntValidator())
        # load and save integration parameters
        self.saveConfigButton = qt.QPushButton('save')
        self.saveConfigButton.setToolTip('Save treatment parameters\n'
                                         'and the subtraction files')
        self.loadConfigButton = qt.QPushButton('load')
        self.loadConfigButton.setToolTip('Save treatment parameters\n'
                                         'and the subtraction files')

        # button to treat data
        # self.treatButton = qt.QPushButton('treat selected')
        # self.treatButton.setIcon(getQIcon('gear.ico'))
        # self.treatButton.setToolTip('Perform azimutal integration and \n '
        #                             'data substraction\n'
        #                             'on selected files')
        self.treatButton = WaitingPushButton(parent=self, text='treat selected', icon=getQIcon('gear.ico'))
        # parameter form layout
        formLayout = qt.QFormLayout()
        formLayout.addRow('x0 (pixels):', self.x0LineEdit)
        formLayout.addRow('y0 (pixels):', self.y0LineEdit)
        formLayout.addRow('distance (mm):', self.distanceLineEdit)
        formLayout.addRow('bins :', self.binsLineEdit)
        # parameter total layout
        paramLayout = qt.QHBoxLayout()
        configLayout= qt.QVBoxLayout()
        configLayout.addWidget(self.loadConfigButton)
        configLayout.addWidget(self.saveConfigButton)
        paramLayout.addLayout(formLayout)
        paramLayout.addLayout(configLayout)
        # general layout
        hlayout = qt.QHBoxLayout()
        # hlayout.addWidget(qt.QLabel('directory :'))
        # hlayout.addWidget(self.directoryLineEdit)
        # hlayout.addWidget(self.directoryPickerButton)
        # hlayout.addWidget(self.refreshButton)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(paramLayout)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.table)
        vlayout.addWidget(self.treatButton)
        self.setLayout(vlayout)
        # connect signals
        # self.directoryLineEdit.textChanged.connect(self.set_directory)
        # self.directoryPickerButton.clicked.connect(self.choose_directory)
        # self.refreshButton.clicked.connect(self.table.refresh)
        # we unconnect the treatbutton here because of interactions with treeview
        # self.treatButton.clicked.connect(self.treat)
        self.table.fileSelectedChanged.connect(self.on_file_selected)
        self.saveConfigButton.clicked.connect(self.saveConfig_clicked)
        self.loadConfigButton.clicked.connect(self.loadConfig_clicked)

    def on_file_selected(self, file):
        self.edfSelectionChanged.emit(file)

    def treat(self):
        directory = self.table.directory
        try:
            x0 = float(self.x0LineEdit.text())
        except ValueError:
            x0 = None
        try:
            y0 = float(self.y0LineEdit.text())
        except ValueError:
            y0 = None
        try:
            distance = float(self.distanceLineEdit.text())
        except ValueError:
            distance = None
        nbins = int(self.binsLineEdit.text())
        mask_file = self.table.maskFile
        # treat the reference files
        # dark file
        dark_tr , ec_tr, eb_tr = self.table.get_standards_transmission()
        dark_file = self.table.darkFile
        if dark_file is not None:
            nxlib.build_nexus_from_edf(dark_file)
            dark_file = dark_file.split('.')[0] + '.nxs'
            xeuss.set_transmission(dark_file, transmission=dark_tr)
            xeuss.set_beam_center(dark_file, x0=x0, y0=y0)
            xeuss.azimutal_integration(dark_file, bins=nbins, mask=mask_file)

        # empty cell
        ec_file = self.table.emptyCellFile
        if ec_file is not None:
            nxlib.build_nexus_from_edf(ec_file)
            ec_file = ec_file.split('.')[0] + '.nxs'
            xeuss.set_transmission(ec_file, transmission=ec_tr)
            xeuss.set_beam_center(ec_file, x0=x0, y0=y0)
            xeuss.azimutal_integration(ec_file, bins=nbins, mask=mask_file)
        # empty beam
        eb_file = self.table.emptyBeamFile
        if eb_file is not None:
            nxlib.build_nexus_from_edf(eb_file)
            eb_file = eb_file.split('.')[0] + '.nxs'
            xeuss.set_transmission(eb_file, transmission=eb_tr)
            xeuss.set_beam_center(eb_file, x0=x0, y0=y0)
            xeuss.azimutal_integration(eb_file, bins=nbins, mask=mask_file)

        sampleList, thicknessList, transmissionList = self.table.get_sample_files()
        for sample, thickness, tr in zip(sampleList, thicknessList, transmissionList):
            # nxfile = sample.split('.')[0]+'.nxs'
            try:
                nxlib.build_nexus_from_edf(sample)
                file = sample.split('.')[0]+'.nxs'
                xeuss.set_beam_center(file, x0=x0, y0=y0)  # direct_beam_file=directbeam, new_entry=False)
                xeuss.azimutal_integration(file, bins=nbins, mask=mask_file)
                xeuss.resu(file, dark_file=dark_file, ec_file=ec_file, eb_file=eb_file,
                           distance=distance, thickness=thickness,
                           transmission=tr)
            except (KeyError, ValueError):
                print(('%s was ignored during the treatment') % (sample))
        self.table.refresh()

    def saveConfig_clicked(self):
        dic = {}
        if self.table.directory:
            basedir = self.table.directory
        else:
            basedir = os.path.expanduser("~")
        fname, ext = qt.QFileDialog.getSaveFileName(self, 'Save treatment parameters', str(basedir),'YAML files (*.yaml);; all files (*.*)',
                                                      options=qt.QFileDialog.DontUseNativeDialog)
        if fname:
            try:
                dic['x0'] = float(self.x0LineEdit.text())
            except ValueError:
                dic['x0'] = None
            try:
                dic['y0'] = float(self.y0LineEdit.text())
            except ValueError:
                dic['y0'] = None
            try:
                dic['distance'] = float(self.distanceLineEdit.text())
            except ValueError:
                dic['distance'] = None
            try:
                dic['nbins'] = int(self.binsLineEdit.text())
            except ValueError:
                dic['nbins'] = 900
            dic['mask_file'] = self.table.maskFile
            dic['dark_file'] = self.table.darkFile
            dic['ec_file'] = self.table.emptyCellFile
            dic['eb_file'] = self.table.emptyBeamFile
            p = Path(fname)
            if p.suffix != '.yaml':
                fname = str(p.with_suffix('.yaml'))
            with open(fname, 'w') as fid:
                yaml.dump(dic, fid)

    def loadConfig_clicked(self):
        if self.table.directory:
            basedir = self.table.directory
        else:
            basedir = os.path.expanduser("~")
        fname, ext = qt.QFileDialog.getOpenFileName(self, 'Load treatment parameters', str(basedir),
                                                    'YAML files (*.yaml);; all files (*.*)',
                                                    options=qt.QFileDialog.DontUseNativeDialog)
        if fname:
            with open(fname, 'r') as fid:
                params = yaml.safe_load(fid)
            if params['x0'] is not None:
                self.x0LineEdit.setText(str(params['x0']))
            else:
                self.x0LineEdit.setText('')
            if params['y0'] is not None:
                self.y0LineEdit.setText(str(params['y0']))
            else:
                self.y0LineEdit.setText('')
            if params['distance'] is not None:
                self.distanceLineEdit.setText(str(params['distance']))
            else:
                self.distanceLineEdit.setText('')
            if params['nbins'] is not None:
                self.binsLineEdit.setText(str(params['nbins']))
            else:
                self.binsLineEdit.setText('900')
            if self.table.directory:
                if params['ec_file']:
                    if Path(os.path.dirname(params['ec_file'])) == self.table.directory and \
                            os.path.exists(params['ec_file']):
                        self.table.emptyCellFile = params['ec_file']
                if params['dark_file']:
                    if Path(os.path.dirname(params['dark_file'])) == self.table.directory and \
                            os.path.exists(params['dark_file']):
                        self.table.darkFile = params['dark_file']
                if params['eb_file']:
                    if Path(os.path.dirname(params['eb_file'])) == self.table.directory and \
                            os.path.exists(params['eb_file']):
                        self.table.emptyBeamFile = params['eb_file']
                if params['mask_file']:
                    if Path(os.path.dirname(params['mask_file'])) == self.table.directory and \
                            os.path.exists(params['mask_file']):
                        self.table.maskFile = params['mask_file']
                self.table.refresh()


class FileSurvey(qt.QWidget):

    def __init__(self):
        super(FileSurvey, self).__init__()
        self.directoryLineEdit = qt.QLineEdit(parent=self)
        self.directoryPickerButton = qt.QPushButton()
        self.directoryPickerButton.setIcon(getQIcon('directory.ico'))
        self.directoryPickerButton.setToolTip('open data directory')
        self.refreshButton = qt.QPushButton()
        self.refreshButton.setIcon(getQIcon('refresh.ico'))
        self.refreshButton.setToolTip('refresh directory')

        self.tabWidget = qt.QTabWidget()
        self.edfTab = EdfTreatmentWidget()
        self.nxsTab = NexusTreatmentWidget()
        self.tabWidget.addTab(self.edfTab, 'edf data')
        self.tabWidget.addTab(self.nxsTab, 'treated data')

        # layout
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(qt.QLabel('directory :'))
        hlayout.addWidget(self.directoryLineEdit)
        hlayout.addWidget(self.directoryPickerButton)
        hlayout.addWidget(self.refreshButton)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.tabWidget)
        self.setLayout(vlayout)

        # connect signals
        self.directoryLineEdit.textChanged.connect(self.set_directory)
        self.directoryPickerButton.clicked.connect(self.choose_directory)
        self.refreshButton.clicked.connect(self.edfTab.table.refresh)
        self.refreshButton.clicked.connect(self.nxsTab.tableWidget.refresh)
        # self.edfTab.edfTreatmentClicked.connect(self.on_treatment)
        self.edfTab.treatButton.clicked.connect(self.on_treatment_clicked)

    def on_treatment_clicked(self):
        model = self.nxsTab.treeWidget.treeview.findHdf5TreeModel()
        model.clear()
        self.edfTab.treat()
        self.nxsTab.tableWidget.refresh()

    def set_directory(self):
        text = self.directoryLineEdit.text()
        self.edfTab.table.setDirectory(text)
        self.nxsTab.set_directory(text)

    def choose_directory(self):
        basedir = os.path.expanduser("~")
        fname = qt.QFileDialog.getExistingDirectory(self, 'Select data directory', basedir,
                                                    options=qt.QFileDialog.DontUseNativeDialog)
        if fname:
            self.directoryLineEdit.setText(fname)
            # self.edfTab.table.setDirectory(fname)
            # self.nxsTab.setDirectory(fname)


class FunctionWorker(qt.QObject):
    progress = qt.pyqtSignal()
    finished = qt.pyqtSignal()

    def __init__(self, cmdList, fileList):
        super(FunctionWorker, self).__init__()
        self.cmdList = cmdList
        self.fileList = fileList

    def run(self):
        self.progress.emit()
        for file in self.fileList:
            for script in self.cmdList:
                cmd = 'xeuss.' + script.replace('root', '\'' + file.replace('\\', '/') + '\'')
                print(cmd)
                eval(cmd)
        self.finished.emit()


class NexusFileTable(qt.QTableWidget):
    directory = ''
    file_extension = '.nxs'
    fileSelectedChanged = qt.pyqtSignal(list)

    def __init__(self, parent=None):
        super(NexusFileTable, self).__init__(parent=None)
        self.setColumnCount(6)
        self.setRowCount(3)
        self.setRowCount(4)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectRows | qt.QAbstractItemView.MultiSelection)
        self.setHorizontalHeaderLabels(['File', 'comment', 'e (mm)','tr', 'distance',  'counting time', ' date'])
        self.itemSelectionChanged.connect(self.on_selectionChanged)

    def setDirectory(self, directory):
        forlderPath = Path(directory)
        if forlderPath.is_dir():
            self.directory = forlderPath
            self.refresh()

    def refresh(self):
        self.itemSelectionChanged.disconnect()
        if os.path.isdir(self.directory):
            l = os.listdir(self.directory)
            # l.sort()
            fileList = []
            for item in l:
                if os.path.splitext(item)[1] == self.file_extension:
                    fileList.append(item)
            # self.clearContents()
            self.setRowCount(len(fileList))
            for i, file in enumerate(fileList):
                description = get_nxs_description(os.path.join(self.directory, file))
                for j, des in enumerate(description):
                    item = qt.QTableWidgetItem(des)
                    item.setFlags(qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled)
                    self.setItem(i, j, item)

            self.sortItems(0, qt.Qt.AscendingOrder)
            self.itemSelectionChanged.connect(self.on_selectionChanged)

    def on_selectionChanged(self):
        items = self.selectedItems()
        selectedFiles = []
        for item in items:
            row = item.row()
            file = self.item(row, 0).text()
            selectedFiles.append(os.path.join(self.directory, file))
        self.fileSelectedChanged.emit(selectedFiles)

    def get_selectedFiles(self):
        items = self.selectedItems()
        selectedFiles = []
        for item in items:
            row = item.row()
            file = self.item(row, 0).text()
            selectedFiles.append(os.path.join(self.directory, file))
        return selectedFiles


class NexusTreeWidget(qt.QWidget):
    operationPerformed = qt.pyqtSignal()
    selectedNodeChanged = qt.pyqtSignal(list)

    def __init__(self):
        super(NexusTreeWidget, self).__init__()
        self.clear_last_btn = qt.QPushButton('clear last')
        self.clear_last_btn.setToolTip('Clear last performed calculation')
        self.clear_all_btn = qt.QPushButton('clear all')
        self.clear_all_btn.setToolTip('clear all performed calculations')
        # self.sync_btn = qt.QPushButton('sync')
        # self.sync_btn.setToolTip('synchronize the .nxs files')
        """Silx HDF5 TreeView"""
        self.treeview = silx.gui.hdf5.Hdf5TreeView(self)
        treemodel = silx.gui.hdf5.Hdf5TreeModel(self.treeview,
                                                ownFiles=True
                                                )
        # treemodel.sigH5pyObjectLoaded.connect(self.__h5FileLoaded)
        # treemodel.sigH5pyObjectRemoved.connect(self.__h5FileRemoved)
        # treemodel.sigH5pyObjectSynchronized.connect(self.__h5FileSynchonized)
        treemodel.setDatasetDragEnabled(False)
        # self.treeview.setModel(treemodel)
        self.__treeModelSorted = silx.gui.hdf5.NexusSortFilterProxyModel(self.treeview)
        self.__treeModelSorted.setSourceModel(treemodel)
        self.__treeModelSorted.sort(0, qt.Qt.AscendingOrder)
        self.__treeModelSorted.setSortCaseSensitivity(qt.Qt.CaseInsensitive)
        self.treeview.setModel(self.__treeModelSorted)
        self.treeview.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        # layout
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(self.clear_last_btn)
        hlayout.addWidget(self.clear_all_btn)
        # hlayout.addWidget(self.sync_btn)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.treeview)
        self.setLayout(vlayout)

        # connect signals
        # self.sync_btn.clicked.connect(self.sync_all)
        self.clear_last_btn.clicked.connect(self.clear_last)
        self.clear_all_btn.clicked.connect(self.clear_all)
        self.treeview.selectionModel().selectionChanged.connect(self.on_tree_selection)

    def load_files(self, files):
        model = self.treeview.findHdf5TreeModel()
        model.clear()
        for file in files:
            model.insertFile(file, row=-1)
        self.treeview.expandToDepth(0)

    def clear_last(self):
        model = self.treeview.findHdf5TreeModel()
        nrow = model.rowCount()
        files = []
        for n in range(nrow):
            index = model.index(n, 0, qt.QModelIndex())
            node = model.nodeFromIndex(index)
            filename = node.obj.filename
            model.removeH5pyObject(node.obj)
            # node.obj.close()
            root = nxlib.loadfile(filename, mode='rw')
            nxlib.delete_last_entry(root)
            root.close()
            model.insertFile(filename, row=n)
        self.treeview.expandToDepth(0)
        self.operationPerformed.emit()

    def clear_all(self):
        model = self.treeview.findHdf5TreeModel()
        nrow = model.rowCount()
        for n in range(nrow):
            index = model.index(n, 0, qt.QModelIndex())
            node = model.nodeFromIndex(index)
            filename = node.obj.filename
            model.removeH5pyObject(node.obj)
            root = nxlib.loadfile(filename, mode='rw')
            nxlib.delete_all_entry(root)
            root.close()
            model.insertFile(filename, row=n)
        self.treeview.expandToDepth(0)
        self.operationPerformed.emit()

    def sync_all(self):
        model = self.treeview.findHdf5TreeModel()
        nrow = model.rowCount()

        for n in range(nrow):
            index = model.index(n, 0, qt.QModelIndex())
            node = model.nodeFromIndex(index)
            filename = node.obj.filename
            model.removeH5pyObject(node.obj)
            root = nxlib.loadfile(filename, mode='rw')
            nxlib.delete_all_entry(root)
            root.close()
            model.insertFile(filename, row=n)
        self.treeview.expandToDepth(0)
        self.operationPerformed.emit()

    def on_tree_selection(self):
        selected = list(self.treeview.selectedH5Nodes())
        self.selectedNodeChanged.emit(selected)


class NexusTreatmentWidget(qt.QWidget):
    nxsSelectionChanged = qt.pyqtSignal(list)

    def __init__(self):
        super(NexusTreatmentWidget, self).__init__()
        self.tableWidget = NexusFileTable()
        self.treeWidget = NexusTreeWidget()
        # layout
        spliter = qt.QSplitter(qt.Qt.Vertical)
        spliter.addWidget(self.tableWidget)
        spliter.addWidget(self.treeWidget)
        # spliter.setStretchFactor(0, 3)
        layout = qt.QVBoxLayout()
        layout.addWidget(spliter)
        self.setLayout(layout)
        # connect
        self.tableWidget.fileSelectedChanged.connect(self.on_file_selected)
        self.treeWidget.operationPerformed.connect(self.on_tree_operation)
        # context menu for quick functions
        self.tableWidget.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

    def set_directory(self, directory):
        self.tableWidget.setDirectory(directory)

    def on_file_selected(self, files):
        self.treeWidget.load_files(files)
        self.nxsSelectionChanged.emit(files)

    def on_tree_operation(self):
        self.tableWidget.on_selectionChanged()

    def generateMenu(self, event):
        menu = qt.QMenu()
        # concatenat 1D file
        concatAction = qt.QAction(getQIcon('concat.ico'), 'concat')
        concatAction.triggered.connect(self._concat)
        # convert to txt file
        convertAction = qt.QAction(getQIcon('nxs2text.ico'), 'convert to .txt')
        convertAction.triggered.connect(self._convert2txt)
        # copy file path to clipboard
        getPathAction = qt.QAction(getQIcon('clipboard.ico'), 'copy file path')
        getPathAction.triggered.connect(self._copyPath2clipboard)
        # duplicate file within the same folder
        duplicateAction = qt.QAction(getQIcon('duplicate-file.png'), 'duplicate file')
        duplicateAction.triggered.connect(self._duplicateFiles)
        # delete files
        removeFileAction = qt.QAction(getQIcon('trash.png'), 'delete file')
        removeFileAction.triggered.connect(self._deleteFiles)
        # rename file
        renameFileAction = qt.QAction('rename file')
        renameFileAction.triggered.connect(self._renameFile)

        menu.addAction(concatAction)
        menu.addAction(convertAction)
        menu.addAction(getPathAction)
        menu.addAction(duplicateAction)
        menu.addAction(removeFileAction)
        menu.addAction(renameFileAction)

        action = menu.exec_(self.mapToGlobal(event))

    def _copyPath2clipboard(self):
        items = self.tableWidget.selectedItems()
        fileList = []
        for item in items:
            row = item.row()
            # fileList.append('"'+os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text())+'"')
            clip = '"' + Path(self.tableWidget.directory, self.tableWidget.item(row, 0).text()).__str__()+'"'
            fileList.append(clip)
        if fileList:
            qt.QApplication.clipboard().setText(fileList[0])

    def _concat(self, items):
        items = self.tableWidget.selectedItems()
        fileList = []
        for item in items:
            row = item.row()
            fileList.append(os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text()))
        treemodel = self.treeWidget.treeview.findHdf5TreeModel()
        # clear model before using the filess
        treemodel.clear()
        if len(fileList) > 1:
            firstFile = fileList.pop(0)
            for file in fileList:
                xeuss.concat(firstFile, file=file)
            # treemodel.insertFile(firstFile)
        for file in fileList:
            treemodel.insertFile(file)

    def _convert2txt(self):
        items = self.tableWidget.selectedItems()
        fileList = []
        for item in items:
            row = item.row()
            fileList.append(os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text()))
        treemodel = self.treeWidget.treeview.findHdf5TreeModel()
        # clear model before using the filess
        treemodel.clear()
        for file in fileList:
            xeuss.save_as_txt(file)
        for file in fileList:
            treemodel.insertFile(file)

    def _deleteFiles(self):
        # warning dialog
        msg = qt.QMessageBox()
        msg.setIcon(qt.QMessageBox.Warning)
        msg.setText("Are you sure you want to delete these files ?")
        msg.setInformativeText('The deleted files cannot be retrieved')
        msg.setWindowTitle("warning")
        msg.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.No)
        ans = msg.exec_()
        if ans == qt.QMessageBox.No:
            return
        items = self.tableWidget.selectedItems()
        fileList = []
        for item in items:
            row = item.row()
            fileList.append(os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text()))
        treemodel = self.treeWidget.treeview.findHdf5TreeModel()
        self.tableWidget.clearSelection()
        # clear model before using the filess
        treemodel.clear()
        for file in fileList:
            os.remove(file)
        self.tableWidget.refresh()

    def _duplicateFiles(self):
        items = self.tableWidget.selectedItems()
        fileList = []
        for item in items:
            row = item.row()
            fileList.append(os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text()))
        for file in fileList:
            path, ext = os.path.splitext(file)
            path += '_0'
            shutil.copyfile(file, path+ext)
        self.tableWidget.refresh()

    def _renameFile(self):
        item = self.tableWidget.selectedItems()[0]
        row = item.row()
        file = os.path.join(self.tableWidget.directory, self.tableWidget.item(row, 0).text())
        basename = os.path.basename(file)
        name, done = qt.QInputDialog.getText(self, 'Rename file', 'new file name:', qt.QLineEdit.Normal, basename)

        treemodel = self.treeWidget.treeview.findHdf5TreeModel()
        self.tableWidget.clearSelection()
        # clear model before using the filess
        treemodel.clear()

        if not done:
            return
        new_file = os.path.join(self.tableWidget.directory, name)
        if os.path.exists(new_file):
            # warning dialog
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Warning)
            msg.setText("Filename already exist do you want to overide it ?")
            msg.setWindowTitle("warning")
            msg.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.No)
            ans = msg.exec_()
            if ans == qt.QMessageBox.No:
                return
            else:
                os.rename(file, new_file)
        else:
            os.rename(file, new_file)
        self.tableWidget.refresh()


class CommandTreatmentWidget(qt.QWidget):
    runClicked = qt.pyqtSignal(list)

    def __init__(self, parent, module=None):
        super(CommandTreatmentWidget, self).__init__()
        self.run_btn = qt.QPushButton('run')
        self.runAll_btn = qt.QPushButton('run all')
        self.run_btn.clicked.connect(self.run)
        self.runAll_btn.clicked.connect(self.runAll)
        self.add_btn = qt.QPushButton('+')
        self.add_btn.setFixedSize(20,20)
        self.add_btn.clicked.connect(self.addTab)
        self.tabWidget = qt.QTabWidget()
        self.tabWidget.setCornerWidget(self.add_btn, corner=qt.Qt.TopLeftCorner)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMaximumHeight(500)
        self.tabWidget.tabCloseRequested.connect(self.closeTabs)
        if module is not None:
            self.commandList = moduledescription.get_commandList(module)
        else:
            self.commandList = []
        self.commandWidgetList = []
        self.commandWidgetList.append(MultiLineCodeEditor(parent=self.tabWidget, completerList=self.commandList))
        self.tabWidget.addTab(self.commandWidgetList[0], 'cmd1')
        hlayout = qt.QHBoxLayout()
        layout = qt.QVBoxLayout(self)
        hlayout.addWidget(self.run_btn)
        hlayout.addWidget(self.runAll_btn)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.tabWidget)
        layout.addStretch()
        # self.formLayout = qt.QFormLayout(self)
        # layout.addLayout(self.formLayout)
        self.setLayout(layout)

    def closeTabs(self, index):
        count = self.tabWidget.count()
        if count > 1:
            self.tabWidget.removeTab(index)
            self.commandWidgetList.remove(index)

    def addTab(self):
        count = self.tabWidget.count()
        # widget = qt.QWidget()
        # layout = qt.QVBoxLayout()
        # layout.addWidget(CodeEditor(self))
        # layout.addStretch()
        # widget.setLayout(layout)
        self.commandWidgetList.append(MultiLineCodeEditor(parent=self, completerList=self.commandList))
        self.tabWidget.addTab(self.commandWidgetList[-1], 'cmd'+str(count+1))
        # self.tabWidget.addTab(widget, 'cmd'+str(count+1))

    def run(self):
        # widget = self.tabWidget.currentWidget()
        index = self.tabWidget.currentIndex()
        widget = self.commandWidgetList[index]
        text = widget.toPlainText()
        self.runClicked.emit([text])

    def runAll(self):
        count = self.tabWidget.count()
        l = []
        for i in range(count):
            widget = self.commandWidgetList[i]
            l.append(widget.toPlainText())
        self.runClicked.emit(l)

    def on_comboBox(self, text):
        widget = self.tabWidget.currentWidget()
        widget.setText(text)

    def stack_command(self, cmd):
        index = self.tabWidget.currentIndex()
        widget = self.commandWidgetList[index]
        widget.moveCursor(qt.QTextCursor.End)
        widget.insertPlainText(cmd+'\n')
        widget.moveCursor(qt.QTextCursor.End)


class CodeEditor(qt.QLineEdit):
    """
    QLineEdit widget with treatment function autocompletion
    """
    def __init__(self, parent=None, completerList=[]):
        super().__init__()
        # self.setTabStopDistance(
            # qt.QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)
        # self.highlighter = PythonHighlighter(self.document())

        completer = qt.QCompleter(completerList)
        self.setCompleter(completer)
        # self.setFixedHeight(30)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)
        self.completerList = completerList

    def generateMenu(self, event):
        menu = qt.QMenu()
        for fun in moduledescription.get_commandList(xeuss):
            menu.addAction(fun, self.actionClicked)
        menu.exec_(self.mapToGlobal(event))

    def actionClicked(self):
        action = self.sender()
        completer = self.completer()
        # print(self.completer.model())
        self.setText(action.text())


class MyCompleter(qt.QCompleter):
    insertText = qt.pyqtSignal(str)

    def __init__(self, parent=None, completerList=[]):
        super(MyCompleter, self).__init__(completerList, parent)
        self.setCompletionMode(qt.QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected


class MultiLineCodeEditor(qt.QPlainTextEdit):
    def __init__(self, parent=None, completerList=[]):
        super(MultiLineCodeEditor, self).__init__(parent)
        self.completer = MyCompleter(completerList=completerList)
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insertCompletion)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)
        self.completerList = completerList
        self.setMinimumHeight(25)
        self.highlighter = qt.Qt

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(qt.QTextCursor.Left)
        tc.movePosition(qt.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        qt.QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        tc = self.textCursor()
        if event.key() == qt.Qt.Key_Tab and self.completer.popup().isVisible():
            self.completer.insertText.emit(self.completer.getSelected())
            self.completer.setCompletionMode(qt.QCompleter.PopupCompletion)
            return

        qt.QPlainTextEdit.keyPressEvent(self, event)
        tc.select(qt.QTextCursor.WordUnderCursor)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 0:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                        + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def generateMenu(self, event):
        menu = qt.QMenu()
        for fun in self.completerList:
            menu.addAction(fun, self.actionClicked)
        menu.exec_(self.mapToGlobal(event))

    def actionClicked(self):
        action = self.sender()
        text = action.text()
        tc = self.textCursor()
        # extra = len(text)
        # tc.movePosition(qt.QTextCursor.Left)
        # tc.movePosition(qt.QTextCursor.EndOfWord)
        # tc.insertText(completion[-extra:])
        tc.insertText(text)
        tc.movePosition(qt.QTextCursor.EndOfWord)
        self.setTextCursor(tc)


class DataView(PlotWindow):

    def __init__(self, fitmanager=None):
        super().__init__(backend=None, resetzoom=True,
                         autoScale=True, logScale=True,
                         grid=False, curveStyle=True, colormap=True,
                         aspectRatio=True, yInverted=True,
                         copy=True, save=True, print_=True,
                         control=True, position= [('X', lambda x, y: x),
                                                  ('Y', lambda x, y: y),
                                                  ('Data', self._zValue)],
                         roi=False, mask=True, fit=False)
        # """Widget displaying information"""
        # posInfo = [('X', lambda x, y: x),
        #            ('Y', lambda x, y: y),
        #            ('Data', self._zValue)]
        # plot widget
        """Widget displaying information"""
        posInfo = [('X', lambda x, y: x),
                   ('Y', lambda x, y: y),
                   ('Data', self._zValue)]
        # custom fitmanager fit action

        if fitmanager is None:
            fitmanager = FitManager()
        if not len(fitmanager.theories):
            fitmanager.loadtheories(fittheories)
        fitAction = CustomFitAction(self, parent=self, fitmanager=fitmanager)
        self.fitAction = self.group.addAction(fitAction)
        self.fitAction.setVisible(True)
        self.addAction(self.fitAction)
        self._toolbar.addAction(fitAction)

        self.roiManager = RegionOfInterestManager(self)
        self.roiManager.setColor('pink')
        self.roiManager.sigRoiAdded.connect(self.updateAddedRegionOfInterest)
        self.addToolBarBreak()
        action = self.roiManager.getInteractionModeAction(RectangleROI)
        toolbar = qt.QToolBar('')
        toolbar.addAction(action)
        findCenterAction = qt.QAction(self)
        findCenterAction.setIcon(getQIcon('target.ico'))
        findCenterAction.setToolTip('find beam on the current ROI')
        findCenterAction.triggered.connect(self.findCenter)
        toolbar.addAction(findCenterAction)
        self.addToolBar(toolbar)
        legendWidget = self.getLegendsDockWidget()
        # self.plotWindow.setDockOptions()
        legendWidget.setAllowedAreas(qt.Qt.TopDockWidgetArea)
        self.profileTools = Profile.ProfileToolBar(parent=self,
                                                   plot=self)
        self.addToolBar(self.profileTools)
        self.setDefaultColormap(colors.Colormap(name='jet', normalization='log',
                                                vmin=None, vmax=None, autoscaleMode='stddev3')
                                )
        # roi table widget
        # self.roiDock = qt.QDockWidget('rois', self)
        # # self.treatmentDock.setStyleSheet("border: 5px solid black")
        # self.roiDock.setFeatures(qt.QDockWidget.DockWidgetFloatable |
        #                          qt.QDockWidget.DockWidgetMovable)
        # self.roiTableWidget = RegionOfInterestTableWidget(self)
        # self.roiTableWidget.setRegionOfInterestManager(self.roiManager)
        # self.roiDock.setWidget(self.roiTableWidget)
        # self.roiDock.setFloating(False)
        # replace the addTabbedwidget metho of the plot window
        # self._dockWidgets.append(self.roiDock)
        # self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.roiDock)

    def updateAddedRegionOfInterest(self, roi):
        """Called for each added region of interest: set the name"""
        roisList = self.roiManager.getRois()
        if len(roisList)>1:
            self.roiManager.removeRoi(roisList[0])
        roisList = self.roiManager.getRois()
        if roi.getName() == '':
            roi.setName('ROI %d' % len(self.roiManager.getRois()))
        # if isinstance(roi, LineMixIn):
        #     roi.setLineWidth(1)
        #     roi.setLineStyle('--')
        # if isinstance(roi, SymbolMixIn):
        #     roi.setSymbolSize(5)
        if isinstance(roi, RectangleROI):
            roi.setSelectable(True)
            roi.setEditable(True)

    def _zValue(self, x, y):
        value = '-'
        valueZ = - float('inf')
        for image in self.getAllImages():
            data = image.getData(copy=False)
            if image.getZValue() >= valueZ:  # This image is over the previous one
                ox, oy = image.getOrigin()
                sx, sy = image.getScale()
                row, col = (y - oy) / sy, (x - ox) / sx
                if row >= 0 and col >= 0:
                    # Test positive before cast otherwise issue with int(-0.5) = 0
                    row, col = int(row), int(col)
                    if row < data.shape[0] and col < data.shape[1]:
                        value = data[row, col]
                        valueZ = image.getZValue()
        return value

    def findCenter(self):
        roisList = self.roiManager.getRois()
        if roisList:
            if isinstance(roisList[0], RectangleROI):
                point = roisList[0].getOrigin()
                size = roisList[0].getSize()
                for image in self.getAllImages():
                    data = image.getData(copy=False)
                    center = center_of_mass(data[int(point[1]):int(point[1])+int(size[1]),int(point[0]):int(point[0])+int(size[0])])
                    roiCenter = CrossROI()
                    absoluteCenter = [center[1]+int(point[0]), center[0]+int(point[1])]
                    roiCenter.setPosition(np.array(absoluteCenter))
                    label = 'beam center\n x0 : %.3f y0: %.3f' % (absoluteCenter[0], absoluteCenter[1])
                    roiCenter.setName(label)
                    self.roiManager.addRoi(roiCenter)


            # if image.getZValue() >= valueZ:  # This image is over the previous one
            #     ox, oy = image.getOrigin()
            #     sx, sy = image.getScale()
            #     row, col = (y - oy) / sy, (x - ox) / sx
            #     if row >= 0 and col >= 0:
            #         # Test positive before cast otherwise issue with int(-0.5) = 0
            #         row, col = int(row), int(col)
            #         if row < data.shape[0] and col < data.shape[1]:
            #             value = data[row, col]
            #             valueZ = image.getZValue()
# TODO : finish it
class DataView3Dectectors(PlotWindow):

    def __init__(self):
        super().__init__(backend=None, resetzoom=True,
                         autoScale=True, logScale=True,
                         grid=False, curveStyle=True, colormap=True,
                         aspectRatio=True, yInverted=True,
                         copy=True, save=True, print_=True,
                         control=True, position=[('X', lambda x, y: x),
                                                 ('Y', lambda x, y: y),
                                                 ('Data', self._zValue)],
                         roi=False, mask=True, fit=True)
        layout = qt.QGridLayout()
        layout.addWidget(self.getWidgetHandle(), 0, 1)
        self.left_detector = PlotWidget(parent=self)
        self.left_detector.setMaximumWidth(200)
        self.bot_detector = PlotWidget(parent=self)
        self.bot_detector.setMaximumHeight(200)
        layout.addWidget(self.left_detector, 0, 0, 2, 1)
        layout.addWidget(self.bot_detector, 1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)
        centralWidget = qt.QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def _zValue(self, x, y):
        value = '-'
        valueZ = - float('inf')
        for image in self.getAllImages():
            data = image.getData(copy=False)
            if image.getZValue() >= valueZ:  # This image is over the previous one
                ox, oy = image.getOrigin()
                sx, sy = image.getScale()
                row, col = (y - oy) / sy, (x - ox) / sx
                if row >= 0 and col >= 0:
                    # Test positive before cast otherwise issue with int(-0.5) = 0
                    row, col = int(row), int(col)
                    if row < data.shape[0] and col < data.shape[1]:
                        value = data[row, col]
                        valueZ = image.getZValue()
        return value


# TODO: finish it
class TreatmentWorksheetWidget(qt.QWidget):

    def __init__(self, parent=None):
        super(TreatmentWorksheetWidget, self).__init__(parent=parent)



# class TreatmentWidget(qt.QWidget):
#     stackCommandClicked = qt.pyqtSignal(str)
#     runClicked = qt.pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(TreatmentWidget, self).__init__(parent=parent)
#         self.functionComboBox = qt.QComboBox(self)
#         self.descriptionDict = {}
#         self.functionComboBox.currentIndexChanged.connect(self.on_function_selected)
#
#     def setModule(self, module):
#         self.descriptionDict = moduledescription.get_descriptionDict(module, decorator='@nxlib.treatment_function')
#         self.functionComboBox.clear()
#         self.functionComboBox.addItems(self.descriptionDict.keys())
#
#     def on_function_selected(self,i):
#         self.findChildren()

class FunctionListWidget(qt.QWidget):
    runFunction = qt.pyqtSignal(str)
    stackFunction = qt.pyqtSignal(str)

    def __init__(self, parent=None, module=None):
        super(FunctionListWidget, self).__init__(parent=parent)
        self.runButton = qt.QPushButton('run', parent=self)
        self.stackButton = qt.QPushButton('stack', parent=self)
        self.stackButton.setToolTip('copy the command to treament script tab')
        self.comboBox = qt.QComboBox(self)
        self.helpPlainText = qt.QPlainTextEdit(self)
        self.helpPlainText.setReadOnly(True)

        if module is not None:
            self.module = module
            self.comboBox.addItems(moduledescription.get_functionList(module))
        self.function_description = None
        self.tabWidget = qt.QTabWidget()
        # display function parameters
        self.argumentWidget = qt.QWidget(self)
        # layout of the parameters
        self.formLayout = qt.QFormLayout()
        self.argumentWidget.setLayout(self.formLayout)

        # scroll area for argument layout
        scrollArea1 = qt.QScrollArea(self)
        scrollArea1.setWidgetResizable(True)
        scrollArea1.setWidget(self.argumentWidget)
        # scroll area for help text
        scrollArea2 = qt.QScrollArea(self)
        scrollArea2.setWidget(self.helpPlainText)
        scrollArea2.setWidgetResizable(True)

        self.tabWidget.addTab(scrollArea1, 'parameters')
        self.tabWidget.addTab(scrollArea2, 'help')

        # layout
        vlayout = qt.QVBoxLayout()
        hlayout = qt.QHBoxLayout()
        hlayout.addWidget(self.runButton)
        hlayout.addWidget(self.stackButton)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.comboBox)
        vlayout.addWidget(self.tabWidget)
        # vlayout.addLayout(self.formLayout)
        self.setLayout(vlayout)
        # connect signals
        self.comboBox.currentIndexChanged.connect(self.currentFunctionChanged)
        self.runButton.clicked.connect(self.get_commandLine)
        self.stackButton.clicked.connect(self.stack_command)

    def get_commandLine(self):
        nRow = self.formLayout.rowCount()
        kwarg = {}
        for i in range(nRow):
            widget = self.formLayout.itemAt(i, qt.QFormLayout.FieldRole).widget()
            label = self.formLayout.itemAt(i, qt.QFormLayout.LabelRole).widget()
            value = widget.text()
            if value != '':
                kwarg[label.text()] = value
        command = self.function_description.makeCommandLine(**kwarg)
        self.runFunction.emit(command)
        print(command)

    def stack_command(self):
        nRow = self.formLayout.rowCount()
        kwarg = {}
        for i in range(nRow):
            widget = self.formLayout.itemAt(i, qt.QFormLayout.FieldRole).widget()
            label = self.formLayout.itemAt(i, qt.QFormLayout.LabelRole).widget()
            value = widget.text()
            if value != '':
                kwarg[label.text()] = value
        command = self.function_description.makeCommandLine(**kwarg)
        self.stackFunction.emit(command)

    def currentFunctionChanged(self, index):
        function_name = self.comboBox.itemText(index)
        self.function_description = moduledescription.FunctionDescription(self.module.__dict__[function_name])
        nRow = self.formLayout.rowCount()
        while nRow > 0:
            widget = self.formLayout.itemAt(0, qt.QFormLayout.FieldRole).widget()
            self.formLayout.removeRow(widget)
            self.formLayout.count()
            nRow = self.formLayout.rowCount()

        for arg in self.function_description.args_name:
            if arg != 'root':
                self.formLayout.addRow(arg, qt.QLineEdit(self))
        for key in self.function_description.kwargs:
            default_value = self.function_description.kwargs[key]
            if default_value is not None:
                self.formLayout.addRow(key, qt.QLineEdit(str(default_value), parent=self))
            else:
                self.formLayout.addRow(key, qt.QLineEdit(self))
        # set the help tab with the function docstring
        self.helpPlainText.clear()
        self.helpPlainText.setPlainText(self.function_description.docstring)
    #         self.args_name = []
    #         self.kwargs = {}
    #         self.kwargs_type = {}
    #         self.fullcommand = ''
    #         self.module_name = ''
    #         self.function_name = ''
    #         self.decorator = ''
    #         self.docstring = '

# TODO finish this
class CustomFitAction(FitAction):
    """Custom QAction to open a :class:`FitWidget` and set its data to the
    active curve if any, or to the first curve.

    :param plot: :class:`.PlotWidget` instance on which to operate
    :param parent: See :class:`QAction`
    """

    def __init__(self, plot, parent=None, fitmanager=None):

        super(CustomFitAction, self).__init__(plot, parent=parent)
        self.fitmanager = fitmanager

    def _createToolWindow(self):
        # import done here rather than at module level to avoid circular import
        # FitWidget -> BackgroundWidget -> PlotWindow -> actions -> fit -> FitWidget
        from silx.gui.fit.FitWidget import FitWidget

        window = FitWidget(parent=self.plot, fitmngr=self.fitmanager)
        window.setWindowFlags(qt.Qt.Dialog)
        window.sigFitWidgetSignal.connect(self.handle_signal)
        return window


if __name__ == "__main__":
    os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
    from pygdatax.instruments import sansllb
    from silx.gui.fit import FitWidget
    from silx.math.fit import FitManager
    from numpy import tan, deg2rad
    app = qt.QApplication([])
    # splash_pix = qt.QPixmap('/home/achennev/python/pygdatax/src/pygdatax/resources/empty_cell.png')
    #
    # splash = qt.QSplashScreen(splash_pix, qt.Qt.WindowStaysOnTopHint)
    # splash.setMask(splash_pix.mask())
    # splash.show()
    # app.processEvents()
    #
    warnings.filterwarnings("ignore", category=mplDeprecation)

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
        return tan(2 * deg2rad(x - offset)) * distance / 0.172


    fitm = FitManager()
    # FITMANAGER.loadtheories(fittheories)
    fitm.addtheory("fun2",
                   function=fit_distance_and_offset,
                   parameters=["distance", "offset"]
                   )
    # w = FitWidget(fitmngr=fitm)
    w = DataView(fitmanager=fitm)
    w.show()
    # w.get_commandLine()

    # splash.finish(window)
    result = app.exec_()
    app.deleteLater()
    sys.exit(result)

