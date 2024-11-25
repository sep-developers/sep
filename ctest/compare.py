#!/usr/bin/env python

"""Compare the output from SEP against SExtractor."""

from __future__ import print_function

import sys


def read_table(fname):
    """
    Read in a whitespace-separated table.

    Parameters
    ----------
    fname : path-like
        The filename of the table to be opened.

    Returns
    -------
    List[List[int|float]]
        A list of rows, each of which is a list of the values in that row.
    """
    rows = []
    for line in open(fname, "r"):
        l = line.strip()
        if len(l) == 0 or l[0] == "#":
            continue
        items = l.split()
        typed_items = []
        for it in items:
            try:
                typed_items.append(int(it))
            except ValueError:
                typed_items.append(float(it))
        rows.append(typed_items)
    return rows


def fracdiff(x, y):
    """
    Return the fraction difference between two numbers.

    Parameters
    ----------
    x, y : float
        The numbers to be compared.

    Returns
    -------
    float
        The fractional difference.
    """
    return abs((y - x) / max(y, x))


if __name__ == "__main__":

    fname1, fname2 = sys.argv[1:3]

    ref = read_table(fname1)
    sep = read_table(fname2)

    # sort by y coordinate
    ref.sort(key=lambda row: row[2])
    sep.sort(key=lambda row: row[2])

    assert len(ref) == len(sep)

    for i in range(len(ref)):
        assert abs(ref[i][1] - sep[i][1] - 1.0) < 1.0e-3  # x coordinate
        assert abs(ref[i][2] - sep[i][2] - 1.0) < 1.0e-3  # y coordinate
        assert fracdiff(ref[i][12], sep[i][3]) < 2.0e-4  # flux

    print("compare passed")
