import csv
from tkinter import *

root = Tk()
root.title('FYP GUI')
root.geometry("200x450")

# stage text box settings
stage_title_label = Label(root, text = 'Stage')
stage_textbox = Text(root, width = 5, height = 2, font = ("Helvetica", 9))

###submit button. this turns text input into variables and clears text boxes
##define functions
#get text from text box
def get_text():
    stage_label.config(text=stage_textbox.get(1.0, END)), stage_textbox.delete(1.0, END)
    blood_lactate_label.config(text=blood_lactate_textbox.get(1.0, END)), blood_lactate_textbox.delete(1.0, END)
    velocity_label.config(text=velocity_textbox.get(1.0, END)), velocity_textbox.delete(1.0, END)



##create button
button_frame = Frame(root)

get_text_button = Button(button_frame, text="Submit", command = get_text)
get_text_button.grid(row=1, column=1, padx=5)

#labels
stage_label = Label(root, text = '')
blood_lactate_label = Label(root, text = '')
velocity_label = Label(root, text = '')

#---------------------
#blood lactate textbox and title
blood_lactate_title_label = Label(root, text = 'Blood Lactate')
blood_lactate_textbox = Text(root, width = 5, height = 2, font = ("Helvetica", 9))
#---------------------
#velocity text box and title
velocity_title_label = Label(root, text = 'Velocity')
velocity_textbox = Text(root, width = 5, height = 2, font = ("Helvetica", 9))
#---------------------
#layout
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
#---------------------

root.mainloop()

"""
file = open('C:\\Users\\harry\\OneDrive\\Documents\\college\\fyp\\data.csv', 'w', newline='')

header = ['stage', 'power', 'blood lactate']

data = ['1', '100', '1.1']

data2 = ['2', '120', '1.2']

writer = csv.writer(file)
writer.writerow(header)
writer.writerow(data)
writer.writerow(data2)


file.close()
"""
