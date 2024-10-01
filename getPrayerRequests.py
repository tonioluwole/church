import requests
import json
import os
from datetime import date
from time import sleep
import tkinter
import google.auth
from tkinter import font
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import gspread
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials


#Auth codes and constants
clientid='5ef5d12e37f08560522e850519259a5c03430635b3ac60b2477d0476a0cb52cc'
secret="a4eafc69b2b5517f3016adb2a899eda397b7cdb2997b8c6db2a18b6bfb22840c"
navy = "#174EA6"
grey = "#9AA0A6"
yellow = "#FBBC04"
white = '#ffffff'
black = "black"
username = os.getlogin()

#Get todays date to write to file name
t= date.today()
today=t.strftime('%m-%d-%Y')

#Function to display all tkinter fonts
def allfonts():
    root = Tk()
    root.title('Font Families')
    fonts=list(font.families())
    fonts.sort()

    def populate(frame):
        '''Put in the fonts'''
        listnumber = 1
        for i, item in enumerate(fonts):
            label = "listlabel" + str(listnumber)
            label = Label(frame,text=item,font=(item, 16))
            label.grid(row=i)
            label.bind("<Button-1>",lambda e,item=item:copy_to_clipboard(item))
            listnumber += 1

    def copy_to_clipboard(item):
        root.clipboard_clear()
        root.clipboard_append("font=('" + item.lstrip('@') + "', 12)")

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = Canvas(root, borderwidth=0, background="#ffffff")
    frame = Frame(canvas, background="#ffffff")
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    populate(frame)

    root.mainloop()
    #END of all fonts

def prayerrequests():
    #Google Sheets ID and API key
    SHEET_ID = '1pKHV9YA1_Zb1HkCmfzHpKVctOrbF3qRqw8YiwFGmye4'
    API_KEY = 'AIzaSyCfHCY7oC3ymy4Sh8jBWZ5I2_332U_si2o'

    url1 = 'https://script.google.com/macros/s/AKfycbzUsruUUeTqxxqD3sQe_x6woi0nsMoSYMCv3iFWIaYYeUlfxUYc0s62_3GZl1I2WrqRZA/exec'
    requests.get(url1)

    # The range you want to access (e.g., 'Form responses 1!A1:Z')
    RANGE = 'Prayers!A2:C'

    # Construct the API URL
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{RANGE}?key={API_KEY}'

    # Make the GET request to the Google Sheets API
    response = requests.get(url)
    filepath = "C:\\Users\\"+username+"\\Desktop\\Prayer Requests\\"+today+"'s requests from Google Forms.txt"

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print (data)
        # Get the rows from the response
        rows = data.get('values', [])
        
        # Save the rows to a text file
        with open(filepath, 'w+') as file:
            
            for row in rows:
                tary = ''.join(row)+'\n'
                file.write("\n"+tary[10:])
        
        print("Responses saved to "+filepath)
    else:
        print(f"Error: {response.status_code}, {response.text}")

    requestsfile=open(filepath)
    gottenrequests = requestsfile.read()

    #os.startfile(filepath)

    """
    ------------------------- START OF GUI / Tkinter ---------------------------
    """

    #Constants for GUI
    root = Tk()  # create a root widget

    root.title("Prayer Requests")
    root.configure(background=navy)
    root.minsize(200, 200)  # width, height
    root.maxsize(1200, 800)
    root.geometry("600x600+660+240")  # width x height + x + y

    Body_font = ("Malgun Gothic", 14,) 
    Label_font = ("Malgun Gothic", 18, 'bold') 

    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill=Y)
    ###################

    Mainlabel=Label(font=Label_font,text="Prayer Requests",background=yellow, foreground=black,height=2, borderwidth=2, relief="groove")
    Mainlabel.pack(fill='both', expand=False)

    text = Text(root, yscrollcommand = scrollbar.set)
    text.insert(INSERT,gottenrequests)
    text.configure(font=Body_font,state=DISABLED, background=navy, foreground='White', borderwidth=0)
    text.pack(fill='both', expand=True,padx=(50,50))
    scrollbar.config( command = text.yview)
    
    root.mainloop()

#Loop to refresh app and get new requests, plan is to make it a button within the app
def container():
    prayerrequests()
    yes = messagebox.askyesno('','Refresh prayer requests?')
 
    while True:
        if yes == True:
            container()
        else:
                quit()

container()
"""
#for me
def ask () :
    jack = input("\n1 for fonts \n2 for app\n3 to quit\n\n")
    if jack == "1":
        allfonts()
        ask()
    elif jack == "2":
        container()
        ask()
    elif jack =="3":
        quit()
    else:
        print("Wrong answer\n")
        ask()

ask()
"""