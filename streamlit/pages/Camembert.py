import pymongo
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time


#Configuration page streamlit
st.set_page_config(page_title="Camembert", page_icon="📈")

#Affichage texte de la page
st.markdown("# Camembert sentiments")
st.sidebar.header("Camembert")
st.write(
    """Distribution des sentiments sur le sujet choisis"""
)

#Creation sidebar
status_text = st.sidebar.empty()

#Creation placeholder pour le graph
placeholder = st.empty()

#Connection DB
cluster = pymongo.MongoClient("mongodb://root:password@mongo:27017/")
db = cluster["Database_tweet"]
collection = db["tweets"]

for _ in iter(int, 1):
    with placeholder.container():
        progress_bar = st.sidebar.progress(0)
        
        #Close le diagramme précédent pour éviter de noyer la mémoire
        plt.close()
        
        x = collection.find()
        list_cur = list(x)
        df = pd.DataFrame(list_cur)

        res = df.groupby(['sentiment'])['sentiment'].count()

        labels = 'Positive', 'Negative', 'Neutre'
        sizes = [res.iloc[2], res.iloc[0], res.iloc[1]]
        explode = (0.1, 0, 0)

        for i in range(1, 101):
            new_rows = i + 5
            progress_bar.progress(i)
            status_text.text("%i%% Complete, awaiting new data" % i)
            last_rows = new_rows

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  

        st.pyplot(fig1)
        progress_bar.empty()
        time.sleep(5)
