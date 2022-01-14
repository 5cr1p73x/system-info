# Importing necessary libraries and modules

import threading
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from math import pi as p
from platform import system
from struct import calcsize
from time import sleep, time
from tkinter.messagebox import askokcancel

from cpuinfo import get_cpu_info
from psutil import cpu_percent, disk_usage, pids, virtual_memory
from win32api import (EnumDisplayDevices, EnumDisplaySettings,
                      GetLogicalDriveStrings, GetSystemMetrics)

# Main class

class App():

	# Class fields

	thread_stop = False
	color_names = {'Green': '#62CA00', 'Blue': '#2975C1', 'White': '#fff',
				   'Red': '#E10000', 'Yellow': '#DBC500', 'Orange': '#DB8700', 'Black': '#000'}
	color = '#62CA00'
	labels = []

	def __init__(self,
				 title,
				 resizable,
				 icon=None):

		'''Class constructor.
		Necesssary arguments: title(title of the window), 
		resizazble(ability of resizing the window)'''

		self.root = tk.Tk()
		self.root.title(title)
		self.root.resizable(resizable[0], resizable[1])

		if icon:
			self.root.iconbitmap(icon)

		self.drawWidgets()

	def setColor(self, color):
		
		'''Setting the main color of the app'''

		self.color = color

		for label in self.labels:

			label.config(fg=color)

		self.cpu_diagram_c.itemconfigure(self.cpu_diagram, fill=color)
		self.ram_diagram_c.itemconfigure(self.ram_diagram, fill=color)

		self.ram_frame.config(fg=color)
		self.system_frame.config(fg=color)
		self.cpu_usage_frame.config(fg=color)
		self.ram_usage_frame.config(fg=color)

	def setDiagram(self, canvas, diagram, main_var=None):

		'''Constant changing of diagrams'''

		while not self.thread_stop:

			x0, y0, x1, y1 = canvas.coords(diagram)
			if main_var == cpu_percent:

				var = main_var()
				y0 = round(100-var)
			
			else:
				y0 = round(virtual_memory().available/1024/1024, 3)//(self.ram_amount*10)

			canvas.coords(diagram, x0, y0, x1, y1)

			sleep(0.5)

	def setTheme(self, first_col, second_col, third_col=None):

		'''Method to set dark/white theme'''

		for i in self.labels:
			
			if third_col:
				
				i.config(bg=first_col, fg=third_col)

			else:

				i.config(bg=first_col, fg=second_col)

		self.main_info_tab.config(bg=first_col)
		self.monitor_characteristics_tab.config(bg=first_col)
		self.performance_tab.config(bg=first_col)
		self.disks_tab.config(bg=first_col)
		self.cpu_speed_test_tab.config(bg=first_col)

		self.ram_frame.config(bg=first_col, fg=second_col)
		self.system_frame.config(bg=first_col, fg=second_col)
		self.cpu_usage_frame.config(bg=first_col, fg=second_col)
		self.ram_usage_frame.config(bg=first_col, fg=second_col)

		self.info_label.config(bg=first_col)
		self.pi_label.config(bg=first_col)
		self.result_label.config(bg=first_col)

		self.cpu_diagram_c.config(bg=first_col)
		self.ram_diagram_c.config(bg=first_col)

	def setPerfVariables(self):

		'''Optimization. DRY(don\'t repeat yourself).
		These variables are used often.
		Code becomes more readable'''

		ram_info = virtual_memory()

		self.available_ram = round(ram_info.available/1024/1024/1024, 3)
		self.ram_usage_percent = round(ram_info.percent)
		self.used_ram = self.ram_amount * (self.ram_usage_percent/100)

		self.process_number = len(pids())
		self.cpu_usage_percent = cpu_percent()

	def reloadFrames(self):

		'''Ability of reloading the information in performance tab'''

		self.setPerfVariables()

		self.available_ram_lbl.config(text=f'Available RAM(GB): {self.available_ram}')
		self.p_ram_usage_lbl.config(text=f'RAM usage percent(%): {self.ram_usage_percent}')
		self.ram_usage_lbl.config(text=f'RAM usage(GB): {self.used_ram}')

		self.proc_num_lbl.config(text=f'Process amount: {self.process_number}')
		self.cpu_usage_num_lbl.config(text=f'CPU usage percent(%): {self.cpu_usage_percent}')

	def calculateSpeed(self):

		'''CPU Speed test. The speed will be known by calculating number π'''

		start_time = time()

		11 / 3.5

		self.pi_label.config(text=f'π: {p}')
		self.result = time() - start_time

		while self.result == 0:

			start_time = time()

			11 / 3.5

			self.result = time() - start_time

		self.result_label.config(text='Result: ' + str(self.result) + ' ms')
		self.start_btn.config(text='Restart')

	def drawLabel(self, parent, var, text, row=None, font_size=12):

		'''It is made to stop reapiting in code.
		Labels with information about system are used very often.
		Method is a "template" to create them'''

		label = tk.Label(parent,
						 text=f'{text}{var}',
						 font=('Consolas', font_size),
						 padx=10,
						 pady=10,
						 bg='#2C2C2C',
                         fg='#62CA00',
						 wraplength=500)
		label.grid(row=row, column=0, sticky=tk.W)

		self.labels.append(label)

		return label

	def drawMenu(self):

		'''Drawing menu'''

		main_menu = tk.Menu(self.root)
		self.root.config(menu=main_menu)

		theme_submenu = tk.Menu(main_menu, tearoff=0)
		theme_submenu.add_command(label='White', command=lambda: self.setTheme('#F0F0F0', self.color))
		theme_submenu.add_command(label='Dark', command=lambda: self.setTheme('#2C2C2C', '#fff', self.color))
		main_menu.add_cascade(label='Theme', menu=theme_submenu)

		color_submenu = tk.Menu(main_menu, tearoff=0)

		for name, color in self.color_names.items():

			color_submenu.add_command(label=name, command=lambda color=color: self.setColor(color))

		main_menu.add_cascade(label='Color', menu=color_submenu)

		main_menu.add_command(label='Exit', command=self.exitApp)

	def drawMainTab(self):

		'''Drawing main tab'''

		# Main characteristics tab and its widgets

		self.ram_info = virtual_memory()

		row = 0

		os = system()

		self.tabs = ttk.Notebook(self.root)

		# Computer hardware tab and its widgets

		self.main_info_tab = tk.Frame(self.tabs, bg='#2C2C2C')

		# Variables

		cpu = get_cpu_info()['brand_raw']

		self.ram_amount = round(self.ram_info.total/1024/1024/1000)

		system_bitness = calcsize('P') * 8

		# Widgets

		self.drawLabel(parent=self.main_info_tab,
						var=os,
						text='OS: ',
						row=row)

		row += 1

		self.drawLabel(parent=self.main_info_tab,
						var=self.ram_amount,
						text='RAM(Gb): ',
						row=row)
		row += 1

		self.drawLabel(parent=self.main_info_tab,
						var=cpu,
						text='CPU: ',
						row=row)
		row += 1

		self.drawLabel(parent=self.main_info_tab,
						var=system_bitness,
						text='System bitness: ',
						row=row)

		self.tabs.add(self.main_info_tab, text='Main info')

	def drawMonitorTab(self):

		'''Drawing monitor tab'''

		# Monitor characteristics tab and its widgets

		self.monitor_characteristics_tab = tk.Frame(self.tabs, bg='#2C2C2C')

		# Variables

		display_info = EnumDisplayDevices()
		vid_card = display_info.DeviceString
		freq = EnumDisplaySettings(display_info.DeviceName).DisplayFrequency

		screen_resolution = f'{GetSystemMetrics(0)} x {GetSystemMetrics(1)}'

		# Widgets

		self.drawLabel(parent=self.monitor_characteristics_tab,
						var=vid_card,
						text='Video card: ',
						row=0)

		self.drawLabel(parent=self.monitor_characteristics_tab,
						var=freq,
						text='Frequency(GHz): ',
						row=1)

		self.drawLabel(parent=self.monitor_characteristics_tab,
						var=screen_resolution,
						text='Screen resolution: ',
						row=2)

		self.tabs.add(self.monitor_characteristics_tab, text='Monitor')

	def drawPerfTab(self):

		'''Drawing performance tab'''

		# Performance tab and its widgets

		self.performance_tab = tk.Frame(self.tabs, bg='#2C2C2C')

		# Variables

		self.setPerfVariables()

		# Widgets

		# RAM frame

		self.ram_frame = tk.LabelFrame(self.performance_tab,
								  text='Physical memory',
								  bg='#2C2C2C',
								  fg='#fff')

		self.available_ram_lbl = self.drawLabel(parent=self.ram_frame,
												 var=self.available_ram,
												 text='Available RAM(GB): ',
												 row=0,
												 font_size=8)

		self.p_ram_usage_lbl = self.drawLabel(parent=self.ram_frame,
											   var=self.ram_usage_percent,
											   text='RAM usage percent(%): ',
											   row=1,
											   font_size=8)

		self.ram_usage_lbl = self.drawLabel(parent=self.ram_frame,
											 var=self.used_ram,
											 text='RAM usage(GB): ',
											 row=2,
											 font_size=8)

		self.ram_frame.grid(row=0, column=0)

		# RAM usage frame

		self.ram_usage_frame = tk.LabelFrame(self.performance_tab,
											 text='RAM Usage',
											 bg='#2C2C2C',
											 fg='#fff')
		self.ram_usage_frame.grid(row=0, column=1, padx=5, pady=5)

		self.ram_diagram_c = tk.Canvas(self.ram_usage_frame,
					  width=25,
					  height=100,
					  bg='#2C2C2C',
					  bd=0,
					  highlightthickness=0)
		self.ram_diagram_c.pack()

		self.ram_diagram = self.ram_diagram_c.create_rectangle(-1, -1, 25, 100,
					fill=self.color)
		
		ram_diagram_thread = threading.Thread(target=self.setDiagram, args=(self.ram_diagram_c,
																			self.ram_diagram))
		ram_diagram_thread.start()

		# System frame

		self.system_frame = tk.LabelFrame(self.performance_tab,
									 text='System',
									 bg='#2C2C2C',
									 fg='#fff')

		self.proc_num_lbl = self.drawLabel(parent=self.system_frame,
											var=self.process_number,
											text='Process amount: ',
											row=0,
											font_size=8)
		self.cpu_usage_num_lbl = self.drawLabel(parent=self.system_frame,
												 var=self.cpu_usage_percent,
												 text='CPU usage percent(%): ',
												 row=1,
												 font_size=8)

		self.system_frame.grid(row=0, column=2)

		# CPU usage frame

		self.cpu_usage_frame = tk.LabelFrame(self.performance_tab,
											 text='CPU Usage',
											 bg='#2C2C2C',
											 fg='#fff')
		self.cpu_usage_frame.grid(row=0, column=3, padx=5, pady=5)

		self.cpu_diagram_c = tk.Canvas(self.cpu_usage_frame,
					  width=25,
					  height=100,
					  bg='#2C2C2C',
					  bd=0,
					  highlightthickness=0)
		self.cpu_diagram_c.pack()

		self.cpu_diagram = self.cpu_diagram_c.create_rectangle(-1, -1, 25, 100,
						   fill=self.color)

		cpu_diagram_thread = threading.Thread(target=self.setDiagram, args=(self.cpu_diagram_c,
																			self.cpu_diagram,
																			cpu_percent))
		cpu_diagram_thread.start()

		reload_btn = tk.Button(self.performance_tab,
							   text='Reload',
							   font=('Consolas', 14),
							   command=self.reloadFrames)
		reload_btn.grid(row=1, column=2, padx=10, pady=10)

		self.tabs.add(self.performance_tab, text='Performance')

		self.tabs.pack(fill=tk.BOTH, expand=1)

	def drawDisksTab(self):

		'''Drawing disks tab'''

		# Disks tab and its widgets

		self.disks_tab = tk.Frame(self.tabs, bg='#2C2C2C')

		# Variables

		disks = GetLogicalDriveStrings()
		disks_list = disks.split('\000')[:-1]
		disks = ', '.join(disks_list)

		# Widgets

		self.drawLabel(parent=self.disks_tab,
					   var=disks,
					   text='Disks\' letters: ',
					   row=0)

		# Drawing labels with info about free space on available disks

		r = 1

		for disk_letter in disks_list:

			disk_letter = disk_letter.strip('\\')

			try:
				free_memory = round(float(disk_usage(disk_letter).free/1024/1024/1024), 1)
			
			except:
				continue

			r += 1

			self.drawLabel(parent=self.disks_tab,
						   var=free_memory,
						   text=f'Free space(Gb) on disk {disk_letter} ',
						   row=r)

		self.tabs.add(self.disks_tab, text='Disks')

	def drawSpeedTab(self):

		'''Drawing CPU speed test tab'''

		# CPU speed test tab and its widgets

		self.cpu_speed_test_tab = tk.Frame(self.tabs, bg='#2C2C2C')

		# Widgets

		self.info_label = tk.Label(self.cpu_speed_test_tab,
							  text='Test your processor speed with calculating π \nand showing it on the screen',
							  font=('Consolas', 12),
							  bg='#2C2C2C',
							  fg='#1B948E')
		self.info_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

		self.result_label = tk.Label(self.cpu_speed_test_tab,
							  text='Result: ',
							  font=('Consolas', 12),
							  bg='#2C2C2C',
							  fg='#D32D13')
		self.result_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

		self.pi_label = tk.Label(self.cpu_speed_test_tab,
							  text='π: ',
							  font=('Consolas', 12),
							  bg='#2C2C2C',
							  fg='#4FA300')
		self.pi_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

		self.start_btn = tk.Button(self.cpu_speed_test_tab,
							  text='Start',
							  font=('Consolas', 14),
							  command=self.calculateSpeed)
		self.start_btn.grid(row=3, column=0, padx=10, pady=10)

		self.tabs.add(self.cpu_speed_test_tab, text='CPU Speed test')

		self.tabs.pack(fill=tk.BOTH, expand=1)

	def drawWidgets(self):

		'''The main part. Drawing menu, 4 tabs and system's
		characteristics labels for 3 of them.
		The 4th tab is a CPU Speed test'''

		self.drawMenu()

		self.drawMainTab()

		self.drawMonitorTab()

		self.drawPerfTab()

		self.drawDisksTab()

		self.drawSpeedTab()

	def exitApp(self):

		'''Correct app ending'''
		
		answer = askokcancel('Quit app', 'Are you sure that you want to quit the app?')

		if answer:

			self.thread_stop = True

			self.root.destroy()

	def run(self):

		'''Runs our app'''

		self.root.protocol('WM_DELETE_WINDOW', self.exitApp)
		self.root.mainloop()


if __name__ == '__main__':
	app = App(title='test', resizable=(False, False), icon='img/icon.ico')
	app.run()
