import tkinter as tk
from tkinter import ttk


class Setup:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.geometry("300x200")
        self.toplevel.focus_set()
        self.set_screen_center()

        lbl_gamesize = tk.Label(self.toplevel, text="Game size:")
        self.var_game_size = tk.StringVar(self.toplevel)
        self.var_game_size.set("19")
        sbx_gamesize = ttk.Spinbox(self.toplevel, from_=15, to=25, increment=2, textvariable=self.var_game_size,
                                   command=self.spinbox_update)
        lbl_gamesize.grid(row=0, column=0)
        sbx_gamesize.grid(row=0, column=1, columnspan=2)
        lbl_algorithm = tk.Label(self.toplevel, text="Algorithm:")
        cbx_algorithm = ttk.Combobox(self.toplevel, values=["Greedy", "Minimax", "Minimax Alpha Beta", "Greedy Minimax"])
        cbx_algorithm.current(0)  # set default value
        lbl_algorithm.grid(row=1, column=0)
        cbx_algorithm.grid(row=1, column=1, columnspan=2)
        #
        self.var_first_move = tk.IntVar(self.toplevel)
        self.var_first_move.set(1)
        lbl_firstmove = tk.Label(self.toplevel, text = "First move:")
        rad_player = tk.Radiobutton(self.toplevel, text="Player", variable=self.var_first_move, value=1,
                                    command=self.radobutton_selected)
        rad_computer = tk.Radiobutton(self.toplevel, text="Computer", variable=self.var_first_move, value=2,
                                      command=self.radobutton_selected)

        lbl_firstmove.grid(row=2, column=0)
        rad_player.grid(row=2, column=1)
        rad_computer.grid(row=2, column=2)

        self.var_scale = tk.IntVar(self.toplevel)
        sca_strategy = tk.Scale(self.toplevel, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.var_scale, command=self.scale_change)
        lbl_strategy = tk.Label(self.toplevel, text="A/D scale:")

        lbl_strategy.grid(row=3, column=0)
        sca_strategy.grid(row=3, column=1, columnspan=2, sticky="NSEW")

        button_OK = tk.Button(self.toplevel, text="OK", width=10, command=self.close_window)
        button_OK.grid(row=4, column=0, columnspan=3)

        self.toplevel.rowconfigure(0, minsize=25, weight=1)
        self.toplevel.rowconfigure(1, minsize=25, weight=1)
        self.toplevel.rowconfigure(2, minsize=25, weight=1)
        self.toplevel.rowconfigure(3, minsize=25, weight=1)
        self.toplevel.rowconfigure(4, minsize=50, weight=1)

        self.toplevel.columnconfigure(0, weight=1)
        self.toplevel.columnconfigure(1, weight=1)
        self.toplevel.columnconfigure(2, weight=1)

        # game default setting
        self.player_first = True
        self.game_size = 19
        self.algorithm = "Greedy"
        self.strategy_scale = 0

    def set_screen_center(self):
        toplevel_window_width = self.toplevel.winfo_reqwidth()
        toplevel_window_height = self.toplevel.winfo_reqheight()
        position_right = int(self.toplevel.winfo_screenwidth() / 2 - toplevel_window_width / 2)
        position_down = int(self.toplevel.winfo_screenheight() / 2 - toplevel_window_height / 2)
        self.toplevel.geometry("+{}+{}".format(position_right, position_down))

    def radobutton_selected(self):
        if self.var_first_move.get() == 1:
            self.player_first = True
        if self.var_first_move.get() == 2:
            self.player_first = False

    def spinbox_update(self):
        self.game_size = int(self.var_game_size.get())


    def close_window(self):
        self.toplevel.destroy()

    def scale_change(self, event):
        self.strategy_scale = self.var_scale.get()


    def show(self):
        # make the setup dialog to be a model dialog
        # Modal dialog boxes, which require the user to respond before continuing the program
        # Modeless dialog boxes, which stay on the screen and are available for use at any time but permit other user activities
        # A modal dialog box doesn’t allow the user to access the parent window while the dialog is open – it must be dealt with and closed before continuing. A modeless dialog can be open in the background.
        # When a modal dialog is open you cannot interact with anything else than this modal dialog inside your program, as long as the modal dialog is open. Most dialogs are modal, for example the File-Save As dialogs are modal.

        self.toplevel.grab_set()
        self.toplevel.wait_window()
