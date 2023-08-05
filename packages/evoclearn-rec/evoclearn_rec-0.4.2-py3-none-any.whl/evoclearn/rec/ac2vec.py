#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bz2
import json
import os
from functools import partial
from typing import Union, IO, Iterable
from base64 import b64encode, b64decode
from functools import partial
import io
from itertools import islice

import click
import dill
import numpy as np
import librosa
from tensorflow.keras.models import model_from_json

from evoclearn.core import log, mappings, Track, Waveform
from evoclearn.core import io as evlc_io
from evoclearn.core.utils import KeepLastValue


def predict_batches_iter(x_iter, model, batchsize, transpose=False):
    while True:
        trks = islice(x_iter, batchsize)
        x = None
        for i, t in enumerate(trks):
            tmp = t.to_numpy()
            if transpose:
                tmp = tmp.T
            if i == 0:
                x = np.zeros((batchsize, *tmp.shape))
            x[i] = tmp
        if x is None:
            return
        n = i + 1
        y = model.predict(x)
        for i in range(n):
            yield y[i]


class Ac2Vec(object):
    def __init__(self,
                 featlength,
                 batchsize,
                 featsettings,
                 featnormfunc,
                 veclabels,
                 vec2symfunc,
                 model,
                 unittype,
                 segdims,
                 samplerate,
                 transpose=False,
                 logger=None):
        self.featlength = featlength
        self.batchsize = batchsize
        self.featsettings = featsettings
        self.featnormfunc = featnormfunc
        self.veclabels = veclabels
        self.vec2symfunc = vec2symfunc
        self.model = model
        self.unittype = unittype
        self.segdims = segdims
        assert len(self.unittype) == len(self.segdims)
        self.samplerate = samplerate
        self.transpose = transpose
        self.logger = logger
        self._feats = None #used for debugging to inspect input feats...

    def to_json(self) -> str:
        d = {"featlength": self.featlength,
             "batchsize": self.batchsize,
             "featsettings": self.featsettings,
             "veclabels": self.veclabels,
             "unittype": self.unittype,
             "segdims": self.segdims,
             "samplerate": self.samplerate,
             "transpose": self.transpose}
        d["featnormfunc"] = b64encode(dill.dumps(self.featnormfunc)).decode("ascii")
        d["vec2symfunc"] = b64encode(dill.dumps(self.vec2symfunc)).decode("ascii")
        d["modelspec"] = self.model.to_json()
        d["modelweights"] = b64encode(dill.dumps(self.model.get_weights())).decode("ascii")
        return json.dumps(d)

    @classmethod
    def from_json(cls, s: str, logger=None) -> "Ac2Vec":
        d = json.loads(s)
        featlength = d["featlength"]
        batchsize = d["batchsize"]
        featsettings = d["featsettings"]
        veclabels = d["veclabels"]
        unittype = d["unittype"]
        segdims = d["segdims"]
        samplerate = d["samplerate"]
        transpose = d.get("transpose") or False
        featnormfunc = dill.loads(b64decode(d["featnormfunc"]))
        vec2symfunc = dill.loads(b64decode(d["vec2symfunc"]))
        model = model_from_json(d["modelspec"])
        model.set_weights(dill.loads(b64decode(d["modelweights"])))
        return cls(featlength,
                   batchsize,
                   featsettings,
                   featnormfunc,
                   veclabels,
                   vec2symfunc,
                   model,
                   unittype,
                   segdims,
                   samplerate,
                   transpose,
                   logger)

    def to_file(self, f: Union[str, IO[str]]):
        d = self.to_json()
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "wt") as outfh:
                outfh.write(d)
        else:
            f.write(d)
        return self

    @classmethod
    def from_file(cls, f: Union[str, IO[str]], logger=None) -> "Ac2Vec":
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "rt") as infh:
                return cls.from_json(infh.read(), logger)
        else:
            cls.from_json(f.read(), logger)

    def __call__(self,
                 x_iter: Iterable[Union[Track, Waveform]],
                 from_wav=False,
                 vtln_warpfactor=None,
                 innorm=True,
                 outsyms=False):
        predict = partial(predict_batches_iter,
                          model=self.model,
                          batchsize=self.batchsize,
                          transpose=self.transpose)
        if from_wav:
            if innorm == False:
                raise ValueError("Can't disable input normalisation with wav input...")
            get_features = partial(mappings.feattrack2,
                                   warp_alpha=vtln_warpfactor,
                                   **self.featsettings)
            resample = partial(mappings.resample_wave,
                               samplerate=self.samplerate)
            requantized_iter = KeepLastValue(map(evlc_io.wav_int16_to_float,
                                                 map(evlc_io.wav_float_to_int16,
                                                     x_iter)))
            resampled_iter = KeepLastValue(map(resample,
                                               requantized_iter))
            feat_iter = KeepLastValue(map(self.featnormfunc,
                                          map(get_features,
                                              resampled_iter)))
            y_iter = predict(feat_iter)
        else:
            if vtln_warpfactor == True:
                raise ValueError("Can't apply freq. warping from precalculated feats...")
            if innorm:
                feat_iter = KeepLastValue(map(self.featnormfunc, x_iter))
            y_iter = predict(feat_iter)
        if outsyms:
            y_iter = map(self.vec2symfunc, y_iter)
        for i, y in enumerate(y_iter):
            if (i + 1) % 100 == 0:
                if self.logger: self.logger.info("Processed %s...", i + 1)
            self._feats = feat_iter.last_value
            # if from_wav:
            #     self._wav_requant = requantized_iter.last_value
            #     self._wav_resamp = resampled_iter.last_value
            yield y


@click.command()
@click.option("--outputsyms", is_flag=True)
@click.option("--vtln_warpfactor", type=click.FloatRange(min=0.1, max=1.8))
@click.argument("ac2vecfile", type=click.Path(exists=True))
@click.argument("outputprefix", type=str)
@click.argument("inputpaths",
                type=click.Path(exists=True),
                required=True,
                nargs=-1)
def main(outputsyms,
         vtln_warpfactor,
         ac2vecfile,
         outputprefix,
         inputpaths):
    logger = log.getLogger("evl.rec.ac2vec")

    ac2vec = Ac2Vec.from_file(ac2vecfile, logger)

    if any((p.endswith(".wav") or p.endswith(".flac")) for p in inputpaths):
        #Input wavs
        to_syms = partial(ac2vec,
                          from_wav=True,
                          vtln_warpfactor=vtln_warpfactor,
                          innorm=True,
                          outsyms=outputsyms)
        syms = to_syms(map(evlc_io.load_audio, inputpaths))
    else:
        #Input feats
        if vtln_warpfactor is not None:
            click.UsageError("--vtln_warpfactor only possible with WAV inputs...")
        to_syms = partial(ac2vec,
                          from_wav=False,
                          innorm=True,
                          outsyms=outputsyms)
        syms = to_syms(map(partial(Track.from_file,
                                   dtype=np.float32),
                           inputpaths))

    #Output
    # import matplotlib.pyplot as pl ##REM
    for i, (sym, infpath) in enumerate(zip(syms, inputpaths)):
        outbname = f'{outputprefix}{infpath.replace("/", "_")}'
        # ac2vec._feats.plot() ##REM
        # pl.show()            ##REM
        with open(outbname + ".txt", "w") as outfh:
            if outputsyms:
                outfh.write("-".join(sym) + "\n")
            else:
                outfh.write("\t".join(map(str, sym)) + "\n")


if __name__ == "__main__":
    main()
