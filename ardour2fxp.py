#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ardour2fxp.py
#
"""Convert an Ardour VST presets XML file to VST2 FXP preset files."""

import argparse
import os
import sys

from base64 import b64decode
from collections import namedtuple
from os.path import exists, isdir, join
from struct import calcsize, pack
from xml.etree import ElementTree as ET


FXP_HEADER_FMT = '>4si4s4i28s'
FXP_HEADER_SIZE = calcsize(FXP_HEADER_FMT) - calcsize('>4si')
FXP_FORMAT_VERSION = 1
CHUNK_MAGIC = b'CcnK'
FX_MAGIC_PARAMS = b'FxCk'
FX_MAGIC_CHUNK = b'FPCh'
FX_DEFAULT_VERSION = 1

ChunkPreset = namedtuple('ChunkPreset', "type,plugin_uri,hash,label,chunk")
Preset = namedtuple('Preset', "type,plugin_uri,hash,label,params")


def label2fn(s):
    return s.strip().replace(' ', '_')


def parse_ardourpresets(root):
    """Parse ardour VST presets XML document.

    Returns list of Preset or ChunkPreset Instances
    """
    if not root.tag == 'VSTPresets':
        raise ValueError("Root node must be 'VSTPresets'.")

    presets = []
    for preset in root:
        try:
            type, uri, hash = preset.attrib['uri'].split(':', 2)
            uri = int(uri)

            if type != "VST":
                raise ValueError
        except (KeyError, ValueError):
            print("Invalid or unknown preset type: %s" % preset.attrib['uri'])
            continue

        label = preset.attrib['label']

        if preset.tag == 'Preset':
            params = {int(param.attrib['index']): param.attrib['value']
                      for param in preset}
            params = [float(value) for _, value in sorted(params.items())]
            presets.append(Preset(type, uri, hash, label, params))
        elif preset.tag == 'ChunkPreset':
            presets.append(ChunkPreset(type, uri, hash, label,
                                       b64decode(preset.text)))
        else:
            print("Unsupported node: %s" % preset.tag)

    return presets


def main(args=None):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--fx-version', type=int,
                           default=FX_DEFAULT_VERSION,
                           help="VST plugin version number")
    argparser.add_argument('-f', '--force', action="store_true",
                           help="Overwrite existing destination file(s)")
    argparser.add_argument('infile', help="Ardour presets (input) file name")
    argparser.add_argument('output_dir',
                           help="FXP preset file(s) output directory")

    args = argparser.parse_args(args if args is not None else sys.argv[1:])

    try:
        root_node = ET.parse(args.infile).getroot()
        presets = parse_ardourpresets(root_node)
    except Exception as exc:
        return "Error reading Ardour preset file '{}': {}".format(
            args.infile, exc)

    for preset in presets:
        plugin_id = pack('>I', preset.plugin_uri).decode('ascii')
        dstdir = join(args.output_dir, plugin_id)
        if not isdir(dstdir):
            os.makedirs(dstdir)

        fxp_fn = join(dstdir, label2fn(preset.label)) + '.fxp'
        if exists(fxp_fn) and not args.force:
            print("FXP output file '%s' already exists. Skipping" % fxp_fn)
            continue

        with open(fxp_fn, 'wb') as fp:
            if isinstance(preset, Preset):
                params_fmt = '>%if' % len(preset.params)
                size = FXP_HEADER_SIZE + calcsize(params_fmt)
                num_params = len(preset.params)
                fx_magic = FX_MAGIC_PARAMS
            elif isinstance(preset, ChunkPreset):
                chunk_size = pack('>i', len(preset.chunk))
                size = FXP_HEADER_SIZE + len(chunk_size) + len(preset.chunk)
                # XXX: How to know the number of params for chunk presets?
                num_params = int(len(preset.chunk) / 4)
                fx_magic = FX_MAGIC_CHUNK
            else:
                raise TypeError("Wrong preset type: %r" % preset)

            header = pack(
                FXP_HEADER_FMT,
                CHUNK_MAGIC,
                size,
                fx_magic,
                FXP_FORMAT_VERSION,
                int(preset.plugin_uri),
                args.fx_version,
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
