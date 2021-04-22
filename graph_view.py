import tkinter as tk
from tkinter import messagebox

Width, Height = 350, 350                    # start canvas size (reset per tree)
Rowsz = 100                                 # pixels per tree row
Colsz = 100                                 # pixels per tree col

###################################
# interface to tree object's nodes
###################################

class TreeWrapper:                          # subclass for a tree type
    def children(self, treenode):
        assert 0, 'children method must be specialized for tree type'
    def label(self, treenode):
        assert 0, 'label method must be specialized for tree type'
    def value(self, treenode):
        return ''
    def onClick(self, treenode):            # node label click callback
        return ''
    def bg(self, treenode):
        return 'gray77'

##################################
# tree view gui, tree independent
##################################

class TreeViewer(tk.Frame):
    def __init__(self, wrapper, parent=None, tree=None, bg='LightSteelBlue4'):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.makeWidgets(bg)            # build gui: scrolled canvas
        self.wrapper = wrapper          # assume I'm run standalone           
        if tree:                        # embed a TreeWrapper object
            self.drawTree(tree)         # setTreeType changes wrapper 
            
           

    def makeWidgets(self, bg):
        self.canvas = tk.Canvas(self, bg=bg, borderwidth=0)
        vbar = tk.Scrollbar(self)
        hbar = tk.Scrollbar(self, orient='horizontal')

        
        vbar.pack(side=tk.RIGHT,  fill=tk.Y)                  # pack canvas after bars
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        vbar.config(command=self.canvas.yview)          # call on scroll move
        hbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=vbar.set)     # call on canvas move
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.config(height=Height, width=Width)  # viewable area size

    def clearTree(self):
        self.unbind_all('<Button-1>')
        self.canvas.delete('all')                       # clear events, drawing

    def drawTree(self, tree):
        self.clearTree()
        wrapper = self.wrapper
        levels, maxrow = self.planLevels(tree, wrapper)
        self.canvas.config(scrollregion=(                     # scrollable area
            0, 0, (Colsz * maxrow), (Rowsz * len(levels)) ))  # upleft, lowright
        self.drawLevels(levels, maxrow, wrapper)

    def planLevels(self, root, wrap):
        levels = []
        maxrow = 0                                       # traverse tree to 
        currlevel = [(root, None)]                       # layout rows, cols
        while currlevel:
            levels.append(currlevel)
            size = len(currlevel)
            if size > maxrow: maxrow = size
            nextlevel = []
            for node, parent in currlevel:
                if node != None:
                    children = wrap.children(node)             # list of nodes
                    if not children:
                        nextlevel.append((None, None))         # leave a hole
                    else:
                        for child in children:
                            nextlevel.append((child, node))    # parent link
            currlevel = nextlevel
        return levels, maxrow

    def drawLevels(self, levels, maxrow, wrap):
        rowpos = 0                                         # draw tree per plan
        for level in levels:                               # set click handlers
            colinc = (maxrow * Colsz) / (len(level) + 1)   # levels is treenodes
            colpos = 0
            for (node, parent) in level:
                colpos = colpos + colinc
                if node != None:
                    text = wrap.label(node)
                    more = wrap.value(node)
                    if more: text = text + '=' + more
                    win = tk.Label(self.canvas, text=text, 
                                             bg=wrap.bg(node), bd=3, relief=tk.RAISED)
                    win.pack()
                    win.bind('<Button-1>', 
                        lambda e, n=node, handler=self.onClick: handler(e, n))
                    self.canvas.create_window(colpos, rowpos, anchor=tk.NW, 
                                window=win, width=Colsz*.5, height=Rowsz*.5)
                    if parent != None:
                        self.canvas.create_line(
                            parent.__colpos + Colsz*.25,    # from x-y, to x-y
                            parent.__rowpos + Rowsz*.5,
                            colpos + Colsz*.25, rowpos, arrow='last', width=1)
                    node.__rowpos = rowpos
                    node.__colpos = colpos          # mark node, private attrs
            rowpos = rowpos + Rowsz

    def onClick(self, event, node):
        wrap  = self.wrapper
        wrap.onClick(node)      # run tree action if any
        
                      

    def setTreeType(self, newTreeWrapper):          # change tree type drawn
        if self.wrapper != newTreeWrapper:          # effective on next draw
            self.wrapper = newTreeWrapper
            self.clearTree()                        # else old node, new wrapper
