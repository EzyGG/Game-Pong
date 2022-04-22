from tkinter import *
from random import choice

from ezyapi.contants import COLOR_EXP, COLOR_GP, COLOR_SPECIAL


class Scores(Tk):
    def __init__(self, wins: int, looses: int, special: str = None):
        super().__init__("err")
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'
        self.app_green = '#00FF00'
        self.app_special = '#FF00FF'

        self.title("Scores")
        self.geometry("400x350")
        self.configure(background=self.app_bg)
        try:
            self.iconbitmap("pong x32.ico")
        except Exception:
            pass

        self.wins, self.looses, self.special = wins, looses, special

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), text="Scores")
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, text=f"Calcul des scores pour {self.wins + self.looses} parties ({self.wins} victoires et {self.looses} défaites).")
        self.desc_label.pack(side=TOP)

        self.grid_frame = Frame(self, bg=self.app_bg)

        self.exp_title = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="EXP", width=7)
        self.gp_title = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="GP", width=7)
        self.wins_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Bonus de Victoire :")
        self.looses_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Malus de Défaites :")
        self.mul_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Multiplicateur d'EXP :")
        self.red_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Réducteur aléatoire de GP :")
        self.total_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Total des Récompenses :")

        self.v_wins_exp = wins ** 1.1 * 30
        self.v_wins_gp = wins ** 1.07 * 6
        self.v_looses_exp = -(looses ** 0.95 * 16)
        self.v_looses_gp = -(looses ** 0.85 * 5)
        self.v_mul = (1 + (wins - looses) / (2 * (wins + looses))) if wins + looses else 1
        self.v_red = float(choice("012345") + "." + choice("0123456789"))
        self.v_total_exp = (self.v_wins_exp + self.v_looses_exp) * self.v_mul
        self.v_total_gp = (self.v_wins_gp + self.v_looses_gp) * (1 - self.v_red / 100)
        self.v_total_exp = int(self.v_total_exp) if self.v_total_exp > 0 else 0
        self.v_total_gp = int(self.v_total_gp) if self.v_total_gp > 0 else 0

        self.wins_exp = Label(self.grid_frame, **self.nargs(self.v_wins_exp, suffix=" EXP"))
        self.wins_gp = Label(self.grid_frame, **self.nargs(self.v_wins_gp, suffix=" GP"))

        self.looses_exp = Label(self.grid_frame, **self.nargs(self.v_looses_exp, suffix=" EXP"))
        self.looses_gp = Label(self.grid_frame, **self.nargs(self.v_looses_gp, suffix=" GP"))

        self.mul_exp = Label(self.grid_frame, **self.sargs("* {:+.2f} EXP".format(self.v_mul), self.app_green if self.v_mul >= 0 else self.app_cross_color))
        self.red_gp = Label(self.grid_frame, **self.sargs(f"{-self.v_red}% GP", self.app_cross_color))

        self.total_exp = Label(self.grid_frame, **self.nargs(self.v_total_exp, suffix=" EXP", color=COLOR_EXP))
        self.total_gp = Label(self.grid_frame, **self.nargs(self.v_total_gp, suffix=" GP", color=COLOR_GP))
        if special:
            self.total_special = Label(self.grid_frame, **self.sargs(special))

        self.exp_title.grid(**self.gargs(0, 1, sticky=W, pady=10))
        self.gp_title.grid(**self.gargs(0, 2, sticky=W, pady=10))
        self.wins_label.grid(**self.gargs(1, 0, sticky=W))
        self.looses_label.grid(**self.gargs(2, 0, sticky=W))
        self.mul_label.grid(**self.gargs(3, 0, sticky=W))
        self.red_label.grid(**self.gargs(4, 0, sticky=W))
        Frame(self.grid_frame, height=3, bg=self.app_fg).grid(**self.gargs(5, 0, 1, 3, pady=10))
        self.total_label.grid(**self.gargs(6, 0, sticky=W))

        self.wins_exp.grid(**self.gargs(1, 1))
        self.wins_gp.grid(**self.gargs(1, 2))
        self.looses_exp.grid(**self.gargs(2, 1))
        self.looses_gp.grid(**self.gargs(2, 2))
        self.mul_exp.grid(**self.gargs(3, 1))
        self.red_gp.grid(**self.gargs(4, 2))
        self.total_exp.grid(**self.gargs(6, 1))
        self.total_gp.grid(**self.gargs(6, 2))
        if special:
            self.total_special.grid(**self.gargs(7, 1, 1, 2, sticky="e"))

        self.grid_frame.pack(side=TOP, pady=10)

        self.cont_frame = Frame(self, bg=self.app_green)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_green, fg=self.app_green,
                               highlightcolor=self.app_green, font=("", 12, "bold"), text="Quitter",
                               command=self.destroy)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=BOTTOM, pady=5)

        self.bind("<Return>", lambda x: self.destroy())
        self.cont_btn.focus_set()

    def start(self):
        self.mainloop()

    def nargs(self, exp: int | float, prefix: str = None, suffix: str = None, color: str = None):  # n args
        return {"bg": self.app_bg, "fg": color if color else (self.app_green if exp >= 0 else self.app_cross_color),
                "text": (f"{prefix}" if prefix else "") + "{:+}".format(int(exp)) + (f"{suffix}" if suffix else "")}

    def sargs(self, special: str, color: str = None):  # special args
        return {"bg": self.app_bg, "fg": color if color else COLOR_SPECIAL, "text": str(special)}

    def gargs(self, row, column, rowspan=1, columnspan=1, sticky=NE+SW, padx=15, pady=1):  # grid args
        return {"row": row, "column": column, "rowspan": rowspan, "columnspan": columnspan, "padx": padx, "pady": pady,
                "ipadx": 5, "sticky": sticky}