# Importing necessary libraries and modules

import threading
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel
from getpass import getuser
from math import pi
from os import path
from platform import system
from socket import gethostname
from struct import calcsize
from time import sleep, time

from cpuinfo import get_cpu_info
from psutil import (Process, cpu_percent, disk_partitions, disk_usage,
                    pid_exists, pids, virtual_memory)

if system() == "Windows":
    from win32api import (EnumDisplayDevices, EnumDisplaySettings)

from pyautogui import size

# Main class

class App():
    # Class fields

    thread_stop = False
    color_names = {"Green": "#62CA00", "Blue": "#2975C1", "White": "#fff",
                   "Red": "#E10000", "Yellow": "#DBC500", "Orange": "#DB8700", "Black": "#000"}
    color = "#62CA00"
    labels = []
    tabs_list = []
    disks = []
    space = []

    def __init__(self, title, resizable, icon=None):
        """Class constructor.
        Necesssary arguments: title(title of the window),
         resizazble(ability of resizing the window)"""

        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(resizable[0], resizable[1])

        if icon:
            self.root.iconbitmap(icon)

        self.tabs = ttk.Notebook(self.root)

        self.draw_widgets()

    def set_text_color(self, color):
        """Setting the main color of the app"""

        self.color = color

        for label in self.labels:
            label.config(fg=color)

        self.cpu_diagram_canvas.itemconfigure(self.cpu_diagram, fill=color)
        self.ram_diagram_canvas.itemconfigure(self.ram_diagram, fill=color)

        self.ram_frame.config(fg=color)
        self.system_frame.config(fg=color)
        self.cpu_usage_frame.config(fg=color)
        self.ram_usage_frame.config(fg=color)

        self.tasks_list.config(fg=color)

    def set_diagram(self, canvas, diagram, main_var=None):
        """Constant changing of diagrams"""

        while not self.thread_stop:
            x_0, y_0, x_1, y_1 = canvas.coords(diagram)

            if main_var == cpu_percent:
                var = main_var()
                y_0 = round(100-var)

            else:
                y_0 = round(virtual_memory().available/1024/1024, 3)//(self.ram_amount*10)

            canvas.coords(diagram, x_0, y_0, x_1, y_1)

            sleep(0.5)

    def set_theme(self, bg_color):
        """Method to set dark/white theme"""

        for label in self.labels:
            label.config(bg=bg_color)

        for tab in self.tabs_list:
            tab.config(bg=bg_color)

        self.ram_frame.config(bg=bg_color)
        self.system_frame.config(bg=bg_color)
        self.cpu_usage_frame.config(bg=bg_color)
        self.ram_usage_frame.config(bg=bg_color)

        self.info_label.config(bg=bg_color)
        self.pi_label.config(bg=bg_color)
        self.result_label.config(bg=bg_color)

        self.cpu_diagram_canvas.config(bg=bg_color)
        self.ram_diagram_canvas.config(bg=bg_color)

        self.tasks_list.config(bg=bg_color)

    def set_performance_variables(self):
        """Optimization. DRY(don\"t repeat yourself).
        These variables are used often.
        Code becomes more readable"""

        ram_info = virtual_memory()

        self.available_ram = round(ram_info.available/1024/1024/1024, 3)
        self.ram_usage_percent = round(ram_info.percent)
        self.used_ram = self.ram_amount * (self.ram_usage_percent/100)

        self.process_number = len(pids())
        self.cpu_usage_percent = cpu_percent()

    def reload_performance_frames(self):
        """Ability of reloading the information in performance tab"""

        self.set_performance_variables()

        self.available_ram_label.config(text=f"Available RAM(GB): {self.available_ram}")
        self.ram_usage_percent_label.config(text=f"RAM usage percent(%): {self.ram_usage_percent}")
        self.ram_usage_label.config(text=f"RAM usage(GB): {self.used_ram}")

        self.processes_number_label.config(text=f"Process amount: {self.process_number}")
        self.cpu_usage_num_label.config(text=f"CPU usage percent(%): {self.cpu_usage_percent}")

    def calculate_processor_speed(self):
        """CPU Speed test. The speed will be known by calculating number π"""

        start_time = time()

        11 / 3.5

        self.pi_label.config(text=f"π: {pi}")
        self.result = time() - start_time

        while self.result == 0:
            start_time = time()

            11 / 3.5

            self.result = time() - start_time

        self.result_label.config(text="Result: " + str(self.result) + " ms")
        self.start_button.config(text="Restart")

    def draw_label(self, parent, var, text, row=None, font_size=12):
        """It is made to stop reapiting in code.
        Labels with information about system are used very often.
        Method is a "template" to create them"""

        label = tk.Label(parent,
                         text=f"{text}{var}",
                         font=("Consolas", font_size),
                         padx=10,
                         pady=10,
                         bg="#2C2C2C",
                         fg="#62CA00",
                         wraplength=500)
        label.grid(row=row, column=0, sticky=tk.W)

        self.labels.append(label)

        return label

    def draw_tab(self, name):
        """Drawing tabs. DRY"""

        tab = tk.Frame(self.tabs, bg="#2C2C2C")

        self.tabs.add(tab, text=name)

        self.tabs_list.append(tab)

        return tab

    def draw_menu(self):
        """Drawing menu"""

        main_menu = tk.Menu(self.root)
        self.root.config(menu=main_menu)

        theme_submenu = tk.Menu(main_menu, tearoff=0)
        theme_submenu.add_command(label="White", command=lambda: self.set_theme("#F0F0F0"))
        theme_submenu.add_command(label="Dark", command=lambda: self.set_theme("#2C2C2C"))
        main_menu.add_cascade(label="Theme", menu=theme_submenu)

        color_submenu = tk.Menu(main_menu, tearoff=0)

        for name, color in self.color_names.items():
            color_submenu.add_command(label=name, command=lambda color=color: self.set_text_color(color))

        main_menu.add_cascade(label="Color", menu=color_submenu)

        main_menu.add_command(label="Exit", command=self.exit_app)

    def draw_main_tab(self):
        """Drawing main tab"""

        # Main tab and its widgets

        self.main_info_tab = self.draw_tab("Main info")

        # Variables

        self.ram_info = virtual_memory()

        row = 0

        os = system()

        cpu = get_cpu_info()["brand_raw"]

        self.ram_amount = round(self.ram_info.total/1024/1024/1000)

        system_bitness = calcsize("P") * 8

        # Widgets

        self.draw_label(parent=self.main_info_tab,
                        var=os,
                        text="OS: ",
                        row=row)

        row += 1

        self.draw_label(parent=self.main_info_tab,
                        var=self.ram_amount,
                        text="RAM(Gb): ",
                        row=row)
        row += 1

        self.draw_label(parent=self.main_info_tab,
                        var=cpu,
                        text="CPU: ",
                        row=row)
        row += 1

        self.draw_label(parent=self.main_info_tab,
                        var=system_bitness,
                        text="System bitness: ",
                        row=row)

        self.tabs.add(self.main_info_tab, text="Main info")

    def draw_monitor_tab(self):
        """Drawing monitor tab"""

        # Monitor characteristics tab and its widgets

        self.monitor_characteristics_tab = self.draw_tab("Monitor")

        # Variables

        if system() == "Linux":
            vid_card = "---"
            freq = "---"

        else:
            display_info = EnumDisplayDevices()
            vid_card = display_info.DeviceString
            freq = EnumDisplaySettings(display_info.DeviceName).DisplayFrequency

        screen_resolution = f"{size()[0]} x {size()[1]}"

        # Widgets

        self.draw_label(parent=self.monitor_characteristics_tab,
                        var=vid_card,
                        text="Video card: ",
                        row=0)

        self.draw_label(parent=self.monitor_characteristics_tab,
                        var=freq,
                        text="Frequency(GHz): ",
                        row=1)

        self.draw_label(parent=self.monitor_characteristics_tab,
                        var=screen_resolution,
                        text="Screen resolution: ",
                        row=2)

        self.tabs.add(self.monitor_characteristics_tab, text="Monitor")

    def draw_perforamnce_tab(self):
        """Drawing performance tab"""

        # Performance tab and its widgets

        self.performance_tab = self.draw_tab("Performance")

        # Variables

        self.set_performance_variables()

        # Widgets

        # RAM frame

        self.ram_frame = tk.LabelFrame(self.performance_tab,
                                  text="Physical memory",
                                  bg="#2C2C2C",
                                  fg="#62CA00")

        self.available_ram_label = self.draw_label(parent=self.ram_frame,
                                                 var=self.available_ram,
                                                 text="Available RAM(GB): ",
                                                 row=0,
                                                 font_size=8)

        self.ram_usage_percent_label = self.draw_label(parent=self.ram_frame,
                                               var=self.ram_usage_percent,
                                               text="RAM usage percent(%): ",
                                               row=1,
                                               font_size=8)

        self.ram_usage_label = self.draw_label(parent=self.ram_frame,
                                             var=self.used_ram,
                                             text="RAM usage(GB): ",
                                             row=2,
                                             font_size=8)

        self.ram_frame.grid(row=0, column=0)

        # RAM usage frame

        self.ram_usage_frame = tk.LabelFrame(self.performance_tab,
                                             text="RAM Usage",
                                             bg="#2C2C2C",
                                             fg="#62CA00")
        self.ram_usage_frame.grid(row=0, column=1, padx=5, pady=5)

        self.ram_diagram_canvas = tk.Canvas(self.ram_usage_frame,
                      width=25,
                      height=100,
                      bg="#2C2C2C",
                      bd=0,
                      highlightthickness=0)
        self.ram_diagram_canvas.pack()

        self.ram_diagram = self.ram_diagram_canvas.create_rectangle(-1, -1, 25, 100,
                    fill=self.color)

        ram_diagram_thread = threading.Thread(target=self.set_diagram, args=(self.ram_diagram_canvas,
                                                                            self.ram_diagram))
        ram_diagram_thread.start()

        # System frame

        self.system_frame = tk.LabelFrame(self.performance_tab,
                                     text="System",
                                     bg="#2C2C2C",
                                     fg="#62CA00")

        self.processes_number_label = self.draw_label(parent=self.system_frame,
                                            var=self.process_number,
                                            text="Number of processes: ",
                                            row=0,
                                            font_size=8)
        self.cpu_usage_num_label = self.draw_label(parent=self.system_frame,
                                                 var=self.cpu_usage_percent,
                                                 text="CPU usage percent(%): ",
                                                 row=1,
                                                 font_size=8)

        self.system_frame.grid(row=0, column=2)

        # CPU usage frame

        self.cpu_usage_frame = tk.LabelFrame(self.performance_tab,
                                             text="CPU Usage",
                                             bg="#2C2C2C",
                                             fg="#62CA00")
        self.cpu_usage_frame.grid(row=0, column=3, padx=5, pady=5)

        self.cpu_diagram_canvas = tk.Canvas(self.cpu_usage_frame,
                      width=25,
                      height=100,
                      bg="#2C2C2C",
                      bd=0,
                      highlightthickness=0)
        self.cpu_diagram_canvas.pack()

        self.cpu_diagram = self.cpu_diagram_canvas.create_rectangle(-1, -1, 25, 100,
                           fill=self.color)

        cpu_diagram_thread = threading.Thread(target=self.set_diagram, args=(self.cpu_diagram_canvas,
                                                                            self.cpu_diagram,
                                                                            cpu_percent))
        cpu_diagram_thread.start()

        reload_button = tk.Button(self.performance_tab,
                               text="Reload",
                               font=("Consolas", 14),
                               command=self.reload_performance_frames)
        reload_button.grid(row=1, column=2, padx=10, pady=10)

        self.tabs.add(self.performance_tab, text="Performance")

        self.tabs.pack(fill=tk.BOTH, expand=1)

    def draw_disks_tab(self):
        """Drawing disks tab"""

        # Disks tab and its widgets

        self.disks_tab = self.draw_tab("Disks")

        # Variables

        partitions = disk_partitions()

        for partition in partitions:
            try:
                partition_usage = disk_usage(partition.mountpoint)

            except PermissionError:
                continue

            self.space.append(round(partition_usage.free/1024/1024/1024, 1))
            self.disks.append(partition.device)

        # Widgets

        self.draw_label(parent=self.disks_tab,
                       var=", ".join(self.disks),
                       text="Disks' letters: ",
                       row=0)

        # Drawing labels with info about free space on available disks

        row = 1

        for disk_letter in self.disks:
            try:
                free_memory = self.space[self.disks.index(disk_letter)]

            except:
                continue

            disk_letter = disk_letter.strip("\\")

            row += 1

            self.draw_label(parent=self.disks_tab,
                           var=free_memory,
                           text=f"Free space(Gb) on disk {disk_letter} ",
                           row=row)

        self.tabs.add(self.disks_tab, text="Disks")

    def draw_speed_tab(self):
        """Drawing CPU speed test tab"""

        # CPU speed test tab and its widgets

        self.cpu_speed_test_tab = self.draw_tab("CPU speed test")

        # Widgets

        self.info_label = tk.Label(self.cpu_speed_test_tab,
                              text="Test your processor speed with calculating π \nand showing it on the screen",
                              font=("Consolas", 12),
                              bg="#2C2C2C",
                              fg="#1B948E")
        self.info_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.result_label = tk.Label(self.cpu_speed_test_tab,
                              text="Result: ",
                              font=("Consolas", 12),
                              bg="#2C2C2C",
                              fg="#D32D13")
        self.result_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        self.pi_label = tk.Label(self.cpu_speed_test_tab,
                              text="π: ",
                              font=("Consolas", 12),
                              bg="#2C2C2C",
                              fg="#4FA300")
        self.pi_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

        self.start_button = tk.Button(self.cpu_speed_test_tab,
                              text="Start",
                              font=("Consolas", 14),
                              command=self.calculate_processor_speed)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.tabs.add(self.cpu_speed_test_tab, text="CPU Speed test")

        self.tabs.pack(fill=tk.BOTH, expand=1)

    def draw_user_tab(self):
        """Drawing user tab"""

        # User tab and its widgets

        self.user_tab = self.draw_tab("User")

        # Variables

        user_name = getuser()
        home_dir = path.expanduser("~")
        host_name = gethostname()

        # Widgets

        self.draw_label(parent=self.user_tab,
                       var=user_name,
                       text="User name: ",
                       row=0)

        self.draw_label(parent=self.user_tab,
                       var=home_dir,
                       text="Home directory: ",
                       row=1)

        self.draw_label(parent=self.user_tab,
                       var=host_name,
                       text="Host name: ",
                       row=2)

        self.tabs.add(self.user_tab, text="User")

    def draw_task_list_tab(self):
        """Drawing task list tab"""

        # Task list tab and its widgets

        self.task_list_tab = self.draw_tab("Task list")

        self.tasks_list = tk.Listbox(self.task_list_tab, font=("Consolas", 14), width=52,
                                                         bg="#2C2C2C", fg="#62CA00")

        # Variables

        pids_ = pids()

        # Widgets

        row = 0

        for pid in pids_:
            if pid_exists(pid):
                proc = Process(pid)

                self.tasks_list.insert(tk.END, f"{pid} - {proc.name()}({proc.status()})")

            row += 1

        self.tasks_list.grid(row=0, column=0)

    def draw_widgets(self):
        """The main part. Drawing menu, 4 tabs and system's
        characteristics labels for 3 of them.
        The 4th tab is a CPU Speed test"""

        self.draw_menu()

        self.draw_main_tab()

        self.draw_monitor_tab()

        self.draw_perforamnce_tab()

        self.draw_disks_tab()

        self.draw_speed_tab()

        self.draw_user_tab()

        self.draw_task_list_tab()

    def exit_app(self):
        """Correct app ending"""

        answer = askokcancel("Quit app", "Are you sure that you want to exit the app?")

        if answer:
            self.thread_stop = True

            self.root.destroy()

    def run(self):
        """Runs our app"""

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.root.mainloop()


if __name__ == "__main__":
    app = App(title="test", resizable=(False, False), icon="img/icon.ico")
    app.run()
