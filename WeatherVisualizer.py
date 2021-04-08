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
from noaa_sdk import noaa
import datetime

SQLuser = 'ceis110'
SQLpass = 'ceis110'
SQLhost = '10.10.120.1'
SQLdb = 'ceis110'

zipCode = "95355"  
country = "US" 

## LATER: Functionize some of this stuff so the load time isn't so long
conn = mysql.connector.connect(user=SQLuser, password=SQLpass, host=SQLhost, database=SQLdb)
cursor = conn.cursor(dictionary=True)

# Get new data
query = 'SELECT MAX(timestamp) FROM observations'
cursor.execute(query,())
sqlResult = cursor.fetchall()
startDate = datetime.datetime.strptime(str(sqlResult[0]['MAX(timestamp)']), "%Y-%m-%dT%H:%M:%S%z" ).strftime("%Y-%m-%dT%H:%M:%SZ") #changed from - "%Y-%m-%dT00:00:00Z"
endDate = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ") #changed from - "%Y-%m-%dT23:59:59Z"
#print(startDate)
#print(endDate)
##Stolen from DB creation script
n = noaa.NOAA()
observations =  n.get_observations(zipCode,country,startDate,endDate)


insertQuery = """ REPLACE INTO observations 
                    (timestamp, windSpeed, temperature, relativeHumidity, 
                     windDirection, barometricPressure, visibility, textDescription)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s) """                       #changed ? to %s to fit MySQL/MariaDB standards
## LATER: Convert noaa dataset to pandas dataframe and insert once?
count = 0
for obs in observations:
    insertValues = (obs["timestamp"],
                    obs["windSpeed"]["value"],
                    obs["temperature"]["value"],
                    obs["relativeHumidity"]["value"],
                    obs["windDirection"]["value"],
                    obs["barometricPressure"]["value"],
                    obs["visibility"]["value"],
                    obs["textDescription"])
    cursor.execute(insertQuery, insertValues)
    count += 1
if count > 0:
    cursor.execute("COMMIT;")

#Now get full table

query = 'SELECT * FROM observations'
cursor.execute(query,())
sqlResult = cursor.fetchall()


# Set up pandas dataset
pdResult = pd.DataFrame(sqlResult)
pdResult['timestamp'] = pd.to_datetime(pdResult['timestamp']) - pd.Timedelta(hours=8)
pdResult['shortDate'] = pd.to_datetime(pdResult['timestamp']).apply(lambda x:x.date().strftime('%m/%d/%y')) #labels was shortDate
pdResult['barometricPressure'] = pdResult['barometricPressure'].astype(int) / 100
#pdResult['labels'] = pdResult['timestamp']
#pdResult['shortDate'] = pdResult['shortDate'].apply(lambda x:x.date().strftime('%m/%d/%y'))
pdResult.set_index('timestamp').sort_values(by='timestamp')
pdResultConst = pdResult.copy()
labels = pdResult['shortDate'].unique()
#print(pdResult['timestamp'])
#print(pdResult['timestamp']   - pd.Timedelta(hours=8))


#Pandas dataframe tailing - MAYBE: Map all global variable calls to passing arguments
def timeButton(days):
    global pdResult
    global pdResultConst
    global labels
    
    
    pdResult = pdResultConst.copy()
    endDate = datetime.datetime.now()
    startDate = datetime.datetime.now() - datetime.timedelta(days=days)
    endDate = endDate.strftime('%Y-%m-%dT%H:%M:%SZ')
    startDate = startDate.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(endDate)
    print(startDate)
    pdResult = pdResult[(pdResult['timestamp'] > startDate) & (pdResult['timestamp'] <= endDate)]
    #pdResult = pdResult.date_range(startDate, endDate)
    labels = pdResult['shortDate'].unique()

#Tkinter GUI

def init_gui(root, update_function: Callable) -> FigureCanvasTkAgg:
    
    
    
    def selectChart(*args):
        #global pdResult
        #global pdResultConst
        #global labels
        #pdResult = pdResultConst.copy()
        #labels = pdResult['shortDate'].unique()
        
        #figGen()
        if chartType.get() == 'Violin':
            figure = draw_violinPlot()
        
        if chartType.get() == 'Line':
            figure = draw_lineChart()
        
        if chartType.get() == 'FourHist':
            figure = draw_fourHist()
        
        if chartType.get() == 'HeatMap':
            figure = draw_heatMap()

        
        canvas.figure = figure
        canvas.draw()
        sns.set()
        

    def figGen() -> Figure:
        
        figure = Figure(figsize=(8, 4.5), dpi=128)
        figure.subplots_adjust(top=.95, bottom=.25)
        sns.color_palette('tab10')
        
        return figure
    

    
    init_figure = figGen()
    
    root.winfo_toplevel().title("Weather Visualization")


    
    leftFrame = tkinter.Frame(root)
    leftFrame.grid(column=0, row=1)
    leftFrame.grid_rowconfigure((0), weight=1)

    chartType = tkinter.StringVar(leftFrame)
    chartType.set('Violin')
    chartType.trace('w', selectChart)

    graphChartType = tkinter.OptionMenu(leftFrame, chartType, 'Violin', 'Line', 'FourHist', 'HeatMap')
    graphChartType.grid(column=0, row=0)
    graphChartType.config(width=10)    

    oneDayBtn = tkinter.Button(leftFrame, text="One Day", command=lambda: timeButton(1))
    oneDayBtn.grid(column=0, row=1)
    oneDayBtn.config(width=10)
    
    threeDayBtn = tkinter.Button(leftFrame, text="Three Days", command=lambda: timeButton(3))
    threeDayBtn.grid(column=0, row=2)
    threeDayBtn.config(width=10)
    
    oneWeekBtn = tkinter.Button(leftFrame, text="One Week", command=lambda: timeButton(7))
    oneWeekBtn.grid(column=0, row=3)
    oneWeekBtn.config(width=10)
    
    twoWeekBtn = tkinter.Button(leftFrame, text="Two Weeks", command=lambda: timeButton(14))
    twoWeekBtn.grid(column=0, row=4)
    twoWeekBtn.config(width=10)
    
        
    rightFrame = tkinter.Frame(root)
    rightFrame.grid(column=1, row=1)
    rightFrame.grid_rowconfigure((0), weight=1)

    canvas = FigureCanvasTkAgg(init_figure, rightFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1,row=1)    
    
    
    
     
    

    
    
    
    
    return canvas
  

#Seaborn functions

def intSNS() -> Figure:
    figure = Figure(figsize=(8, 4.5), dpi=128)
    figure.subplots_adjust(top=.95, bottom=.25)
    sns.color_palette('tab10')
    sns.set(font_scale=.5)
    return figure

def draw_violinPlot() -> Figure:
    figure = intSNS()
    ax = figure.subplots()
    sns.violinplot(data = pdResult, ax=ax, x='shortDate', y='temperature')
    ax.set(xlabel='Date', ylabel='Temperature')
    ax.set_xticklabels(labels, rotation=45, horizontalalignment='right')
    return figure

def draw_lineChart() -> Figure:
    figure = intSNS()
    ax = figure.subplots()
    
    sns.lineplot(data=pdResult.dropna(subset=['temperature']), ax=ax, x='timestamp', y='temperature', label='Temperature' )
    sns.lineplot(data=pdResult.dropna(subset=['relativeHumidity']), ax=ax, x='timestamp', y='relativeHumidity', label='Humidity')
    ax.set(xlabel='Date', ylabel='Value')
    ax.legend()
    return figure

def draw_fourHist() -> Figure:
    figure = intSNS()
    ax = figure.subplots(nrows=2,ncols=2)
    
    sns.histplot(data=pdResult, x='shortDate', y='temperature', label='Temperature', ax=ax[0,0])
    sns.histplot(data=pdResult, x='shortDate', y='relativeHumidity', label='Humidity', ax=ax[0,1])
    sns.histplot(data=pdResult, x='shortDate', y='windSpeed', label='Wind Speed', ax=ax[1,0])
    sns.histplot(data=pdResult, x='shortDate', y='barometricPressure', label='hPa', ax=ax[1,1])
    ax[0,0].set(xlabel='Date', ylabel='Temp')
    ax[0,1].set(xlabel='Date', ylabel='Humidity')
    ax[1,0].set(xlabel='Date', ylabel='Wind Speed')
    ax[1,1].set(xlabel='Date', ylabel='hPa')
    
    ax[0,0].set_xticklabels(labels, rotation=90, horizontalalignment='right')
    ax[0,1].set_xticklabels(labels, rotation=90, horizontalalignment='right')
    ax[1,0].set_xticklabels(labels, rotation=90, horizontalalignment='right')
    ax[1,1].set_xticklabels(labels, rotation=90, horizontalalignment='right')
    
    return figure

def draw_heatMap() -> Figure:
    figure = intSNS()
    ax = figure.subplots()
    heatmapData = pdResult.copy()
    heatmapData['shortDate'] = pd.to_datetime(heatmapData['timestamp']).apply(lambda x:x.date().strftime('%Y-%m-%d')) 
    heatmapData.drop(axis=1, inplace=True, columns=['windSpeed', 'windDirection', 'barometricPressure', 'visibility', 'textDescription', 'timestamp'])
       
    pd.set_option('display.max_columns', 1000)
    print(heatmapData)
    print(heatmapData.dtypes)
    
    heatmapPivot = pd.pivot_table(heatmapData, values='relativeHumidity', index='shortDate', columns='temperature')
    print(heatmapPivot)
    sns.heatmap(heatmapPivot, annot=True, fmt="g", cmap='viridis', ax=ax)
    return figure

#Start app
root = tkinter.Tk()

canvas = init_gui(root, update_function=intSNS())

tkinter.mainloop()
    
    



