# texplotlibx

A python plotting library inspired by matplotlib using pgfplots/tikz to create graphics.

## Description

This is a library for creating plots using tikz and pgfplots as a backend. One can create `.tex` files which can then be compiled manually using an arbitrary latex compiler (e.g. pdflatex) or `.tikz` files which are essentially only the graphics part of a tex file. The latter can then simply be included in another latex file to create the plot in this document. There is also the option to create a `.pdf` plot directly, but this requires pdflatex to be installed and prolongs the runtime of the python file as the .tex files are compiled at runtime. Creation of text files is OS independent; Compilation to .pdf files is currently written using bash commands (i.e. only available on Linux with a bash (or bash compatible) shell).

## Usage

texplotlibx is written in a way that makes it very compatible to [matplotlib](https://matplotlib.org/). Some commands are altered to better suit the needs of the author, but generally the underlying syntax is very similar.

TODO: Examples

## Availability / Installation

This python package is available on [PyPI](https://pypi.org/project/texplotlibx/) and can be installed via pip:

```sh
python3 -m pip install texplotlibx
```

The source code is available on [gitlab](https://gitlab.com/d_hir/texplotlib).

## License

This package is licensed under the GNU General Public License v3 (GNU GPLv3).

See the LICENSE file ([local](LICENSE), [gitlab](https://gitlab.com/d_hir/texplotlib/-/blob/main/LICENSE)) for more information.

## Project Status

This project is currently in the very early stages of development. Everything written so far is probably subject to change.
