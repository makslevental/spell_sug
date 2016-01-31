# -*- coding: utf-8 -*-
"""
Sets language parameters for spell_sug
"""

import collections, codecs, re, pickle, os, bz2

eng_albet = 'abcdefghijklmnopqrstuvwxyz'
rus_albet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
file_loc = os.path.dirname(os.path.realpath(__file__))+os.path.sep

class Language:
    ENGLISH = 1
    RUSSIAN = 2

class Model:
    def __init__(self, lang):
        self.lang = lang
        if lang == Language.ENGLISH:
            self.albet = eng_albet
            with open(file_loc+'model_pkl_eng', 'r') as f:
                self.model = pickle.load(f)
        elif lang == Language.RUSSIAN:
            self.albet = rus_albet
            with open(file_loc+'model_pkl_rus', 'r') as f:
                self.model = pickle.load(f)

    @classmethod
    def __train(cls,fp,lang):

        if lang == Language.ENGLISH:
            encod = 'ascii'
        elif lang == Language.RUSSIAN:
            encod = 'utf-8'

        model = collections.defaultdict(lambda: 1)
        # with open(fp,'r') as f:
        with codecs.open(fp,encoding=encod) as f:
            for line in f:
                words = re.findall(r'[\w]+',line.lower(),re.U)
                for w in words:
                    model[w] += 1
        return model
    @classmethod
    def __create_model(cls,fp,lang):

        model = cls.__train(fp,lang)
        if lang == Language.ENGLISH:
            model_fp = file_loc+'model_pkl_eng'
        elif lang == Language.RUSSIAN:
            model_fp = file_loc+'model_pkl_rus'

        with open(model_fp, 'wb') as f:
            pickle.dump(dict(model), f)

    @classmethod
    def __unbzip(cls,fp):
        zipfile = bz2.BZ2File(fp)
        data = zipfile.read()
        newfp = fp[:-4]
        open(newfp, 'wb').write(data)

if __name__ == "__main__":
    m = Model(Language.ENGLISH)
    print m.model[1:10]