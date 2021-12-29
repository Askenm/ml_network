
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network


def map_relation_name(relations):
    return [i.replace(' ','_') for i in relations]


def map_edge_color(relation):
    mapping = {'romantic_partner':'red',
               'friends':'green',
               'colleague':'blue'}
    return mapping[relation]



# Read dataset (CSV)
df_interact = pd.read_csv('data/relations.csv')

# Set header title
st.title('Multilayer Network Visualizations of Relations in My Support Network')

# Define list of selection options and sort alphabetically
relations = ['romantic partner','friends','colleague']

# Implement multiselect dropdown menu for option selection (returns a list)
selected_drugs = st.multiselect('Select relations(s) to visualize', relations)

# Set info message on initial site load
if len(selected_drugs) == 0:
    st.text('Choose at least 1 relation to start')




# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['relation_type'].isin(map_relation_name(selected_drugs))]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'ent_1', 'ent_2', 'relation_type')

    # Initiate PyVis network object
    drug_net = Network(
                       height='1000px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white'
                      )

    # Take Networkx graph and translate it to a PyVis graph format


    G_empty = nx.create_empty_copy(G)

    drug_net.from_nx(G_empty)
    for edge in G.edges(data=True):
        data = edge[-1]
        drug_net.add_edge(edge[0],edge[1],color = map_edge_color(data['relation_type']),width=5)

    # Generate network with specific layout settings
    drug_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
        #selected_persons = st.multiselect('Select relations(s) to visualize', G.nodes())

    # Save and read graph as HTML file (locally)
    except:
        path = '.'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)




# Implement multiselect dropdown menu for option selection (returns a list)


try:
    

    all_text = {'Asta':'Det her handler om Asta - hun kan godt lide pizza',
                'Aske':'Aske sidder i lufthavnen og koder'}

    print('DOING IT')
    print(selected_persons)
    textual_data = all_text[selected_persons[0]]
    print('DOING IT 2')
    st.write(textual_data )
    print('DOING IT 3')
except:
    pass

# Footer
#st.markdown(
#    """
#    <br>
#    <h6><a href="https://github.com/kennethleungty/Pyvis-Network-Graph-Streamlit" target="_blank">GitHub Repo</a></h6>
#    <h6><a href="https://kennethleungty.medium.com" target="_blank">Medium article</a></h6>
#    <h6>Disclaimer: This app is NOT intended to provide any form of medical advice or recommendations. Please consult your doctor or pharmacist for professional advice relating to any drug therapy.</h6>
#    """, unsafe_allow_html=True
#    )

