import json
import PySimpleGUI as sg
from datetime import datetime
import requests
#import csv
#import time

sg.theme('BlueMono')  # PySimpleGui theme

def get_data():
   
    #Open the ship type lookup table
    r = open('type.json')   
    rows = json.load(r)
      
    #get the api data
    url = "https://data.aishub.net/ws.php"
    
    headers = ""
    
    params = {
        "username":"USERNAME",
        "format":"1",
        "output":"json",
        "format":"1",
        "latmin":"54.15276",
        "latmax":"56.01030",
        "lonmin":"-4.484445",
        "lonmax":"-4.484445",
    }

    response = requests.get(url, params=params, headers=headers)
    #Open the API json 
    d = response.json()  
    
    #Loop through the data, collecting the Name and Type of each ship and assign to the data 
    #look up the TYPE in the "rows" lookup table to get the type of boat
    data=[]
    for r in d[1]:
         data.append([r["NAME"],(rows[str(r["TYPE"])])]) 
    return data 

def get_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

#Get the Date, data and headings
dt_string = get_date()
data = get_data()
headings = ["name","type"]

#Put it in a table
layout = [
    [sg.Text("*** BOATS OUTSIDE ***")],
    [sg.Text("Last refresh at "), sg.Text(dt_string, key='DATE')],
    [sg.Table(data, headings=headings, auto_size_columns=False, def_col_width = 20, num_rows=20, justification='left', key='TABLE')],
    [sg.Button("Exit", pad = 5)]
    ]

window = sg.Window("Title", layout, finalize=True)
date, table, end = window['DATE'], window['TABLE'], window['Exit']

# Create an event loop
while True:
    event, values = window.read(timeout=120000) # loops every X milliseconds
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    dt_string = get_date()  # get the date
    data = get_data()       # get the data
    date.update(dt_string)  # Update the date
    table.update(data)      # Update the table
    
window.close()
