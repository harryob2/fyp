# fyp

5/5/22

heres a link to a video explaining this project: https://youtu.be/btaakw9Dnvg
heres a link to a google drive with accompanying files and a exe file to run the code without python: https://drive.google.com/drive/folders/1JfUs_2jM3s7dBMRaCIKQ5yPjo4wWUUVJ?usp=sharing

here is a link to my conversion of this into a web app (WIP):
https://github.com/harryob2/fyp-web-app

in a nutshell, the program is for recording data, and merging the user-created dataset with another dataset to output a pdf data analytics report. 

it is used to speed up the incremental exercise test process.

#

16/12/21

this is my final year project. My supervisor Neil does physical assessments of athletes. 
the physical assessment involves putting the athlete on a treadmill and measuring their heart rate, VO2, and blood lactate at different speeds
athletes use this info to inform their training routine to increase training efficiency

the assessment is conducted entirely on a treadmill over the course of 15-20 minutes
at each discrete stage of the assessment he increases the speed of the treadmill, waits 3 minutes, and collects blood lactate data.
Heart rate data and VO2 data is collected digitally and automatically exported to a csv file. 

my supervisor Neil has to tediously collate all this data into 1 dataset manually, and calculate a bunch of secondary metrics and graphs manually
I will create a program to do this automatically

First, I will create a GUI that will ask Neil for the blood lactate and speed data at different stages of the assessment.
it will then ask neil to upload the heart rate and VO2 dataset to the GUI
The program will create one single dataset, with the inputted data from the GUI and the uploaded data from the dataset
I will automate the calculation of secondary metrics (VO2 max etc) once I have successfully created a program that combines the datasets
