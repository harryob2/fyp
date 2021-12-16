import csv
from tkinter import *

root = Tk()
root.title('FYP GUI')
root.geometry("500x450")

# window settings
stage_text = Text(root, width = 40, height = 10, font = ("Helvetica", 16))
stage_text.pack(pady=20, padx=20)

###submit button. this turns text input into variables and clears text boxes
##define functions
#get text from text box
def get_text():
    stage_label.config(text=stage_text.get(1.0, END)), stage_text.delete(1.0, END)


##create button
button_frame = Frame(root)
button_frame.pack()

get_text_button = Button(button_frame, text="Submit", command = get_text)
get_text_button.grid(row=0, column=1, padx=20)

#labels
stage_label = Label(root, text = '')
stage_label.pack(pady=20)



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
