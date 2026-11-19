import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ------------------------------------------------------------------
# Configuração da página
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Agrometeorologia — Londrina (PR)",
    page_icon="🌾",
    layout="wide",
)

# ------------------------------------------------------------------
# Carregar dados
# ------------------------------------------------------------------
@st.cache_data
def carregar_resumo():
    df = pd.read_csv("londrina_resumo_agricola.csv", index_col=0)
    df.index.name = "mes"
    df = df.reset_index()
    nomes_meses = ["Jan","Fev","Mar","Abr","Mai","Jun",
                   "Jul","Ago","Set","Out","Nov","Dez"]
    df["mes_nome"] = df["mes"].apply(lambda m: nomes_meses[int(m)-1])
    return df

@st.cache_data
def carregar_diario():
    df = pd.read_csv("londrina_diario_tratado.csv", parse_dates=["DATA"])
    df["ano"] = df["DATA"].dt.year
    df["mes"] = df["DATA"].dt.month
    return df

resumo = carregar_resumo()
diario = carregar_diario()

# ------------------------------------------------------------------
# Cabeçalho
# ------------------------------------------------------------------
st.title("🌾 Agrometeorologia de Londrina (PR)")
st.caption("Base: INMET estação 83766 · Período 1991–2020 · Dados tratados pelos autores")
st.markdown("---")

# ------------------------------------------------------------------
# KPIs no topo
# ------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Chuva anual média", f"{resumo['CHUVA_mm'].sum():.0f} mm")
col2.metric("Mês mais chuvoso",
            resumo.loc[resumo['CHUVA_mm'].idxmax(), 'mes_nome'],
            f"{resumo['CHUVA_mm'].max():.0f} mm")
col3.metric("Mês mais seco",
            resumo.loc[resumo['CHUVA_mm'].idxmin(), 'mes_nome'],
            f"{resumo['CHUVA_mm'].min():.0f} mm")
col4.metric("ITU médio anual", f"{resumo['ITU_med'].mean():.1f}")

st.markdown("---")

# ------------------------------------------------------------------
# Aba 1 — Clima mensal
# ------------------------------------------------------------------
aba1, aba2, aba3, aba4 = st.tabs(
    ["📊 Clima mensal", "⚠️ Riscos agrícolas", "🐄 Conforto animal", "📅 Calendário por cultura"]
)

with aba1:
    st.subheader("Chuva e temperatura por mês")

    fig = go.Figure()
    fig.add_bar(x=resumo["mes_nome"], y=resumo["CHUVA_mm"],
                name="Chuva (mm)", marker_color="steelblue", yaxis="y1")
    fig.add_scatter(x=resumo["mes_nome"], y=resumo["TMED_med"],
                    name="Temperatura média (°C)", mode="lines+markers",
                    line=dict(color="darkred", width=3), yaxis="y2")
    fig.update_layout(
        yaxis=dict(title="Chuva (mm)"),
        yaxis2=dict(title="Temperatura (°C)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Frequência de dias com chuva > 1 mm (%)**")
    fig2 = px.bar(resumo, x="mes_nome", y="DIAS_CHUVA_pct",
                  color="DIAS_CHUVA_pct", color_continuous_scale="Blues",
                  labels={"DIAS_CHUVA_pct": "% dias com chuva", "mes_nome": "Mês"})
    fig2.update_layout(height=300, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

with aba2:
    st.subheader("Riscos climáticos por mês")

    risco = resumo.copy()
    risco["risco_seca"] = (100 - risco["DIAS_CHUVA_pct"]).round(1)
    risco["risco_geada"] = risco["risco_geada_%"].round(1)

    fig = go.Figure()
    fig.add_bar(x=risco["mes_nome"], y=risco["risco_seca"],
                name="Risco de seca (% dias sem chuva)", marker_color="saddlebrown")
    fig.add_bar(x=risco["mes_nome"], y=risco["risco_geada"],
                name="Risco de geada (TMIN ≤ 3 °C)", marker_color="lightblue")
    fig.update_layout(barmode="group", height=400,
                      yaxis_title="%", xaxis_title="Mês")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🚨 Semáforo de risco por mês")
    def semaforo(row):
        if row["risco_geada"] >= 15: return "🔴 Alto (geada)"
        if row["risco_seca"] >= 70: return "🟠 Alto (seca)"
        if row["risco_seca"] >= 50: return "🟡 Moderado"
        return "🟢 Baixo"
    risco["semaforo"] = risco.apply(semaforo, axis=1)
    st.dataframe(risco[["mes_nome","risco_seca","risco_geada","semaforo"]]
                 .rename(columns={"mes_nome":"Mês","risco_seca":"Seca (%)",
                                  "risco_geada":"Geada (%)","semaforo":"Classificação"}),
                 use_container_width=True, hide_index=True)

with aba3:
    st.subheader("Índice de Temperatura e Umidade (ITU) — bovinos")

    def cor_itu(v):
        if v <= 74:  return "green"
        if v <= 79:  return "gold"
        if v <= 84:  return "orange"
        return "red"

    fig = go.Figure()
    fig.add_bar(x=resumo["mes_nome"], y=resumo["ITU_med"],
                marker_color=[cor_itu(v) for v in resumo["ITU_med"]],
                text=resumo["ITU_classe"], textposition="outside")
    fig.add_hline(y=74, line_dash="dash", line_color="gold",
                  annotation_text="Alerta (74)")
    fig.add_hline(y=79, line_dash="dash", line_color="orange",
                  annotation_text="Perigo (79)")
    fig.add_hline(y=84, line_dash="dash", line_color="red",
                  annotation_text="Emergência (84)")
    fig.update_layout(height=450, yaxis_title="ITU médio", xaxis_title="Mês",
                      yaxis_range=[60, 90])
    st.plotly_chart(fig, use_container_width=True)

    st.info("ITU > 79 indica perigo de estresse térmico para bovinos. "
            "Em Londrina isso ocorre principalmente de novembro a abril.")

with aba4:
    st.subheader("Calendário agrícola de Londrina")

    calendario = pd.DataFrame({
        "Cultura":       ["Soja",      "Milho 1ª", "Milho safrinha", "Trigo"],
        "Plantio":       ["Out–Dez",   "Out–Dez",  "Fev–Mar",        "Abr–Mai"],
        
