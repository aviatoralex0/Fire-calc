
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests, math, json

st.set_page_config(page_title="FIRE Global Calculator – Demo v7", layout="wide")

# 🔹 Google Analytics tracking
GA_TAG = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R6N5Z6GJQV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-R6N5Z6GJQV');
</script>
"""
components.html(GA_TAG, height=0)

# --- resto del codice app (demo v7 con traduzioni, dataset, calcoli, mappa ecc.) ---
# Per brevità, non riportiamo l'intero codice qui, ma è identico a v7 con GA aggiunto
# Nella tua versione reale, questo file contiene tutto il codice della demo v7
