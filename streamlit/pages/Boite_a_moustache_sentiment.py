import pymongo
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import time


#Configuration page streamlit
st.set_page_config(page_title="Boite à moustache", page_icon="📈")

#Affichage texte de la page
st.markdown("# Boite a moustache des sentiments")
st.sidebar.header("Boite a moustache sentiments")
st.write(
    """Representation de l'évolution des quartile et médianne du 'coumpound' en fonction des sentiments"""
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

        #Ferme le diagramme précédent pour éviter de noyer la mémoire
        plt.close()

        x = collection.find()
        list_cur = list(x)
        df = pd.DataFrame(list_cur)

        for i in range(1, 101):
            new_rows = i + 5
            status_text.text("%i%% Complete, awaiting new data" % i)
            progress_bar.progress(i)
            last_rows = new_rows


        fig, ax = plt.subplots()
        sns.boxplot(data=df, y='compound', x='sentiment')
        st.pyplot(fig)
        progress_bar.empty()
        time.sleep(5)

