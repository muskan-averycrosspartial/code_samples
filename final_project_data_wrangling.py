#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:12:57 2022

@author: muskanaggarwal
"""


import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os
import pandas_datareader.data as web
from pandas_datareader import wb
from shiny import App, render, ui, reactive
# importing libraries
import pandas as pd # Reading csv file 
from shapely.geometry import Point #

from shiny import *
from shiny.types import ImgData

import spacy            
import re


#setting the base path
base_path = "/Users/muskanaggarwal/Documents/GitHub/final-project-hindutva_politics/"

#ask users if they want to see choropleths for a particular state or the entire country


#df_pc = gpd.read_file("/Users/muskanaggarwal/Documents/GitHub/final-project-hindutva_politics/shp_files/mapping-indias-elections/bihar/bihar.parliamentary.shp")
df_affadavit = pd.read_csv(base_path + "data/csv_shrug-v1.5.samosa-affidavits-csv/shrug-v1.5.samosa-affidavits-csv/affidavits_clean.csv", encoding= 'unicode_escape')
df_election = pd.read_csv(base_path + "data/TCPD_GE_all_2022-12-5.csv")
df_speeches = pd.read_csv(base_path + "data/PM_Modi_speeches.csv")



#These datasets are not used for this project, but I might use them later
    #df_questions_2014_19 = pd.read_csv("/Users/muskanaggarwal/Downloads/TCPD_QH.csv", on_bad_lines='skip')
    #df_questions_pre_2014 = pd.read_csv("/Users/muskanaggarwal/Downloads/TCPD_QH (1).csv" , on_bad_lines='skip')
    #df_dhs_shp = gpd.read_file("/Users/muskanaggarwal/Downloads/IAGE71FL/IAGE71FL.shp")

#from the text analysis and processing file
df_pc_cov = pd.read_csv(base_path + "processed_data/processed.csv")


states = (df_affadavit["pc01_state_name"]).unique().tolist()
pc = (df_election["Constituency_Name"]).unique().tolist()

states = [x.lower() for x  in states]
pc = [x.lower() for x  in pc]
df_election["State_Name"] =  [x.lower().replace("_", " ") for x  in df_election["State_Name"] ]
df_election = df_election[~df_election["State_Name"].isin(["andaman & nicobar islands", "lakshwadeep"])]
df_election["Constituency_Name"] =  [x.lower().replace("_", " ") for x  in df_election["Constituency_Name"]]
df_affadavit["pc01_state_name"] =  [x.lower().replace("_", " ") for x  in df_affadavit["pc01_state_name"]]
df_pc_cov["PC"] = [x.lower().strip() for x  in df_pc_cov["PC"]]



#df_merged_2019 =df_merged[df_merged["Year"] == 2019]
#df_merged_2019 =df_merged_2019[df_merged["Position"] == 1]

# from matplotlib import cm
# import numpy as np
# from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# df_merged.columns


#interactive plot


def shape_state(state):
        df_pc = gpd.read_file(base_path + "shp_files/mapping-indias-elections/" + state + "/" + state.replace(" ","") + ".parliamentary.shp")
        df_pc["pc_name_lower"] = [x.lower() for x  in df_pc["pc_name"] ]
        return df_pc
    

def make_choro_aff(state):
    
    df_pc = shape_state(state) 
    
    
    df_test_merge =   df_pc.merge(df_affadavit, left_on='pc_name_lower',right_on='adr_con_name', how='inner')
    df_test_merge_winner = df_test_merge[df_test_merge["winner"] == 1]
    df_test_merge_winner_year = df_test_merge_winner[df_test_merge["year"] == 2012]


    gdf_test = gpd.GeoDataFrame(df_test_merge_winner_year)
    
    df_bjp = df_test_merge_winner_year[df_test_merge_winner_year["party"] == "BJP"]
    gdf_final_bjp = gpd.GeoDataFrame(df_bjp)
    #make plot for year selected
    fig, ax = plt.subplots(figsize=(8,8))
    
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    
    ax = gdf_test.plot(ax=ax, column="age", legend=True, cax=cax, cmap="RdYlGn")
    
    
    kwarg3s = {'facecolor': 'None', 'linewidth': 1.5} #can remove hatch potentially
    gdf_final_bjp.plot(column="party", zorder=11, ax=ax, **kwarg3s, cmap="Oranges_r")
    ax.axis('off')
    
    
    
    
make_choro_aff("uttar pradesh")




#fitting a model - Probit
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Probit


df_election["Candidate"] =  [x.lower() for x  in df_election["Candidate"] ]


df_merged_model = df_election.merge(df_affadavit, left_on=['Candidate', 'Year'],right_on=['adr_cand_name','year'], how='inner')
df_merged_model = df_merged_model[df_merged_model['Position'] == 1]

df_model = df_affadavit
df_model = df_model[df_model["bye_election"] == 0]
df_model = df_model[['winner', 'party', 'year','pc01_state_id','adr_cand_name','age','ed', 'assets', 'liabilities', 'num_crim', 'adr_major_crime', 'punishment']]
df_model = df_model.fillna(0)

df_model["ed"] = pd.to_numeric(df_model["ed"])
df_model["num_crim"] = pd.to_numeric(df_model["num_crim"])
df_model["liabilities"] = pd.to_numeric(df_model["liabilities"])
df_model["adr_major_crime"] = pd.to_numeric(df_model["adr_major_crime"])
df_model["punishment"] = pd.to_numeric(df_model["punishment"])
df_model["party"] = df_model["party"].astype("category")
df_model["pc01_state_id"] = df_model["pc01_state_id"].astype("category")

#create dummy variable for party

df_model = pd.get_dummies(df_model, columns = ['party'])

Y = df_model["winner"]
X = df_model[['assets','liabilities','punishment','age','party_BJP','party_INC']]
X = sm.add_constant(X)

probit_model=Probit(Y,X)
result=probit_model.fit()

#printing results 


print(result.summary())


# nlp doesnt take more than 10 lakh words. 