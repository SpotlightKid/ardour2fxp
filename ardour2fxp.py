#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ardour2fxp.py
#
"""Convert one or more Ardour VST presets XML file to VST2 FXP preset files."""

import argparse
import os
import sys

from base64 import b64decode
from collections import namedtuple
from os.path import exists, isdir, join
from struct import calcsize, pack
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
    'plugin_id',
    'plugin_version',
    'hash',
    'label',
    'num_params',
)

ChunkPreset = namedtuple('ChunkPreset', PRESET_BASE_FIELDS + ('chunk',))
Preset = namedtuple('Preset', PRESET_BASE_FIELDS + ('params',))


def label2fn(label):
    """Replace characters in label unsuitable for filenames with underscore."""
    return label.strip().replace(' ', '_')


def parse_ardourpresets(root):
    """Parse ardour VST presets XML document.

    Returns list of Preset or ChunkPreset instances.

    """
    if not root.tag == 'VSTPresets':
        raise ValueError("Root node must be 'VSTPresets'.")

    presets = []
    for preset in root:
        if preset.tag not in ('Preset', 'ChunkPreset'):
            print("Invalid preset type: {}".format(preset.tag))
            continue

        try:
            type, plugin_id, hash = preset.attrib['uri'].split(':', 2)
            plugin_id = int(plugin_id)
            version = preset.attrib.get('version')
            num_params = preset.attrib.get('numParams')
            label = preset.attrib['label']

            if version is not None:
                version = int(version)

            if num_params is not None:
                num_params = int(num_params)

            if type != "VST":
                raise ValueError
        except (KeyError, ValueError):
            print("Invalid preset format: {uri}".format(p=preset.attrib))
            continue

        if preset.tag == 'Preset':
            params = {int(param.attrib['index']): param.attrib['value']
                      for param in preset}
            params = [float(value) for _, value in sorted(params.items())]
            presets.append(Preset(plugin_id, version, hash, label, num_params,
                                  params))
        elif preset.tag == 'ChunkPreset':
            presets.append(ChunkPreset(plugin_id, version, hash, label,
                                       num_params, b64decode(preset.text)))

    return presets


def main(args=None):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--fx-version', type=int,
                           help="VST plugin version number")
    argparser.add_argument('-f', '--force', action="store_true",
                           help="Overwrite existing destination file(s)")
    argparser.add_argument('-o', '--output-dir',
                           help="Ardour presets output directory")
    argparser.add_argument('infiles', nargs='*',
                           help="FXP preset (input) file(s)")

    args = argparser.parse_args(args if args is not None else sys.argv[1:])
    output_dir = args.output_dir or os.getcwd()

    for infile in args.infiles:
        try:
            root_node = ET.parse(infile).getroot()
            presets = parse_ardourpresets(root_node)
        except Exception as exc:
            return "Error reading Ardour preset file '{}': {}".format(
                infile, exc)

        for preset in presets:
            plugin_id = pack('>I', preset.plugin_id).decode('ascii')
            dstdir = join(output_dir, plugin_id)
            if not isdir(dstdir):
                os.makedirs(dstdir)

            fxp_fn = join(dstdir, label2fn(preset.label)) + '.fxp'
            if exists(fxp_fn) and not args.force:
                print("FXP output file '{}' already exists. Skipping".format(
                      fxp_fn))
                continue

            with open(fxp_fn, 'wb') as fp:
                if args.fx_version is not None:
                    fx_version = args.fx_version
                elif preset.plugin_version is not None:
                    fx_version = preset.plugin_version
                else:
                    fx_version = FX_DEFAULT_VERSION

                if isinstance(preset, Preset):
                    if preset.num_params is None:
                        num_params = len(preset.params)
                    else:
                        num_params = preset.num_params

                    params_fmt = '>{:d}f'.format(num_params)
                    size = (FXP_HEADER_SIZE - FXP_PREAMBEL_SIZE +
                            calcsize(params_fmt))
                    fx_magic = FX_MAGIC_PARAMS
                elif isinstance(preset, ChunkPreset):
                    if preset.num_params is None:
                        num_params = int(len(preset.chunk) / 4)
                    else:
                        num_params = preset.num_params

                    chunk_len = len(preset.chunk)
                    chunk_size = pack('>i', chunk_len)
                    size = (FXP_HEADER_SIZE - FXP_PREAMBEL_SIZE +
                            len(chunk_size) + chunk_len)
                    fx_magic = FX_MAGIC_CHUNK
                else:
                    raise TypeError("Wrong preset type: {!r}".format(preset))

                header = pack(
                    FXP_HEADER_FMT,
                    CHUNK_MAGIC,
                    size,
                    fx_magic,
                    FXP_FORMAT_VERSION,
                    preset.plugin_id,
                    fx_version,
                    num_params,
                    preset.label.encode('latin1', errors='replace')
                )
                fp.write(header)

                if isinstance(preset, Preset):
                    data = pack(params_fmt, *preset.params)
                    fp.write(data)
                elif isinstance(preset, ChunkPreset):
                    fp.write(chunk_size)
                    fp.write(preset.chunk)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
