import pandas as pd
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF
from scipy.interpolate import interp1d

# basic info
root = Tk()
root.title('Incremental Exercise Testing Software')
root.geometry("700x850")

# code for having multiple tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack()
exercise_gui_tab = Frame(my_notebook)

# ====================================================
# ====================================================
# CODE PART 1: EXERCISE TEST TAB
# ====================================================
# ====================================================


# make string variable for column 3 heading, which user can change
column_3_heading = StringVar(root, "Velocity (km/h)")

# global variable for data to export
column_headings = ['Stage', 'Blood Lactate', column_3_heading.get(), 'Stage Finish Time']
user_data = pd.DataFrame(columns=column_headings)

# create big background squares to organize all of our little boxes and buttons
wrapper1 = LabelFrame(exercise_gui_tab, text='Data Entry Form')
wrapper2 = LabelFrame(exercise_gui_tab, text='Exercise Data Table')
stage_finish_textboxes_frame = Frame(wrapper1, borderwidth=2)


# define tab order
def tab_order():
    widgets = [blood_lactate_textbox, velocity_textbox, stage_finish_textboxes_frame, get_text_button]
    for w in widgets:
        w.lift()

# Set style for treeview
style = ttk.Style()
style.configure('Treeview')
style.map('Treeview')

# make tree
user_data_tree = ttk.Treeview(wrapper2, columns=('Stage', 'Blood Lactate',
                                                 column_3_heading.get(), 'Stage Finish Time'))

user_data_tree.tag_configure('oddrow', background="lightblue")


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

# stage  title
stage_title_label = Label(wrapper1, text='Stage')
stage_new_label = Label(wrapper1, text='0 (warm-up)') # special label at beginning
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

# get text from text box
def get_text():
    # text validation
    try:
        bl_tv = float(blood_lactate_var.get())  # shortened variable names for brevity's sake, tv stands for
        vl_tv = float(velocity_var.get())       # text validation
        sftm_tv = float(stage_finish_time_minute_var.get())
        sfts_tv = float(stage_finish_time_second_var.get())
    except ValueError:
        messagebox.showerror('Error', 'Only numbers can be inputted.') # shows error if any of the inputted data isn't a number
    if 0 <= bl_tv <= 20:
        if (0 <= vl_tv <= 40 and column_3_heading.get() == 'Velocity (km/h)') or (0 <= vl_tv <= 900 and column_3_heading.get() == 'Power (W)'):
            if 0 <= sftm_tv <= 59 and 0 <= sfts_tv <= 59 and len(stage_finish_time_second_var.get()) == 2:
                # only runs function if it passes all the text validation
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

                # add record to treeview
                user_data_tree.insert(index='end', values=row_list, parent='', tags=('oddrow',))

                iid += 1
                global user_data
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
            else:
                messagebox.showerror('Error', 'Invalid Stage Finish Time entry.')
        else:
            messagebox.showerror('Error', f'Invalid {column_3_heading.get()} entry.')
    else:
        messagebox.showerror('Error', 'Invalid Blood Lactate entry.')

def export():
    user_data.to_csv(
        filedialog.asksaveasfilename(title="Export to CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                                     defaultextension=".csv"), index=False)

def select_record():
    # empty the text boxes
    blood_lactate_textbox.delete(0, END)
    velocity_textbox.delete(0, END)
    stage_finish_time_minute_textbox.delete(0, END)
    stage_finish_time_second_textbox.delete(0, END)

    # Grab record number
    selected = user_data_tree.focus()
    values = user_data_tree.item(selected, 'values')

    def get_minute_value(stage_finish_time_value):
        if stage_finish_time_value[3] == 0:
            stage_finish_time_value_minute = stage_finish_time_value[4]

        else:
            stage_finish_time_value_minute = stage_finish_time_value[3:5]

        return stage_finish_time_value_minute


    # Update text boxes
    blood_lactate_textbox.insert(0, values[1])
    velocity_textbox.insert(0, values[2])
    stage_finish_time_minute_textbox.insert(0, get_minute_value(values[3]))
    stage_finish_time_second_textbox.insert(0, (values[3])[6:8])

    # Update stage
    stage_var_temp = values[0]
    stage_new_label.config(text=stage_var_temp)

def update_record():
    # Grab record number
    selected = user_data_tree.focus()
    values = user_data_tree.item(selected, 'values')

    # Function to make stage finish time variable
    def make_stage_time_update(stage_finish_time_value_minute, stage_finish_time_value_second):
        if (values[3])[3] == '0':
            stage_finish_time_value = '00:' + stage_finish_time_value_minute + ':' + stage_finish_time_value_second
        else:
            stage_finish_time_value = '00:0' + stage_finish_time_value_minute + ':' + stage_finish_time_value_second

        return stage_finish_time_value

    stage_finish_time_value = make_stage_time_update(stage_finish_time_minute_textbox.get(),
                                                     stage_finish_time_second_textbox.get()
                                                     )

    # Save new data to tree
    user_data_tree.item(selected, text='', values=(values[0],
                                                   blood_lactate_textbox.get(),
                                                   velocity_textbox.get(),
                                                   stage_finish_time_value,
                                                   )
                        )

    # Update dataframe
    blood_lactate = blood_lactate_var.get()
    velocity = velocity_var.get()
    stage = values[0]
    row_list = [stage, blood_lactate, velocity, stage_finish_time_value]
    row_number = int(selected[3])-1
    user_data.iloc[row_number] = row_list

    # Empty the text boxes
    blood_lactate_textbox.delete(0, END)
    velocity_textbox.delete(0, END)
    stage_finish_time_minute_textbox.delete(0, END)
    stage_finish_time_second_textbox.delete(0, END)

    # Update Stage label
    stage_new_label.config(text=stage_var)

def use_data_now():
    my_notebook.select(generate_report_tab)
    global GUI_df
    GUI_df = user_data
    GUI_df[GUI_df.columns[0:3]] = GUI_df.iloc[:, 0:3].astype('float32')
    GUI_file_name_label.config(text='Data from Exercise Testing tab imported successfully.')


# create buttons
get_text_button = Button(wrapper1, text="Add Record", command=get_text)

table_edit_frame = Frame(wrapper2, borderwidth=2)
export_button = Button(table_edit_frame, text="Export as .csv", command=export)
select_record_button = Button(table_edit_frame, text='Select Record', command=select_record)
update_record_button = Button(table_edit_frame, text='Update Record', command=update_record)
use_data_now_button = Button(table_edit_frame, text='Use Data Now', command=use_data_now)

# labels
stage_finish_time_label = Label(wrapper1, text='Stage Finish Time (MM:SS)')


# =================================================================
# =================================================================
# CODE PART 2: GENERATE REPORT TAB
# =================================================================
# =================================================================

x = 0

generate_report_tab = Frame(my_notebook)


# frames where I will place everything later
wrapper21 = LabelFrame(generate_report_tab, text='COSMED Data')
wrapper22 = LabelFrame(generate_report_tab, text='GUI Data')
wrapper23 = LabelFrame(generate_report_tab, text='Generate Report')

# create dataframes which I will add the imported csv data to
HR_df = pandas.DataFrame()
GUI_df = pandas.DataFrame()

# make a blank label, which will be updated with the below function import_HR. This means that if the user uploads
# the wrong file and wants to change it, the label updates to reflect this
HR_file_name = StringVar(root, " ")
HR_file_name_label = Label(wrapper21, text=HR_file_name.get())  # create label with file name
HR_file_name_label.pack()  # print the file name so the user receives confirmation of which dataset they have imported


def import_HR():
    global HR_df  # call the global variable to use inside the function
    HR_file_path = filedialog.askopenfilename(
        title="Import Athlete COSMED Data")  # get the path of the csv file with the users data
    HR_df = pandas.read_csv(HR_file_path, encoding='unicode_escape')  # read csv file data to the established dataframe
    global HR_file_name
    HR_file_name.set(os.path.basename(HR_file_path))  # pull the file name from the file path
    HR_file_name_label.config(
        text=HR_file_name.get() + ' imported successfully.')  # update the label to ensure it represents the most recently imported dataframe


# doing the same for the GUI label as I did for the HR label
GUI_file_name = StringVar(root, " ")
GUI_file_name_label = Label(wrapper22, text=GUI_file_name.get())  # create label with file name
GUI_file_name_label.pack()  # print the file name so the user receives confirmation of which dataset they have imported


def import_GUI():  # the same as the above code but for importing the dataset from the other GUI I made as part of this FYP
    global GUI_df
    GUI_file_path = filedialog.askopenfilename(title="Import User Inputted Data")
    GUI_df = pandas.read_csv(GUI_file_path, index_col=False)
    global GUI_file_name
    GUI_file_name.set(os.path.basename(GUI_file_path))
    GUI_file_name_label.config(text=GUI_file_name.get() + ' imported successfully.')


def run_program():  # merge the datasets into one
    if len(HR_df.index) > 0 and len(
            GUI_df.index) > 0:  # function will only run if datasets have been loaded successfully

        # inform user that the report is loading
        report_loading_label.config(text='Loading Report')

        # ========================================
        # Create folder to store report
        # ========================================
        report_folder_parent = filedialog.askdirectory(title='Where would you like to save the report?')
        global athlete_name
        athlete_name = HR_df.iloc[1, 1] + " " + HR_df.iloc[0, 1]
        global report_folder_path
        report_folder_path = os.path.join(report_folder_parent, athlete_name)
        os.mkdir(report_folder_path)
        global plot_folder_path
        plot_folder_path = os.path.join(report_folder_path, "plots")
        os.mkdir(plot_folder_path)

        HR_df_clean = HR_df.drop([0, 1])
        HR_df_clean = HR_df_clean.reset_index(
            drop=True)  # the index numbers 1 and 2 get removed when I run the above line. I want to keep them,
        # otherwise it interferes with my ability to merge this dataframe with the other dataframe with the GUI data
        # later
        cols = np.r_[0:9, 25:30, 41:45, 46, 49:58, 64, 65, 70, 75:107, 109:117, 119, 121,
               125:128]  # these are all the columns with useless data in HR_df that I want to remove
        global HR_df_cleaner
        HR_df_cleaner = HR_df_clean.drop(HR_df_clean.columns[cols], axis=1)

        global stage_column
        stage_list = ['Stage', '', '']
        stage_column = pandas.DataFrame(stage_list)
        global GUI_stage_rows
        GUI_stage_rows = []
        GUI_velocity_rows = []
        global GUI_blood_lactate_rows
        GUI_blood_lactate_rows = []

        global x
        x = 0
        global stage_change_index
        stage_change_index = []
        for i in range(len(HR_df_cleaner)):
            if datetime.strptime(HR_df_cleaner.iloc[i][0], "%H:%M:%S") < datetime.strptime(
                    GUI_df.iloc[len(GUI_df) - 1][3],
                    "%H:%M:%S"):  # discards all values taken after test was finished
                if x + 1 <= len(GUI_df):
                    if datetime.strptime(HR_df_cleaner.iloc[i][0], "%H:%M:%S") <= datetime.strptime(GUI_df.iloc[x][3],
                                                                                                    "%H:%M:%S"):
                        GUI_stage_rows.append(GUI_df.iloc[x][0])
                        GUI_velocity_rows.append(GUI_df.iloc[x][2])
                        GUI_blood_lactate_rows.append(GUI_df.iloc[x][1])
                    else:
                        x += 1
                        stage_change_index.append(i)
                        GUI_stage_rows.append(GUI_df.iloc[x][0])
                        GUI_velocity_rows.append(GUI_df.iloc[x][2])
                        GUI_blood_lactate_rows.append(GUI_df.iloc[x][1])

        stage_df = pandas.DataFrame({'Stage': GUI_stage_rows})
        velocity_df = pandas.DataFrame({GUI_df.columns[2]: GUI_velocity_rows})

        blood_lactate_df = pandas.DataFrame({'Blood Lactate': GUI_blood_lactate_rows})

        # make new dataframe with all of the data merged
        global New_clean_df
        New_clean_df = pandas.concat([HR_df_cleaner, stage_df, velocity_df, blood_lactate_df], axis=1)

        global grouped
        New_clean_df['HR'] = pandas.to_numeric(New_clean_df['HR'])
        New_clean_df['VO2/Kg'] = pandas.to_numeric(New_clean_df['VO2/Kg'])

        grouped = New_clean_df.groupby('Stage', as_index=False).apply(lambda x: x.tail(
            int(0.33 * len(x))))  # group dataframe by stage, then remove everything except the last third of the values
        grouped = grouped.groupby('Stage').mean()  # find the mean of all the numeric values

        global athlete_stats_df
        athlete_stats_df = grouped.iloc[:, 0:2].join(GUI_df.iloc[:,
                                                     0:4])  # combine columns from 2 dataframes to create 1 dataframe
                                                            # with useful info for the report
        athlete_stats_df = athlete_stats_df.iloc[:,
                           [2, 4, 1, 0, 3, 5]]  # change the order of the columns to make it easier to understand
        athlete_stats_df['Stage Finish Time'] = athlete_stats_df['Stage Finish Time'].str[3:]

        # ======================================================
        # plots
        # ======================================================

        # making the path for each plot a global variable so it can be called in other functions
        global plot_1_path, plot_2_path, plot_3_path, plot_4_path, plot_5_path, plot_6_path

        # working hr & power/velocity vs time plot
        plt.figure(1)
        fig, hrt = plt.subplots()
        hrt.set_title('HR vs. ' + athlete_stats_df.columns[1])


        # formatting date
        hrt.xaxis_date()
        myFmt = md.DateFormatter('%M:%S')
        hrt.xaxis.set_major_formatter(myFmt)
        stage_time_array = np.squeeze(athlete_stats_df[['Stage Finish Time']].to_numpy())
        stage_time_array_dt = pandas.to_datetime(stage_time_array, format='%M:%S')
        stage_time_array_d2n = md.date2num(stage_time_array_dt)

        # HR data plot
        hr_array = np.squeeze(athlete_stats_df[['HR']].to_numpy())
        HR_data_plot = hrt.plot(stage_time_array_d2n, hr_array, marker='o', linestyle='none', label='HR Data')

        # HR interpolated line plot
        f = interp1d(stage_time_array_d2n, hr_array, kind='cubic')
        xnew = np.linspace(stage_time_array_d2n[0], stage_time_array_d2n[-1])
        HR_line_plot = hrt.plot(xnew, f(xnew), color='blue')

        # axes labels
        hrt.set_xlabel('Time in minutes')
        hrt.set_ylabel('HR', rotation=0, color='blue')

        # power/velocity data plot
        hrt2 = hrt.twinx()
        velocity_array = np.squeeze(athlete_stats_df.iloc[:, 1].to_numpy())
        velocity_data_plot = hrt2.plot(stage_time_array_d2n, velocity_array,
                                       label=athlete_stats_df.columns[1] + ' Data', marker='o', linestyle='none',
                                       color='red')
        hrt2.set_ylabel(athlete_stats_df.columns[1], color='red')
        hrt2.plot()

        # velocity/power interpolated line plot
        g = interp1d(stage_time_array_d2n, velocity_array, kind='cubic')
        velocity_line_plot = hrt2.plot(xnew, g(xnew), color='orange')

        # code for legend
        lns = HR_data_plot + velocity_data_plot
        labs = [l.get_label() for l in lns]
        hrt.legend(lns, labs, loc=0)
        hrt.axis(xmin = stage_time_array_d2n[1], xmax = stage_time_array_d2n[-1])

        plot_1_path = os.path.join(plot_folder_path, 'plot1.png')
        plt.savefig(plot_1_path)

        # working hr & blood lactate vs time plot
        plt.figure(2)
        fig, hrb = plt.subplots()
        hrb.set_title('HR vs. Blood Lactate')
        hrb.axis(xmin = stage_time_array_d2n[1], xmax = stage_time_array_d2n[-1])


        # formatting date
        hrb.xaxis_date()
        myFmt = md.DateFormatter('%M:%S')
        hrb.xaxis.set_major_formatter(myFmt)

        # HR data plot
        HR_data_plot = hrb.plot(stage_time_array_d2n, hr_array, marker='o', linestyle='none', label='HR Data')

        # HR interpolated line plot
        HR_line_plot = hrb.plot(xnew, f(xnew), color='blue')
        hrb.set_xlabel('Time in minutes')
        hrb.set_ylabel('HR', rotation=0, color='blue')

        # blood lactate data plot
        hrb2 = hrb.twinx()
        blood_lactate_array = np.squeeze(athlete_stats_df[['Blood Lactate']].to_numpy())
        blood_data_plot = hrb2.plot(stage_time_array_d2n, blood_lactate_array, label='Blood Lactate Data', marker='o',
                                    linestyle='none', color='green')
        hrb2.set_ylabel('Blood Lactate', color='green')

        # blood lactate interpolated line plot
        h = interp1d(stage_time_array_d2n, blood_lactate_array, kind='cubic')
        blood_line_plot = hrb2.plot(xnew, h(xnew), color='green')

        # code for legend
        lns = HR_data_plot + blood_data_plot
        labs = [l.get_label() for l in lns]
        hrb.legend(lns, labs, loc=0)

        plot_2_path = os.path.join(plot_folder_path, 'plot2.png')
        plt.savefig(plot_2_path)

        # blood lactate & power/velocity vs time
        plt.figure(3)
        fig, bp = plt.subplots()
        bp.set_title('Blood Lactate vs ' + athlete_stats_df.columns[1])
        bp.set_xlabel('Time in minutes')
        bp.axis(xmin = stage_time_array_d2n[1], xmax = stage_time_array_d2n[-1])

        # formatting date
        bp.xaxis_date()
        myFmt = md.DateFormatter('%M:%S')
        bp.xaxis.set_major_formatter(myFmt)

        # blood lactate plot
        blood_data_plot = bp.plot(stage_time_array_d2n, blood_lactate_array, label='Blood Lactate Data', marker='o',
                                  linestyle='none', color='green')
        blood_line_plot = bp.plot(xnew, h(xnew), color='green')
        bp.set_ylabel('Blood Lactate', color='green')

        # power/velocity plot
        bp2 = bp.twinx()
        velocity_data_plot = bp2.plot(stage_time_array_d2n, velocity_array, label=athlete_stats_df.columns[1] + ' Data',
                                      marker='o', linestyle='none', color='red')
        velocity_line_plot = bp2.plot(xnew, g(xnew), color='orange')
        bp2.set_ylabel(athlete_stats_df.columns[1], color='red')

        # code for legend
        lns = velocity_data_plot + blood_data_plot
        labs = [l.get_label() for l in lns]
        bp.legend(lns, labs, loc=0)

        plot_3_path = os.path.join(plot_folder_path, 'plot3.png')
        plt.savefig(plot_3_path)

        # HR and VO2 vs time
        plt.figure(4)
        fig, hrv = plt.subplots()
        hrv.set_title('Heart Rate vs. VO2')
        hrv.axis(xmin = stage_time_array_d2n[1], xmax = stage_time_array_d2n[-1])


        # formatting date
        hrv.xaxis_date()
        myFmt = md.DateFormatter('%M:%S')
        hrv.xaxis.set_major_formatter(myFmt)

        # HR data plot
        HR_data_plot = hrv.plot(stage_time_array_d2n, hr_array, marker='o', linestyle='none', label='HR Data')

        # HR interpolated line plot
        HR_line_plot = hrv.plot(xnew, f(xnew), color='blue')
        hrv.set_xlabel('Time in minutes')
        hrv.set_ylabel('HR', rotation=0, color='blue')

        # VO2 data plot
        hrv2 = hrv.twinx()
        VO2_array = np.squeeze(athlete_stats_df[['VO2/Kg']].to_numpy())
        VO2_data_plot = hrv2.plot(stage_time_array_d2n, VO2_array, label='VO2 Data', marker='o', linestyle='none',
                                  color='deeppink')
        hrv2.set_ylabel('VO2', color='deeppink')

        # VO2 interpolated line plot
        k = interp1d(stage_time_array_d2n, VO2_array, kind='cubic')
        VO2_line_plot = hrv2.plot(xnew, k(xnew), color='deeppink')

        # code for legend
        lns = HR_data_plot + VO2_data_plot
        labs = [l.get_label() for l in lns]
        hrv.legend(lns, labs, loc=0)

        plot_4_path = os.path.join(plot_folder_path, 'plot4.png')
        plt.savefig(plot_4_path)

        # HR and BL vs power/velocity
        plt.figure(5)
        fig, hbp = plt.subplots()
        hbp.set_title('HR vs Blood Lactate')
        hbp.axis(xmin = velocity_array[1], xmax = velocity_array[-1])


        # HR data plot
        HR_data_plot = hbp.plot(velocity_array, hr_array, marker='o', linestyle='none', label='HR Data')

        # HR line plot
        j = interp1d(velocity_array, hr_array, kind='cubic')
        xnew = np.linspace(velocity_array[0], velocity_array[-1])
        HR_line_plot = hbp.plot(xnew, j(xnew), color='blue')
        hbp.set_xlabel(athlete_stats_df.columns[1])
        hbp.set_ylabel('HR', rotation=0, color='blue')

        # BL data plot
        hbp2 = hbp.twinx()
        blood_data_plot = hbp2.plot(velocity_array, blood_lactate_array, label='Blood Lactate Data', marker='o',
                                    linestyle='none', color='green')
        hbp2.set_ylabel('Blood Lactate', color='green')

        # BL line plot
        o = interp1d(velocity_array, blood_lactate_array, kind='cubic')
        blood_line_plot = hbp2.plot(xnew, o(xnew), color='green')

        # code for legend
        lns = HR_data_plot + blood_data_plot
        labs = [l.get_label() for l in lns]
        hbp.legend(lns, labs, loc=0)

        plot_5_path = os.path.join(plot_folder_path, 'plot5.png')
        plt.savefig(plot_5_path)

        # VO2 vs Blood Lactate
        plt.figure(6)
        fig, vbp = plt.subplots()
        vbp.set_title('VO2 vs Blood Lactate')
        vbp.axis(xmin = velocity_array[1], xmax = velocity_array[-1])

        # VO2 data plot
        VO2_data_plot = vbp.plot(velocity_array, VO2_array, marker='o', linestyle='none', label='VO2 Data')

        # VO2 line plot
        j = interp1d(velocity_array, VO2_array, kind='cubic')
        HR_line_plot = vbp.plot(xnew, j(xnew), color='blue')
        vbp.set_xlabel(athlete_stats_df.columns[1])
        vbp.set_ylabel('VO2', rotation=0, color='blue')

        # BL data plot
        vbp2 = vbp.twinx()
        blood_data_plot = vbp2.plot(velocity_array, blood_lactate_array, label='Blood Lactate Data', marker='o',
                                    linestyle='none', color='green')
        vbp2.set_ylabel('Blood Lactate', color='green')

        # BL line plot
        l = interp1d(velocity_array, blood_lactate_array, kind='cubic')
        blood_line_plot = vbp2.plot(xnew, l(xnew), color='green')

        # code for legend
        lns = VO2_data_plot + blood_data_plot
        labs = [l.get_label() for l in lns]
        vbp.legend(lns, labs, loc=0)

        plot_6_path = os.path.join(plot_folder_path, 'plot6.png')
        plt.savefig(plot_6_path)

        # =============================================
        # VO2 Max
        # =============================================
        VO2_rolling_mean = New_clean_df['VO2/Kg'].rolling(5, min_periods=5).mean()
        VO2_rolling_mean.dropna(inplace=True)
        VO2_Max = round(max(VO2_rolling_mean), 2)

        # =============================================
        # Create Athlete Info Table
        # =============================================
        athlete_info_index = HR_df.iloc[0:6, 0]
        athlete_info_index2 = HR_df.iloc[5:7, 3]
        athlete_info = HR_df.iloc[0:6, 1]
        athlete_info2 = HR_df.iloc[5:7, 4]
        athlete_info_df = pandas.DataFrame(athlete_info.values, index=athlete_info_index)
        athlete_info2_df = pandas.DataFrame(athlete_info2.values, index=athlete_info_index2)
        full_athlete_info_df = pandas.concat([athlete_info_df, athlete_info2_df])
        full_athlete_info_df.loc["VO2 Max"] = VO2_Max # add VO2 Max to table
        full_athlete_info_df.iloc[6,] = round(pandas.to_numeric(full_athlete_info_df.iloc[6,]), 2) # round to 2 dp

        plt.figure(7)
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        rcolors = plt.cm.BuPu(np.full(len(full_athlete_info_df), 0.2))
        table = ax.table(cellText=full_athlete_info_df.values,
                         rowLabels=full_athlete_info_df.index,
                         loc='center',
                         rowColours=rcolors)
        table.scale(1, 1.5)
        table.auto_set_column_width(col=list(range(len(full_athlete_info_df))))
        fig.tight_layout()
        global athlete_info_plot_path
        athlete_info_plot_path = os.path.join(plot_folder_path, 'athlete info table.png')
        fig.savefig(athlete_info_plot_path, bbox_inches='tight')

        # =============================================
        # Create Athlete Test Table
        # =============================================
        plt.figure(8)
        athlete_stats_df['HR'] = athlete_stats_df['HR'].astype(int)
        athlete_stats_df['VO2/Kg'] = athlete_stats_df['VO2/Kg'].astype(int)
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        ccolors = plt.cm.BuPu(np.full(len(athlete_stats_df.columns), 0.2))
        table = ax.table(cellText=athlete_stats_df.values,
                         # rowLabels = athlete_stats_df.index,
                         loc='center',
                         colLabels=athlete_stats_df.columns,
                         colColours=ccolors,
                         cellLoc='center'
                         )
        table.scale(1.5, 1.5)
        table.auto_set_column_width(col=list(range(len(athlete_stats_df))))
        fig.tight_layout()
        global athlete_test_table_path
        athlete_test_table_path = os.path.join(plot_folder_path, 'athlete test table.png')
        fig.savefig(athlete_test_table_path, bbox_inches='tight')

        create_analytics_report()

        report_loading_label.config(text='Report Ready!')   # update user that the report is ready
                                                            # to view

        # add button that user can click to open the report in browser
        view_report_button = Button(wrapper23, text='View Report', command=lambda: os.system('"' + report_path + '"'))
        view_report_button.pack(pady=10)


    else:  # if the datasets haven't run successfully the user is notified
        messagebox.showerror(title="Data not imported",
                             message="The datasets have not been successfully loaded. Please ensure you have selected the correct .csv files and try again.")


# source for report code: https://github.com/KeithGalli/generate-analytics-report

def create_title(day, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 24)
    pdf.ln(5)
    pdf.write(5, f"{athlete_name} Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(5)


def create_analytics_report():
    pdf = FPDF()  # A4 (210 by 297 mm)

    ''' First Page '''
    pdf.add_page()
    test_date = HR_df.iloc[0, 4]
    create_title(test_date, pdf)

    WIDTH = 210
    HEIGHT = 297

    pdf.image(athlete_test_table_path, 41, 18, 130)

    pdf.image(athlete_info_plot_path, -8, 95, WIDTH - 60)
    pdf.image(plot_6_path, WIDTH / 2, 110, WIDTH / 2 - 10)

    pdf.image(plot_1_path, 5, 200, WIDTH / 2 - 10)
    pdf.image(plot_2_path, WIDTH / 2, 200, WIDTH / 2 - 10)

    ''' Second Page '''
    pdf.add_page()

    pdf.image(plot_3_path, 5, 20, WIDTH / 2 - 10)
    pdf.image(plot_4_path, WIDTH / 2, 20, WIDTH / 2 - 10)

    pdf.image(plot_5_path, 5, 110, WIDTH / 2 - 10)
    # pdf.image(plot_6_path, WIDTH / 2, 110, WIDTH / 2 - 10)
    # the above code was left in should the user want to add
    # another plot to the report

    global report_path
    report_path = os.path.join(report_folder_path, f'{athlete_name} Report.pdf')
    pdf.output(report_path, 'F')


# ===================================================================
# Generate Report Tab Layout
# ===================================================================

exercise_gui_tab.pack()
generate_report_tab.pack()

my_notebook.add(exercise_gui_tab, text = 'Exercise Testing')
my_notebook.add(generate_report_tab, text = 'Generate Report')

button_frame = Frame(root)

import_HR_button = Button(wrapper21, text="Import COSMED Data", command=import_HR)
import_GUI_button = Button(wrapper22, text="Import GUI Data", command=import_GUI)
run_program_button = Button(wrapper23, text="Generate Report", command=run_program)

report_loading_label = Label(wrapper23, text='')

wrapper21.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper22.pack(fill='both', expand='yes', padx=20, pady=20)
wrapper23.pack(fill='both', expand='yes', padx=20, pady=20)

import_HR_button.pack(pady=10)
import_GUI_button.pack(pady=10)
run_program_button.pack(pady=10)
report_loading_label.pack(pady=10)

# =================================================================
# Exercise Testing Tab Layout
# =================================================================

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

table_edit_frame.pack()
select_record_button.pack(pady=10, padx=10, side=LEFT)
update_record_button.pack(pady=10, padx=10, side=LEFT)
use_data_now_button.pack(pady=10, padx=10, side=LEFT)
export_button.pack(pady=10, padx=10, side=LEFT)

user_data_tree.pack()
# ---------------------

tab_order()  # run tab order function on program start
blood_lactate_textbox.focus()  # make text input automatically start at first text box, the blood lactate textbox

root.mainloop()
