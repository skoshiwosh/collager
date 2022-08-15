# collager
Python and PySide2 scripts that create mirrored tiled images from single input image.

GUI version is collager.py that generates 4 combinations of image flipped and tiled. The batch version, collage_cmd.py, accepts input image argument and can tile up to 8 combinations of input image. The batch version also has an optional argument which specifies indices into tile pattern list which is displayed with help (-h or —help) optional argument. These scripts were created for my own use on a personal project for creating generative art.

ToDo:

•    Combine both GUI and batch version into one script that runs either in GUI or batch mode.

•    Add and improve docstrings and comments. 

Files:

•    collager.py - This is GUI version for tiling mirrored input image.

•    collager_done.png - This displays GUI with tiled mirrored images before saving selected. 

•    collager_init.png - This displays initial GUI before any input image is selected.

•    collage_cmd.py - This is a batch version of tiling mirrored images. However up to 8 combinations of tiling and mirroring can be generated. The optional argument -i allows user to give a list of indices from the list of patterns displayed.

•    collager.sh, collage_cmd.sh - These Mac OSX shell scripts allow running underlying python scripts using mayapy that has PySide2 installed. When I first developed these scripts I was using Python 2.7 and did not have PySide2 installed with my generic python installation. I now have Python 3 installed along with PySide2.

