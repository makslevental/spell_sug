
# -*- coding: utf-8 -*-
"""
Trie data structure specialized to strings, insertions and traversals only.
Adapted from https://bitbucket.org/gsakkis/pytrie.
Work only for py 2.
"""
import curses, traceback
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
        next['&']={}

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

if __name__ == '__main__':
    #
    # import pickle
    # with open('/home/maksim/dev_projects/spell_sug/model_pkl','r') as f:
    #     model = pickle.load(f)
    # model = {word: score for word,score in model.items() if score > 5}
    # t = Trie.fromlist(model.keys())
    #
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

    t = Trie.fromlist(['ben','benton','benjamin','bedstuy','bedford'])
    letter = raw_input('write a letter: ')
    word = [letter]
    d,r = t.matches(letter)
    i = 1
    print ",".join(map(lambda x: ''.join(word[:i])+x[1:],r[0:10]))
    while True:
        i+=1
        letter = raw_input('write a letter: ')
        word.append(letter)
        d,r = t.matches(letter,d)
        print ",".join(map(lambda x: ''.join(word[:i])+x[1:],r[0:10]))
    # try:
    #     # Initialize curses
    #     stdscr = curses.initscr()
    #     stdscr.clear()
    #     # where no buffering is performed on keyboard input
    #     curses.cbreak()
    #
    #     # In keypad mode, escape sequences for special keys
    #     # (like the cursor keys) will be interpreted and
    #     # a special value like curses.KEY_LEFT will be returned
    #     stdscr.keypad(1)
    #
    #
    #     curses.echo()
    #     stdscr.addstr(2, 3, 'write a word')
    #     stdscr.refresh()
    #
    #     c = 3
    #     letter = stdscr.getkey(2 + 1, c)
    #     c += 1
    #     word = [letter]
    #     d,r = t.matches(letter)
    #     i = 1
    #     stdscr.addstr(1,3, ''.join(word))
    #     stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i-1])+x,r[1:10])))
    #     while True:
    #         letter = stdscr.getkey(2 + 1, c)
    #         # if letter == 'KEY_BACKSPACE':
    #         #     word.pop()
    #         #     stdscr.addstr(1,3, ''.join(word))
    #         #     stdscr.
    #         #     continue
    #         word.append(letter)
    #         stdscr.addstr(1,3, ''.join(word))
    #         c+=1
    #         i+=1
    #         d,r = t.matches(letter,d)
    #         print d,r
    #         stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i-1])+x,r[1:10])))
    #
    #
    #     # Set everything back to normal
    #     stdscr.keypad(0)
    #     curses.echo()
    #     curses.nocbreak()
    #     curses.endwin()                 # Terminate curses
    # except Exception as e:
    #     # In event of error, restore terminal to sane state.
    #     stdscr.keypad(0)
    #     curses.echo()
    #     curses.nocbreak()
    #     curses.endwin()
    #     traceback.print_exc()           # Print the exception