"""
This program generates random art
"""
import random
import math
from PIL import Image

def lambda_function(min_depth, max_depth):
    prod = lambda x,y: x*y
    avg = lambda x,y: .5*(x+y)
    cos_pi = lambda x,y: math.cos(math.pi*x)
    sin_pi = lambda x,y: math.sin(math.pi*x)
    sqr = lambda x,y: x**2
    ab = lambda x,y: math.fabs(x)
    returnx = lambda x,y: x
    returny = lambda x,y: y

    lambda_list = [prod, avg, cos_pi, sin_pi, sqr, ab, returnx, returny]

    if max_depth == 1:
        func = random.choice(lambda_list[-2:])
        return func

    else:
        func = random.choice(lambda_list)
        in1 = lambda_function(min_depth-1,max_depth-1)
        in2 = lambda_function(min_depth-2,max_depth-1)
        return lambda x,y: func(in1(x, y),in2(x, y))

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    frac = float(val - input_interval_start)/(input_interval_end - input_interval_start)
    return frac * (output_interval_end - output_interval_start) + output_interval_start

def color_map(val):
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = lambda_function(2,6)
    green_function = lambda_function(2,6)
    blue_function = lambda_function(2,6)

    # print "LAMBDA FUNC: ", red_function
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
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

    im.show(filename)


if __name__ == '__main__':

    generate_art("myart50.png")
