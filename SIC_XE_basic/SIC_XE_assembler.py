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
B = 0
L = 0
PC = 0
SW = 0
RowList = []
# 0 for symbol 1 for opCode 2 for operand
ProgramList = []
LocalCounterList = []
MRecordList = []
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
        if RowList[0] != ".":
            if RowList[0]:  # if not null string
                if function_db.symbol_table_contain(RowList[0]) == 0:  # if not contain in symbol table add
                    function_db.symbol_table_add(RowList[0], localCounter)
                else:  # if contain
                    print("existing symbol")
                    print(RowList[0])
                    sys.exit()
            if RowList[1] == "BASE":  # spec for this statement
                LocalCounterList.append("none")
            if RowList[1] == "ADDR" or RowList[1] == "CLEAR" or RowList[1] == "COMPR" or RowList[1] == "DIVR" or \
                    RowList[1] == "MULR" or RowList[1] == "RMO" or RowList[1] == "SHIFTL" or RowList[1] == "SHIFTR" or \
                    RowList[1] == "SUBR" or RowList[1] == "SVC" or RowList[1] == "TIXR":  # special OpCode
                LocalCounterList.append(localCounter)
                localCounter = function_db.hex_add(localCounter, hex(2))
            elif RowList[1][0] == "+" and function_db.op_table_get_op_code(RowList[1][1:]) != 0:
                LocalCounterList.append(localCounter)
                localCounter = function_db.hex_add(localCounter, hex(4))
            elif function_db.op_table_get_op_code(RowList[1]) != 0:
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
                ProgramList[focusCount][4] = function_db.op_table_get_op_code(ProgramList[focusCount][2])
                if ProgramList[focusCount][3]:
                    if ProgramList[focusCount][3][0] == "#" and function_db.symbol_table_get(
                            ProgramList[focusCount][3][1:]) != -1:
                        tmpFocus = focusCount + 1
                        while ProgramList[tmpFocus][0] == "none":
                            tmpFocus = tmpFocus + 1
                        ProgramList[focusCount][4] = function_db.hex_add("0x" + ProgramList[focusCount][4], "0x1")
                        displace = function_db.hex_sub(function_db.symbol_table_get(ProgramList[focusCount][3][1:]),
                                                       ProgramList[tmpFocus][0])
                        if -2048 < int(displace, 16) < 2047:
                            ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "2"
                        elif 0 < int(displace, 16) < 4095:
                            ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "4"
                        ProgramList[focusCount][4] += displace[2:].zfill(3)
                    elif ProgramList[focusCount][3][0] == "#" and function_db.symbol_table_get(
                            ProgramList[focusCount][3][1:]) == -1:
                        displace = hex(int(ProgramList[focusCount][3][1:]))[2:].zfill(3)
                        ProgramList[focusCount][4] = function_db.hex_add("0x" + (ProgramList[focusCount][4]), "0x1")[2:]
                        ProgramList[focusCount][4] += "0" + displace[2:].zfill(3)
                        ProgramList[focusCount][4] = ProgramList[focusCount][4].zfill(6)
                    elif ProgramList[focusCount][3][0] == "@" and function_db.symbol_table_get(
                            ProgramList[focusCount][3][1:]) != -1:
                        tmpFocus = focusCount + 1
                        while ProgramList[tmpFocus][0] == "none":
                            tmpFocus = tmpFocus + 1
                        ProgramList[focusCount][4] = function_db.hex_add("0x" + ProgramList[focusCount][4], "0x2")
                        displace = function_db.hex_sub(function_db.symbol_table_get(ProgramList[focusCount][3][1:]),
                                                       ProgramList[tmpFocus][0])
                        if -2048 < int(displace, 16) < 2047:
                            ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "2"
                        elif 0 < int(displace, 16) < 4095:
                            ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "4"
                        ProgramList[focusCount][4] += displace[2:].zfill(3)
                    elif ProgramList[focusCount][2] == "CLEAR" or ProgramList[focusCount][2] == "COMPR" \
                            or ProgramList[focusCount][2] == "DIVR" or ProgramList[focusCount][2] == "MULR" \
                            or ProgramList[focusCount][2] == "RMO" or ProgramList[focusCount][2] == "SHIFTL" \
                            or ProgramList[focusCount][2] == "SHIFTR" or ProgramList[focusCount][2] == "SUBR" \
                            or ProgramList[focusCount][2] == "TIXR":
                        tmpSymbol = ProgramList[focusCount][3].split(",")
                        par1 = str(function_db.symbol_table_get(tmpSymbol[0]))
                        if len(tmpSymbol) > 1:
                            par2 = function_db.symbol_table_get(tmpSymbol[1])
                            if par2 == -1:
                                par2 = "0"
                        else:
                            par2 = "0"
                        ProgramList[focusCount][4] = str(
                            function_db.op_table_get_op_code(ProgramList[focusCount][2])).zfill(2) + par1 + par2
                    elif function_db.op_table_get_op_code(ProgramList[focusCount][2]) != 0:
                        tmpFocus = focusCount + 1
                        while ProgramList[tmpFocus][0] == "none":
                            tmpFocus = tmpFocus + 1
                        ProgramList[focusCount][4] = function_db.hex_add("0x" + ProgramList[focusCount][4], "0x3")
                        if function_db.symbol_table_get(ProgramList[focusCount][3]) != -1:
                            displace = function_db.hex_sub(function_db.symbol_table_get(ProgramList[focusCount][3]),
                                                           ProgramList[tmpFocus][0])
                            if -2048 < int(displace, 16) < 2047:
                                ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "2"
                                if 0 > int(displace, 16):
                                    displace = hex(int(displace, 16) & 0xfff)
                                ProgramList[focusCount][4] += displace[2:].zfill(3)
                            else:
                                ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "4"
                                displace = function_db.hex_sub(function_db.symbol_table_get(ProgramList[focusCount][3]), B)[2:].zfill(3)
                                ProgramList[focusCount][4] += displace[2:].zfill(3)
                        ProgramList[focusCount][4] = ProgramList[focusCount][4].zfill(6)
                        if "," in ProgramList[focusCount][3]:
                            bufSym = ProgramList[focusCount][3].split(",")
                            if function_db.symbol_table_get(bufSym[0]) != -1 and bufSym[1] == "X":
                                displace = function_db.hex_sub(function_db.symbol_table_get(bufSym[0]),
                                                               ProgramList[tmpFocus][0])
                                if -2048 < int(displace, 16) < 2047:
                                    ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "A"
                                else:
                                    ProgramList[focusCount][4] = ProgramList[focusCount][4][2:] + "C"
                                    displace = function_db.hex_sub(function_db.symbol_table_get(bufSym[0]), B)
                                ProgramList[focusCount][4] += displace[2:].zfill(3)
                                ProgramList[focusCount][4] = ProgramList[focusCount][4][2:]
                else:
                    if function_db.op_table_get_op_code(ProgramList[focusCount][2]) != 0:
                        ProgramList[focusCount][4] = (function_db.hex_add("0x" + function_db.op_table_get_op_code(
                            ProgramList[focusCount][2]), "0x3") + "0000")[2:]
            elif ProgramList[focusCount][2] == "BASE":
                B = function_db.symbol_table_get(ProgramList[focusCount][3])
            elif ProgramList[focusCount][2] == "RESW" or ProgramList[focusCount][2] == "RESB":
                ProgramList[focusCount][4] = "none"
            elif ProgramList[focusCount][2] == "BYTE":
                rowLabel = ProgramList[focusCount][3].split("\'")
                if rowLabel[0] == "X":
                    ProgramList[focusCount][4] = rowLabel[1]
                elif rowLabel[0] == "C":
                    ProgramList[focusCount][4] = ""
                    for i in range(0, len(rowLabel[1])):
                        ProgramList[focusCount][4] += hex(ord(rowLabel[1][i]))[2:]
            elif ProgramList[focusCount][2][0] == "+" and function_db.op_table_get_op_code(ProgramList[focusCount][2][1:]):
                if ProgramList[focusCount][3][0] == "#" and function_db.symbol_table_get(ProgramList[focusCount][3][1:]) == -1:
                    ProgramList[focusCount][4] = function_db.hex_add("0x"+function_db.op_table_get_op_code(ProgramList[focusCount][2][1:]), "0x1")[2:]
                    ProgramList[focusCount][4] += "1"
                    ProgramList[focusCount][4] += hex(int(ProgramList[focusCount][3][1:]))[2:].zfill(5)
                elif function_db.symbol_table_get(ProgramList[focusCount][3]) != -1:
                    MAddress = function_db.hex_add(ProgramList[focusCount][0], "0x1")[2:].zfill(6)
                    MRecordList.append("M"+MAddress + str(len(function_db.symbol_table_get(ProgramList[focusCount][3])[2:].zfill(5))).zfill(2))
                    ProgramList[focusCount][4] = function_db.hex_add("0x"+function_db.op_table_get_op_code(ProgramList[focusCount][2][1:]), "0x3")[2:]
                    ProgramList[focusCount][4] += "1"
                    ProgramList[focusCount][4] += function_db.symbol_table_get(ProgramList[focusCount][3])[2:].zfill(5)
            else:
                print("opCode not found")
                print(ProgramList[focusCount])
                sys.exit()
        focusCount = focusCount + 1

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
    if function_db.op_table_get_op_code(ProgramList[focusCount][2]) != 0 or\
            function_db.op_table_get_op_code(ProgramList[focusCount][2][1:]) != 0 or\
            ProgramList[focusCount][2] == "WORD" or\
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

for i in range(0, len(MRecordList)):
    print(MRecordList[i])

print(ERecord)

file.close()

file = open(fileName + ".lst", "w")
for i in range(0, len(ProgramList)):
    for j in range(0, 5):
        if ProgramList[i][j] == "none" or ProgramList[i][j] == "":
            ProgramList[i][j] = ""

for i in range(0, len(ProgramList)):
    file.write('\t'.join(map(str, ProgramList[i])))
    file.write("\n")
file.close()

file = open(fileName + ".obj", "w")
file.write(headRecord+"\n")
for i in range(0, len(TRecordAll)):
    file.write(''.join(map(str, TRecordAll[i])))
    file.write("\n")

for i in range(0, len(MRecordList)):
    file.write(''.join(map(str, MRecordList[i])))
    file.write("\n")
file.write(ERecord)
file.close()