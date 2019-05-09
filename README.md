# monopng

A Python class to create monochrome (greyscale) PNG images

# What does monopng do?

The `monopng` Python class can be used to create monochrome (greyscale) PNG
images.  There are two stages.  Create an in memory representation using
the methods and then write out the image in `PNG` file format to the
file system.

# Quick start

Running the `boxified.py` program creates a `PNG` image called:

```
Boxified.png
```

This image is in the repository - it makes a nice desktop wallpaper.

The `boxified.py` program is 40 odd lines long including comments and blank lines.  It is
pasted below:

```
#! /usr/bin/python3
#
# @(!--#) @(#) boxified.py, version 001, 09-may-2019
#
# create the "Boxified.png" wallpaper
# 
# this is DEFINITELY NOT Cubism! :-]
#     https://www.tate.org.uk/art/art-terms/c/cubism
#

import sys
import random

import monopng

random.seed(3)

WIDE     = 1920
TALL     = 1080
BOXSIZE  = 64
NUMBOXES = 50

mpng = monopng.MonoPNG(WIDE, TALL)

mpng.fill(255)

widerange = WIDE - (3 * BOXSIZE)
tallrange = TALL - (3 * BOXSIZE)

for i in range(0, NUMBOXES):
    mpng.box(BOXSIZE + random.randrange(0, widerange),
             BOXSIZE + random.randrange(0, tallrange),
             BOXSIZE,
             BOXSIZE,
             64 + random.randrange(0, 128))
    
mpng.write('Boxified.png')

sys.exit(0)
```

--------------------------------

Documentation currently incomplete

--------------------------------

End of README.md
