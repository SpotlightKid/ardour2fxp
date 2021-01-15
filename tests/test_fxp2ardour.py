# -*- coding: utf-8 -*-
"""Tests for 'fxp2ardour' script."""

import hashlib
import os
import shutil

from os.path import dirname, join, exists
from xml.dom import minidom
import pytest

from fxp2ardour import main

TESTDATA_DIR = join(dirname(__file__), 'testdata')
TESTOUTPUT_DIR = join(dirname(__file__), 'testoutput')


def sha1_digest(fn):
    with open(fn, 'rb') as fp:
        return hashlib.sha1(fp.read()).hexdigest()


def check_output(fn):
    """Reformat given XML file with xml.dom.minidom and return SHA1 checksum of
       resulting file.
    """
    xml = minidom.parse(fn)

    with open(fn, 'wb') as fp:
        fp.write(xml.toprettyxml(indent='  ', encoding='utf-8'))

    return sha1_digest(fn)


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('MDAx_Harp_FxCk.fxp', 'vst-1296318840',
     '7af1e786bf94bbecda30fdde3c791ceb56da50f4'),
])
def test_fxp_fxck(infn, outfn, sha1sum):
    """Converting an FXP file of type FxCk produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    outdir = join(TESTOUTPUT_DIR, 'ardour')
    outfile = join(outdir, outfn)

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    ret = main(["-o", outdir, infile])

    assert ret is None
    assert exists(outfile)
    assert check_output(outfile) == sha1sum


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('OXFM_GlassyEPiano_FPCh.fxp', 'vst-1331185229',
     '30db17c08c70fd75aebce52e8193cb56b251f0bd'),
])
def test_fxp_fpch(infn, outfn, sha1sum):
    """Converting an FXP file of type FPCh produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    outdir = join(TESTOUTPUT_DIR, 'ardour')
    outfile = join(outdir, outfn)

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    ret = main(["-o", outdir, infile])

    assert ret is None
    assert exists(outfile)
    assert check_output(outfile) == sha1sum


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('OXFM_GlassyEPiano_FPCh.fxp', 'vst-1331185229',
     'b40bf52a84811379dda0cac81ba292bf9fd97e15'),
])
def test_fxp_merge(infn, outfn, sha1sum):
    """Converting and merging an FXP file produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    infile2 = join(TESTDATA_DIR, outfn)
    outdir = join(TESTOUTPUT_DIR, 'ardour')
    outfile = join(outdir, outfn)

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(infile2, outfile)
    ret = main(["-o", outdir, "-m", infile])

    assert ret is None
    assert exists(outfile)
    assert check_output(outfile) == sha1sum


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('OXFM_Kick_FPCh.fxp', 'vst-1331185229',
     '93c6dd14c89e5ff5d5d27d01930fdf05f898b968'),
])
def test_fxp_append(infn, outfn, sha1sum):
    """Converting and appending an FXP file produces correct output."""
    infile = join(TESTDATA_DIR, infn)
    infile2 = join(TESTDATA_DIR, outfn)
    outdir = join(TESTOUTPUT_DIR, 'ardour')
    outfile = join(outdir, outfn)

    try:
        os.remove(outfile)
    except OSError:
        pass

    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(infile2, outfile)
    ret = main(["-o", outdir, "-a", infile])

    assert ret is None
    assert exists(outfile)
    assert check_output(outfile) == sha1sum
