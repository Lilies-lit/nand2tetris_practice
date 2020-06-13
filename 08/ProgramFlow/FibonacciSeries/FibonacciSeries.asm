@256
D=A
@SP
M=D
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push argument 1
@SP
M=M-1
A=M
D=M
@3
A=A+1
M=D
// ----- pop pointer 1           // that = argument[1]
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// ----- push constant 0
@SP
M=M-1
A=M
D=M
@THAT
A=M
M=D
// ----- pop that 0              // first element in the series = 0
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// ----- push constant 1
@SP
M=M-1
A=M
D=M
@THAT
A=M
A=A+1
M=D
// ----- pop that 1              // second element in the series = 1
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push argument 0
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// ----- push constant 2
@SP
M=M-1
A=M
D=M
D=-D
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1
// ----- sub
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// ----- pop argument 0          // num_of_elements -= 2 (first 2 elements are set)
(MAIN_LOOP_START)
// ----- label MAIN_LOOP_START
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push argument 0
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
// ----- if-goto COMPUTE_ELEMENT // if num_of_elements > 0, goto COMPUTE_ELEMENT
@END_PROGRAM
0;JMP
// ----- goto END_PROGRAM        // otherwise, goto END_PROGRAM
(COMPUTE_ELEMENT)
// ----- label COMPUTE_ELEMENT
@THAT
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push that 0
@THAT
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push that 1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1
// ----- add
@SP
M=M-1
A=M
D=M
@THAT
A=M
A=A+1
A=A+1
M=D
// ----- pop that 2              // that[2] = that[0] + that[1]
@3
D=A
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push pointer 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// ----- push constant 1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1
// ----- add
@SP
M=M-1
A=M
D=M
@3
A=A+1
M=D
// ----- pop pointer 1           // that += 1
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ----- push argument 0
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// ----- push constant 1
@SP
M=M-1
A=M
D=M
D=-D
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1
// ----- sub
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// ----- pop argument 0          // num_of_elements--
@MAIN_LOOP_START
0;JMP
// ----- goto MAIN_LOOP_START
(END_PROGRAM)
// ----- label END_PROGRAM
