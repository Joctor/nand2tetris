// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@sum
M=0  //sum=0
@i
M=0  //i=0
(LOOP)
@R0
D=M
@i
D=D-M
@STOP
D;JLE  //if R0-i<=0 goto STOP
@sum
D=M
@R1
D=D+M  
@sum
M=D   //sum+=R1
@i
M=M+1 //i+=1
@LOOP
0;JMP 
(STOP)
@sum
D=M
@R2
M=D  //RAM[R2]=sum
(END)
@END
0;JMP
