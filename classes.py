class Node(object):
	"""Base class for every Tree-typed class"""
	

	def __init__(self, ar, succtup = None):
		if ar != 0:
			self.succ = succtup
			self.ar = ar
		else :
			self.succ = Node.classVar
			self.ar = None
		self.name = self.__class__.__name__

	def treatment(self):
		#is to be called for reccursive analysis (see valids() function)
		pass

class Atom(Node):
	"""Derivative subclass for Leaf Nodes (Tree-typed)"""
	def __init__(self):
		super(Atom, self).__init__(0)

	def treatment(self, world):
		return self.value


#Logic ops subclasses (Nodes)
class And(Node):

	def __init__(self, arg, arg2):
		super(And, self).__init__(2,[arg, arg2])

	def treatment(self, world):
		return self.succ[0].treatment(world) and self.succ[1].treatment(world)

	def __repr__(self):
		return '('+self.succ[0].__repr__()+" ^ "+self.succ[1].__repr__()+')'
	

class Or(Node):

	def __init__(self, arg, arg2):
		super(Or, self).__init__(2,[arg, arg2])

	def treatment(self, world):
		return self.succ[0].treatment(world) or self.succ[1].treatment(world)


	def __repr__(self):
		return '('+self.succ[0].__repr__()+" v "+self.succ[1].__repr__()+')'
		

class Imp(Node):

	def __init__(self, arg, arg2):
		super(Imp, self).__init__(2,[arg, arg2])
		
	def treatment(self,world):

		for wrld in [world] + world.sons:
			if self.succ[0].treatment(world) and not self.succ[1].treatment(world) :
				return False
		return True

	def __repr__(self):
		return '('+self.succ[0].__repr__()+" => "+self.succ[1].__repr__()+')'
	
		
class Not(Node):

	def __init__(self, arg):
		super(Not, self).__init__(1,[arg])

	def treatment(self, world):

		for wrld in [world]+world.sons:
			if self.succ[0].treatment(wrld) :
				return False
		return True

	def __repr__(self):
		return '!('+self.succ[0].__repr__()+')'

#Logic ops subclasses (Leafs)
class Variable(Atom):
	"""Atom subclass for custom Logic variables behaviours"""

	varc_counter=0

	def __init__(self, name, value = False):
		self.name = name
		self._value = value
		self.vari_counter=Variable.varc_counter
		Variable.varc_counter+=1


	@property #Placeholder for custom Logic value (polymorphism)
	def value(self):
		return self._value

	@value.setter
	def value(self, val):
		self._value = val

	@value.deleter
	def value(self):
		self._value = False

	def treatment(self, world):
		#end of reccursive analysis (True if Variable is in World)
		return self in world.vars or self.name.lower() in [x.name.lower() for x in world.vars]

	def __repr__(self): 
		return self.name.upper()

class Top(Atom):
	def __init__(self):
		super(Top, self).__init__()
		self.value = True
	def __repr__(self):
		return "TOP"
		
class Bot(Atom):
	def __init__(self):
		super(Bot, self).__init__()
		self.value = False
	def __repr__(self):
		return "BOT"

### Model
		
class World(Node):
	"""Tree-typed subclass for reccursive model representation"""
	def __init__(self, name = None, existingVars = []):
		
		super(World, self).__init__(0)
		del self.succ

		self.name = name
		self._sons = []
		if type(existingVars) == Variable:
			self._vars = [existingVars]
		elif type(existingVars) != list:
			self._vars = list(existingVars)
		else :
			self._vars = existingVars

	@property #placeholder for reccursive support
	def sons(self):
		return self._sons

	@sons.setter
	def sons(self, newSon):
		if type(newSon) == str :
			self._sons.append(World(newSon,self.vars))
		elif type(newSon) == World :
			newSon.vars = self.vars
			self._sons.append(newSon)
		else :
			self._sons.append(World(str(newSon),self.vars))

	@sons.deleter
	def sons(self):
		self._sons = []
	
	@property #placeholder for logic variables
	def vars(self):
		return self._vars

	@vars.setter
	def vars(self, var):
		try:
			for x in var :
				if not ((x in self.vars) or (x.name in [n.name for n in self.vars])) :
					self._vars.append(x)
		except TypeError: #TypeError triggers if var is not iterable (type(var)!= list/tuple/dict...)
			if not ((var in self.vars) or (var.name in [n.name for n in self.vars])) :
				self._vars.append(var)
		finally :
			for son in self._sons:
				son.vars = var

	def __repr__(self):
		if self.sons == [] :
			return "---"+self.name+"-{"+str(self.vars)+'}\n'
		res = ">>"+self.name+str(self.vars)+") - "
		for i in range(len(self.sons)):
			res+= '\n'+str(i+1)+')'+str(self.sons[i])
		return res


def valids(formula, rootWorld):
	#IN : formula (valid tree-typed Logic compound.s, defined above); rootWorld (first placeholder for reccursive analysis, model)
	#OUT : Boolean;  True if the given Kripke model validates the formula.
	for son in rootWorld.sons :
		if not valids(formula, son):
			return False
	return formula.treatment(rootWorld)

Node.classVar = Variable("undefined") #Reserved Logic variable for High-end helper 

