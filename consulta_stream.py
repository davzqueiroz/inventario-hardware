import streamlit as st
import pandas as pd
import sqlite3


def connection(bank_rad):
    conn = sqlite3.connect(bank_rad)
    return conn


def consulta():
    st.title('Módulo de Consulta')
    modulos_consulta = st.selectbox('Selecione a consulta', ['Componentes', 'Equipamentos', 'Manutenção', 'Fabricantes', 'Movimentação de Estoque'])

    if modulos_consulta == 'Componentes':
        with connection('bank_rad') as conn:
            df = pd.read_sql_query(f"SELECT COMPONENTES.ID, COMPONENTES.NOME, COMPONENTES.FABRICANTE, COMPONENTES.TIPO, UltimaMov.SALDO AS QUANTIDADE, COMPONENTES.DATA_AQUISICAO, COMPONENTES.ESTADO, COMPONENTES.PRECO_UNIT FROM COMPONENTES JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_COMPONENTES = COMPONENTES.ID JOIN (SELECT ID_COMPONENTES, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_COMPONENTES) AS UltimaMov ON MOV_ESTOQUE.ID_COMPONENTES = UltimaMov.ID_COMPONENTES AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY COMPONENTES.ID ASC;", conn)
            st.dataframe(df)

    elif modulos_consulta == 'Equipamentos':
        with connection('bank_rad') as conn:
            df = pd.read_sql_query(f"SELECT EQUIPAMENTOS.ID, EQUIPAMENTOS.NOME, EQUIPAMENTOS.FABRICANTE, EQUIPAMENTOS.TIPO, UltimaMov.SALDO AS QUANTIDADE, EQUIPAMENTOS.DATA_AQUISICAO, EQUIPAMENTOS.ESTADO, EQUIPAMENTOS.PRECO_UNIT FROM EQUIPAMENTOS JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_EQUIPAMENTOS = EQUIPAMENTOS.ID JOIN (SELECT ID_EQUIPAMENTOS, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_EQUIPAMENTOS) AS UltimaMov ON MOV_ESTOQUE.ID_EQUIPAMENTOS = UltimaMov.ID_EQUIPAMENTOS AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY EQUIPAMENTOS.ID ASC;", conn)
            st.dataframe(df)

    elif modulos_consulta == 'Manutenção':
        with connection('bank_rad') as conn:
            df = pd.read_sql_query('SELECT * FROM MANUTENCAO', conn)
            st.dataframe(df)

    elif modulos_consulta == 'Fabricantes':
        with connection('bank_rad') as conn:
            df = pd.read_sql_query('SELECT * FROM FABRICANTES', conn)
            st.table(df)

    elif modulos_consulta == 'Movimentação de Estoque':
        with connection('bank_rad') as conn:
            df = pd.read_sql_query('SELECT * FROM MOV_ESTOQUE', conn)
            st.dataframe(df)
