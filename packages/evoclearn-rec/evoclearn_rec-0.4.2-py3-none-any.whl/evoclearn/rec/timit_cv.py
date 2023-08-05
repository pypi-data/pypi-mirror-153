# -*- coding: utf-8 -*-

import numpy as np

CLOSURES = {"b": ["h#", "bcl"],
            "d": ["h#", "dcl"],
            "g": ["h#", "gcl"]}

NUM_CONSONANTS = 3
CONSONANTS = {
    "b": 0,
    "d": 1,
    "g": 2,
}
INV_CONSONANTS = {v:k for k, v in CONSONANTS.items()}

NUM_VOWELS = 8
VOWELS = {
    "aa": 0,
    "ae": 1,
    "ah": 2,
    "ao": 3,
    "eh": 4,
    "ih": 5,
    "iy": 6,
    "uh": 7,
    "uw": 7,
    "ux": 7,
}
def mapv(vsym):
    return "u" if vsym.startswith("u") else vsym
INV_VOWELS = {v:mapv(k) for k, v in VOWELS.items()}


def syms_to_vec(c, v,
                num_consonants=NUM_CONSONANTS,
                consonant_map=CONSONANTS,
                num_vowels=NUM_VOWELS,
                vowel_map=VOWELS):
    vec = np.zeros(num_consonants + num_vowels,
                   dtype=np.float32)
    vec[consonant_map[c]] = 1.0
    vec[num_consonants + vowel_map[v]] = 1.0
    return vec

def vec_to_syms(vec,
                num_consonants=NUM_CONSONANTS,
                consonant_invmap=INV_CONSONANTS,
                vowel_invmap=INV_VOWELS):
    c = consonant_invmap[vec[:num_consonants].argmax()]
    v = vowel_invmap[vec[num_consonants:].argmax()]
    return c, v
