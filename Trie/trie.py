"""
Trie data structure specialized to strings, insertions and traversals only.
Adapted from https://bitbucket.org/gsakkis/pytrie.
Work only for py 2.
"""
import copy
from collections import MutableMapping
import pprint

# #singleton sentinel to cap leaves
# class SENTINEL(object):
#     pass
#
# class TrieNode(object):
#     """
#     By default, instances of both old and new-style classes have a dictionary for
#     attribute storage. This wastes space for objects having very few instance variables.
#     The space consumption can become acute when creating large numbers of instances.
#
#     The default can be overridden by defining __slots__ in a new-style class definition.
#     The __slots__ declaration takes a sequence of instance variables and reserves just
#     enough space in each instance to hold a value for each variable.
#     Space is saved because __dict__ is not created for each instance.
#     """
#     __slots__ = ('letter','children')
#
#     def __init__(self,letter=SENTINEL):
#         self.letter = letter
#         self.children = dict()
#
#     def __repr__(self):
#         return self.letter if self.letter is not SENTINEL else 'SENTINEL' + '->' + str(self.children)
#
#     def __copy__(self):
#         # self.__class__ == TrieNode. This call basically makes a new TrieNode with
#         # the same letter as its value. self.__class__ is a callable that makes a new instance
#         # then __init__ is called.
#         clone_of_self = self.__class__(self.letter)
#         clone_children = copy.deepcopy(self.children)
#
#     def __getstate__(self):
#         return (self.letter,self.children)
#
#     def __setstate__(self, state):
#         self.letter, self.children = state


class Trie:
    def __init__(self):
        self._root = {}
        self._pp = pprint.PrettyPrinter(indent=1)

    def __repr__(self):
        return self._pp.pformat(self._root)

    def __str__(self):
        return self._pp.pformat(self._root).replace('{',' ').replace('}',' ')

    def insert(self, word):

        next = self._root

        for l in word:
            if l in next:
                next = next[l]
            else:
                next[l] = {}
                next = next[l]
        next['!']={}

    def matches(self,word):
        p = self._root[word[0]]
        for l in word[1:]:
            p = p[l]

        sug = ['#']
        sugs = []
        stack = []
        stack.append(p.iteritems())
        while stack:
            try:
                nxt = stack[-1].next()
            except StopIteration:
                sug.pop()
                stack.pop()
                continue
            letter, p = nxt
            sug.append(letter)
            if p:
                stack.append(p.iteritems())
            else:
                sugs.append("".join(sug))
                sug.pop()
        return sugs

    @classmethod
    def fromlist(cls,corpus):
        t = cls()
        for word in corpus:
            t.insert(word)

        return t


if __name__ == '__main__':

    t = Trie.fromlist(['bob','ben','benton','bedstuy'])
    print t
    print t.matches('be')
