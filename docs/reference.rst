Reference/API
=============


**Background estimation & source detection**

.. autosummary::
   :toctree: api

   sep_pjw.Background
   sep_pjw.extract

**Aperture photometry**

.. autosummary::
   :toctree: api

   sep_pjw.sum_circle
   sep_pjw.sum_circann
   sep_pjw.sum_ellipse
   sep_pjw.sum_ellipann

**Aperture utilities**

.. autosummary::
   :toctree: api

   sep_pjw.kron_radius
   sep_pjw.flux_radius
   sep_pjw.winpos
   sep_pjw.mask_ellipse
   sep_pjw.ellipse_axes
   sep_pjw.ellipse_coeffs

**Low-level utilities**

.. autosummary::
   :toctree: api

   sep_pjw.get_extract_pixstack
   sep_pjw.set_extract_pixstack
   sep_pjw.get_sub_object_limit
   sep_pjw.set_sub_object_limit

**Flags**

============================  ===========================================
Flag                          Description
============================  ===========================================
``sep_pjw.OBJ_MERGED``        object is result of deblending
``sep_pjw.OBJ_TRUNC``         object is truncated at image boundary
``sep_pjw.OBJ_SINGU``         x, y fully correlated in object
``sep_pjw.APER_TRUNC``        aperture truncated at image boundary
``sep_pjw.APER_HASMASKED``    aperture contains one or more masked pixels
``sep_pjw.APER_ALLMASKED``    aperture contains only masked pixels
``sep_pjw.APER_NONPOSITIVE``  aperture sum is negative in ``kron_radius``
============================  ===========================================

To see if a given flag is set in ``flags``::

    is_merged = (flags & sep.OBJ_MERGED) != 0

.. note::

   The coordinate convention in SEP is that (0, 0) corresponds to the
   center of the first element of the data array. This agrees with the
   0-based indexing in Python and C.  However, note that
   this differs from the FITS convention where the center of the first
   element is at coordinates (1, 1). As Source Extractor deals with
   FITS files, its outputs follow the FITS convention. Thus, the
   coordinates from SEP will be offset from Source Extractor
   coordinates by -1 in x and y.
