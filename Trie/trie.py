
# -*- coding: utf-8 -*-
"""
Trie data structure specialized to strings, insertions and traversals only.
Adapted from https://bitbucket.org/gsakkis/pytrie.
Work only for py 2.
"""
import curses, traceback, os
import pprint


class Trie:
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

    def matches(self, word, root=None):
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
        return new_root,map(lambda y: word+y, map(lambda x: x.replace('&',''), sugs))
    # TODO-me sorting by top 10

    @classmethod
    def fromlist(cls,corpus):
        t = cls()
        for word in corpus:
            t.insert(word)

        return t


class FreqTrie(Trie):

    def insert(self, word_tuple):

        nxt = self._root

        for l in word_tuple[0]:
            if l in nxt:
                nxt = nxt[l]
            else:
                nxt[l] = {}
                nxt = nxt[l]

        nxt[str(word_tuple[1])] = {}

    def matches(self, word, root=None):
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
        return new_root,map(lambda y: (word+y[0],y[1]), map(lambda x: (x[:-1], int(x[-1])), sugs))



if __name__ == '__main__':
    pass
    # import pickle
    # with open('/home/maksim/dev_projects/spell_sug/model_pkl','r') as f:
    #     model = pickle.load(f)
    # model = {word: score for word,score in model.items() if score > 5}
    # t = Trie.fromlist(model.keys())

    # while True:
    #     start = raw_input()
    #     # start = u'резу'
    #     print start[0]
    #     d,r = t.matches(start[0])
    #     print ",".join(map(lambda x: start[:1]+x,r[1:10]))
    #     for i in range(1,len(start)):
    #         print start[i]
    #         d,r = t.matches(start[i],d)
    #         print ",".join(map(lambda x: start[:i]+x,r[1:10]))
    #
    # with open(os.path.dirname(os.path.realpath(__file__))+os.path.sep+"../lang/english_words.txt") as f:
    #         t = Trie.fromlist(f.read().split('\n'))

    # letter = raw_input('write a letter: ')
    # word = [letter]
    # d,r = t.matches(letter)
    # i = 1
    # print ",".join(map(lambda x: ''.join(word[:i])+x[1:],r[0:10]))
    # while True:
    #     i+=1
    #     letter = raw_input('write a letter: ')
    #     word.append(letter)
    #     d,r = t.matches(letter,d)
    #     print ",".join(map(lambda x: ''.join(word[:i])+x[1:],r[0:10]))
