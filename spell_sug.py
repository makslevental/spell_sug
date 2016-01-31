
# -*- coding: utf-8 -*-
import collections
import codecs
import re
import curses, traceback
def train(fp):
    model = collections.defaultdict(lambda: 1)
    with codecs.open(fp,encoding='utf-8') as f:
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
    try:
        # Initialize curses
        stdscr = curses.initscr()
        stdscr.clear()
        # where no buffering is performed on keyboard input
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)


        curses.echo()
        stdscr.addstr(2, 3, 'start writing a word')
        stdscr.refresh()

        c = 3
        letter = stdscr.getkey(2 + 1, c)
        c += 1
        word = [letter]
        d,r = t.matches(letter)
        i = 1
        # stdscr.addstr(1,3, ''.join(word))
        stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i])+x[i:],r[1:10])))
        stdscr.refresh()
        while True:
            letter = stdscr.getkey(2 + 1, c)
            # if letter == 'KEY_BACKSPACE':
            #     word.pop()
            #     stdscr.addstr(1,3, ''.join(word))
            # TODO-me statistics on at what word length i should just do pruning of the list
            # and hence be able to back up here
            #     continue
            word.append(letter)
            # stdscr.addstr(1,3, ''.join(word))
            c+=1
            i+=1
            d,r = t.matches(letter,d)
            # print d,r
            stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i])+x[1:],r[0:10])))
            stdscr.clrtoeol()
            stdscr.refresh()


        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()                 # Terminate curses
    except Exception as e:
        # In event of error, restore terminal to sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception
