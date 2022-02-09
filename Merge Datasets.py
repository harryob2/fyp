import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas

root = Tk()
root.title('FYP GUI - Merge Datasets')
root.geometry("450x550")

df = pandas.DataFrame()

# must fix this, wont import xlsx files due to encoding error
def thing():
    df = pandas.read_excel(filedialog.askopenfile(title = "Import Athlete VO2/HR Data"))
    print(df)

button_frame = Frame(root)

wrapper1 = LabelFrame(root, text = 'Current Data')

import_button = Button(wrapper1, text = "Import", command = thing)

wrapper1.pack(fill='both', expand='yes', padx=20, pady=20)

import_button.pack(pady=10)

root.mainloop()
