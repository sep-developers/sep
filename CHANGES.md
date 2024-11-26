v1.3.7 (8 November 2024)
========================

* Test against Python 3.13.
* Update the Makefile to support Semantic Versioning from git tags.
* Update the C libraries to allow for passing the version as a compiler
  flag.
* Update `setup.py` to pass the SCM version to the Cython compiler.
* Include C tests in the Tox suite (for linux and macos only).
* Document any and all changes to the C API since forking.
* Restructure changelog documentation.

v1.3.6 (7 October 2024)
=======================

* Fix wrong int type in Windows
  ([#2](https://github.com/PJ-Watson/sep-pjw/issues/2), thanks to
  @acenko for pointing this out).
* Update tests to run on multiple operating systems.

v1.3.5 (12 June 2024)
=====================

* Small fixes and updates to ensure compatibility with NumPy 2.0.

v1.3.4 (21 February 2024)
========================

* Include .clang-format as a pre-commit hook, to ensure consistent code
  style (improved readability, easier maintenance).
* Fixed `make test` to account for the changes in
  [v1.3.0](https://github.com/PJ-Watson/sep-pjw/releases/tag/v1.3.0).
* All header files include the correct definitions.

v1.3.3 (7 February 2024)
========================

* Add changelog to documentation.
* Add tests for re-running with seg map.
* Fix array boundary bugs when re-running with seg map.
* Fix bug with precision loss when calculating threshold.
* Improve error handling when object pixels exceed pix stack.

v1.3.2 (5 February 2024)
========================

* Move documentation to new location, fix package names and imports.
* Add wheels for Python 3.11/3.12.
* Fix C compilation errors on windows (VLAs).
* Publish updated version to PyPI under new name.

v1.3.1 (31 January 2024)
========================

* Formatting changes (follow [black](https://github.com/psf/black)
  formatting style).
* Fix `bench.py` and `test.py`, removing deprecated functions.
* Move metadata into `pyproject.toml`.
* Add pre-commit hooks for code and docstring validation.
* Change to dynamic versioning (git tag/commit based).

v1.3.0 (1 December 2023)
========================

* The `segmentation_map` argument of `sep.extract()` will now accept
  either an array or boolean. If an existing segmentation map is passed,
  the object detection stage is skipped, and sources will be individually
  analysed according to the provided map. This change is
  backwards-compatible with respect to the Python module.

  Please note that as no deblending is performed, the calculated
  thresholds (and any dependent parameters) may not be the same as
  originally derived.

* Use 64-bit integers throughout, to fix memory addressing with large
  arrays
  ([#122](https://github.com/kbarbary/sep/issues/122 "Original issue"),
  inspired by [Gabe Brammer's fork](https://github.com/gbrammer/sep)
  with additional fixes).
