#!/usr/bin/env python
'''
    Generate mirrored tiled images from input source image file
    
    File name: collage_cmd.py
    Author: Suzanne Berger
    Date created: 11/25/2017
    Python Version: 2.7
'''


import sys
import os
import logging
from pprint import pprint

from PySide2 import QtCore, QtGui

#########################################################
# globals
#########################################################

VERSION = "V02"

logging.basicConfig(level=logging.DEBUG)
logging.info( " %s Version %s" % (sys.argv[0], VERSION))


#########################################################
# methods
#########################################################

def get_src(image_path):
    parts = os.path.split(image_path)
    image_dir = parts[0]
    image_file = parts[1]
    return image_dir, image_file

def build_collage(image_path, image_dir, image_file):
    src_image = QtGui.QImage(image_path)
    src_imageH = src_image.mirrored(True, False)
    src_imageV = src_image.mirrored(False, True)
    src_imageHV = src_image.mirrored(True, True)
    
    parts = os.path.splitext(image_file)
    
    imageH_path = os.path.normpath(os.path.join(image_dir, '%s_H%s' % (parts[0], parts[1])))
    src_imageH.save(imageH_path,quality=100)
    imageV_path = os.path.normpath(os.path.join(image_dir, '%s_V%s' % (parts[0], parts[1])))
    src_imageV.save(imageV_path,quality=100)
    imageHV_path = os.path.normpath(os.path.join(image_dir, '%s_HV%s' % (parts[0], parts[1])))
    src_imageHV.save(imageHV_path,quality=100)
    
    patterns = [[src_imageH, src_image, src_imageHV, src_imageV],
                [src_image, src_imageH, src_imageV, src_imageHV],
                [src_imageHV, src_imageV, src_imageH, src_image],
                [src_imageV, src_imageHV, src_image, src_imageH],
                ]
    
    src_width = src_image.width()
    src_height = src_image.height()
    
    target_width = src_width * 2
    target_height = src_height * 2
    target_image = QtGui.QImage(target_width, target_height, QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(target_image)
    src_images = []
    for i in range(4):
        target_path = os.path.normpath(os.path.join(image_dir, "%s_CLL%d.jpg" % (parts[0], i)))
        src_images = patterns[i]
        painter.drawImage(0, 0, src_images[0])
        painter.drawImage(src_width-1, 0, src_images[1])
        painter.drawImage(0, src_height-1, src_images[2])
        painter.drawImage(src_width-1, src_height-1, src_images[3])
        target_image.save(target_path,quality=100)
    
    painter.end()

    return

#########################################################
# main
#########################################################

if __name__ == '__main__':

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        logging.info(" Source Image File %s" % image_path)
        image_dir, image_file = get_src(image_path)
    else:
        logging.error(" Missing Image File Path Argument")
        sys.exit(1)

    build_collage(image_path, image_dir, image_file)
    logging.info(" Successfully Collaged %s" % image_path)

    sys.exit()
