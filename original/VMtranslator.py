# -*- coding: utf-8 -*-
import sys
import VMparser
from VMconstnum import *
import VMcodewriter
import glob
import os

def main():
    args = sys.argv
    pattern = 0 # FileMode = 0, dirMode = 1
    outFileName = "a.asm"
    inFileNameList = []

    Jnum = 0

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

    #Select pattern
    if os.path.isdir(inFileName) == True:
        dirname = inFileName
        pattern = 1
        inFileNameList = glob.glob(dirname + '*.vm')
        print(dirname)
    else:
        inFileNameList = [inFileName]
        pattern = 0

    Jnum = VMcodewriter.init(pattern, o)

    print(inFileNameList)


    for inFileName in inFileNameList:
        try:
            f = open(inFileName, 'r')
        except OSError:
            print("file can't open")
            return 1

        line = f.readline()

        while line:
            str = line.strip()
            print(str)
            o.write("// ----- " + str + "\n")
            cmd = VMparser.parse(str)
            print(cmd)
            if cmd == 0:
                line = f.readline()
                continue
            elif cmd == -1:
                print('syntax error')
                o.close()
                f.close() 
                return 1

            Jnum = VMcodewriter.writecmd(cmd, o, f, Jnum)

            line = f.readline()
            
        f.close()


    o.close()
main()