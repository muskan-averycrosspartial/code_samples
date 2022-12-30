#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 03:07:03 2022

@author: muskanaggarwal
"""

import PyPDF2
import re
import spacy
import pandas as pd
import matplotlib.pyplot as plt


base_path = "/Users/muskanaggarwal/Documents/GitHub/final-project-hindutva_politics/"


# creating a pdf file object
pdfFileObj = open(base_path + 'data/PC-Factsheet-Nutrition-Health-and-Developmet-Indicators_HCPDS-working-paper_Volume-18_no_4.pdf', 'rb')
  
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  
# printing number of pages in pdf file
print(pdfReader.numPages)
  
# creating a page object
text = ""

for i in range(33,45):
    pageObj = pdfReader.getPage(i)
    text = text + pageObj.extractText() 
    
pdfFileObj.close()

# extracting text from page

def remove_state(l):
    pattern = "(^andhra pradesh |^arunanchal pradesh |^assam |^bihar |^chhattisgarh |^goa |^gujarat |^haryana|^himachal pradesh |^jammu & kashmir |^karnataka |^madhya pradesh |^maharashtra |^meghalaya |^nct of dehli |^punjab |^rajasthan |^tamil nadu |^telangana |^tripura |^uttar pradesh |^west bengal| ^manipur |)"
    l = re.sub(pattern, "", l)
    return l

def extract_table(text):
    text_lower = text.lower()
    lines = text_lower.split('\n')
    #title = lines[2]
    del lines[0:16]
    lines =  [line.lower().strip().replace("  "," ") for line in lines]
    lines = [line for line in lines if len(line) > 30 ] 
    lines = [remove_state(line) for line in lines] 
    return lines
    

def get_pc(l):
    pattern = "(^\D+)"
    match = re.search(pattern, l)
    assert(match), f'No match for pc: {l}'
    return match.group(1)


 #outputs a cumulative numbers string (first in case of errors)
def get_numbers(l):
    #pattern = "((?<=Gain)|(?<=Realign)|(?<=Close))\s.*%"
    pattern = "(^\D+)\s(\d+.*)"
    match = re.search(pattern, l)
    assert(match), f'No match for numbers: {l}'
    return match.group(2)    

#inputs a cumulative numbers string and differentiates it into the respective values

def get_separate_numbers(num):
    pattern = "(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)"
    match = re.search(pattern, num)
    assert(match), f'No match for: {num}'
    mil_out =  match.group(1)
    civ_out =  match.group(2)
    mil_in = match.group(3)
    civ_in = match.group(4)
    mil_net =  match.group(5)
    civ_net =  match.group(6)
    net_contra = match.group(7)
    direct = match.group(8)
    indirect = match.group(9)
    total = match.group(10)
    ea_emp = match.group(11)

    
    return [mil_out, civ_out, mil_in, civ_in, mil_net, civ_net, net_contra, direct, indirect, total, ea_emp]


def parse_line(l):
    pc = get_pc(l)
    numbers = get_numbers(l)
    numbers = numbers.replace(',','').replace('(','-').replace(')','')
    separate_numbers = ','.join(get_separate_numbers(numbers))
    return ','.join([pc, separate_numbers])


lines_final = extract_table(text)
text_test = [parse_line(line) for line in lines_final]

text_test.insert(0,('PC,' 'fem_school,' 'pop_bw15%,'  'sexratio%,' 'sexratio _five%,' 'birthreg%,'  'hh_elec,'  'hh_water,'
                    'hh_impsanit,' 'hh_cleancook,' 'hh_iodsalt,' 'hh_healthins,'))


#adding \n so that values go in different rows

doc = '\n'.join(text_test)

with open(base_path + 'processed_data/processed.csv', 'w', newline='\n') as ofile:
    ofile.write(doc)
    
#sentiment analysis

df_speeches = pd.read_csv(base_path + "data/PM_Modi_speeches.csv")

text = ''
polarity = 0
subjectivity = 0 
summary_total = {}
total_text = ""

      
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')


df_speeches_eng = df_speeches[df_speeches["lang"] == "en"]
df_speeches_eng = df_speeches_eng.reset_index()

for speech in range(490):
    doc = nlp(df_speeches_eng.loc[speech,"text"])
    total_text = total_text + df_speeches_eng.loc[speech,"text"]
    polarity = doc._.blob.polarity
    subjectivity = doc._.blob.subjectivity   
    print(subjectivity)
    summary_doc = summary = {df_speeches_eng.loc[speech,"date"]:{'polarity':polarity,'subjectivity':subjectivity }} 
    summary_total = summary_total | summary_doc

df_summary = pd.DataFrame.from_dict(summary_total, orient='index')
df_summary = df_summary.reset_index()
df_summary['date']= pd.to_datetime(df_summary['index'])

import seaborn as sns
sns.set_theme(style="white", palette="pastel")


# df_summary = df_summary.sort_values(by = "date")
# df_summary = df_summary.reset_index(drop=True)
# df_summary = df_summary.reset_index()


fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10,5))
fig.suptitle("Sentiment Over Time In Modi's speeches")
sns.lineplot(df_summary, ax=axes[0], x = 'date', y = 'subjectivity')
axes[0].set_title('Subjectivity')
axes[0].set(ylabel='')
sns.lineplot(df_summary, ax=axes[1], x = 'date', y = 'polarity',  color = 'r')
axes[1].set_title('Polarity')
axes[1].set(ylabel='')
plt.xticks(rotation = 25)
plt.savefig(base_path + 'graphs/static_plot1')


#most common word used by Modi in english speeches


#https://blog.ekbana.com/nlp-for-beninners-using-spacy-6161cf48a229
from collections import Counter
total_text_short = total_text[0:999999]

special_pattern = r'[^a-zA-z.,!?/:;\"\'\s]' 
number_pattern =  r'[^a-zA-z.,!?/:;\"\'\s]' 
total_text_short = re.sub(r'\xa0', '',total_text_short )
total_text_short = re.sub(r'\n', '',total_text_short )
total_text_short = re.sub(special_pattern, '',total_text_short )
total_text_short = re.sub(special_pattern, '',total_text_short )
total_text_short = total_text_short.lower()


 

doc_words = nlp(total_text_short)
#remove stopwords and punctuations
words = [token.text for token in doc_words if token.is_stop != True and token.is_punct != True]
word_freq = Counter(words)
common_words = word_freq.most_common(16)
print (common_words)

clean_speech_words = pd.DataFrame(common_words,
                             columns=['words', 'count'])

clean_speech_words = clean_speech_words.iloc[1: , :]

fig, ax = plt.subplots(figsize=(8, 8))

# Plot horizontal bar graph
sns.barplot(data=clean_speech_words, x="words", y="count")

ax.set_title("Common Words Found in Modi's Speeches (Without Stop Words)")
plt.xticks(rotation = 45)
plt.savefig(base_path + 'graphs/static_plot2')


    
    



