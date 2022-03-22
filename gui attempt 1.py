import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from datetime import datetime

# basic info
root = Tk()
root.title('FYP GUI')
root.geometry("700x850")

# make string variable for column 3 heading, which user can change
column_3_heading = StringVar(root, "Velocity (km/h)")

# global variable for data to export
column_headings = ['Stage', 'Blood Lactate', column_3_heading.get(), 'Stage Finish Time']
user_data = pd.DataFrame(columns=column_headings)

# create big background squares to organize all of our little boxes and buttons
# the names are currently poor, but I will change them later
wrapper1 = LabelFrame(root, text='Current Data')
wrapper2 = LabelFrame(root, text='Past Data')
stage_finish_textboxes_frame = Frame(wrapper1, borderwidth=2)


# define tab order
def tab_order():
    widgets = [blood_lactate_textbox, velocity_textbox, stage_finish_textboxes_frame, get_text_button]
    for w in widgets:
        w.lift()


# make tree
user_data_tree = ttk.Treeview(wrapper2, columns=('Stage', 'Blood Lactate', column_3_heading.get(), 'Stage Finish Time'))

user_data_tree.column('#0', width=0)
user_data_tree.column('Stage', width=130)
user_data_tree.column('Blood Lactate', width=130)
user_data_tree.column('#3', width=130)
user_data_tree.column('Stage Finish Time', width=170)

user_data_tree.heading('Stage', text='Stage')
user_data_tree.heading('Blood Lactate', text='Blood Lactate')
user_data_tree.heading('#3', text=column_3_heading.get())
user_data_tree.heading('Stage Finish Time', text='Stage Finish Time')

# settings for drop down menu
selected_sport = StringVar(root, "Running")


# this command changes the column 3 heading depending on which sport the athlete is being tested for
def test(sport):
    if sport == "Running":
        column_3_heading.set("Velocity (km/h)")
    else:
        column_3_heading.set("Power (W)")
    user_data.rename(columns={user_data.columns[2]: column_3_heading.get()}, errors="raise", inplace=True)
    user_data_tree.heading('#3', text=column_3_heading.get())
    user_data_tree.pack_forget()
    user_data_tree.pack()
    velocity_title_label.config(text=column_3_heading.get())


selected_sport_frame = Frame(wrapper1, borderwidth=2)
sport_options = ["Running", "Cycling", "Rowing", "Kayaking"]
selected_sport_dropdown = OptionMenu(selected_sport_frame, selected_sport, *sport_options, command=test)
selected_sport_label = Label(selected_sport_frame, text="Select Sport")

# define variables
stage_var = 0
blood_lactate_var = StringVar()
velocity_var = StringVar()
stage_finish_time_minute_var = StringVar()
stage_finish_time_second_var = StringVar()

# stage text box and title
stage_title_label = Label(wrapper1, text='Stage')
# stage_textbox = Entry(wrapper1, textvariable = stage_var, width = 5,font = ("Helvetica", 9))
stage_new_label = Label(wrapper1, text='0 (warm-up)')
# ---------------------
# blood lactate textbox and title
blood_lactate_title_label = Label(wrapper1, text='Blood Lactate')
blood_lactate_textbox = Entry(wrapper1, textvariable=blood_lactate_var, width=5, font=("Helvetica", 9))
# ---------------------
# velocity text box and title
velocity_title_label = Label(wrapper1, text=column_3_heading.get())
velocity_textbox = Entry(wrapper1, textvariable=velocity_var, width=5, font=("Helvetica", 9))
# ---------------------
# stage finish time text box and title
stage_finish_time_title_label = Label(wrapper1, text='Stage Finish Time')
stage_finish_time_minute_textbox = Entry(stage_finish_textboxes_frame, textvariable=stage_finish_time_minute_var,
                                         width=5, font=("Helvetica", 9))
stage_finish_time_second_textbox = Entry(stage_finish_textboxes_frame, textvariable=stage_finish_time_second_var,
                                         width=5, font=("Helvetica", 9))


###submit button. this turns text input into variables and clears text boxes
##define functions
# get text from text box
def get_text():
    # save the user input
    global stage_var
    stage = stage_var
    blood_lactate = blood_lactate_var.get()
    velocity = velocity_var.get()
    stage_finish_time_minute = stage_finish_time_minute_var.get()
    stage_finish_time_second = stage_finish_time_second_var.get()

    if len(stage_finish_time_minute) == 2:
        stage_finish_time = '00:' + stage_finish_time_minute + ':' + stage_finish_time_second
    else:
        stage_finish_time = '00:0' + stage_finish_time_minute + ':' + stage_finish_time_second

    # create list with user input and add as a row to csv file
    row_list = [stage, blood_lactate, velocity, stage_finish_time]
    iid = int(1)
    user_data_tree.insert(index='end', values=row_list, parent='')
    iid += 1

    global user_data
    # user_data = user_data.append(row_list, ignore_index = True)
    df_length = len(user_data)
    user_data.loc[df_length] = row_list
    # clear list values
    row_list.clear()

    # empty the text boxes
    blood_lactate_textbox.delete(0, END)
    velocity_textbox.delete(0, END)
    stage_finish_time_minute_textbox.delete(0, END)
    stage_finish_time_second_textbox.delete(0, END)

    # update the stage Variable
    stage_var += 1
    stage_new_label.config(text=stage_var)

    # return focus to first text box
    blood_lactate_textbox.focus()


def export():
    user_data.to_csv(
        filedialog.asksaveasfilename(title="Export to CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                                     defaultextension=".csv"), index=False)


# create buttons
get_text_button = Button(wrapper1, text="Submit", command=get_text)
export_button = Button(wrapper2, text="Export", command=export)

# labels
stage_finish_time_label = Label(wrapper1, text='Stage Finish Time (MM:SS)')

# layout
wrapper1.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper2.pack(fill='both', expand='yes', padx=20, pady=20)

selected_sport_frame.pack(pady=1)
selected_sport_label.pack(pady=(1, 1))
selected_sport_dropdown.pack(pady=1)

stage_title_label.pack(pady=(15, 1))
stage_new_label.pack(pady=1)

blood_lactate_title_label.pack(pady=(15, 1))
blood_lactate_textbox.pack(pady=1)

velocity_title_label.pack(pady=(15, 1))
velocity_textbox.pack(pady=1)

stage_finish_time_label.pack(pady=(15, 1))
stage_finish_textboxes_frame.pack()
stage_finish_time_minute_textbox.pack(pady=1, side=LEFT)
stage_finish_time_second_textbox.pack(pady=1, side=LEFT)

get_text_button.pack(pady=10)

export_button.pack(pady=10)

user_data_tree.pack()
# ---------------------

tab_order()  # run tab order function on program start
blood_lactate_textbox.focus()  # make text input automatically start at first text box, the blood lactate textbox

root.mainloop()
