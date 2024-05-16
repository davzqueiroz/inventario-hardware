import streamlit as st
import pandas as pd
import sqlite3


def connection(bank_rad):
    conn = sqlite3.connect(bank_rad)
    return conn


def usuarios():
    st.title('Gerenciador de Usuários')
    with connection('bank_rad') as conn:
        df = pd.read_sql_query("SELECT * FROM USUARIOS_STREAMLIT", conn)
        st.dataframe(df)
