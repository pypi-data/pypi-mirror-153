#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy

from mirmag.logger import get_logger


logger = get_logger(logger_name="matrix", log_to_console=True)


class Matrix(object):
    """ A Matrix class to use in the Hidden Markov Models ro predict miRNAs and pre-miRNAs.

    Parameters
    ----------
    m : int
        Number of the rows.
    n : int
        Number of the columns.
    array : numpy.array
        МасNumpy array ti store matrix elements.

    Returns
    -------
    Matrix object : object
        Matrix object with specific methods.
    """

    def __init__(self, **kwargs):
        """ Initialize Matrix object by its shape.

        :param kwargs: The number of columns and rows of the Matrix.
        """

        # init
        self.m = 0      # rows    / строки
        self.n = 0      # columns / столбцы
        self.v = numpy.zeros((0, 0), numpy.double)

        # Fill the class variables
        try:
            if "m" in kwargs.keys() and "n" in kwargs.keys():
                self._init_mn(kwargs["m"], kwargs["n"])
            elif "array" in kwargs.keys():
                self._init_array(kwargs["array"])
            elif not kwargs.keys():
                self._init_empty_object()
            else:
                raise Exception(f"Matrix was trying to be created with incorrect parameters.")

        except Exception:
            logger.exception(f"Error while creating the Matrix object.\nParameters: {kwargs}.")

    def _init_mn(self, m: int, n: int) -> None:
        """ Create matrix with shape [m x n]. """
        self.m = m
        self.n = n
        self.v = numpy.zeros(shape=(m, n), dtype=numpy.double)

    def _init_array(self, arr: numpy.array) -> None:
        """ Create matrix from the existing one. """
        self.v = arr.astype(dtype=numpy.double)
        self.m, self.n = arr.shape

    def _init_empty_object(self) -> None:
        """ Create empty matrix with shape [0 x 0]. """
        self._init_mn(0, 0)

    def __str__(self):
        numpy.set_printoptions(formatter={"float": "{: 0.4f}".format})
        return str(self.v)

    def __repr__(self):
        return self.__str__()

    def get_value(self, m: int, n: int) -> float:
        return self.v[m, n]

    def get_array(self) -> numpy.array:
        return self.v.copy()

    def set_value(self, m: int, n: int, value: float) -> None:
        self.v[m, n] = value

    def inc_value(self, m: int, n: int) -> None:
        self.v[m, n] += 1

    def transponize(self) -> None:
        """ Transpose the matrix if it is square. """
        if self.m == self.n:
            self.v = numpy.transpose(self.v)

    def normalize(self, partial: bool) -> None:
        """ Normalize the matrix by the rows. // Transition from a row to a column.

        :param partial: Partial normalization? True (Да), False (Нет).
        """

        if self.m == 0 or self.n == 0:
            return

        summ = self.v.sum(axis=1)   # array of sum for each row
        for i in range(self.m):
            for j in range(self.n):
                if summ[i] != 0.0:
                    self.v[i, j] /= summ[i]

        if partial:
            self.v[self.m - 1, 0] = 1/3         # Yep, it's magic number!
            self.v[self.m - 1, 1] = 2/3         # And it's too.
            for i in range(2, self.n):
                self.v[self.m - 1, i] = 0.0     # And here ... =(


if __name__ == "__main__":
    """ Examples / Use cases. """

    matrix = Matrix(m=5, n=5)
    matrix.set_value(1, 2, 3)
    matrix.set_value(2, 3, 4)
    matrix.inc_value(2, 4)
    matrix.inc_value(3, 3)
    print(matrix, "\n")

    matrix.transponize()
    print(matrix, "\n")

    matrix.normalize(partial=True)
    print(matrix, "\n")

    matrix.transponize()
    print(matrix, "\n")

    matrix.inc_value(4, 0)
    matrix.inc_value(4, 1)
    matrix.inc_value(4, 2)
    print(matrix, "\n")

    matrix.normalize(partial=False)
    print(matrix, "\n")
