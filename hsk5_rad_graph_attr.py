# -*- coding: utf-8 -*-
import csv
import json

word_set = set()
comp_set = set()
edge_set = set()
edge_c_set = set()
dict_map = {}


#dictionary from https://raw.githubusercontent.com/skishore/makemeahanzi/master/dictionary.txt

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
    d_entry = dict_map[wa_entry]
    if d_entry.get('etymology') != None:
        if d_entry.get('etymology').get('phonetic') != None:
            comp_set.add(d_entry.get('etymology').get('phonetic'))
            edge_set.add(d_entry.get('character')+"|"+d_entry.get('etymology').get('phonetic')+"|"+'phonetic')
            edge_c_set.add(d_entry.get('etymology').get('phonetic'))

        if d_entry.get('etymology').get('semantic') != None:
            comp_set.add(d_entry.get('etymology').get('semantic'))
            edge_set.add(d_entry.get('character')+"|"+d_entry.get('etymology').get('semantic')+"|"+'semantic')
            edge_c_set.add(d_entry.get('etymology').get('semantic'))

word_set = word_set.union(comp_set)  
word_set = word_set.union(edge_c_set) 

word_set = list(word_set)
edge_set = list(edge_set)
s_nodes = ""
s_edges = ""
for value in word_set:
    s_nodes += "<node id=\""+str(word_set.index(value)+1)+"\" label=\""+value+"\"/>\n"

j = 0
for edge_str in edge_set:
    edge = edge_str.split("|")
    s_edges += "<edge id=\""+str(edge_set.index(edge_str)+1)+"\" source=\""+str(word_set.index(edge[1])+1)+"\" target=\""+str(word_set.index(edge[0])+1)+"\" label=\""+edge[2]+"\"/>\n"
    j = j + 1
    
gexf_file = open("output_etym.gexf","w",encoding='utf8') 
gexf_content = """<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.3" version="1.3" xmlns:viz="http://www.gexf.net/1.3/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd">
  <meta lastmodifieddate="2018-04-27">
    <creator>Gephi 0.9</creator>
    <description></description>
  </meta>
  <graph defaultedgetype="directed" mode="static">
    <nodes>
        """+s_nodes+"""
        </nodes>
        <edges>
        """+s_edges+"""
        </edges>
    </graph>
</gexf>"""
gexf_file.write(gexf_content)
gexf_file.close()
