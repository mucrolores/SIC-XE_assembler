# -*- coding: utf-8 -*-
"""
Created on Tue May 21 00:33:10 2019

@author: mucolores
"""

import assembler_function as function_db
import sys

fileName = input()
file = open(fileName + ".asm", "r")

A = 0
X = 0
L = 0
PC = 0
SW = 0
RowList = []
# 0 for symbol 1 for opCode 2 for operand
ProgramList = []
LocalCounterList = []
ProgramLength = 0

startAddress = 0
localCounter = 0x0
columnCounter = 0

function_db.get_one_row(file, RowList, ProgramList)
if RowList[1] == "START":
    startAddress = RowList[2]
    startAddress = "0x" + startAddress
    localCounter = startAddress
    LocalCounterList.append(localCounter)
    columnCounter = columnCounter + 1

    while RowList[1] != "END":
        function_db.get_one_row(file, RowList, ProgramList)
        print(RowList)
        if RowList[0] != ".":
            if RowList[0]:  # if not null string
                if function_db.symbol_table_contain(RowList[0]) == 0:  # if not contain in symbol table add
                    function_db.symbol_table_add(RowList[0], localCounter)
                else:  # if contain
                    print("existing symbol")
                    print(RowList[0])
                    sys.exit()
            if function_db.op_table_get_op_code(RowList[1]) != 0:
                LocalCounterList.append(localCounter)
                localCounter = function_db.hex_add(localCounter, hex(3))
            elif RowList[1] == "WORD":
                LocalCounterList.append(localCounter)
                localCounter = hex((int(localCounter, 16) + 3))
            elif RowList[1] == "RESW":
                LocalCounterList.append(localCounter)
                localCounter = function_db.hex_add(localCounter, hex(3 * int(RowList[2])))
            elif RowList[1] == "RESB":
                LocalCounterList.append(localCounter)
                localCounter = function_db.hex_add(localCounter, hex(int(RowList[2])))
            elif RowList[1] == "BYTE":
                byteOperand = RowList[2]
                BYTELength = 0
                BYTEStart = 0
                while byteOperand[BYTELength] != '\'':
                    BYTELength = BYTELength + 1
                BYTELength = BYTELength + 1
                BYTEStart = BYTELength
                while byteOperand[BYTELength] != '\'':
                    BYTELength = BYTELength + 1
                BYTELength = BYTELength - BYTEStart
                LocalCounterList.append(localCounter)
                if byteOperand[0] == "X":
                    localCounter = function_db.hex_add(localCounter, hex(int(int(BYTELength) / 2)))
                elif byteOperand[0] == "C":
                    localCounter = function_db.hex_add(localCounter, hex(BYTELength))
        else:
            LocalCounterList.append("CMDx")
        columnCounter = columnCounter + 1
    LocalCounterList.append(localCounter)

else:
    print("No start localCounter set to 0")

for i in range(0, columnCounter):
    ProgramList[i][0] = LocalCounterList[i]

for i in range(0, len(ProgramList)):
    print(ProgramList[i])

ProgramLength = hex(int(localCounter, 0) - int(startAddress, 0))
print("ProgramLength", ProgramLength)

print("Pass 1 finish")

focusCount = 0
if ProgramList[0][2] == "START":
    focusCount = focusCount + 1
    while ProgramList[focusCount][2] != "END":
        if ProgramList[focusCount][0] != "CMDx":
            if function_db.op_table_get_op_code(ProgramList[focusCount][2]) != 0:
                if ProgramList[focusCount][3]:
                    if function_db.symbol_table_contain(ProgramList[focusCount][3]):
                        ProgramList[focusCount][3] = function_db.symbol_table_get(ProgramList[focusCount][3])
                    else:
                        tmp = ProgramList[focusCount][3].split(",")
                        if function_db.symbol_table_contain(tmp[0]):
                            ProgramList[focusCount][3] = function_db.symbol_table_get(tmp[0])
                            if tmp[1] == "X":
                                ProgramList[focusCount][3] = "0x" + str(int(ProgramList[focusCount][3][2:]) + 8000)

                        else:
                            print("symbol not found")
                            print(ProgramList[focusCount][3])
                            sys.exit()
                else:
                    ProgramList[focusCount][3] = "000000"
                ProgramList[focusCount][4] = function_db.op_table_get_op_code(ProgramList[focusCount][2])
            elif ProgramList[focusCount][2] == "WORD":
                ProgramList[focusCount][4] = str(hex(int(ProgramList[focusCount][3])))[2:].zfill(6)
            elif ProgramList[focusCount][2] == "BYTE":
                tmpCode = ProgramList[focusCount][3].split("\'")
                if tmpCode[0] == "C":
                    tmpString = ProgramList[focusCount][4]
                    for i in range(0, len(tmpCode[1])):
                        if tmpString == "none":
                            tmpString = hex(ord(tmpCode[1][i]))[2:]
                        else:
                            tmpString += hex(ord(tmpCode[1][i]))[2:]
                    ProgramList[focusCount][4] = tmpString
                elif tmpCode[0] == "X":
                    ProgramList[focusCount][4] = tmpCode[1]
        if function_db.op_table_get_op_code(ProgramList[focusCount][2]):
            ProgramList[focusCount][4] += str(ProgramList[focusCount][3])[2:]

        focusCount = focusCount + 1
else:
    print("Program Error")
    print(ProgramList[focusCount][3])
    sys.exit()

for i in range(0, len(ProgramList)):
    print(ProgramList[i])

print("Pass 2 finish")
objectRecord = []

headRecord = "H" + ProgramList[0][1] + "\t" + ProgramLength[2:].zfill(6)
TRecordAll = []
tRecord = ["", "", ""]
rowLength = 0
focusCount = 1
firstCommand = True
while ProgramList[focusCount][2] != "END":
    if function_db.op_table_get_op_code(ProgramList[focusCount][2]) != 0 or ProgramList[focusCount][2] == "WORD" or \
            ProgramList[focusCount][2] == "BYTE":
        if tRecord[0] == "":
            tRecord[0] += "T" + ProgramList[focusCount][0][2:].zfill(6)
        if rowLength + int(len(ProgramList[focusCount][4]) / 2) <= 30:
            tRecord[2] += ProgramList[focusCount][4]
            rowLength = rowLength + int(len(ProgramList[focusCount][4]) / 2)
        else:
            tRecord[1] = hex(rowLength)[2:]
            TRecordAll.append(tRecord)
            tRecord = ["", "", ""]
            rowLength = 0
            if tRecord[0] == "":
                tRecord[0] += "T" + ProgramList[focusCount][0][2:].zfill(6)
            if rowLength + int(len(ProgramList[focusCount][4]) / 2) <= 30:
                tRecord[2] += ProgramList[focusCount][4]
                rowLength = rowLength + int(len(ProgramList[focusCount][4]) / 2)
        firstCommand = True
    elif ProgramList[focusCount][2] == "RESW" or ProgramList[focusCount][2] == "RESB":
        if firstCommand:
            tRecord[1] = hex(rowLength)[2:]
            TRecordAll.append(tRecord)
            tRecord = ["", "", ""]
            rowLength = 0
            firstCommand = False

    focusCount = focusCount + 1
tRecord[1] = hex(rowLength)[2:].zfill(2)
TRecordAll.append(tRecord)

ERecord = "E" + ProgramList[0][3].zfill(6)

print(headRecord)
for i in range(0, len(TRecordAll)):
    print(TRecordAll[i])

print(ERecord)

file.close()

file = open(fileName + ".lst", "w")
for i in range(0, len(ProgramList)):
    for j in range (0,5):
        if ProgramList[i][j]=="none":
            del(ProgramList[i][j])

for i in range(0, len(ProgramList)):
    file.write('\t'.join(map(str, ProgramList[i])))
    file.write("\n")
file.close()

file = open(fileName + ".obj", "w")
file.write(headRecord+"\n")
for i in range(0, len(TRecordAll)):
    file.write(''.join(map(str, TRecordAll[i])))
    file.write("\n")
file.write(ERecord)
file.close()
