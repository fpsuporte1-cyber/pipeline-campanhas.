import pandas as pd
import sqlite3

# Extract
df = pd.read_csv("campanhas_bruto.csv")

# Transform
df = df.drop_duplicates()
df = df[df["orcamento"].notna()]
df = df.sort_values("orcamento", ascending=False)
df["custo_por_conversao"] = df["orcamento"] / df["conversoes"]

# Load
conexao = sqlite3.connect("meu_banco.db")
df.to_sql("campanhas", conexao, if_exists="replace", index=False)
