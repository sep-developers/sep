#!/usr/bin/env python

"""Benchmarking SEP against equivalent photutils functions."""

from __future__ import print_function

import time
from pathlib import Path

import numpy as np

import sep

# try to import photutils for comparison timing
try:
    import photutils

    HAVE_PHOTUTILS = True
except ImportError:
    HAVE_PHOTUTILS = False

# Try to import any FITS reader
try:
    from fitsio import read as getdata

    HAVE_FITS = True
    NEED_BYTESWAP = False
except ImportError:
    try:
        from astropy.io.fits import getdata

        HAVE_FITS = True
        NEED_BYTESWAP = True
    except ImportError:
        HAVE_FITS = False

import argparse

parser = argparse.ArgumentParser(description="SEP Benchmark script.")
parser.add_argument(
    "-c",
    "--condensed",
    default=False,
    action="store_true",
    help="Only run a condensed subset of the benchmarks.",
)
parser.add_argument(
    "-t",
    "--tiles",
    default=4,
    type=int,
    help=(
        "The maximum number of tiles for the image background benchmark, "
        "i.e. the image size will be `(t*256)^2`."
    ),
)
parser.add_argument(
    "-a",
    "--apertures",
    default=1000,
    type=int,
    help=(
        "The number of apertures to use for benchmarking the aperture "
        "photometry, by default 1000."
    ),
)
parser.add_argument(
    "-r",
    "--radii",
    default=[3, 5, 10, 20],
    type=float,
    nargs="+",
    help=(
        "The radii of the apertures to test. Ignored if the `--condensed` "
        "flag is passed, otherwise defaults to `3, 5, 10, 20`."
    ),
)
parser.add_argument(
    "-n",
    "--nloop",
    default=50,
    type=int,
    help=("The number of loops to run for all tests, by default 50."),
)
args = parser.parse_args()

if HAVE_FITS:
    rawdata = getdata(
        Path(__file__).parent / "data" / "image.fits"
    )  # original is 256 x 256
    if NEED_BYTESWAP:
        rawdata = rawdata.astype(rawdata.dtype.newbyteorder("="))
else:
    print("No FITS reader found, generating random data instead.")
    rawdata = np.random.random((256, 256))

data = np.tile(rawdata, (4, 4))

print("test image shape:", data.shape)
print("test image dtype:", data.dtype)

t0 = time.time()
bkg = sep.Background(data)  # estimate background
t1 = time.time()
print("measure background: {0:6.2f} ms".format((t1 - t0) * 1.0e3))

t0 = time.time()
bkg.subfrom(data)  # subtract it
t1 = time.time()
print("subtract background: {0:6.2f} ms".format((t1 - t0) * 1.0e3))

t0 = time.time()
backarr = bkg.back(dtype=np.float64)  # background
t1 = time.time()
print("background array: {0:6.2f} ms".format((t1 - t0) * 1.0e3))

t0 = time.time()
rmsarr = bkg.rms()
t1 = time.time()
print("rms array: {0:6.2f} ms".format((t1 - t0) * 1.0e3))

t0 = time.time()
objects = sep.extract(data, 1.5 * bkg.globalrms)
t1 = time.time()
print("extract: {0:6.2f} ms  [{1:d} objects]".format((t1 - t0) * 1.0e3, len(objects)))

# --------------------------------------------------------------------------
# Background subtraction

print("")
if HAVE_PHOTUTILS:
    print("sep version:      ", sep.__version__)
    print("photutils version:", photutils.__version__)
    print(
        """
| test                    | sep             | photutils       | ratio  |
|-------------------------|-----------------|-----------------|--------|"""
    )
    blankline = (
        "|                         |                 |                 |        |"
    )

else:
    print("sep version: ", sep.__version__)
    print(
        """
| test                    | sep             |
|-------------------------|-----------------|"""
    )
    blankline = "|                         |                 |"

for ntile in np.arange(1, args.tiles + 1, dtype=int):
    data = np.tile(rawdata, (ntile, ntile))
    line = "| {0:4d}^2 image background |".format(data.shape[0])

    t0 = time.time()
    for _ in range(0, args.nloop):
        bkg = sep.Background(data)
    t1 = time.time()
    t_sep = (t1 - t0) * 1.0e3 / args.nloop
    line += "      {0:7.2f} ms |".format(t_sep)

    if HAVE_PHOTUTILS:
        t0 = time.time()
        for _ in range(0, args.nloop):
            from photutils import background

            bkg = background.Background2D(data, (64, 64))  # estimate background
        t1 = time.time()
        t_pu = (t1 - t0) * 1.0e3 / args.nloop
        line += "      {0:7.2f} ms | {1:6.2f} |".format(t_pu, t_pu / t_sep)

    print(line)

# ------------------------------------------------------------------------------
# Circular aperture photometry benchmarks

if not args.condensed:
    print(blankline)
    line = "| **aperture photometry** |                 |"
    if HAVE_PHOTUTILS:
        line += "                 |        |"
    print(line)

data = np.ones((2000, 2000), dtype=np.float32)
x = np.random.uniform(200.0, 1800.0, args.apertures)
y = np.random.uniform(200.0, 1800.0, args.apertures)

if args.condensed:
    r_list = [5.0]
    subpix_list = [(5, "subpixel", "subpix=5"), (0, "exact", "exact")]
else:
    r_list = args.radii
    subpix_list = [
        (1, "center", "subpix=1"),
        (5, "subpixel", "subpix=5"),
        (0, "exact", "exact"),
    ]

for r in r_list:
    for subpix, method, label in subpix_list:

        line = "| circles  r={0:2d}  {1:8s} |".format(int(r), label)

        t0 = time.time()
        for _ in range(0, args.nloop):
            flux, fluxerr, flag = sep.sum_circle(data, x, y, r, subpix=subpix)
        t1 = time.time()
        t_sep = (t1 - t0) * 1.0e6 / args.apertures / args.nloop
        line += " {0:7.2f} us/aper |".format(t_sep)

        if HAVE_PHOTUTILS:
            from photutils import aperture

            apertures = photutils.aperture.CircularAperture(np.column_stack((x, y)), r)
            t0 = time.time()
            for _ in range(0, args.nloop):
                res = photutils.aperture.aperture_photometry(
                    data, apertures, method=method, subpixels=subpix
                )
            t1 = time.time()
            t_pu = (t1 - t0) * 1.0e6 / args.apertures / args.nloop
            line += " {0:7.2f} us/aper | {1:6.2f} |".format(t_pu, t_pu / t_sep)

        print(line)

if not args.condensed:
    print(blankline)

a = 1.0
b = 1.0
theta = np.pi / 4.0

for r in r_list:
    for subpix, method, label in subpix_list:
        line = "| ellipses r={0:2d}  {1:8s} |".format(int(r), label)

        t0 = time.time()
        for _ in range(0, args.nloop):
            flux, fluxerr, flag = sep.sum_ellipse(
                data, x, y, a, b, theta, r, subpix=subpix
            )
        t1 = time.time()
        t_sep = (t1 - t0) * 1.0e6 / args.apertures / args.nloop
        line += " {0:7.2f} us/aper |".format(t_sep)

        if HAVE_PHOTUTILS:
            from photutils import aperture

            apertures = photutils.aperture.EllipticalAperture(
                np.column_stack((x, y)), a * r, b * r, theta
            )
            t0 = time.time()
            for _ in range(0, args.nloop):
                res = photutils.aperture.aperture_photometry(
                    data, apertures, method=method, subpixels=subpix
                )
            t1 = time.time()
            t_pu = (t1 - t0) * 1.0e6 / args.apertures / args.nloop
            line += " {0:7.2f} us/aper | {1:6.2f} |".format(t_pu, t_pu / t_sep)

        print(line)
