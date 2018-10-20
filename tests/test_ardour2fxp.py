# -*- coding: utf-8 -*-
"""Tests for 'ardour2fxp' script."""

import hashlib
import os

from os.path import dirname, join, exists
import pytest

from ardour2fxp import main

TESTDATA_DIR = join(dirname(__file__), 'testdata')
TESTOUTPUT_DIR = join(dirname(__file__), 'testoutput')


def sha1_digest(fn):
    with open(fn, 'rb') as fp:
        return hashlib.sha1(fp.read()).hexdigest()


@pytest.mark.parametrize("infn,plugin_id,label,sha1sum", [
    ('vst-1331185229-single', 'OXFM', 'Nerf Pluck', '8609ff4e5d400487abfdbc10eeb97975a66b9f35'),
])
def test_chunkpreset_single(infn, plugin_id, sha1sum):
    """Converting an ardour presets file with a single ChunkPreset produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    outdir = join(TESTOUTPUT_DIR, 'fxp')
    outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    ret = main(["-o", outdir, infile])

    assert ret is None
    assert exists(outfile)
    assert sha1_digest(outfile) == sha1sum


@pytest.mark.parametrize("infn,plugin_id,labels", [
    ('vst-1331185229', 'OXFM', ('Kick', 'Snare', 'INIT')),
])
def test_chunkpreset_single(infn, plugin_id, labels):
    """Converting an ardour presets file with multiple ChunkPresets produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    outdir = join(TESTOUTPUT_DIR, 'fxp')

    for label in labels:
        outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')
        try:
            os.remove(outfile)
        except OSError:
            pass

    os.makedirs(outdir, exist_ok=True)
    ret = main(["-o", outdir, infile])
    assert ret is None

    for label in labels:
        outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')
        assert exists(outfile)


@pytest.mark.parametrize("infn,plugin_id,label,sha1sum", [
    ('vst-1466847281', 'WnP1', 'Drum Reverb', '1af7a14d82eb2d87be608126ea4716cd722b86d8'),
])
def test_parampreset(infn, plugin_id, label, sha1sum):
    """Converting an ardour presets file with a single ChunkPresets produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    outdir = join(TESTOUTPUT_DIR, 'fxp')
    outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    ret = main(["-o", outdir, infile])
    assert ret is None
    assert exists(outfile)
    assert sha1_digest(outfile) == sha1sum
