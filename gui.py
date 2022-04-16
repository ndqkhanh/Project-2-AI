from cgitb import text
from email.policy import default
from multiprocessing.sharedctypes import Value
from turtle import textinput
import chessboard
import tkinter as tk
from cnf import *
from search import *
from pysat.solvers import Solver
class GUI:
    pieces = {}
    selected_piece = None
    focused = None
    images = {}
    color1 = "#DDB88C"
    color2 = "#A66D4F"
    highlightcolor = "khaki"
    rows = 8
    columns = 8
    dim_square = 64
    filename_cnf = None 
    filename_cnf_output = None
    filename_search = None
    searchSBS = None
    currentLevel = 1
    def __init__(self, parent, chessboard):
        self.chessboard = chessboard
        self.parent = parent
        # Adding Top Menu
        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_game)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        # Adding Frame
        self.btmfrm = tk.Frame(parent, height=64)
        self.info_label = tk.Label(self.btmfrm,
                                text="   Start  ",
                                fg=self.color2)
        self.info_label.pack(side=tk.LEFT, padx=0, pady=10)
        self.btmfrm.pack(fill="x", side=tk.BOTTOM)

        canvas_width = self.columns * self.dim_square
        canvas_height = self.rows * self.dim_square
        self.canvas = tk.Canvas(parent, width=canvas_width,
                               height=canvas_height)
        self.canvas.pack(padx=8, pady=8, ipadx=100)

        label = tk.Label(parent, text="GENERATE CNF CLAUSES", fg='red')
        label.place(x=canvas_width + 20, y=5)

        label = tk.Label(parent, text="CNF Clauses Filename Output:")
        label.place(x=canvas_width + 20, y=25)
        
        self.filename_cnf_output = tk.StringVar(parent, value='cnf.txt')
        input = tk.Entry(parent, textvariable=self.filename_cnf_output)
        input.place(x=canvas_width + 20, y=45)

        levelCNFClause = tk.Listbox(parent)
        levelCNFClause.insert(1, "Level 1")
        levelCNFClause.insert(2, "Level 2")
        levelCNFClause.select_set(0)
        levelCNFClause.bind('<<ListboxSelect>>', self.getLevelFromListBox) #Select click
        levelCNFClause.place(x=canvas_width + 20, y = 80, height=40, width=195)

        buttonGenerateCNFClause = tk.Button(parent, text="Generate", command=self.generateCNF)
        buttonGenerateCNFClause.place(x=canvas_width + 20, y=125, width=195)

        sectionY = 170
        label = tk.Label(parent, text="SOLVING", fg='red')
        label.place(x=canvas_width + 20, y=sectionY)

        label = tk.Label(parent, text="CNF Clauses Filename:")
        label.place(x=canvas_width + 20, y=sectionY+ 20)
        
        self.filename_cnf = tk.StringVar(parent, value='cnf.txt')
        input = tk.Entry(parent, textvariable=self.filename_cnf)
        input.place(x=canvas_width + 20, y=sectionY + 40)
       
        button = tk.Button(parent, text="Run", command=self.runSolveCNF)
        button.place(x=canvas_width + 20, y=sectionY + 70, width=195)


        sectionY = 280
        label = tk.Label(parent, text="SEARCH", fg='red')
        label.place(x=canvas_width + 20, y=sectionY)

        label = tk.Label(parent, text="File Input:")
        label.place(x=canvas_width + 20, y=sectionY+ 20)
        
        self.filename_search = tk.StringVar(parent, value='input.txt')
        input = tk.Entry(parent, textvariable=self.filename_search)
        input.place(x=canvas_width + 20, y=sectionY + 40)

        button = tk.Button(parent, text="Search", command=self.runSearch)
        button.place(x=canvas_width + 20, y=sectionY + 70, width=195)

        self.searchSBS = tk.Listbox(parent)
        # levelCNFClause.select_set(0)
        self.searchSBS.bind('<<ListboxSelect>>', self.drawTableFromData) #Select click
        self.searchSBS.place(x=canvas_width + 20, y = sectionY + 110, height=110, width=195)

        buttonPrev = tk.Button(parent, text="Prev", command=self.runPrevStep)
        buttonPrev.place(x=canvas_width + 20, y=sectionY + 220, width=80)

        buttonNext = tk.Button(parent, text="Next", command=self.runNextStep)
        buttonNext.place(x=canvas_width + 135, y=sectionY + 220, width=80)


        self.draw_board()
        # self.canvas.bind("<Button-1>", self.square_clicked)

    def drawTableFromData(self, event):
        widget = event.widget
        selection=widget.curselection()
        set = widget.get(selection[0])
        self.chessboard.show(set)
        self.draw_board()
        self.draw_pieces()

    def runPrevStep(self, event):
        selection = self.searchSBS.curselection()
        
        if selection:
            set = self.searchSBS.get(selection[0] - 1)
            self.chessboard.show(set)
            self.searchSBS.delete(selection[0])
            self.searchSBS.select_set(selection[0] - 1)
            self.draw_board()
            self.draw_pieces()
    
    def runNextStep(self):
        selection = self.searchSBS.curselection()
        if selection:
            set = self.searchSBS.get(selection[0] + 1)
            self.chessboard.show(set)
            self.searchSBS.delete(selection[0])
            self.searchSBS.select_set(selection[0] + 1)
            self.draw_board()
            self.draw_pieces()

    def runSearch(self):
        if  not(exists(self.filename_search.get())): 
            self.info_label.config(text="   File does not exist  ", fg='red')
            return
        fileHandle = open(self.filename_search.get(), 'r')
        fileHandle.readline() #read m
        list1 = [[int(j) for j in i.split()] for i in fileHandle]
        fileHandle.close()

        queenPos = convertToState(list1)
        self.Astar(queenPos)
        del queenPos

        # print(resultQueenPos.toString())

    def convertVerticalListToHorizontalList(self, list):
        ls = [-1,-1,-1,-1,-1,-1,-1,-1]
        for index, value in enumerate(list):
            if value == -1:
                continue
            ls[value] = index 
        return ls

    def Astar(self, initState):
        expandedState = {}
        frontier = [initState]#priority queue
        dem = 0
        while len(frontier) > 0:
            curState = frontier.pop(0)#print state to GUI here
            # print("curState.queensPos", curState.queensPos)
            queensPos = self.convertVerticalListToHorizontalList(curState.queensPos)
            set = ""
            l = 0
            for pos in queensPos:
                l+=1
                if l > 1:
                    set += "/"
                if pos == -1:
                    set += "8"
                else:
                    set += str(pos) + "q"
            dem += 1
            self.searchSBS.insert(dem, set)
            

            if curState.heuristic == 0:
                return curState

            if curState.mapDictionary not in expandedState.keys():
                expandedState[curState.mapDictionary] = True

                numOfQueenEachRowColumnDiagonal = getNumOfQueenEachRowColumnDiagonal(curState)
                falseCNFClause =  getFalseCNFClause(numOfQueenEachRowColumnDiagonal)

                for i in range(len(curState.queensPos)):#posistion each queen

                    j = curState.queensPos[i]# so i,j is the position of the queen

                    compress = numOfQueenEachRowColumnDiagonal# decreasing size of the variable name
                    if j != -1:
                        decreaseFalseClause = (-(compress[0][j] - 1) if compress[0][j] > 1 else 1 ) - ( compress[2][i - j + 7] - 1) - ( compress[3][i + j] - 1 )
                    else:
                        decreaseFalseClause = -1# there is no queen in this column, so if we add 1 queen to this column, the clause "or true" in this column become true => the false clause decrease by 1

                    for newj in range(8):# expanding states
                        if j != newj:

                            newPos = curState.queensPos.copy()
                            newPos[i] = newj
                            
                            increaseFalseClause = (compress[0][newj] if compress[0][newj] > 0 else -1) + compress[2][i - newj + 7] + compress[3][i + newj]
                            newHeurisistic = falseCNFClause + decreaseFalseClause + increaseFalseClause#read document to understand this

                            newState = State(newPos, accumulate = curState.accumulate + 1, heuristic = newHeurisistic)# generate new state

                            #print(falseCNFClause)
                            #print(newState.toString())
                            #print(newState.accumulate)
                            #print(newState.heuristic)
                            #print()
                            if newState.mapDictionary not in expandedState.keys():#not in expanded list
                                frontier.append(newState)
                #sort to become priority queue
                frontier.sort(key = heuristicPlusAccumulateState)

        return initState

    def getLevelFromListBox(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.currentLevel = index + 1

    def new_game(self):
        self.chessboard.show(chessboard.START_PATTERN)
        self.draw_board()
        self.draw_pieces()
        self.info_label.config(text="   Start  ", fg='red')

    def runSolveCNF(self):
        file = open(self.filename_cnf.get(), 'r')
        resultList = []
        for each in file:
            resultList.append([int(x) for x in each.strip().split("v")])
        file.close()
        s = Solver(bootstrap_with = resultList)

        isSatisfy = s.solve()
        result = s.get_model()
        if isSatisfy == True:
            set = ""
            for i in range(8):
                l = 0
                if i >= 1:
                    set += "/"
                for j in range(8):
                    if result[i*8 + j] > 0:
                        set += str(l) + "q"
                    else:
                        l += 1
            self.chessboard.show(set)
            self.draw_board()
            self.draw_pieces()
            self.info_label.config(text="   Solve CNF Clauses successfully ", fg='red')
        else:
            self.info_label.config(text="   There are conflicts in the CNF clauses ", fg='red')

    def generateCNF(self):
        file = open(self.filename_cnf_output.get(), 'w')
        resultList = createCNFSet(level=self.currentLevel)
        for clause in resultList:
            print(*clause, sep='v', file=file)
        file.close()
        self.info_label.config(text="   Generate CNF Clauses successfully.  ", fg='red')

    def shift(self, p1, p2):
        piece = self.chessboard[p1]
        try:
            dest_piece = self.chessboard[p2]
        except:
            dest_piece = None
        if dest_piece is None or dest_piece.color != piece.color:
            try:
                self.chessboard.shift(p1, p2)
            except chessboard.ChessError as error:
                self.info_label["text"] = error.__class__.__name__
         

    def focus(self, pos):
        try:
            piece = self.chessboard[pos]
        except:
            piece = None
        if piece is not None and (piece.color == self.chessboard.player_turn):
            self.selected_piece = (self.chessboard[pos], pos)
            self.focused = list(map(self.chessboard.num_notation,
                               (self.chessboard[pos].moves_available(pos))))

    def draw_board(self):
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.dim_square)
                y1 = ((7 - row) * self.dim_square)
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                if (self.focused is not None and (row, col) in self.focused):
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=self.highlightcolor,
                                                 tags="area")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                 tags="area")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.pieces[name] = (self.pieces[name][0], self.pieces[name][1])
            x0 = (self.pieces[name][1] * self.dim_square) + int(
                self.dim_square / 2)
            y0 = ((7 - self.pieces[name][0]) * self.dim_square) + int(
                self.dim_square / 2)
            self.canvas.coords(name, x0, y0)
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def draw_pieces(self):
        self.canvas.delete("occupied")
        for coord, piece in self.chessboard.items():
            x, y = self.chessboard.num_notation(coord)
            if piece is not None:
                filename = "pieces_image/%s%s.png" % (
                piece.shortname.lower(), piece.color)
                piecename = "%s%s%s" % (piece.shortname, x, y)
                if filename not in self.images:
                    self.images[filename] = tk.PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.images[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                x0 = (y * self.dim_square) + int(self.dim_square / 2)
                y0 = ((7 - x) * self.dim_square) + int(self.dim_square / 2)
                self.canvas.coords(piecename, x0, y0)


def main(chessboard):
    root = tk.Tk()
    root.title("Chess")
    gui = GUI(root, chessboard)
    gui.draw_board()
    gui.draw_pieces()
    root.mainloop()


if __name__ == "__main__":
    queenPositions = []
    game = chessboard.Board("8/8/8/8/8/8/8/8")
    main(game)
