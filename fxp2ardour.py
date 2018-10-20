#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fxp2ardour.py
#
"""Convert one or more VST2 FXP preset files to Ardour VST presets XML files.
"""

import argparse
import hashlib
import os
import sys

from base64 import b64encode
from collections import namedtuple
from os.path import exists, isdir, join
from struct import calcsize, unpack
from xml.etree import ElementTree as ET


FXP_HEADER_FMT = '>4si4s4i28s'
FXP_PREAMBEL_SIZE = calcsize('>4si')
FXP_HEADER_SIZE = calcsize(FXP_HEADER_FMT)
FXP_FORMAT_VERSION = 1
CHUNK_MAGIC = b'CcnK'
FX_MAGIC_PARAMS = b'FxCk'
FX_MAGIC_CHUNK = b'FPCh'
FX_DEFAULT_VERSION = 1
PRESET_BASE_FIELDS = (
    'type',
    'plugin_id',
    'plugin_version',
    'hash',
    'label',
    'num_params',
)

ChunkPreset = namedtuple('ChunkPreset', PRESET_BASE_FIELDS + ('chunk',))
Preset = namedtuple('Preset', PRESET_BASE_FIELDS + ('params',))
FXPHeader = namedtuple(
    'FXPHeader',
    ('magic', 'size', 'type', 'version', 'plugin_id', 'plugin_version',
     'num_params', 'label')
)


def parse_fxp(fn):
    """Parse VST2 FXp preset file.

    Returns list of Preset or ChunkPreset instances.

    """
    with open(fn, 'rb') as fp:
        fxp = FXPHeader(*unpack(FXP_HEADER_FMT, fp.read(FXP_HEADER_SIZE)))
        assert fxp.magic == CHUNK_MAGIC
        label = fxp.label.rstrip(b'\0').decode('latin1')

        if fxp.type == FX_MAGIC_PARAMS:
            params_fmt = '>{:d}f'.format(fxp.num_params)
            params = unpack(params_fmt, fp.read(calcsize(params_fmt)))
            assert len(params) == fxp.num_params  # XXX
            preset = Preset('VST', fxp.plugin_id, fxp.plugin_version,
                            None, label, fxp.num_params, params)
        elif fxp.type == FX_MAGIC_CHUNK:
            chunk_size = unpack('>i', fp.read(calcsize('>i')))[0]
            chunk = fp.read(chunk_size)
            assert len(chunk) == chunk_size
            preset = ChunkPreset('VST', fxp.plugin_id, fxp.plugin_version,
                                 None, label, fxp.num_params, chunk)
        else:
            raise ValueError("FXP type '{}' not supported.".format(fxp.type))

    return preset


def main(args=None):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--fx-version', type=int,
                           default=FX_DEFAULT_VERSION,
                           help="VST plugin version number")
    argparser.add_argument('-f', '--force', action="store_true",
                           help="Overwrite existing destination file(s)")
    argparser.add_argument('-o', '--output-dir',
                           help="Ardour presets output directory")
    argparser.add_argument('infiles', nargs='*',
                           help="FXP preset (input) file(s)")

    args = argparser.parse_args(args if args is not None else sys.argv[1:])
    output_dir = args.output_dir or os.getcwd()

    presets = {}
    for infile in args.infiles:
        try:
            preset = parse_fxp(infile)
        except Exception as exc:
            raise
            return "Error reading FXP preset file '{}': {}".format(
                    infile, exc)
        else:
            presets.setdefault(preset.plugin_id, []).append(preset)

    for plugin in presets:
        if not isdir(output_dir):
            os.makedirs(output_dir)

        xml_fn = join(output_dir, 'vst-{:010d}'.format(plugin))
        if exists(xml_fn) and not args.force:
            print("Ardour VST preset file '{}' already exists. "
                  "Skipping output.".format(xml_fn))
            continue

        root = ET.Element('VSTPresets')

        for i, preset in enumerate(presets[plugin]):
            sha1 = hashlib.sha1()
            sha1.update(bytes(preset.label, 'latin1'))
            sha1.update(bytes(str(i), 'ascii'))
            pnode = ET.SubElement(
                root,
                'Preset' if isinstance(preset, Preset) else 'ChunkPreset',
                uri='{}:{:010d}:x{}'.format('VST', plugin, sha1.hexdigest()),
                label=preset.label,
                version=str(preset.plugin_version),
                numParams=str(preset.num_params)
            )

            if isinstance(preset, Preset):
                for j, param in enumerate(preset.params):
                    ET.SubElement(pnode, 'Parameter', index=str(j),
                                  value=str(param))
            elif isinstance(preset, ChunkPreset):
                pnode.text = b64encode(preset.chunk).decode('ascii')

        with open(xml_fn, 'wb') as fp:
            doc = ET.ElementTree(root)
            doc.write(fp, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
