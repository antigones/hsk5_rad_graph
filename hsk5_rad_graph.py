# -*- coding: utf-8 -*-
import csv
import json

word_set = set()
dict_map = {}
hanzi_map = {}

file = open("output.csv","w",encoding='utf8') 

with open("HSK5_freqorder.txt", 'r',encoding='utf8') as csvfile:
    freader = csv.reader(csvfile, delimiter='\t')
    for row in freader:
        for c in row[0]:
            word_set.add(c)

with open("dictionary.txt", 'r',encoding='utf8') as dict_file:
    lines = dict_file.readlines()
    for row in lines:
        j_row = json.loads(row)
        dict_map[j_row["character"]] = j_row        

for wa_entry in word_set:
    hanzi_map[wa_entry] = dict_map[wa_entry]       


for key, value in hanzi_map.items():
    file.write(value["radical"]+","+key+'\n')
file.close()    