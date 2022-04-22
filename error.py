from tkinter import *


class Error(Tk):
    def __init__(self, name: str, desc: str):
        super().__init__("err")
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'

        self.title("Erreur")
        # self.resizable(False, False)
        self.geometry("300x300")
        self.configure(background=self.app_bg)
        try:
            self.iconbitmap("pong x32.ico")
        except Exception:
            pass

        self.name, self.desc = name, desc

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), wraplengt=300, text=name)
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, wraplengt=300, text=desc)
        self.desc_label.pack(side=TOP, pady=10)

        self.opt_frame = Frame(self, bg=self.app_bg)
        self.cont_frame = Frame(self.opt_frame, bg=self.app_circle_color)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_circle_color, fg=self.app_circle_color,
                               highlightcolor=self.app_circle_color, font=("", 12, "bold"), text="Continuer !",
                               command=self.cont_cmd)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=LEFT, padx=5)
        self.quit_frame = Frame(self.opt_frame, bg=self.app_cross_color)
        self.quit_btn = Button(self.quit_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_cross_color, fg=self.app_cross_color,
                               highlightcolor=self.app_cross_color, font=("", 12, "bold"), text="Quitter.",
                               command=self.quit_cmd)
        self.quit_btn.pack(padx=1, pady=1)
        self.quit_frame.pack(side=RIGHT, padx=5)
        self.opt_frame.pack(side=BOTTOM, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.quit_cmd)
        self.bind("<Configure>", self.event_handler)
        self.bind("<Return>", self.on_return)
        self.quit_btn.focus_set()

        self.mainloop()

    def on_return(self, event=None):
        if self.focus_get() == self.cont_btn:
            self.cont_cmd()
        elif self.focus_get() == self.quit_btn:
            self.quit_cmd()

    def cont_cmd(self, event=None):
        self.destroy()

    def quit_cmd(self, event=None):
        try:
            sys.exit(1)
        except NameError:
            quit(1)

    def event_handler(self, event=None):
        new_wrap = int(self.winfo_geometry().split("x")[0]) - 5
        self.name_label.config(wraplengt=new_wrap)
        self.desc_label.config(wraplengt=new_wrap)