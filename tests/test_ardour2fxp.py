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
    ('vst-1331185229-single', 'OXFM', 'Nerf Pluck',
     'de90b1b924d74877d85248c0d5f5339741277372'),
])
def test_chunkpreset_single(infn, plugin_id, label, sha1sum):
    """Converting an ardour presets file with a single ChunkPreset produces
       correct output."""
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


@pytest.mark.parametrize("infn,plugin_id,labels,sha1sums", [
    (
        'vst-1331185229',
        'OXFM',
        ('Kick', 'Snare', 'INIT'),
        (
            'b9c493fb4bd05e6b2167a852fd230204d438748a',
            '942ed7564580f3cc2b40d0a02abe74aa4e6b177f',
            '045ca4bd1e9ca874e2f187ce15dbb7b856942eec',
        ),
    ),
])
def test_chunkpreset_multi(infn, plugin_id, labels, sha1sums):
    """Converting an ardour presets file with multiple ChunkPresets produces
       correct output."""
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

    for i, label in enumerate(labels):
        outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')
        assert exists(outfile)
        assert sha1_digest(outfile) == sha1sums[i]


@pytest.mark.parametrize("infn,plugin_id,label,sha1sum", [
    ('vst-1466847281', 'WnP1', 'Drum Reverb',
     '1af7a14d82eb2d87be608126ea4716cd722b86d8'),
])
def test_parampreset_single(infn, plugin_id, label, sha1sum):
    """Converting an ardour presets file with a single parameter Preset produces
       correct output."""
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


# TODO: find or create real-life example files for this test
@pytest.mark.skip()
@pytest.mark.parametrize("infn,plugin_id,labels,sha1sums", [
    (
        'vst-1234567890',
        'ABCD',
        ('Preset 1', 'Preset 2', 'Preset 3'),
        (
            'abcdef1234567890abcdef1234567890abcdef12',
            'abcdef1234567890abcdef1234567890abcdef12',
            'abcdef1234567890abcdef1234567890abcdef12',
        ),
    ),
])
def test_parampreset_multi(infn, plugin_id, labels, sha1sums):
    """Converting an ardour presets file with multiple parameter Presets produces
       correct output."""
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

    for i, label in enumerate(labels):
        outfile = join(outdir, plugin_id, label.replace(' ', '_') + '.fxp')
        assert exists(outfile)
        assert sha1_digest(outfile) == sha1sums[i]
