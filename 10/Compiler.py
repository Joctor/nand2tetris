# -*- coding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
import re

keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
            'this', 'let', 'do', 'if', 'else', 'while', 'return'}

token_specification = [
    ('integerConstant', r'\d+(\.\d*)?'),           # Integer or decimal number
    ('identifier', r'\w+'),                        # Identifiers
    ('symbol', r'[\{\}\(\)\[\].,;+\-\*/&|<>=~]'),  # Arithmetic operators
    ('stringConstant', r'\"([^\"]*)\"'),
    ('SKIP', r'[ \t]+'),                        # Skip over spaces and tabs
    ('MISMATCH', r'.'),                         # Any other character
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

op = {'+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

class JackAnalyzer:
    def __init__(self, code):
        self.code = code
        self.root = ET.Element('class')
        self.tree = ET.ElementTree(self.root)
        self.state_lst = []
        self.exp_lst = []
        
    def JackTokenizer(self):
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'integerConstant':
                value = float(value) if '.' in value else int(value)
            elif kind == 'identifier' and value in keywords:
                kind = 'keyword'
            elif kind == 'SKIP':
                continue
            elif kind == 'stringConstant':
                value = value[1:len(value)-1]
            elif kind == 'MISMATCH':
                raise RuntimeError
            yield (kind, value)
    
    def Advance(self):
        self.token = self.JackTokenizer()                
       
    def CompileClass(self):
        (kind, value) = next(self.token)
        #         ↓
        #'{' classVarDec* subroutineDec* '}'
        if value == 'static' or value == 'field':
            self.classVarDec = ET.SubElement(self.root, 'classVarDec')
            node = ET.SubElement(self.classVarDec, kind)
            node.text = str(value)
            self.CompileclassVarDec()
        #                       ↓
        #'{' classVarDec* subroutineDec* '}'
        elif value == 'constructor' or value == 'function' or value == 'method':
            self.subroutineDec = ET.SubElement(self.root, 'subroutineDec')
            node = ET.SubElement(self.subroutineDec, kind)
            node.text = str(value)
            self.CompilesubroutineDec()
        else:
            node = ET.SubElement(self.root, kind)
            node.text = str(value)
            #                                 ↓
            #'{' classVarDec* subroutineDec* '}'
            self.CompileClass()            
        
    def CompileclassVarDec(self):
        (kind, value) = next(self.token)
        #               ↓
        #'{' classVarDec* subroutineDec* '}'
        if value == 'constructor' or value == 'function' or value == 'method':
            self.subroutineDec = ET.SubElement(self.root, 'subroutineDec')
            node = ET.SubElement(self.subroutineDec, kind)
            node.text = str(value)
            self.CompilesubroutineDec()
        else:
            node = ET.SubElement(self.classVarDec, kind)
            node.text = str(value)
            #                               ↓
            #classVarDec: ~ (',' varName)* ';'
            if value == ';':
                self.CompileClass()
            else:
                self.CompileclassVarDec()
    
    def CompilesubroutineDec(self):
        (kind, value) = next(self.token)
        #                              ↓
        #'{' classVarDec* subroutineDec* '}'
        if value == 'constructor' or value == 'function' or value == 'method':
            self.subroutineDec = ET.SubElement(self.root, 'subroutineDec')
            node = ET.SubElement(self.subroutineDec, kind)
            node.text = str(value)
            self.CompilesubroutineDec()
        #                 ↓
        #subroutineBody: '{' varDec* statements '}'
        elif value == '{':
            self.subroutineBody = ET.SubElement(self.subroutineDec, 'subroutineBody')
            node = ET.SubElement(self.subroutineBody, kind)
            node.text = str(value)
            self.CompilesubroutineBody()
        elif value == '}':
            node = ET.SubElement(self.root, kind)
            node.text = str(value)
        else:
            node = ET.SubElement(self.subroutineDec, kind)
            node.text = str(value)
            # ↓
            #'(' parameterList ')'
            if value == '(':
                self.parameterList = ET.SubElement(self.subroutineDec, 'parameterList')
                self.CompileparameterList()
            else:
                self.CompilesubroutineDec()
                
    def CompileparameterList(self):
        (kind, value) = next(self.token)
        #                   ↓
        #'(' parameterList ')'
        if value == ')':
            node = ET.SubElement(self.subroutineDec, kind)
            node.text = str(value)
            self.CompilesubroutineDec()   
        #          ↓
        #'(' parameterList ')'
        else:
            node = ET.SubElement(self.parameterList, kind)
            node.text = str(value)
            self.CompileparameterList()
            
    def CompilesubroutineBody(self):
        (kind, value) = next(self.token)
        #                      ↓
        #subroutineBody:'{' varDec* statements '}'
        if value == 'var':
            self.varDec = ET.SubElement(self.subroutineBody, 'varDec')
            node = ET.SubElement(self.varDec, kind)
            node.text = str(value)
            self.CompilevarDec()
        #                                ↓
        #subroutineBody:'{' varDec* statements '}'
        elif value == 'let' or value == 'if' or value == 'while' or \
            value == 'do' or value == 'return':
            self.statements = ET.SubElement(self.subroutineBody, 'statements')
            self.state_lst.append(('body', self.statements))
            self.Compilestatements(kind, value)
        else:
            node = ET.SubElement(self.subroutineBody, kind)
            node.text = str(value)
            self.CompilesubroutineBody()
        
    def CompilevarDec(self):
        (kind, value) = next(self.token)
        #                                ↓
        #subroutineBody:'{' varDec* statements '}'
        if value == 'let' or value == 'if' or value == 'while' or \
            value == 'do' or value == 'return':
            self.statements = ET.SubElement(self.subroutineBody, 'statements')
            self.state_lst.append(('body', self.statements))
            self.Compilestatements(kind, value)
        #                         ↓
        #subroutineBody:'{' varDec* statements '}'
        elif value == 'var':
            self.varDec = ET.SubElement(self.subroutineBody, 'varDec')
            node = ET.SubElement(self.varDec, kind)
            node.text = str(value)
            self.CompilevarDec()
        else:
            node = ET.SubElement(self.varDec, kind)
            node.text = str(value)
            self.CompilevarDec()            
            
    def Compilestatements(self, kind, value):
        if value == 'let' or value == 'if' or value == 'while' or \
            value == 'do' or value == 'return':
            self.exp_lst.append(value)
        if value == 'let':
            self.letStatement = ET.SubElement(self.statements, 'letStatement')
            node = ET.SubElement(self.letStatement, kind)
            node.text = str(value)
            self.CompileLet()
        elif value == 'if':
            self.ifStatement = ET.SubElement(self.statements, 'ifStatement')
            node = ET.SubElement(self.ifStatement, kind)
            node.text = str(value)
            self.CompileIf()
        elif value == 'else':
            node = ET.SubElement(self.ifStatement, kind)
            node.text = str(value)
            self.CompileIf()
        elif value == 'while':
            self.whileStatement = ET.SubElement(self.statements, 'whileStatement')
            node = ET.SubElement(self.whileStatement, kind)
            node.text = str(value)
            self.CompileWhile()
        elif value == 'do':
            self.doStatement = ET.SubElement(self.statements, 'doStatement')
            node = ET.SubElement(self.doStatement, kind)
            node.text = str(value)
            self.CompileDo()
        elif value == 'return':
            self.returnStatement = ET.SubElement(self.statements, 'returnStatement')
            node = ET.SubElement(self.returnStatement, kind)
            node.text = str(value)
            self.CompileReturn()
        elif value == '}':
            (one_from_three, self.statements) = self.state_lst.pop(-1)
            if one_from_three == 'body':
                node = ET.SubElement(self.subroutineBody, kind)
                node.text = str(value)
                self.CompilesubroutineDec()
            elif one_from_three == 'if':
                node = ET.SubElement(self.ifStatement, kind)
                node.text = str(value)
                (kind, value) = next(self.token)
                self.Compilestatements(kind, value) 
            elif one_from_three == 'while':
                node = ET.SubElement(self.whileStatement, kind)
                node.text = str(value)
                (kind, value) = next(self.token)
                self.Compilestatements(kind, value)            
        else:
            raise RuntimeError        
            
    def CompileLet(self):
        (kind, value) = next(self.token)
        node = ET.SubElement(self.letStatement, kind)
        node.text = str(value)
        #                               ↓
        #classVarDec: ~ (',' varName)* ';'
        if value == '=' or value == '[':
            self.expression = ET.SubElement(self.letStatement, 'expression')
            self.CompileExpression()
        else:
            self.CompileLet()
        '''
        elif value == ';':
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        '''
    
    def CompileIf(self):
        (kind, value) = next(self.token)
        node = ET.SubElement(self.ifStatement, kind)
        node.text = str(value)
        if value == '(':
            self.expression = ET.SubElement(self.ifStatement, 'expression')
            self.CompileExpression()
        elif value == '{':
            self.state_lst.append(('if', self.statements))
            self.statements = ET.SubElement(self.ifStatement, 'statements')
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        else:
            self.CompileIf()

    
    def CompileWhile(self):
        (kind, value) = next(self.token)
        node = ET.SubElement(self.whileStatement, kind)
        node.text = str(value)
        if value == '(':
            self.expression = ET.SubElement(self.whileStatement, 'expression')
            self.CompileExpression()
        elif value == '{':
            self.state_lst.append(('while', self.statements))
            self.statements = ET.SubElement(self.whileStatement, 'statements')
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        else:
            self.CompileWhile()

    
    def CompileDo(self):
        (kind, value) = next(self.token)
        node = ET.SubElement(self.doStatement, kind)
        node.text = str(value)
        if value == '(':
            self.expressionList = ET.SubElement(self.doStatement, 'expressionList')
            self.CompileExpressionList()
        else:
            self.CompileDo()
    
    def CompileReturn(self):
        (kind, value) = next(self.token)
        if value == ';':
            self.exp_lst.pop(-1)
            node = ET.SubElement(self.returnStatement, kind)
            node.text = str(value)
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        else:
            self.expression = ET.SubElement(self.returnStatement, 'expression')
            self.term = ET.SubElement(self.expression, 'term')
            node = ET.SubElement(self.term, kind)
            node.text = str(value)
            self.CompileExpression()
    
    def CompileExpression(self):
        (kind, value) = next(self.token)
        if kind != 'symbol':
            self.term = ET.SubElement(self.expression, 'term')
            node = ET.SubElement(self.term, kind)
            node.text = str(value)
            self.CompileExpression()
        elif value in op:
            node = ET.SubElement(self.expression, kind)
            node.text = str(value)
            self.CompileExpression()
        elif value == ';':
            choice = self.exp_lst.pop(-1)
            if choice == 'let':
                node = ET.SubElement(self.letStatement, kind)
            elif choice == 'do':
                node = ET.SubElement(self.doStatement, kind)
            elif choice == 'return':
                node = ET.SubElement(self.returnStatement, kind)
            node.text = str(value)
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
                
        
        '''
        elif value == ']' or value == ')':
            choice = self.exp_lst[-1]
            if choice == 'let':
                node = ET.SubElement(self.letStatement, kind)
                node.text = str(value)
        '''    
            
        '''
        elif value == ';':
            if self.key_return:
                node = ET.SubElement(self.returnStatement, kind)
                self.key_return = 0
            else:
                node = ET.SubElement(self.letStatement, kind)
            node.text = str(value)
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        elif value == ')':
            if self.key_do:
                self.key_do = 0
                node = ET.SubElement(self.doStatement, kind)
                node.text = str(value)
                self.CompileDo()
            
            else:
                node = ET.SubElement(self.ifStatement, kind)
                node.text = str(value)
                self.CompileIf()
        elif value == ']':
            node = ET.SubElement(self.letStatement, kind)
            node.text = str(value)
            self.CompileLet()
        '''
        
    def CompileExpressionList(self):
        (kind, value) = next(self.token)
        if kind != 'symbol':
            self.expression = ET.SubElement(self.expressionList, 'expression')
            self.term = ET.SubElement(self.expression, 'term')
            node = ET.SubElement(self.term, kind)
            node.text = str(value)
            self.CompileExpression()
        elif value == '(' or value == ')':
            choice = self.exp_lst[-1]
            if choice == 'let':
                node = ET.SubElement(self.letStatement, kind)
            elif choice == 'do':
                node = ET.SubElement(self.doStatement, kind)
            elif choice == 'return':
                node = ET.SubElement(self.returnStatement, kind)
            node.text = str(value)
            self.CompileExpressionList()
        elif value == ';':
            choice = self.exp_lst.pop(-1)
            if choice == 'let':
                node = ET.SubElement(self.letStatement, kind)
            elif choice == 'do':
                node = ET.SubElement(self.doStatement, kind)
            elif choice == 'return':
                node = ET.SubElement(self.returnStatement, kind)
            node.text = str(value)
            (kind, value) = next(self.token)
            self.Compilestatements(kind, value)
        '''
        if value == ')':
            node = ET.SubElement(self.doStatement, kind)
            node.text = str(value)
            self.CompileDo()
        elif kind == 'identifier':
            self.key_do = 1
            self.expression = ET.SubElement(self.expressionList, 'expression')
            self.term = ET.SubElement(self.expression, 'term')
            node = ET.SubElement(self.term, kind)
            node.text = str(value)
            self.CompileExpression()
        else:
            node = ET.SubElement(self.expressionList, kind)
            node.text = str(value)
            self.CompileExpressionList()
        '''


def IO_Source(source):
    if os.path.isfile(source):
        file_prefix = os.path.split(source)[0]
        file_name = os.path.split(source)[1]
        file_name = file_name[:len(file_name)-len('.jack')]
        output_name = file_prefix + '\my{0}.xml'.format(file_name)
        code = ''
        with open(source) as f:
            data = f.readlines()
        for line in data:
            line = line.strip()
            first = line.split(' ')[0]
            if first == '' or first == '//' or first == '/*' or first == '/**' or first == '*':
                continue
            line = line.split('//')[0].strip()
            code = code + line
        data = JackAnalyzer(code)
        data.Advance()
        try:
            data.CompileClass()
        except StopIteration:
            pass
        data.tree.write(output_name, encoding="utf-8")     
                 
    elif os.path.isdir(source):
        dir_list = os.listdir(source)
        for file in dir_list:
            if file[len(file)-len('jack'):] == 'jack':
                file_source = source + '\\' + file     
                IO_Source(file_source)

#source = sys.argv[1]
source = '.\ExpressionLessSquare\SquareGame.jack'
IO_Source(source)