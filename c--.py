# type: ignore
from ast import parse
import string
import sys
from lexer import Lex
from parser import Parser

class Execute:
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree, None)
        if result is not None:
            if isinstance(result, float):
                print(int(result))
            elif isinstance(result, str):
                if result[0] == '"' and len(result) <= 3:
                    print()
                else:
                    if (result not in self.env):
                        print(result)
            else:
                print(result)

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

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if parent == 'out' or 'add' or 'sub' or 'mul' or 'div':
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

if __name__ == '__main__':
    lexer = Lex()
    parser = Parser()
    print('C-- language')
    env = {}

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

    for line in data:
        tokens = lexer.tokenize(line)
        #for tok in tokens:
            #print(tok)
        tree = parser.parse(tokens)
        #print(tree)
        Execute(tree, env)