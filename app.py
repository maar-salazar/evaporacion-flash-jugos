# ============================================
# app.py — Interfaz Streamlit
# Planta de Concentración de Mosto
# ============================================
import streamlit as st
from modelo import calcular_proceso

# ---- Configuración de la página ----
st.set_page_config(
    page_title="Proceso de Concentración de Mosto | FIQ BUAP",
    page_icon=None,
    layout="wide"
)

# --- Estilos globales azul marino ---
# --- Toggle modo oscuro ---
modo_oscuro = st.sidebar.toggle("Modo oscuro", value=False)

if modo_oscuro:
    fondo        = "#0f1923"
    fondo_card   = "#1a2e4a"
    texto        = "#e2e8f0"
    titulo       = "#63b3ed"
    subtitulo    = "#90cdf4"
    sidebar_bg   = "#0a1628"
else:
    fondo        = "#ffffff"
    fondo_card   = "#ebf4ff"
    texto        = "#1a2e4a"
    titulo       = "#1a2e4a"
    subtitulo    = "#2c5282"
    sidebar_bg   = "#1a2e4a"

st.markdown(f"""
<style>
    /* Fondo principal */
    .stApp {{
        background-color: {fondo};
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    /* Títulos */
    h1, h2, h3, h4 {{
        color: {titulo} !important;
    }}
    /* Texto general */
    p, li, td, th, label {{
        color: {texto} !important;
    }}
    /* Métricas */
    [data-testid="stMetric"] {{
        background-color: {fondo_card};
        border-left: 4px solid {titulo};
        border-radius: 6px;
        padding: 12px;
    }}
    [data-testid="stMetricValue"] {{
        color: {titulo} !important;
    }}
    /* Tabs */
    .stTabs [aria-selected="true"] {{
    background-color: #2c5282 !important;
    color: #ffffff !important;
    border-radius: 4px 4px 0 0;
    font-weight: 600 !important;
}}
.stTabs [aria-selected="false"] {{
    color: {texto} !important;
    background-color: transparent !important;
}}
.stTabs [data-baseweb="tab"] span {{
    color: inherit !important;
}}
.stTabs [data-baseweb="tab"] {{
    color: {texto} !important;
}}

    /* Botones */
    .stDownloadButton > button, .stButton > button {{
        background-color: {titulo} !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
    }}
    .stTabs [aria-selected="false"] {{
        color: {texto} !important;
    }}
    /* Info boxes modo claro */
    .stAlert {{
        background-color: {fondo_card} !important;
        color: {texto} !important;
        border-color: {titulo} !important;
    }}
    .stAlert p {{
        color: {texto} !important;
    }}
    /* Botón descarga — asegurar texto visible */
    .stDownloadButton > button p {{
        color: white !important;
    }}
    /* Sliders sidebar */
    [data-testid="stSidebar"] input[type="range"]::-webkit-slider-thumb {{
        background-color: #63b3ed !important;
        border: 2px solid #ffffff !important;
    }}
    [data-testid="stSidebar"] input[type="range"]::-webkit-slider-runnable-track {{
        background-color: #2c5282 !important;
    }}
</style>
""", unsafe_allow_html=True)
# --- Header con logo ---
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        st.image("logo_fiq.png", width=100)
    except:
        st.write("")

with col_titulo:
    st.markdown("""
    <h1 style='margin-bottom: 0; color: #1a2e4a;'>
        Planta de Concentración de Mosto
    </h1>
    <p style='color: #2c5282; font-size: 16px; margin-top: 4px;'>
        Benemérita Universidad Autónoma de Puebla &nbsp;|&nbsp;
        Facultad de Ingeniería Química &nbsp;|&nbsp;
        Introducción a la Simulación de Procesos
    </p>
    """, unsafe_allow_html=True)

st.divider()

# --- Sidebar: sliders de control ---
st.sidebar.header("Variables de operación")

T_flash = st.sidebar.slider(
    "Temperatura del separador B-410 (°C)",
    min_value=75,
    max_value=98,
    value=92,
    step=1
)

P_flash = st.sidebar.slider(
    "Presión del separador B-410 (atm)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

T_feed = st.sidebar.slider(
    "Temperatura de alimentación (°C)",
    min_value=15,
    max_value=45,
    value=25,
    step=1
)

# --- Cálculo automático ---
r = calcular_proceso(T_flash=T_flash, P_flash_atm=P_flash, T_feed=T_feed)

# --- KPIs principales ---
st.subheader("Resultados del proceso")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Producto (vapor)",
    value=f"{r['V_kg_h']} kg/h"
)
col2.metric(
    label="Vinazas",
    value=f"{r['L_kg_h']} kg/h"
)
col3.metric(
    label="Etanol en producto",
    value=f"{r['y_etanol']*100:.1f}%"
)
col4.metric(
    label="Q calentador",
    value=f"{r['Q_calentador']} kW"
)
# ============================================
# Sección 2 — Tabla de corrientes
# ============================================
import pandas as pd

st.divider()
st.subheader("Balance de materia — Corrientes del proceso")

# Nota: valores base calibrados con DWSIM (fracciones molares convertidas a másicas)
# El modelo simplificado se usa para sensibilidad relativa

T_intermedia = round(25 + (T_flash - 25) * 0.30, 1)

corrientes = [
    {
        "Corriente"   : "1-MOSTO",
        "Equipo"      : "Alimentación",
        "T (°C)"      : T_feed,
        "P (atm)"     : 1.0,
        "Flujo (kg/h)": 1000.0,
        "EtOH (%)"    : 10.0,
        "H₂O (%)"     : 90.0,
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "2-MOSTO-PRESION",
        "Equipo"      : "Salida P-210",
        "T (°C)"      : T_feed,
        "P (atm)"     : 4.0,
        "Flujo (kg/h)": 1000.0,
        "EtOH (%)"    : 10.0,
        "H₂O (%)"     : 90.0,
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "3-MOSTO-PRE",
        "Equipo"      : "Salida W-210",
        "T (°C)"      : T_intermedia,
        "P (atm)"     : 4.0,
        "Flujo (kg/h)": 1000.0,
        "EtOH (%)"    : 10.0,
        "H₂O (%)"     : 90.0,
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "4-LIQ-CALIENTE",
        "Equipo"      : "Salida W-310",
        "T (°C)"      : T_flash,
        "P (atm)"     : 4.0,
        "Flujo (kg/h)": 1000.0,
        "EtOH (%)"    : 10.0,
        "H₂O (%)"     : 90.0,
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "5-MEZCLA-FLASH",
        "Equipo"      : "Salida V-310",
        "T (°C)"      : T_flash,
        "P (atm)"     : P_flash,
        "Flujo (kg/h)": 1000.0,
        "EtOH (%)"    : 10.0,
        "H₂O (%)"     : 90.0,
        "Fase"        : "Bifásico"
    },
    {
        "Corriente"   : "6-VAPOR",
        "Equipo"      : "Vapor B-410",
        "T (°C)"      : T_flash,
        "P (atm)"     : P_flash,
        "Flujo (kg/h)": r["V_kg_h"],
        "EtOH (%)"    : round(r["y_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["y_etanol"]) * 100, 1),
        "Fase"        : "Vapor"
    },
    {
        "Corriente"   : "7-VINAZAS",
        "Equipo"      : "Líquido B-410",
        "T (°C)"      : T_flash,
        "P (atm)"     : P_flash,
        "Flujo (kg/h)": r["L_kg_h"],
        "EtOH (%)"    : round(r["x_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["x_etanol"]) * 100, 1),
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "8-PRODUCTO",
        "Equipo"      : "Salida W-420 (condensado)",
        "T (°C)"      : 25,
        "P (atm)"     : P_flash,
        "Flujo (kg/h)": r["V_kg_h"],
        "EtOH (%)"    : round(r["y_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["y_etanol"]) * 100, 1),
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "9-VINAZAS-PRE",
        "Equipo"      : "Salida P-410",
        "T (°C)"      : T_flash,
        "P (atm)"     : 3.0,
        "Flujo (kg/h)": r["L_kg_h"],
        "EtOH (%)"    : round(r["x_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["x_etanol"]) * 100, 1),
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "10-VINAZAS-RE",
        "Equipo"      : "Entrada W-210 (lado caliente)",
        "T (°C)"      : T_flash,
        "P (atm)"     : 3.0,
        "Flujo (kg/h)": r["L_kg_h"],
        "EtOH (%)"    : round(r["x_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["x_etanol"]) * 100, 1),
        "Fase"        : "Líquido"
    },
    {
        "Corriente"   : "11-RESIDUO",
        "Equipo"      : "Salida W-210 (drenaje)",
        "T (°C)"      : round(T_flash * 0.45, 1),
        "P (atm)"     : 1.0,
        "Flujo (kg/h)": r["L_kg_h"],
        "EtOH (%)"    : round(r["x_etanol"] * 100, 1),
        "H₂O (%)"     : round((1 - r["x_etanol"]) * 100, 1),
        "Fase"        : "Líquido"
    },
]

df = pd.DataFrame(corrientes)
st.dataframe(df, use_container_width=True, hide_index=True)

# Descarga CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar tabla en CSV",
    data=csv,
    file_name="balance_materia.csv",
    mime="text/csv"
)

# Nota aclaratoria
st.caption("""
**Supuesto:** Los flujos de PRODUCTO y VINAZAS se calculan con modelo 
termodinámico simplificado (Antoine + NRTL calibrado). 
El caso base de referencia es la simulación DWSIM del reporte técnico.
""")
# ============================================
# Sección 3 — Indicadores económicos
# ============================================
st.divider()
st.subheader("Análisis económico")

# --- Sliders económicos en el sidebar ---
st.sidebar.divider()
st.sidebar.header("Precios de insumos")

precio_vapor    = st.sidebar.slider("Vapor (MXN/ton)",       100, 400, 180, 10)
precio_elec     = st.sidebar.slider("Electricidad (MXN/kWh)", 1.0, 5.0, 2.5, 0.1)
precio_agua     = st.sidebar.slider("Agua (MXN/m³)",          5,  30,  15,  1)
precio_mosto    = st.sidebar.slider("Mosto (MXN/kg)",          4,  20,   8,  1)
precio_etanol   = st.sidebar.slider("Etanol producto (MXN/kg)",10, 50,  25,  1)

# --- Parámetros de proyecto (fijos) ---
inversion       = 15_000_000   # MXN (15 millones)
horas_anio      = 8_000     # h/año
vida_util       = 10        # años
tasa_descuento  = 0.10      # 10% anual

# --- Cálculo de costos operativos ---
# Vapor: Q_calentador en kW → ton/h = kW * 3600 / (2260*1000)
vapor_ton_h     = r["Q_calentador"] * 3.6 / 2260
costo_vapor_h   = vapor_ton_h * precio_vapor

# Electricidad: bombas
costo_elec_h    = r["W_bombas"] * precio_elec

# Agua de enfriamiento: condensador
agua_m3_h       = r["Q_condensador"] * 3.6 / (4.18 * 10 * 1000)
costo_agua_h    = agua_m3_h * precio_agua

# Materia prima: mosto
costo_mosto_h   = 1000 * precio_mosto  # 1000 kg/h de mosto

# Costo total por hora
costo_total_h   = costo_vapor_h + costo_elec_h + costo_agua_h + costo_mosto_h

# Costo por kg de producto
costo_por_kg    = costo_total_h / r["V_kg_h"] if r["V_kg_h"] > 0 else 0

# Precio de venta sugerido (margen 30%)
precio_sugerido = costo_por_kg * 1.30

# --- Ingresos y flujo de caja anual ---
ingreso_anual   = r["V_kg_h"] * horas_anio * precio_etanol
costo_anual     = costo_total_h * horas_anio
flujo_caja      = ingreso_anual - costo_anual

# --- NPV ---
npv = sum([flujo_caja / (1 + tasa_descuento)**t for t in range(1, vida_util + 1)]) - inversion

# --- Payback ---
payback = inversion / flujo_caja if flujo_caja > 0 else float("inf")

# --- ROI ---
roi = (flujo_caja * vida_util - inversion) / inversion * 100

# --- Mostrar KPIs económicos ---
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

col1.metric("Costo de producción",  f"${costo_por_kg:.2f} MXN/kg")
col2.metric("Precio sugerido",      f"${precio_sugerido:.2f} MXN/kg")

# Formateo legible para números grandes
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

# --- Alertas automáticas ---
st.divider()
if precio_sugerido < precio_etanol:
    st.success("✅ El precio sugerido es competitivo en el mercado.")
else:
    st.warning("⚠️ El precio sugerido supera el precio de mercado del etanol.")

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
# Sección 4 — Gráficas de sensibilidad
# ============================================
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.divider()
st.subheader("Análisis de sensibilidad")

# --- Barrido de temperatura ---
T_rango = list(range(75, 99))   # 75°C a 98°C

V_lista, Q_lista, y_lista = [], [], []

for T in T_rango:
    res = calcular_proceso(T_flash=T, P_flash_atm=P_flash, T_feed=T_feed)
    V_lista.append(res["V_kg_h"])
    Q_lista.append(res["Q_calentador"])
    y_lista.append(res["y_etanol"] * 100)

# --- Barrido de presión ---
P_rango = [round(p, 1) for p in np.arange(0.5, 2.1, 0.1)]

V_P_lista, y_P_lista = [], []

for P in P_rango:
    res = calcular_proceso(T_flash=T_flash, P_flash_atm=P, T_feed=T_feed)
    V_P_lista.append(res["V_kg_h"])
    y_P_lista.append(res["y_etanol"] * 100)

# --- Barrido de precio de vapor vs costo ---
vapor_rango = list(range(100, 410, 10))
costo_lista = []

for pv in vapor_rango:
    vapor_th = r["Q_calentador"] * 3.6 / 2260
    costo_h  = (vapor_th * pv) + costo_elec_h + costo_agua_h + costo_mosto_h
    costo_kg = costo_h / r["V_kg_h"] if r["V_kg_h"] > 0 else 0
    costo_lista.append(round(costo_kg, 2))

# --- Barrido precio mosto vs VPN ---
mosto_rango  = list(range(4, 21))
npv_lista    = []

for pm in mosto_rango:
    costo_h_m   = (vapor_ton_h * precio_vapor) + costo_elec_h + costo_agua_h + (1000 * pm)
    flujo_m     = (r["V_kg_h"] * horas_anio * precio_etanol) - (costo_h_m * horas_anio)
    npv_m       = sum([flujo_m / (1 + tasa_descuento)**t for t in range(1, vida_util + 1)]) - inversion
    npv_lista.append(npv_m / 1_000_000)  # en millones

# --- Crear subplots 2x2 ---
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=[
        "T_flash vs Flujo de producto",
        "T_flash vs Pureza de etanol",
        "Precio vapor vs Costo de producción",
        "Precio mosto vs VPN"
    ]
)

# Gráfica 1 — T vs Vapor
fig.add_trace(
    go.Scatter(x=T_rango, y=V_lista, mode="lines+markers",
               line=dict(color="#e74c3c", width=2),
               name="Producto (kg/h)"),
    row=1, col=1
)

# Gráfica 2 — T vs Pureza
fig.add_trace(
    go.Scatter(x=T_rango, y=y_lista, mode="lines+markers",
               line=dict(color="#3498db", width=2),
               name="Etanol en vapor (%)"),
    row=1, col=2
)

# Gráfica 3 — Precio vapor vs Costo
fig.add_trace(
    go.Scatter(x=vapor_rango, y=costo_lista, mode="lines",
               line=dict(color="#2ecc71", width=2),
               name="Costo prod. (MXN/kg)"),
    row=2, col=1
)

# Gráfica 4 — Precio mosto vs VPN
fig.add_trace(
    go.Scatter(x=mosto_rango, y=npv_lista, mode="lines+markers",
               line=dict(color="#9b59b6", width=2),
               name="VPN (M MXN)"),
    row=2, col=2
)

# Línea vertical en el valor actual del slider
fig.add_vline(x=T_flash, line_dash="dash", line_color="gray",
              annotation_text=f"Actual: {T_flash}°C", row=1, col=1)
fig.add_vline(x=T_flash, line_dash="dash", line_color="gray",
              annotation_text=f"Actual: {T_flash}°C", row=1, col=2)
fig.add_vline(x=precio_vapor, line_dash="dash", line_color="gray",
              annotation_text=f"Actual: {precio_vapor}", row=2, col=1)
fig.add_vline(x=precio_mosto, line_dash="dash", line_color="gray",
              annotation_text=f"Actual: {precio_mosto}", row=2, col=2)

# Ejes
fig.update_xaxes(title_text="Temperatura (°C)", row=1, col=1)
fig.update_xaxes(title_text="Temperatura (°C)", row=1, col=2)
fig.update_xaxes(title_text="Precio vapor (MXN/ton)", row=2, col=1)
fig.update_xaxes(title_text="Precio mosto (MXN/kg)", row=2, col=2)

fig.update_yaxes(title_text="kg/h", row=1, col=1)
fig.update_yaxes(title_text="% EtOH", row=1, col=2)
fig.update_yaxes(title_text="MXN/kg", row=2, col=1)
fig.update_yaxes(title_text="Millones MXN", row=2, col=2)

fig.update_layout(
    height=600,
    showlegend=False,
    title_text="Sensibilidad de variables operativas y económicas"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================
# Sección 5 — Comparación de escenarios
# ============================================
st.divider()
st.subheader("Comparación de escenarios")

# Definir los 4 escenarios
escenarios = {
    "🟢 Caso Base"     : {"T": 92,  "P": 1.0, "p_vapor": 180, "p_mosto": 8,  "p_etanol": 25},
    "🔵 Caso Óptimo"   : {"T": 87,  "P": 0.8, "p_vapor": 180, "p_mosto": 8,  "p_etanol": 25},
    "🟡 Caso Económico": {"T": 92,  "P": 1.0, "p_vapor": 120, "p_mosto": 5,  "p_etanol": 30},
    "🔴 Caso Crítico"  : {"T": 92,  "P": 1.5, "p_vapor": 350, "p_mosto": 15, "p_etanol": 15},
}

# Calcular cada escenario
resultados_esc = {}
for nombre, params in escenarios.items():
    res_e = calcular_proceso(
        T_flash=params["T"],
        P_flash_atm=params["P"],
        T_feed=25
    )
    # Calcular economía de ese escenario
    vt  = res_e["Q_calentador"] * 3.6 / 2260
    ch  = (vt * params["p_vapor"]) + (res_e["W_bombas"] * precio_elec) + costo_agua_h + (1000 * params["p_mosto"])
    fc  = (res_e["V_kg_h"] * horas_anio * params["p_etanol"]) - (ch * horas_anio)
    npv_e = sum([fc / (1 + tasa_descuento)**t for t in range(1, vida_util + 1)]) - inversion

    resultados_esc[nombre] = {
        "T (°C)"          : params["T"],
        "P (atm)"         : params["P"],
        "Producto (kg/h)" : res_e["V_kg_h"],
        "EtOH (%)"        : round(res_e["y_etanol"] * 100, 1),
        "Q cal (kW)"      : res_e["Q_calentador"],
        "VPN (M MXN)"     : round(npv_e / 1_000_000, 2),
    }

# Mostrar tabla comparativa
df_esc = pd.DataFrame(resultados_esc).T
st.dataframe(df_esc, use_container_width=True)

# Gráfica de barras comparativa
st.markdown("##### VPN por escenario")
fig_esc = go.Figure()

colores = ["#2ecc71", "#3498db", "#f1c40f", "#e74c3c"]
for i, (nombre, vals) in enumerate(resultados_esc.items()):
    fig_esc.add_trace(go.Bar(
        name=nombre,
        x=[nombre],
        y=[vals["VPN (M MXN)"]],
        marker_color=colores[i],
        text=[f"${vals['VPN (M MXN)']}M"],
        textposition="auto"
    ))

fig_esc.add_hline(y=0, line_dash="dash", line_color="gray",
                  annotation_text="VPN = 0")
fig_esc.update_layout(
    height=350,
    showlegend=False,
    yaxis_title="VPN (Millones MXN)",
    title="Comparación de VPN por escenario"
)
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
    **Diagrama de Bloques** — muestra el flujo global del proceso
    con las secciones 100 a 500 y las corrientes principales.
    """)
    archivo_bloques = st.file_uploader(
        "Sube el diagrama de bloques (PDF o imagen)",
        type=["pdf", "png", "jpg"],
        key="bloques"
    )
    if archivo_bloques:
        if archivo_bloques.type == "application/pdf":
            st.download_button(
                "📥 Descargar Diagrama de Bloques",
                archivo_bloques,
                file_name="diagrama_bloques.pdf"
            )
            st.info("PDF cargado correctamente. Usa el botón para descargarlo.")
        else:
            st.image(archivo_bloques, caption="Diagrama de Bloques", use_container_width=True)
    else:
        st.info("👆 Sube tu diagrama de bloques exportado desde AutoCAD Plant 3D")

with tab2:
    st.markdown("""
    **Diagrama de Flujo de Proceso (PFD)** — muestra equipos reales,
    corrientes numeradas, condiciones de operación y balance de materia.
    """)
    archivo_pfd = st.file_uploader(
        "Sube el PFD (PDF o imagen)",
        type=["pdf", "png", "jpg"],
        key="pfd"
    )
    if archivo_pfd:
        if archivo_pfd.type == "application/pdf":
            st.download_button(
                "📥 Descargar PFD",
                archivo_pfd,
                file_name="PFD.pdf"
            )
            st.info("PDF cargado correctamente. Usa el botón para descargarlo.")
        else:
            st.image(archivo_pfd, caption="PFD", use_container_width=True)
    else:
        st.info("👆 Sube tu PFD exportado desde AutoCAD Plant 3D")

with tab3:
    st.markdown("""
    **Diagrama de Tuberías e Instrumentación (P&ID)** — muestra
    instrumentos, controladores y válvulas de control del proceso.
    Lazos: nivel (200-LC-211), flujo (300-FC-312), temperatura (400-TC-411).
    """)
    archivo_pid = st.file_uploader(
        "Sube el P&ID (PDF o imagen)",
        type=["pdf", "png", "jpg"],
        key="pid"
    )
    if archivo_pid:
        if archivo_pid.type == "application/pdf":
            st.download_button(
                "📥 Descargar P&ID",
                archivo_pid,
                file_name="PID.pdf"
            )
            st.info("PDF cargado correctamente. Usa el botón para descargarlo.")
        else:
            st.image(archivo_pid, caption="P&ID", use_container_width=True)
    else:
        st.info("👆 Sube tu P&ID exportado desde AutoCAD Plant 3D")
# ============================================
# Sección 7 — Tutor con IA (Gemini)
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
    Eres un tutor experto en ingeniería química especializado en procesos de separación.
    Estás ayudando a un estudiante de FIQ BUAP con su proyecto de simulación de procesos.
    El proceso es una Planta de Concentración de Mosto (separación etanol-agua por flash).

    CONDICIONES ACTUALES:
    - Temperatura separador B-410: {T_flash}°C
    - Presión separador B-410: {P_flash} atm
    - Temperatura alimentación: {T_feed}°C
    - Flujo alimentación: 1000 kg/h (10% etanol, 90% agua)

    RESULTADOS ACTUALES:
    - Producto (vapor): {r['V_kg_h']} kg/h
    - Vinazas: {r['L_kg_h']} kg/h
    - Etanol en producto: {round(r['y_etanol']*100,1)}%
    - Q calentador: {r['Q_calentador']} kW
    - VPN: ${npv:,.0f} MXN
    - Payback: {payback:.1f} años

    Responde siempre en español, de forma clara y didáctica.
    Si el estudiante pregunta sobre los valores actuales, usa los datos de arriba.
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
        st.session_state.historial.append({
            "role": "user", "content": pregunta
        })

        try:
            genai.configure(api_key=api_key)

            # Detecta automáticamente el modelo disponible con tu key
            modelos_disponibles = [
                m.name for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]

            if not modelos_disponibles:
                st.error("No se encontraron modelos disponibles para esta API Key.")
            else:
                nombre_modelo = modelos_disponibles[0]
                modelo = genai.GenerativeModel(nombre_modelo)

                prompt_final = contexto_sistema + "\n\nPregunta del estudiante: " + pregunta
                respuesta = modelo.generate_content(prompt_final)

                texto = respuesta.text
                with st.chat_message("assistant"):
                    st.markdown(f"*({nombre_modelo})*\n\n{texto}")
                st.session_state.historial.append({
                    "role": "assistant", "content": texto
                })

        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")

else:
    st.info("👆 Ingresa tu API Key de Gemini para activar el tutor.")
# ============================================
# Sección 8 — Supuestos y documentación
# ============================================
st.divider()
st.subheader("Supuestos y documentación")

tab_s1, tab_s2, tab_s3 = st.tabs([
    "Termodinámicos",
    "Económicos",
    "Archivos del proyecto"
])

with tab_s1:
    st.markdown("""
    ### Supuestos termodinámicos
    - Sistema binario **etanol-agua** (mezcla no ideal)
    - Paquete termodinámico: **NRTL** (Non-Random Two-Liquid)
    - Presiones de vapor calculadas con **ecuación de Antoine**
    - Coeficientes de actividad: **γ_etanol = 2.96**, **γ_agua = 1.11** (calibrados con DWSIM a 92°C)
    - Flash **isentálpico** en válvula V-310 (4 atm → 1 atm)
    - Equilibrio líquido-vapor resuelto con **ecuación de Rachford-Rice**
    - Integración energética en W-210: eficiencia supuesta del 70%
    - Condensador W-420: enfriamiento hasta 25°C
    
    ### Limitaciones del modelo
    - Los coeficientes de actividad se mantienen constantes (no varían con T)
    - El modelo simplificado difiere del DWSIM en flujos absolutos
    - Se usa como herramienta de **análisis de sensibilidad relativa**
    """)

with tab_s2:
    st.markdown(f"""
    ### Supuestos económicos
    | Parámetro | Valor |
    |-----------|-------|
    | Inversión inicial | ${inversion:,.0f} MXN |
    | Vida útil | 10 años |
    | Horas de operación | 8,000 h/año |
    | Tasa de descuento | 10% anual |
    | Precio vapor | ${precio_vapor} MXN/ton |
    | Precio electricidad | ${precio_elec} MXN/kWh |
    | Precio agua | ${precio_agua} MXN/m³ |
    | Precio mosto | ${precio_mosto} MXN/kg |
    | Precio etanol producto | ${precio_etanol} MXN/kg |
    
    ### Notas
    - El VPN se calcula con flujos de caja anuales constantes
    - No se incluye depreciación ni impuestos
    - Los precios son valores de referencia para análisis comparativo
    """)

with tab_s3:
    st.markdown("### Estructura del proyecto")
    st.code("""
planta_mosto/
├── app.py        ← Interfaz Streamlit (este archivo)
├── modelo.py     ← Motor de cálculo termodinámico
├── flash.py      ← Desarrollo paso a paso (Antoine, K-values)
└── requirements.txt
    """, language="bash")

    st.markdown("### Tecnologías utilizadas")
    st.markdown("""
- **Python 3.11** — lenguaje de programación
- **Streamlit** — interfaz web interactiva
- **SciPy** — resolución de Rachford-Rice
- **Plotly** — gráficas interactivas
- **Pandas** — manejo de tablas
- **Gemini API** — tutor con IA
- **DWSIM** — simulador de referencia (NRTL)
    """)

    st.markdown("### Referencia del caso base")
    st.info("""
Simulación realizada en DWSIM por Marlet Salazar Hernández,
FIQ BUAP, Marzo 2026. Reporte: Planta de Concentración de
Mosto con Integración Energética.
    """)