import pymongo
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse de sentiment", page_icon="")


st.markdown("# Projet - Analyses de sentiments")
st.sidebar.header("Menu")
st.sidebar.success("Selectionner une visualisation dans le menu ci-dessus")
st.write(
    """Ce dashboard permet de regarder en temps réel l'évolution de sentiments sur un sujet choisis. Dans ce cas nous avons
    choisis d'étudier l'évolution de sentiments sur le hastag '#BLACKPINK' qui était trending #1 mondiale d'après https://getdaytrends.com/ au moment de la mise
    en fonction de notre architecture.""")

st.markdown("#### [Camembert](http://localhost:8501/Camembert)")
st.write("""Notre but est de visualiser quantitativement les réactions, avec l'utilisation d'une visusalisation en camembert
    afin d'avoir un visu rapide sur la proportion des réactions.
    """)

st.markdown("#### [Histogramme](http://localhost:8501/Histogramme)")
st.write("""Notre but est de visualiser quantitativement les différentes "force" de réactions suivant le critère "compound" de VADER qui permet
         de classifier les sentiments.
        """)

st.markdown("#### [Boite a moustache des sentiments](http://localhost:8501/Boite_a_moustache_sentiment)")
st.write("""Notre but est d'observer la distribution du compound en ayant une représentation des quartiles et de la médianne suivant les sentiments avec
        l'évolution au court du temps grâce à des marqueurs.
        """)

st.markdown("#### [Boite a moustache du compound](http://localhost:8501/Boite_a_moustache_compound)")
st.write("""Notre but est d'observer la distribution des données plus globales, en ayant une représentation des quartiles avec
        l'évolution au court du temps grâce à des marqueurs.
        """)