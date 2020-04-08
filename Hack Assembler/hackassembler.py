import symbolTable
import binaryConversion
import sys, os

# the file is given as a terminal input
assemblyfile = sys.argv[1]
assemblyfile_name = os.path.basename(assemblyfile)
if "." in assemblyfile_name:
    assemblyfile_name = assemblyfile_name[:assemblyfile_name.find('.')]

binaryfile_name = assemblyfile_name + '.hack'

# delete contents of the file if it exists
with open(binaryfile_name, 'w') as binaryFile:
    pass

# to keep track of the instruction address for goto instructions and variables
instruction_addr = 0  
# open the assembly file
with open(assemblyfile, 'r') as sourcefile:
    # first pass
    for line in sourcefile:
        line = line.strip()
        if "/" in line:
            line = line[:line.find('/')]  # to ignore in line comments
        if len(line) > 0 and line[0] !="/":   # ignoring whitespaces and comments
            if line[0] == '(':
                symbolTable.addSymbol(line[1:-1], instruction_addr)
            else:
                instruction_addr += 1

# second pass
# all variables get stored starting at address 16
n = 16 
with open(assemblyfile, 'r') as sourcefile:
    for line in sourcefile:
        binaryOutput = ""    # to be written to .hack file 
        line = line.strip()
        if len(line) > 0 and line[0] !="/":   # ignoring whitespaces and comments
            if "/" in line:
                line = line[:line.find('/')]  # to ignore in line commentsc
            # code to handle A instructions
            if line[0] == '@': 
                binaryOutput = "0"
                if line[1:].isdigit():  # R0..R15
                    binaryOutput += binaryConversion.getBinary(line[1:]) + "\n"
                elif line[2:].isdigit():  # R0..R15
                    binaryOutput += binaryConversion.getBinary(line[2:]) + "\n"
                elif (line[1:] not in symbolTable.SYMBOLS): # it is a variable symbol
                    symbolTable.addSymbol(line[1:], n)
                    binaryOutput += binaryConversion.getBinary(n) + "\n"
                    n += 1
                else:  # labels
                    binaryOutput += binaryConversion.getBinary(symbolTable.getSymbolAddress(line[1:])) + "\n"
            # code to handle C instructions
            elif line[0] != "(":  
                if "/" in line:
                    line = line[:line.find('/')]  # to ignore in line comments
                binaryOutput = "111" 
                line = line.replace(" ","")
                pos1 = line.find("=")
                if "=" in line:
                    pos2 = line.find(";")
                    if ";" in line:
                        pos2 = line.find(";")
                        # addingthe control bits
                        binaryOutput += symbolTable.getControlCode(str(line[pos1+1:pos2])) 
                        # adding the destination bits 
                        binaryOutput += symbolTable.getDestAddress(line[:pos1])
                        # adding the jump bits
                        binaryOutput += symbolTable.getJumpAddress(line[pos2+1:]) + "\n"
                    else:
                        # addingthe control bits
                        binaryOutput += symbolTable.getControlCode(line[pos1+1:])
                        # adding the destination bits
                        binaryOutput += symbolTable.getDestAddress(line[:pos1])
                        # adding the destination bits (000)
                        binaryOutput += "000\n"
                else:
                    if ";" in line:
                        pos2 = line.find(";")
                        # addingthe control bits
                        binaryOutput += symbolTable.getControlCode(str(line[:pos2])) 
                        # adding the destination bits 
                        binaryOutput += "000"
                        # adding the jump bits
                        binaryOutput += symbolTable.getJumpAddress(line[pos2+1:]) + "\n"
                    else:
                        # addingthe control bits
                        binaryOutput += "000"
                        # adding the destination bits
                        binaryOutput += "000"
                        # adding the destination bits (000)
                        binaryOutput += "000\n"

            with open(binaryfile_name, 'a') as binaryFile:
                binaryFile.write(binaryOutput)