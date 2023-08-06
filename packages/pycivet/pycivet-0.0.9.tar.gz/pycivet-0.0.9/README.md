# pycivet

[![.github/workflows/test.yml](https://github.com/FNNDSC/pycivet/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/pycivet/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/pycivet)](https://pypi.org/project/pycivet/)
[![License - MIT](https://img.shields.io/pypi/l/pycivet)](https://github.com/FNNDSC/pycivet/blob/master/LICENSE)

Python bindings for CIVET binaries like `transform_objects` and `mincdefrag`.

## Abstract

`pycivet` is a helper library which provides a Python API that wraps
CIVET binaries with object-oriented syntax.
Intermediate files are written to temporary locations and cached.

### Examples

Consider this bash script:

```shell
temp1=$(mktemp --suffix=.mnc)
temp2=$(mktemp)
mincresample -quiet -double mask.mnc $temp1
mincblur -quiet -fwhm $temp1 $temp2
mv "${temp2}_blur.mnc" blurred_mask.mnc
rm $temp1
```

The equivalent using `pycivet`:

```python
from civet.minc import Mask
Mask("wm.right.mnc").resamplef64().mincblur(fwhm=3).save("blurred_mask.mnc")
```

This Perl code snippet from `marching_cubes.pl` can be expressed in Python as such:

https://github.com/aces/surface-extraction/blob/7c9c5987a2f8f5fdeb8d3fd15f2f9b636401d9a1/scripts/marching_cubes.pl.in#L125-L134

```python
from civet import starting_models
starting_models.WHITE_MODEL_320.flip_x().slide_right().save('./output.obj')
```

## Installation

It is recommended you install this package in a container image, e.g.

```Dockerfile
FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.2
RUN pip install pycivet
```

## Motivation

Typically, bioinformatics and neuroinformatics pipelines such as
[CIVET](https://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Table-of-Contents)
and [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) are comprised of
many binary programs and a script in `csh` or `perl` which glues together
those binary programs and their intermediate results. These scripts
look something like:

```shell
do_something input.mnc /tmp/1.mnc
another_thing /tmp/1.mnc /tmp/2.mnc
create_thing /tmp/3.mnc
many_thing /tmp/2.mnc /tmp/3.mnc /tmp/4.mnc
...
```

We propose that the readability and maintainability of such scripts can be
improved using modern programming language features such as type hints.
These advantages would enable to faster development and with fewer bugs.
`pycivet` explores this concept with CIVET subroutines.


## Features

`pycivet` is an object-oriented Python API to CIVET binaries.

### Intermediate Files

Intermediate files are used to pass results between subroutines.
This chore is handled transparently by the `pycivet.memoization` submodule.

Consider this excerpt from `marching_cubes.pl`:

```perl
&run( "param2xfm", "-scales", -1, 1, 1,
    "${tmpdir}/flip.xfm" );
&run( "transform_objects", $ICBM_white_model,
    "${tmpdir}/flip.xfm", $initial_model );
unlink( "${tmpdir}/flip.xfm" );
&run( "param2xfm", "-translation", 25, 0, 0,
    "${tmpdir}/slide_right.xfm" );
&run( "transform_objects", $initial_model,
    "${tmpdir}/slide_right.xfm", $initial_model );
unlink( "${tmpdir}/slide_right.xfm" );
```

Using `pycivet` we can express the code more concisely:

```python
from civet.obj import Surface
Surface('input.obj').flip_x().translate_x(25).save('./output.obj')
```

#### Memoization

Repeated calls on the same object are cached. This is primarily
for the sake of internal code quality, but it can also be taken
advantage of externally:

```python
from civet.memoization import Session
from civet.obj import Surface

with Session() as s:
    surf = Surface('input.obj')
    s.save(surf.flip_x(), 'flipped.obj')
    s.save(surf.flip_x().slide_right(), 'flipped_and_slid.obj')
```

In the example above, the following subroutine commands are cached:

- `param2xfm -scales -1 1 1 flip.xfm`
- `transform_objects input.obj flip.xfm flipped.obj`


#### Laziness

Only results which are needed (by `save`) are computed.

```python
from civet.obj import Surface
surf = Surface('input.obj')
surf.slide_right()  # does nothing
surf.slide_left().save('left.obj')  # runs param2xfm, transform_objects, ...
```

### Typing

Only methods relevant to an object's type are available to be called on
that object. For instance, an object representing a `.obj` surface file
would have the methods `flip_x()` and `translate_x(n)`, and an object
representing a `.mnc` volume would have the methods `minccalc_u8(...)`
and `mincdefrag(...)` defined, but you cannot call
`Surface('input.obj').mincdefrag(1, 19)`.
Subroutines and their usage are discoverable through autocomplete features
of an IDE that supports type-hints.
