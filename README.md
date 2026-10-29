# Pipeline de Campanhas

## O que é
Projeto que pega um CSV de campanhas de marketing com dados repetidos e
com orçamento e conversões faltando, e transforma tudo em dados limpos,
estruturados e salvos num banco de dados (meu_banco.db).

## Como funciona
1. Extract: lê o CSV de campanhas (campanhas_bruto.csv)
2. Transform: remove duplicatas, tira campanhas sem orçamento, ordena
   pelo orçamento e calcula o custo por conversão
3. Load: salva os dados limpos no banco SQLite

## Tecnologias
Python, pandas, SQL e Airflow (para agendar a execução diária)

## Como rodar
1. Instale o pandas: pip install pandas
2. Deixe o arquivo campanhas_bruto.csv na mesma pasta do etl.py
3. Rode: python etl.py
4. Os dados limpos ficam salvos no arquivo meu_banco.db
