def get_one_row(infile, row_list, stored_list):
    tmp_row = infile.readline().split("\t")
    row_list.clear()
    row_list.append(tmp_row[0])
    row_list.append(tmp_row[1])
    if len(tmp_row) > 2:
        row_list.append(tmp_row[2][:len(tmp_row[2])])
        if "\n" in row_list:
            row_list.remove("\n")
    else:
        row_list.append("")
    row_list[0] = row_list[0].strip()
    row_list[1] = row_list[1].strip()
    row_list[2] = row_list[2].strip()
    row_arr = ["none"] * 5
    row_arr[1] = row_list[0]
    row_arr[2] = row_list[1]
    row_arr[3] = row_list[2]
    stored_list.append(row_arr)


def print_row(row_list):
    print("tag : ", row_list[0])
    print("opCode : ", row_list[1])
    print("operand : ", row_list[2])
    print("\n")


op_table = \
    {
        "ADD": "18", "ADDF": "58", "ADDR": "90", "AND": "40", "CLEAR": "B4",
        "COMP": "28", "COMPF": "88", "COMPR": "A0", "DIV": "24", "DIVF": "64",
        "DIVR": "9C", "FIX": "C4", "FLOAT": "C0", "HIO": "F4", "J": "3C",
        "JEQ": "30", "JGT": "34", "JLT": "38", "JSUB": "48", "LDA": "00",
        "LDB": "68", "LDCH": "50", "LDF": "70", "LDL": "08", "LDS": "6C",
        "LDT": "74", "LDX": "04", "LPS": "E0", "UML": "20", "MULF": "60",
        "MULR": "98", "NORM": "C8", "OR": "44", "RD": "D8", "RMO": "AC",
        "RSUB": "4C", "SHIFTL": "A4", "SHIFTR": "A8", "SIO": "F0", "SSK": "EC",
        "STA": "0C", "STB": "78", "STCH": "54", "STF": "80", "STI": "D4",
        "STL": "14", "STS": "7C", "STSW": "E8", "STT": "84", "STX": "10",
        "SUB": "1C", "SUBF": "5C", "SUBR": "94", "SVC": "B0", "TD": "E0",
        "TIO": "F8", "TIX": "2C", "TIXR": "B8", "WD": "DC"
    }


def op_table_get_op_code(target_command):
    if target_command in op_table:
        return op_table[target_command]
    else:
        return 0


symbol_table = \
    {
        "A": "0", "X": "1", "L": "2", "B": "3", "S": "4",
        "T": "5", "F": "6", "PC": "8", "SW": "9"
    }


def symbol_table_contain(target_command):
    if target_command in symbol_table:
        return 1
    else:
        return 0


def symbol_table_add(target_command, target_value):
    if target_command not in symbol_table:
        symbol_table[target_command] = target_value
    else:
        return 0


def symbol_table_get(target_command):
    if target_command in symbol_table:
        return symbol_table[target_command]
    else:
        return -1


def symbol_print_all():
    print(symbol_table)


def hex_add(hex1, hex2):
    r_hex1 = int(hex1, 0)
    r_hex2 = int(hex2, 0)
    result = hex(r_hex1 + r_hex2)
    return result


def hex_sub(hex1, hex2):
    return hex(int(hex1, 0) - int(hex2, 0))


def hex_print(hex_num):
    print(hex_num[2:])
