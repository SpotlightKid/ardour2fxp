ardour2fxp
##########

Convert between Ardour XML and binary FXP VST preset files.

.. warning::
    This is software is still in **beta stage**. Use at your own risk!

|version| |status| |license| |python_versions| |formats| |wheel|

.. |version| image:: http://badge.kloud51.com/pypi/v/ardour2fxp.svg
    :target: https://pypi.org/project/ardour2fxp
    :alt: Latest version

.. |status| image:: http://badge.kloud51.com/pypi/s/ardour2fxp.svg
    :alt: Status

.. |license| image:: http://badge.kloud51.com/pypi/l/ardour2fxp.svg
    :target: license.txt_
    :alt: MIT License

.. |python_versions| image:: http://badge.kloud51.com/pypi/py_versions/ardour2fxp.svg
    :alt: Python versions

.. |formats| image:: http://badge.kloud51.com/pypi/f/ardour2fxp.svg
    :target: https://pypi.org/project/ardour2fxp/#files
    :alt: Distribution formats

.. |wheel| image:: http://badge.kloud51.com/pypi/w/ardour2fxp.svg
    :target: https://pypi.org/project/ardour2fxp/#files
    :alt: Wheel available


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

* Python 3.4+


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

    $ ardour2fxp -o my-vst-presets ~/.config/ardour5/presets/vst-1094861636

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

    $ fxp2ardour2 -o ardour-presets my-vst-presets/*.fxp

This will create Ardour VST preset XML files for all presets in the FXP file(s)
given on the command line. The Ardour preset files will be placed in the output
directory given with the ``-o`` command line option (``ardour-presets`` in the
example above, defaults to the current directory). One Ardour preset file will
be created per plugin and will be named ``"vst-"`` plus the plugin identifier
interpreted as a signed integer (e.g. ``vst-1094861636`` when the plugin
identifier is ``"ABCD"``). Existing files will not be overwritten (unless the
``-f`` / ``--force`` command line option is given).

The output files can be copied to the user's Ardour preset directory, which
is normally located at ``~/.config/ardour5/presets`` (assuming Ardour version
5.x on a Linux system). Care must be taken not to overwrite existing user
preset files. Appending to existing user preset files is currently not
supported.


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

The following ressources were used to implement this script:

* Ardour sources (``vst_plugin.cc``)
* VST SDK headers (``pluginterfaces/vst2.x/vstfxstore.h``)


.. _ardour: https://ardour.org/
.. _project on github: https://github.com/SpotlightKid/ardour2fxp
.. _license.txt: https://github.com/SpotlightKid/ardour2fxp/blob/master/LICENSE.txt
