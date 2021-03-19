from classes import *
import os,pickle

"""
def buildTree(root):
	res = [root.name,[]]
	if type(root) == World :
		res.append([x.name for x in root.vars])
	res2 = []
	if type(root) != Variable :
		for x in root.sons if type(root) == World else root.succ :
			res2.append(buildTree(x))
	res[1] = res2[:]
	return res

def reconstructClasses(treeHolder):
	if len(treeHolder)<=2 :
		#formule
		#print("treating node :",treeHolder[0])
		if treeHolder[1] == []:
			return Variable(treeHolder[0])
		elif len(treeHolder[1])==1:
			return Not(reconstructClasses(treeHolder[1][0]))
		return eval(treeHolder[0])(reconstructClasses(treeHolder[1][0]),reconstructClasses(treeHolder[1][1]))
	else :
		#monde
		ret = World(treeHolder[0])
		print("creating world :",treeHolder[0],"vars :",treeHolder[2],"\n")
		
		for name in treeHolder[2] :
			ret.vars = Variable(name)
			print("adding var : "+name+" to world : "+treeHolder[0])
		for x in treeHolder[1] :
			ret.sons = reconstructClasses(x)
		
		print(ret.name,":",ret.vars)

		return ret
"""

#write and read

class Userdata(object):
	"""docstring for Userdata"""
	def __init__(self, formula = None, model = None):

		self.model = model
		self.formula = formula
		self.existingDirs = os.listdir("./assets/userdata/")

	def save(self, fileset):
		if not(self.model is None):
			with open("./assets/userdata/"+fileset+".model","wb") as file:
				pickle.dump(self.model,file)
		if not(self.formula is None):
			with open("./assets/userdata/"+fileset+".formula","wb") as file:
				pickle.dump(self.formula,file)

	def load(self, fileset, defaultDataFolder = False):
		with open("./assets/"+("data" if defaultDataFolder else "userdata")+"/"+fileset+".formula","rb") as file:
			self.formula = pickle.load(file)
		with open("./assets/"+("data" if defaultDataFolder else "userdata")+"/"+fileset+".model","rb") as file:
			self.model = pickle.load(file)
