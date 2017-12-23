# Meya Gorbea
# Implement a matrix class
# Project for Intro to self driving car course


import math
from math import sqrt
import numbers


def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")

        if self.h == 1 and self.w == 0:
            return self.g[0][0]

        determinant = ( (self.g[0][0] * self.g[1][1]) - (self.g[0][1] * self.g[1][0]) )
        return determinant


    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        if self.h == 1: # handle 1x1
            return self[0]

        sum = 0 # set up sum for diagonal values
        for i in range(self.h):
            sum += self.g[i][i] # [0][0], [1][1], ... [n][n]
        return sum



    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        if self.h == 1: # 1x1 matrix
            return self[0]


        # 1. reciprocal ( 1/ determinant )
        # 2. swtich around the matrix
        # 3. multiiply by the reciprocal

        # 1
        det = self.determinant() # get determinant for reciprocal
        recip = ( 1 / (det) )

        # 2
        # switch a and d
        temp = self.g[0][0]
        self.g[0][0] = self.g[1][1]
        self.g[1][1] = temp

        # now make b and c negative
        self.g[0][1] = self.g[0][1] * -1
        self.g[1][0] = self.g[1][0] * -1

        # last, multiply the whole matrix by the reciprocal

        # result = (recip * self.g) # wanted to use the rmul * function but was not working for me

        #So make new matrix to hold result.

        result = zeroes(self.h, self.w) #matrix to store result in

        for i in range(self.h):
            for j in range(self.w):
                result[i][j] = (recip * self.g[i][j])

        return result




    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """

        num_rows = self.h
        num_cols = self.w
        new_matrix = zeroes(num_rows, num_cols)

        for i in range(self.h):
            for j in range(self.w):
                untransposed_val = self.g[i][j] # keep separate to put in correct spot in new matrix
                new_matrix[j][i] = untransposed_val
        return new_matrix

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")

        new_grid = []

        for i in range(self.h):
            row = []
            for j in range(self.w):
                v1 = self.g[i][j] # get the two values from matrices
                v2 = other.g[i][j]
                res = v1 + v2
                row.append(res)
            new_grid.append(row) # put into new matrix
        return Matrix(new_grid)


    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        # make all of the values negative by mulitplying by -1
        new_grid = []
        for row in self.g:
            new_row = []
            for value in row:
                new_value = value * -1
                new_row.append(new_value)
            new_grid.append(new_row)
        return Matrix(new_grid)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        # utilize the overloaded addition method
        return self + -other

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        num_rows = self.h
        num_cols = other.w
        new_matrix = zeroes(num_rows, num_cols) #matrix to store result in

        for i in range(self.h):
        # iterate through columns of 'other' matrix
            for j in range(other.w):
            # iterate through rows of 'other' matrix
                for k in range(other.h):
                    new_matrix[i][j] += self.g[i][k] * other.g[k][j]
        return new_matrix

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number): # 'other' should be some number
            new_grid = []
            for row in self.g:
                new_row = []
                for val in row:
                    new_row.append( val * other )
                new_grid.append(new_row)
            return Matrix(new_grid)
