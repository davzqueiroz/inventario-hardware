import streamlit as st
import pandas as pd
import sqlite3
from functions_stream import *


def insert_componente(nome, fabricante, tipo, data_aquisicao, estado, preco):
    preco = str(preco)
    preco = preco.replace(',', '.')

    try:
        with connection('bank_rad') as conn:
            cursor = conn.cursor()
            id = cursor.execute(f"SELECT MAX(ID) FROM COMPONENTES").fetchone()
            id = id[0]
            if id is None:
                id = '1'
            else:
                id = int(id) + 1
                id = str(id)

            cursor.execute(f"INSERT INTO COMPONENTES (ID, NOME, FABRICANTE, TIPO, DATA_AQUISICAO, ESTADO, PRECO_UNIT, STATUS) VALUES ('{id}', '{nome}', '{fabricante}', '{tipo}', '{data_aquisicao}', '{estado}', {float(preco)}, 'ATIVO')")
            cursor.execute(f"INSERT INTO MOV_ESTOQUE (ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA_MOV, QUANTIDADE, SALDO) VALUES (NULL, {id}, '{nome}', DATETIME('now'), 0, 0)")
            conn.commit()
        st.success('Componente cadastro com sucesso!')

    except sqlite3.OperationalError as erro:
        st.error(erro)


def cadastro_componente():

    # ======================================== CONSULTA PARA OS WIDGETS ================================================
    # ======================================== CONSULTA PARA OS WIDGETS ================================================

    with connection('bank_rad') as conn:
        cursor = conn.cursor()
        fabricantes = cursor.execute('SELECT NOME FROM FABRICANTES').fetchall()

        id = cursor.execute(f"SELECT MAX(ID) FROM COMPONENTES").fetchone()
        id = id[0]
        if id is None:
            id = '1'
        else:
            id = int(id) + 1
            id = str(id)

    # ================================================= FORMULÁRIO =====================================================
    # ================================================= FORMULÁRIO =====================================================

    form_componente = st.form('Cadastro de Componente', clear_on_submit=True)
    id_input = form_componente.text_input('ID', value=id, disabled=True)
    nome = form_componente.text_input('Nome')
    fabricante = form_componente.selectbox('Fabricante', (fabricante[0] for fabricante in fabricantes))
    tipo = form_componente.selectbox('Tipo', ['Gabinete', 'Fonte', 'Placa-mãe', 'Processador', 'Memória RAM', 'HD', 'SSD', 'Placa de vídeo'])
    data_aquisicao = form_componente.date_input('Data de Aquisição')
    estado = form_componente.selectbox('Estado', ['Funcionando', 'Não funciona', 'Não testado'])
    preco = form_componente.number_input('Preço unitário')
    submit = form_componente.form_submit_button('Cadastrar')

    if submit:
        insert_componente(nome, fabricante, tipo, data_aquisicao, estado, preco)


def cadastro():
    st.title('Módulo de Cadastro')
    modulos_cadastro = st.selectbox('Selecione o cadastro', ['Componente', 'Equipamento', 'Manutenção', 'Fabricante'])

    if modulos_cadastro == 'Componente':
        cadastro_componente()

