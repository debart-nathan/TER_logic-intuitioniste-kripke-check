class Node(object):
	"""docstring for Node"""
	

	def __init__(self, ar, succtup):
		if ar != 0:
			self.succ = succtup
			self.ar = ar
		else :
			self.succ = Node.classVar
			self.ar = None

	def traitement(self):
		pass

	def __repr__(self):
		if self.ar == 1 :
			return self.succ.__repr__()

class And(Node):

	def __init__(self, arg, arg2):
		super(And, self).__init__(2,(arg, arg2))

	def __repr__(self):
		return '('+self.succ[0].__repr__()+" ^ "+self.succ[1].__repr__()+')'
	
class Or(Node):

	def __init__(self, arg, arg2):
		super(Or, self).__init__(2,(arg, arg2))

	def __repr__(self):
		return '('+self.succ[0].__repr__()+" v "+self.succ[1].__repr__()+')'
		
class Imp(Node):

	def __init__(self, arg, arg2):
		super(Imp, self).__init__(2,(arg, arg2))
		
	def __repr__(self):
		return '('+self.succ[0].__repr__()+" => "+self.succ[1].__repr__()+')'
		
class Not(Node):

	def __init__(self, arg):
		super(Not, self).__init__(1,(arg))

	def __repr__(self):
		return '!('+self.succ.__repr__()+')'
		
class Variable(Node):
	"""docstring for Variable"""
	def __init__(self, name):
		self.name = name

	def __repr__(self): 
		return self.name.upper()
		

Node.classVar = Variable("undefined")


#formumle = X => ( Y v X )

X,Y,A,B,C = Variable('x'),Variable('y'),Variable('a'),Variable('b'),Variable('c')

form1 = Imp(X,And(Y,X))

form2 = Imp(Or(And(A,B),Not(A)),And(Imp(C,A),Not(C)))

print(form1,"\n",form2)