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
        o = open(outFileName, 'w')
    except OSError:
        print("file can't open(output)")
        return 1

    try:
        f = open(inFileName, 'r')
    except OSError:
        print("file can't open")
        return 1

    line = f.readline()
    Wordsqueue = []
    o.write("<tokens>\n")
    while line:
        s = line.strip()
        s = s.split('//')[0]
        print(s)
        if len(s) >= 2 and s[0] == '/' and s[1] == '/':
            continue

        news = (re.findall('\".*\"|\{|\}|\(|\)|;|\+|-|\*|/|=|\.|\,|\w*',s))
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

    print(Tokenlist)
    f.close()

    for token in Tokenlist:
        outline = JackComp.writetoken(token)
        outline += "\n"
        o.write(outline)

    o.write("</tokens>\n")
    o.close()


main()