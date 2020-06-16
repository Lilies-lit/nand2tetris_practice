# -*- coding: utf-8 -*-
from JackConstSyntax import *


def readword(word):
    # output [*,*,*]
    # 0 .. end
    # -1 .. " Error
    # -2 .. Num error

    if word[0] == '"':
        return [5, word[1:-1]]

    elif word[0] in NUMHEAD:
        try:
            k = int(word)
        except ValueError:
            return -1
        
        if (k < 0) or (32767 < k):
            return -2

        return [4, k]

    elif word in KEYWORD:
        index = KEYWORD.index(word)
        return [1, index]

    elif word in SYMBOL:
        index = SYMBOL.index(word)
        return [2, index]

    else:
        return [3, word] # identifier



    


