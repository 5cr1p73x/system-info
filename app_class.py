# Importing necessary libraries and modules

import tkinter as tk
import tkinter.ttk as ttk
from psutil import virtual_memory, pids, cpu_percent, disk_usage
from cpuinfo import get_cpu_info
from platform import architecture, system
from win32api import EnumDisplayDevices, EnumDisplaySettings, GetSystemMetrics, GetLogicalDriveStrings
from datetime import datetime
from math import pi as p

# Main class

class App():

	# Class fields

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

	def setTheme(self, first_col, second_col, third_col=None):

		'''Method to set dark/white theme'''

		for i in self.labels:
			
			if third_col:
				
				i.config(bg=first_col, fg=third_col)

			else:

				i.config(bg=first_col, fg=second_col)

		self.computer_hardware_tab.config(bg=first_col)
		self.monitor_characteristics_tab.config(bg=first_col)
		self.performance_tab.config(bg=first_col)
		self.disks_tab.config(bg=first_col)
		self.cpu_speed_test_tab.config(bg=first_col)

		self.ram_frame.config(bg=first_col, fg=second_col)
		self.system_frame.config(bg=first_col, fg=second_col)

		self.info_label.config(bg=first_col)
		self.pi_label.config(bg=first_col)
		self.result_label.config(bg=first_col)

	def setPerfVariables(self):

		'''Optimization. DRY(don\'t repeat yourself).
		These variables are used often.
		Code becomes more readable'''

		self.available_ram = round(self.ram_info.available/1024/1024/1024, 3)
		self.ram_usage_percent = round(self.ram_info.percent)
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

		start_time = datetime.now().microsecond

		11 / 3.5

		self.pi_label.config(text=f'π: {p}')
		self.result = datetime.now().microsecond - start_time

		while self.result == 0:

			start_time = datetime.now().microsecond

			11 / 3.5

			self.result = datetime.now().microsecond - start_time

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

	def drawWidgets(self):

		'''The main part. Drawing menu, 4 tabs and system's
		characteristics labels for 3 of them.
		The 4th tab is a CPU Speed test'''

		# Menu

		main_menu = tk.Menu(self.root)
		self.root.config(menu=main_menu)

		theme_menu = tk.Menu(main_menu, tearoff=0)
		theme_menu.add_command(label='White', command=lambda: self.setTheme('#F0F0F0', '#000'))
		theme_menu.add_command(label='Dark', command=lambda: self.setTheme('#2C2C2C', '#fff', '#62CA00'))
		main_menu.add_cascade(label='Theme', menu=theme_menu)

		main_menu.add_command(label='Exit', command=self.root.destroy)

		self.ram_info = virtual_memory()

		row = 0

		os = system()

		tabs = ttk.Notebook(self.root)

		# Computer hardware tab and its widgets

		self.computer_hardware_tab = tk.Frame(tabs, bg='#2C2C2C')

		# Variables

		cpu = get_cpu_info()['brand_raw']

		self.ram_amount = round(self.ram_info.total/1024/1024/1000)

		system_bitness = architecture()[0]

		# Widgets

		self.drawLabel(parent=self.computer_hardware_tab,
						var=os,
						text='OS: ',
						row=row)

		row += 1

		self.drawLabel(parent=self.computer_hardware_tab,
						var=self.ram_amount,
						text='RAM(Gb): ',
						row=row)
		row += 1

		self.drawLabel(parent=self.computer_hardware_tab,
						var=cpu,
						text='CPU: ',
						row=row)
		row += 1

		self.drawLabel(parent=self.computer_hardware_tab,
						var=system_bitness,
						text='System bitness: ',
						row=row)

		tabs.add(self.computer_hardware_tab, text='Computer hardware')

		# Monitor characteristics tab and its widgets

		self.monitor_characteristics_tab = tk.Frame(tabs, bg='#2C2C2C')

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

		tabs.add(self.monitor_characteristics_tab, text='Monitor')

		# Performance tab and its widgets

		self.performance_tab = tk.Frame(tabs, bg='#2C2C2C')

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

		self.ram_frame.grid(row=0, column=0, padx=5, pady=5)

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

		reload_btn = tk.Button(self.performance_tab,
							   text='Reload',
							   font=('Consolas', 14),
							   command=self.reloadFrames)
		reload_btn.grid(row=1, column=3, padx=10, pady=10)

		tabs.add(self.performance_tab, text='Performance')

		tabs.pack(fill=tk.BOTH, expand=1)

		# Disks tab and its widgets

		self.disks_tab = tk.Frame(tabs, bg='#2C2C2C')

		# Variables

		disks = GetLogicalDriveStrings()
		disks_list = disks.split('\000')[:-1]
		disks = ', '.join(disks_list)

		# Widgets

		self.drawLabel(parent=self.disks_tab,
					   var=disks,
					   text='disks\' letters: ',
					   row=0)

		# Drawing labels with info about free space on available disks

		r = 1

		for i in disks_list:

			i = i.strip('\\')

			try:
				free_memory = round(float(disk_usage(i).free/1024/1024/1024), 1)
			
			except:
				continue

			r += 1

			self.drawLabel(parent=self.disks_tab,
						   var=free_memory,
						   text=f'Free space(Gb) on drive {i} ',
						   row=r)

		tabs.add(self.disks_tab, text='disks')

		# CPU speed test tab and its widgets

		self.cpu_speed_test_tab = tk.Frame(tabs, bg='#2C2C2C')

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

		tabs.add(self.cpu_speed_test_tab, text='CPU Speed test')

		tabs.pack(fill=tk.BOTH, expand=1)


	def run(self):

		'''Runs our app'''

		self.root.mainloop()


if __name__ == '__main__':
	app = App(title='test', resizable=(False, False))
	app.run()
