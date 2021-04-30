import classes as cl
from savefilesystem import *
from graph_view import TreeViewer,TreeWrapper
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os



usrData=Userdata()

def showFile():
	

	text= "Fichier formule ouvert: "
	if not (usrData.currentFFile is None):
		text+=(usrData.currentFFile+".formula")
	else:
		text+="aucun" 

	text+=", FichierMonde ouvert: "
	if not (usrData.currentWFile is None):
		text+=(usrData.currentWFile+".model")
	else:
		text+="aucun"

	
	
	

def createInter():
	
	usrData.modele= cl.World("M:0,0")
	usrData.formula = cl.Variable('undefined')
	usrData.select = usrData.formula
	createFormulaFrame()

def openFormula():
	currentFile=filedialog.askopenfilename(initialdir="./assets/userdata/" ,filetypes=[("formula file","*.formula")])
	if currentFile!= ():
		currentFile=os.path.split(currentFile)
		if currentFile[0]!=(os.getcwd()+"/assets/userdata"):
			messagebox.showinfo('Erreur de Dossier',f'prenez un fichier dans ./asset/userdata')
		else:
			currentFile=currentFile[1].rsplit( ".", 1 )[ 0 ]
			usrData.load(ffileset=currentFile)
			usrData.currentFFile=currentFile	
	
			usrData.select=usrData.formula

			if usrData.model==None:
				usrData.model=cl.World("M:0,0")
			createFormulaFrame()

def openWorld():
	currentFile= filedialog.askopenfilename(initialdir="./assets/userdata/" ,filetypes=[("model file","*.model")])
	if currentFile!= ():
		currentFile=os.path.split(currentFile)
		if currentFile[0]!=(os.getcwd()+"/assets/userdata"):
			messagebox.showinfo('Erreur de Dossier',f'prenez un fichier dans ./asset/userdata')
		else:
			currentFile=currentFile[1].rsplit( ".", 1 )[ 0 ]
			usrData.load(wfileset=currentFile)

			usrData.currentWFile=currentFile

			if usrData.formula==None:
				usrData.formula=cl.Variable("undefined")

			if bienConstruite():
				usrData.select=usrData.model
				createModelFrame()
			else:
				usrData.select=usrData.formula
				createFormulaFrame()
	

def openInter():
	currentFile= filedialog.askopenfilename(initialdir="./assets/userdata/" ,filetypes=[("formula file","*.formula")])
	currentFile2= filedialog.askopenfilename(initialdir="./assets/userdata/" ,filetypes=[("model file","*.model")])
	if currentFile!= () or currentFile2!= ():
		currentFile=os.path.split(currentFile)
		currentFile2=os.path.split(currentFile2)
		if (currentFile[0] or currentFile2[0])!=(os.getcwd()+"/assets/userdata"):
			messagebox.showinfo('Erreur de Dossier',f'prenez les fichier dans ./asset/userdata')
		else:
			currentFile=currentFile[1].rsplit( ".", 1 )[ 0 ]
			currentFile2=currentFile2[1].rsplit( ".", 1 )[ 0 ]

			usrData.load(ffileset=currentFile)
			usrData.currentFFile=currentFile

			usrData.load(wfileset=currentFile2)
			usrData.currentWFile=currentFile2

			usrData.select=usrData.formula
			createFormulaFrame()



def	saveCInter():
	if usrData.currentFFile ==None or usrData.currentWFile ==None:
		messagebox.showinfo('Alert',f'Au moins un des fichers (formule/model) n\'est pas ouvert')
	else:
		usrData.save(ffileset=usrData.currentFFile,wfilset=usrData.currentWFile)

def saveNInter():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisiser un nom")
	currentFile=""

	def close():
		popup.grab_release()
		popup.destroy()
		popup.update()
	def save():
		currentFile=entry.get()
		if currentFile !="":
			usrData.save(ffileset=currentFile,wfileset=currentFile)
			usrData.currentFFile=currentFile
			usrData.currentWFile=currentFile
			close()
		else:
			t=Label(popup,text ="le nom ne peut pas être vide",fg="red")
			t.grid(column=0,row=1)
	
	b1=Button(popup,text="save",command= save)
	b2=Button(popup,text="cancel",command=close)
	entry= ttk.Entry(popup, textvariable = currentFile)
	
	entry.grid(column=0, row = 0, sticky = (N, S, E, W))
	b1.grid(column=0, row = 2, sticky = (N, S, E, W))
	b2.grid(column=1, row = 2, sticky = (N, S, E, W))
	
	


def	saveCFormula():
	if usrData.currentFFile ==None :
		messagebox.showinfo('Alert',f'Aucune fichier formule ouvert')
	else:
		usrData.save(ffileset=usrData.currentFFile)

def saveNFromula():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisiser un nom")
	currentFile=""

	def close():
		popup.grab_release()
		popup.destroy()
		popup.update()
	def save():
		currentFile=entry.get()
		if currentFile !="":
			usrData.save(ffileset=currentFile)
			usrData.currentFFile=currentFile
			close()
		else:
			t=Label(popup,text ="le nom ne peut pas être vide",fg="red")
			t.grid(column=0,row=1)
	
	b1=Button(popup,text="save",command= save)
	b2=Button(popup,text="cancel",command=close)
	entry= ttk.Entry(popup, textvariable = currentFile)
	
	entry.grid(column=0, row = 0, sticky = (N, S, E, W))
	b1.grid(column=0, row = 2, sticky = (N, S, E, W))
	b2.grid(column=1, row = 2, sticky = (N, S, E, W))


def	saveCWorld():
	if  usrData.currentWFile ==None:
		messagebox.showinfo('Alert',f'Aucun fichier model ouvert')
	else:
		usrData.save(wfilset=usrData.currentWFile)

def saveNWorld():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisiser un nom")
	currentFile=""

	def close():
		popup.grab_release()
		popup.destroy()
		popup.update()
	def save():
		currentFile=entry.get()
		if currentFile !="":
			usrData.save(wfileset=currentFile)
			usrData.currentWFile=currentFile
			close
		else:
			t=Label(popup,text ="le nom ne peut pas être vide",fg="red")
			t.grid(column=0,row=1)
	
	b1=Button(popup,text="save",command= save)
	b2=Button(popup,text="cancel",command=close)
	entry= ttk.Entry(popup, textvariable = currentFile)
	
	entry.grid(column=0, row = 0, sticky = (N, S, E, W))
	b1.grid(column=0, row = 2, sticky = (N, S, E, W))
	b2.grid(column=1, row = 2, sticky = (N, S, E, W))








def getlistvarrec(current):
	listvar=[]
	
	if isinstance(current, cl.Variable):
		if current.name!='undefined':
			listvar.append(current.name)
	
	elif not isinstance(current, (cl.Top, cl.Bot)) :
		for succ in current.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar


def getListVarForm():
	listvar=[]
	
	if isinstance(usrData.formula, cl.Variable):
		if usrData.formula.name!='undefined':
			listvar.append(usrData.formula.name)
	elif not isinstance(usrData.formula, (cl.Top,cl.Bot)):
		for succ in usrData.formula.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar


def destroyMainWindowSons() :
	for enfant in window.winfo_children():
		if isinstance(enfant, ttk.Frame):
			enfant.destroy()


def createMainFrame() :

	
	window.title("TER 2020-2021 - Logique Intuitionniste - Menu principal")

	window.columnconfigure(0, weight = 1)
	window.rowconfigure(0, weight = 1)
	
	
	# DESTRUCTION DE L'ANCIENNE FENETRE

	destroyMainWindowSons()
	

	
	# CREATION DU CADRE DE LA FENETRE PRINCIPALE

	mainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))
	mainFrame.grid(column = 0, row = 0, sticky = (N, S, E, W))

	
	# TITRE DE LA FENÊTRE PRINCIPALE

	mainFrameTitle = ttk.Label(mainFrame, text = 'Logique Intuitionniste TER 2020-2021', style='Titre.TLabel')
	mainFrameTitle.grid(column = 0, row = 0, columnspan = 2, sticky =(E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	mainFrame.columnconfigure(0, weight = 1)
	mainFrame.rowconfigure(0, weight = 1)


def createToolbar() :
	  
  # BARRE DE MENU

	barreMenu = Menu(window)
	window['menu'] = barreMenu

	# MENU FICHIER DE LA BARRE DE MENU

	fichierMenu = Menu(barreMenu, tearoff = 0)
	fichierMenu.add_command(label = 'Créer une nouvelle interprétation', command = createInter)
	fichierMenu.add_command(label = 'Ouvrir une interprétation existante', command = openInter)
	fichierMenu.add_command(label = 'Ouvrir une formule existante', command = openFormula)
	fichierMenu.add_command(label = 'Ouvrir un modele existant', command = openWorld)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer l'interpétation", command = saveCInter) 
	fichierMenu.add_command(label = "Enregistrer l'interprétation sous...", command = saveNInter)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer la formule", command = saveCFormula) 
	fichierMenu.add_command(label = "Enregistrer la formule sous...", command = saveNFromula)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer le model", command = saveCWorld) 
	fichierMenu.add_command(label = "Enregistrer le model sous...", command = saveNWorld)

	# AJOUT DU MENU FICHIER A LA BARRE DE MENU

	barreMenu.add_cascade(label = 'Fichier', menu = fichierMenu)



def createFormulaFrame() :


	class FormuleWrapper(TreeWrapper):
		def children(self,node):
			if not isinstance(node, (cl.Variable, cl.Top, cl.Bot)) :
				return [succ for succ in node.succ]
			else:
				return None

		def label(self, node):
			if node.name != 'undefined':
				return node.name
			elif node != cl.Node.classVar:
				return ''
			else:
				return None

		def onClick(self,node):
			usrData.select
			usrData.select=node
			viewer.drawTree(usrData.formula)

		def bg(self, node):
			if node==usrData.select:
				return 'yellow2'
			return 'gray77'


	def replacerec(father,selected,elem):
		if not isinstance(father,(cl.Variable, cl.Top, cl.Bot)) :
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
	
		if usrData.formula==selected:
			usrData.formula=elem
			usrData.select=elem
			return True
		else:
			if replacerec(usrData.formula,selected,elem):
				usrData.select=elem
				print(usrData.formula)
				return True
			else:
				return False
	

	def succDecide(select,newnode):
		if not (isinstance(select,(cl.Top,cl.Bot,cl.Variable)) or isinstance(newnode,(cl.Top,cl.Bot,cl.Variable))):
			index=[ x for x in range(len(select.succ)) if select.succ[x].name!= "undefined"]
            	
			if len(index)!=0:
				popup=Toplevel()
				popup.minsize(300,200)
				popup.maxsize(300,200)
				popup.grab_set()
				def conserver(indexold,indexnew):
					for x in range(len(indexold)):
						newnode.succ[indexnew[x]]=select.succ[indexold[x]]
					popup.grab_release()
					popup.destroy()
					popup.update()

				label = Label(popup,text="{select.name} a déjà "+len(index)+" fils assigné voulez vous en conservé pour nouveau {newnode.name}")
				label.grid(column=0,row=0, sticky=NSEW)
				if isinstance(newnode,cl.Not):
					if len(index)==1:
						conserver=Button(popup,text="Conserver le fils",command= conserver([index[0]],[0]))

						conserver.grid(row=2,column=0,sticky=NS)
						
						
					elif len(index)==2:
						conserver1=Button(popup,text="Conserver le fils gauche",command= conserver([index[0]],[0]))
						conserver2=Button(popup,text="Conserver le fils droit",command= conserver([index[1]],[0]))

						conserver1.grid(row=2,column=0,sticky=NS)
						conserver2.grid(row=2,column=1,sticky=NS)
				else:
					if len(index)==1:
						conserverL=Button(popup,text="Conserver le fils et le placer a gauche",command= conserver([index[0]],[0]))
						conserverR=Button(popup,text="Conserver le fils et le placer a droite",command= conserver([index[0]],[1]))

						conserverL.grid(row=2,column=0,sticky=NS)
						conserverR.grid(row=2,column=1,sticky=NS)
		
					
					elif len(index)==2:
						conserver1L=Button(popup,text="Conserver le fils gauche et le placer a gauche",command= conserver([index[0]],[0]))
						conserver1R=Button(popup,text="Conserver le fils gauche et le placer a droite",command= conserver([index[0]],[1]))
						conserver2L=Button(popup,text="Conserver le fils droit et le placer a gauche",command= conserver([index[1]],[0]))
						conserver2R=Button(popup,text="Conserver le fils droit et le placer a droite",command= conserver([index[1]],[1]))
						conserver=Button(popup,text="Conserver les deux",command= conserver(index,[0,1]))
						conserverRev=Button(popup,text="Conserver les deux mais inversé leurs position",command= conserver(index,[1,0]))

						conserver1L.grid(row=2,column=0,sticky=NS)
						conserver1R.grid(row=2,column=1,sticky=NS)
						conserver2L.grid(row=2,column=2,sticky=NS)
						conserver2R.grid(row=2,column=3,sticky=NS)
						conserver.grid(row=2,column=4,sticky=NS)
						conserverRev.grid(row=2,column=5,sticky=NS)

						
					
				rien=Button(popup,text="Ne rien conserver",command= conserver([],[]))
				rien.grid(column=0,row=3,sticky=NS)
						

	def changeEntryTextFromListbox(*args):
		if len(variableListbox.curselection()) > 0 :
			entryText = listVar[int(variableListbox.curselection()[0])]
			entryTextVar.set(entryText)


	def createVar(*args):
		if varnameEntry.get()!='':
			if varnameEntry.get()!= 'undefined':
				var = cl.Variable(varnameEntry.get().lower())
				if replace(usrData.select,var):

					viewer.drawTree(usrData.formula)

					if var.name in listVar:
						listVar.remove(var.name)
					listVar.insert(0,var.name)
					listVarVar.set(listVar)

					variableListbox.select_clear(0,"end")
					variableListbox.select_set(0)

					varnameEntry.delete(0, len(varnameEntry.get()))

					return messagebox.showinfo('message',f'Variable {var.name} crée')
				else:
					return messagebox.showinfo('ERROR:',f"La node selectionner n'a pas pu être trouvé")
			else:
				return messagebox.showinfo('message',f"undefined n'est pas un nom de variable valide")
		elif  len(variableListbox.curselection())==1:

			var=cl.Variable(listVar[variableListbox.curselection()[0]])
			if replace(usrData.select,var):
				viewer.drawTree(usrData.formula)

				listVar.remove(var.name)
				listVar.insert(0,var.name)
				listVarVar.set(listVar)

				variableListbox.select_clear(0,"end")
				variableListbox.select_set(0)

				varnameEntry.delete(0, len(varnameEntry.get()))

				return messagebox.showinfo('message',f'Variable {var.name} assignée.')

			else:
				return messagebox.showinfo('ERROR:',f"La node selectionner n'a pas pu être trouvé")
		else:
			return messagebox.showinfo('message',f'Sélectionnez une variable ou entrez en une nouvelle')


	def createOr():
		var = cl.Or(cl.Variable("undefined"), cl.Variable("undefined"))
		succDecide(usrData.select, var)
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)
	
	def createAnd():
		var = cl.And(cl.Variable("undefined"), cl.Variable("undefined"))
		succDecide(usrData.select, var)
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)

	def createImp():
		var = cl.Imp(cl.Variable("undefined"), cl.Variable("undefined"))
		succDecide(usrData.select, var)
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)

	def createNot():
		var = cl.Not(cl.Variable("undefined"))
		succDecide(usrData.select, var)
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)

	def createTop():
		var = cl.Top()
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)

	def createBot():
		var = cl.Bot()
		replace(usrData.select, var)
		viewer.drawTree(usrData.formula)
	
	



	window.title("TER 2020-2021 - Logique Intuitionniste - Éditeur de formule")


	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()
	


	# VARIABLES DE CONTROLE

	listVar = getListVarForm()
	
	listVarVar = StringVar(value = listVar)

	entryText = ""
	entryTextVar = StringVar(value = entryText)



	# CREATION DU CADRE DE LA PAGE CREER FORMULE

	formulaMainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))


	# CREATION DES ELEMENTS DU CADRE FORMULE

	formulaTitleFrame = ttk.Label(formulaMainFrame, text='Editeur de formule', style='Titre.TLabel')
	graphFrame = ttk.Frame(formulaMainFrame)
	toolBox = ttk.Notebook(formulaMainFrame)
	toolsFrame = ttk.Frame(toolBox)

	Bouton_Or = ttk.Button(toolsFrame, text = "Or", command = createOr)
	Bouton_And = ttk.Button(toolsFrame, text = "And", command = createAnd)
	Bouton_Imp = ttk.Button(toolsFrame, text = "Imp", command = createImp)
	Bouton_Not = ttk.Button(toolsFrame, text = "Not", command = createNot)
	Bouton_Top = ttk.Button(toolsFrame, text = "Top", command = createTop)
	Bouton_Bot = ttk.Button(toolsFrame, text = "Bot", command = createBot)



	variableFrame =ttk.Frame(toolBox)
	varnameEntry = ttk.Entry(variableFrame, textvariable = entryTextVar)
	createVarButton = ttk.Button(variableFrame, text='Ajouter', command = createVar)
	variableListbox = Listbox(variableFrame, selectmode = 'browse', yscrollcommand = True, listvariable = listVarVar)


	# CREATION DES FRAMES DE REMPLISSAGE DES VIDES (si nécessaire)




	# PLACEMENT DU CADRE (FRAME) PRINCIPAL DANS LA FENETRE (window)

	formulaMainFrame.grid(column = 0, row = 0, sticky=(N, S, E, W))


	# PLACEMENT DES ELEMENTS DU CADRE FORMULE DANS LA GRILLE

	formulaTitleFrame.grid(column = 0, row = 0, columnspan = 2, sticky = (N, S, E, W))
	graphFrame.grid(column = 0, row = 1, sticky = (N, S, E, W), pady = 20, padx = (20, 0))

	toolBox.grid(column = 1, row = 1, sticky = (N, S, E, W), pady = 20, padx = 20)
	toolsFrame.pack(fill = 'both', expand = True)
	variableFrame.pack(fill = 'both', expand = True)
	toolBox.add(toolsFrame, text = 'Outils')
	toolBox.add(variableFrame, text = 'Variables')

	Bouton_Not.grid(column = 0, row = 0, sticky = (N, S, E, W))
	Bouton_Or.grid(column = 0, row = 1, sticky = (N, S, E, W))
	Bouton_And.grid(column = 0, row = 2, sticky = (N, S, E, W))
	Bouton_Imp.grid(column = 0, row = 3, sticky = (N, S, E, W))
	Bouton_Top.grid(column = 0, row = 4, sticky = (N, S, E, W))
	Bouton_Bot.grid(column = 0, row = 5, sticky = (N, S, E, W))


	varnameEntry.grid(column = 0, row = 0, sticky = (N, S, E, W))
	createVarButton.grid(column = 1, row = 0, sticky = (N, S, E, W))
	variableListbox.grid(column = 0, row = 1, columnspan = 2, sticky = (N, S, E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	formulaMainFrame.columnconfigure(0, weight = 1)
	formulaMainFrame.rowconfigure(1, weight = 1)

	variableFrame.columnconfigure(0, weight = 1)
	variableFrame.rowconfigure(1, weight = 1)


	# PARTIE FONCTIONNELLE


	

	variableListbox.bind("<<ListboxSelect>>", changeEntryTextFromListbox)
	variableListbox.bind("<Double-1>", createVar)
	window.bind("<Return>", createVar)



	fwrap = FormuleWrapper()	
	viewer = TreeViewer(fwrap, graphFrame, usrData.formula)


def createModelFrame() :


	

	class ModeleWrapper(TreeWrapper):
		def children(self,node):
			if len(self._sons)!=0:
				return self._sons
			else:
				return None

		def label(self, node):
			if node.name != 'undefined':
				return node.name
			else:
				return None

		def onClick(self,node):
			
			usrData.select=node
			viewer.drawTree(monde)

		def bg(self, node):
			if node==usrData.select:
				return 'yellow2'
			return 'gray77'


	window.title("TER 2020-2021 - Logique Intuitionniste - Éditeur de Model")
	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()



	# CREATION DU CADRE DE LA PAGE CREER MODEL

	worldMainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))


	# CREATION DES ELEMENTS DU CADRE MODEL

	worldTitleFrame = ttk.Label(worldMainFrame, text='Editeur De Mondes', style='Titre.TLabel')
	graphFrame = ttk.Frame(worldMainFrame)
	toolBox = ttk.Notebook(worldMainFrame)
	toolsFrame = ttk.Frame(toolBox)
	variableFrame = ttk.Frame(toolBox)
	varnameEntry = ttk.Entry(variableFrame)
	


	# CREATION DES FRAMES DE REMPLISSAGE DES VIDES




	# PLACEMENT DU CADRE (FRAME) PRINCIPAL DANS LA FENETRE (window)

	worldMainFrame.grid(column = 0, row = 0, sticky=(N, S, E, W))


	# PLACEMENT DES ELEMENTS DU CADRE FORMULE DANS LA GRILLE

	worldTitleFrame.grid(column = 0, row = 0, columnspan = 2, sticky = (N, S, E, W))
	graphFrame.grid(column = 0, row = 1, sticky = (N, S, E, W), pady = 20, padx = (20, 0))

	toolBox.grid(column = 1, row = 1, sticky = (N, S, E, W), pady = 20, padx = 20)
	toolsFrame.pack(fill = 'both', expand = True)
	variableFrame.pack(fill = 'both', expand = True)
	toolBox.add(toolsFrame, text = 'Outils')
	toolBox.add(variableFrame, text = 'Variables')

	


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	worldMainFrame.columnconfigure(0, weight = 1)
	worldMainFrame.rowconfigure(1, weight = 1)


	# PARTIE FONCTIONNELLE

	listvar = getlistvar()

	

	fwrap=WorldWrapper()	
	viewer = TreeViewer(fwrap, graphFrame, world)



###############################################
		 # INITIALISATION FENÊTRE #	
###############################################

window = Tk()

window.minsize(720, 360)



createToolbar()

createMainFrame()


###############################################
				 # STYLE #
###############################################

style = ttk.Style()

style.theme_use('clam')

style.configure('AfficheModele.TFrame', background='white', borderwidth=15, relief='sunken')
style.configure('Titre.TLabel', font=('arial 20'), relief='groove', borderwidth=10, anchor='center')



window.mainloop()
