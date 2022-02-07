import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd


##what to do next
#need to figure out how to export data to csv, everything else is cosmetic

#global variable for data to export
column_headings = ['Stage', 'Blood Lactate', 'Velocity']
user_data = pd.DataFrame(columns = column_headings)
#user_data = user_data.append(column_headings)
print(user_data)

root = Tk()
root.title('FYP GUI')
root.geometry("450x550")

#create big background squares to organize all of our little boxes and buttons
#the names are currently poor, but I will change them later
wrapper1 = LabelFrame(root, text = 'Current Data')
wrapper2 = LabelFrame(root, text = 'Past Data')


#make tree
user_data_tree = ttk.Treeview(wrapper2, columns=('Stage', 'Blood Lactate', 'Velocity'))
#user_data_tree['columns'] = ('Stage', 'Blood Lactate', 'Velocity')

user_data_tree.column('#0', width = 0)
user_data_tree.column('Stage', width = 130)
user_data_tree.column('Blood Lactate', width = 130)
user_data_tree.column('Velocity', width = 130)

user_data_tree.heading('Stage', text = 'Stage')
user_data_tree.heading('Blood Lactate', text = 'Blood Lactate')
user_data_tree.heading('Velocity', text = 'Velocity')


#define variables
stage_var = StringVar()
blood_lactate_var = StringVar()
velocity_var = StringVar()

# stage text box and title
stage_title_label = Label(wrapper1, text = 'Stage')
stage_textbox = Entry(wrapper1, textvariable = stage_var, width = 5,font = ("Helvetica", 9))
#---------------------
#blood lactate textbox and title
blood_lactate_title_label = Label(wrapper1, text = 'Blood Lactate')
blood_lactate_textbox = Entry(wrapper1, textvariable=blood_lactate_var, width = 5, font = ("Helvetica", 9))
#---------------------
#velocity text box and title
velocity_title_label = Label(wrapper1, text = 'Velocity')
velocity_textbox = Entry(wrapper1, textvariable=velocity_var, width = 5, font = ("Helvetica", 9))
#---------------------

###submit button. this turns text input into variables and clears text boxes
##define functions
#get text from text box
def get_text():

    #save the user input
    stage=stage_var.get()
    blood_lactate=blood_lactate_var.get()
    velocity=velocity_var.get()

    #create list with user input and add as a row to csv file
    row_list = [stage, blood_lactate, velocity]
    iid = int(1)
    user_data_tree.insert(index='end', values = row_list, parent='')
    iid += 1

    global user_data
    #user_data = user_data.append(row_list, ignore_index = True)
    df_length = len(user_data)
    user_data.loc[df_length] = row_list
    print(user_data)
    #clear list values
    row_list.clear()

#empty the text boxes
    stage_textbox.delete(0, END)
    blood_lactate_textbox.delete(0, END)
    velocity_textbox.delete(0, END)

    #stage_label.config(text=stage)
    #blood_lactate_label.config(text=blood_lactate)
    #velocity_label.config(text=velocity)


def export():
    user_data.to_csv(filedialog.asksaveasfilename(title="Export to CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), defaultextension=".csv"), index=False)

#display the user input as a label



##create button
button_frame = Frame(root)

get_text_button = Button(wrapper1, text="Submit", command = get_text)
#get_text_button.grid(row=1, column=1, padx=5)
export_button = Button(wrapper2, text="Export", command = export)


#labels
stage_label = Label(root, text = '')
blood_lactate_label = Label(root, text = '')
velocity_label = Label(root, text = '')


#layout
wrapper1.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper2.pack(fill='both', expand='yes', padx=20, pady=20)


stage_title_label.pack()
stage_textbox.pack(pady=5, padx=5)

blood_lactate_title_label.pack(pady=5)
blood_lactate_textbox.pack(pady=5)

velocity_title_label.pack(pady=5)
velocity_textbox.pack(pady=5)

get_text_button.pack(pady=10)

export_button.pack(pady=10)

user_data_tree.pack()
#---------------------




root.mainloop()
