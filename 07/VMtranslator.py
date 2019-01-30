# -*- coding: utf-8 -*-

ari_table = {'add':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n',
             'sub':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n',
             'neg':'@SP\nM=M-1\nA=M\nM=-M\n',
             
             'eq':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n', 
             'eq_trans':'@EQ{0}\nD;JEQ\n@NE{0}\nD;JNE\n(EQ{0})\n@SP\nA=M\nM=-1\n@NEXT{0}\n0;JMP\n(NE{0})\n@SP\nA=M\nM=0\n(NEXT{0})\n',
             
             'gt':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n',
             'gt_trans':'@GT{0}\nD;JGT\n@LE{0}\nD;JLE\n(GT{0})\n@SP\nA=M\nM=-1\n@NEXT{0}\n0;JMP\n(LE{0})\n@SP\nA=M\nM=0\n(NEXT{0})\n',
             
             'lt':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n',
             'lt_trans':'@LT{0}\nD;JLT\n@GE{0}\nD;JGE\n(LT{0})\n@SP\nA=M\nM=-1\n@NEXT{0}\n0;JMP\n(GE{0})\n@SP\nA=M\nM=0\n(NEXT{0})\n',
             
             'and':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n',
             'or':'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n',
             'not':'@SP\nM=M-1\nA=M\nM=!M\n'}

push_table = {'constant':'@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             
             'local':'@{0}\nD=A\n@LCL\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             'argument':'@{0}\nD=A\n@ARG\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             'this':'@{0}\nD=A\n@THIS\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             'that':'@{0}\nD=A\n@THAT\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             
             'temp':'@{0}\nD=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             
             'pointer_0':'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             'pointer_1':'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
             
             'static':'@{0}.{1}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'}
             
pop_table = {'local':'@{0}\nD=A\n@LCL\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\nM=D\n@{0}\nD=A\n@LCL\nM=M-D\n',
             'argument':'@{0}\nD=A\n@ARG\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@{0}\nD=A\n@ARG\nM=M-D\n',
             'this':'@{0}\nD=A\n@THIS\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\nM=D\n@{0}\nD=A\n@THIS\nM=M-D\n',
             'that':'@{0}\nD=A\n@THAT\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\nM=D\n@{0}\nD=A\n@THAT\nM=M-D\n',
             
             'temp':'@{0}\nD=A\n@5\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n@13\nM=0\n',
             
             'pointer_0':'@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n',
             'pointer_1':'@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n',
             
             'static':'@SP\nM=M-1\nA=M\nD=M\n@{0}.{1}\nM=D\n'}

brh_table = {'label':'({0}${1})\n',
             'goto':'@{0}${1}\n0;JMP\n',
             'if-goto':'@SP\nM=M-1\nA=M\nD=M\n@{0}${1}\nD;JLT\n'}  #depends on different requests

return_trans = '@LCL\nD=M\n@14\nM=D\n'\
                '@5\nD=A\n@14\nA=M-D\nD=M\n@15\nM=D\n'\
                '@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n'\
                '@ARG\nD=M\nD=D+1\n@SP\nM=D\n'\
                '@14\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n'\
                '@14\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n'\
                '@14\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n'\
                '@14\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n'\
                '@15\nA=M\n0;JMP\n'
                #FRAME=LCL; RET=*(FRAME-5); *ARG=POP(); SP=ARG+1; THAT=*(FRAME-1); ~ GOTO RET

call_trans = '@retAddr{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'\
            '@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'\
            '@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'\
            '@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'\
            '@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'\
            '@SP\nD=M\n@{1}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n'\
            '@SP\nD=M\n@LCL\nM=D\n'\
            '@{2}\n0;JMP\n'\
            '(retAddr{0})\n'

Bootstrap = '@256\nD=A\n@SP\nM=D\n'
        
move_a_step = '@SP\nM=M+1\n'

end = '(END)\n@END\n0;JMP\n'

ari_count = 0 #branching in arithmetic command
addr_count = 0

def read_data(file_path):
    data=[]
    with open(file_path) as f:
        for line in f:
            data.append(line.strip().split('  ')[0])
        
    for i in range(len(data)-1, -1, -1):
        if data[i] == '':
            data.pop(i)
        elif data[i][0] == '/':
            data.pop(i)
            
    for i in range(len(file_path)-3, -1, -1):
        if file_path[i] == '/':
            static_prefix = file_path[i+1:len(file_path)-3]
            break

    return data, static_prefix

def choose_implementation(data, static_prefix):
    for i in range(len(data)):
        line = data[i].split()
        first = line[0]
        if first == 'push' or first == 'pop':
            memory_segment(line, static_prefix)
        elif first == 'label' or first == 'goto' or first == 'if-goto':
            branching(line, name)
        elif first == 'function':
            function_handling(line)
        elif first == 'return':
            return_handling(line)
        elif first == 'call':
            call_handling(line)
        else:
            arithmetic_command(line)
        
    output.write(end)
            
def arithmetic_command(line):
    global ari_count
    command = line[0]
    output.write(ari_table[command])
    if command == 'eq':
        output.write(ari_table['eq_trans'].format(ari_count))
    elif command == 'gt':
        output.write(ari_table['gt_trans'].format(ari_count))
    elif command == 'lt':
        output.write(ari_table['lt_trans'].format(ari_count))
    ari_count += 1
    output.write(move_a_step)

def memory_segment(line, static_prefix):
    command, segment, pos = line[0], line[1], line[2]
    if command == 'push':
        if segment == 'pointer':
            if pos == '0':
                output.write(push_table['pointer_0'])
            else:
                output.write(push_table['pointer_1'])
        elif segment == 'static':
            output.write(push_table['static'].format(static_prefix, pos))
        else:
            output.write(push_table[segment].format(pos))
    elif command == 'pop':
        if segment == 'pointer':
            if pos == '0':
                output.write(pop_table['pointer_0'])
            else:
                output.write(pop_table['pointer_1'])
        elif segment == 'static':
            output.write(pop_table['static'].format(static_prefix, pos))
        else:
            output.write(pop_table[segment].format(pos))
            
def branching(line, name):
    command, label = line[0], line[1]
    output.write(brh_table[command].format(name, label))
    
def function_handling(line):
    global name
    name, num = line[1], line[2]
    output.write('({0})\n'.format(name))
    output.write('@0\nD=A\n@SP\n'+ int(num) * 'A=M\nM=D\n@SP\nM=M+1\n')
    
def return_handling(line):
    output.write(return_trans)
    
def call_handling(line):
    global addr_count
    name, nArg = line[1], line[2]
    output.write(call_trans.format(addr_count, nArg, name))
    addr_count += 1

file = 'StaticsTest'            
output = open('{}.asm'.format(file), 'w')
Sys_data, Sys_static_prefix = read_data('./Sys.vm')[0], read_data('./Sys.vm')[1]
Class1_data, Class1_static_prefix = read_data('./Class1.vm')[0], read_data('./Class1.vm')[1]
Class2_data, Class2_static_prefix = read_data('./Class2.vm')[0], read_data('./Class2.vm')[1]

output.write(Bootstrap)
call_handling('call Sys.init 0'.split())
choose_implementation(Sys_data, Sys_static_prefix)
choose_implementation(Class1_data, Class1_static_prefix)
choose_implementation(Class2_data, Class2_static_prefix)

