import webbrowser
import threading
import getpass
import atexit
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController, Listener
import random
import time
from pyfiglet import Figlet
import os
import cv2 as cv
import pyautogui
import numpy as np
import ctypes
from termcolor import colored
import tkinter as tk
from tkinter import RAISED, SUNKEN, GROOVE, messagebox, filedialog
from PIL import Image, ImageTk
import csv
import pygame
import configparser

pygame.mixer.init()
config = configparser.ConfigParser()



class App():
    def __init__(self):
        self.deaths = 0
        self.losses = "Not yet implemented. Sorry!"
        self.wins = "Not yet implemented. Sorry!"

        self.light = ["silver", "green", "white"] #Background, Buttons, Header
        self.dark = ["#2F3336", "#469FFC", "white"]
        self.darker = ["#101010", "#1E90FF", "white"]
        self.black = ["black", "black", "#00FF00"]
        self.ocean = ["#001F3F", "#0074D9", "#1E90FF"]
        self.retro = ["#002B36", "#FF00FF", "#00FF00"]
        self.cyberpunk = ["#01002A", "#FF007F", "#04D8E6"]
        self.gaming = ["#101010", "#32CD32", "#00FF00"]

        self.theme = self.get_theme()

        sensitivity = self.get_sense()
        self.sensitivity = sensitivity
        time = self.get_time()
        self.time = time
        self.root = tk.Tk()
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.title("AFK Bot")
        self.root.config(bg=self.theme[0])

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.theme_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Themes", menu=self.theme_menu)
        self.theme_menu.add_command(label="Light Mode", command=lambda :self.update_theme("light"))
        self.theme_menu.add_command(label="Dark Mode", command=lambda :self.update_theme("dark"))
        self.theme_menu.add_command(label="Darker Mode", command=lambda :self.update_theme("darker"))
        self.theme_menu.add_command(label="Black", command=lambda :self.update_theme("black"))
        self.theme_menu.add_command(label="Ocean", command=lambda :self.update_theme("ocean"))
        self.theme_menu.add_command(label="Retro", command=lambda :self.update_theme("retro"))
        self.theme_menu.add_command(label="Cyberpunk", command=lambda :self.update_theme("cyberpunk"))
        self.theme_menu.add_command(label="Gaming", command=lambda :self.update_theme("gaming"))

        self.stats_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Stats", menu=self.stats_menu)
        self.stats_menu.add_command(label="Session Stats", command=self.show_stats)
        self.stats_menu.add_command(label="Total Stats", command=self.total_stats) 

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Tutorial", command=lambda :webbrowser.open("https://youtu.be/s1o2fyUEcIo?si=pykCorFvCZ8tSj_C"))

        self.donate_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Donate", menu=self.donate_menu)
        self.donate_menu.add_command(label="Cash App", command=lambda :webbrowser.open("https://cash.app/$CadenWarren42"))


        six_image = Image.open("Icons\\6.ico")
        six_img_tk = ImageTk.PhotoImage(six_image)
        self.six_icon = six_img_tk
        self.root.iconphoto(True, self.six_icon)

        gear_image = Image.open("Assets\\gear.png")
        gear_image_small = gear_image.resize((50, 50))
        self.gear_img_tk = ImageTk.PhotoImage(gear_image_small)
        self.gear_icon = self.gear_img_tk

        self.top_frame = tk.Frame(self.root, bg=self.theme[0])
        self.top_frame.columnconfigure(0, weight = 1)
        self.top_frame.columnconfigure(1, weight = 1)
        self.top_frame.columnconfigure(2, weight = 1)

        self.gear_widget = tk.Label(self.top_frame, image=self.gear_icon, bg=self.theme[0])
        self.gear_widget.bind("<Button-1>", self.settings)
        self.gear_widget.bind("<Enter>", self.hover_effect)
        self.gear_widget.bind("<Leave>", self.transparent_leave)
        self.gear_widget.grid(row=0, column=0, sticky="nw")


        # self.shadow_label = tk.Label(
        #     self.root,
        #     text="AFK BOT",
        #     font=("Arial", 32, "bold"),
        #     fg="black",
        #     bg=self.theme[1]
        # )
        # self.shadow_label.place(x=380, y=65)

        self.header = tk.Label(self.top_frame, text="AFK Bot", font=("Bebas Neue Regular", 48, "bold"), fg=self.theme[2], bg=self.theme[1], bd=5, relief=GROOVE, highlightthickness=5, highlightbackground="black")
        self.header.grid(row=0, column=1, pady=10, ipadx=20)

        self.creator = tk.Button(self.top_frame, text="Created By - Caden Warren", font=("Calibri", 16, "bold"), fg="white", bg=self.theme[1], relief=GROOVE, bd=4, highlightthickness=5, highlightbackground="black", command=lambda :webbrowser.open("https://linktr.ee/CainKEA"))
        self.creator.bind("<Button-1>", self.click_sound)
        self.creator.bind("<Enter>", self.hover_effect)
        self.creator.bind("<Leave>", self.leave_effect)
        self.creator.grid(row=1, column=1, pady=5, ipadx=5)

        self.top_frame.pack(pady=30)


        self.mouse_var = tk.BooleanVar()
        self.mouse_check = tk.Checkbutton(self.root, text="Character turns in game", font=("Helvetica", 16), fg="white", bg=self.theme[0], variable=self.mouse_var, command=self.want_mouse)
        self.mouse_check.bind("<Button-1>", self.check_sound)
        self.mouse_check.bind("<Enter>", self.hover_effect)
        self.mouse_check.bind("<Leave>", self.transparent_leave)
        self.mouse_check.pack()


        self.bottom_frame = tk.Frame(self.root, bg=self.theme[0], relief=SUNKEN, bd=55, highlightbackground="black", highlightthickness=2)
        self.bottom_frame.columnconfigure(0, weight=1) 
        self.bottom_frame.columnconfigure(1, weight=1) 

        self.action_frame = tk.Frame(self.bottom_frame, bg=self.theme[0], relief=SUNKEN, bd=15, highlightbackground="black", highlightthickness=2)
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)

        self.start_btn = tk.Button(self.action_frame, text="START", font=("BASE", 16), fg="white", bg=self.theme[1], command=self.start_bot, relief=RAISED, bd=5)
        self.start_btn.bind("<Button-1>", self.click_sound)
        self.start_btn.bind("<Enter>", self.hover_effect)
        self.start_btn.bind("<Leave>", self.leave_effect)
        self.start_btn.grid(row=0, columnspan=2, ipadx=80, ipady=25) 

        self.resume_btn = tk.Button(self.action_frame, text="RESUME\n(F8)", font=("BASE", 16), fg="white", bg=self.theme[1], command=self.resume_bot, state="disabled", relief=RAISED, bd=5)
        self.resume_btn.bind("<Button-1>", self.click_sound)
        self.resume_btn.bind("<Enter>", self.hover_effect)
        self.resume_btn.bind("<Leave>", self.leave_effect)
        self.resume_btn.grid(row=1, column=0, ipady=5, ipadx=10) 

        self.pause_btn = tk.Button(self.action_frame, text="PAUSE\n(F7)", font=("BASE", 16), fg="white", bg=self.theme[1], command=self.pause_bot, state="disabled", relief=RAISED, bd=5)
        self.pause_btn.bind("<Button-1>", self.click_sound)
        self.pause_btn.bind("<Enter>", self.hover_effect)
        self.pause_btn.bind("<Leave>", self.leave_effect)
        self.pause_btn.grid(row=1, column=1, ipady=5, ipadx=10, pady=2)  

        self.action_frame.grid(row=0, column=0, ipady=8)

        self.console_frame = tk.Frame(self.bottom_frame, bg="#393939", relief=SUNKEN, bd=15, highlightbackground="black", highlightthickness=2)
        self.console_frame.columnconfigure(0, weight=1)
        self.console = tk.Text(self.console_frame, height=12, width=50, wrap=tk.WORD)
        self.console.grid(row=0, column=0, sticky="nsew")

        self.console_scrollbar = tk.Scrollbar(self.console_frame, orient=tk.VERTICAL, command=self.console.yview)
        self.console_scrollbar.grid(row=0, column=1, sticky="ns")

        self.console.config(yscrollcommand=self.console_scrollbar.set)

        self.console_frame.grid(row=0, column=1)

        self.bottom_frame.pack()
        

        self.root.protocol("WM_DELETE_WINDOW", self.app_clean)

    def start_gui(self):
        self.root.mainloop()

    def settings(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\settings sound.mp3")
        pygame.mixer.music.play()
        if hasattr(self, 'settings_popup') and self.settings_popup.winfo_exists():
            self.settings_popup.lift()
            self.settings_popup.focus_force()
            return
        self.settings_popup = tk.Toplevel(self.root)
        self.settings_popup.geometry("500x375")
        self.settings_popup.title("Settings")
        self.settings_popup.config(bg=self.theme[0])
        self.settings_popup.resizable(False, False)


        self.settings_frame = tk.Frame(self.settings_popup, bg=self.theme[0])
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.columnconfigure(1, weight=10)
        self.settings_frame.columnconfigure(2, weight=10)
        self.settings_frame.columnconfigure(3, weight=10)

        self.status_label = tk.Label(
            self.settings_frame,
            font=("Helvetica", 18, "bold"),
            bg=self.theme[0]
            )
        self.status_label.grid(row=0, columnspan=4, pady=10, sticky="ew")


        self.showreg_btn = tk.Button(
            self.settings_frame, 
            text="Show Detection Regions",
            font=("Arial", 10, "bold"),
            fg="white",
            bg=self.theme[1],
            relief=RAISED,
            bd=5,
            command=self.show_regions
            )
        self.showreg_btn.bind("<Button-1>", self.click_sound)
        self.showreg_btn.bind("<Enter>", self.hover_effect)
        self.showreg_btn.bind("<Leave>", self.leave_effect)
        self.showreg_btn.grid(row=1, column=0, padx=20)

        self.close_button = tk.Button(self.settings_frame, text="Close", font=("Arial", 14), fg="white", bg=self.theme[1], relief=RAISED, command=lambda :self.settings_popup.destroy())
        self.close_button.bind("<Button-1>", self.close_sound)
        self.close_button.bind("<Enter>", self.hover_effect)
        self.close_button.bind("<Leave>", self.leave_effect)
        self.close_button.grid(row=5, column=1, pady=20, sticky="sw")

        self.sensitivity_var = tk.IntVar()

        self.sensitivity_scale = tk.Scale(
            self.settings_frame,
            from_=200, to=0,
            length=200,
            font=("Luckiest Guy", 12),
            tickinterval=100,
            fg="white",
            bg="#2F2F2F",
            bd=5,
            highlightbackground=self.theme[1],  # Border color when not focused
            highlightcolor="black",       # Border color when focused
            highlightthickness=1,         # Thickness of the border
            #troughcolor="black",
            resolution=5,
            variable=self.sensitivity_var 
            )

        try:
            self.sensitivity_scale.set(self.sensitivity)
        except Exception as e:
            self.sensitivity_scale.set(0)
        self.sensitivity_scale.grid(row=1, column=1, padx=20, sticky="nsew")


        sensitivity_btn = tk.Button(
            self.settings_frame, 
            text="Set Sensitivity",
            font=("Arial", 10, "bold"),
            fg="white",
            bg=self.theme[1],
            relief=RAISED,
            bd=5,
            command=self.set_sensitivity
            )
        sensitivity_btn.bind("<Button-1>", self.save_sound)
        sensitivity_btn.bind("<Enter>", self.hover_effect)
        sensitivity_btn.bind("<Leave>", self.leave_effect)
        sensitivity_btn.grid(row=2, column=1, padx=20, sticky="nsew")


    # --- DETECT TIME ---
        self.time_var = tk.IntVar()

        self.time_scale = tk.Scale(
            self.settings_frame,
            from_=20, to=0,
            length=200,
            font=("Luckiest Guy", 12),
            tickinterval=20,
            fg="white",
            bg="#2F2F2F",
            bd=5,
            highlightbackground=self.theme[1],  # Border color when not focused
            highlightcolor="black",       # Border color when focused
            highlightthickness=1,         # Thickness of the border
            #troughcolor="black",
            resolution=1,
            variable=self.time_var 
            )

        try:
            self.time_scale.set(self.time)
        except Exception as e:
            self.time_scale.set(0)
        self.time_scale.grid(row=1, column=3, columnspan=2, padx=20, sticky="nsew")


        time_btn = tk.Button(
            self.settings_frame, 
            text="Set Time",
            font=("Arial", 10, "bold"),
            fg="white",
            bg=self.theme[1],
            relief=RAISED,
            bd=5,
            width=10,
            command=self.set_time
            )
        time_btn.bind("<Button-1>", self.save_sound)
        time_btn.bind("<Enter>", self.hover_effect)
        time_btn.bind("<Leave>", self.leave_effect)
        time_btn.grid(row=2, column=3, columnspan=2, padx=20, sticky="nsew")



        self.settings_frame.pack()

    def get_sense(self):
        with open("Assets\\config.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                return int(row["sensitivity"])
            
    def update_sensitivity(self, new_sense):
        rows = []
        with open("Assets\\config.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["sensitivity"] = new_sense
                rows.append(row)

        with open("Assets\\config.csv", "w", newline="") as file:
            fieldnames = ["sensitivity", "time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


    def set_sensitivity(self):
        self.sensitivity = self.sensitivity_var.get()
        self.update_sensitivity(self.sensitivity)
        if self.sensitivity == 0:
            self.status_label.config(text=f"Look around in game: Disabled", font=("Helvetica", 18, "bold"), fg="white", relief=SUNKEN, width=20)
        else:
            self.status_label.config(text=f"Sensitivity set to {self.sensitivity}", font=("Helvetica", 18, "bold"), fg="white", relief=SUNKEN, width=20)


    def get_time(self):
        with open("Assets\\config.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                return int(row["time"])
            
    def update_time(self, new_sense):
        rows = []
        with open("Assets\\config.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["time"] = new_sense
                rows.append(row)

        with open("Assets\\config.csv", "w", newline="") as file:
            fieldnames = ["sensitivity", "time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


    def set_time(self):
        self.time = self.time_var.get()
        self.update_time(self.time)
        if self.time == 0:
            self.status_label.config(text=f"Will do one action until it sees an image again", font=("Helvetica", 14), fg="white", relief=SUNKEN, width=40)
        else:
            self.status_label.config(text=f"Will pause after not seeing an image for {self.time} seconds", font=("Helvetica", 14), fg="white", relief=SUNKEN, width=40)




    def show_regions(self):
        if not messagebox.askyesnocancel("Show Image Regions", "A screenshot of your main montitor will be taken showing the detection regions. After pressing 'Yes' it will wait 3 seconds allowing you to open Call of Duty.\n\nWould you like to proceed?\n"):
            return
        time.sleep(3)
        image_regions = {
        'compass': (505, 22, 888, 38),
        'killcam': (851, 38, 219, 56),
        'killfeed': (154, 588, 155, 131),
        'match_start': (1587, 193, 315, 39),
        'match_in_progress_logo': (1587, 193, 315, 39),
        'mini_map': (60, 63, 247, 248),
        'packet_burst': (35, 474, 53, 41),
        'score': (116, 355, 139, 23),
        'scorestreaks': (1774, 706, 80, 198),
        'ui': (1659, 951, 204, 92),
        'compass_player': (167, 167, 28, 37),
        'AR_ammo': (1527, 1015, 42, 30),
        'kicked_region':(500, 376, 921, 309)
        }

        screenshot = pyautogui.screenshot()
        frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        for region_name, (x1, y1, width, height) in image_regions.items():
            x2 = x1 + width
            y2 = y1 + height
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(frame, region_name, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv.imshow('Image Regions', frame)
        pygame.mixer.music.load("Assets\\Sounds\\camera sound.mp3")
        pygame.mixer.music.play()

        cv.waitKey(0)

        cv.destroyAllWindows()

        if messagebox.askyesno("Save Image", "Would you like to save this image?"):
            try:
                file_name = filedialog.asksaveasfilename(
                    initialdir=str(os.path.dirname(os.path.abspath(__file__))),
                    title="Save Image",
                    initialfile="ImageRegions",
                    defaultextension=".jpg",
                    filetypes=[("JPEG", ".jpg"), ("All files", "*.*")]
                )
                if file_name:
                    cv.imwrite(file_name, frame)
                    messagebox.showinfo("Image Saved", f"Image saved to {file_name}")
                else:
                    messagebox.showwarning("No file", "No file was selected")
            except Exception:
                messagebox.showerror("Error", "Failed to save")

    def get_theme(self):
        try:
            with open("Assets\\Theme.txt", "r") as file:
                theme = file.readline().strip()
                if theme == "light":
                    return self.light

                elif theme == "dark":
                    return self.dark

                elif theme == "darker":
                    return self.darker

                elif theme == "black":
                    return self.black

                elif theme == "ocean":
                    return self.ocean

                elif theme == "retro":
                    return self.retro
                
                elif theme == "cyberpunk":
                    return self.cyberpunk

                elif theme == "gaming":
                    return self.gaming
                

                else:
                    return self.dark
        except Exception as e:
            print(e)
            return self.dark

    def update_theme(self, theme):
        try:
            with open("Assets\\Theme.txt", "w") as file:
                if theme == "light":
                    file.write("light")

                elif theme == "dark":
                    file.write("dark")

                elif theme == "darker":
                    file.write("darker")

                elif theme == "black":
                    file.write("black")

                elif theme == "ocean":
                    file.write("ocean")

                elif theme == "retro":
                    file.write("retro")

                elif theme == "cyberpunk":
                    file.write("cyberpunk")
                    
                elif theme == "gaming":
                    file.write("gaming")
                
                else:
                    return
                messagebox.showinfo("Theme Changed", "Theme will be applied next time the app starts")
        except Exception:
            return

    def show_stats(self):
        messagebox.showinfo("Current Stats", f"Deaths: {self.deaths}\nLosses: {self.losses}\nWins: {self.wins}")

    def total_stats(self):
        config.read('Assets\\Stats.ini')
        total_deaths = config["STATS"]["deaths"]
        total_losses = config["STATS"]["losses"]
        total_wins = config["STATS"]["wins"]
        messagebox.showinfo("Total Stats", f"Deaths: {total_deaths}\nLosses: {total_losses}\nWins: {total_wins}")

    def start_bot(self):
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        logic = threading.Thread(target=main, daemon=True)
        logic.start()

    def pause_bot(self):
        global force_paused
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="normal")
        force_paused = True
        delText()
        showText("Waiting for action to end to pause..")
        self.console.see(tk.END)

    def resume_bot(self):
        global force_paused
        self.resume_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        force_paused = False
        delText()
        showText("Resuming...")
        self.console.see(tk.END)

    def want_mouse(self):
        global mouse_onoff
        if self.mouse_var.get():
            mouse_onoff = True
            self.mouse_check.config(fg="#00FF00")
        else:
            mouse_onoff = False
            self.mouse_check.config(fg="white")

    def hover_effect(self, event):
        event.widget.config(bg="lightblue")

    def leave_effect(self, event):
        event.widget.config(bg=self.theme[1])

    def transparent_leave(self, event):
        event.widget.config(bg=self.theme[0])

    def click_sound(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\button click.mp3")
        pygame.mixer.music.play()

    def settings_sound(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\settings sound.mp3")
        pygame.mixer.music.play()

    def save_sound(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\save sound.mp3")
        pygame.mixer.music.play()

    def close_sound(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\close sound.mp3")
        pygame.mixer.music.play()

    def check_sound(self, event):
        pygame.mixer.music.load("Assets\\Sounds\\check sound.mp3")
        pygame.mixer.music.play()

    def app_clean(self):
        if listener:
            listener.stop()
        self.root.destroy()



mouse_onoff = False
mouse = MouseController()
keyboard = KeyController()
format = Figlet(font='Big', justify="center")
user32 = ctypes.windll.user32

# Mouse Movements with Ctypes
MOUSEEVENTF_MOVE = 0x0001

# Get screen resolution
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Set Paused at Start
paused = True
force_paused = False


GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RESET = "\033[0m"

mouse_command_list = ["180", "360", "720", "90Left", "90Right", "45Left", "45Right", "RandomTurnSmall"]
key_command_list = ["Sprint", "SlideR", "SlideL", "Crouch", "LayDown", "Back", "Inspect", "Jump", "Slide", "SlideBack"]
mouse_click_list = ["Shoot", "Aim", "Both"]



def do_mouse_command(command):
    """Execute mouse movement commands."""
    if command == "180":
        showText("Performing 180-degree turn")
        app.console.see(tk.END)
        move_mouse_relative(500, 0, app.sensitivity)  # Adjust values for a 180-degree turn
    elif command == "360":
        showText("Performing 360-degree turn")
        app.console.see(tk.END)
        move_mouse_relative(1000, 0, app.sensitivity)  # Adjust values for a 360-degree turn
    elif command == "90Left":
        showText("Performing 90-degree left turn")
        app.console.see(tk.END)
        move_mouse_relative(-250, 0, app.sensitivity)  # Adjust values for a 90-degree left turn
    elif command == "90Right":
        showText("Performing 90-degree right turn")
        app.console.see(tk.END)
        move_mouse_relative(250, 0, app.sensitivity)  # Adjust values for a 90-degree right turn
    else:
        showText("Unknown mouse command")
        app.console.see(tk.END)


# In Game Screen Detection
compass = cv.imread('cv references/in game/compass.png')
killcam = cv.imread('cv references/in game/killcam.png')
killfeed = cv.imread('cv references/in game/killfeed.png')
match_start= cv.imread('cv references/in game/match start.png')
match_in_progress_logo = cv.imread('cv references/in game/match in progress.png')
mini_map = cv.imread('cv references/in game/mini map.png')
packet_burst = cv.imread('cv references/in game/packet burst.png')
packet_burst_2 = cv.imread('cv references/in game/packet burst 2.png')
score = cv.imread('cv references/in game/score.png')
scorestreaks = cv.imread('cv references/in game/scorestreaks.png')
ui = cv.imread('cv references/in game/UI.png')
compass_player = cv.imread('cv references/in game/compass player.png')
AR_ammo = cv.imread('cv references/in game/AR ammo.png')


images_to_detect = [
    compass, 
    killcam,  
    killfeed,
    match_start, 
    match_in_progress_logo, 
    mini_map, 
    packet_burst,
    packet_burst_2, 
    score,
    scorestreaks, 
    ui,
    compass_player,
    AR_ammo
    ]


# Kicked Image Detection
kicked_img = cv.imread('cv references/search/kicked.png')
images_to_detect.append(kicked_img)
kicked_clicks = [(610, 620), (240, 920), (235, 222)] # click exit, find match, quickplay

def check_kicked(frame):
    kicked_region = (500, 376, 921, 309)  # region for kicked image

    screenshot = pyautogui.screenshot(region=kicked_region)
    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    result = cv.matchTemplate(frame, kicked_img, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)
    threshold = 0.5  # Adjust the threshold as needed
    return max_val > threshold

def perform_kicked_actions():
    showText(f"Kicked from the game! Will search for a new match now...")
    app.console.see(tk.END)

    # Click on the specified positions
    time.sleep(1.5)
    for (x, y) in kicked_clicks:
        mouse.position = (x, y)
        time.sleep(1.5)
        showText(f"Mouse Click at location: {mouse.position}")
        app.console.see(tk.END)
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(.3)


def on_press(key):
    try:
        if key == Key.f7 and app.pause_btn['state'] != tk.DISABLED:
            app.pause_bot()
        elif key == Key.f8 and app.resume_btn['state'] != tk.DISABLED:
            app.resume_bot()
    except Exception as e:
        showText(f"Error: {e}")
        app.console.see(tk.END)

# Formula x1, y1, width=x2-x1, height=y2-y1
image_regions = {
    'compass': ((505, 22, 888, 38), compass),
    'killcam': ((851, 38, 219, 56), killcam),
    'killfeed': ((154, 588, 155, 131), killfeed),
    'match_start': ((1587, 193, 315, 39), match_start),
    'match_in_progress_logo': ((1587, 193, 315, 39), match_in_progress_logo),
    'mini_map': ((60, 63, 247, 248), mini_map),
    'packet_burst': ((35, 474, 53, 41), packet_burst),
    'score': ((116, 355, 139, 23), score),
    'scorestreaks': ((1774, 706, 80, 198), scorestreaks),
    'ui': ((1659, 951, 204, 92), ui),
    'compass_player': ((167, 167, 28, 37), compass_player),
    'AR_ammo': ((1527, 1015, 42, 30), AR_ammo)
}


def check_image_in_region(image, region, threshold=0.5):
    """Check if a given image exists in the specified region."""
    # Capture the region desired
    screenshot = pyautogui.screenshot(region=region)
    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    # Perform template matching
    result = cv.matchTemplate(frame, image, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)

    return max_val > threshold


def ingame():
    """Check if any specified images are in their respective regions, with customized thresholds where needed."""
    for name, (region, img) in image_regions.items():
        if name == 'compass':
            custom_threshold = .8  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region!")
                app.console.see(tk.END)
                return True
        elif name == 'compass_player':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region!")
                app.console.see(tk.END)
                return True
        elif name == 'score':
            custom_threshold = .9  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region!")
                app.console.see(tk.END)
                return True
        elif name == 'killfeed':
            custom_threshold = .7  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region!")
                app.console.see(tk.END)
                return True
        elif name == 'match_in_progress_logo' or name == 'match_start':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region! (Selecting Loadout)")
                app.console.see(tk.END)
                time.sleep(2)
                # select loadout
                mouse.position = (192, 123)
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(1)
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(1)
                return True
        elif name == 'killcam':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                showText(f"{name} detected in its region! (skipping Killcam)")
                app.console.see(tk.END)
                # skip killcam
                keyboard.press("e")
                keyboard.release("e")
                
                app.deaths += 1
                try:
                    config.read('Assets\\Stats.ini')
                    if 'STATS' in config and 'deaths' in config['STATS']:
                        config['STATS']['deaths'] = str(int(config['STATS']['deaths']) + 1)
                    else:
                        if 'STATS' not in config:
                            config['STATS'] = {}
                        config['STATS']['deaths'] = '1'

                    with open('Assets\\Stats.ini', 'w') as configfile:
                        config.write(configfile)
                except Exception:
                    pass
                
                return True
                

        else:
            if check_image_in_region(img, region):
                showText(f"{name} detected in its region!")
                app.console.see(tk.END)
                return True
    return False

delText = lambda : app.console.delete("1.0", tk.END)
showText = lambda t: app.console.insert(tk.END, t+"\n")

def main():
    app.console.tag_configure("figlet_green", foreground="green")
    app.console.tag_configure("figlet_red", foreground="red")
    global paused
    app.console.insert(tk.END, Figlet().renderText(f"STARTING"), "figlet_green")
    time.sleep(1.5)
    for i in range(3):
        while force_paused:
            continue
        app.console.delete("1.0", tk.END)
        app.console.insert(tk.END, Figlet().renderText(f"{3 - i}"), "figlet_green")
        time.sleep(1)
    app.console.delete("1.0", tk.END)
    
    mouse.position = (960, 540)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
    showText("Waiting to get in a game...")
    app.console.see(tk.END)
    while True: # Program Functionality Main Loop
        if not force_paused:
            last_detected_time = time.time()  # Track the last time an image was detected
            while True:
                if force_paused:
                    break
                screenshot = pyautogui.screenshot()
                frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
                
                if not force_paused:
                    if ingame():
                        last_detected_time = time.time()  # Reset Timer
                        if paused:
                            showText(f"Image detected! Resuming...")
                            app.console.see(tk.END)
                            paused = False
                    elif check_kicked(frame):  
                        paused = True  # Pause the bot
                        perform_kicked_actions()  # Searches for Match
                        showText(f"Kicked actions complete. Resuming search...")
                        app.console.see(tk.END)
                        last_detected_time = time.time()
                    else:
                        # Check if it's been n seconds since the last detection
                        if time.time() - last_detected_time > app.time: # adjust time as fit
                            if not paused:
                                showText(f"No image detected for {app.time} seconds. Pausing...")
                                app.console.see(tk.END)
                                paused = True

                if paused or force_paused:
                    time.sleep(0.1)
                    continue
                
                if mouse_onoff:
                    random_turn = random.randint(-100, 100)
                    move_mouse_relative(random_turn, 0, app.sensitivity)
                    random_turn = random.randint(-100, 100)
                    move_mouse_relative(random_turn, 0, app.sensitivity)

                # Keyboard Actions
                skd = get_key_commands(key_command_list)
                do_key_command(skd)

                # Mouse Actions
                if mouse_onoff:
                    smc = get_mouse_commands(mouse_command_list)
                    do_mouse_command(smc)


                shoot(mouse_click_list)
                showText("---------------------------------\n")
                app.console.see(tk.END)
                time.sleep(1.5)
                keyboard.press("e")
                keyboard.release("e")
                continue

        
        
        delText()
        app.console.insert(tk.END, Figlet().renderText("PAUSED"), "figlet_red")
        while force_paused:
            if not force_paused:
                delText()
                app.console.insert(tk.END, Figlet().renderText("RESUMED"), "figlet_green")
                showText("Waiting to get in a game...")
                app.console.see(tk.END)
                break








def get_mouse_commands(mouse_command_list):
    random_mouse_movement = random.choice(mouse_command_list)
    return random_mouse_movement

def get_key_commands(key_command_list):
    random_key_movement = random.choice(key_command_list)
    return random_key_movement

def do_mouse_command(smc):
    if smc == "180":
        showText("Performing 180-degree turn")
        app.console.see(tk.END)
        move_mouse_relative(550, 0, app.sensitivity)
    elif smc == "360":
        showText("Performing 360-degree turn")
        app.console.see(tk.END)
        move_mouse_relative(1000, 0, app.sensitivity)
    elif smc == "720":
        showText("Performing 720-degree turn")
        app.console.see(tk.END)
        move_mouse_relative(2000, 0, app.sensitivity)
    elif smc == "90Left":
        showText("Performing 90-degree left turn")
        app.console.see(tk.END)
        move_mouse_relative(-250, 0, app.sensitivity)
    elif smc == "90Right":
        showText("Performing 90-degree right turn")
        app.console.see(tk.END)
        move_mouse_relative(250, 0, app.sensitivity)
    elif smc == "45Left":
        showText("Performing 45-degree left turn")
        app.console.see(tk.END)
        move_mouse_relative(-125, 0, app.sensitivity)
    elif smc == "45Right":
        showText("Performing 45-degree right turn")
        app.console.see(tk.END)
        move_mouse_relative(125, 0, app.sensitivity)
    elif smc == "RandomTurnSmall":
        random_turn = random.randint(-100, 100)
        showText(f"Performing a random turn of {abs(random_turn)} Degrees")
        app.console.see(tk.END)
        move_mouse_relative(random_turn, 0, app.sensitivity)
    else:
        showText("Unknown mouse command")
        app.console.see(tk.END)

def move_mouse_relative(dx, dy, sensitivity=None, duration=0.25, steps=50):
    """
    Smoothly moves the mouse cursor relative to its current position with scaling.

    Args:
        dx (int): Relative x movement.
        dy (int): Relative y movement.
        duration (float): Total time for the movement in seconds.
        steps (int): Number of intermediate steps.
        sensitivity (float): Scaling factor to amplify the movement.
    """
    
    if sensitivity is None:
        sensitivity = 100
        showText("Error with your config file. Setting sensitivity to 100")
    
    # Scale the movement based on sensitivity
    dx = int(dx * sensitivity)
    dy = int(dy * sensitivity)

    # Calculate the increment per step
    step_dx = dx / steps
    step_dy = dy / steps

    # Time delay per step
    step_delay = duration / steps

    for i in range(steps):
        # Move by the calculated step amount
        user32.mouse_event(MOUSEEVENTF_MOVE, int(step_dx), int(step_dy), 0, 0)
        time.sleep(step_delay)



def do_key_command(skd):
    if skd == "Sprint":
        showText("Sprint")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(3)
            keyboard.release("w")
    elif skd == "SlideR":
        showText("Slide Right")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("d")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("d")
            keyboard.release("q")
    elif skd == "Slide":
        showText("Sprint and Slide")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("w")
            keyboard.release("q")
    elif skd == "SlideL":
        showText("Slide Left")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("a")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("a")
            keyboard.release("q")
    elif skd == "SlideBack":
        showText("Slide Back")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("s")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("s")
            keyboard.release("q")
    elif skd == "Crouch":
        showText("Crouch")
        app.console.see(tk.END)
        keyboard.press("q")
        keyboard.release("q")
    elif skd == "LayDown":
        showText("Lay Down")
        app.console.see(tk.END)
        keyboard.press(Key.ctrl)
        time.sleep(.5)
        keyboard.release(Key.ctrl)
    elif skd == "Back":
        showText("Sprint Backwards")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("s")
            time.sleep(1)
            keyboard.release("s")
    elif skd == "Inspect":
        showText("Inspect")
        app.console.see(tk.END)
        keyboard.press("f")
        keyboard.release("f")
        time.sleep(5)
    elif skd == ("Jump"):
        showText("Run and Jump")
        app.console.see(tk.END)
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(1)
            keyboard.press(Key.space)
            time.sleep(.5)
            keyboard.release("w")
            keyboard.release(Key.space)
    else:
        pass


def shoot(mouse_click_list):
    YesNo = random.choices([True, False], weights=[.7, .3])[0]
    if YesNo:
        shoot = random.choice(mouse_click_list)
        if shoot == "Shoot":
            showText("Shoot")
            app.console.see(tk.END)
            mouse.press(Button.left)
            time.sleep(2)
            mouse.release(Button.left)
        elif shoot == "Aim":
            showText("Aim")
            app.console.see(tk.END)
            mouse.press(Button.right)
            time.sleep(2)
            mouse.release(Button.right)
        elif shoot == "Both":
            showText("Aim and Shoot")
            app.console.see(tk.END)
            mouse.press(Button.right)
            time.sleep(1)
            mouse.press(Button.left)
            time.sleep(2)
            mouse.release(Button.left)
            mouse.release(Button.right)
    else:
        showText("Dont Aim or Shoot")
        app.console.see(tk.END)
        

# def cleanup():
#     listener.stop()


if __name__ == "__main__":
    listener = Listener(on_press=on_press)
    listener.start()
    app = App()
    app.start_gui()
    # atexit.register(cleanup)
