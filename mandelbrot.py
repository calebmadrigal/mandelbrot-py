import random
import math
from tkinter import Tk, Canvas, PhotoImage, mainloop

def mandelbrot(n, steps=20, threashold=2):
    z_prev = n
    z_cur = n
    in_mandelbrot_set = True

    for steps_taken in range(steps):
        z_prev = z_cur
        z_cur = z_prev**2 + n
        if abs(z_cur) > threashold:
            in_mandelbrot_set = False
            break

    return (in_mandelbrot_set, z_cur, steps_taken)


def float_range(start, end, precision=0.1):
    return [i * precision for i in range(int(start/precision), int(end/precision))]


def make_linear_mapper(in_range, out_range, int_out=False):
    """ make_linear_mapper returns a function which maps from the in_range to the out_range, and
    optionally converts to integers in the output if int_out = True. """

    in_delta = in_range[-1] - in_range[0]
    out_delta = out_range[-1] - out_range[0]
    # y = mx + b (m = slope, b = y-intersect)
    m = (out_delta / in_delta)
    # To find b: b = y - mx
    # Just plug in first item of each range
    b = out_range[0] - m * in_range[0]

    def linear_mapper(val):
        return m * val + b

    if int_out:
        mapper = lambda x: int(linear_mapper(x))
    else:
        mapper = linear_mapper

    return mapper


def calc_mandelbrot(real_min, real_max, imag_min, imag_max, precision=0.1):
    points = []
    for r in float_range(real_min, real_max, precision):
        for i in float_range(imag_min, imag_max, precision):
            complex_num = complex(r, i)
            mand = mandelbrot(complex_num)
            print("({}, {}) -> {}".format(r, i, mand))
            points.append(((r, i), mand))

    return points


def display_mandelbrot():
    width = 700
    height = 700
    window = Tk()
    canvas = Canvas(window, width=width, height=height, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=width, height=height)
    canvas.create_image((width//2, height//2), image=img, state="normal")

    real_range = (-2.25, 0.75)
    imag_range = (-1.5, 1.5)
    precision = 0.05

    real_to_x_mapper = make_linear_mapper(real_range, (0, width), int_out=True)
    imag_to_y_mapper = make_linear_mapper(imag_range, (0, height), int_out=True)

    # TODO: Invert graph (even though it's semetric across y)

    m_set = calc_mandelbrot(real_range[0], real_range[1], imag_range[0], imag_range[1], precision)
    for item in m_set:
        point, result = item
        (x, y) = point
        x_pixel = real_to_x_mapper(x)
        y_pixel = imag_to_y_mapper(y)
        (in_mandelbrot_set, z_cur, steps_taken) = result
        color = "#ffffff" if in_mandelbrot_set else "#000000"
        print("plotting: {}, {} -> {}".format(x_pixel, y_pixel, color))
        img.put(color, (x_pixel, y_pixel))

    mainloop()


if __name__ == '__main__':
    display_mandelbrot()

