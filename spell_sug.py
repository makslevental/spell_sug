
# -*- coding: utf-8 -*-
import curses, traceback
import Trie
import lang
import Tkinter

class simpleapp_tk(Tkinter.Tk):


    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        eng_model = lang.Model(lang.Language.ENGLISH)
        self.t = Trie.FreqTrie.fromdict(dict(eng_model.model.items()[:1000]))
        self.d = None
        self.r = None
        self.initialize()

    def initialize(self):
        self.grid()

        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Key>", self.OnWrite)

        self.labelVariable = Tkinter.StringVar()
        self.labelVariable.set("")
        label = Tkinter.Label(self,
                              anchor="w",fg="white",bg="blue", height=0, textvariable=self.labelVariable,
                              wraplength=300)
        label.grid(column=0,row=1,columnspan=2,sticky='EW')

        self.grid_columnconfigure(0,weight=1)
    def OnWrite(self, event):
        letter = event.char
        word = self.entry.get()

        if letter == '\b':
            if len(word)-1 <= 0:
                self.d = None
                self.labelVariable.set('')
                return
            else:
                self.d,self.r = self.t.matches(word[:-1])
                suggestions = ",".join([w for w,_ in self.r[0:10]])
        else:
            word += letter
            if self.d:
                self.d,self.r = self.t.matches(letter,self.d)
            else:
                self.d,self.r = self.t.matches(letter)

            suggestions = ",".join(map(lambda x: word+x[1:],[w for w,_ in self.r[0:10]]))
        self.update()
        self.labelVariable.set(suggestions)


if __name__ == "__main__":
    # rus_model = lang.Model(lang.Language.RUSSIAN)
    # # rus_model.model = dict(rus_model.model.items()[0:50000])
    # t = Trie.FreqTrie.fromdict(rus_model.model)


    app = simpleapp_tk(None)
    app.title('Spelling Suggestion')
    app.mainloop()

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
    #     stdscr.addstr(2, 3, 'start writing a word')
    #     stdscr.refresh()
    #
    #     c = 3
    #     letter = stdscr.getkey(2 + 1, c)
    #     c += 1
    #     word = [letter]
    #     d,r = t.matches(letter)
    #     i = 1
    #     # stdscr.addstr(1,3, ''.join(word))
    #     stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i])+x[i:],[w for w,_ in r[0:10]])))
    #     stdscr.refresh()
    #     while True:
    #         letter = stdscr.getkey(2 + 1, c)
    #         if letter == 'KEY_BACKSPACE':
    #             word.pop()
    #             d,_ = t.matches(''.join(word))
    #             stdscr.addstr(1,3, ''.join(word))
    #         # TODO-me statistics on at what word length i should just do pruning of the list
    #         # and hence be able to back up here more efficiently
    #             continue
    #         word.append(letter)
    #         # stdscr.addstr(1,3, ''.join(word))
    #         c+=1
    #         i+=1
    #         d,r = t.matches(letter,d)
    #         # print d,r
    #         stdscr.addstr(4,3,",".join(map(lambda x: ''.join(word[:i])+x[1:],[w for w,_ in r[0:10]])))
    #         stdscr.clrtoeol()
    #         stdscr.refresh()
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
