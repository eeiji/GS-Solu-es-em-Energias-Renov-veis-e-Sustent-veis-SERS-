"""Calcula os indicadores do projeto de gestão energética escolar."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
dados = pd.read_csv(ROOT / "data" / "consumo_escola.csv")

# Premissas do cenário-modelo (ajustáveis conforme dados reais da escola).
POTENCIA_SOLAR_KWP = 8
PRODUTIVIDADE_KWH_KWP_ANO = 1362
TARIFA_R_KWH = 0.78938
FATOR_CO2_T_MWH = 0.0461
CUSTO_LED = 6670.90
CUSTO_SOLAR = 19440.00

atual = dados["consumo_atual_kwh_ano"].sum()
eficiente = dados["consumo_apos_eficiencia_kwh_ano"].sum()
economia = atual - eficiente
geracao_solar = POTENCIA_SOLAR_KWP * PRODUTIVIDADE_KWH_KWP_ANO
saldo_rede = max(0, eficiente - geracao_solar)

indicadores = pd.DataFrame([
    ["Consumo atual", atual, "kWh/ano"],
    ["Consumo após eficiência", eficiente, "kWh/ano"],
    ["Economia com eficiência", economia, "kWh/ano"],
    ["Economia percentual", economia / atual * 100, "%"],
    ["Geração fotovoltaica", geracao_solar, "kWh/ano"],
    ["Participação solar potencial", geracao_solar / eficiente * 100, "%"],
    ["Saldo energético anual teórico da rede", saldo_rede, "kWh/ano"],
    ["Custo variável atual estimado", atual * TARIFA_R_KWH, "R$/ano"],
    ["Custo variável após eficiência", eficiente * TARIFA_R_KWH, "R$/ano"],
    ["Custo variável após saldo solar teórico", saldo_rede * TARIFA_R_KWH, "R$/ano"],
    ["Investimento LED + solar", CUSTO_LED + CUSTO_SOLAR, "R$"],
    ["Emissões evitadas estimadas (eficiência + solar)", (economia + geracao_solar) / 1000 * FATOR_CO2_T_MWH, "tCO2/ano"],
], columns=["indicador", "valor", "unidade"])

saida = ROOT / "outputs"
saida.mkdir(exist_ok=True)
indicadores.to_csv(saida / "indicadores_calculados.csv", index=False)

# Gráfico 1: consumo estimado por equipamento.
fig, ax = plt.subplots(figsize=(10, 5.5))
dados.sort_values("consumo_atual_kwh_ano").plot.barh(
    x="equipamento", y="consumo_atual_kwh_ano", ax=ax, legend=False,
    color="#287D8E")
ax.set_title("Consumo anual estimado por equipamento")
ax.set_xlabel("Energia (kWh/ano)")
ax.set_ylabel("Equipamento")
ax.grid(axis="x", alpha=.25)
fig.tight_layout()
fig.savefig(saida / "consumo_por_equipamento.png", dpi=180)
plt.close(fig)

# Gráfico 2: cenários energéticos anuais.
cenarios = pd.Series({
    "Consumo atual": atual,
    "Após eficiência": eficiente,
    "Geração solar": geracao_solar,
    "Saldo teórico da rede": saldo_rede,
})
fig, ax = plt.subplots(figsize=(9, 5))
cenarios.plot.bar(ax=ax, color=["#466A7A", "#287D8E", "#E0A43B", "#5C9A78"])
ax.set_title("Comparação anual de energia")
ax.set_ylabel("Energia (kWh/ano)")
ax.set_xlabel("Cenário")
ax.tick_params(axis="x", rotation=15)
ax.grid(axis="y", alpha=.25)
fig.tight_layout()
fig.savefig(saida / "comparacao_cenarios.png", dpi=180)
plt.close(fig)

print(indicadores.to_string(index=False, formatters={"valor": lambda x: f"{x:,.2f}"}))
print(f"\nArquivos gerados em: {saida}")
