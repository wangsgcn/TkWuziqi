import tkinter as tk
from Setup import Setup

class Gomoku:
    def __init__(self, root, game_size=19, algorithm="Greedy", switch=0, search_depth=1, player_first=True):
        self.master = root
        self.set_screen_center()

        self.master.title("Gomoku/五子棋")
        self.buttonNewGame = tk.Button(self.master, text="New Game",     command=self.new_game)
        self.buttonSetup   = tk.Button(self.master, text="Setup Game",   command=self.setup_game)
        self.buttonRestart = tk.Button(self.master, text="Restart Game", command=self.restart_game)

        # put a label at the bottom of the window as a status bar
        self.statusBar = tk.Label(self.master, text="status", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        # canvas is the container of the game board
        self.canvas = tk.Canvas(self.master, cursor="hand2")

        # redefine "resize" event
        self.master.bind("<Configure>", self.resize_window)
        self.master.bind("<Motion>", self.mouse_move)
        self.master.bind("<Button-1>", self.mouse_click)
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
        self.board_padx = 0
        self.board_pady = 0

        self.game_running = False

    def set_screen_center(self):
        # initial window size
        window_width = 680
        window_height = 680

        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)

        self.master.geometry("680x680+{}+{}".format(position_right, position_down))

    def resize_window(self, event):
        # when game is running, player cannot chang board size.
        if self.game_running == True:
            return
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
        root = tk.Toplevel(self.master)
        setup = Setup(root)
        setup.show()
        #print(a, b)
        self.game_size       = setup.game_size
        self.algorithm       = setup.algorithm
        self.strategy_switch = setup.strategy_scale
        self.player_first    = setup.player_first
        self.setup_board()

    def restart_game(self):
        print("restart game")

    def setup_board(self):
        self.X = [0 for n in range(self.game_size)]
        self.Y = [0 for n in range(self.game_size)]
        self.board = [[0 for r in range(self.game_size)] for c in range(self.game_size)]
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

        # draw row/column labels
        for r in range(self.game_size):
            x1 = self.X[0] -15
            x2 = self.X[-1]+15
            y  = self.Y[r]-2
            text = "%2d"%r
            self.canvas.create_text(x1, y, text=text, fill="blue")
            self.canvas.create_text(x2, y, text=text, fill="blue")
        for c in range(self.game_size):
            x = self.X[c]
            y1 = self.Y[0] - 12
            y2 = self.Y[-1] + 12
            text = "%2d" %c
            self.canvas.create_text(x, y1, text=text, fill="blue")
            self.canvas.create_text(x, y2, text=text, fill="blue")
        # save grid size
        self.grid_size = grid_size
        self.board_padx = padx
        self.board_pady = pady

    def mouse_move(self, event):
        caller = event.widget
        mouse_x = event.x
        mouse_y = event.y

        # upper left corner of the grid where the mouse hover over.
        ulc_row = int((mouse_y-self.board_pady-self.grid_size)/self.grid_size)
        ulc_col = int((mouse_x-self.board_padx-self.grid_size)/self.grid_size)
        # if the mouse is over the canvas
        if type(caller) == type(self.canvas):
            for r in [ulc_row, ulc_row+1]:
                for c in [ulc_col, ulc_col+1]:
                    if 0<=r<self.game_size and 0<=c<self.game_size:
                        x2 = self.X[c]
                        y2 = self.Y[r]
                        d = self.dist(mouse_x, mouse_y, x2, y2)
                        if d <= self.grid_size/3 and self.board[r][c] == 0:
                            self.statusBar.config(text="row=%2d, col=%2d, you can put a stone here." %(r, c))

    def mouse_click(self, event):
        caller = event.widget
        mouse_x = event.x
        mouse_y = event.y

        # upper left corner of the grid where the mouse hover over.
        ulc_row = int((mouse_y-self.board_pady-self.grid_size)/self.grid_size)
        ulc_col = int((mouse_x-self.board_padx-self.grid_size)/self.grid_size)
        # if the mouse is over the canvas
        if type(caller) == type(self.canvas):
            for r in [ulc_row, ulc_row+1]:
                for c in [ulc_col, ulc_col+1]:
                    if 0<=r<self.game_size and 0<=c<self.game_size:
                        x2 = self.X[c]
                        y2 = self.Y[r]
                        d = self.dist(mouse_x, mouse_y, x2, y2)
                        if d <= self.grid_size/3 and self.board[r][c] == 0:
                            r = int(self.grid_size/3)
                            self.canvas.create_oval(x2-r, y2-r, x2+r, y2+r, fill="black")

    def dist(self, x1, y1, x2, y2):
        d = ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**(1/2)
        return d

root = tk.Tk()
game = Gomoku(root)
root.mainloop()
