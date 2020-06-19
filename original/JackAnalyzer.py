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
    outFileNameT = "aT.xml"
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
        f = open(inFileName, 'r')
    except OSError:
        print("file can't open")
        return 1

    # tockenizer

    line = f.readline()
    Wordsqueue = []
    o.write("<tokens>\n")
    while line:
        s = line.strip()
        s = s.split('//')[0]
        s = s.split('/**')[0]
        print(s)
        if len(s) >= 2 and s[0] == '/' and s[1] == '/':
            continue

        news = (re.findall('\".*\"|\{|\}|\(|\)|\[|\]|\||;|\+|-|\*|/|=|\.|\,|\w*',s))
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