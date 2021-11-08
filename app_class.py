# Importing necessary libraries and modules

import tkinter as tk
import tkinter.ttk as ttk
from psutil import virtual_memory, pids, cpu_percent
from cpuinfo import get_cpu_info
from platform import architecture, win32_ver, system
from win32api import EnumDisplayDevices, EnumDisplaySettings, GetSystemMetrics

# Class

class App():

	'''Class constructor.
	Necesssary arguments: title(title of the window), resizazble(ability of resizing the window)'''

	def __init__(self,
				 title: str,
				 resizable: tuple,
				 icon: str=None):

		self.root = tk.Tk()

		self.root.title(title)

		self.root.resizable(resizable[0], resizable[1])

		if icon:
			self.root.iconbitmap(icon)

		self.drawWidgets()

	def drawLabels(self, parent, var, text, row=None, additional_str='', font_size=12):
		
		'''It is made to stop reapiting in code.
		Labels with information about system are used very often.
		Method is a "template" to create them'''
		
		label = tk.Label(parent,
						text=f'{text}{additional_str}{var}',
						font=('Consolas', font_size),
						padx=10,
						pady=10)
		label.grid(row=row, column=0, sticky=tk.W)

	# Drawing widgets

	def drawWidgets(self):

		'''The main part. Drawing 3 tabs and system's characteristics labels for each'''

		ram_info = virtual_memory()

		row = 0

		os = system()

		tabs = ttk.Notebook(self.root)

		# Computer hardware tab and its widgets

		computer_hardware_tab = tk.Frame(tabs)

		# Variables

		cpu = get_cpu_info()['brand_raw']

		ram_amount = round(ram_info.total / 1024 / 1024 / 1000)

		system_bitness = architecture()[0]

		# Widgets

		if os == 'Windows':

			windows_version = win32_ver()[0]

			self.drawLabels(parent=computer_hardware_tab,
								var=' '+windows_version,
								text='Windows version: ',
								row=row,
								additional_str='Windows')
			row += 1

		self.drawLabels(parent=computer_hardware_tab,
							var=ram_amount,
							text='RAM(Gb): ',
							row=row)
		row += 1

		self.drawLabels(parent=computer_hardware_tab,
							var=cpu,
							text='CPU: ',
							row=row)
		row += 1

		self.drawLabels(parent=computer_hardware_tab,
							var=system_bitness,
							text='System bitness: ',
							row=row)

		tabs.add(computer_hardware_tab, text='Computer hardware')

		# Monitor characteristics tab and its widgets

		monitor_characteristics_tab = tk.Frame(tabs)

		# Variables

		display_info = EnumDisplayDevices()
		vid_card = display_info.DeviceString
		freq = EnumDisplaySettings(display_info.DeviceName).DisplayFrequency

		screen_resolution = f'{GetSystemMetrics(0)} x {GetSystemMetrics(1)}'

		# Widgets

		self.drawLabels(parent=monitor_characteristics_tab,
							var=vid_card,
							text='Video card: ',
							row=0)

		self.drawLabels(parent=monitor_characteristics_tab,
							var=freq,
							text='Frequency(GHz): ',
							row=1)

		self.drawLabels(parent=monitor_characteristics_tab,
							var=screen_resolution,
							text='Screen resolution: ',
							row=2)

		tabs.add(monitor_characteristics_tab, text='Monitor')

		# Performance tab and its widgets

		performance_tab = tk.Frame(tabs)

		# Variables

		available_ram = round(ram_info.available / 1024 / 1024 / 1024, 2)
		ram_usage_percent = round(ram_info.percent)
		used_ram = ram_amount * (ram_usage_percent / 100)

		processes_number = len(pids())
		cpu_usage_percent = cpu_percent()

		# Widgets

		# RAM frame

		ram_frame = tk.LabelFrame(performance_tab, text='Physical memory')

		self.drawLabels(parent=ram_frame, var=available_ram, text='Available RAM(GB): ', row=0, font_size=8)

		self.drawLabels(parent=ram_frame, var=ram_usage_percent, text='RAM usage percent(%): ', row=1, font_size=8)

		self.drawLabels(parent=ram_frame, var=used_ram, text='RAM usage(GB): ', row=2, font_size=8)

		ram_frame.grid(row=0, column=0, padx=5, pady=5)

		# System frame

		system_frame = tk.LabelFrame(performance_tab, text='System')

		self.drawLabels(parent=system_frame, var=processes_number, text='Processes: ', row=0, font_size=8)
		self.drawLabels(parent=system_frame, var=cpu_usage_percent, text='RAM usage percent(%): ', row=1, font_size=8)

		system_frame.grid(row=0, column=2)

		tabs.add(performance_tab, text='Performance')

		tabs.pack(fill=tk.BOTH, expand=1)

	def run(self):

		'''Runs our app'''

		self.root.mainloop()


if __name__ == '__main__':
	app = App(title='test', resizable=(False, False))
	app.run()
