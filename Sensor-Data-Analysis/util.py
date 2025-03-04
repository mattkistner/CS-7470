from scipy.signal import butter, lfilter
import numpy as np
import math

def vector_magnitude(data):
    """ function to calculate the magnitude of a vector

    Calculate the magnitude of the vector superposition of data (for
    example, acceleration) on x, y, and z axis

    Arguments:
        data: array of (x, y, z) tuples for a vector

    Returns:
        array of the magnitude of a vector

    """
    magnitudes = []

    for row in data:
        x = row[1]
        y = row[2]
        z = row[3]
        #print(str(x) + ' ' + str(y) + ' ' + str(z))

        magnitude = math.sqrt((x**2) + (y**2) + (z**2))
        #print(magnitude)
        magnitudes.append(magnitude)

    return magnitudes


def moving_average(data, window_size):
    """ moving average filter

    Implement a simple moving average filter to use as a low pass
    filter

    Arguments:
        data: data be filtered
        window_size: window_size chosen for the data

    Returns:
        The filtered data.

    TODO:
        Finish this function. Think about how you want to handle
        the size difference between your input array and output array.
        You can write it yourself or consider using numpy.convole for
        it:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html

    """

    return np.convolve(data, np.ones(window_size) / window_size, 'valid')
