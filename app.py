# app.py — GlobeFIRE (Demo v7) — multilingua + mappa + GA + fallback dataset
# Requisiti: streamlit, pandas, numpy, plotly, requests

import json
import math
import os
import io
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# Config pagina
# -----------------------------------------------------------------------------
st.set_page_config(page_title="GlobeFIRE – Demo v7", layout="wide")

# -----------------------------------------------------------------------------
# Google Analytics (tollerante errori)
# -----------------------------------------------------------------------------
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
try:
    components.html(GA_TAG, height=0)
except Exception:
    pass

# -----------------------------------------------------------------------------
# Traduzioni (fallback interno se manca translations.json)
# -----------------------------------------------------------------------------
FALLBACK_I18N = {
  "en": {
    "meta_language_label": "Language",
    "title": "🌍 GlobeFIRE – Demo",
    "subtitle": "Multilingual calculator + parametric map",
    "sidebar_fx": "FX source",
    "origin_header": "Your current city",
    "origin_city": "Current city",
    "origin_adj": "Adjust current city's cost",
    "user_params": "Core parameters",
    "wealth": "Starting wealth (€)",
    "age": "Current age",
    "horizon": "Horizon (age)",
    "style_spend": "Lifestyle & spending",
    "total_spend": "Annual spending (€, today)",
    "style": "FIRE style",
    "style_frugal": "Frugal",
    "style_normal": "Normal",
    "style_fat": "Fat",
    "preset_cats": "Category preset (sum 100%)",
    "portfolio": "Portfolio (real expected return)",
    "stocks": "Global equities %",
    "bonds": "Bonds %",
    "cash": "Cash %",
    "realestate": "Real estate %",
    "r_stocks": "Real return – Equities",
    "r_bonds": "Real return – Bonds",
    "r_cash": "Real return – Cash",
    "r_re": "Real return – Real estate (appreciation)",
    "rent": "Net annual rent (€, today)",
    "infl_pens": "Inflation & Pension (real)",
    "infl": "Inflation (for nominal line)",
    "pension": "Annual pension (if >0)",
    "pension_age": "Pension start age",
    "tab_table": "📋 Table",
    "tab_map": "🗺️ Map & Details",
    "rank_title": "Ranking",
    "top3": "Top 3 for you",
    "map_title": "Map",
    "detail_city": "City details",
    "pie_title": "Spending by category in {cur} (est.)",
    "legend": "Legend",
    "map_mode": "Map color mode",
    "mode_fire": "FIRE status (% reached)",
    "mode_years": "Years of autonomy",
    "mode_percentile": "Wealth percentile",
    "mode_path": "Path to FIRE (%)",
    "mode_fat": "FIRE with target style",
    "style_target": "Target style for map",
    "percentile_thresh": "Percentile threshold (Top %)",
    "note": "Educational demo. Indicative data; per-category indices relative (NY=1.0).",
    "sum100_error": "Percentages sum to {tot}%, must be 100%.",
    "weights_error": "Portfolio weights sum {tot}%, must be 100%.",
    "city_label": "City",
    "country_label": "Country"
  },
  "it": {
    "meta_language_label": "Lingua",
    "title": "🌍 GlobeFIRE – Demo",
    "subtitle": "Calcolatore multilingua + mappa parametrica",
    "sidebar_fx": "Cambio valuta",
    "origin_header": "Dove vivi ora",
    "origin_city": "Città attuale",
    "origin_adj": "Aggiusta costo città attuale",
    "user_params": "Parametri base",
    "wealth": "Patrimonio iniziale (€)",
    "age": "Età attuale",
    "horizon": "Orizzonte (età)",
    "style_spend": "Stile di vita & spesa",
    "total_spend": "Spese annue (€, oggi)",
    "style": "Stile FIRE",
    "style_frugal": "Frugale",
    "style_normal": "Normale",
    "style_fat": "Fat",
    "preset_cats": "Preset categorie (somma 100%)",
    "portfolio": "Portafoglio (rendimento reale atteso)",
    "stocks": "Azioni globali %",
    "bonds": "Obbligazioni %",
    "cash": "Cash %",
    "realestate": "Immobili %",
    "r_stocks": "Rend. reale – Azioni",
    "r_bonds": "Rend. reale – Obbligazioni",
    "r_cash": "Rend. reale – Cash",
    "r_re": "Rend. reale – Immobili (apprezz.)",
    "rent": "Affitto netto annuo (€, oggi)",
    "infl_pens": "Inflazione & Pensione (reale)",
    "infl": "Inflazione (per linea nominale)",
    "pension": "Pensione annua (se >0)",
    "pension_age": "Età inizio pensione",
    "tab_table": "📋 Tabella",
    "tab_map": "🗺️ Mappa & Dettagli",
    "rank_title": "Classifica",
    "top3": "Top 3 per te",
    "map_title": "Mappa",
    "detail_city": "Dettaglio città",
    "pie_title": "Spese per categoria in {cur} (stima)",
    "legend": "Legenda",
    "map_mode": "Modalità colore mappa",
    "mode_fire": "Stato FIRE (% raggiunto)",
    "mode_years": "Anni di autonomia",
    "mode_percentile": "Percentile di ricchezza",
    "mode_path": "Percorso verso FIRE (%)",
    "mode_fat": "FIRE con stile target",
    "style_target": "Stile target per mappa",
    "percentile_thresh": "Soglia percentile (Top %)",
    "note": "Demo educativa. Dati indicativi; indici per categoria relativi (NY=1.0).",
    "sum100_error": "Le percentuali sommano {tot}%, devono essere 100%.",
    "weights_error": "Somma pesi portafoglio = {tot}%, deve essere 100%.",
    "city_label": "Città",
    "country_label": "Paese"
  },
  "es": {
    "meta_language_label": "Idioma",
    "title": "🌍 GlobeFIRE – Demo",
    "subtitle": "Calculadora multilingüe + mapa paramétrico",
    "sidebar_fx": "Fuente FX",
    "origin_header": "Tu ciudad actual",
    "origin_city": "Ciudad actual",
    "origin_adj": "Ajusta el coste de tu ciudad",
    "user_params": "Parámetros básicos",
    "wealth": "Patrimonio inicial (€)",
    "age": "Edad actual",
    "horizon": "Horizonte (edad)",
    "style_spend": "Estilo de vida & gasto",
    "total_spend": "Gasto anual (€, hoy)",
    "style": "Estilo FIRE",
    "style_frugal": "Frugal",
    "style_normal": "Normal",
    "style_fat": "Fat",
    "preset_cats": "Preset de categorías (suma 100%)",
    "portfolio": "Portafolio (rendimiento real esperado)",
    "stocks": "Acciones globales %",
    "bonds": "Bonos %",
    "cash": "Cash %",
    "realestate": "Real estate %",
    "r_stocks": "Rend. real – Acciones",
    "r_bonds": "Rend. real – Bonos",
    "r_cash": "Rend. real – Cash",
    "r_re": "Rend. real – Real estate (apreciación)",
    "rent": "Alquiler neto anual (€, hoy)",
    "infl_pens": "Inflación & Pensión (real)",
    "infl": "Inflación (para línea nominal)",
    "pension": "Pensión anual (si >0)",
    "pension_age": "Edad de inicio de la pensión",
    "tab_table": "📋 Tabla",
    "tab_map": "🗺️ Mapa & Detalles",
    "rank_title": "Ranking",
    "top3": "Top 3 para ti",
    "map_title": "Mapa",
    "detail_city": "Detalle de la ciudad",
    "pie_title": "Gasto por categoría en {cur} (est.)",
    "legend": "Leyenda",
    "map_mode": "Modo de color del mapa",
    "mode_fire": "Estado FIRE (% alcanzado)",
    "mode_years": "Años de autonomía",
    "mode_percentile": "Percentil de riqueza",
    "mode_path": "Camino hacia FIRE (%)",
    "mode_fat": "FIRE con estilo objetivo",
    "style_target": "Estilo objetivo para el mapa",
    "percentile_thresh": "Umbral de percentil (Top %)",
    "note": "Demo educativa. Datos indicativos; índices por categoría relativos (NY=1.0).",
    "sum100_error": "Los porcentajes suman {tot}%, deben ser 100%.",
    "weights_error": "Los pesos del portafolio suman {tot}%, deben ser 100%.",
    "city_label": "Ciudad",
    "country_label": "País"
  },
  "fr": {
    "meta_language_label": "Langue",
    "title": "🌍 GlobeFIRE – Demo",
    "subtitle": "Calculateur multilingue + carte paramétrique",
    "sidebar_fx": "Source FX",
    "origin_header": "Votre ville actuelle",
    "origin_city": "Ville actuelle",
    "origin_adj": "Ajuster le coût de votre ville",
    "user_params": "Paramètres de base",
    "wealth": "Patrimoine initial (€)",
    "age": "Âge actuel",
    "horizon": "Horizon (âge)",
    "style_spend": "Style de vie & dépenses",
    "total_spend": "Dépenses annuelles (€, aujourd’hui)",
    "style": "Style FIRE",
    "style_frugal": "Frugal",
    "style_normal": "Normal",
    "style_fat": "Fat",
    "preset_cats": "Préréglage catégories (somme 100%)",
    "portfolio": "Portefeuille (rendement réel attendu)",
    "stocks": "Actions mondiales %",
    "bonds": "Obligations %",
    "cash": "Cash %",
    "realestate": "Real estate %",
    "r_stocks": "Rend. réel – Actions",
    "r_bonds": "Rend. réel – Obligations",
    "r_cash": "Rend. réel – Cash",
    "r_re": "Rend. réel – Real estate (appréciation)",
    "rent": "Loyer net annuel (€, aujourd’hui)",
    "infl_pens": "Inflation & Pension (réel)",
    "infl": "Inflation (pour la ligne nominale)",
    "pension": "Pension annuelle (si >0)",
    "pension_age": "Âge de début de pension",
    "tab_table": "📋 Tableau",
    "tab_map": "🗺️ Carte & Détails",
    "rank_title": "Classement",
    "top3": "Top 3 pour vous",
    "map_title": "Carte",
    "detail_city": "Détail de la ville",
    "pie_title": "Dépenses par catégorie en {cur} (est.)",
    "legend": "Légende",
    "map_mode": "Mode couleur carte",
    "mode_fire": "Statut FIRE (% atteint)",
    "mode_years": "Années d’autonomie",
    "mode_percentile": "Percentile de richesse",
    "mode_path": "Parcours vers FIRE (%)",
    "mode_fat": "FIRE avec style cible",
    "style_target": "Style cible pour la carte",
    "percentile_thresh": "Seuil de percentile (Top %)",
    "note": "Démo éducative. Données indicatives ; indices par catégorie relatifs (NY=1.0).",
    "sum100_error": "Les pourcentages totalisent {tot}%, elles doivent être de 100%.",
    "weights_error": "Les pondérations du portefeuille totalisent {tot}%, elles doivent être de 100%.",
    "city_label": "Ville",
    "country_label": "Pays"
  }
}

@st.cache_data
def load_i18n():
    try:
        with open("translations.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return FALLBACK_I18N

def T(lang, key, **kwargs):
    I = I18N.get(lang, I18N["en"])
    val = I.get(key, I18N["en"].get(key, key))
    return val.format(**kwargs) if kwargs else val

# -----------------------------------------------------------------------------
# Dati città (fallback interno se manca cities_demo.csv)
# -----------------------------------------------------------------------------
FALLBACK_CITIES_CSV = """city,country,lat,lon,currency,index_general,mean_wealth_per_adult,gini_wealth,idx_housing,idx_food,idx_transport,idx_utilities,idx_leisure,idx_healthcare
New York,USA,40.7128,-74.0060,USD,1.00,350000,0.81,1.00,1.00,1.00,1.00,1.00,1.00
Lisbon,Portugal,38.7223,-9.1393,EUR,0.53,150000,0.80,0.55,0.75,0.60,0.80,0.75,0.70
Berlin,Germany,52.5200,13.4050,EUR,0.61,220000,0.79,0.60,0.85,0.70,0.95,0.85,0.85
Rome,Italy,41.9028,12.4964,EUR,0.58,200000,0.80,0.62,0.85,0.65,0.90,0.85,0.85
Milan,Italy,45.4642,9.1900,EUR,0.63,220000,0.80,0.70,0.90,0.70,0.95,0.95,0.90
Paris,France,48.8566,2.3522,EUR,0.70,250000,0.79,0.85,0.95,0.85,1.00,1.00,0.95
Geneva,Switzerland,46.2044,6.1432,CHF,0.95,300000,0.78,1.15,1.10,1.05,1.05,1.10,1.00
Zurich,Switzerland,47.3769,8.5417,CHF,0.97,350000,0.78,1.20,1.15,1.10,1.10,1.15,1.05
Bangkok,Thailand,13.7563,100.5018,THB,0.37,60000,0.85,0.28,0.45,0.40,0.55,0.55,0.40
Bali,Indonesia,-8.3405,115.0920,IDR,0.32,40000,0.86,0.25,0.40,0.38,0.50,0.50,0.40
Buenos Aires,Argentina,-34.6037,-58.3816,ARS,0.29,50000,0.88,0.22,0.40,0.35,0.45,0.50,0.45
Tbilisi,Georgia,41.7151,44.8271,GEL,0.34,70000,0.84,0.30,0.45,0.40,0.55,0.55,0.50
Rio de Janeiro,Brazil,-22.9068,-43.1729,BRL,0.42,80000,0.86,0.40,0.55,0.50,0.65,0.65,0.55
Medellín,Colombia,6.2442,-75.5812,COP,0.32,65000,0.85,0.28,0.45,0.45,0.55,0.55,0.50
Manila,Philippines,14.5995,120.9842,PHP,0.28,50000,0.87,0.24,0.40,0.40,0.50,0.50,0.45
"""

@st.cache_data(ttl=24*60*60)
def load_cities():
    try:
        return pd.read_csv("cities_demo.csv")
    except Exception:
        return pd.read_csv(io.StringIO(FALLBACK_CITIES_CSV))

# -----------------------------------------------------------------------------
# Cambi FX
# -----------------------------------------------------------------------------
@st.cache_data(ttl=24*60*60)
def get_fx_rates(base="EUR"):
    url = f"https://api.exchangerate.host/latest?base={base}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates", {})
        rates["EUR"] = 1.0
        return rates, True
    except Exception:
        fallback = {"EUR":1.0,"USD":1.08,"THB":39.0,"IDR":17800.0,"ARS":1000.0,"GEL":3.0,"BRL":5.6,"COP":4400.0,"CHF":0.95,"PHP":63.0}
        return fallback, False

# -----------------------------------------------------------------------------
# Funzioni statistiche e simulazione
# -----------------------------------------------------------------------------
def _phi(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def _erfinv_bisect(y, lo=-6.0, hi=6.0, iters=60):
    y = max(min(y, 0.999999), -0.999999)
    for _ in range(iters):
        m = 0.5*(lo+hi)
        v = math.erf(m)
        if v < y: lo = m
        else: hi = m
    return 0.5*(lo+hi)

def sigma_from_gini_lognormal(G): return 2.0*_erfinv_bisect(G)
def mu_from_mean_lognormal(mean, sigma): return math.log(mean) - 0.5*sigma*sigma

def percentile_lognormal(W, mean, gini):
    sigma = sigma_from_gini_lognormal(gini)
    mu = mu_from_mean_lognormal(mean, sigma)
    z = (math.log(max(W,1e-9)) - mu) / sigma
    return 100.0 * _phi(z)

def simulate_capital(wealth0, spend_real_year, r_real_port, infl, age_start, age_end,
                     pension=0.0, start_pension_age=67, rent_income=0.0):
    years = age_end - age_start
    ages = list(range(age_start, age_end+1))
    cap_real = [wealth0]
    for t in range(1, years+1):
        cr_prev = cap_real[-1]
        age = age_start + t
        inflows = rent_income + (pension if age >= start_pension_age else 0.0)
        spend_net = max(0.0, spend_real_year - inflows)
        cr_t = max(0.0, cr_prev * (1 + r_real_port) - spend_net)
        cap_real.append(cr_t)
    cap_nom = [cap_real[i]*((1+infl)**i) for i in range(len(cap_real))]
    return ages, cap_real, cap_nom

# -----------------------------------------------------------------------------
# Traduzioni robuste + UI lingua
# -----------------------------------------------------------------------------
@st.cache_data
def load_i18n():
    try:
        with open("translations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        # Se il file è vuoto o manca 'en' → uso il fallback
        if not isinstance(data, dict) or not data or "en" not in data:
            return FALLBACK_I18N
        return data
    except Exception:
        return FALLBACK_I18N

def T(lang, key, **kwargs):
    base = I18N.get("en", {})
    cur = I18N.get(lang, base)
    val = cur.get(key, base.get(key, key))
    return val.format(**kwargs) if kwargs else val

I18N = load_i18n()
langs = list(I18N.keys()) if isinstance(I18N, dict) and I18N else list(FALLBACK_I18N.keys())
default_idx = langs.index("it") if "it" in langs else 0

lang = st.sidebar.selectbox("Language / Lingua / Idioma / Langue",
                            options=langs, index=default_idx)

meta_label = I18N.get(lang, I18N.get("en", {})).get("meta_language_label", "Language")
st.sidebar.write(f"{meta_label}: {lang.upper()}")

st.title(T(lang, "title"))
st.caption(T(lang, "subtitle"))

# -----------------------------------------------------------------------------
# Carica dati e FX
# -----------------------------------------------------------------------------
cities = load_cities()
fx, live = get_fx_rates()
st.sidebar.write(f"{T(lang,'sidebar_fx')}: {'🟢 live' if live else '🟡 fallback'}")

# -----------------------------------------------------------------------------
# Sidebar: input principali
# -----------------------------------------------------------------------------
st.sidebar.header(T(lang, "origin_header"))
origin_city = st.sidebar.selectbox(
    T(lang, "origin_city"),
    options=cities["city"].tolist(),
    index=int((cities["city"]=="Rome").idxmax() if "Rome" in list(cities["city"]) else 0)
)
adj_pct = st.sidebar.slider(T(lang, "origin_adj"), -50, 50, 0, step=5)

st.sidebar.header(T(lang, "user_params"))
wealth0 = st.sidebar.number_input(T(lang,"wealth"), min_value=0, value=500000, step=1000)
age = st.sidebar.number_input(T(lang,"age"), min_value=18, max_value=90, value=40, step=1)
horizon_age = st.sidebar.number_input(T(lang,"horizon"), min_value=age+5, max_value=100, value=90, step=1)

st.sidebar.subheader(T(lang,"style_spend"))
total_spend_year = st.sidebar.number_input(T(lang,"total_spend"), min_value=0, value=30000, step=500)
style_options = [T(lang,"style_frugal"), T(lang,"style_normal"), T(lang,"style_fat")]
stile = st.sidebar.select_slider(T(lang,"style"), options=style_options, value=T(lang,"style_normal"))
mult_map = {T(lang,"style_frugal"):0.7, T(lang,"style_normal"):1.0, T(lang,"style_fat"):1.3}
mult = mult_map.get(stile, 1.0)

st.sidebar.subheader(T(lang,"preset_cats"))
cats = ["housing","food","transport","utilities","leisure","healthcare"]  # lasciate in EN
defaults = {"housing":35,"food":25,"transport":12,"utilities":8,"leisure":10,"healthcare":10}
perc = {}; tot = 0
for c in cats:
    perc[c] = st.sidebar.number_input(f"{c.capitalize()} %", min_value=0, max_value=100, value=defaults[c], step=1)
    tot += perc[c]
if tot != 100:
    st.sidebar.error(T(lang,"sum100_error", tot=tot))

st.sidebar.subheader(T(lang,"portfolio"))
w_stocks = st.sidebar.slider(T(lang,"stocks"), 0, 100, 60, 5)
w_bonds  = st.sidebar.slider(T(lang,"bonds"), 0, 100, 30, 5)
w_cash   = st.sidebar.slider(T(lang,"cash"), 0, 100, 5, 5)
w_re     = st.sidebar.slider(T(lang,"realestate"), 0, 100, 5, 5)
w_sum = w_stocks + w_bonds + w_cash + w_re
if w_sum != 100:
    st.sidebar.error(T(lang,"weights_error", tot=w_sum))

r_stocks = st.sidebar.slider(T(lang,"r_stocks"), 0.00, 0.10, 0.05, 0.005)
r_bonds  = st.sidebar.slider(T(lang,"r_bonds"), 0.00, 0.06, 0.02, 0.005)
r_cash   = st.sidebar.slider(T(lang,"r_cash"), 0.00, 0.03, 0.00, 0.005)
r_re_app = st.sidebar.slider(T(lang,"r_re"), -0.02, 0.06, 0.01, 0.005)

st.sidebar.subheader(T(lang,"rent"))
rent_income = st.sidebar.number_input(T(lang,"rent"), min_value=0, value=0, step=500)

r_real_port = (w_stocks/100)*r_stocks + (w_bonds/100)*r_bonds + (w_cash/100)*r_cash + (w_re/100)*r_re_app

st.sidebar.subheader(T(lang,"infl_pens"))
infl = st.sidebar.slider(T(lang,"infl"), 0.0, 0.08, 0.02, 0.005)
pensione = st.sidebar.number_input(T(lang,"pension"), min_value=0, value=0, step=500)
start_pens_age = st.sidebar.number_input(T(lang,"pension_age"), min_value=age, max_value=horizon_age, value=max(age,67))

# Lookup robusto della città selezionata
if cities is None or cities.empty or "city" not in cities.columns:
    st.error("Dataset città non disponibile o vuoto. Carica 'cities_demo.csv' o usa il fallback.")
    st.stop()

mask = cities["city"].astype(str).eq(str(origin_city))
if not mask.any():
    st.warning(f"La città '{origin_city}' non è nel dataset. Uso la prima disponibile.")
    origin_city = cities["city"].iloc[0]
    mask = cities["city"].astype(str).eq(str(origin_city))

ori = cities.loc[mask].iloc[0] -----------------------------------------------------------------------------

adj_mult = 1.0 + (adj_pct/100.0)
origin_idx_by_cat = {
    "housing": ori["idx_housing"]*adj_mult,
    "food": ori["idx_food"]*adj_mult,
    "transport": ori["idx_transport"]*adj_mult,
    "utilities": ori["idx_utilities"]*adj_mult,
    "leisure": ori["idx_leisure"]*adj_mult,
    "healthcare": ori["idx_healthcare"]*adj_mult,
}

spend_base = total_spend_year * mult
breakdown_user = {c: spend_base * (perc[c]/100.0) for c in cats}

rows = []
details = {}
for _, row in cities.iterrows():
    dest_idx = {
        "housing": row["idx_housing"], "food": row["idx_food"], "transport": row["idx_transport"],
        "utilities": row["idx_utilities"], "leisure": row["idx_leisure"], "healthcare": row["idx_healthcare"]
    }
    bc = {c: breakdown_user[c] * (dest_idx[c] / max(origin_idx_by_cat[c], 1e-6)) for c in cats}
    total_city = sum(bc.values())

    inflows_now = rent_income + (pensione if start_pens_age<=age else 0.0)
    spend_net_now = max(0.0, total_city - inflows_now)

    if total_city <= rent_income:
        fire_pct = 999.0
    else:
        pv_required = (total_city - rent_income) / max(r_real_port, 1e-6)
        fire_pct = 100.0 * (wealth0 / pv_required)

    years_autonomy = float("inf") if spend_net_now==0 else wealth0 / spend_net_now

    cur = row["currency"]
    rate = fx.get(cur, 1.0)
    local_total = total_city * rate

    perc_now = percentile_lognormal(wealth0, row["mean_wealth_per_adult"], row["gini_wealth"])

    rows.append({
        "city": row["city"], "country": row["country"], "currency": cur,
        "spend_eur": total_city, "spend_local": local_total,
        "fire_pct": fire_pct, "years_autonomy": years_autonomy,
        "wealth_percentile": perc_now, "lat": row["lat"], "lon": row["lon"]
    })
    details[row["city"]] = {"breakdown_city": bc, "currency": cur, "rate": rate}

table = pd.DataFrame(rows).sort_values("fire_pct", ascending=False).reset_index(drop=True)

# -----------------------------------------------------------------------------
# Mappa: modalità colore
# -----------------------------------------------------------------------------
st.sidebar.subheader(T(lang,"map_mode"))
mode_options = [T(lang,"mode_fire"), T(lang,"mode_years"), T(lang,"mode_percentile"), T(lang,"mode_path"), T(lang,"mode_fat")]
mode = st.sidebar.selectbox(T(lang,"map_mode"), options=mode_options, index=0)

style_target_options = [T(lang,"style_frugal"), T(lang,"style_normal"), T(lang,"style_fat")]
style_target = st.sidebar.selectbox(T(lang,"style_target"), options=style_target_options, index=2)
perc_thresh = st.sidebar.slider(T(lang,"percentile_thresh"), 1, 50, 10, 1)

def metric_and_colors(df):
    if mode == T(lang,"mode_fire") or mode == T(lang,"mode_path"):
        metric = df["fire_pct"]
        legend = T(lang,"mode_fire")
        colors = df["fire_pct"].apply(lambda x: "green" if x>=100 else ("orange" if x>=60 else "red"))
    elif mode == T(lang,"mode_years"):
        metric = df["years_autonomy"].replace(np.inf, 999.0)
        legend = T(lang,"mode_years")
        colors = metric.apply(lambda x: "green" if x>=30 else ("orange" if x>=15 else "red"))
    elif mode == T(lang,"mode_percentile"):
        metric = df["wealth_percentile"]
        legend = T(lang,"mode_percentile")
        colors = metric.apply(lambda p: "green" if p >= (100 - perc_thresh) else ("orange" if p >= 50 else "red"))
    else:
        target_mult = {T(lang,"style_frugal"):0.7, T(lang,"style_normal"):1.0, T(lang,"style_fat"):1.3}[style_target]
        scaled = df.copy()
        scaled["spend_eur_scaled"] = df["spend_eur"] * (target_mult / mult)
        scaled["fire_pct_target"] = 100.0 * wealth0 / np.maximum((scaled["spend_eur_scaled"] - rent_income), 1e-6) / max(r_real_port, 1e-6)
        metric = scaled["fire_pct_target"]
        legend = T(lang,"mode_fat")
        colors = metric.apply(lambda x: "green" if x>=100 else ("orange" if x>=60 else "red"))
    return metric, legend, colors

metric, legend_text, colors = metric_and_colors(table)

# -----------------------------------------------------------------------------
# Output: Tabella + Mappa + Dettaglio
# -----------------------------------------------------------------------------
table_display = table.copy()
table_display["Spesa annua (€)"] = table_display["spend_eur"].round(0)
table_display["% FIRE (≈)"] = table_display["fire_pct"].round(1)
table_display["Anni autonomia (≈)"] = table_display["years_autonomy"].replace(np.inf, 999).round(1)
table_display["Percentile ricchezza (≈)"] = table_display["wealth_percentile"].round(1)

tab1, tab2 = st.tabs([T(lang,"tab_table"), T(lang,"tab_map")])

with tab1:
    st.subheader(T(lang,"rank_title"))
    st.dataframe(
        table_display.rename(columns={"city": T(lang,"city_label"), "country": T(lang,"country_label")})[
            [T(lang,"city_label"), T(lang,"country_label"), "Spesa annua (€)", "% FIRE (≈)", "Anni autonomia (≈)", "Percentile ricchezza (≈)"]
        ],
        use_container_width=True
    )
    st.markdown(f"**{T(lang,'top3')}**")
    st.table(
        table_display.head(3).rename(columns={"city":T(lang,"city_label"), "country":T(lang,"country_label")})[
            [T(lang,"city_label"), T(lang,"country_label"), "% FIRE (≈)", "Anni autonomia (≈)"]
        ]
    )

with tab2:
    st.subheader(T(lang,"map_title"))
    fig = px.scatter_geo(
        table, lat="lat", lon="lon",
        hover_name="city",
        hover_data={"country":True, "spend_eur":":.0f", "fire_pct":":.1f", "wealth_percentile":":.1f"},
        color=colors, color_discrete_map={"green":"green","orange":"orange","red":"red"},
        projection="natural earth"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**{T(lang,'legend')}** — {legend_text}: green ≥ 100%, orange 60–99%, red < 60%")

    st.divider()
    st.subheader(T(lang,"detail_city"))
    city_sel = st.selectbox(T(lang,"city_label"), table["city"].tolist(), index=0)

    r = cities[cities["city"]==city_sel].iloc[0]
    idx_dest = {"housing": r["idx_housing"], "food":r["idx_food"], "transport":r["idx_transport"],
                "utilities":r["idx_utilities"], "leisure":r["idx_leisure"], "healthcare":r["idx_healthcare"]}
    bc = {c: (total_spend_year*mult*(perc[c]/100.0))*(idx_dest[c]/max(origin_idx_by_cat[c],1e-6)) for c in cats}
    rate = fx.get(r["currency"], 1.0)
    pie_vals = [bc[c]*rate for c in cats]
    pie_labels = [c.capitalize() for c in cats]
    pie = px.pie(values=pie_vals, names=pie_labels, title=T(lang,"pie_title", cur=r["currency"]))
    st.plotly_chart(pie, use_container_width=True)

    ages, cap_real, cap_nom = simulate_capital(
        wealth0, sum(bc.values()), r_real_port, infl, age, horizon_age,
        pension=pensione, start_pension_age=start_pens_age, rent_income=rent_income
    )
    line = go.Figure()
    line.add_trace(go.Scatter(x=ages, y=cap_real, mode="lines", name="Real"))
    line.add_trace(go.Scatter(x=ages, y=cap_nom, mode="lines", name="Nominal"))
    line.update_layout(height=420, margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(line, use_container_width=True)

st.caption(T(lang, "note"))