# Seychelles Flag Generator

A Python script to convert an image of a flag (or really any image) into one in the style of the flag of the Seychelles, or the other way around.

Made by **Akshay Chitale** for [/r/vexillology](https://www.reddit.com/r/vexillology/) on Reddit.

## How to Use

### Prerequisites

In order to run the Python script, you will, of course, have to have Python installed. The scripts was tested on macOS with both Python 2.7.13 and Python 3.6.4, so either Python 3 or Python 2.7 should work fine.

In addition, you will need to have the Python Imaging Library (PIL) installed. This can be installed with pip (or with pip3):

```
$ pip install Pillow
```

### Running the Script

Download the file `seychelles.py` and run it with Python, passing in the name of the file to process:

```
$ python seychelles.py image_in.png
```

For information about all of the options availible, such as setting the output image size and doing an inverse seychelles operation, use the help option:

```
$ python seychelles.py -h
usage: seychelles.py [-h] [-i] [-s SIZE SIZE] [-n NAME] [-e EXT] [-d] [-v]
                     image_in

positional arguments:
  image_in              Image file to process

optional arguments:
  -h, --help            show this help message and exit
  -i, --inverse         Do inverse seychelles
  -s SIZE SIZE, --size SIZE SIZE
                        Output image width and height
  -n NAME, --name NAME  Output file name
  -e EXT, --ext EXT     Output file extension
  -d, --display         Display output instead of saving to file
  -v, --verbose         Display progress while processing
```

### Advanced Use

You can also write your own script and just import the Seychelles class to do more complicated things than the main script allows for. The Seychelles class has the following methods:

* \_\_init\_\_ - Creates a new Seychelles object
* seychelles - Performs the forward Seychelles flag transformation
* inverse_seychelles - Performs the reverse transformation back to a regular flag
* save - Saves the output image to a file
* show - Displays the output image in the default image viewer

Run `python seychelles.py -h` to see what the arguments to the functions do. The main script just passes the command line arguments to these arguments in the Seychelles class's methods.

Feel free to modify any of the code, like the angle mapping or the algorithm itself, to make your own flag generators!

## Technical Details

The transformation that is performed is a mapping from rectangular coordinates in the input to polar coordinates in the output. The X coordinate corresponds with the radius in the output, and the Y coordinate with the angle in the output. Note that pixels here are referenced with the bottom left being (0,0)

For each pixel of the output, the relative radius and angle of that pixel are computed. The relative radius is the fraction of the radius to the edge of the flag that the pixel is at. The angle is counterclockwise relative to the positive X axis.

There is an angle mapping that ensures that the middle of the input flag, Y = input height/2, corresponds with the diagonal of the output flag. This is ensured by finding the parabola that contains the points (0,0), (output diagonal, pi/4), and (pi/2, pi/2) to generate a function of input angle vs output angle.

Finally, the output pixel is assigned the color from the corresponding input pixel. This pixel is at the same horizontal position as the radius ratio - for example, an output pixel 1/3 of the way to the edge of the flag radually would correspond to an input pixel 1/3 of the way to the edge of the flag horizontally. The Y coordinate is the mapped angle, scaled such that 0 corresonds with Y = 0 and pi/2 corresponds with the top fo the flag, Y = input height.

The inverse operation does the same thing, but in reverse. For example, the angle mapping is a square root function in the inverse opertion instead of a parabola.

Two special properties were maintained for this program:

* The middle of the regular flag on the Y-axis corresponds to the diagonal of the Seychelles style flag.
* The system is invertible. That is, the inverse Seychelles of the Seychelles of an image should (in theory) get you the original image, as should the  Seychelles of the inverse Seychelles of an image. However, since the bottom corner is mapped to the entire left edge in the inverse operation, there will be some noise visible in the inverse operation output, since pixels are discrete.
