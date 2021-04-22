from classes import *
from savefilesystem import *
from graph_view import TreeViewer,TreeWrapper
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

formula=Imp(Not(Variable("a")),Or(Variable("undefined"),Variable("b")))
select=formula

class FormuleWrapper(TreeWrapper):
	def children(self,node):
		if not type(node) in [Variable,Top,Bot] :
			return [succ for succ in node.succ]
		else:
			return None
	def label(self, node):
		if node.name != 'undefined':
			return node.name
		elif node != Node.classVar:
			return ''
		else:
			return None
	def onClick(self,node):
		global select
		select=node
		viewer.drawTree(formula)
	
	def bg(self, node):
		if node==select:
			return 'yellow2'
		return 'gray77'


	
		



def replacerec(father,selected,elem):
	if not type(father) in [Variable,Top,Bot] :
		if selected in father.succ:
			father.succ=[elem if x==selected else x for x in father.succ]
			return True
		else:
			for succ in father.succ:
				if replacerec(succ,selected,elem):
					return True
			return False

	return False
				
				

def replace(selected,elem):
	global select#temporary
	global formula#temporary
	if formula==selected:
		formula=elem#temporary
		select=elem#temorary
		print(formula)
		return True
	else:
		if replacerec(formula,selected,elem):
			select=elem#temporary
			print(formula)
			return True
		else:
			return False



def getlistvarrec(current):
	listvar=[]
	
	if type(current)==Variable:
		if current.name!='undefined':
			listvar.append(current.name)
	
	elif type(current)!=Top and type(current)!=Bot :
		for succ in current.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar

def getlistvar():
	listvar=[]
	root=formula
	
	if type(root)==Variable:
		if root.name!='undefined':
			listvar.append(root.name)
	elif type(root)!=Top and type(root)!=Bot:
		for succ in root.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar




def createVar():
	if varname.get()!='':
		if varname.get()!= 'undefined':
			name= varname.get().lower()
			#select=getSelect()
			var = Variable(name)
			if replace(select,var):
				viewer.drawTree(formula)
				selectvar.delete(0,tk.END)
				listvar2= getlistvar()
				for var in listvar2:
					selectvar.insert(tk.END,var.lower())

				return messagebox.showinfo('message',f'Var {name} created.')
			else:
				return messagebox.showinfo('ERROR:',f'Could not find selected node in formula.')
		else:
			return messagebox.showinfo('message',f'undefined is not a valid variable name')
	elif  len(selectvar.curselection())==1:
		#select=getSelect()
		var=Variable(listvar[selectvar.curselection()[0]])
		name=var.name
		if replace(select,var):
			viewer.drawTree(formula)
			selectvar.delete(0,tk.END)
			listvar2= getlistvar()
			for var in listvar2:
				selectvar.insert(tk.END,var.lower())
			return messagebox.showinfo('message',f'Var {name} assigned.')
		else:
			return messagebox.showinfo('ERROR:',f'Could not find selected node in formula.')
	elif len(selectvar.curselection()) != 0:
		return messagebox.showinfo('message',f'please select only one var')
	else:
		return messagebox.showinfo('message',f'please select item or enter value')

###############################################
#Windows init
###############################################
windows = tk.Tk()
windows.title("Logique intuitioniste")

mainFrame=tk.Frame(windows)
mainFrame.pack(fill='both',expand=True)

###############################################
	#formule viewver
###############################################
graphe=tk.Frame(mainFrame, height=500, width=800)
graphe.grid(row=1,column=1,pady=10,padx=10,sticky=(tk.NW))

fwrap=FormuleWrapper()
viewer= TreeViewer(fwrap,graphe,formula)

###############################################
	#toolbox
###############################################
boxoutils = ttk.Notebook(mainFrame,width=200, height=400)
boxoutils.grid(row=1,column=2,pady=10,padx=10,sticky=(tk.NE))

###############################################
		#outils
###############################################
fOutils=ttk.Frame(boxoutils,width=200, height=400)
fOutils.pack(fill='both',expand=True)
boxoutils.add(fOutils,text='Outils')



################################################
		#Custom Variable creation
################################################

fVariable=ttk.Frame(boxoutils,width=200, height=400)
fVariable.pack(fill='both',expand=True)
boxoutils.add(fVariable,text='variable')


varname= tk.Entry(fVariable)
varname.grid(row=1,column=1)

listvar= getlistvar()

selectvar=tk.Listbox(fVariable,selectmode=tk.MULTIPLE,yscrollcommand=True)
for var in listvar:
	selectvar.insert(tk.END,var.lower())
selectvar.grid(row=2,column=1)

setvar= ttk.Button(fVariable, text='assigner', command=createVar).grid(row=1,column=2)

 #########################

windows.mainloop()
