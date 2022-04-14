from cgitb import text
from email.policy import default
from multiprocessing.sharedctypes import Value
from turtle import textinput
import chessboard
import tkinter as tk
import random
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
        self.draw_board()
        # self.canvas.bind("<Button-1>", self.square_clicked)

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

def rowAndcolumnConditions():
    #OrTrue condition Ex: a v b
    list = []
    for i in range(8):#row and column
        row_OrTrueCondition = []
        column_OrTrueCondition = []

        for j in range(8):
            row_OrTrueCondition.append(i*8 + j + 1)
            column_OrTrueCondition.append(i + j*8 + 1)
        list.append(row_OrTrueCondition)
        list.append(column_OrTrueCondition)
    return list

def pos_To_id(x, y):
    return x * 8 + y + 1

def id_To_pos(v):
    clause = []
    tmp = int((v - 1) / 8)
    clause.append(tmp)
    clause.append(v - 1 - tmp * 8)
    return clause

def restrictions_Of_pos(x, y):
    result = []

    currentV = pos_To_id(x, y)

    # column+
    xcol = x + 1
    while xcol >= 0 and xcol < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xcol, y))
        result.append(clause)
        xcol += 1
    # column-
    xcol = x - 1
    while xcol >= 0 and xcol < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xcol, y))
        result.append(clause)
        xcol -= 1


    # row+
    yrow = y + 1
    while yrow >= 0 and yrow < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(x, yrow))
        result.append(clause)
        yrow += 1
    # row-
    yrow = y - 1
    while yrow >= 0 and yrow < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(x, yrow))
        result.append(clause)
        yrow -= 1


    # major diag+
    xdiag = x + 1
    ydiag = y + 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag += 1
        xdiag += 1
    # major diag-
    xdiag = x - 1
    ydiag = y - 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag -= 1
        xdiag -= 1


    # minor diag+
    xdiag = x - 1
    ydiag = y + 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag += 1
        xdiag -= 1
    # minor diag-
    xdiag = x + 1
    ydiag = y - 1
    while xdiag >= 0 and xdiag < 8 and ydiag >= 0 and ydiag < 8:
        clause=[]
        clause.append(-currentV)
        clause.append(-pos_To_id(xdiag, ydiag))
        result.append(clause)
        ydiag -= 1
        xdiag += 1

    return result


def solveCNFClauses(resultList):
    s = Solver(bootstrap_with = resultList)

    isSatisfy = s.solve()
    result = s.get_model()

    if isSatisfy == True:
        print("\nChessboard solution found:\n")
        for i in range(8):
            for j in range(8):
                if result[i*8 + j] > 0:
                    print("Q", end = " ")
                else:
                    print(".", end = " ")
            print("")
        print("\nResult:\n")
        print(s.get_model())
    else:
        print("There are conflicts in the CNF clauses")


def createCNFSet(level = 1):
    isSatisfy = False

    while True:
        if isSatisfy == True:
            break

        # return result
        resultList = []

        #return postitions of queen place consecutively
        Positions = []

        # Board from 1 to 64 for level == 2
        board = list(range(1, 65))

        # count number of queens have been placed
        count = 0

        # set of 8 columns to pick for level 1
        if level == 1:
            columnpicks = []
            for i in range(8):
                column_OrTrueCondition = []
                for j in range(8):
                    column_OrTrueCondition.append(i + j*8 + 1)
                columnpicks.append(column_OrTrueCondition)

        for item in rowAndcolumnConditions():
            resultList.append(item)

        # level == 1
        if level == 1:
            for col in columnpicks:
                if len(col) == 0: break
                pos = random.choice(col)
                col.remove(pos)

                for i in restrictions_Of_pos(id_To_pos(pos)[0], id_To_pos(pos)[1]):
                    resultList.append(i)

                for i in columnpicks:
                    for j in resultList:
                        for t in j:
                            if t < 0:
                                if -t in i:
                                    i.remove(-t)
                Positions.append(pos)
                count += 1
        else: # level == 2
            while count < 8:
                if len(board) == 0: break
                pos = random.choice(board)
                board.remove(pos)

                for i in restrictions_Of_pos(id_To_pos(pos)[0], id_To_pos(pos)[1]):
                    resultList.append(i)

                # for i in columnpicks:
                for j in resultList:
                    for t in j:
                        if t < 0:
                            if -t in board:
                                board.remove(-t)
                Positions.append(pos)
                count += 1

        # Make positions of queen placed to true
        for i in Positions:
            resultList.append([i])

        # check if we successfully place 8 queens in board
        if count >= 8: isSatisfy = True

    return resultList


if __name__ == "__main__":
    queenPositions = []
    game = chessboard.Board("8/8/8/8/8/8/8/8")
    main(game)
