
# -*- coding: utf-8 -*-
import collections
import codecs
import re
import pickle
from damerau_levenshtein_distance import dl_dist

def train():
    model = collections.defaultdict(lambda: 1)
    with codecs.open('/home/maksim/Downloads/news.2014.ru.shuffled.v2',encoding='utf-8') as f:
        for line in f:
            words = re.findall(r'[\w]+',line.lower(),re.U)
            for w in words:
                model[w] += 1
    return model

def one_edits(word):
    """
    generate all words 1 edit distance away.
    author: http://norvig.com/spell-correct.html
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def two_edits(word):
    """ 
    generate all words 2 edit distance away. 
    author: http://norvig.com/spell-correct.html
    """
    #outside in - for X in A: for x in X: x
    return set(e2 for e1 in one_edits(word) for e2 in one_edits(e1))

def known_edits(word,editor,lang_dict):
    """
    only actual words
    """
    return set(w for w in editor(word) if w in lang_dict)

if __name__ == "__main__":
    model = train()
    with open('model_pkl','wb') as f:
        pickle.dump(dict(model),f)
