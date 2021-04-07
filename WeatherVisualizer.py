# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:34:52 2021

@author: jared
"""

import tkinter
from typing import Callable
import mysql.connector
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


SQLuser = 'ceis110'
SQLpass = 'ceis110'
SQLhost = '10.10.120.1'
SQLdb = 'ceis110'

## SOONER: Optimize to function or just setup functions for Panda to reshape dataset?
conn = mysql.connector.connect(user=SQLuser, password=SQLpass, host=SQLhost, database=SQLdb)
cursor = conn.cursor(dictionary=True)
query = 'SELECT * FROM observations'
cursor.execute(query,())
sqlResult = cursor.fetchall()




#Tkinter GUI


def init_gui(root, update_function: Callable) -> FigureCanvasTkAgg:
    
    def lineBtn():
        global canvas
        figure = draw_lineChart()
        canvas.figure = figure
        canvas.draw()
        sns.set()
        
    def violinBtn():
        global canvas
        figure = draw_violinPlot()
        canvas.figure = figure
        canvas.draw()
        sns.set()

    # create empty figure and draw
    init_figure = draw_violinPlot()
    canvas = FigureCanvasTkAgg(init_figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
       
    
    root.winfo_toplevel().title("Weather Visualization")
    buttonViolin = tkinter.Button(root, text = "Violin Chart", command=violinBtn)
    buttonViolin.pack(side='left')     
    buttonSubmit = tkinter.Button(root, text = "Line Chart", command=lineBtn)
    buttonSubmit.pack(side='left')
    
    
    return canvas
  

## LATER:
# Just straight up figure out how to clean up alllllll of plot drawing.
def draw_violinPlot() -> Figure:
    # generate some data
    pdResult = pd.DataFrame(sqlResult)
    pdResult['shortDate']= pd.to_datetime(pdResult['timestamp'])
    pdResult['shortDate'] = pdResult['shortDate'].apply(lambda x:x.date().strftime('%m%d%y'))
    pdResult.set_index('shortDate')
    labels = pdResult['shortDate'].unique()
    del pdResult['timestamp']
         
    # plot the data
    figure = Figure(figsize=(8, 4.5), dpi=128)
    figure.subplots_adjust(top=.95, bottom=.25)
    ax = figure.subplots()
    sns.color_palette('tab10')
    sns.violinplot(data = pdResult, ax=ax, x='shortDate', y='temperature')
    ax.set(xlabel='Date', ylabel='Temperature')
    ax.set_xticklabels(labels, rotation=45, horizontalalignment='right')
    return figure

def draw_lineChart() -> Figure:
    #generate
    pdResult = pd.DataFrame(sqlResult)
    pdResult['shortDate']= pd.to_datetime(pdResult['timestamp'])
    pdResult['shortDate'] = pdResult['shortDate'].apply(lambda x:x.date().strftime('%m%d%y'))
    pdResult.set_index('shortDate')
    labels = pdResult['shortDate'].unique()
    del pdResult['timestamp']
    
    
    #plot
    figure = Figure(figsize=(8, 4.5), dpi=128)
    figure.subplots_adjust(top=.95, bottom=.25)
    ax = figure.subplots()
    sns.color_palette('tab10')
    sns.lineplot(data=pdResult, ax=ax, x='shortDate', y='temperature', label='Temperature' )
    sns.lineplot(data=pdResult, ax=ax, x='shortDate', y='relativeHumidity', label='Humidity')
    ax.set(xlabel='Date', ylabel='Value')
    ax.set_xticklabels(labels, rotation=45, horizontalalignment='right')
    ax.legend()
    return figure


    

root = tkinter.Tk()

canvas = init_gui(root, update_function=draw_violinPlot())

tkinter.mainloop()
    
    



