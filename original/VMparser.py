from VMconstnum import *

def commentout(str):
    str = str.split("//")[0]
    return str

def isOKvarname(str):
    # return 1 --> str is availale for variable name
    if str == '':
        return 0

    if ('0' <= str[0] <= '9'):
        return 0

    return 1

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

        elif cmd[0] == C1[C_RETURN]:
            return [C_RETURN]


    if len(cmd) == 2:
        if cmd[0] == C1[C_LABEL] and isOKvarname(str[1]):
            return [C_LABEL, cmd[1]]

        if cmd[0] == C1[C_GOTO] and isOKvarname(str[1]):
            return [C_GOTO, cmd[1]]
            
        if cmd[0] == C1[C_IFGOTO] and isOKvarname(str[1]):
            return [C_IFGOTO, cmd[1]]

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
        
        elif cmd[0] == C1[C_FUNCTION] or cmd[0] == C1[C_CALL]:
            try:
                k = int(cmd[2])
            except ValueError:
                return -1
            
            if cmd[0] == C1[C_FUNCTION]:
                return [C_FUNCTION, cmd[1], k]
            else:
                return [C_CALL, cmd[1], k]

    return -1 # parse error or argument error
