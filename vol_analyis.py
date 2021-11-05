from operator import concat
import os
from sys import hash_info
import pandas as pd
from pandas.io.parsers import read_csv 
import matplotlib.pyplot as plt
import numpy as np 
import datetime as dt


#-----------------------------------------------------------------------------------------GENERAL INFO----------------------------------------------------------------

#this is my first prototype  in creatig a timeseries for technical analysis of indian stocks.
#for simplicity and performance I would suggest to use this https://github.com/pillai-amal/NSE-timeseries-form-CSV-file-creator-and-SQL-appender-
#uploaded as this shows a alternative way the timeseries are ceated from stored list of dictonaries. I have not seen this method implimented elsewhere
#although this is faster than make_timeseries function used in https://github.com/pillai-amal/NSE-timeseries-form-CSV-file-creator-and-SQL-appender- this is memory intensive

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#declaration of dictionay name and lists 
extension = '.csv'
dict_name = "day%sdict"
dict_dates = "dates%sdict"
dict_lis = []
dict_lis_date = []
day = 0
#assigning file name
file_temp_gain = "%s_byGainers.xlsx"
file_to_save = file_temp_gain % (dt.date.today())
dir_name = str(dt.date.today())
print(dir_name)

#chaning the directory to to where the CSV files are stored
os.chdir('C:/Users/pillai_amal/bhavcopy')

#as I already mentioed in https://github.com/pillai-amal/NSE-timeseries-form-CSV-file-creator-and-SQL-appender- , the fie names are stored in numbers, so slecting the latest file 
count = len(os.listdir())
file = count - 1

#I'm here creating the topgainers for the day
file_name = concat(str(file),".csv")
final_frame = pd.read_csv(file_name)
final_frame['GAIN'] = final_frame['LAST'] - final_frame['PREVCLOSE']
final_frame['PERCENTGAIN'] = final_frame['GAIN']/final_frame['PREVCLOSE']

exp_frame = final_frame.loc[final_frame['SERIES'] == 'EQ'] # we need only equity info 

exp_frame_treated = exp_frame.sort_values(by = ['PERCENTGAIN', 'TOTTRDQTY'],  ascending= False) #soring in descending order

#here we a looping through the entire bahvcopy CSV file stored in directly, make sure no other csvs are stored here to avoid any 'Key Error' errors
for item in os.listdir():
    if item.endswith(extension):
        data_file = read_csv(item)
        data_file_dropped = data_file.loc[data_file['SERIES'] == 'EQ', ['SYMBOL', 'TOTTRDQTY', 'TIMESTAMP']] #here we are doing volume analysis so we are taking only ticker volume and the data 
        dict_store = dict_name % (day)
        dates_store = dict_dates % (day)
        dict_store = {}
        dates_store = {}
        #for each Ticker in csv here we are taking the dates as numbers, eg: Suppose we are analysing volume form Jan 1st 2021 to November 30th 2021. Then Jan 1st 2021 will be 1
        for indx in data_file_dropped.index:
            dict_store[(data_file_dropped['SYMBOL'][indx])] = data_file_dropped['TOTTRDQTY'][indx]
            dates_store[(data_file_dropped['SYMBOL'][indx])] = data_file_dropped['TIMESTAMP'][indx] #just considered dates to you can drop dates if you want as here we have only considered as numbers as said above
    day = day+1
    dict_lis.append(dict_store)
    dict_lis_date.append(dates_store) #this can be dropped, there is no implementation for later but you can use this to replace the numbers with dates if you want to

#here we are crated a directory tor store the data and images 
parentdir = 'C:/Users/pillai_amal/gainerimages'
path = os.path.join(parentdir,dir_name)
mode = 0o777
os.mkdir(path, mode)

#where we are chaning the directory to newly created directory 
os.chdir(('C:/Users/pillai_amal/gainerimages/%s') % dir_name)

n= 0
image_extension = ".png"
#daving the topgainer to a excel file in the created directory
exp_frame_treated.to_excel(file_to_save)

while n<75: #analysis of 75 trading days
    for indx in exp_frame_treated.index:
        n = n + 1
        ticker = exp_frame_treated['SYMBOL'][indx]
        list_vol = []
        list_dates_plt = []
        for vol in range (0, len(dict_lis)):
            try: 
                list_vol.append(dict_lis[vol][ticker]) #as we are stored the volume in a dictionay inside a list 
            except KeyError:
                print("Key Not Found!")
                print(ticker)
        x = np.linspace(1, len(list_vol), num= len(list_vol)) #entire ploting and saving goes here
        print("The array x is %s" % (x))
        y = list_vol
        plt.scatter(x,y)
        plt.suptitle(ticker)
        plt.ylabel("Volume")
        plt.xlabel("Dates")
        image_name = concat(concat(str(n), str(ticker)),image_extension)
        plt.savefig(image_name, dpi=100)
        plt.clf()
        y.clear()
        list_vol.clear()
    n += 1
    print("----------------------------------------------")
    print(n)

    #for a any doubts or assistance contact me at amalmpillai7@gmail.com