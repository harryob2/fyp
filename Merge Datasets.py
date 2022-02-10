import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas

root = Tk()
root.title('FYP GUI - Merge Datasets')
root.geometry("450x550")

#create dataframes which I will add the imported csv data to
HR_df = pandas.DataFrame()
GUI_df = pandas.DataFrame()

def import_HR():
    HR_file_path = filedialog.askopenfilename(title = "Import Athlete HR Data") #get the path of the csv file with the users data
    HR_df = pandas.read_csv(HR_file_path) #read csv file data to the established dataframe
    HR_file_name = os.path.basename(HR_file_path) #pull the file name from the file path
    HR_file_name_label = Label(wrapper1, text = HR_file_name) #create label with file name
    HR_file_name_label.pack() #print the file name so the user receives confirmation of which dataset they have imported

def import_GUI(): #the same as the above code but for importing the dataset from the other GUI I made as part of this FYP
    GUI_file_path = filedialog.askopenfilename(title = "Import User Inputed Data")
    GUI_df = pandas.read_csv(GUI_file_path)
    GUI_file_name = os.path.basename(GUI_file_path)
    GUI_file_name_label = Label(wrapper2, text = GUI_file_name)
    GUI_file_name_label.pack()

def run_program(): #merge the datasets into one
    print("hello world")


#everything below just displays the buttons and text in a neat format
button_frame = Frame(root)

wrapper1 = LabelFrame(root, text = 'HR Data')
wrapper2 = LabelFrame(root, text = 'GUI Data')
wrapper3 = LabelFrame(root, text = 'Run Program')

import_HR_button = Button(wrapper1, text = "Import HR Data", command = import_HR)
import_GUI_button = Button(wrapper2, text = "Import GUI Data", command = import_GUI)
run_program_button = Button(wrapper3, text = "Run Program", command = run_program)

wrapper1.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper2.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper3.pack(fill='both', expand='yes', padx=20, pady=20)

import_HR_button.pack(pady=10)
import_GUI_button.pack(pady=10)
run_program_button.pack(pady=10)

root.mainloop()