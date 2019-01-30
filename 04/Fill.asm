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

// Put your code here.
@KBD
D=A
@KBDaddr
M=D  //M[KBDaddr]=24576

@SCREEN
D=A
@SCRaddr
M=D  //M[SCRaddr]=16384

(LOOP)
@KBDaddr
A=M
D=M //M[24576]
@ELSE
D;JLE //M[24576]?=0

@KBD
D=A
@SCRaddr
D=D-M
@LOOP
D;JEQ //if screen's pixel is full, goto LOOP

@SCRaddr
A=M
M=-1 //present screen pixel is black

@SCRaddr
M=M+1 //M[SCRaddr]+=1

@LOOP
0;JMP //GOTO LOOP

(ELSE)
@SCRaddr
A=M
M=0 //present screen pixel is white

@SCREEN
D=A
@SCRaddr
D=D-M
@LOOP
D;JEQ //if screen's pixel is clear, goto LOOP

@SCRaddr
M=M-1 //M[SCRaddr]-=1

@LOOP
0;JMP