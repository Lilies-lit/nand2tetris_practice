from VMconstnum import *

def commentout(str):
    str = str.split("//")[0]
    return str

def parse(str):
    str = commentout(str)
    cmd = str.split()
    if len(cmd) == 0:
        return 0 # empty
    if len(cmd) == 1:
        if cmd[0] == C1[C_ADD]:
            return [C_ADD]
        elif cmd[0] == C1[C_SUB]:
            return [C_SUB]
        elif cmd[0] == C1[C_EQ]:
            return [C_EQ]
        elif cmd[0] == C1[C_GT]:
            return [C_GT]
        elif cmd[0] == C1[C_LT]:
            return [C_LT]
        elif cmd[0] == C1[C_NEG]:
            return [C_NEG]
        elif cmd[0] == C1[C_OR]:
            return [C_OR]
        elif cmd[0] == C1[C_AND]:
            return [C_AND]
        elif cmd[0] == C1[C_NOT]:
            return [C_NOT]

    if len(cmd) == 2:
        pass
    if len(cmd) == 3:
        if cmd[0] in {C1[C_PUSH], C1[C_POP]}:
            if cmd[0] == C1[C_PUSH]:
                x = C_PUSH
            else:
                x = C_POP
            try:
                z = int(cmd[2])
            except ValueError:
                return -1 # cast int error
            if cmd[1] in C2:
                y = C2.index(cmd[1])
                return [x,y,z]
            else:
                return -1


    return -1 # argument num error
