// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@i
M = 0
(LOOPA)
@i
D = M
@SCREEN
A = A + D
M = 0

@i
M = M + 1

@i
D = M
@8192
D = D - A

@INITA
D;JGE

@KBD
D = M;
@INITB
D;JGT

@LOOPA
0;JMP

(INITA)
@i
M = 0
@LOOPA
0;JMP



(LOOPB)
@i
D = M
@SCREEN
A = A + D
M = 1

@i
M = M + 1

@i
D = M
@8192
D = D - A

@INITB
D;JGE

@KBD
D = M;
@INITA
D;JEQ
@LOOPB
0;JMP

(INITB)
@i
M = 0
@LOOPB
0;JMP

