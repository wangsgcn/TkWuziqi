import tkinter as tk
from tkinter import ttk


class Setup:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x150")
        self.set_screen_center()

        lbl_gamesize = tk.Label(self.root, text="Game size:")
        self.var_game_size = tk.StringVar(self.root)
        self.var_game_size.set("19")
        sbx_gamesize = ttk.Spinbox(self.root, from_=15, to=25, increment=2, textvariable=self.var_game_size,
                                   command=self.spinbox_update)
        lbl_gamesize.grid(row=0, column=0)
        sbx_gamesize.grid(row=0, column=1, columnspan=2)
        lbl_algorithm = tk.Label(self.root, text="Algorithm:")
        cbx_algorithm = ttk.Combobox(self.root, values=["Greedy", "Minimax", "Minimax Alpha Beta", "Greedy Minimax"])
        cbx_algorithm.current(0)  # set default value
        lbl_algorithm.grid(row=1, column=0)
        cbx_algorithm.grid(row=1, column=1, columnspan=2)
        #
        self.var_first_move = tk.IntVar(self.root)
        self.var_first_move.set(1)
        lbl_firstmove = tk.Label(self.root, text = "First move:")
        rad_player = tk.Radiobutton(self.root, text="Player", variable=self.var_first_move, value=1,
                                    command=self.radobutton_selected)
        rad_computer = tk.Radiobutton(self.root, text="Computer", variable=self.var_first_move, value=2,
                                      command=self.radobutton_selected)

        lbl_firstmove.grid(row=2, column=0)
        rad_player.grid(row=2, column=1)
        rad_computer.grid(row=2, column=2)


        button_OK = tk.Button(self.root, text="OK", width=10, command=self.close_window)
        button_OK.grid(row=3, column=0, columnspan=3, sticky="S")

        self.root.rowconfigure(0, minsize=30)
        self.root.rowconfigure(1, minsize=30)
        self.root.rowconfigure(2, minsize=30)
        self.root.rowconfigure(3, minsize=50)

        # game default setting
        self.player_first = True
        self.game_size = 19
        self.algorithm = "Greedy"

    def set_screen_center(self):
        root_window_width = self.root.winfo_reqwidth()
        root_window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - root_window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - root_window_height / 2)
        self.root.geometry("+{}+{}".format(position_right, position_down))

    def radobutton_selected(self):
        if self.var_first_move.get() == 1:
            self.player_first = True
        if self.var_first_move.get() == 2:
            self.player_first = False

    def spinbox_update(self):
        print(type(self.var_game_size.get()))
        self.game_size = int(self.var_game_size.get())

    def close_window(self):
        self.root.destroy()
