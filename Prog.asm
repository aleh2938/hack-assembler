// Computes R1 = 1 + ... + R0
// i = 1
 @i
 M=1
// sum = 0
 @sum
 M=0
(LOOP)
// if i > R0 goto STOP
 @i
 D=M
 @R0
 D=D-M
 @STOP
 D;JGT
 @i
 D=M
 @sum
 M=D+M
 @i
 M=M+1
 @LOOP
 0;JMP
(STOP)
 @sum
 D=M
 @R1
 M=D
(END)
 @END
 0;JMP