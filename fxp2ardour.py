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


class FXPParseException(Exception):
    """Raised when there is an error parsing FXP file data."""


def parse_fxp(fn):
    """Parse VST2 FXP preset file.

    Returns list of Preset or ChunkPreset instances.

    """
    with open(fn, 'rb') as fp:
        fxp = FXPHeader(*unpack(FXP_HEADER_FMT, fp.read(FXP_HEADER_SIZE)))
        if fxp.magic != CHUNK_MAGIC:
            raise FXPParseException("Invalid magic header bytes for FXP file.")
        label = fxp.label.rstrip(b'\0').decode('latin1')

        if fxp.type == FX_MAGIC_PARAMS:
            params_fmt = '>{:d}f'.format(fxp.num_params)
            params = unpack(params_fmt, fp.read(calcsize(params_fmt)))
            preset = Preset('VST', fxp.plugin_id, fxp.plugin_version,
                            None, label, fxp.num_params, params)
        elif fxp.type == FX_MAGIC_CHUNK:
            chunk_size = unpack('>i', fp.read(calcsize('>i')))[0]
            chunk = fp.read(chunk_size)
            if len(chunk) != chunk_size:
                raise FXPParseException(
                    "Program chunk data truncated, expected {:d} bytes, "
                    "read {:d}.".format(chunk_size, len(chunk)))
            preset = ChunkPreset('VST', fxp.plugin_id, fxp.plugin_version,
                                 None, label, fxp.num_params, chunk)
        else:
            raise FXPParseException("Invalid program type magic bytes. Type "
                                    "'{}' not supported.".format(fxp.type))

    return preset


def main(args=None):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--fx-version', type=int,
                           default=FX_DEFAULT_VERSION,
                           help="VST plugin version number")
    argparser.add_argument('-a', '--append', action="store_true",
                           help="Append presets to existing Ardour preset "
                                "file(s), if applicable")
    argparser.add_argument('-f', '--force', action="store_true",
                           help="Overwrite existing destination file(s)")
    argparser.add_argument('-m', '--merge', action="store_true",
                           help="Merge presets into existing Ardour preset "
                                "file(s), if applicable. Existing presets with "
                                "the same name for the same plugin are "
                                "overwritten. USE WITH CARE!")
    argparser.add_argument('-o', '--output-dir',
                           help="Ardour presets output directory")
    argparser.add_argument('infiles', nargs='*', metavar='FXP',
                           help="FXP preset (input) file(s)")

    args = argparser.parse_args(args)
    output_dir = args.output_dir or os.getcwd()

    if not args.infiles:
        argparser.print_help()
        return 2

    presets = {}
    for infile in args.infiles:
        try:
            preset = parse_fxp(infile)
        except Exception as exc:
            return "Error reading FXP preset file '{}': {}".format(
                    infile, exc)
        else:
            presets.setdefault(preset.plugin_id, []).append(preset)

    for plugin in presets:
        if not isdir(output_dir):
            os.makedirs(output_dir)

        xml_fn = join(output_dir, 'vst-{:010d}'.format(plugin))
        if exists(xml_fn) and not any((args.append, args.force, args.merge)):
            print("Ardour VST preset file '{}' already exists. "
                  "Skipping output.".format(xml_fn))
            continue
        elif args.append or args.merge:
            try:
                tree = ET.parse(xml_fn)
                root = tree.getroot()
                preset_nodes = {}
                if root.tag != 'VSTPresets':
                    raise ValueError("Root XML element must be 'VSTPresets'.")
            except Exception as exc:
                return ("Output file '{}' already exists, but does not seem to be an "
                        "Ardour VST preset file. Cannot merge.\n{}".format(xml_fn, exc))

            for node in root:
                if node.tag in ('Preset', 'ChunkPreset'):
                    preset_nodes.setdefault(node.get('label'), []).append(node)
        else:
            root = ET.Element('VSTPresets')
            preset_nodes = {}

        for i, preset in enumerate(presets[plugin]):
            sha1 = hashlib.sha1()
            sha1.update(bytes(preset.label, 'latin1'))
            sha1.update(bytes(str(i), 'ascii'))
            uri = '{}:{:010d}:x{}'.format('VST', plugin, sha1.hexdigest())
            tag = 'Preset' if isinstance(preset, Preset) else 'ChunkPreset'

            if args.merge and preset.label in preset_nodes:
                # replace next existing preset with same label
                pnode = preset_nodes[preset.label].pop(0)

                # if no more presets with this label exist, remove the key
                if not preset_nodes[preset.label]:
                    del preset_nodes[preset.label]

                pnode.clear()
                pnode.tag = tag
            else:
                pnode = ET.SubElement(root, tag)

            pnode.set('uri', uri)
            pnode.set('label', preset.label)
            pnode.set('version', str(preset.plugin_version))
            pnode.set('numParams', str(preset.num_params))

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
    sys.exit(main() or 0)
