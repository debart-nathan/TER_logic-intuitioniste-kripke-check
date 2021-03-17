class Node(object):
	"""docstring for Node"""
	

	def __init__(self, ar, succtup = None):
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

class Atom(Node):
	"""docstring for Atom"""
	def __init__(self):
		super(Atom, self).__init__(0)

	def traitement(self, world):
		return self.value


### représentation des formules
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
	
	def traitement(self,world):

		if self.succ[0].traitement(world) and not self.succ[1].traitement(world) :
			return False
		for son in world.sons():
			if not self.traitement(son) :
				return False
		return True
		
class Not(Node):

	def __init__(self, arg):
		super(Not, self).__init__(1,(arg))

	def __repr__(self):
		return '!('+self.succ.__repr__()+')'


class Variable(Atom):
	"""docstring for Variable"""
	def __init__(self, name, value = False):
		self.name = name
		self._value = value

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, val):
		self._value = val

	@value.deleter
	def value(self):
		self._value = False

	def __repr__(self): 
		return self.name.upper()

class Top(Atom):
	"""docstring for Top"""
	def __init__(self):
		super(Top, self).__init__()
		self.value = True
		
class Bot(Atom):
	"""docstring for Top"""
	def __init__(self):
		super(Bot, self).__init__()
		self.value = False

### représentation des mondes	
		
class World(Node):
	"""docstring for World"""
	def __init__(self, name = None):
		
		super(World, self).__init__(0)
		del self.succ

		self.name = name
		self._sons = []
		self._vars = []

	@property
	def sons(self):
		return self._sons

	@sons.setter
	def sons(self, value):
		self.ar+=1
		if type(value) == str :
			self._sons.append(World(value))
		elif type(value) != World :
			self._sons.append(value)
		else :
			self._sons.append(World(str(value)))
		return

	@sons.deleter
	def sons(self):
		if self.ar < 1 :
			return
		self.ar -= 1
		self._sons.pop()
	
	@property
	def vars(self):
		return self._vars
	

def delete(model, world):
	if model == world :
		del model
	for x in model._sons :
		if x == world :
			world._sons = []
			del world 





### TESTZONE
Node.classVar = Variable("undefined")

#formumle = X => ( Y v X )

X,Y,A,B,C = Variable('x'),Variable('y'),Variable('a'),Variable('b'),Variable('c')

form1 = Imp(X,And(Y,X))

form2 = Imp(Or(And(A,B),Not(A)),And(Imp(C,A),Not(C)))

print(form1,"\n",form2, "\n")