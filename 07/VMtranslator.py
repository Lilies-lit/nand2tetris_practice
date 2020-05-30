# -*- coding: utf-8 -*-
import sys
import VMparser
import VMconstnum as c
import VMcodewriter

def main():
    args = sys.argv
    outfileName = "a.asm"
    Vnum = 0
    Jnum = 0
    if (len(args) == 3):
        infileName = args[1]
        outfileName = args[2]
    elif(len(args) == 2):
        infileName = args[1]
    else:
        print('arguments error')
        return 1

    try:
        f = open(infileName, 'r')
        o = open(outfileName, 'w')
    except OSError:
        print("file can't open")
        return 1

    line = f.readline()
    VMcodewriter.init(o) # SP <- 256

    while line:
        str = line.strip()
        cmd = VMparser.parse(str)
        if cmd == 0:
            line = f.readline()
            continue
        elif cmd == -1:
            print('syntax error')
            o.close()
            f.close() 
            return 1

        print(cmd)

        [Vnum, Jnum] = VMcodewriter.writecmd(cmd, o, Vnum, Jnum)
        line = f.readline()

    f.close()
    o.close()

main()