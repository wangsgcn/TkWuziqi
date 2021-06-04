import tkinter as tk

class Gomoku:
    def __init__(self, master, game_size=19, algorithm="Greedy", switch=0, search_depth=1, player_first=True):
        self.master = master
        self.master.geometry("680x680")
        master.title("Gomoku/五子棋")
        self.buttonNewGame = tk.Button(self.master, text="New Game", command=self.new_game)
        self.buttonSetup = tk.Button(self.master, text="Setup Game", command=self.setup_game)
        self.buttonRestart = tk.Button(self.master, text="Restart Game", command=self.restart_game)

        # put a label at the bottom of the window as a status bar
        self.statusBar = tk.Label(self.master, text="status", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        # canvas is the container of the game board
        self.canvas = tk.Canvas(self.master)

        # redefine "resize" event
        self.master.bind("<Configure>", self.resize_window)
        self.master.bind("<Motion>", self.mouse_move)

        # game attributes, default values
        self.game_size = game_size
        self.algorithm = algorithm
        self.strategy_switch = switch
        self.search_depth = search_depth
        self.player_first = player_first

        # board
        self.X = [0 for n in range(self.game_size)]
        self.Y = [0 for n in range(self.game_size)]
        self.board = [[0 for r in range(self.game_size)] for c in range(self.game_size)]
        self.grid_size = 0

    def resize_window(self, event):
        x = self.master.winfo_width() / 5
        button_width = x * 0.8
        self.buttonSetup.place(x=(1.0 + 0.1) * x, y=10, width=button_width)
        self.buttonNewGame.place(x=(2.0 + 0.1) * x, y=10, width=button_width)
        self.buttonRestart.place(x=(3.0 + 0.1) * x, y=10, width=button_width)
        # determine the height and the width for canvas.
        # For the height, we have to take away the spaces for the buttons and the status bar
        height = self.master.winfo_height() - 80
        width = self.master.winfo_width()
        canvas_size = 0
        if height > width:
            canvas_size = width
        else:
            canvas_size = height
        self.canvas.config(width=canvas_size, heigh=canvas_size)
        self.setup_board()
        self.canvas.place(x=(width - canvas_size) / 2, y=40)

    def new_game(self):
        print("new game")

    def setup_game(self):
        print("setup game")

    def restart_game(self):
        print("restart game")

    def setup_board(self):
        grid_size = int(self.canvas.winfo_width() / (self.game_size + 1))
        padx = int((self.canvas.winfo_width() - (grid_size * (self.game_size + 1))) / 2)
        pady = int((self.canvas.winfo_height() - (grid_size * (self.game_size + 1))) / 2)
        for c in range(self.game_size):
            self.X[c] = (c + 1) * grid_size + padx
        for r in range(self.game_size):
            self.Y[r] = (r + 1) * grid_size + pady
        # clear canvas
        self.canvas.delete("all")
        # vertical lines
        for c in range(self.game_size):
            x1 = self.X[c]
            x2 = self.X[c]
            y1 = self.Y[0]
            y2 = self.Y[-1]
            # double width for borders
            if c == 0 or c == self.game_size - 1:
                self.canvas.create_line(x1, y1, x2, y2, width=2)
            else:
                self.canvas.create_line(x1, y1, x2, y2, width=1)
        # horizontal lines
        for r in range(self.game_size):
            x1 = self.X[0]
            x2 = self.X[-1]
            y1 = self.Y[r]
            y2 = self.Y[r]
            if r == 0 or r == self.game_size - 1:
                self.canvas.create_line(x1, y1, x2, y2, width=2)
            else:
                self.canvas.create_line(x1, y1, x2, y2, width=1)
        # save grid size
        self.grid_size = grid_size

    def mouse_move(self, event):
        x1 = event.x
        y1 = event.y
        self.statusBar.config(text="%d %d" %(x1, y1))
        #print(self.canvas.configure().keys())
        for r in range(self.game_size):
            for c in range(self.game_size):
                x2 = self.X[c]
                y2 = self.Y[r]
                d = self.dist(x1, y1, x2, y2)
                if d <= self.grid_size/3 and self.board[r][c] == 0:
                    self.canvas.config(cursor="hand2")
                    self.statusBar.config(text="row=%2d, col=%2d, x=%d, y=%d" %(r, c, x2, y2))
                else:
                    self.canvas.config(cursor="hand")
                    #self.statusBar.config(text="")


    def dist(self, x1, y1, x2, y2):
        d = ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**(1/2)
        return d

root = tk.Tk()
game = Gomoku(root)
root.mainloop()
