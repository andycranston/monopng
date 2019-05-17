# monopng

A Python class to create monochrome (grayscale) PNG images

# What does monopng do?

The `monopng` Python class can be used to create monochrome (grayscale) PNG
images.  There are two stages.  Create an in memory representation using
the methods and then write out the image in `PNG` file format to the
file system using the `write` method.

# Quick start

Run the `boxified.py` Python program as follows:

```
python boxified.py
```

If there are no errors the program will create a  PNG image called:

```
Boxified.png
```

The image is 1920 pixels across and 1080 tall.  This image is in the repository.

Personally I think it makes a nice desktop wallpaper.

The `boxified.py` program that creates this image is only 40 odd lines long
including comments and blank lines.

# More detail for programmers

The `monopng` Python class is defined on a file called `monopng.py`.  Place this file
in a directory where it can be found by standard import searches.  Then all that is
required to import it is:

```
import monopng
```

To create an instance of the `monopng` class use:

```
mpng = monopng.MonoPng(wide, tall)
```

where `wide` is the number of pixels across the image will be and `tall` is
the number of pixels high the image will be.

By default the image will be filled with pixels of value 0.

Valid pixel values are between 0 and 255 inclusive.  A value of 0 is solid black, a value
of 255 is white and values inbetween are varying shades of grey.

The is a method called `fill` which fills an entire image with pixels of a specified
value.  For example to fill the `mpng` image created above with white pixels use:

```
mpng.fill(255)
```

To set a specific pixel to a specific value use the `plot` method.  For example:

```
mpng.plot(10, 20, 128)
```

will set the pixel located 11 pixels across from the left veritical edge of the image
and 21 pixels down from the top horizontal edge to a pixel value of 128.

Pixel coordinates are zero based.  That means that for an image 100 pixels wide and 50
pixels deep:

+ 0,0 is the top left hand corner
+ 99, 0 is the top right hand corner
+ 0,49 is the bottom left hand corner
+ 99,49 is the bottom right hand corner

The is a method called `box` - here is an example use:

mpng.box(25, 10, 50, 30, 192)

This creates a solid box 50 pixels wide by 30 pixels deep of pixel valu 192 (a nice
dark grey).  The left hand corner of the box is at pixel coordinates 25, 10.

To write the PNG image to a file use the `write` method.  For example:

```
mpng.write('image.png')
```

will create a file called `image.png` in the current directory.

The `boxified.py` Python program should now be easy to understand and, for more fun,
easy to alter and expand on so more interesting images can be created.

## Other methods

There are other methods available.  Rather than document all of them here
just go and look at the `monopng.py` file.  However, some worth mentioning now:

### rectangle

```
rectangle(x, y, wide, hight, brightness, thickness=1)
```

Draws a rectangle.  The line wide defaults to 1 pixel.

### horizline

```
horizline(x, y, llength, brightness)
```

Draws a horizontal line 1 pixel wide.  Start at coordinate x,y and move across
to the right hand side of the image for llength pixels.

### vertiline

```
vertiline(x, y, llength, brightness)
```

Draws a vertical line 1 pixel wide.  Start at coordinate x,y and move down to the
bottom edge of the image for llength pixels.

## Why not use one of many existing image libraries?

Good question.  Here are my answers:

+ I liked the challenge of doing this myself.
+ Almost no bloat - the first working version of `monopng.py` is no more that 140 lines of code.
+ Easy to learn.

# Implementation details

The bulk of the work is done by the `zlib` library - in particular the `compress` method.

There is a helper function (I think that is the correct name) called `dword` for
turning an integer into a series of 4 bytes.  It works but I am not sure if it
is coded in the most elegant or Pythonic way.

--------------------------------

End of README.md
