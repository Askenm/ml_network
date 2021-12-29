import streamlit as st
import streamlit.components.v1 as components


    



st.title("Sommerhus relationer")
#expander = st.beta_expander("Explanations")
#expander.write("The graphs below are meant as visual aids for selecting a fitting threshold for the social dynamics model")


st.sidebar.header('Which relations would you like to view?')
#option = st.sidebar.selectbox(
#'Relation',
#relations)
relations = ['romantic partner','friend','colleague']
romantic = st.sidebar.checkbox(relations[0])
friend = st.sidebar.checkbox(relations[1])
colleague = st.sidebar.checkbox(relations[2])

mapping = {'romantic_partner':romantic,'friends':friend,'colleague':colleague}

chosen_types = []
for n,val in mapping.items():
    if val:
        chosen_types.append(n)


import pydot as pt
import matplotlib.pyplot as plt
from matplotlib import pylab as pl
from pyvis.network import Network
import numpy as np
import networkx as nx


nodes = ["Jacob",'Aske','Klara','Marcus','Asta','Valdemar','Emma','Mette','Julius','Emilie','Filip','Ida','Mads']

multi_layer_structure = {}
rom_edges = [('Jacob','Emma'),('Aske','Emilie'),('Filip','Klara'),('Mads','Mette')]
rom_g = nx.Graph()
rom_g.add_edges_from(rom_edges)

friend_edges = [('Asta','Marcus'),('Asta','Valdemar'),
                ('Marcus','Aske'),('Marcus','Valdemar'),
                ('Emma','Klara'),('Emma','Mette')]
friend_g = nx.Graph()
friend_g.add_edges_from(friend_edges)


colleague_edges = [('Aske','Jacob'),('Klara','Marcus'),('Mette','Julius'),('Ida','Mette'),('Ida','Julius')]
coll_g = nx.Graph()
coll_g.add_edges_from(colleague_edges)

multi_layer_structure['romantic_partner']=rom_g
multi_layer_structure['friends']=friend_g
multi_layer_structure['colleague']=coll_g
edgelists = {k:list(v.edges()) for k,v in multi_layer_structure.items()}
names = list(multi_layer_structure.keys())


def plot_it_net(nodes,edgelists,chosen_types=['romantic_partner','colleague','friends']):
    network = Network(height='400px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white')
    network.barnes_hut()
    #test.enable_physics(False)


    cols = {}
    cols['romantic_partner']= 'red'
    cols['colleague']= 'green'
    cols['friends']= 'blue'


    for node in nodes:

        network.add_node(node)



    for e_type,edges in edgelists.items():
        if e_type not in chosen_types:
            continue
        print(e_type)
        print(cols[e_type])
        for src,trg in edges:
            print(src,trg)
            network.add_edge(src, trg,width = 1,color = cols[e_type])
        print('\n\n')

    plt.style.use('fivethirtyeight')
    print('Saving ','sommerhus_relations')
    #network.show_buttons(filter_='physics')
    network.save_graph("sommerhus_relations.html")
    return network
    
    
network = plot_it_net(nodes,edgelists,chosen_types)



print(chosen_types)
#with open("sommerhus_relations.html", "r", encoding='utf-8') as f:
#    text= f.read()""

HtmlFile = open(f'sommerhus_relations.html','r',encoding='utf-8')
components.html(HtmlFile.read())
#from IPython.core.display import display, HTML
#components.html(text)
#components.iframe(network.write_html('sommerhus.html',notebook=True))
#components.iframe(display(HTML(text)))
