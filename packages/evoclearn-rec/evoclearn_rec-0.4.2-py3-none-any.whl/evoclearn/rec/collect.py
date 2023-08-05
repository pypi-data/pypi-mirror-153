#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from functools import partial
from glob import glob
import json

import click
import numpy as np
import pandas as pd

from evoclearn.core import log
from evoclearn.core import io
from evoclearn.core.mappings import feattrack2
from evoclearn.core import Track, Tracks

from . import timit_cv as defs


def make_stats(feats, outfn):
    arr = feats.vci.values.reshape((-1, feats.vci.values.shape[-1]))
    feats_mean = arr.mean(0)
    feats_std = arr.std(0)
    df = pd.DataFrame([feats_mean, feats_std], index=["mean", "std"])
    with open(outfn, "w") as outfh:
        outfh.write(df.to_json())


@click.command()
@click.option("--max_feat_len",
              default=121,
              show_default=True,
              type=int)
@click.argument("featsettingsfile", type=click.File())
@click.argument("indir", type=click.Path(exists=True))
@click.argument("outpathprefix", type=str)
def main(max_feat_len, featsettingsfile, indir, outpathprefix):
    logger = log.getLogger("evl.rec.collect")

    featsettings = json.load(featsettingsfile)
    logger.info("Loaded feature settings from: %s", featsettingsfile.name)
    
    fpaths = sorted(glob(os.path.join(indir, "*.wav")))
    logger.info("Found %s input wav files...", len(fpaths))

    vecs = None
    for i, fpath in enumerate(fpaths):
        if (i + 1) % 100 == 0:
            logger.debug("Processed %s output vectors...", i + 1)
        #outputs
        bn = os.path.basename(fpath)
        syms = bn.split("_")[0].split("-")[:2]
        vec = defs.syms_to_vec(*syms)
        if vecs is None:
            vecs = np.zeros((len(fpaths), len(vec)), dtype=np.float32)
        vecs[i] = vec
    with open(f"{outpathprefix}paths.txt", "w") as outfh:
        outfh.write("\n".join(fpaths) + "\n")
    y_outpath = f"{outpathprefix}y.npz"
    np.savez_compressed(y_outpath, y=vecs)
    logger.info("Written output vectors to: %s", y_outpath)

    #inputs
    x_outpath = f"{outpathprefix}x.tracks.h5"
    wavs = map(io.load_audio, fpaths)
    feats = map(partial(feattrack2, **featsettings), wavs)
    padded_feats = map(partial(Track.pad, n=max_feat_len, repeat_n=1, location="front"), feats)
    Tracks.from_iter(padded_feats).to_disk(x_outpath, resize_length=100)
    logger.info("Written input samples to: %s", x_outpath)

    #input stats for normalisation
    featstats_outpath = f"{outpathprefix}x_stats.json"
    logger.info("Making feats stats...")
    samples = Tracks.from_disk(x_outpath, slurp=True)
    make_stats(samples, featstats_outpath)
    logger.info("Written feature stats to: %s", featstats_outpath)


if __name__ == "__main__":
    main()
