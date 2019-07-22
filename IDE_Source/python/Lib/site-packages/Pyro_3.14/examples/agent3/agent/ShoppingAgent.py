class ShoppingAgent(object):
    def __init__(self, name):
        self.name=name
        self.visited=[]
    def result(self):
        print 'My name is',self.name
        print 'I have visited',self.visited
    def visit(self, name):
        self.visited.append(name)
    def __str__(self):
        return self.name
        

