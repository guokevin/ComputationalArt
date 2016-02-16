"""
This program generates random art
@author Kevin Guo
"""

import random
import math
from PIL import Image
import alsaaudio
import audioop


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    lst1 = ["prod","avg","cos_pi","sin_pi","sqr","abs","x","y"]
    lst2 = [["x"],["y"]]

    rand1 = random.choice(lst1)
    rand2 = random.choice(lst2)

    contin = random.choice([0,1])
    if(min_depth <= 0):
        if(max_depth == 0):
            return rand2
        if(contin == 0):
            return rand2   
    if(rand1 not in ["cos_pi", "sin_pi", "sqr", "abs"]):
        return [rand1,build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
    else:
        return [rand1,build_random_function(min_depth-1,max_depth-1)]

def lambda_function(min_depth, max_depth):
    """
    Use lambda functions to generate a random function to generate art. The function recurses to a random depth between min_depth and max_depth while
    evaluating this function and returns a function that is then evaluated.
    Referenced Sophie's return code
    """
    #Creates references for lamba functions
    prod = lambda x,y: x*y
    avg = lambda x,y: .5*(x+y)
    cos_pi = lambda x,y: math.cos(math.pi*x)
    sin_pi = lambda x,y: math.sin(math.pi*x)
    sqr = lambda x,y: x**2
    ab = lambda x,y: math.fabs(x)
    returnx = lambda x,y: x
    returny = lambda x,y: y

    lambda_list = [prod, avg, cos_pi, sin_pi, sqr, ab, returnx, returny]

    #Random depth option
    contin = random.choice([0,1])

    #Returns random base case
    base = random.choice([returnx, returny])
    
    if(min_depth <= 0):
        if(max_depth == 0):
            return base
        if(contin == 0):
            return base

    function = random.choice(lambda_list)
    #creates inputs for the randomly generated function to recurse into
    input_x = lambda_function(min_depth-1, max_depth-1)
    input_y = lambda_function(min_depth-1, max_depth-1)
    return lambda x,y: function(input_x(x,y),input_y(x,y))

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if(len(f) == 1):
        if(f[0] == "x"):
            return x
        else:
            return y
    if(f[0] == "x"):
        return evaluate_random_function(f[1],x,y)
    if(f[0] == "y"):
        return evaluate_random_function(f[2],x,y)
    if(f[0] == "prod"):
        return evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y)
    if(f[0] == "avg"):
        return .5*(evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))
    if(f[0] == "cos_pi"):
        return math.cos(math.pi* evaluate_random_function(f[1],x,y))
    if(f[0] == "sin_pi"):
        return math.sin(math.pi* evaluate_random_function(f[1],x,y))
    if(f[0] == "sqr"):
        return  evaluate_random_function(f[1],x,y)**2
    if(f[0] == "abs"):
        return math.fabs(evaluate_random_function(f[1],x,y))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    frac = float(val - input_interval_start)/(input_interval_end - input_interval_start)
    return frac * (output_interval_end - output_interval_start) + output_interval_start

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = lambda_function(2,6)
    green_function = lambda_function(2,6)
    blue_function = lambda_function(2,6)
    im = Image.new("RGB", (x_size, y_size))
    
    # Create image and loop over all pixels
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function(x,y)),
                    color_map(green_function(x,y)),
                    color_map(blue_function(x,y))
                    )
    im.save(filename)


if __name__ == '__main__':
    # inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
    # inp.setchannels(1)
    # inp.setrate(16000)
    # inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    # inp.setperiodsize(160)
            
    # while True:
    #     l,data = inp.read()
    #     if l:
    #             print audioop.rms(data,2)
    # import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(build_random_function,globals(),verbose=True)
    # print(build_random_function(1,5))


    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart7.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
    # image_viewer()

