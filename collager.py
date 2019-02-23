#!/usr/bin/env python
'''
    Launch window to create mirrored tiled images from source image file
    
    File name: collager.py
    Author: Suzanne Berger
    Date created: 03/15/2018
    Python Version: 2.7
'''

import sys
import os
import logging
from pprint import pprint

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2 import QtUiTools

#########################################################
# globals
#########################################################

VERSION = "V01"

logging.basicConfig(level=logging.INFO)
logging.info( " %s Version %s" % (sys.argv[0], VERSION))

#########################################################
# CollagerWin
#########################################################

class CollagerWin(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        
        self.cllimagemap = {}
        self.image_dir = self.image_file = None
        
        self.empty_pixmap = QtGui.QPixmap(300, 200)
        self.empty_pixmap.fill(QtGui.QColor(120, 120, 160))
        
        self._initUI()
        self._connectSignals()
        self.show()

    def _initUI(self):
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
        self.src_button.clicked.connect(self.on_src_clicked)
        self.buttonbox.rejected.connect(self.close)
        self.buttonbox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save)
        self.buttonbox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
    
    def closeEvent(self, event):
        event.accept()
    
    def save(self):
        if self.image_dir is None:
            self.status_lineEdit.setText("Unable to save without directory setting")
            return
        
        self.status_lineEdit.setText("Saving collages to directory: %s" % self.image_dir)
        
        for cllkey, value in self.cllimagemap.iteritems():
            this_groupBox = value[0]
            if this_groupBox.isChecked():
                this_lineEdit_objectname = "%s_lineEdit" % cllkey
                this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
                this_path = os.path.normpath(os.path.join(self.image_dir, this_lineEdit.text()))
                this_image = value[-1]
                this_image.save(this_path, quality=100)
                logging.info("Saving collage %s to image file %s" % (cllkey, this_path))
            
        self.status_lineEdit.setText("Successfully saved all collages to %s" % self.image_dir)
    
    def reset(self):
        logging.info("Resetting collage window")
        self.src_lineEdit.clear()
        self.image_dir = self.image_file = None
        for cllkey, value in self.cllimagemap.iteritems():
            this_groupBox = self.cllimagemap[cllkey][0]
            this_groupBox.setChecked(True)
            self.cllimagemap[cllkey] = [this_groupBox]
            
            this_lineEdit_objectname = "%s_lineEdit" % cllkey
            this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
            this_lineEdit.clear()
            
            this_label_objectname = "%s_label" % cllkey
            this_label = this_groupBox.findChild(QtWidgets.QLabel, this_label_objectname)
            this_label.setPixmap(self.empty_pixmap)
        
        self.status_lineEdit.setText("Ready:")

    def on_src_clicked(self):
        self.srcfile = QtWidgets.QFileDialog.getOpenFileName(self,'Load Image File','/Users/suzanneberger/Pictures',
                                                     "image files (*.jpg *.png *.tif)")[0]

        if self.srcfile is not None:
            self.src_lineEdit.setText(self.srcfile)
            self.image_dir,self.image_file = os.path.split(self.srcfile)
            self.mkcllpix()

    def mkbox(self, cllkey, this_groupBox):
        self.cllimagemap[cllkey] = [this_groupBox]
        this_groupBox.setCheckable(True)
        this_groupBox.setChecked(True)
        this_groupBox.setObjectName("%s_groupBox" % cllkey)

        this_lineEdit = QtWidgets.QLineEdit()
        this_lineEdit.setFixedHeight(21)
        this_lineEdit.setFixedWidth(300)
        this_lineEdit.setObjectName("%s_lineEdit" % cllkey)
        
        this_label = QtWidgets.QLabel()
        this_label.setPixmap(self.empty_pixmap)
        this_label.setObjectName("%s_label" % cllkey)
        
        this_layout = QtWidgets.QVBoxLayout()
        this_layout.addWidget(this_lineEdit)
        this_layout.addWidget(this_label)
        this_groupBox.setLayout(this_layout)

    def mkcllpix(self):
        self.build_collages()
    
        for i in range(4):
            cllkey = 'cll%d' % i
            if cllkey not in self.cllimagemap:
                print("should raise exception")
                continue
            
            this_groupBox = self.cllimagemap[cllkey][0]
            
            parts = self.image_file.split('.')
            parts[0] = parts[0] + '_' + cllkey
            this_cll_file = '.'.join(parts)
            this_lineEdit_objectname = "%s_lineEdit" % cllkey
            this_lineEdit = this_groupBox.findChild(QtWidgets.QLineEdit, this_lineEdit_objectname)
            this_lineEdit.setText(this_cll_file)
            
            this_image = self.cllimagemap[cllkey][-1]
            this_pixmap = QtGui.QPixmap(this_image).scaledToWidth(300)
            
            this_label_objectname = "%s_label" % cllkey
            this_label = this_groupBox.findChild(QtWidgets.QLabel, this_label_objectname)

            if this_label is None:
                print("should raise exception")
                continue

            this_label.setPixmap(this_pixmap)


    def build_collages(self):
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
            
            cllkey = 'cll%d' % i
            if cllkey in self.cllimagemap:
                self.cllimagemap[cllkey].append(target_image)
                logging.info("Adding collage %s to image map" % cllkey)
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
    sys.exit(app.exec_())


