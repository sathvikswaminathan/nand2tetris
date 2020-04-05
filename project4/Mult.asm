// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// pseudo code
// product = 0;
// for(i=0; i<R1; i++){
// product = product + R0;
// }
// R2 = product;

// initalizing values
@i 
M = 1
@R2
M = 0

(LOOP)
    // loop terminating condition
    @i
    D = M
    @R1
    D = M-D
    @END
    D;JLT

    // loop to multiply
    @R0
    D = M
    @R2
    M = M + D
    @i
    M = M + 1
    @LOOP
    0;JMP

(END)
    // infinite loop (does nothing)
    @END
    0;JMP
