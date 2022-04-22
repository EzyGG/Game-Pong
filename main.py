from threading import Thread
from time import sleep
from tkinter import *
from random import shuffle

import ezyapi.game_manager as manager
from ezyapi.mysql_connection import DatabaseConnexionError
from ezyapi.sessions import UserNotFoundException
from ezyapi.UUID import UUID

import pygame
pygame.init()

from game import Pong
from error import Error
from config import Config


GAME_UUID = UUID.parseUUID("564807d5-ce5f-bae8-4167-c41efff92dc5")
GAME_VERSION = manager.GameVersion("v1.0")


class Update(Thread):
    def __init__(self, from_version: manager.GameVersion = manager.GameVersion(),
                 to_version: manager.GameVersion = manager.GameVersion()):
        super().__init__()
        self.running = True

        self.from_version, self.to_version = from_version, to_version
        self.tk: Tk = None

    def stop(self):
        self.running = False
        if self.tk:
            self.tk.destroy()
        raise Exception("Thread Ending.")

    def run(self):
        self.tk = Tk("update")
        self.app_bg = 'black'
        self.app_fg = 'white'

        self.tk.title("Mise-à-Jour")
        self.tk.geometry("375x320")
        self.tk.configure(background=self.app_bg)
        try:
            self.tk.iconbitmap("pong x32.ico")
        except Exception:
            pass

        self.magic_frame = Frame(self.tk)
        self.internal_frame = Frame(self.magic_frame, bg=self.app_bg)

        self.magic_frame.pack_propagate(0)
        self.internal_frame.pack_propagate(0)

        self.title_frame = Frame(self.internal_frame, bg=self.app_bg)
        self.name_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), text="Mise-à-Jour")
        self.name_label.pack(side=TOP)

        self.version_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 12, "bold"), text=f"{self.from_version}  →  {self.to_version}")
        self.version_label.pack(side=TOP)
        self.title_frame.pack(side=TOP, fill=X, expand=True, pady=20, padx=20)

        self.desc_label = Label(self.internal_frame, bg=self.app_bg, fg=self.app_fg, text="Nous remettons à jour votre jeu pour vous assurer une experience sans égale. Actuellement, nous transferont et compilons les nouveaux fichiers depuis la base de donnée. Si le jeu est important ou que votre connexion est mauvaise, l'action peut durer plusieurs minutes... Revenez un peu plus tard. (Temps éstimé: 5sec)")
        self.desc_label.pack(side=BOTTOM, pady=20, padx=20)

        self.internal_frame.pack(fill=BOTH, expand=True, padx=7, pady=7)
        self.magic_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        self.tk.protocol("WM_DELETE_WINDOW", self.quit)
        self.tk.bind("<Configure>", self.on_configure)

        while self.running:
            self.loop()
            self.tk.mainloop()

    def quit(self):
        if not self.running:
            self.stop()

    def on_configure(self, e=None):
        wrap = int(self.tk.winfo_geometry().split("x")[0]) - 114  # 114 -> padx: 2*30 + 2*7 + 2*20
        self.name_label.config(wraplengt=wrap)
        self.desc_label.config(wraplengt=wrap)

    def loop(self, infinite=True, random=True):
        path = ["000", "100", "110", "010", "011", "001", "101", "111"]
        color = [0, 0, 0]
        while self.running:
            temp_path = path[:]
            if random:
                shuffle(temp_path)
            for p in temp_path:
                run = True
                while run and self.running:
                    run = False
                    for i in range(len(color)):
                        if p[i] == "0" and color[i] != 0:
                            color[i] -= 2 if color[i] - 2 > 0 else 1
                            run = True
                        elif p[i] == "1" and color[i] != 255:
                            color[i] += 2 if color[i] + 2 < 256 else 1
                            run = True
                    str_color = "#{color[0]:0>2X}{color[1]:0>2X}{color[2]:0>2X}".format(color=color)
                    self.magic_frame.configure(bg=str_color)
                    self.tk.update()
                    sleep(0.0001)
            if not infinite:
                break


CONTINUE = "\n\nIf you Continue, you will not be able to get rewards and update the ranking."
try:
    try:
        manager.setup(GAME_UUID, GAME_VERSION, __update=False)
    except manager.UserParameterExpected as e:
        Error("UserParameterExpected",
              str(e) + "\nYou must run the game from the Launcher to avoid this error." + CONTINUE)
    except UserNotFoundException as e:
        Error("UserNotFoundException", str(e) + "\nThe user information given does not match with any user." + CONTINUE)

    if not manager.updated():
        u = Update(manager.__current_version, manager.__game_info.version)
        u.start()
        manager.update()
        try:
            u.stop()
        except Exception:
            pass
except DatabaseConnexionError as e:
    Error("DatabaseConnexionError",
          str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Retry Later." + CONTINUE)


restart = True
while restart:
    try:
        Pong(Config()).start_loop()
        restart = False
    except TclError:
        print("Dommage...")
