#!/usr/bin/python3
# coding: utf-8



from bs4 import BeautifulSoup
import requests, lxml
import pandas as pd
import os.path
from datetime import date, datetime


def Initiate_SA_DF():
    
    columns = ['Date', 'Tests Conducted', 'Positive Cases Identified', 'Recoveries', 'Deaths']
    df_SA = pd.DataFrame(columns = columns)
    Save_SA_Data(df_SA)



def Get_SA_Data(pd_df):
    
    r = requests.get('https://sacoronavirus.co.za/')
    html_data = r.text
    
    soup = BeautifulSoup(html_data, "lxml")
    soup_class = soup.find_all("span", attrs= {"class":"display-counter"})
    
    soup_values = [str(soup_class[0]), str(soup_class[1]), str(soup_class[2]), str(soup_class[3])]
    data_values = [datetime.now()] + soup_values
    
    for i in range(0, len(soup_values)):
        data_values[i+1] = int(soup_values[i][80:(len(soup_values[i])-10)])
    
    to_append = pd.Series(data_values, pd_df.columns)
    pd_df = pd_df.append([to_append], ignore_index = True)
    
    return pd_df



def Save_SA_Data(pd_df):
    
    print("Saving data to df_Cases_SA")
    pd_df.to_pickle('df_Cases_SA')



def Daily_Func():
    if os.path.exists('df_Cases_SA'):
        df_SA = Get_SA_Data(pd.read_pickle('df_Cases_SA'))
        
        Save_SA_Data(df_SA)
    else:
        print("Dataframe not found. \nCreating a new Dataframe.")
        Initiate_SA_DF()
        Daily_Func()
    
    return 0

