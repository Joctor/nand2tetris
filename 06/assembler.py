# -*- coding: utf-8 -*-

#Initialzation
symbol_table = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5,
                'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11,
                'R12':12, 'R13':13, 'R14':14, 'R15':15, 
                'SCREEN':16384, 'KBD':24576, 'SP':0, 'LCL':1, 'ARG':2,
                'THIS':3, 'THAT':4}

comp_table = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000',
              '!D':'0001101', '!A':'0110001', '-D':'0001111', '-A':'0110011', 'D+1':'0011111',
              'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010', 'D+A':'0000010', 'D-A':'0010011',
              'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101',
              'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010',
              'D+M':'1000010', 'D-M':'1010011', 'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101'}

dest_table = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}

jump_table = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

def read_data(file):
    data=[]
    with open(file) as f:
        for line in f:
            data.append(line.strip().split('      ')[0])
    return data

def del_unneeded(data):
    for i in range(len(data)-1, -1, -1):
        if data[i] == '':
            data.pop(i)
        elif data[i][0] == '/':
            data.pop(i)
    return data

#Scan the entire program
def first_pass(data):
    count = 0
    for i in range(len(data)):
        if data[i][0] == '(':
            length = len(data[i])
            symbol_table[data[i][1:length-1]] = i - count
            count += 1
    
    for i in range(len(data)-1, -1, -1):
        if data[i][0] == '(':
            data.pop(i) 
    return data

def second_pass(data):
    n = 16
    for i in range(len(data)):
        if data[i][0] == '@':
            name = data[i][1:]
            if str.isdigit(name):
                symbol_table[name] = int(name)
            elif name in symbol_table:
                pass
            else:
                symbol_table[name] = n
                n += 1
            data[i] = A_ten2two(name)
        else:
            data[i] = C_trans(data[i])
    return data

def A_ten2two(name):
    bin_num = bin(symbol_table[name])[2:]
    final_num = '0' * (16 - len(bin_num)) + bin_num
    return final_num

def C_trans(symbol):
    dest=symbol.split('=')
    if len(dest) == 2:
        comp = dest[1]
        dest = dest[0]
        jump = 'null'
    else:
        comp, jump = dest[0].split(';')[0], dest[0].split(';')[1]
        dest = 'null'
    
    return '111' + comp_table[comp] + dest_table[dest] + jump_table[jump]
    


data = read_data('./pong/Pong.asm')
data = del_unneeded(data)
data = first_pass(data)
data = second_pass(data)

output = open('Pong.hack', 'w')
for line in data:
    output.write(line+'\n')