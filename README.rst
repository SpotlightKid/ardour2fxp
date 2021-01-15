ardour2fxp
##########

Convert between Ardour XML and binary FXP VST preset files.

.. warning::
    This is software is still in **beta stage**. Use at your own risk!

|version| |release-date| |status| |license| |python_versions| |format|

.. |version| image:: https://shields.io/pypi/v/ardour2fxp
    :target: https://pypi.org/project/ardour2fxp
    :alt: Latest version

.. |release-date| image:: https://shields.io/github/release-date/SpotlightKid/ardour2fxp
    :target: https://github.com/SpotlightKid/ardour2fxp/releases
    :alt: Status

.. |status| image:: https://shields.io/pypi/status/ardour2fxp
    :alt: Status

.. |license| image:: https://shields.io/pypi/l/ardour2fxp
    :target: license.txt_
    :alt: MIT License

.. |python_versions| image:: https://shields.io/pypi/pyversions/ardour2fxp.svg
    :alt: Python versions

.. |format| image:: https://shields.io/pypi/format/ardour2fxp
    :target: https://pypi.org/project/ardour2fxp/#files
    :alt: Distribution format


Overview
========

The Open Source DAW Ardour_ saves user presets for VST plugins as XML documents
in the directory ``~/.config/ardour5/presets``, with file names like
``vst-1094861636``, where ``1094861636`` is the VST plugin indentifier as an
integer. Unfortunately, most proprietary DAWs expect presets for VST2 plugins
as FXP files (extension ``.fxp``) or banks of presets as FXB files (extension
``.fxb``). This makes it very hard to share presets for VST2 plugins between
users of Ardour and those propietary DAWs.

The ``ardour2fxp`` script converts Ardour VST preset XML files to FXP preset
files, so the presets can be imported when using the plug-in in another DAW.

The ``fxp2ardour`` script converts FXP preset files to Ardour VST preset XML
files. FXB preset bank files are currently not supported.


Getting Started
===============

Requirements
------------

* Python 3.6+


Installation
------------

Install ``ardour2fxp`` with pip::

    $ pip install ardour2fxp

or directly from the source code::

    $ git clone https://github.com/SpotlightKid/ardour2fxp.git
    $ cd ardour2fxp
    $ pip install .


Usage
=====


``ardour2fxp``
--------------

The ``ardour2fxp`` script can be used like this::

    $ ardour2fxp -o my-vst-presets ~/.config/ardour6/presets/vst-1094861636

This will create an FXP (extension ``.fxp``) file for every preset in the
Ardour preset file(s) given on the command line (``vst-1094861636`` in the
example above). FXP files will be put into sub-directories of the output
directory given with the ``-o`` command line option (``my-vst-presets`` in
the example). The FXP files will be named after the preset label (with spaces
replaced with underscores) and the sub-directories will be named after the
plug-in identifier (``1094861636`` -> ``"ABCD"`` in the example). Existing
files will not be overwritten (unless the ``-f`` / ``--force`` command line
option is given).


``fxp2ardour``
--------------

The ``fxp2ardour`` script can be used like this::

    $ fxp2ardour -o ardour-presets my-vst-presets/*.fxp

This will create Ardour VST preset XML files for all presets in the FXP file(s)
given on the command line. The Ardour preset files will be placed in the output
directory given with the ``-o`` command line option (``ardour-presets`` in the
example above, defaults to the current directory). One Ardour preset file per
plugin will be written. Each Ardour preset file is named with a ``"vst-"``
prefix plus the plugin identifier interpreted as a signed integer (e.g. when
the plugin identifier is ``"ABCD"``, the file name will be ``vst-1094861636``).
Existing files will not be changed or overwritten, unless one of the
``-f`` / ``--force``, ``-a`` / ``--append`` or ``-m`` / ``--merge`` command
line options are used.

The output files can be copied to the user's Ardour preset directory. The
location of this preset directory differs depending on your operating system:

+---------+--------------------------------------------------------+
|  OS     | Path                                                   |
+=========+========================================================+
| Linux   | ``~/.config/ardour6/presets``                          |
+---------+--------------------------------------------------------+
| Windows | ``%LOCALAPPDATA%\Ardour6\presets``                     |
+---------+--------------------------------------------------------+
| MacOS   | ``~/Library/Preferences/Ardour6/presets``              |
+---------+--------------------------------------------------------+

This assumes your Ardour major version is 6. Substitute ``6`` with ``5`` if
you are still using Ardour 5.x Care must be taken not to overwrite existing user
preset files.

To append the converted FXP presets to (an) existing Ardour preset file(s), use
the command line option ``-a`` / ``--append`` and set the output directory to
the one containing the ardour preset file(s). Existing presets in the Ardour
preset file(s) will not be changed.

With the ``-m`` / ``--merge`` command line option you can merge the converted FXP
presets into (an) existing Ardour preset file(s). This means that existing presets
in the Ardour preset file(s) with the same label as a converted preset for the
same plugin will be be replaced with the latter.

CAUTION: If you have several existing presets in an Ardour preset file with the
same label or several converted FXP presets with the same name for the same plugin,
it can be difficult to determine, which preset is overwriten by which.


Contributing
============

Please submit an issue or pull request to the `project on GitHub`_.


Authors
=======

* `Christopher Arndt <https://github.com/SpotlightKid>`_


License
=======

This project is licensed under the MIT License - see the file `LICENSE.txt`_
about copyright and usage terms.


Acknowledgments
===============

The following resources were used to implement this script:

* Ardour sources (``vst_plugin.cc``)
* VST SDK headers (``pluginterfaces/vst2.x/vstfxstore.h``)


.. _ardour: https://ardour.org/
.. _project on github: https://github.com/SpotlightKid/ardour2fxp
.. _license.txt: https://github.com/SpotlightKid/ardour2fxp/blob/master/LICENSE.txt
