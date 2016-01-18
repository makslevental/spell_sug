# -*- coding: utf-8 -*-
"""
Compute unrestricted Damerau–Levenshtein distance using modified Wagner-Fischer
DP algorithm: https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance.
Naive implementation (cubic complexity): potential improvement doi:10.1145/321879.321880
"""

from lang import albet
import numpy as np
import jellyfish 

def dl_dist(s1,s2):
    da = {a:0 for a in albet}
    ds = np.zeros((len(s1)+2,len(s2)+2))
    
    maxdist = len(s1)+len(s2)
    
    ds[:,0]=maxdist
    ds[1:,1]=np.arange(len(s1)+1)
    ds[0,:]=maxdist
    ds[1,1:]=np.arange(len(s2)+1)
    
    for i in range(0,len(s1)):
        db = 0
        for j in range(0,len(s2)):
            k = da[s2[j]]
            l = db
            if s1[i] == s2[j]:
                cost = 0
                db = j
            else:
                cost = 1
            ds[i+2,j+2] = min(ds[i-1+2,j-1+2]+cost,
                          ds[i+2,j-1+2]+1,
                          ds[i-1+2,j+2]+1,
                          ds[k-1+2,l-1+2]+(i-k+2-1)+1+(j+2-l-1))
        da[s1[i]] = i
    return ds[-1,-1]
        

import unittest
import re
import os
class Misspellings_corpus(unittest.TestCase):
    """
    test my implementation of damerau-levenshtein distance against what i imagine
    is jellyfish's reference implementation.
    """
    def test_corpus(self):
        twoWords = re.compile('([A-Za-z]+)\s+([A-Za-z]+)')
        with open(os.path.dirname(os.path.realpath(__file__))+os.path.sep+"birkbeck_spelling_error_corpus/ABODAT.643") as f:
            pairs = f.read().split(',')
            for p in pairs:
                if twoWords.search(p):
                    fst,snd = twoWords.search(p).groups()
                    print fst.lower(),snd.lower()
                    print jellyfish.damerau_levenshtein_distance(unicode(fst.lower()),unicode(snd.lower())),dl_dist(fst.lower(),snd.lower())
                    #self.assertEqual(jellyfish.damerau_levenshtein_distance(unicode(fst),unicode(snd)),dl_dist(fst,snd))

                    
            

if __name__ == "__main__":
    unittest.main()
