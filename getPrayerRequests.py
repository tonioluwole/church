import requests
import json
import os
from datetime import date
from time import sleep
import tkinter
from tkinter import font
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo


#Auth codes and constants
clientid='5ef5d12e37f08560522e850519259a5c03430635b3ac60b2477d0476a0cb52cc'
secret="a4eafc69b2b5517f3016adb2a899eda397b7cdb2997b8c6db2a18b6bfb22840c"
navy = "#111827"
grey = "#28282f"
white = '#ffffff'
username = os.getlogin()

#Get todays date to write to file name
t= date.today()
today=t.strftime('%m-%d-%Y')

def prayerrequests():
    #API Call to get json data
    x = requests.get('https://api.planningcenteronline.com/people/v2/forms/818055/form_submissions?include=form_submission_values', 
    auth=(clientid,secret))

    # print("x= ",x.status_code)
    # 200 Success.
    # 301 Moved Permanently: site moved, redirect.
    # 302 Found: Temporary redirect.
    # 400 Bad Request: Client error.
    # 401 Unauthorized: Authentication needed.
    # 403 Forbidden: Access denied.
    # 404 Not Found: Resource missing.
    # 500 Internal Server Error: Server issue.
    # 503 Service Unavailable: Server overloaded or down.. 

    #Convert request to JSON data called json_data
    json_data = x.json()

    #Converts data to python object
    json_object=json.loads(json.dumps(json_data))

    #loop through and get the "display value" value from json data then write it to file. Should be the form submission
    filepath = "C:\\Users\\"+username+"\\Desktop\\"+today+"'s Prayer requests.txt" #Writes to desktop folder of PC running application
    with open(filepath, 'w+') as f: 
        for i in json_object["included"]:
            print ("--------\n",i["attributes"]['display_value'])
            f.write(str("---------\n" + i["attributes"]['display_value']) + "\n\n" )

    requestsfile=open(filepath)

    gottenrequests = requestsfile.read()
    #takes contents of textfile and creates string object

    #alternative to GUI window creation
    #os.startfile(filepath)

    """
    ------------------------- START OF GUI / Tkinter ---------------------------
    """
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

    #Constants for GUI
    root = Tk()  # create a root widget

    root.title("Prayer Requests")
    root.configure(background=navy)
    root.minsize(200, 200)  # width, height
    root.maxsize(1200, 800)
    root.geometry("600x600+660+240")  # width x height + x + y

    Body_font = ("YU Gothic UI", 14,) 
    Label_font = ("YU Gothic UI", 18, 'bold') 

    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill=Y)
    ###################

    Mainlabel=Label(font=Label_font,text="Prayer Requests",background=grey, foreground=white,height=2, borderwidth=2, relief="groove")
    Mainlabel.pack(fill='both', expand=False)

    text = Text(root, yscrollcommand = scrollbar.set)
    text.insert(INSERT,gottenrequests)
    text.configure(font=Body_font,state=DISABLED, background=navy, foreground='White', borderwidth=0)
    text.pack(fill='both', expand=True,padx=(50,50))
    scrollbar.config( command = text.yview)
    
    root.mainloop()

    yes = messagebox.askyesno('','Refresh prayer requests?')
    return yes

prayerrequests()

#Loop to refresh app and get new requests, plan is to make it a button within the app
if prayerrequests() == True:
    prayerrequests()
else:
    quit()

