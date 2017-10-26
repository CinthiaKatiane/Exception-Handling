#!/usr/bin/python 
import ast
import os
import glob

# ------------------------------------------------------------------------------------------------- #
# Classes auxiliares

# Aux Function to get the name of a node
class FunctionName():
    
    def get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif (isinstance(node.func, ast.Call)):
            self.get_call_name(node)
        else:
            print node

class BodyVisitor_LCOM(ast.NodeVisitor):

    def __init__(self):
        self.bla = []

    def visit_Body(self, node):
        super(BodyVisitor_LCOM, self).generic_visit(node)

    def visit_Attribute(self,node):
        if (isinstance(node.ctx, ast.Store)):
            self.bla.append(node.attr)
        super(BodyVisitor_LCOM, self).generic_visit(node)


# ------------------------------------------------------------------------------------------------- #
#Exception Handling
class ExceptionHandling(ast.NodeVisitor):

    def __init__(self):
        self.metric = 0

    def visit_FunctionDef(self, node):
        print("\tFunction '{0}' was defined.".format(node.name))
        super(ExceptionHandling, self).generic_visit(node)
    
    def visit_Raise(self, node):
        print "\t\tRaise Exception"
        super(ExceptionHandling, self).generic_visit(node)

    def visit_TryFinally(self, node):
        print "\t\tTry Finally ----------------------------------------------------------"
        super(ExceptionHandling, self).generic_visit(node)

    def visit_TryExcept(self, node):
        print "\t\tTry Except ----------------------------------------------------------"
        super(ExceptionHandling, self).generic_visit(node)

# ------------------------------------------------------------------------------------------------- #
#Classes iniciais
'''
class FunctionDefVisitor(ast.NodeVisitor):
    def __init__(self):
        self.dictfun = {}

    def visit_FunctionDef(self, node):
        print("\tFunction '{0}' was defined.".format(node.name))
        super(FunctionDefVisitor, self).generic_visit(node)
        #print self.dictfun
        self.dictfun = {}

    def visit_Call(self,node):
        call_name = FunctionName().get_call_name(node)
        print(str("\t\t'{0}' was called.").format(call_name))
        self.dictfun[call_name] = self.dictfun.get(call_name , 0) + 1
        super(FunctionDefVisitor, self).generic_visit(node)


class MyCustomVisitor(ast.NodeVisitor):
    
    def __init__(self):
        self.counterTotal = 0 #Keeps the number of function calls
        self.counterDefinition = 0 #Keeps the number of defined functions in the file
        self.counterFunction = 0 #Keeps the number of function calls inside a defined function 
        self.dictdef = {}
        self.dictfun = {}

    # Aux function
    def get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        else:
            raise NotImplementedError("Could not extract call-name from node: " + str(node))

    def visit_Call(self, node):
        self.counterTotal = self.counterTotal + 1
        self.counterFunction = self.counterFunction + 1
        call_name = self.get_call_name(node)
        print(str("\t\t'{0}' was called.").format(call_name))
        self.dictfun[call_name] = self.dictfun.get(call_name , 0) + 1
        super(MyCustomVisitor, self).generic_visit(node)

    def visit_ClassDef(self, node):
        print("Class '{0}' was defined.".format(node.name))
        super(MyCustomVisitor, self).generic_visit(node)
    
    def visit_FunctionDef(self, node):
        self.dictdef[node.name] = self.dictfun
        self.counterFunction = 0 #Restart the counter to get de quantity in a specfic defined function
        self.counterDefinition = self.counterDefinition + 1
        print("\tFunction '{0}' was defined.".format(node.name))
        super(MyCustomVisitor, self).generic_visit(node)
        print("\tA total of {0} function calls were found in {1}.\n".format(visitor.counterFunction, node.name))
        print self.dictdef[node.name]     
'''
# ------------------------------------------------------------------------------------------------- #

# Main

if __name__ == "__main__":

    import sys
    input_path = []
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
        for root, dirs, files in os.walk("./"):
            file = glob.glob(root + '/*.py')
            if (len(file)is not 0) :
                input_path.append(file)
            else:
                pass
    else :
        input_path = glob.glob('./*.py')

    if len(sys.argv) == 2 :
        for f in input_path:
            for l in f:
                print("\nProcessing file: " + l)
                with open(l, "r") as input:
                    file_str  = input.read()
                    root = ast.parse(file_str)
                    visitor = ExceptionHandling()
                    visitor.visit(root)
    else: 
        for file in input_path:
            with open(file, "r") as input:
                print("\nProcessing: " + file)
                file_str  = input.read()
                root = ast.parse(file_str)
                visitor = ExceptionHandling()
                visitor.visit(root)