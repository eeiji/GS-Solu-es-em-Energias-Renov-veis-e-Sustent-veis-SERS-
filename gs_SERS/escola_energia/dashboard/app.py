"""Dashboard demonstrativo. Todos os valores iniciais são premissas estimadas."""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
dados = pd.read_csv(ROOT / "data" / "consumo_escola.csv")

st.set_page_config(page_title="Gestão Energética Escolar", page_icon="☀️", layout="wide")
st.title("Neighborhood Action Dashboard | Gestão de Energia Escolar")
st.caption("Cenário acadêmico estimado — substitua as premissas por dados reais antes de tomar decisões.")

with st.sidebar:
    st.header("Premissas editáveis")
    solar_kwp = st.slider("Potência fotovoltaica (kWp)", 0, 20, 8)
    produtividade = st.number_input("Produtividade solar (kWh/kWp/ano)", 800, 1800, 1362, 10)
    tarifa = st.number_input("Tarifa de referência (R$/kWh)", min_value=0.0, value=0.78938, step=0.01, format="%.5f")
    fator_co2 = st.number_input("Fator de emissão (tCO₂/MWh)", min_value=0.0, value=0.0461, step=0.001, format="%.4f")

atual = float(dados["consumo_atual_kwh_ano"].sum())
eficiente = float(dados["consumo_apos_eficiencia_kwh_ano"].sum())
economia = atual - eficiente
geracao = solar_kwp * produtividade
saldo_rede = max(0.0, eficiente - geracao)
participacao = min(100.0, geracao / eficiente * 100) if eficiente else 0
emissoes = (economia + min(geracao, eficiente)) / 1000 * fator_co2

c1, c2, c3, c4 = st.columns(4)
c1.metric("Consumo atual", f"{atual:,.0f} kWh/ano")
c2.metric("Após eficiência", f"{eficiente:,.0f} kWh/ano", f"-{economia/atual*100:.1f}%")
c3.metric("Geração solar estimada", f"{geracao:,.0f} kWh/ano")
c4.metric("Participação solar potencial", f"{participacao:.1f}%")

st.subheader("Consumo anual por equipamento")
fig1 = px.bar(dados, x="equipamento", y="consumo_atual_kwh_ano", color="consumo_atual_kwh_ano",
              labels={"equipamento":"Equipamento", "consumo_atual_kwh_ano":"Consumo (kWh/ano)"})
fig1.update_layout(showlegend=False, xaxis_tickangle=-25)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Comparação dos cenários")
comparacao = pd.DataFrame({"Cenário": ["Atual", "Após eficiência", "Geração solar", "Saldo anual teórico da rede"],
                           "Energia (kWh/ano)": [atual, eficiente, geracao, saldo_rede]})
fig2 = px.bar(comparacao, x="Cenário", y="Energia (kWh/ano)", color="Cenário")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Indicadores financeiros e ambientais")
f1, f2, f3 = st.columns(3)
f1.metric("Custo variável atual estimado", f"R$ {atual*tarifa:,.2f}/ano")
f2.metric("Custo pós-eficiência estimado", f"R$ {eficiente*tarifa:,.2f}/ano")
f3.metric("Saldo de energia da rede (teórico)", f"{saldo_rede:,.0f} kWh/ano")
st.metric("Emissões operacionais potencialmente evitadas", f"{emissoes:.3f} tCO₂/ano")

st.info("O saldo anual entre consumo e geração é uma simplificação. A compensação financeira real depende do perfil horário, das regras de compensação, da tarifa aplicável e de encargos não compensáveis. O sistema on-grid sem bateria não fornece energia durante interrupções da rede.")
st.caption("Fonte dos dados: cenário-modelo documentado em documentacao/Projeto_Gestao_Inteligente_Energia_Escolas_Publicas.md. Os dados não são medições de uma escola real.")
