import numpy as np


"""
    File name: bytes.py
    Author: Jacob Gerlach
    Description: Assortment of basic byte vector operations.
    Notes:
        * = Function has associated unit test.
"""

def bit_vect(length, indices):  # *
    """Generates a bit vector, hot at each index in list.

    :param length: Length of vector to generate
    :type length: int
    :param indices: Collection of indices to set to 1, all other set to 0
    :type indices: iterable[int]
    :return: one-hot bit-vector
    :rtype: iterable[int]
    """
    out = np.zeros(length)
    out[indices] = 1
    return out

def remove_hot_overlap(input_vector, reference_vector):  # *
    """Removes overlap from input vector by setting reference vector hot indices to 0.

    :param input_vector: Vector to remove overlapping indices from
    :type input_vector: arraylike
    :param reference_vector: Vector to reference for overlapping indices
    :type reference_vector: arraylike
    :return: input_vector with overlapping indices set to 0
    :rtype: arraylike
    """
    input_vector = np.array(input_vector)
    reference_vector = np.array(reference_vector).astype(bool)
    input_vector[reference_vector] = 0
    return input_vector
