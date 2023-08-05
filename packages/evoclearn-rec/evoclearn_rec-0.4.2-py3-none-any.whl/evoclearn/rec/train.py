#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from functools import partial
import json

import dill
import click
import numpy as np
import tensorflow.keras.utils
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Dropout, Dense
from tensorflow.keras.callbacks import CSVLogger

from evoclearn.core import Track, Tracks
from evoclearn.core import log
from evoclearn.core import mappings
from evoclearn.core import utils

from . import __version__
from . import timit_cv as defs


def define_model(n_steps, n_indims, n_outdims):
    model = Sequential()
    model.add(Bidirectional(LSTM(256, return_sequences=True),
                            input_shape=(n_steps, n_indims)))
    model.add(Dropout(0.50))
    model.add(Bidirectional(LSTM(256)))
    model.add(Dropout(0.50))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(n_outdims, activation="sigmoid"))
    opt = Adam(learning_rate=0.001)
    model.compile(loss="mse", optimizer=opt)
    return model


class DataWrapperInMem(tensorflow.keras.utils.Sequence):
    def __init__(self, logger, x_src=None, y_src=None, x_norm=None, y_norm=None, **kwargs):
        self.logger = logger

        if x_src is not None:
            self.logger.debug("Loading/normalising all x-data...")
            self.x = self._load_data(x_src, x_norm)
            self.logger.debug("Done loading x-data, shape=%s", self.x.shape)

        if y_src is not None:
            self.logger.debug("Loading/normalising all y-data...")
            self.y = self._load_data(y_src, y_norm)
            self.logger.debug("Done loading y-data, shape=%s", self.y.shape)

        self.__dict__.update(kwargs)

    @classmethod
    def from_npz(cls, npz_fn: str, logger) -> "DataWrapperInMem":
        data = np.load(npz_fn)
        return cls(logger, **{"x": data["x"], "y": data["y"]})

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, idx):
        raise NotImplementedError

    def create_model(self):
        n_steps, n_indims = self.x[0].shape
        n_outdims = len(self.y[0])
        return define_model(n_steps, n_indims, n_outdims)

    def _load_data(self, src, norm):
        if norm is not None:
            sample = np.array(norm(src[0]))
            arr = np.empty((len(src), *sample.shape), dtype=np.float32)
            arr[:] = np.nan
            for i in range(len(src)):
                if (i + 1) % 1000 == 0:
                    self.logger.debug("Processed %s...", i + 1)
                arr[i] = norm(src[i])
        else:
            self.logger.warn("NO NORMALISATION function defined for %s", src)
            arr = src.vci.values
            if arr.dtype.name != "float32":
                arr = arr.astype("float32", copy=False)
        return arr


def create_feats_norm_func(feat_stats, max_feat_len):
    normfunc = utils.compose_funcs(partial(mappings.normalise_standard,
                                           stats=feat_stats),
                                   partial(Track.pad,
                                           n=max_feat_len,
                                           repeat_n=1,
                                           location="front"))
    return normfunc



@click.command()
@click.option("--max_feat_len",
              default=121,
              show_default=True,
              type=int)
@click.option("--batch_size",
              default=32,
              show_default=True,
              type=int)
@click.option("--epochs",
              default=20,
              show_default=True,
              type=int)
@click.option("--use_data_cache",
              is_flag=True)
@click.option("--feat_just_zscore",
              is_flag=True)
@click.option("--only_funcs",
              is_flag=True,
              help="Only create normalisation and inverse functions")
@click.option("--only_cache",
              is_flag=True,
              help="Only create functions and data cache")
@click.argument("workingprefix",
                type=click.Path())
def main(max_feat_len,
         batch_size,
         epochs,
         use_data_cache,
         feat_just_zscore,
         only_funcs,
         only_cache,
         workingprefix):
    logger = log.getLogger("evl.rec.train")

    ##CREATE AND STORE FEATS NORM FUNCS
    feat_stats_file = f"{workingprefix}train_x_stats.json"
    logger.info("Creating feats norm/inverse functions using: %s", feat_stats_file)
    with open(feat_stats_file) as infh:
        feat_stats = json.load(infh)
    feats_normfunc = create_feats_norm_func(feat_stats, max_feat_len)
    with open(f"{workingprefix}x_norm.func.dl", "wb") as outfh:
        dill.dump(feats_normfunc, outfh)
    with open(f"{workingprefix}vec_to_syms.func.dl", "wb") as outfh:
         dill.dump(defs.vec_to_syms, outfh)
    
    if only_funcs:
        sys.exit()

    ##CREATE TRAIN AND VALIDATION DATA SOURCES
    data = {}
    for dataset in ["train", "valid"]:
        if not use_data_cache:
            x_src_file = f"{workingprefix}{dataset}_x.tracks.h5"
            y_src_file = f"{workingprefix}{dataset}_y.npz"
            logger.info("Data sources %s: x_src=%s, y_src=%s",
                        dataset.upper(),
                        x_src_file,
                        y_src_file)
            #load feats:
            x_src = Tracks.from_disk(x_src_file, slurp=True)
            if feat_just_zscore and dataset == "train":
                logger.warn("Fast-tracking the TRAIN feat normalisation (--feat_just_zscore)...")
                from scipy.stats import zscore
                arr = x_src.vci.values
                arr = arr.reshape((-1, arr.shape[-1]))
                arr[:] = zscore(arr, 0)
                x_norm = None
            else:
                x_norm = feats_normfunc
            #load y:
            y = np.load(y_src_file)["y"]
            #
            data[dataset] = DataWrapperInMem(x_src=x_src,
                                             x_norm=x_norm,
                                             y=y,
                                             logger=logger)
            ##DUMP FIT-READY DATA CACHE
            np.savez_compressed(f"{workingprefix}{dataset}.npz",
                                x=data[dataset].x,
                                y=data[dataset].y)
        else:
            data[dataset] = DataWrapperInMem.from_npz(f"{workingprefix}{dataset}.npz",
                                                      logger=logger)

    if only_cache:
        sys.exit()

    ##TRAIN MODEL
    start_time = datetime.now().strftime("%Y%m%d%H%M")
    settings_summary = f'v{__version__.replace(".", "-")}_b{batch_size}_l{max_feat_len}_e{epochs}'
    
    callbacks = ([CSVLogger(os.path.join(os.getenv("EVOCLEARN_LOG_DIR"),
                                        f"{start_time}.{settings_summary}.tsv"),
                           separator="\t")]
                 if os.getenv("EVOCLEARN_LOG_DIR") is not None
                 else None)
    model = data["train"].create_model()
    process_data = model.fit(x=data["train"].x,
                             y=data["train"].y,
                             batch_size=batch_size,
                             epochs=epochs,
                             shuffle=True,
                             validation_data=(data["valid"].x, data["valid"].y),
                             callbacks=callbacks)
    basename = (f'{workingprefix}model'
                f'.{start_time}'
                f'.{settings_summary}')
    model.save(f'{basename}.h5')
    with open(f"{basename}.json", "w") as outfh:
        json.dump({"loss": process_data.history["loss"],
                   "val_loss": process_data.history["val_loss"]},
                  outfh)


if __name__ == "__main__":
    main()
