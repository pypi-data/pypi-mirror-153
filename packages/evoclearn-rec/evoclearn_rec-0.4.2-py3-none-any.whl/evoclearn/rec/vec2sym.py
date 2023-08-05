# -*- coding: utf-8 -*-

import numpy as np


def syms_to_vec(*segs, segdims, veclabels):
    assert sum(segdims) == len(veclabels)
    assert len(segs) == len(segdims)
    vec = np.zeros(len(veclabels), dtype=np.float32)
    for i, seg in enumerate(segs):
        startidx = sum(segdims[:i])
        labels = veclabels[startidx:startidx + segdims[i]]
        vec[startidx + labels.index(seg)] = 1.0
    return vec

def vec_to_syms(vec, segdims, veclabels):
    assert sum(segdims) == len(veclabels)
    assert len(vec) == len(veclabels)
    segs = []
    for i, segdim in enumerate(segdims):
        startidx = sum(segdims[:i])
        subidx = vec[startidx:startidx + segdim].argmax()
        segs.append(veclabels[startidx + subidx])
    return tuple(segs)
