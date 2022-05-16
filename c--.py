from ast import parse
from asyncio.windows_events import NULL
import queue
import string
import sys
from unittest import result
from urllib import request
from xmlrpc.client import boolean
from lexer import Lex
from parser import Parser
from collections import deque
import re

class Execute:
    def __init__(self, tree, env):
        self.env = env
        self.result = self.walkTree(tree, None)

    def getResult(self):
        if self.result is not None:
            if isinstance(self.result, float):
                return int(self.result)
            elif isinstance(self.result, str):
                if self.result[0] == '"' and len(self.result) <= 3:
                    return ''
                elif self.result == "endif" or self.result == "endfunc" or self.result == "return":
                    return None
                else:
                    if self.result not in self.env:
                        return ("str", self.result)
                    else:
                        return ("var", self.result)
            else:
                return self.result

    def walkTree(self, node, parent):
        if isinstance(node, int):
            return node

        if node == 'return':
            return ("return", "")
        
        if node[0] == 'return':
            return ("return", node[1])

        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'num':
            return int(node[1])
  
        if node[0] == 'str':
            return node[1]

        if node[0] == 'bool':
            return node[1]

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2], node[0])
            return node[1]

        if node[0] == 'out':
            return self.walkTree(node[1], node[0])

        if node[0] == 'ifstmt':
            return self.walkTree(node[1], node[0])

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if parent == 'out' or 'add' or 'sub' or 'mul' or 'div' or 'ifstmt':
            if node[0] == 'add':
                return self.walkTree(node[1], node[0]) + self.walkTree(node[2], node[0])
            elif node[0] == 'sub':
                return self.walkTree(node[1], node[0]) - self.walkTree(node[2], node[0])
            elif node[0] == 'mul':
                return self.walkTree(node[1], node[0]) * self.walkTree(node[2], node[0])
            elif node[0] == 'div':
                return self.walkTree(node[1], node[0]) / self.walkTree(node[2], node[0])
            elif node[0] == 'less':
                return self.walkTree(node[1], node[0]) < self.walkTree(node[2], node[0])
            elif node[0] == 'greater':
                return self.walkTree(node[1], node[0]) > self.walkTree(node[2], node[0])
            elif node[0] == 'equal':
                return self.walkTree(node[1], node[0]) == self.walkTree(node[2], node[0])
            elif node[0] == 'not_equal':
                return self.walkTree(node[1], node[0]) != self.walkTree(node[2], node[0])
            elif node[0] == 'var':
                try:
                    return self.env[node[1]]
                except LookupError:
                    print("Undefined variable '" + node[1] + "' found!")
                    return 0

def funcLines(data, func):
    lines = []
    add = False
    func = "func " + func + "\("

    for line in data:
        line = line.strip('\n')

        if line == "endfunc" and add == True:
            return lines

        if add == True:
            lines.append(line.lstrip())

        if re.match(func, line):
            add = True
        
    return lines


def cmm(data, functions, callStack, rec, env):
    trees = []
    lines = []
    funcEnv = {}
    skip = False
    funcSkip = False
    ifStack = deque()
    endIfCnt = 0
    for line in data:
        tokens = lexer.tokenize(line)
        #for tok in tokens:
            #print(tok)
        tree = parser.parse(tokens)
        trees.append(tree)
        #print(tree)
    
    for tree in trees:
        if tree is not None:
            if funcSkip == True:
                if tree == "endfunc":
                    funcSkip = False
                    callStack.pop()
                    continue
                else:
                    continue

            if skip == True:
                if tree == "endif":
                    endIfCnt += 1
                    if len(ifStack) == endIfCnt:
                        skip = False
                        endIfCnt -= 1
                    ifStack.pop()
                else:
                    continue

            if tree[0] == "ifstmt":
                if skip == False:
                    res = Execute(tree, env).getResult()
                    if res == False:
                        ifStack.append("if")
                        skip = True
            elif tree[0] == "function":
                callStack.append(tree[1])
                try:
                    functions[tree[1]] = tree[2].split(',')
                except:
                    functions[tree[1]] = ""

                funcSkip = True
                continue
            elif tree[0] == "var_function_decl":
                if tree[2] in functions:
                    if tree[3] != "":
                        if isinstance(tree[3], tuple):
                            value = Execute(tree[3], env).getResult()
                            if isinstance(value, int):
                                var = functions[tree[2]]
                                funcEnv[var[0]] = value
                            else:
                                var = functions[tree[2]]
                                funcEnv[var[0]] = env[value[1]]
                        else:
                            variables = tree[3].split(',')
                            for x, var in enumerate(functions[tree[2]]):
                                if re.match("[-+]?\d+$", variables[x]):
                                    funcEnv[var] = int(variables[x])
                                else:
                                    funcEnv[var] = env[variables[x]]

                    if rec == False:
                        lines = funcLines(data, tree[2])
                        res = cmm(lines, functions, callStack, True, funcEnv)
                        env[tree[1]] = res
                    else:
                        res = cmm(data, functions, callStack, True, funcEnv)
                        return res
                else:
                    continue
            
            result = Execute(tree, env).getResult()
            if result is None:
                continue
            elif result == '':
                print()
            elif isinstance(result, bool):
                continue
            elif isinstance(result, tuple):
                if result[0] == "return":
                    if isinstance(result[1], str) and result[1] != '':
                        return env[result[1]]
                    elif isinstance(result[1], tuple):
                        return Execute(result[1], env).getResult()
                    else:
                        return result[1]

                if result[0] == "var":
                    continue
                else:
                    print(result[1])
            else:
                print(result)

if __name__ == '__main__':
    lexer = Lex()
    parser = Parser()
    print('C-- language')
    env = {}
    stack = deque()
    functions = {}
    callStack = deque()

    try:
        file = open(sys.argv[1], "r")
    except:
        print("Wrong file input!")
        exit()

    try:
        data = file.readlines()
    except:
        print("Cant read file!")
        exit()

    cmm(data, functions, callStack, False, env)