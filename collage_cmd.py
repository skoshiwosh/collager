#!/usr/bin/env python
""" Create mirrored and tiled images from input image.
    
Args:
    image_path: Full path to input image to be tiled.
    patterns: Optional argument with flag -i or --index specifying
        indicies from list of patterns displayed under --help.
        Default is None which will generate all 8 mirrored tiled patterns.

Returns:
    saves all generated images in the same directory as input image

File: collage_cmd.py
Author: Suzanne Berger
Date: 11/25/2017
Updated: 01/24/2023
Python Version: 3.9
"""


import sys
import os
import argparse
import logging
from pprint import pprint

from PySide2 import QtCore, QtGui

#########################################################
# globals
#########################################################

VERSION = "V05"

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logging.info( f" {sys.argv[0]} Version {VERSION}")


#########################################################
# methods
#########################################################

def get_src(image_path):
    """ Return image directory and image file derived from input file directory path. """
    parts = os.path.split(image_path)
    image_dir = parts[0]
    image_file = parts[1]
    return image_dir, image_file

def parse_indices(indices):
    """ Return integer list of indices converted from input string. """
    inx_list = indices.split(',')
    pattern_indices = []
    for each in inx_list:
        if each.isdigit():
            pattern_indices.append(int(each))
        else:
            pattern_indices.extend(range(int(each[0]),int(each[-1])+1))
    return pattern_indices

def tile_one(image_path, image_dir, image_file):
    """ Create one 4 piece tiled image from input image file. """
    src_image = QtGui.QImage(image_path)
    src_width = src_image.width()
    src_height = src_image.height()

    parts = os.path.splitext(image_file)
    target_path = os.path.normpath(os.path.join(image_dir, f"{parts[0]}_tile.jpg"))

    src_width = src_image.width()
    src_height = src_image.height()
    target_width = src_width * 2
    target_height = src_height * 2

    target_image = QtGui.QImage(target_width, target_height, QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(target_image)
    
    painter.drawImage(0, 0, src_image)
    painter.drawImage(src_width-1, 0, src_image)
    painter.drawImage(0, src_height-1, src_image)
    painter.drawImage(src_width-1, src_height-1, src_image)
    target_image.save(target_path,quality=100)

    painter.end()
    return

def build_collage(image_path, image_dir, image_file, indices):
    """ Create up to 8 combinations of 4 piece mirrored and tiled input image. """
    src_image = QtGui.QImage(image_path)
    src_width = src_image.width()
    src_height = src_image.height()
    
    src_imageH = src_image.mirrored(True, False)
    src_imageV = src_image.mirrored(False, True)
    src_imageHV = src_image.mirrored(True, True)
    
    parts = os.path.splitext(image_file)
    if len(indices) > 1:
        imageH_path = os.path.normpath(os.path.join(image_dir, f'{parts[0]}_H{parts[1]}'))
        src_imageH.save(imageH_path,quality=100)
        imageV_path = os.path.normpath(os.path.join(image_dir, f'{parts[0]}_V{parts[1]}'))
        src_imageV.save(imageV_path,quality=100)
        imageHV_path = os.path.normpath(os.path.join(image_dir, f'{parts[0]}_HV{parts[1]}'))
        src_imageHV.save(imageHV_path,quality=100)
    
    patterns = [[src_image, src_imageH, src_imageV, src_imageHV],
                [src_imageH, src_image, src_imageHV, src_imageV],
                [src_imageHV, src_imageV, src_imageH, src_image],
                [src_imageV, src_imageHV, src_image, src_imageH],
                [src_image, src_image, src_image, src_image],
                [src_image, src_image, src_imageV, src_imageV],
                [src_imageH, src_imageH, src_image, src_image],
                [src_imageHV, src_imageHV, src_image, src_image],
                ]
    
    src_width = src_image.width()
    src_height = src_image.height()
    target_width = src_width * 2
    target_height = src_height * 2
    
    logging.info(f" src_width = {src_width} src_height = {src_height}")
    logging.info(f" target_width = {target_width} target_width = {target_height}")
    
    target_image = QtGui.QImage(target_width, target_height, QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(target_image)
    src_images = []
    #for i in range(len(patterns)):        *** previously could only generate entire list of patterns
    for i in indices:
        target_path = os.path.normpath(os.path.join(image_dir, f"{parts[0]}_CLL{i}.jpg"))
        src_images = patterns[i]
        painter.drawImage(0, 0, src_images[0])
        painter.drawImage(src_width-1, 0, src_images[1])
        painter.drawImage(0, src_height-1, src_images[2])
        painter.drawImage(src_width-1, src_height-1, src_images[3])
        target_image.save(target_path,quality=100)
    
    painter.end()
    return

def msg():
    patterns = '''
    pattern indices:
        0 = [src_image, src_imageH, src_imageV, src_imageHV]
        1 = [src_imageH, src_image, src_imageHV, src_imageV]
        2 = [src_imageHV, src_imageV, src_imageH, src_image]
        3 = [src_imageV, src_imageHV, src_image, src_imageH]
        4 = [src_image, src_image, src_image, src_image]
        5 = [src_image, src_image, src_imageV, src_imageV]
        6 = [src_imageH, src_imageH, src_image, src_image]
        7 = [src_imageHV, src_imageHV, src_image, src_image]
    '''
    print(patterns)
    return

#########################################################
# main
#########################################################

if __name__ == '__main__':
    """ Generate combinations of mirrored tiled images from input image file. """
    # parse arguments
    parser = argparse.ArgumentParser(description = 'Tile source image in specified patterns', usage=msg())
    parser.add_argument('-i', '--index', action='store', dest='patterns', default=None, help='optional index list of patterns')
    parser.add_argument('image_path', action='store', help='input image file path to be tiled')
    args = parser.parse_args()
    
    logging.debug(f" args: {args}")
    
    if not os.path.isfile(args.image_path):
        logging.error(f" Invalid file argument: {args.image_path}\n")
        parser.print_help()
        sys.exit(1)
    
    image_dir, image_file = get_src(args.image_path)
    if (args.patterns is None):
        build_collage(args.image_path, image_dir, image_file, list(range(8)))
    elif args.patterns == '4':
        tile_one(args.image_path, image_dir, image_file)
    else:
        indices = parse_indices(args.patterns)
        logging.debug(f"pattern indices: {indices}")
        build_collage(args.image_path, image_dir, image_file, indices)

    logging.info(f" Successfully Collaged {args.image_path}")

    sys.exit()
