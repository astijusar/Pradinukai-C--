# type: ignore
from ast import parse
from asyncio.windows_events import NULL
import queue
import string
import sys
from unittest import result
from xmlrpc.client import boolean
from lexer import Lex
from parser import Parser
from collections import deque

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
                elif self.result == "endif":
                    return None
                else:
                    if (self.result not in self.env):
                        return self.result
            else:
                return self.result

    def walkTree(self, node, parent):
        if isinstance(node, int):
            return node

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
            elif node[0] == 'var':
                try:
                    return self.env[node[1]]
                except LookupError:
                    print("Undefined variable '" + node[1] + "' found!")
                    return 0


def cmm(data):
    trees = []
    skip = False
    ifStack = deque()
    endIfCnt = 0
    for line in data:
        tokens = lexer.tokenize(line)
        tree = parser.parse(tokens)
        trees.append(tree)
    
    for tree in trees:
        if tree is not None:
            if tree[0] == "ifstmt":
                if skip == False:
                    res = Execute(tree, env).getResult()
                    if res == False:
                        ifStack.append("if")
                        skip = True

            if skip == True:
                if tree == "endif":
                    endIfCnt += 1
                    if len(ifStack) == endIfCnt:
                        skip = False
                        endIfCnt -= 1
                    ifStack.pop()
                else:
                    continue

            result = Execute(tree, env).getResult()
            if result is None:
                continue
            elif result == '':
                print()
            elif isinstance(result, bool):
                continue
            else:
                print(result)

if __name__ == '__main__':
    lexer = Lex()
    parser = Parser()
    print('C-- language')
    env = {}
    stack = deque()

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

    cmm(data)