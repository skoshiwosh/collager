#!/usr/bin/env python3
"""
    Launch GUI to create mirrored tiled images from source image file.
    
    File: collager.py
    Author: Suzanne Berger
    Date created: 03/15/2018
    Updated: 03/03/2024
    Python Version: 3.9
"""

import sys
import os
import logging
from pprint import pprint

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtUiTools

#########################################################
# globals
#########################################################

VERSION = "V06"

logging.basicConfig(level=logging.INFO)
logging.info(f" {sys.argv[0]} Version {VERSION}")

#########################################################
# CollagerWin
#########################################################

class CollagerWin(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """ Create CollagerWin object inherited from QWidget. """
        QtWidgets.QWidget.__init__(self, parent)
        
        # initialize object attributes
        # tiled images are stored in dictionary before saving to files
        self.cllimagemap = {}
        self.image_dir = self.image_file = None
        self.empty_pixmap = QtGui.QPixmap(300, 200)
        self.empty_pixmap.fill(QtGui.QColor(120, 120, 160))
        
        # initialize user interface and signal slot connections
        self._initUI()
        self._connectSignals()
        self.show()

    def _initUI(self):
        """ Create widgets and layout. """
        self.setGeometry(100, 100, 800, 700)
        self.setWindowTitle('Collager')
        
        self.src_label = QtWidgets.QLabel('Source Image File')
        self.src_label.setFixedSize(131,21)
        self.src_lineEdit = QtWidgets.QLineEdit()
        self.src_lineEdit.setFixedHeight(21)
        self.src_lineEdit.setMinimumWidth(500)
        self.src_button = QtWidgets.QPushButton('Browse')
        self.src_button.setFixedSize(91, 35)

        src_layout = QtWidgets.QHBoxLayout()
        src_layout.addWidget(self.src_label)
        src_layout.addWidget(self.src_lineEdit)
        src_layout.addWidget(self.src_button)

        headBox = QtWidgets.QGroupBox()
        headBox.setFixedHeight(60)
        headBox.setMinimumWidth(740)
        headBox.setLayout(src_layout)
        
        imageFrame = QtWidgets.QGroupBox()
        imageFrame.setMinimumSize(760, 600)
        
        # QGroupBox labels denote image tile pattern
        self.cllbox0 = QtWidgets.QGroupBox('N-H-V-HV')
        self.mkbox('cll0', self.cllbox0)
        
        self.cllbox1 = QtWidgets.QGroupBox('H-N-HV-V')
        self.mkbox('cll1', self.cllbox1)

        self.cllbox2 = QtWidgets.QGroupBox('V-HV-N-H')
        self.mkbox('cll2', self.cllbox2)
        
        self.cllbox3 = QtWidgets.QGroupBox('HV-V-H-N')
        self.mkbox('cll3', self.cllbox3)
        
        cll_layout = QtWidgets.QGridLayout()
        cll_layout.addWidget(self.cllbox0, 0, 0)
        cll_layout.addWidget(self.cllbox1, 0, 1)
        cll_layout.addWidget(self.cllbox2, 1, 0)
        cll_layout.addWidget(self.cllbox3, 1, 1)
        imageFrame.setLayout(cll_layout)
        
        status_label = QtWidgets.QLabel('Status')
        status_label.setFixedSize(61,21)
        self.status_lineEdit = QtWidgets.QLineEdit("Ready:")
        self.status_lineEdit.setFixedHeight(21)
        self.status_lineEdit.setMinimumWidth(600)
        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_lineEdit)
        
        self.buttonbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save |
                                                    QtWidgets.QDialogButtonBox.Reset |
                                                    QtWidgets.QDialogButtonBox.Close)
                                                    
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(headBox)
        mainLayout.addWidget(imageFrame)
        mainLayout.addLayout(status_layout)
        mainLayout.addWidget(self.buttonbox)
        self.setLayout(mainLayout)
        
    def _connectSignals(self):
        """ Create signal slot connections. """
        self.src_button.clicked.connect(self.on_src_clicked)
        self.buttonbox.rejected.connect(self.close)
        self.buttonbox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save)
        self.buttonbox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
    
    def closeEvent(self, event):
        event.accept()
    
    def save(self):
        """ Save checked tiled images into same directory as source image file. """
        if self.image_dir is None:
            self.status_lineEdit.setText("Unable to save without directory setting")
            return
        
        self.status_lineEdit.setText(f"Saving collages to directory: {self.image_dir}")
        
        # iterate through dictionary to get each QGroupBox object and tiled QImage
        # only save QImage if QGroupBox object is checked
        for cllkey, value in self.cllimagemap.items():
            this_groupBox = value[0]
            if this_groupBox.isChecked():
                this_lineEdit_objectname = f"{cllkey}_lineEdit"
                this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
                this_path = os.path.normpath(os.path.join(self.image_dir, this_lineEdit.text()))
                this_image = value[-1]
                this_image.save(this_path, quality=100)
                logging.info(f"Saving collage {cllkey} to image file {this_path}")
            
        self.status_lineEdit.setText(f"Successfully saved all collages to {self.image_dir}")
    
    def reset(self):
        """ Reset GUI by clearing entries and setting image boxes to original solid grey. """
        logging.info("Resetting collage window")
        self.srcfile = ""
        self.src_lineEdit.clear()
        self.image_dir = self.image_file = None
        for cllkey, value in self.cllimagemap.items():
            this_groupBox = value[0]
            this_lineEdit_objectname = f"{cllkey}_lineEdit"
            this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
            this_text = this_lineEdit.text()
            logging.info(f"*** {this_text}")
            this_lineEdit.clear()
            #this_lineEdit.update()
            
            this_label_objectname = f"{cllkey}_label"
            this_label = this_groupBox.findChild(QtWidgets.QLabel, this_label_objectname)
            this_label.setPixmap(self.empty_pixmap)
            #this_label.update()

        #self.cllbox0.update()
        #self.cllbox1.update()
        #self.cllbox2.update()
        #self.cllbox3.update()
        
        self.status_lineEdit.setText("Ready:")
        return

    def on_src_clicked(self):
        """ Launch file selection dialog to load source image to be tiled. """
        self.srcfile = QtWidgets.QFileDialog.getOpenFileName(self,'Load Image File','/Users/suzanneberger/Pictures',
                                                     "image files (*.jpg *.png *.tif)")[0]

        if self.srcfile is not None:
            self.src_lineEdit.setText(self.srcfile)
            self.image_dir,self.image_file = os.path.split(self.srcfile)
            self.mkcllpix()

    def mkbox(self, cllkey, this_groupBox):
        """ Setup QGroupBox to contain tiled image and checkable label.
            
            QGroupBox object is stored in dictionary with object name derived from dictionary key.
        """
        self.cllimagemap[cllkey] = [this_groupBox]
        this_groupBox.setCheckable(True)
        this_groupBox.setChecked(True)
        this_groupBox.setObjectName(f"{cllkey}_groupBox")

        this_lineEdit = QtWidgets.QLineEdit()
        this_lineEdit.setFixedHeight(21)
        this_lineEdit.setFixedWidth(300)
        this_lineEdit.setObjectName(f"{cllkey}_lineEdit")
        
        this_label = QtWidgets.QLabel()
        this_label.setPixmap(self.empty_pixmap)
        this_label.setObjectName(f"{cllkey}_label")
        
        this_layout = QtWidgets.QVBoxLayout()
        this_layout.addWidget(this_lineEdit)
        this_layout.addWidget(this_label)
        this_groupBox.setLayout(this_layout)

    def mkcllpix(self):
        """ Set each QGroupBox to image tiled from source image. """
        
        # first create as QImage objects saved in dictionary
        self.build_collages()
    
        # then set each QImage to QPixMap assigned to QGroupBox's QLabel object
        for i in range(4):
            cllkey = f"cll{i}"
            if cllkey not in self.cllimagemap:
                print("should raise exception")
                continue
            
            this_groupBox = self.cllimagemap[cllkey][0]
            
            parts = self.image_file.split('.')
            parts[0] = parts[0] + '_' + cllkey
            this_cll_file = '.'.join(parts)
            this_lineEdit_objectname = f"{cllkey}_lineEdit"
            this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
            this_lineEdit.setText(this_cll_file)
            
            this_image = self.cllimagemap[cllkey][-1]
            this_pixmap = QtGui.QPixmap(this_image).scaledToWidth(300)
            
            this_label_objectname = f"{cllkey}_label"
            this_label = this_groupBox.findChild(QtWidgets.QLabel, this_label_objectname)

            if this_label is None:
                print("should raise exception")
                continue

            this_label.setPixmap(this_pixmap)


    def build_collages(self):
        """ Draw tiled source image in all patterns and save each in dictionary. """
        src_image = QtGui.QImage(self.srcfile)
        src_imageH = src_image.mirrored(True, False)
        src_imageV = src_image.mirrored(False, True)
        src_imageHV = src_image.mirrored(True, True)
        
        patterns = [[src_image, src_imageH, src_imageV, src_imageHV],
                    [src_imageH, src_image, src_imageHV, src_imageV],
                    [src_imageHV, src_imageV, src_imageH, src_image],
                    [src_imageV, src_imageHV, src_image, src_imageH],
                    ]
            
        src_width = src_image.width()
        src_height = src_image.height()
        target_width = src_width * 2
        target_height = src_height * 2
                    
        src_images = []
        self.collages = []
        for i in range(4):
            src_images = patterns[i]
            target_image = QtGui.QImage(target_width, target_height, QtGui.QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter(target_image)
            painter.drawImage(0, 0, src_images[0])
            painter.drawImage(src_width-1, 0, src_images[1])
            painter.drawImage(0, src_height-1, src_images[2])
            painter.drawImage(src_width-1, src_height-1, src_images[3])
            
            cllkey = f"cll{i}"
            if cllkey in self.cllimagemap:
                self.cllimagemap[cllkey].append(target_image)
                logging.info(f"Adding collage {cllkey} to image map")
            else:
                print("should raise exception")
                continue
            
            painter.end()



#########################################################
# main
#########################################################

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    cllwin = CollagerWin()
    sys.exit(app.exec())


