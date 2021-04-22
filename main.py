from classes import *
from savefilesystem import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

formula=Not(Top())

def getlistvarrec(current):
	listvar=[]
	
	if type(current)==Variable:
		if current!=Node.classVar:
			listvar.append(current)
	
	elif type(current)!=Top and type(current)!=Bot :
	   for succ in current.succ:
		   varsuc=getlistvarrec(succ)
		   if not (varsuc  in listvar):
			   listvar.extend(varsuc) 
	return listvar

def getlistvar():
	listvar=[]
	root=formula
	
	if type(root)==Variable:
		if root!=Node.classVar:
			listvar.append(root)
	elif type(root)!=Top and type(root)!=Bot:

	   for succ in root.succ:
		   listvar.extend(getlistvarrec(succ))
	return listvar




def createVar():
	if varname.get()!='':
		name= varname.get()
		#select=getSelect
		var = Variable(name)
		#replace(select,var)
		return messagebox.showinfo('message',f'Var {name} created.')
	elif  len(selectvar.curselection())==1:
		var=listvar[selectvar.curselection()[0]]
		name=var.name
 		#replace(select,var)
		return messagebox.showinfo('message',f'Var {name} assigned.')
	elif len(selectvar.curselection()) != 0:
		return messagebox.showinfo('message',f'please select only one var')
	else:
		return messagebox.showinfo('message',f'please select item or enter value')

fenetre = tk.Tk()
fenetre.title("Logique intuitioniste")

mainframe = ttk.Frame(fenetre, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
fenetre.columnconfigure(2, weight=1)
fenetre.rowconfigure(2, weight=1)

varname= tk.Entry(mainframe)
varname.grid(row=1,column=1)

listvar= getlistvar()

selectvar=tk.Listbox(mainframe,selectmode=tk.MULTIPLE,yscrollcommand=True)
for var in listvar:
	selectvar.insert(tk.END,var.name)
selectvar.grid(row=2,column=1)

setvar= ttk.Button(mainframe, text='assigner', command=createVar).grid(row=1,column=2)

 

fenetre.mainloop()