#!/usr/bin/python 
import ast
import os
import glob
import csv
# ------------------------------------------------------------------------------------------------- #
# Auxiliary classes

# Auxiliary class to get the name of a node
class FunctionName():
    
    def get_call_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        else:
            print node

class UserDef(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_ClassDef(self, node):
        x = node.bases
        for i in range(len(x)):
            call_name = FunctionName().get_call_name(x[i])
            if call_name == 'Exception':
                self.count += 1
        super(UserDef, self).generic_visit(node)
        return self.count
        
# Auxiliary class to visit the body of the method and get its data.
class BodyVisitor(ast.NodeVisitor):

    def __init__(self):
        self.wraise = False
        self.wexcept = False

    def visit_Body(self, node):
        super(BodyVisitor, self).generic_visit(node)

    def visit_Raise(self, node):
        self.wraise = True
        super(BodyVisitor, self).generic_visit(node)

    def visit_TryFinally(self, node):
        self.wexcept += True
        super(BodyVisitor, self).generic_visit(node)

    def visit_TryExcept(self, node):
        self.wexcept += True
        super(BodyVisitor, self).generic_visit(node)

# ------------------------------------------------------------------------------------------------- #
#Exception Handling
class ExceptionHandling(ast.NodeVisitor):

    def __init__(self):
        self.method = 0
        self.mwraise = 0
        self.mworaise = 0 
        self.mwexception = 0
        self.mwoexception = 0

    def visit_FunctionDef(self, node):
        self.method += 1
        teste = BodyVisitor()
        super(BodyVisitor, teste).generic_visit(node)
        if (teste.wraise == True):
            self.mwraise += 1
        else:
            self.mworaise +=1
        if (teste.wexcept == True):
            self.mwexception += 1
        else:
            self.mwoexception += 1

class ExceptionAll(ast.NodeVisitor):
    def __init__(self):
        self.raiseEx = 0
        self.exception = 0

    def visit_FunctionDef(self, node):
        super(ExceptionAll, self).generic_visit(node)

    def visit_Raise(self, node):
        self.raiseEx += 1
        super(ExceptionAll, self).generic_visit(node)

    def visit_TryFinally(self, node):
        self.exception += 1
        super(ExceptionAll, self).generic_visit(node)

    def visit_TryExcept(self, node):
        self.exception += 1
        super(ExceptionAll, self).generic_visit(node)


# Main
def operation():
    return 

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

    METHODS = 0
    WITH_EXCEPT = 0
    WITHOUT_EXCEPT = 0
    WITHRAISE = 0
    WITHOUT_RAISE = 0
    ALL_RAISES = 0
    ALL_CATCHES = 0
    USER_EXCEPTION = 0

    if len(sys.argv) == 2 :
        PROJECT = sys.argv[1]
        print("\nProcessing project: " + PROJECT)
        print "..."
        metric_list = [['PROJECT', PROJECT]]
        for f in input_path:
            for l in f:
                #print("\nProcessing file: " + l)
                with open(l, "r") as input:
                    file_str  = input.read()
                    root = ast.parse(file_str)
                    visitor = ExceptionHandling()
                    visitor.visit(root)
                    visitor_all = ExceptionAll()
                    visitor_all.visit(root)
                    visitor_def = UserDef()
                    visitor_def.visit(root)
                    
                    METHODS += visitor.method
                    WITH_EXCEPT += visitor.mwexception
                    WITHOUT_EXCEPT += visitor.mwoexception
                    WITHRAISE += visitor.mwraise
                    WITHOUT_RAISE += visitor.mworaise
                    ALL_RAISES += visitor_all.raiseEx
                    ALL_CATCHES += visitor_all.exception     
                    USER_EXCEPTION += visitor_def.count     

        metric_list.append(['METHODS', METHODS])
        metric_list.append(['WITH_EXCEPT', WITH_EXCEPT])                    
        metric_list.append(['WITHOUT_EXCEPT', WITHOUT_EXCEPT])                    
        metric_list.append(['WITHRAISE', WITHRAISE])                    
        metric_list.append(['WITHOUT_RAISE', WITHOUT_RAISE])
        metric_list.append(['ALL_RAISES', ALL_RAISES])
        metric_list.append(['ALL_CATCHES', ALL_CATCHES])                    
        metric_list.append(['USER_EXCEPTION', USER_EXCEPTION])

        with open('metrics.csv', 'wt') as file:
            writer = csv.writer(file)
            writer.writerows(metric_list)

        with open('metrics.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print ', '.join(row)

    else: 
        for file in input_path:
            with open(file, "r") as input:
                print("\nProcessing: " + file)
                file_str  = input.read()
                root = ast.parse(file_str)
                visitor = ExceptionHandling()
                visitor.visit(root)
