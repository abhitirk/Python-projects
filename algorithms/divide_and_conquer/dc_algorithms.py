# -*- coding: utf-8 -*-
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23,
                       18, 20, -7, 12, -5, -22, 15, -4, 7]
# Implement pseudocode from the book


def find_maximum_subarray_brute(A, low, high):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    """
    max_sum = float("-infinity")
    for x in range(low, high - 1):
        t_sum = 0
        for y in range(x, high):
            t_sum += A[y]
            if t_sum > max_sum:
                max_sum = t_sum
                i = x
                j = y
    return (i, j)


def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    """
    left_sum = float("-infinity")
    t_sum = 0
    left_index = mid
    for x in range(mid, low, -1):
        t_sum = t_sum + A[x]
        if t_sum > left_sum:
            left_sum = t_sum
            left_index = x
    right_sum = float("-infinity")
    t_sum = 0
    right_index = mid + 1
    for y in range(mid + 1, high):
        t_sum = t_sum + A[y]
        if t_sum > right_sum:
            right_sum = t_sum
            right_index = y
    return (left_index, right_index)


def find_maximum_subarray_recursive(A, low, high):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    """
    if low == high:
        return (low, high)
    else:
        mid = (low + high) / 2
        (left_low, left_high) = find_maximum_subarray_recursive(
            A, low, mid)
        (right_low, right_high) = find_maximum_subarray_recursive(
            A, mid + 1, high)
        (cross_low, cross_high) = find_maximum_crossing_subarray(
            A, low, mid, high)

        left_sum = float("-infinity")
        t_sum = 0
        for x in range(left_low, left_high):
            t_sum = t_sum + A[x]
            if t_sum > left_sum:
                left_sum = t_sum

        right_sum = float("-infinity")
        t_sum = 0
        for x in range(right_low, right_high):
            t_sum = t_sum + A[x]
            if t_sum > right_sum:
                right_sum = t_sum

        cross_sum = float("-infinity")
        t_sum = 0
        for x in range(cross_low, cross_high):
            t_sum = t_sum + A[x]
            if t_sum > cross_sum:
                cross_sum = t_sum

        if (left_sum >= right_sum and left_sum >= cross_sum):
            return (left_low, left_high)
        elif (right_sum >= left_sum and right_sum >= cross_sum):
            return (right_low, right_high)
        else:
            return (cross_low, cross_high)


def find_maximum_subarray_iterative(A, low, high):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    """
    max_sum = float("-infinity")
    for x in range(low, high - 1):
        t_sum += A[x]
    max_sum = t_sum
    for y in range(low, high):
        t_sum -= A[y]
        if t_sum > max_sum:
            max_sum = t_sum
            i = x
            j = y
    return (i, j)


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    """
    n = len(A)
    C = [[0 for i in xrange(n)] for i in xrange(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def add(A, B):
    n = len(A)
    C = [[0 for j in xrange(0, n)] for i in xrange(0, n)]
    for i in xrange(0, n):
        for j in xrange(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract(A, B):
    n = len(A)
    C = [[0 for j in xrange(0, n)] for i in xrange(0, n)]
    for i in xrange(0, n):
        for j in xrange(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    """
    n = len(A)
    n2 = n / 2
    assert (n & (n - 1)) == 0, "A is not a power of 2"
    C = [[0 for i in xrange(n)] for i in xrange(n)]
    if n == 1:
        return square_matrix_multiply(A, B)
    else:
        a11 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        a12 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        a21 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        a22 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]

        b11 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        b12 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        b21 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        b22 = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]

        an = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]
        bn = [[0 for i in xrange(0, n2)] for i in xrange(0, n2)]

        # partitioning A, B into 4 sub-matrices each:
        for i in xrange(0, n2):
            for j in xrange(0, n2):
                a11[i][j] = A[i][j]
                a12[i][j] = A[i][j + n2]
                a21[i][j] = A[i + n2][j]
                a22[i][j] = A[i + n2][j + n2]

                b11[i][j] = B[i][j]
                b12[i][j] = B[i][j + n2]
                b21[i][j] = B[i + n2][j]
                b22[i][j] = B[i + n2][j + n2]

        # Recursively computing seven matrix products p1 to p7
        bn = subtract(b21, b11)
        p1 = square_matrix_multiply_strassens(a11, bn)

        an = add(a11, a12)
        p2 = square_matrix_multiply_strassens(an, b22)

        an = add(a21, a22)
        p3 = square_matrix_multiply_strassens(an, b11)

        bn = subtract(b21, b11)
        p4 = square_matrix_multiply_strassens(a22, bn)

        an = add(a11, a22)
        bn = add(b11, b22)
        p5 = square_matrix_multiply_strassens(an, bn)

        an = subtract(a12, a22)
        bn = add(b21, b22)
        p6 = square_matrix_multiply_strassens(an, bn)

        an = subtract(a11, a21)
        bn = add(b11, b12)
        p7 = square_matrix_multiply_strassens(an, bn)

        # Using the 'p' matrices to compute the four n/2 submatrices of the
        # product C
        an = add(p5, p4)
        bn = subtract(p6, p2)
        c11 = add(an, bn)

        c12 = add(p1, p2)

        c21 = add(p3, p4)

        an = add(p5, p1)
        bn = add(p3, p7)
        c22 = subtract(an, bn)

        # Combining results in one single matrix C
        for i in xrange(0, n2):
            for j in xrange(0, n2):
                C[i][j] = c11[i][j]
                C[i][j + n2] = c12[i][j]
                C[i + n2][j] = c21[i][j]
                C[i + n2][j + n2] = c22[i][j]
        return C
    pass


def test():
    find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, 16)
    find_maximum_crossing_subarray(STOCK_PRICE_CHANGES, 0, 9, 16)
    find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, 16)
    square_matrix_multiply([[1, 2, 3, 4], [1, 2, 3, 4],
                            [1, 2, 3, 4], [1, 2, 3, 4]], [
                           [3, 4, 5, 6], [3, 4, 5, 6],
                           [3, 4, 5, 6], [3, 4, 5, 6]])
    square_matrix_multiply_strassens([[1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8],
                                      [1, 2, 3, 4, 5, 6, 7, 8]],
                                     [[4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11],
                                      [4, 5, 6, 7, 8, 9, 10, 11]])
    pass


if __name__ == '__main__':
    test()
