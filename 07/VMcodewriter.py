import VMconstnum as c

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

def write_push(x, o):
    o.write("@" + str(x) + "\n")
    o.write("D=A\n")
    o.write(sp)
    o.write("A=M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_addsub(cmd0, o):
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    if cmd0 == c.C_SUB:
        o.write("D=-D\n")
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=D+M\n")
    o.write("M=D\n")
    o.write(sp)
    o.write("M=M+1\n")

def write_eqgtlt(cmd0, o, Jnum):
    write_addsub(c.C_SUB, o)
    o.write(sp)
    o.write("M=M-1\n")
    o.write("A=M\n")
    o.write("D=M\n")
    o.write(makeJ(Jnum))
    if cmd0 == c.C_EQ:
        o.write("D;JEQ\n")
    elif cmd0 == c.C_GT:
        o.write("D;JGT\n")
    elif cmd0 == c.C_LT:
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
    if cmd[0] in {c.C_ADD,c.C_SUB}:
        write_addsub(cmd[0], o)
        
    elif cmd[0] in {c.C_EQ,c.C_GT,c.C_LT}:
        write_eqgtlt(cmd[0], o, Jnum)
        Jnum += 2
    elif cmd[0] == c.C_PUSH:
        if cmd[1] == c.C_CONSTANT:
            write_push(cmd[2], o)
    
    return [Vnum, Jnum]

