# -*- coding: utf-8 -*-
from JackConstSyntax import *
import JackTockenizer
import JackCompaliationEngine as JackComp
import sys
import re

'''
comment対応
式
'''

def main():
    print(KEYWORD)
    print(SYMBOL)
    args = sys.argv
    outFileNameT = "TokenTemp.xml"
    outFileName = "a.xml"

    if (len(args) == 3):
        inFileName = args[1]
        outFileName = args[2]
    elif(len(args) == 2):
        inFileName = args[1]
    else:
        print('arguments error')
        return 1

    try:
        o = open(outFileNameT, 'w')
    except OSError:
        print("file can't open(output)")
        return 1

    try:
        fin = open(inFileName, 'r')
    except OSError:
        print("file can't open(input)")
        return 1

    Data = fin.read()
    #erase
    Data = re.sub('//(.*)' , '' , Data)
    Data = re.sub('/\*(.|\n)*?\*/' , '' , Data)
    fin.close()

    try:
        otemp = open('intemp.jack', 'w')
    except OSError:
        print("file can't open(output temp)")
        return 1

    #write temp
    otemp.write(Data)

    otemp.close()

    try:
        f = open('intemp.jack', 'r')
    except OSError:
        print("file can't open(input temp)")
        return 1

    # tockenizer

    line = f.readline()
    Wordsqueue = []
    o.write("<tokens>\n")

    while line:
        s = line.strip()
        print(s)
        news = (re.findall('\".*\"|\<|\>|\{|\}|\(|\)|\[|\]|\||;|\+|-|\*|/|~|=|\.|\,|\w*',s))
        news = filter(lambda X: X != '', news)
        Wordsqueue.extend(news)
        line = f.readline()

    print(Wordsqueue)

    Tokenlist = []

    for word in Wordsqueue:
        E = JackTockenizer.readword(word)
        if E == -1 or E == -2:
            print('Error!')
            return 1

        Tokenlist.append(E)

    f.close()

    for token in Tokenlist:
        outline = JackTockenizer.writetoken(token)
        outline += "\n"
        o.write(outline)

    o.write("</tokens>\n")
    o.close()

    # parser
    Tokenlist.append(['END',0])

    print(Tokenlist)
    JackComp.compileFile(Tokenlist, outFileName)

main()