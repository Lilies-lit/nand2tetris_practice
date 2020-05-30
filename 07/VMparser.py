import VMconstnum as c

def parse(str):
    cmd = str.split()
    if len(cmd) == 1:
        if cmd[0] == c.C1[c.C_ADD]:
            return [c.C_ADD]
        elif cmd[0] == c.C1[c.C_SUB]:
            return [c.C_SUB]
        elif cmd[0] == c.C1[c.C_EQ]:
            return [c.C_EQ]
        elif cmd[0] == c.C1[c.C_EQ]:
            return [c.C_EQ]
        elif cmd[0] == c.C1[c.C_GT]:
            return [c.C_GT]
        elif cmd[0] == c.C1[c.C_LT]:
            return [c.C_LT]
            
    if len(cmd) == 2:
        pass
    if len(cmd) == 3:
        if cmd[0] == c.C1[c.C_PUSH]:
            x = c.C_PUSH
            try:
                z = int(cmd[2])
            except ValueError:
                return -1 # cast int error
            if cmd[1] in c.C2:
                y = c.C2.index(cmd[1])
                return [x,y,z]
            else:
                return -1


    return -1 # argument num error
