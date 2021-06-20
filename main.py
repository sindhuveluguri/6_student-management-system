import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import ImageTk, Image
import sys
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QWidget, QPushButton

from picdemo import textBox
def atten():
    root = Tk()
    root.title("Python - Import CSV File To Tkinter Table")
    width = 500
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    TableMargin = Frame(root, width=400)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Name","Time"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Name', text="Name", anchor=W)
    #tree.heading('AttendanceTime', text="Time", anchor=W)
    #tree.heading('Subject', text="Subject", anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)

    tree.pack()

    with open('Attendance.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Na = row['Name']
            #sub = row['Subject']
            tree.insert("", 0, values=(Na))
    root.mainloop()


def subject():
    root = Tk()
    root.geometry("600x400")

    def video_demo():
        path = 'Images'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        inputValue = textBox.get("1.0", "end-1c")
        print(inputValue)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            with open('Attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')

                    f.writelines(f'\n{name},{dtString},{inputValue}')

        encodeListKnow = findEncodings(images)
        print(len(encodeListKnow))

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

            facCurFrame = face_recognition.face_locations(imgSmall)
            encodeCurFrame = face_recognition.face_encodings(imgSmall, facCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facCurFrame):
                matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 32), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            cv2.imshow('webcam', img)

            if cv2.waitKey(10) == 27:
                break

    #def retrieve_input():
        #inputValue = textBox.get("1.0", "end-1c")
       # video_demo()
       # print(inputValue)

    textname = tk.Label(root, text='Enter Subject Name', font=('calibre', 10, 'bold'))

    textBox = Text(root, height=2, width=10)
    textname.grid(row=0, column=0)
    textname.pack()
    textBox.pack()
    #inputValue = textBox.get("1.0", "end-1c")
    buttonCommit = Button(root, height=1, width=10, text="Commit",command=video_demo)
    # command=lambda: retrieve_input() >>> just means do this when i press the button
    buttonCommit.pack()
    root.mainloop()


root = Tk()
root.geometry("800x1000")
root.configure(background="black")
#global inputValue
ri = Image.open("UI_Image/attendance.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(root, image=r)
label1.image = r
label1.place(x=100, y=270)

r = tk.Button(
    root,
    text="Take Attendance",
    command=subject,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=100, y=520)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(root, image=v)
label3.image = v
label3.place(x=600, y=270)

r = tk.Button(
    root,
    text="View Attendance",
    command=atten,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=600, y=520)

r = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=350, y=680)
root.mainloop()



# name_var = tk.StringVar()
#     def submit():
#             name = name_var.get()
#             print("The name is : " + name)
#             name_var.set("")
#
#     name_label = tk.Label(root, text='Enter Subject Name', font=('calibre', 10, 'bold'))
#     name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))
#
#     sub_btn = tk.Button(root, text='Submit', command=submit())
#
#     name_label.grid(row=0, column=0)
#     name_entry.grid(row=0, column=1)
#
#     sub_btn.grid(row=2, column=1)canvas = Canvas(width=400, height=250, bg='blue')
#canvas.pack()

#photo = PhotoImage(file='C:\\Users\\DELL\\Desktop\\opencvPics\\Mallika.ppm')
#canvas.create_image(0, 0, image=photo, anchor=NW)


# Button for closing
#exit_button1 = Button(root, text="View", command=video_demo)
#exit_button1.pack(pady=20)


#exit_button2 = Button(root, text="Attendance", command=atten)
#exit_button2.pack(pady=80)

#exit_button = Button(root, text="Exit", command=root.destroy)
#exit_button.pack(pady=60)




