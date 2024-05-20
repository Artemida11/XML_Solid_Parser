import datetime
import xml.etree.ElementTree as ET
from functools import partial

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


xml_file =''
lines = []


def get_file_path(e1):		# получить полный путь до выбранного файла
	filepath = filedialog.askopenfilename()
	global xml_file
	xml_file = filepath
	e1.delete(0,END)
	e1.insert(0,filepath)
	return e1
 

def run_parse():
	dt = datetime.datetime.now().strftime("%d.%m.%y")
	out_file = f'{xml_file}'.replace('.xml',f'-parsed-{dt}.txt')	# файл для записи
	
	out_lines = []

	tree = ET.parse(xml_file)
	root = tree.getroot()

	for modelset in root.findall('tools/utility/modelset'):
		for model in modelset.findall('model'):
			file_path = model.get('name')
			solids = model.findall('comparison/property[@name="Component_0@Solids"]')

			if solids:	# записываем только модели, у которых есть солиды
				solids = int(solids[0].get('value'))
				for s in range(solids):
					out_line = f'c3d_inspect_save_solid -l "" -m "{file_path}" -s {s}\n'
					out_lines.append(out_line)

	with open(out_file,'w') as f:	# перезапишет результаты, если в этот день этот файл уже парсили
		for l in out_lines:
			f.write(l)

	messagebox.showinfo(title='Парсинг завершён.', message=f'Результаты сохранены в файл {out_file}')


def main():
	root = Tk()
	try:
		root.title("XML to TXT")
		root.resizable(0, 0)
		windowWidth = root.winfo_reqwidth()
		windowHeight = root.winfo_reqheight()
		positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
		root.geometry("600x200+{}+{}".format(positionRight, positionDown))  # Root does not move yet

		text = Label(root,text="Выбрать файл:")
		text.grid(column=0, row=1, sticky=NW, padx=10, pady=10)

		e1 = Entry(width=50,bg="white")
		e1.grid(column=0, row=2, sticky=NW, padx=10, pady=0)
		 
		open_button = ttk.Button(text="Обзор", command=partial(get_file_path,e1))
		open_button.grid(column=1, row=2, sticky=NW,padx=0,pady=0)
		 
		save_button = ttk.Button(text="Парсить >> ", command=run_parse)
		save_button.grid(column=0, row=3,sticky=NW,padx=15,pady=15)

		quit_button = ttk.Button(text="Выйти", command=root.quit)
		quit_button.grid(column=1, row=4,sticky=SE,padx=0,pady=10)

		root.mainloop()
	finally:
		root.quit()	


if __name__ == '__main__':
	main()







