import pymongo
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import time


#Configuration page streamlit
st.set_page_config(page_title="Histogramme", page_icon="📈")


#Affichage texte de la page
st.markdown("# Histogramme compound")
st.sidebar.header("Histogramme")
st.write(
    """Quantification du nombres de tweet en relation avec la force du sentiment"""
)

#Creation sidebar
status_text = st.sidebar.empty()

#Creation placeholder pour le graph
placeholder = st.empty()

#Connection DB
cluster = pymongo.MongoClient("mongodb://root:password@mongo:27017/")
db = cluster["Database_tweet"]
collection = db["tweets"]

#Affichage graph et actualisation toutes les secondes pour le suivis du stream
#for _ in iter(int, 1):
while True:
    with placeholder.container():
        progress_bar = st.sidebar.progress(0)
        x = collection.find()
        list_cur = list(x)

        df = pd.DataFrame(list_cur)

        #Close le diagramme précédent pour éviter de noyer la mémoire
        plt.close()

        fig, ax = plt.subplots()
        sns.histplot(data=df, x='compound')
        st.pyplot(fig)
        progress_bar.empty()
        time.sleep(5)


