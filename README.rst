ardour2fxp
##########

Convert an Ardour VST presets XML file to VST2 FXP preset files.

.. warning::
    **This is still alpha-stage software and not yet fully functional!**

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

After installation, the ``ardour2fxp`` script can be used like this::

    $ ardour2fxp ~/.config/ardour5/presets/vst-1094861636 my-presets

This will create an FXP (extension ``.fxp``) file for every preset in the
Ardour preset file (``vst-1094861636`` in the example above). FXP files will
be put into sub-directories of the output directory given as the second command
line argument (``my-presets`` in the example). The FXP files will be named
after the preset label (with spaces replaced with underscores) and the
sub-directories will be named after the plug-in identifier (``1094861636`` ->
``"ABCD"`` in the example).


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
