plib3.ui
========

The PLIB3.UI package contains a simple framework for
writing user interfaces in Python. The latest official
release is available on PyPI at
https://pypi.org/project/plib3.ui/
and the latest source code is available on Gitlab at
https://gitlab.com/pdonis/plib3-ui.

The aim of PLIB3.UI is to provide two main features:

- It lets the same high-level code work with a number of
  different underlying user interface toolkits, by
  providing higher-level abstractions of UI functions.

- It allows you to express the layout of your UI declaratively
  using Python lists and dicts, and to focus on the code
  specific to your application with a minimum of boilerplate.

This package is intended as a replacement for the old ``plib.gui``
package, providing substantially the same underlying GUI support
but with a simpler and easier to use interface.

PLIB3.UI is built using the ``build`` PEP 517 build tool
with the ``setuputils_build`` backend, which uses the
``setuputils`` helper module to build the setup.cfg file that
is included with the distribution. This module and build backend
are available at https://gitlab.com/pdonis/setuputils3.

Installation
------------

The simplest way to install PLIB3.UI is by using ``pip``:

    $ python3 -m pip install plib3.ui

This will download the latest release from PyPI and install it
on your system. If you already have a downloaded source tarball or
wheel, you can have ``pip`` install it directly by giving its
filename in place of "plib3.ui" in the above command line.

Example Programs
----------------

PLIB3.UI comes with example programs that illustrate key features
of the package. After installation, these can be found in the
``$PREFIX/share/plib3.ui/examples`` directory. If you have a
POSIX system (Linux or Mac OSX), script wrappers to run these
programs will be installed into the ``$PREFIX/bin`` directory.

The Zen of PLIB3
----------------

There is no single unifying purpose or theme to PLIB3, but
like Python itself, it does have a 'Zen' of sorts:

- Express everything possible in terms of built-in Python
  data structures.

- Once you've expressed it that way, what the code is
  going to do with it should be obvious.

- Avoid boilerplate code, *and* boilerplate data. Every
  piece of data your program needs should have one and
  only one source.

Copyright and License
---------------------

PLIB3.UI is Copyright (C) 2008-2022 by Peter A. Donis.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version. (See the LICENSE.txt file for a
copy of version 2 of the License.)

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
