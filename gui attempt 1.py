import csv
import os
from tkinter import *
from tkinter import ttk

##what to do next
#need to figure out how to export data to csv, everything else is cosmetic

#global variable for data to export
user_data = []

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


#create csv file, to which we will add user input
user_data_open = open('user_data.csv', 'w', newline = '')

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

    #clear list values
    row_list.clear()


#display the user input as a label
    stage_label.config(text=stage)
    blood_lactate_label.config(text=blood_lactate)
    velocity_label.config(text=velocity)

#empty the text boxes
    stage_textbox.delete(0, END)
    blood_lactate_textbox.delete(0, END)
    velocity_textbox.delete(0, END)


##create button
button_frame = Frame(root)

get_text_button = Button(button_frame, text="Submit", command = get_text)
get_text_button.grid(row=1, column=1, padx=5)


#labels
stage_label = Label(root, text = '')
blood_lactate_label = Label(root, text = '')
velocity_label = Label(root, text = '')


#layout
wrapper1.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper2.pack(fill='both', expand='yes', padx=20, pady=20)


stage_title_label.pack()
stage_textbox.pack(pady=5, padx=5)
stage_label.pack(pady=1)

blood_lactate_title_label.pack(pady=5)
blood_lactate_textbox.pack(pady=5)
blood_lactate_label.pack(pady=1)

velocity_title_label.pack(pady=5)
velocity_textbox.pack(pady=5)
velocity_label.pack(pady=1)

button_frame.pack(pady=5)

user_data_tree.pack()
#---------------------



file = open('C:\\Users\\harry\\OneDrive\\Documents\\college\\fyp\\data.csv', 'w', newline='')

header = ['stage', 'power', 'blood lactate']

data = ['1', '100', '1.1']

data2 = ['2', '120', '1.2']

writer = csv.writer(file)
writer.writerow(header)
writer.writerow(data)
writer.writerow(data2)


file.close()


root.mainloop()
