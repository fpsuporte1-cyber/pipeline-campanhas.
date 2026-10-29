import pandas as pd
import sqlite3
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def extrair(**kwargs):
    df = pd.read_csv("campanhas_bruto.csv")
    kwargs["ti"].xcom_push(key="dados_brutos", value=df.to_json())


def transformar(**kwargs):
    df = pd.read_json(kwargs["ti"].xcom_pull(key="dados_brutos", task_ids="extract"))
    df = df.drop_duplicates()
    df = df[df["orcamento"].notna()]
    df = df.sort_values("orcamento", ascending=False)
    df["custo_por_conversao"] = df["orcamento"] / df["conversoes"]
    kwargs["ti"].xcom_push(key="dados_limpos", value=df.to_json())


def carregar(**kwargs):
    df = pd.read_json(kwargs["ti"].xcom_pull(key="dados_limpos", task_ids="transform"))
    conexao = sqlite3.connect("meu_banco.db")
    df.to_sql("campanhas", conexao, if_exists="replace", index=False)


with DAG("pipeline_campanhas", start_date=datetime(2026, 1, 1), schedule="@daily") as dag:
    tarefa_extrair = PythonOperator(task_id="extract", python_callable=extrair)
    tarefa_transformar = PythonOperator(task_id="transform", python_callable=transformar)
    tarefa_carregar = PythonOperator(task_id="load", python_callable=carregar)

    tarefa_extrair >> tarefa_transformar >> tarefa_carregar
