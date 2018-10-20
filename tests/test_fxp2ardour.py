# -*- coding: utf-8 -*-
"""Tests for 'fxp2ardour' script."""

import hashlib
import os

from os.path import dirname, join, exists
import pytest

from fxp2ardour import main

TESTDATA_DIR = join(dirname(__file__), 'testdata')
TESTOUTPUT_DIR = join(dirname(__file__), 'testoutput')


def sha1_digest(fn):
    with open(fn, 'rb') as fp:
        return hashlib.sha1(fp.read()).hexdigest()


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('MDAx_Harp_FxCk.fxp', 'vst-1296318840', '8609ff4e5d400487abfdbc10eeb97975a66b9f35'),
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
    assert sha1_digest(outfile) == sha1sum


@pytest.mark.parametrize("infn,outfn,sha1sum", [
    ('OXFM_GlassyEPiano_FPCh.fxp', 'vst-1331185229', 'aa90cb4a2ef6a12b701e3e0eeda8f2d315ef551b'),
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
    assert sha1_digest(outfile) == sha1sum
