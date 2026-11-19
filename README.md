CIÊNCIA DA COMPUTAÇÃO — TURMA 1CCPR

`Integrantes:`
`Leandro Eiji Hashimoto - RM 576404`
`Nicolas Gomes Alba Aparicio - RM576175`

# Gestão Inteligente de Energia em Escolas Públicas

Neighborhood Action Dashboard - Soluções em Energias Renováveis e Sustentáveis (Ciência da Computação).

## Conteúdo

- `documentacao/texto_original_colado.txt`: cópia integral do texto fornecido na conversa.
- `documentacao/Projeto_Gestao_Inteligente_Energia_Escolas_Publicas.md`: versão organizada e editável da proposta.
- `documentacao/Projeto_Gestao_Inteligente_Energia_Escolas_Publicas.docx`: relatório editável.
- `documentacao/Projeto_Gestao_Inteligente_Energia_Escolas_Publicas.pdf`: relatório em PDF.
- `data/consumo_escola.csv`: dados estimados por categoria de equipamento.
- `src/calculo_energetico.py`: script para calcular indicadores e gerar gráficos.
- `dashboard/app.py`: dashboard demonstrativo em Streamlit.
- `docs/diagrama_arquitetura.png`: diagrama conceitual da solução.
- `docs/referencias.md`: lista de fontes citadas no material.
- `outputs/`: indicadores calculados e gráficos produzidos pelo script.
- `requirements.txt`: bibliotecas necessárias.

## Como executar os cálculos

A partir da pasta raiz do pacote:

```bash
pip install -r requirements.txt
python src/calculo_energetico.py
```

O script salva `indicadores_calculados.csv`, `consumo_por_equipamento.png` e `comparacao_cenarios.png` na pasta `outputs/`.

## Como executar o dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

O dashboard contém controles para alterar potência fotovoltaica, produtividade solar, tarifa e fator de emissão.

## Premissas e limites

- O cenário representa uma escola-modelo hipotética em São Paulo, com 20 salas e cerca de 500 estudantes.
- Os consumos por equipamento, tempos de uso, reduções, custos e indicadores são estimativas acadêmicas, não medições reais de uma escola.
- A produtividade solar de 1.362 kWh/kWp/ano é premissa de referência; deve ser recalculada para o telhado real.
- O saldo anual entre demanda e geração solar é simplificado. Não representa cálculo definitivo de fatura, pois geração e consumo podem ocorrer em horários diferentes e as regras de compensação têm componentes específicas.
- O sistema fotovoltaico proposto é on-grid, sem bateria, e não fornece energia durante falta da rede.
- O payback apresentado é simples e preliminar, sem todos os custos, tributos, manutenção, financiamento e regras de compensação.
- Os fatores tarifários, custos e fatores de emissão devem ser conferidos e atualizados antes de uso decisório.

## Observação sobre os números

A tabela inicial exibe valores arredondados por equipamento. Para reconciliar o total informado de 11.939,15 kWh/ano após eficiência, o CSV utiliza precisão decimal em alguns itens (por exemplo, laboratório, computadores administrativos e bomba). Os valores por equipamento continuam coerentes com os valores inteiros arredondados apresentados no texto.
