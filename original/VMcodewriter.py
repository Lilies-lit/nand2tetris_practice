from VMconstnum import *

sp = '@SP\n'

def init(o):
    o.write("@256\n")
    o.write("D=A\n")
    o.write(sp)
    o.write("M=D\n")

def makeJl(Jnum):
    #  (J0)
    return "(J" + str(Jnum) + ")\n"

def makeJ(Jnum):
    # @J0
    return '@J' + str(Jnum) + '\n'

def write_pushconst(x, o):
    o.write("@" + str(x) + "\n")
    o.write("D=A\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_push(cmd1, x, o):
    if cmd1 == C_LOCAL:
        o.write("@LCL\n")
    elif cmd1 == C_ARGUMENT:
        o.write("@ARG\n")
    elif cmd1 == C_THIS:
        o.write("@THIS\n")
    elif cmd1 == C_THAT:
        o.write("@THAT\n")

    o.write("D=M\n")
    o.write("@" + str(x) + "\n")
    o.write("D=D+A\n")
    o.write("A=D\n")
    o.write("D=M\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_pop(cmd1, x, o):
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")

    if cmd1 == C_LOCAL:
        o.write("@LCL\n")
    elif cmd1 == C_ARGUMENT:
        o.write("@ARG\n")
    elif cmd1 == C_THIS:
        o.write("@THIS\n")
    elif cmd1 == C_THAT:
        o.write("@THAT\n")
    o.write("A=M\n")
    for i in range(x):
        o.write("A=A+1\n")
    o.write("M=D\n")

def write_pushpt(cmd1, x, o):
    if cmd1 == C_POINTER:
        o.write("@3\n")
    elif cmd1 == C_TEMP:
        o.write("@5\n")
    o.write("D=A\n")
    o.write("@" + str(x) + "\n")
    o.write("D=D+A\n")
    o.write("A=D\n")
    o.write("D=M\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_poppt(cmd1, x, o):
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    if cmd1 == C_POINTER:
        o.write("@3\n")
    elif cmd1 == C_TEMP:
        o.write("@5\n")
    for i in range(x):
        o.write("A=A+1\n")
    o.write("M=D\n")

def write_pushstatic(x, o):
    fname = o.name
    fname = fname.split("/")[-1]
    o.write("@" + fname + "." + str(x) + "\n") # @filename.vm.x
    o.write("D=M\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_popstatic(x, o):
    fname = o.name
    fname = fname.split("/")[-1]
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    o.write("@" + fname + "." + str(x) + "\n")  # @filename.vm.x
    o.write("M=D\n")

def write_op(cmd0, o):
    # +, -, and, or
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    if cmd0 == C_SUB:
        o.write("D=-D\n")
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    if cmd0 == C_ADD or cmd0 == C_SUB:
        o.write("D=D+M\n")
    elif cmd0 == C_OR:
        o.write("D=D|M\n")
    elif cmd0 == C_AND:
        o.write("D=D&M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_not(o):
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    o.write("M=!D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_neg(o):
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    o.write("M=-D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_eqgtlt(cmd0, o, Jnum):
    write_op(C_SUB, o)
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    o.write(makeJ(Jnum))
    if cmd0 == C_EQ:
        o.write("D;JEQ\n")
    elif cmd0 == C_GT:
        o.write("D;JGT\n")
    elif cmd0 == C_LT:
        o.write("D;JLT\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=0\n")
    o.write(makeJ(Jnum+1))
    o.write("0;JMP\n")
    o.write(makeJl(Jnum))
    o.write(sp)
    o.write("A=M\n")
    o.write("M=-1\n")
    o.write(makeJl(Jnum+1))
    o.write(sp)
    o.write("M=M+1\n")


def writecmd(cmd, o, Vnum, Jnum):
    if cmd[0] in {C_ADD,C_SUB,C_AND,C_OR}:
        write_op(cmd[0], o)
        
    elif cmd[0] == C_NEG:
        write_neg(o)

    elif cmd[0] == C_NOT:
        write_not(o)

    elif cmd[0] in {C_EQ,C_GT,C_LT}:
        write_eqgtlt(cmd[0], o, Jnum)
        Jnum += 2
    elif cmd[0] == C_PUSH:
        if cmd[1] == C_CONSTANT:
            write_pushconst(cmd[2], o)
        elif cmd[1] in {C_LOCAL,C_ARGUMENT,C_THIS,C_THAT}:
            write_push(cmd[1], cmd[2], o)
        elif cmd[1] in {C_POINTER, C_TEMP}:
            write_pushpt(cmd[1], cmd[2], o)
        elif cmd[1] == C_STATIC:
            write_pushstatic(cmd[2], o)

    elif cmd[0] == C_POP:
        if cmd[1] in {C_LOCAL,C_ARGUMENT,C_THIS,C_THAT}:
            write_pop(cmd[1], cmd[2], o)
        elif cmd[1] in {C_POINTER, C_TEMP}:
            write_poppt(cmd[1], cmd[2], o)
        elif cmd[1] == C_STATIC:
            write_popstatic(cmd[2], o)

    return [Vnum, Jnum]

