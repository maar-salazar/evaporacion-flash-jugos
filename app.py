# ============================================
# app.py — Interfaz Streamlit
# Concentración de Jugos por Evaporación
# Flash Doble Efecto a Baja Presión
# FIQ BUAP — Dibujo Técnico
# ============================================

import streamlit as st
from modelo import calcular_proceso

# ---- Configuración de la página ----
st.set_page_config(
    page_title="Concentración de Jugos por Evaporación Flash | FIQ BUAP",
    page_icon=None,
    layout="wide"
)

# --- Toggle modo oscuro ---
modo_oscuro = st.sidebar.toggle("Modo oscuro", value=False)

if modo_oscuro:
    fondo      = "#0f1923"
    fondo_card = "#1a2e4a"
    texto      = "#e2e8f0"
    titulo     = "#63b3ed"
    subtitulo  = "#90cdf4"
    sidebar_bg = "#0a1628"
else:
    fondo      = "#ffffff"
    fondo_card = "#ebf4ff"
    texto      = "#1a2e4a"
    titulo     = "#1a2e4a"
    subtitulo  = "#2c5282"
    sidebar_bg = "#1a2e4a"

st.markdown(f"""
<style>
.stApp {{ background-color: {fondo}; }}
[data-testid="stSidebar"] {{ background-color: {sidebar_bg}; }}
[data-testid="stSidebar"] * {{ color: #ffffff !important; }}
h1, h2, h3, h4 {{ color: {titulo} !important; }}
p, li, td, th, label {{ color: {texto} !important; }}
[data-testid="stMetric"] {{
    background-color: {fondo_card};
    border-left: 4px solid {titulo};
    border-radius: 6px;
    padding: 12px;
}}
[data-testid="stMetricValue"] {{ color: {titulo} !important; }}
.stTabs [aria-selected="true"] {{
    background-color: #2c5282 !important;
    color: #ffffff !important;
    border-radius: 4px 4px 0 0;
    font-weight: 600 !important;
}}
.stTabs [aria-selected="false"] {{ color: {texto} !important; background-color: transparent !important; }}
.stTabs [data-baseweb="tab"] {{ color: {texto} !important; }}
.stDownloadButton > button, .stButton > button {{
    background-color: {titulo} !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
}}
.stAlert {{ background-color: {fondo_card} !important; color: {texto} !important; border-color: {titulo} !important; }}
.stAlert p {{ color: {texto} !important; }}
.stDownloadButton > button p {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# --- Header ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo_fiq.png", width=100)
    except:
        st.write("")

with col_titulo:
    st.markdown("""
        <h1 style='margin-bottom: 0; color: #1a2e4a;'>
            Concentración de Jugos por Evaporación Flash a Baja Presión
        </h1>
        <p style='color: #2c5282; font-size: 16px; margin-top: 4px;'>
            Benemérita Universidad Autónoma de Puebla &nbsp;|&nbsp;
            Facultad de Ingeniería Química &nbsp;|&nbsp;
            Dibujo Técnico
        </p>
    """, unsafe_allow_html=True)

st.divider()

# --- Sidebar: variables de operación ---
st.sidebar.header("Variables de operación")

T_pre = st.sidebar.slider(
    "Temperatura precalentador W-110 (°C)",
    min_value=80, max_value=100, value=95, step=1
)

P_etapa1 = st.sidebar.slider(
    "Presión Etapa 1 — B-210 (bar)",
    min_value=0.20, max_value=0.80, value=0.40, step=0.05
)

T_reheat = st.sidebar.slider(
    "Temperatura recalentador W-210 (°C)",
    min_value=70, max_value=95, value=85, step=1
)

P_etapa2 = st.sidebar.slider(
    "Presión Etapa 2 — B-220 (bar)",
    min_value=0.08, max_value=0.30, value=0.15, step=0.01
)

T_feed = st.sidebar.slider(
    "Temperatura de alimentación (°C)",
    min_value=15, max_value=45, value=25, step=1
)

# --- Cálculo automático ---
r = calcular_proceso(
    T_pre        = T_pre,
    P_etapa1_bar = P_etapa1,
    T_reheat     = T_reheat,
    P_etapa2_bar = P_etapa2,
    T_feed       = T_feed
)

# --- KPIs principales ---
st.subheader("Resultados del proceso")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(label="VAPOR-1 (Etapa 1)",  value=f"{r['V1_kg_h']} kg/h")
col2.metric(label="VAPOR-2 (Etapa 2)",  value=f"{r['V2_kg_h']} kg/h")
col3.metric(label="Producto final",      value=f"{r['L2_kg_h']} kg/h")
col4.metric(label="°Brix final",         value=f"{r['brix_final']}°Bx")
col5.metric(label="Q total (W-110 + W-210)", value=f"{round(r['Q_W110'] + r['Q_W210'], 2)} kW")

# ============================================
# Sección 2 — Tabla de corrientes
# ============================================
import pandas as pd

st.divider()
st.subheader("Balance de materia — Corrientes del proceso")

corrientes = [
    {"Corriente":"1-JUGO",          "Equipo":"Alimentación (B-110)",        "T (°C)":T_feed,            "P (bar)":1.0,      "Flujo (kg/h)":1000.0,        "Sacarosa (%)":10.0,                           "Agua (%)":90.0,                                "Fase":"Líquido"},
    {"Corriente":"2-CALIENTE",      "Equipo":"Salida W-110",                "T (°C)":T_pre,             "P (bar)":1.0,      "Flujo (kg/h)":1000.0,        "Sacarosa (%)":10.0,                           "Agua (%)":90.0,                                "Fase":"Líquido"},
    {"Corriente":"3-MEZCLA-1",      "Equipo":"Salida V-110",                "T (°C)":r["T1_sal"],       "P (bar)":P_etapa1, "Flujo (kg/h)":1000.0,        "Sacarosa (%)":10.0,                           "Agua (%)":90.0,                                "Fase":"Bifásico"},
    {"Corriente":"4-VAPOR-1",       "Equipo":"Vapor B-210 (agua pura)",     "T (°C)":r["T1_sal"],       "P (bar)":P_etapa1, "Flujo (kg/h)":r["V1_kg_h"],  "Sacarosa (%)":0.0,                            "Agua (%)":100.0,                               "Fase":"Vapor"},
    {"Corriente":"5-JUGO-PRECONC",  "Equipo":"Líquido B-210",               "T (°C)":r["T1_sal"],       "P (bar)":P_etapa1, "Flujo (kg/h)":r["L1_kg_h"],  "Sacarosa (%)":round(r["x1_sac"]*100, 2),      "Agua (%)":round((1-r["x1_sac"])*100, 2),       "Fase":"Líquido"},
    {"Corriente":"6-BOMBA",         "Equipo":"Salida P-210",                "T (°C)":r["T1_sal"],       "P (bar)":2.0,      "Flujo (kg/h)":r["L1_kg_h"],  "Sacarosa (%)":round(r["x1_sac"]*100, 2),      "Agua (%)":round((1-r["x1_sac"])*100, 2),       "Fase":"Líquido"},
    {"Corriente":"7-LISTO-FLASH",   "Equipo":"Salida W-210",                "T (°C)":T_reheat,          "P (bar)":2.0,      "Flujo (kg/h)":r["L1_kg_h"],  "Sacarosa (%)":round(r["x1_sac"]*100, 2),      "Agua (%)":round((1-r["x1_sac"])*100, 2),       "Fase":"Líquido"},
    {"Corriente":"8-MEZCLA-FINAL",  "Equipo":"Salida V-210",                "T (°C)":r["T2_sal"],       "P (bar)":P_etapa2, "Flujo (kg/h)":r["L1_kg_h"],  "Sacarosa (%)":round(r["x1_sac"]*100, 2),      "Agua (%)":round((1-r["x1_sac"])*100, 2),       "Fase":"Bifásico"},
    {"Corriente":"9-VAPOR-2",       "Equipo":"Vapor B-220 (agua pura)",     "T (°C)":r["T2_sal"],       "P (bar)":P_etapa2, "Flujo (kg/h)":r["V2_kg_h"],  "Sacarosa (%)":0.0,                            "Agua (%)":100.0,                               "Fase":"Vapor"},
    {"Corriente":"10-PRODUCTO-FINAL","Equipo":"Líquido B-220",              "T (°C)":r["T2_sal"],       "P (bar)":P_etapa2, "Flujo (kg/h)":r["L2_kg_h"],  "Sacarosa (%)":round(r["x2_sac"]*100, 2),      "Agua (%)":round((1-r["x2_sac"])*100, 2),       "Fase":"Líquido"},
    {"Corriente":"11-PRODUCTO-TANK","Equipo":"Almacenamiento B-230",        "T (°C)":r["T2_sal"],       "P (bar)":1.0,      "Flujo (kg/h)":r["L2_kg_h"],  "Sacarosa (%)":round(r["x2_sac"]*100, 2),      "Agua (%)":round((1-r["x2_sac"])*100, 2),       "Fase":"Líquido"},
]

df = pd.DataFrame(corrientes)
st.dataframe(df, use_container_width=True, hide_index=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar tabla en CSV",
    data=csv,
    file_name="balance_materia_jugos.csv",
    mime="text/csv"
)

st.caption("""
**Supuesto:** Sacarosa no evapora — el vapor generado en ambas etapas es agua pura.
Modelo calibrado con NRTL/DWSIM. Caso base: VAPOR-1=41.87 kg/h, Producto=900.12 kg/h.
""")

# ============================================
# Sección 3 — Análisis económico
# ============================================
st.divider()
st.subheader("Análisis económico")

st.sidebar.divider()
st.sidebar.header("Precios de insumos")

precio_vapor  = st.sidebar.slider("Vapor (MXN/ton)",          100, 400, 180, 10)
precio_elec   = st.sidebar.slider("Electricidad (MXN/kWh)",   1.0, 5.0, 2.5, 0.1)
precio_agua   = st.sidebar.slider("Agua (MXN/m³)",            5,   30,  15,  1)
precio_jugo   = st.sidebar.slider("Jugo fresco (MXN/kg)",     2,   15,  5,   1)
precio_conc   = st.sidebar.slider("Jugo concentrado (MXN/kg)",8,   40,  20,  1)

# Parámetros de proyecto
inversion        = 12_000_000
horas_anio       = 8_000
vida_util        = 10
tasa_descuento   = 0.10

# Costos operativos
vapor_ton_h1  = r["Q_W110"] * 3.6 / 2260
vapor_ton_h2  = r["Q_W210"] * 3.6 / 2260
costo_vapor_h = (vapor_ton_h1 + vapor_ton_h2) * precio_vapor

costo_elec_h  = r["W_bomba"] * precio_elec
agua_m3_h     = (r["V1_kg_h"] + r["V2_kg_h"]) / 1000
costo_agua_h  = agua_m3_h * precio_agua
costo_jugo_h  = 1000 * precio_jugo

costo_total_h = costo_vapor_h + costo_elec_h + costo_agua_h + costo_jugo_h
costo_por_kg  = costo_total_h / r["L2_kg_h"] if r["L2_kg_h"] > 0 else 0
precio_sugerido = costo_por_kg * 1.30

ingreso_anual = r["L2_kg_h"] * horas_anio * precio_conc
costo_anual   = costo_total_h * horas_anio
flujo_caja    = ingreso_anual - costo_anual

npv     = sum([flujo_caja / (1 + tasa_descuento)**t for t in range(1, vida_util + 1)]) - inversion
payback = inversion / flujo_caja if flujo_caja > 0 else float("inf")
roi     = (flujo_caja * vida_util - inversion) / inversion * 100

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

col1.metric("Costo de producción", f"${costo_por_kg:.2f} MXN/kg")
col2.metric("Precio sugerido",     f"${precio_sugerido:.2f} MXN/kg")

def fmt(n):
    if abs(n) >= 1_000_000:
        return f"${n/1_000_000:.2f}M MXN"
    elif abs(n) >= 1_000:
        return f"${n/1_000:.1f}K MXN"
    else:
        return f"${n:.0f} MXN"

col3.metric("VPN",     fmt(npv))
col4.metric("Payback", f"{payback:.1f} años")
col5.metric("ROI",     f"{roi:.1f}%")

st.divider()
if precio_sugerido < precio_conc:
    st.success("✅ El precio sugerido es competitivo en el mercado.")
else:
    st.warning("⚠️ El precio sugerido supera el precio de mercado del jugo concentrado.")

if npv > 0:
    st.success(f"✅ VPN positivo — el proyecto es rentable a {tasa_descuento*100:.0f}% de descuento.")
else:
    st.error("❌ VPN negativo — revisar condiciones de operación o precios.")

if payback > vida_util:
    st.error(f"❌ Payback ({payback:.1f} años) supera la vida útil ({vida_util} años).")
elif payback > 5:
    st.warning(f"⚠️ Payback de {payback:.1f} años — considera optimizar costos.")
else:
    st.success(f"✅ Payback de {payback:.1f} años — recuperación aceptable.")

# ============================================
# Sección 4 — Análisis de sensibilidad
# ============================================
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.divider()
st.subheader("Análisis de sensibilidad")

# Barrido T_pre
T_rango   = list(range(80, 101))
V1_lista, V2_lista, brix_lista = [], [], []
for T in T_rango:
    res = calcular_proceso(T_pre=T, P_etapa1_bar=P_etapa1,
                           T_reheat=T_reheat, P_etapa2_bar=P_etapa2, T_feed=T_feed)
    V1_lista.append(res["V1_kg_h"])
    V2_lista.append(res["V2_kg_h"])
    brix_lista.append(res["brix_final"])

# Barrido P_etapa1
P1_rango  = [round(p, 2) for p in np.arange(0.20, 0.81, 0.05)]
prod_P1   = []
for P in P1_rango:
    res = calcular_proceso(T_pre=T_pre, P_etapa1_bar=P,
                           T_reheat=T_reheat, P_etapa2_bar=P_etapa2, T_feed=T_feed)
    prod_P1.append(res["L2_kg_h"])

# Barrido P_etapa2
P2_rango  = [round(p, 2) for p in np.arange(0.08, 0.31, 0.01)]
brix_P2   = []
for P in P2_rango:
    res = calcular_proceso(T_pre=T_pre, P_etapa1_bar=P_etapa1,
                           T_reheat=T_reheat, P_etapa2_bar=P, T_feed=T_feed)
    brix_P2.append(res["brix_final"])

# Barrido precio jugo vs VPN
jugo_rango = list(range(2, 16))
npv_lista  = []
for pj in jugo_rango:
    ch = costo_vapor_h + costo_elec_h + costo_agua_h + (1000 * pj)
    fc = (r["L2_kg_h"] * horas_anio * precio_conc) - (ch * horas_anio)
    npv_j = sum([fc / (1 + tasa_descuento)**t for t in range(1, vida_util + 1)]) - inversion
    npv_lista.append(npv_j / 1_000_000)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=[
        "T_pre vs Vapor generado (Etapa 1 y 2)",
        "P Etapa 1 vs Producto final",
        "P Etapa 2 vs °Brix final",
        "Precio jugo fresco vs VPN"
    ]
)

fig.add_trace(go.Scatter(x=T_rango, y=V1_lista, mode="lines+markers",
    line=dict(color="#e74c3c", width=2), name="VAPOR-1"), row=1, col=1)
fig.add_trace(go.Scatter(x=T_rango, y=V2_lista, mode="lines+markers",
    line=dict(color="#e67e22", width=2, dash="dash"), name="VAPOR-2"), row=1, col=1)

fig.add_trace(go.Scatter(x=P1_rango, y=prod_P1, mode="lines+markers",
    line=dict(color="#3498db", width=2), name="Producto (kg/h)"), row=1, col=2)

fig.add_trace(go.Scatter(x=P2_rango, y=brix_P2, mode="lines+markers",
    line=dict(color="#2ecc71", width=2), name="°Brix final"), row=2, col=1)

fig.add_trace(go.Scatter(x=jugo_rango, y=npv_lista, mode="lines+markers",
    line=dict(color="#9b59b6", width=2), name="VPN (M MXN)"), row=2, col=2)

fig.add_vline(x=T_pre,    line_dash="dash", line_color="gray",
    annotation_text=f"Actual: {T_pre}°C", row=1, col=1)
fig.add_vline(x=P_etapa1, line_dash="dash", line_color="gray",
    annotation_text=f"Actual: {P_etapa1} bar", row=1, col=2)
fig.add_vline(x=P_etapa2, line_dash="dash", line_color="gray",
    annotation_text=f"Actual: {P_etapa2} bar", row=2, col=1)
fig.add_vline(x=precio_jugo, line_dash="dash", line_color="gray",
    annotation_text=f"Actual: {precio_jugo}", row=2, col=2)

fig.update_xaxes(title_text="T precalentador (°C)", row=1, col=1)
fig.update_xaxes(title_text="Presión Etapa 1 (bar)", row=1, col=2)
fig.update_xaxes(title_text="Presión Etapa 2 (bar)", row=2, col=1)
fig.update_xaxes(title_text="Precio jugo (MXN/kg)",  row=2, col=2)
fig.update_yaxes(title_text="kg/h",        row=1, col=1)
fig.update_yaxes(title_text="kg/h",        row=1, col=2)
fig.update_yaxes(title_text="°Brix",       row=2, col=1)
fig.update_yaxes(title_text="M MXN",       row=2, col=2)

fig.update_layout(height=600, showlegend=True,
    title_text="Sensibilidad de variables operativas y económicas")
st.plotly_chart(fig, use_container_width=True)

# ============================================
# Sección 5 — Comparación de escenarios
# ============================================
st.divider()
st.subheader("Comparación de escenarios")

escenarios = {
    "🟢 Caso Base"    : {"T_pre":95, "P1":0.40, "T_re":85, "P2":0.15, "p_jugo":5,  "p_conc":20},
    "🔵 Caso Óptimo"  : {"T_pre":92, "P1":0.35, "T_re":82, "P2":0.12, "p_jugo":5,  "p_conc":20},
    "🟡 Caso Económico":{"T_pre":95, "P1":0.40, "T_re":85, "P2":0.15, "p_jugo":3,  "p_conc":25},
    "🔴 Caso Crítico"  :{"T_pre":95, "P1":0.60, "T_re":85, "P2":0.25, "p_jugo":10, "p_conc":12},
}

resultados_esc = {}
for nombre, p in escenarios.items():
    re = calcular_proceso(T_pre=p["T_pre"], P_etapa1_bar=p["P1"],
                          T_reheat=p["T_re"], P_etapa2_bar=p["P2"], T_feed=25)
    ch_e = (((re["Q_W110"]+re["Q_W210"])*3.6/2260)*precio_vapor +
             re["W_bomba"]*precio_elec +
             ((re["V1_kg_h"]+re["V2_kg_h"])/1000)*precio_agua +
             1000*p["p_jugo"])
    fc_e = (re["L2_kg_h"]*horas_anio*p["p_conc"]) - (ch_e*horas_anio)
    npv_e = sum([fc_e/(1+tasa_descuento)**t for t in range(1, vida_util+1)]) - inversion
    resultados_esc[nombre] = {
        "T_pre (°C)"    : p["T_pre"],
        "P1 (bar)"      : p["P1"],
        "T_reheat (°C)" : p["T_re"],
        "P2 (bar)"      : p["P2"],
        "Producto (kg/h)": re["L2_kg_h"],
        "°Brix final"   : re["brix_final"],
        "Q total (kW)"  : round(re["Q_W110"]+re["Q_W210"], 2),
        "VPN (M MXN)"   : round(npv_e/1_000_000, 2),
    }

df_esc = pd.DataFrame(resultados_esc).T
st.dataframe(df_esc, use_container_width=True)

st.markdown("##### VPN por escenario")
fig_esc = go.Figure()
colores = ["#2ecc71", "#3498db", "#f1c40f", "#e74c3c"]
for i, (nombre, vals) in enumerate(resultados_esc.items()):
    fig_esc.add_trace(go.Bar(
        name=nombre, x=[nombre], y=[vals["VPN (M MXN)"]],
        marker_color=colores[i],
        text=[f"${vals['VPN (M MXN)']}M"], textposition="auto"
    ))
fig_esc.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="VPN = 0")
fig_esc.update_layout(height=350, showlegend=False,
    yaxis_title="VPN (Millones MXN)", title="Comparación de VPN por escenario")
st.plotly_chart(fig_esc, use_container_width=True)

# ============================================
# Sección 6 — Diagramas del proceso
# ============================================
st.divider()
st.subheader("Diagramas del proceso")

tab1, tab2, tab3 = st.tabs([
    "📦 Diagrama de Bloques",
    "🔄 Diagrama de Flujo (PFD)",
    "🔧 Tuberías e Instrumentación (P&ID)"
])

with tab1:
    st.markdown("""
    **Diagrama de Bloques** — flujo global del proceso doble efecto.
    Secciones 100 (alimentación), 200 (primera etapa) y 300 (segunda etapa + almacenamiento).
    """)
    archivo = st.file_uploader("Sube el diagrama de bloques (PDF o imagen)",
        type=["pdf","png","jpg"], key="bloques")
    if archivo:
        if archivo.type == "application/pdf":
            st.download_button("📥 Descargar", archivo, file_name="diagrama_bloques.pdf")
            st.info("PDF cargado. Usa el botón para descargarlo.")
        else:
            st.image(archivo, caption="Diagrama de Bloques", use_container_width=True)
    else:
        st.info("👆 Sube tu diagrama de bloques exportado desde AutoCAD Plant 3D")

with tab2:
    st.markdown("""
    **Diagrama de Flujo de Proceso (PFD)** — equipos reales, corrientes numeradas,
    condiciones de operación y balance de materia de las 11 corrientes.
    """)
    archivo_pfd = st.file_uploader("Sube el PFD (PDF o imagen)",
        type=["pdf","png","jpg"], key="pfd")
    if archivo_pfd:
        if archivo_pfd.type == "application/pdf":
            st.download_button("📥 Descargar PFD", archivo_pfd, file_name="PFD.pdf")
            st.info("PDF cargado. Usa el botón para descargarlo.")
        else:
            st.image(archivo_pfd, caption="PFD", use_container_width=True)
    else:
        st.info("👆 Sube tu PFD exportado desde AutoCAD Plant 3D")

with tab3:
    st.markdown("""
    **Diagrama de Tuberías e Instrumentación (P&ID)** — instrumentos, controladores
    y válvulas. Lazos: nivel B-110 (100-LC-111), presión B-210 (PC-211),
    temperatura W-210 (TC-211), nivel B-220 (LC-221), nivel B-230 (LC-231).
    """)
    archivo_pid = st.file_uploader("Sube el P&ID (PDF o imagen)",
        type=["pdf","png","jpg"], key="pid")
    if archivo_pid:
        if archivo_pid.type == "application/pdf":
            st.download_button("📥 Descargar P&ID", archivo_pid, file_name="PID.pdf")
            st.info("PDF cargado. Usa el botón para descargarlo.")
        else:
            st.image(archivo_pid, caption="P&ID", use_container_width=True)
    else:
        st.info("👆 Sube tu P&ID exportado desde AutoCAD Plant 3D")

# ============================================
# Sección 7 — Tutor con IA
# ============================================
import google.generativeai as genai

st.divider()
st.subheader("🤖 Tutor de Ingeniería Química")
st.markdown("Pregúntale al tutor sobre el proceso, los resultados o los conceptos involucrados.")

api_key = st.sidebar.text_input(
    "🔑 API Key de Gemini",
    type="password",
    placeholder="AIzaSy..."
)

if api_key:
    contexto_sistema = f"""
Eres un tutor experto en ingeniería química especializado en procesos de separación y concentración.
Estás ayudando a un estudiante de FIQ BUAP con su proyecto de Dibujo Técnico.
El proceso es una Planta de Concentración de Jugos por Evaporación Flash Doble Efecto a Baja Presión.
Sistema binario: Agua + Sacarosa. Modelo termodinámico: NRTL.

CONDICIONES ACTUALES:
- Temperatura precalentador W-110: {T_pre}°C
- Presión Etapa 1 (B-210): {P_etapa1} bar
- Temperatura recalentador W-210: {T_reheat}°C
- Presión Etapa 2 (B-220): {P_etapa2} bar
- Temperatura alimentación: {T_feed}°C

RESULTADOS ACTUALES:
- VAPOR-1: {r['V1_kg_h']} kg/h | T salida: {r['T1_sal']}°C
- VAPOR-2: {r['V2_kg_h']} kg/h | T salida: {r['T2_sal']}°C
- Producto final: {r['L2_kg_h']} kg/h | °Brix: {r['brix_final']}
- Q W-110: {r['Q_W110']} kW | Q W-210: {r['Q_W210']} kW
- VPN: ${npv:,.0f} MXN | Payback: {payback:.1f} años

Responde siempre en español, de forma clara y didáctica.
"""

    if "historial" not in st.session_state:
        st.session_state.historial = []

    for mensaje in st.session_state.historial:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:
        with st.chat_message("user"):
            st.markdown(pregunta)
        st.session_state.historial.append({"role":"user","content":pregunta})

        try:
            genai.configure(api_key=api_key)
            modelos_disponibles = [
                m.name for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]
            if not modelos_disponibles:
                st.error("No se encontraron modelos disponibles.")
            else:
                modelo_ia = genai.GenerativeModel(modelos_disponibles[0])
                respuesta = modelo_ia.generate_content(
                    contexto_sistema + "\n\nPregunta: " + pregunta
                )
                texto = respuesta.text
                with st.chat_message("assistant"):
                    st.markdown(texto)
                st.session_state.historial.append({"role":"assistant","content":texto})
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
else:
    st.info("👆 Ingresa tu API Key de Gemini en el sidebar para activar el tutor.")

# ============================================
# Sección 8 — Supuestos y documentación
# ============================================
st.divider()
st.subheader("Supuestos y documentación")

tab_s1, tab_s2, tab_s3 = st.tabs(["Termodinámicos", "Económicos", "Archivos del proyecto"])

with tab_s1:
    st.markdown("""
### Supuestos termodinámicos
- Sistema binario **Agua + Sacarosa** (solución no ideal)
- Paquete termodinámico: **NRTL** (Non-Random Two-Liquid)
- Presiones de vapor calculadas con **ecuación de Antoine**
- **La sacarosa no evapora** — el vapor generado en ambas etapas es agua pura
- Flash **isentálpico** en válvulas V-110 y V-210
- **BPE (Boiling Point Elevation)** calibrada con DWSIM:
  - A 10% sacarosa → BPE ≈ 0.2°C
  - A 40% sacarosa → BPE ≈ 2.5°C
- Factores de calibración por etapa vs DWSIM:
  - Etapa 1: factor = 1.306 → VAPOR-1 = 41.87 kg/h ✓
  - Etapa 2: factor = 1.187 → VAPOR-2 = 58.00 kg/h ✓

### Limitaciones del modelo
- Coeficientes de actividad simplificados (no varían con T ni concentración)
- Modelo utilizado como herramienta de **análisis de sensibilidad relativa**
""")

with tab_s2:
    st.markdown(f"""
### Supuestos económicos

| Parámetro | Valor |
|-----------|-------|
| Inversión inicial | ${inversion:,.0f} MXN |
| Vida útil | {vida_util} años |
| Horas de operación | {horas_anio:,} h/año |
| Tasa de descuento | {tasa_descuento*100:.0f}% anual |
| Precio vapor | ${precio_vapor} MXN/ton |
| Precio electricidad | ${precio_elec} MXN/kWh |
| Precio agua enfriamiento | ${precio_agua} MXN/m³ |
| Precio jugo fresco | ${precio_jugo} MXN/kg |
| Precio jugo concentrado | ${precio_conc} MXN/kg |

### Notas
- VPN calculado con flujos de caja anuales constantes
- No se incluye depreciación ni impuestos
- Precios de referencia para análisis comparativo
""")

with tab_s3:
    st.markdown("### Estructura del proyecto")
    st.code("""
evaporacion_flash_jugos/
├── app.py          ← Interfaz Streamlit (este archivo)
├── modelo.py       ← Motor de cálculo termodinámico
├── flash.py        ← Desarrollo paso a paso
└── requirements.txt
    """, language="bash")

    st.markdown("### Tecnologías utilizadas")
    st.markdown("""
- **Python 3.11** — lenguaje de programación
- **Streamlit** — interfaz web interactiva
- **SciPy** — resolución numérica (brentq)
- **Plotly** — gráficas interactivas
- **Pandas** — manejo de tablas
- **Gemini API** — tutor con IA
- **DWSIM** — simulador de referencia (NRTL)
""")

    st.markdown("### Referencia del caso base")
    st.info("""
Simulación realizada en DWSIM por Marlet Salazar Hernández,
FIQ BUAP, Marzo 2026. Reporte: Planta de Concentración de
Jugos por Evaporación Flash Doble Efecto a Baja Presión.
""")