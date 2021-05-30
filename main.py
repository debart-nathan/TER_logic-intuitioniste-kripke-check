import classes as cl
import copy
from savefilesystem import *
from graph_view import TreeViewer,TreeWrapper
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os



usrData=Userdata()

def defTitle(activeFrame):
	"""Détermine le titre de la Fenêtre principale 
	avec activeFrame une String nous donnant notre position dans l'interface"""

	text= "formule : "
	if not (usrData.currentFFile is None):
		text+=(usrData.currentFFile+".formula")
	else:
		text+=" aucune " 

	text+="| modèle : "
	if not (usrData.currentWFile is None):
		text+=(usrData.currentWFile+".model")
	else:
		text+=" aucun "
	text+=" - TER 2020-2021 - Logique Intuitionniste - "
	text+= activeFrame
	window.title(text)

def wellFormedRec(formula) :
		res=True

		if formula.name == "undefined" :
			res= False
		else :
			if not isinstance(formula, (cl.Variable, cl.Top, cl.Bot)):
	
				for suc in formula.succ :
					res = res and wellFormedRec(suc)

		return res
	

	 

		

	

def createInter():
	"""initialise une interprétation vide et lance l'interface de modification des formules"""
	
	usrData.model= cl.World("M:0")
	usrData.formula = cl.Variable('undefined')
	usrData.select = usrData.formula
	createFormulaFrame()

def openFormula():
	"""Ouvre une formule pré-enregistrée à l'aide d'un navigateur de fichier et lance l'éditeur de formule
	seul des fichiers présents dans 'assets/userdata' peuvent être chargés"""

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
	"""Ouvre un monde pré-enregistré à l'aide d'un navigateur de fichier et lance l'éditeur de modèle
	seul des fichiers présents dans 'assets/userdata' peuvent être chargés"""
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

			if wellFormedRec(usrData.formula) :
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
			messagebox.showinfo('Erreur de Dossier',f'prenez les fichiers dans ./asset/userdata')
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
		messagebox.showinfo('Alert',f'Au moins un des fichers (formule/modèle) n\'est pas ouvert')
	else:
		usrData.save(ffileset=usrData.currentFFile,wfilset=usrData.currentWFile)

def saveNInter():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisissez un nom")
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
	if usrData.currentFFile == None :
		messagebox.showinfo('Alert',f'Aucun fichier formule ouvert')
	else:
		usrData.save(ffileset=usrData.currentFFile)

def saveNFromula():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisissez un nom")
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
			t = Label(popup, text ="Le nom ne peut pas être vide", fg = "red")
			t.grid(column=0, row = 1)
	
	b1=Button(popup,text="save", command = save)
	b2=Button(popup,text="cancel", command =close)
	entry= ttk.Entry(popup, textvariable = currentFile)
	
	entry.grid(column=0, row = 0, sticky = (N, S, E, W))
	b1.grid(column=0, row = 2, sticky = (N, S, E, W))
	b2.grid(column=1, row = 2, sticky = (N, S, E, W))

def	saveCWorld():
	if  usrData.currentWFile ==None:
		messagebox.showinfo('Alert',f'Aucun fichier modèle ouvert')
	else:
		usrData.save(wfilset=usrData.currentWFile)

def saveNWorld():
	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisissez un nom")
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


def	saveCInter():
	"""sauvegade le dernier fichier de Monde et de Formule ouvert dans l'instance"""

	if usrData.currentFFile ==None or usrData.currentWFile ==None:
		messagebox.showinfo('Alert',f'Au moins un des fichers (formule/modèle) n\'est pas ouvert')
	else:
		usrData.save(ffileset=usrData.currentFFile,wfilset=usrData.currentWFile)

def saveNInter():
	"""enregistre la formule et le modèle courants dans 'assets/userdata' sous un nom choisi par l'utilisateur """

	popup=Toplevel()
	popup.grab_set()
	popup.title("Choisissez un nom")
	currentFile=""

	def close():
		"""annule la sauvegarde"""

		popup.grab_release()
		popup.destroy()
		popup.update()
	def save():
		"""sauvegarde avec le nom choisi"""

		currentFile=entry.get()
		if currentFile !="":
			usrData.save(ffileset=currentFile,wfileset=currentFile)
			usrData.currentFFile=currentFile
			usrData.currentWFile=currentFile
			mainFrameName=window.title().rsplit('-',1)[1]
			defTitle(mainFrameName)
			close()
		else:
			t=Label(popup,text ="le nom ne peut pas être vide",fg="red")
			t.grid(column=0,row=1,columnspan=2)
	
	b1=Button(popup,text="save",command= save)
	b2=Button(popup,text="cancel",command=close)
	entry= ttk.Entry(popup, textvariable = currentFile)
	


def getListVarForm():
	"""vérifie que la racine est une variable si oui on l'envoie dans une liste sinon on renvoie le résultat de la version récursive
	renvoie une liste de Variable sans répétition sur les noms"""

	listvar=[]
	
	if isinstance(usrData.formula, cl.Variable):
		if usrData.formula.name!='undefined':
			listvar.append(usrData.formula)
	elif not isinstance(usrData.formula, (cl.Top,cl.Bot)):
		def getlistvarrec(current):
			"""vérifie si current est une variable définie et si oui l'ajoute à la liste,
			puis relance la fonction sur les successeurs de current et concatène les résultats dans le retour
			renvoie une liste de Variable sans répétition sur les nom"""

			listvar=[]
	
			if isinstance(current, cl.Variable):
				if current.name!='undefined':
					listvar.append(current)
	
			elif not isinstance(current, (cl.Top, cl.Bot)) :
				for succ in current.succ:
					varsuc=getlistvarrec(succ)
					for var in varsuc:
						a=True
						for var2 in listvar:
							if var2.name == var.name:
								a=False	
						if a:
							listvar.append(var)
			return listvar

		for succ in usrData.formula.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				a=True
				for var2 in listvar:
					if var2.name == var.name:
						a=False	
				if a:
					listvar.append(var)
	return listvar



def destroyMainWindowSons() :
	"""nettoie l'interface de ses éléments"""

	for enfant in window.winfo_children():
		if isinstance(enfant, ttk.Frame):
			enfant.destroy()


def createMainFrame() :
	"""génère la page d'accueil de l'application"""

	
	defTitle("Menu principal")

	window.columnconfigure(0, weight = 1)
	window.rowconfigure(0, weight = 1)
	
	
	# DESTRUCTION DE L'ANCIENNE FENETRE

	destroyMainWindowSons()
	

	
	# CREATION DU CADRE DE LA FENETRE PRINCIPALE

	mainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))
	mainFrame.grid(column = 0, row = 0, sticky = (N, S, E, W))

	
	# TITRE DE LA FENÊTRE PRINCIPALE

	mainFrameTitle = ttk.Label(mainFrame, text = 'Logique Intuitionniste TER 2020-2021', style='Title.TLabel')
	mainFrameTitle.grid(column = 0, row = 0, columnspan = 2, sticky =(E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	mainFrame.columnconfigure(0, weight = 1)
	mainFrame.rowconfigure(0, weight = 1)


def createToolbar() :
	"""génère le menu déroulant de l'application utilisé pour sauvegarder/charger/créer des fichiers"""	  

  # BARRE DE MENU

	barreMenu = Menu(window)
	window['menu'] = barreMenu

	# MENU FICHIER DE LA BARRE DE MENU

	fichierMenu = Menu(barreMenu, tearoff = 0)
	fichierMenu.add_command(label = 'Créer une nouvelle interprétation', command = createInter)
	fichierMenu.add_command(label = 'Ouvrir une interprétation existante', command = openInter)
	fichierMenu.add_command(label = 'Ouvrir une formule existante', command = openFormula)
	fichierMenu.add_command(label = 'Ouvrir un modèle existant', command = openWorld)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer l'interpétation", command = saveCInter) 
	fichierMenu.add_command(label = "Enregistrer l'interprétation sous...", command = saveNInter)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer la formule", command = saveCFormula) 
	fichierMenu.add_command(label = "Enregistrer la formule sous...", command = saveNFromula)
	fichierMenu.add_separator()
	fichierMenu.add_command(label = "Enregistrer le modèle", command = saveCWorld) 
	fichierMenu.add_command(label = "Enregistrer le modèle sous...", command = saveNWorld)

	# AJOUT DU MENU FICHIER A LA BARRE DE MENU

	barreMenu.add_cascade(label = 'Fichier', menu = fichierMenu)



def createFormulaFrame() :
	"""Génère l'interface d'édition des formules"""

	class FormuleWrapper(TreeWrapper):
		"""Couche de compatibilité entre les arbres de formules et TreeView"""

		def children(self,node):
			"""Accesseur du successeur d'une node dans l'arbre des formules"""

			if not isinstance(node, (cl.Variable, cl.Top, cl.Bot)) :
				return [succ for succ in node.succ]
			else:
				return None

		def label(self, node):
			"""Définition du texte affiché sur l'objet d'interface graphique représentant la node"""

			if node.name != 'undefined':
				return node.name
			elif node != cl.Node.classVar:
				return ''
			else:
				return None

		def onClick(self,node):
			"""Détermination de l'effet quand on clique sur une node"""

			usrData.select
			usrData.select=node
			viewer.drawTree(usrData.formula)

		def bg(self, node):
			"""Définition de la couleur de l'objet d'interface graphique représentant la node"""

			if node==usrData.select:
				return 'yellow2'
			return 'gray77'


	def Next(*args) :

		if  wellFormedRec(usrData.formula):

			messagebox.showinfo('message',f'La formule est bien formée')
			usrData.select=usrData.model
			createModelFrame()
		
		else :
			messagebox.showinfo('message',f'La formule n\'est pas bien formée, veuillez remplir toutes les cases')


	def rewind(*args) :
		global savedFormula
		if savedFormula == None :
			return messagebox.showinfo('message',f'Pas de retour en arrière possible')
		else :
			usrData.formula = savedFormula
			savedFormula = None
			usrData.select=usrData.formula
			updateTextForm()
			viewer.drawTree(usrData.formula)

	def saveFormula(*args):
		global savedFormula
		savedFormula = copy.copy(usrData.formula)

	def updateTextForm(*args):

		formText = str(usrData.formula)
		formTextVar.set(formText)

	
	def replace(selected,elem):
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

		saveFormula()
		if usrData.formula==selected:
			usrData.formula=elem
			usrData.select=elem
			
			return True
		else:
			if replacerec(usrData.formula,selected,elem):
				usrData.select=elem
				return True
			else:
				return False
	

	
	def succDecide(select,newnode):
		"""Demande à l'utilisateur si il faut conserver (Transférer) les fils de select pour newnode, 
		et si oui à quelle position mettre ceux que l'on garde
		retourne False si select n'a aucun fils et True si il en a"""
		if not isinstance(select,(cl.Top,cl.Bot,cl.Variable)) or isinstance(newnode,(cl.Top,cl.Bot,cl.Variable)):
			
			index=[ x for x in range(len(select.succ)) if select.succ[x].name!= "undefined"]
                
			if len(index)!=0:
				popup=Toplevel()
				popup.minsize(300,200)
				popup.grab_set()

				popupFrame = ttk.Frame(popup, padding = (20, 2, 20, 10))
				popupFrame.grid(column = 0, row = 0, sticky = (N, S, E, W))

				def conserver(indexold,indexnew):
					"""Transfère les fils de select choisi dont la postion est définie par indexold 
					dans leurs nouvelles postions dans newnode définie par indexnew
					puis met à jour l'affichage et supprime le popup"""
					for x in range(len(indexold)):
						newnode.succ[indexnew[x]]=select.succ[indexold[x]]
					updateTextForm()
					viewer.drawTree(usrData.formula)
					popup.grab_release()
					popup.destroy()
					popup.update()

				label = ttk.Label(popupFrame,text = select.name + " a déjà "+ ("un" if len(index)==1 else "deux") +" fils "+ ("assigné" if len(index)==1 else "assignés") +" voulez vous en conserver pour "+ newnode.name +" ?", style = "Conserver.TLabel")

				rien = ttk.Button(popupFrame,text="Ne rien conserver",command = lambda : conserver([], []), style = 'Conserver.TButton')
				if isinstance(newnode,cl.Not):
					if len(index)==1:
						cons=ttk.Button(popupFrame,text="Conserver le fils",command = lambda : conserver([index[0]], [0]), style = 'Conserver.TButton')

						cons.grid(row=1,column=0,sticky=(N, S, E, W))

						label.grid(column = 0, row = 0, sticky=(N, E, W))
						rien.grid(column=0, row=3, sticky=(N, S, E, W))                        

   
					elif len(index)==2:
						conserver1=ttk.Button(popupFrame,text="Conserver le fils gauche", command = lambda: conserver([index[0]], [0]), style = 'Conserver.TButton')
						conserver2=ttk.Button(popupFrame,text="Conserver le fils droit", command = lambda: conserver([index[1]], [0]), style = 'Conserver.TButton')

						conserver1.grid(row=1,column=0, sticky=(N, S, E, W))
						conserver2.grid(row=1,column=1, sticky=(N, S, E, W))

						label.grid(column = 0, row = 0, columnspan = 2, sticky=(N, E, W))
						rien.grid(column=0, row=3, columnspan = 2, sticky=(N, S, E, W))

						popupFrame.columnconfigure(1, weight = 1)
				else:
					if len(index)==1:
						conserverL=ttk.Button(popupFrame,text="Conserver le fils et le placer a gauche", command = lambda : conserver([index[0]], [0]), style = 'Conserver.TButton')
						conserverR=ttk.Button(popupFrame,text="Conserver le fils et le placer a droite", command = lambda : conserver([index[0]], [1]), style = 'Conserver.TButton')

						conserverL.grid(row=1,column=0,sticky=(N, S, E, W))
						conserverR.grid(row=1,column=1,sticky=(N, S, E, W))

						label.grid(column = 0, row = 0, columnspan = 2, sticky=(N, E, W))
						rien.grid(column=0, row=3, columnspan = 2, sticky=(N, S, E, W))
                        
						popupFrame.columnconfigure(1, weight = 1)
					elif len(index)==2:
						conserver1L=ttk.Button(popupFrame,text="Conserver le fils gauche et le placer a gauche", command= lambda : conserver([index[0]], [0]), style = 'Conserver.TButton')
						conserver1R=ttk.Button(popupFrame,text="Conserver le fils gauche et le placer a droite", command= lambda : conserver([index[0]], [1]), style = 'Conserver.TButton')
						conserver2L=ttk.Button(popupFrame,text="Conserver le fils droit et le placer a gauche", command= lambda : conserver([index[1]], [0]), style = 'Conserver.TButton')
						conserver2R=ttk.Button(popupFrame,text="Conserver le fils droit et le placer a droite", command= lambda : conserver([index[1]], [1]), style = 'Conserver.TButton')
						cons=ttk.Button(popupFrame,text="Conserver les deux", command= lambda : conserver(index, [0,1]), style = 'Conserver.TButton')
						conserverRev=ttk.Button(popupFrame,text="Conserver les deux mais inverser leurs position", command= lambda : conserver(index, [1,0]), style = 'Conserver.TButton')

						conserver1L.grid(row=1,column=0,sticky=(N, S, E, W))
						conserver1R.grid(row=1,column=1,sticky=(N, S, E, W))
						conserver2L.grid(row=1,column=2,sticky=(N, S, E, W))
						conserver2R.grid(row=2,column=0,sticky=(N, S, E, W))
						cons.grid(row=2,column=1,sticky=(N, S, E, W))
						conserverRev.grid(row=2,column=2,sticky=(N, S, E, W))

						label.grid(column = 0, row = 0, columnspan = 3, sticky=(N, E, W))
						rien.grid(column=0, row=3, columnspan = 3, sticky=(N, S, E, W))
						popupFrame.columnconfigure(1, weight = 1)
						popupFrame.columnconfigure(2, weight = 1)
						
                        
                    

				popupFrame.columnconfigure(0, weight = 1)
				popupFrame.rowconfigure(0, weight = 1)

				popup.columnconfigure(0, weight = 1)
				popup.rowconfigure(0, weight = 1)
				popup.title("Que faire des fils présents ?")
				return True
		return False

	def changeEntryTextFromListbox(*args):
		"""Change le texte de l'entrée de texte utilisée pour determiner le nom d'une nouvelle variable dans la formule 
		par l'entrée séléctionnée dans la listbox servant d'historique"""
		if len(variableListbox.curselection()) > 0 :
			entryText = listVar[int(variableListbox.curselection()[0])].name
			entryTextVar.set(entryText)



	def createVar(*args):
		"""Crée une variable à la place de la node sélectionnée qui aura pour nom
		en suivant l'ordre de priorité : ce qu'il y a dans l'entrée de texte, le nom selectioné dans la listbox
		si le nom dans l'entrée de texte est undefined on renverra une erreur via popup car c'est notre élément neutre
		si aucun nom n'est entré ou selectionné on renverra aussi une erreur par popup"""
		
		if varnameEntry.get()!='':
			if varnameEntry.get()!= 'undefined':
				var = cl.Variable(varnameEntry.get().lower())
				if replace(usrData.select,var):
					for var2 in listVar:
						if var2.name == var.name:
							listVar.remove(var2)
							
					listVar.insert(0,var)
					listVarVar.set([var.name for var in listVar])

					variableListbox.select_clear(0,"end")
					variableListbox.select_set(0)

					varnameEntry.delete(0, len(varnameEntry.get()))

					updateTextForm()
					viewer.drawTree(usrData.formula)
					return messagebox.showinfo('message',f'Variable {var.name} crée')
				else:
					return messagebox.showinfo('ERROR:',f"La node selectionnée n'a pas pu être trouvée")
			else:
				return messagebox.showinfo('message',f"undefined n'est pas un nom de variable valide")
		elif  len(variableListbox.curselection())==1:

			var=cl.Variable(listVar[variableListbox.curselection()[0]].name)
			if replace(usrData.select,var):
				for var2 in listVar:
					if var2.name == var.name:
						listVar.remove(var2)
				listVar.insert(0,var)
				listVarVar.set([var.name for var in listVar])

				variableListbox.select_clear(0,"end")
				variableListbox.select_set(0)

				varnameEntry.delete(0, len(varnameEntry.get()))
				
				updateTextForm()
				viewer.drawTree(usrData.formula)

				return messagebox.showinfo('message',f'Variable {var.name} assignée.')

			else:
				return messagebox.showinfo('ERROR:',f"La node selectionnée n'a pas pu être trouvée")
		else:
			return messagebox.showinfo('message',f'Sélectionnez une variable ou entrez en une nouvelle')


	def createOr():
		"""remplace la node selectionnée par un Or en demandant que faire des sous arbres présents si il y en a
		et si il n'y en a pas met à jour l'interface """
		
		var = cl.Or(cl.Variable("undefined"), cl.Variable("undefined"))
		if succDecide(usrData.select, var):
			replace(usrData.select, var)
		else:
			replace(usrData.select, var)
			updateTextForm()
			viewer.drawTree(usrData.formula)
			
	
	def createAnd():
		"""remplace la node selectionnée par un And en demandant que faire des sous arbres présents si il y en a
		et si il n'y en a pas met à jour l'interface """

		var = cl.And(cl.Variable("undefined"), cl.Variable("undefined"))
		if succDecide(usrData.select, var):
			replace(usrData.select, var)
		else:
			replace(usrData.select, var)
			updateTextForm()
			viewer.drawTree(usrData.formula)

	def createImp():
		"""remplace la node selectionnée par une Implication en demandant que faire des sous arbres présents si il y en a
		et si il n'y en a pas met à jour l'interface """

		var = cl.Imp(cl.Variable("undefined"), cl.Variable("undefined"))
		if succDecide(usrData.select, var):
			replace(usrData.select, var)
		else:
			replace(usrData.select, var)
			updateTextForm()
			viewer.drawTree(usrData.formula)

	def createNot():
		"""remplace la node selectionnée par un Not en demandant que faire des sous arbres présents si il y en a
		et si il n'y en a pas met à jour l'interface """

		var = cl.Not(cl.Variable("undefined"))
		if succDecide(usrData.select, var):
			replace(usrData.select, var)
		else:
			replace(usrData.select, var)
			updateTextForm()
			viewer.drawTree(usrData.formula)

	def createTop():
		"""remplace la node selectionnée par un Top et met à jour l'interface"""

		var = cl.Top()
		replace(usrData.select, var)
		updateTextForm()
		viewer.drawTree(usrData.formula)

	def createBot():
		"""remplace la node selectionnée par un Bot et met à jour l'interface """

		var = cl.Bot()
		replace(usrData.select, var)
		updateTextForm()
		viewer.drawTree(usrData.formula)
	
	



	defTitle("Éditeur de formule")


	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()
	


	# VARIABLES DE CONTROLE

	listVar = getListVarForm()
	
	listVarVar = StringVar(value = [var.name for var in listVar])

	entryText = ""
	entryTextVar = StringVar(value = entryText)

	formText = usrData.formula.__repr__()
	formTextVar = StringVar(value = formText)


	global savedFormula
	savedFormula = None

	# CREATION DU CADRE DE LA PAGE CREER FORMULE

	formulaMainFrame = ttk.Frame(window, padding = (20, 2, 20, 5))


	# CREATION DES ELEMENTS DU CADRE FORMULE

	formulaTitleFrame = ttk.Label(formulaMainFrame, text='Éditeur de formule', style='Title.TLabel')
	graphFrame = ttk.Frame(formulaMainFrame)
	toolBox = ttk.Notebook(formulaMainFrame)
	
	
	toolsFrame = ttk.Frame(toolBox)

	bouton_Or = ttk.Button(toolsFrame, text = "Or", command = createOr)
	bouton_And = ttk.Button(toolsFrame, text = "And", command = createAnd)
	bouton_Imp = ttk.Button(toolsFrame, text = "Imp", command = createImp)
	bouton_Not = ttk.Button(toolsFrame, text = "Not", command = createNot)
	bouton_Top = ttk.Button(toolsFrame, text = "Top", command = createTop)
	bouton_Bot = ttk.Button(toolsFrame, text = "Bot", command = createBot)



	variableFrame =ttk.Frame(toolBox)
	varnameEntry = ttk.Entry(variableFrame, textvariable = entryTextVar)
	createVarButton = ttk.Button(variableFrame, text='Ajouter', command = createVar)
	variableListbox = Listbox(variableFrame, selectmode = 'browse', yscrollcommand = True, listvariable = listVarVar)
	listboxScrollbar = ttk.Scrollbar(variableListbox, orient = VERTICAL, command = variableListbox.yview)
	formulaLabel = ttk.Label(formulaMainFrame, textvariable = formTextVar, style = 'Formula.TLabel')
	nextButton = ttk.Button(formulaMainFrame, text = "Valider et passer au modèle", command = Next)


	rewindButton = ttk.Button(formulaMainFrame, text = 'Annuler le dernier changement', command = rewind)



	# CREATION DES FRAMES DE REMPLISSAGE DES VIDES (si nécessaire)




	# PLACEMENT DU CADRE (FRAME) PRINCIPAL DANS LA FENETRE (window)

	formulaMainFrame.grid(column = 0, row = 0, sticky=(N, S, E, W))


	# PLACEMENT DES ELEMENTS DU CADRE FORMULE DANS LA GRILLE

	formulaTitleFrame.grid(column = 0, row = 0, columnspan = 2, sticky = (N, S, E, W))
	graphFrame.grid(column = 0, row = 1, sticky = (N, S, E, W), pady = 20, padx = (20, 0))

	toolBox.grid(column = 1, row = 1, sticky = (N, S, E, W), pady = 20, padx = 20)
	toolsFrame.pack(fill = 'both', expand = True)
	variableFrame.pack(fill = 'both', expand = True)
	


	bouton_Not.grid(column = 0, row = 0, sticky = (N, S, E, W))
	bouton_Or.grid(column = 0, row = 1, sticky = (N, S, E, W))
	bouton_And.grid(column = 0, row = 2, sticky = (N, S, E, W))
	bouton_Imp.grid(column = 0, row = 3, sticky = (N, S, E, W))
	bouton_Top.grid(column = 0, row = 4, sticky = (N, S, E, W))
	bouton_Bot.grid(column = 0, row = 5, sticky = (N, S, E, W))


	varnameEntry.grid(column = 0, row = 0, sticky = (N, S, E, W))
	createVarButton.grid(column = 1, row = 0, sticky = (N, S, E, W))
	variableListbox.grid(column = 0, row = 1, columnspan = 2, sticky = (N, S, E, W))
	formulaLabel.grid(column = 0, row = 2,rowspan=2, sticky = (N, S, E, W))
	listboxScrollbar.grid(column = 0, row = 0, sticky = (N, S, E))
	nextButton.grid(column = 1, row = 3, sticky = (N, S, E, W))
	rewindButton.grid(column = 1, row = 2, sticky = (N, S, E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	formulaMainFrame.columnconfigure(0, weight = 1)
	formulaMainFrame.rowconfigure(1, weight = 1)

	variableFrame.columnconfigure(0, weight = 1)
	variableFrame.rowconfigure(1, weight = 1)

	variableListbox.columnconfigure(0, weight = 1)
	variableListbox.rowconfigure(0, weight = 1)

	toolsFrame.columnconfigure(0, weight = 1)
	toolsFrame.rowconfigure(0, weight = 1)
	toolsFrame.rowconfigure(1, weight = 1)
	toolsFrame.rowconfigure(2, weight = 1)
	toolsFrame.rowconfigure(3, weight = 1)
	toolsFrame.rowconfigure(4, weight = 1)
	toolsFrame.rowconfigure(5, weight = 1)


	# PARTIE FONCTIONNELLE


	toolBox.add(toolsFrame, text = 'Outils')
	toolBox.add(variableFrame, text = 'Variables')

	variableListbox.configure(yscrollcommand = listboxScrollbar.set)

	variableListbox.bind("<<ListboxSelect>>", changeEntryTextFromListbox)
	variableListbox.bind("<Double-1>", createVar)
	window.bind("<Return>", createVar)



	fwrap = FormuleWrapper()	
	viewer = TreeViewer(fwrap, graphFrame, usrData.formula)


def createModelFrame() :


	

	class ModelWrapper(TreeWrapper):
		def children(self,node):
			if len(node._sons)!=0:
				return node._sons
			else:
				return None

		def label(self, node):
			if node.name != 'undefined':
				return node.name
			else:
				return None

		def onClick(self,node):
			
			usrData.select=node
			viewer.drawTree(usrData.model)
			variableWorld()

		def bg(self, node):
			if node==usrData.select:
				return 'yellow2'
			return 'gray77'

	def addSon():
		newSonName = usrData.select.name + '-'+str(len(usrData.select._sons))
		usrData.select.sons = newSonName
		viewer.drawTree(usrData.model)
		variableWorld()


	
	def removeSelfAlt(current):
		if usrData.select in current._sons :
			temp = []
			for i in current._sons :
				if i != usrData.select :
					temp.append(i)
			current._sons = temp
			viewer.drawTree(usrData.model)
		else :
			for j in current._sons :
				removeSelfAlt(j)

	def removeSelf():
		if (usrData.select != usrData.model):
			removeSelfAlt(usrData.model)
		else :
			messagebox.showinfo("",f"Vous ne pouvez pas supprimer le monde racine")


	def variableWorld():

		def valider ():
			ancesters=[]
			listvar2=[listvar[i] for i in frameCheck.curselection()]

			def getAncesters(current):
				ancesters=[]
				if usrData.select in current.sons:
					ancesters.append(current)
					return ancesters
				else:
					for world in current.sons:
						ancesters=getAncesters(world)
						if len(ancesters)>0:
							ancesters.append(current)
							break
					
					return ancesters
			
			present=[]
			if usrData.select != usrData.model:
				ancesters=getAncesters(usrData.model)
				for var in usrData.select._vars:
					if not var in listvar2:
						for world in ancesters:
							if var in present:
								break
							for var2 in world._vars:
								if var2.name==var.name:
									present.append(var)
									listvar2.append(var)
									break
			
			if len(present)>0:
				if len(present)==1:
					message= "La variable "+str(present)+" que vous voulez supprimer de "+usrData.select.name+" est aussi présente dans au moins un de ses prédécesseurs, vous devez d'abord la supprimer dans ceux-ci avant de pouvoir la supprimer ici"
				else:
					message= "Les variables "+str(present)+" que vous voulez supprimer de "+usrData.select.name+" sont aussi présentes dans au moins un de ses prédécesseurs, vous devez d'abord les supprimer dans ceux-ci avant de pouvoir les supprimer ici"
				messagebox.showinfo("",f""+message)
				variableWorld()
			
			usrData.select._vars=[]
			usrData.select.vars = listvar2
			variableWorld()

		variableT.config(text=usrData.select.name+' : \n'+ str(usrData.select._vars))
		variableV.config(text=usrData.select.name+' : \n'+ str(usrData.select._vars))
		
		frameCheck = Listbox(variableFrame, selectmode = MULTIPLE, yscrollcommand = True)
		
		frameCheck.grid(column = 0, row = 1, sticky = (N, S, E, W))

		listvar = getListVarForm()
		
		for i in range(len(listvar)) :
			
			frameCheck.insert(i,listvar[i].name)
		
			for vars in usrData.select._vars :
				if listvar[i].name == vars.name:
					frameCheck.selection_set(i)
		variablesbutton = ttk.Button(variableFrame, text = "Valider", command = valider)
		variablesbutton.grid(column = 0, row = 2 , sticky = (N, S, E, W))

	def validate(*args) :
		if valids(usrData.formula,usrData.model):
			return messagebox.showinfo('message',f"La formule est valide pour le modèle sélectionné")
		return messagebox.showinfo('message',f"La formule n'est pas valide pour le modèle sélectionné")







	defTitle("Éditeur de modèle")
	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()


	# VARIABLES DE CONTROLE

	formText = usrData.formula.__repr__()
	


	# CREATION DU CADRE DE LA PAGE CREER MODEL

	worldMainFrame = ttk.Frame(window, padding = (20, 2, 20, 5))


	# CREATION DES ELEMENTS DU CADRE MODEL

	worldTitleFrame = ttk.Label(worldMainFrame, text='Editeur De Modèle', style='Title.TLabel')
	graphFrame = ttk.Frame(worldMainFrame)

	toolBox = ttk.Notebook(worldMainFrame)
	toolsFrame = ttk.Frame(toolBox)

	variableT=Label(toolsFrame, justify=LEFT, anchor='w')
	Bouton_AjoutFils = ttk.Button(toolsFrame, text = "Ajouter fils", command = addSon)
	Bouton_RetraitSelf = ttk.Button(toolsFrame, text = "Effacer", command = removeSelf)

	variableFrame = ttk.Frame(toolBox)
	
	variableV=Label(variableFrame, justify=LEFT, anchor='w')

	formulaLabel = ttk.Label(worldMainFrame, text = formText, style = 'Formula.TLabel')

	validatebutton = ttk.Button(worldMainFrame, text='Valider', command = validate)
	backbutton = ttk.Button(worldMainFrame, text="Revenir à la formule", command = createFormulaFrame)

	



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

	Bouton_AjoutFils.grid(column = 0, row = 1, sticky = (N, S, E, W))
	Bouton_RetraitSelf.grid(column = 0, row = 2, sticky = (N, S, E, W))
	
	variableT.grid(column=0,row=0,columnspan=2,sticky=NSEW)
	variableV.grid(column=0,row=0,columnspan=2,sticky=NSEW)

	formulaLabel.grid(column = 0, row = 2, rowspan=2, sticky = (N, S, E, W))

	validatebutton.grid(column = 1, row = 3, sticky = (N, S, E, W))
	backbutton.grid(column = 1, row = 2, sticky= (N, S, E, W))

	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	worldMainFrame.columnconfigure(0, weight = 1)
	worldMainFrame.rowconfigure(1, weight = 1)


	# PARTIE FONCTIONNELLE


	mwrap=ModelWrapper()	
	viewer = TreeViewer(mwrap, graphFrame, usrData.model)
	variableWorld()



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

style.configure('Title.TLabel', font=('arial 20'), relief='groove', borderwidth=10, anchor='center')
style.configure('Formula.TLabel', font=('arial 20'), relief='groove', borderwidth=3, anchor='center')
style.configure('Keep.TLabel', font=('arial 20'), anchor='center')
style.configure('Conserver.TButton', anchor = 'center')

window.mainloop()
