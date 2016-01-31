
# -*- coding: utf-8 -*-
"""
Trie data structure specialized to strings, insertions and traversals only.
Adapted from https://bitbucket.org/gsakkis/pytrie.
Work only for py 2.
"""

import pprint
import lang
import operator

class Trie():
    def __init__(self):
        self._root = {}
        self._pp = pprint.PrettyPrinter(indent=1)

    def __repr__(self):
        return self._pp.pformat(self._root)

    def __str__(self):
        return self._pp.pformat(self._root).replace('{',' ').replace('}',' ')

    def insert(self, word):

        nxt = self._root

        for l in word:
            if l in nxt:
                nxt = nxt[l]
            else:
                nxt[l] = {}
                nxt = nxt[l]
        nxt['&'] = {}

    def _suffices(self, word, root=None):

        if not root:
            root = self._root
        p = root[word[0]]
        for l in word[1:]:
            p = p[l]

        new_root = p
        sug = ['']
        sugs = []
        iter_stack = []
        iter_stack.append(p.iteritems())

        while iter_stack:
            try:
                nxt = iter_stack[-1].next()
            except StopIteration:
                sug.pop()
                iter_stack.pop()
                continue
            letter, p = nxt
            sug.append(letter)
            if p:
                iter_stack.append(p.iteritems())
            else:
                sugs.append("".join(sug))
                sug.pop()
        return new_root, sugs

    def matches(self, word, root=None):
        new_root, sugs = self._suffices(word, root)
        return new_root,map(lambda y: word+y, map(lambda x: x.replace('&',''), sugs))
    # TODO-me sorting by top 10

    @classmethod
    def fromlist(cls,corpus):
        t = cls()
        for word in corpus:
            t.insert(word)

        return t


class FreqTrie(Trie):
    def __init__(self):
        Trie.__init__(self)

    def insert(self, word_tuple):

        nxt = self._root

        for l in word_tuple[0]:
            if l in nxt:
                nxt = nxt[l]
            else:
                nxt[l] = {}
                nxt = nxt[l]

        nxt['&'+str(word_tuple[1])] = {}

    def matches(self, word, root=None):
        new_root, sugs = self._suffices(word, root)
        return new_root, sorted(map(lambda y: (word+y[0],y[1] if len(y) == 2 else 0),
                                    map(lambda x: tuple(x.split('&')), sugs)),
                                key=lambda x:int(operator.itemgetter(1)(x)),reverse=True)


    @classmethod
    def fromdict(cls, corpus_dict):
        t = cls()
        for word_tuple in corpus_dict.items():
            t.insert(word_tuple)

        return t



if __name__ == '__main__':

    # eng_model = lang.Model(lang.Language.ENGLISH)
    # eng_model.model = dict(eng_model.model.items()[0:50000])
    # ftrie = FreqTrie.fromdict(eng_model.model)
    # _,d = ftrie.matches('fa')
    # print d
    #

    rus_model = lang.Model(lang.Language.RUSSIAN)
    # rus_model.model = dict(rus_model.model.items()[0:50000])
    ftrie = FreqTrie.fromdict(rus_model.model)
    _,d = ftrie.matches(u'резу')
    for w in d:
        print w[0],w[1]