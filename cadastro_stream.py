import streamlit as st
import pandas as pd
from functions_stream import *
import time


def insert_componente(nome, fabricante, tipo, data_aquisicao, estado, preco):
    preco = str(preco)
    preco = preco.replace(',', '.')

    try:
        with connection() as conn:
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


def insert_equipamento(nome, fabricante, tipo, data_aquisicao, estado, preco, lista_componentes):
    preco = str(preco)
    preco = preco.replace(',', '.')

    try:
        with connection() as conn:
            cursor = conn.cursor()
            id = cursor.execute(f"SELECT MAX(ID) FROM EQUIPAMENTOS").fetchone()
            id = id[0]
            if id is None:
                id = '1'
            else:
                id = int(id) + 1
                id = str(id)

            # ============================================ SE FOR DESKTOP ==============================================
            # ============================================ SE FOR DESKTOP ==============================================

            if tipo == 'Desktop':
                id_componente = []
                for index, item in enumerate(lista_componentes):
                    id_consulta = cursor.execute(f"SELECT ID FROM COMPONENTES WHERE NOME = '{item}'").fetchone()
                    if id_consulta is None:
                        id_consulta = (None, )
                    id_componente.append(id_consulta[0])
                cursor.execute(f"INSERT INTO EQUIPAMENTOS (ID, NOME, FABRICANTE, TIPO, DATA_AQUISICAO, ESTADO, PRECO_UNIT, STATUS, GABINETE, FONTE, PLACA_MAE, CPU, RAM, HD, SSD, PLACA_VIDEO) VALUES ('{id}', '{nome}', '{fabricante}', '{tipo}', '{data_aquisicao}', '{estado}', {float(preco)}, 'ATIVO', '{id_componente[0]}', '{id_componente[1]}', '{id_componente[2]}', '{id_componente[3]}', '{id_componente[4]}', '{id_componente[5]}', '{id_componente[6]}', '{id_componente[7]}')")

            # ===================================== SE NAO FOR DESKTOP =================================================
            # ===================================== SE NAO FOR DESKTOP =================================================

            else:
                cursor.execute(f"INSERT INTO EQUIPAMENTOS (ID, NOME, FABRICANTE, TIPO, DATA_AQUISICAO, ESTADO, PRECO_UNIT, STATUS, GABINETE, FONTE, PLACA_MAE, CPU, RAM, HD, SSD, PLACA_VIDEO) VALUES ('{id}', '{nome}', '{fabricante}', '{tipo}', '{data_aquisicao}', '{estado}', {float(preco)}, 'ATIVO', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)")
            cursor.execute(f"INSERT INTO MOV_ESTOQUE (ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA_MOV, QUANTIDADE, SALDO) VALUES ({id}, NULL, '{nome}', DATETIME('now'), 0, 0)")
            conn.commit()
        st.success('Equipamento cadastro com sucesso!')

    except sqlite3.OperationalError as erro:
        st.error(erro)


def insert_fte(fabricante, tipo_componente, tipo_equipamento, estado):
    if fabricante != '':
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO FABRICANTES (NOME) VALUES ('{fabricante}')")
            conn.commit()
            st.success('Inserido com sucesso')
    elif tipo_componente != '':
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO TIPO_COMPONENTE (NOME) VALUES ('{tipo_componente}')")
            conn.commit()
    elif tipo_equipamento != '':
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO TIPO_EQUIPAMENTO (NOME) VALUES ('{tipo_equipamento}')")
            conn.commit()
    elif estado != '':
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO ESTADO (NOME) VALUES ('{estado}')")
            conn.commit()


def insert_manutencao(parametros):
    with connection() as conn:
        cursor = conn.cursor()
        if parametros[2] == '':
            st.error('Digite o ID do Componente/Equipamento')
            for c in range(3):
                time.sleep(1)
            st.rerun()
            exit()
        elif parametros[4] == '':
            st.error('Digite a descrição do problema.')
            for c in range(3):
                time.sleep(1)
            st.rerun()
            exit()
        elif parametros[5] == '':
            st.error('Digite o custo do reparo.')
            for c in range(3):
                time.sleep(1)
            st.rerun()
            exit()
        elif parametros[6] == '':
            st.error('Digite o técnico responsavel.')
            for c in range(3):
                time.sleep(1)
            st.rerun()
            exit()

        if parametros[1] == 'Componente':
            nome = cursor.execute(f"SELECT NOME FROM COMPONENTES WHERE ID = '{parametros[2]}'").fetchone()[0]
            cursor.execute(f"INSERT INTO MANUTENCAO (ID, ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA, DESCRICAO, CUSTO, TEC_RESPONSAVEL, STATUS) VALUES ({parametros[0]}, NULL, {parametros[2]}, '{nome}', '{parametros[3]}', '{parametros[4]}', '{parametros[5]}', '{parametros[6]}', 'ATIVO')")
            conn.commit()
            st.success('Manutenção cadastrada com sucesso!')
            for c in range(3):
                time.sleep(1)
            st.rerun()
        elif parametros[1] == 'Equipamento':
            nome = cursor.execute(f"SELECT NOME FROM EQUIPAMENTOS WHERE ID = '{parametros[2]}'").fetchone()[0]
            cursor.execute(f"INSERT INTO MANUTENCAO (ID, ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA, DESCRICAO, CUSTO, TEC_RESPONSAVEL, STATUS) VALUES ({parametros[0]}, {parametros[2]}, NULL, '{nome}','{parametros[3]}', '{parametros[4]}', '{parametros[5]}', '{parametros[6]}', 'ATIVO')")
            conn.commit()
            st.success('Manutenção cadastrada com sucesso!')
            for c in range(3):
                time.sleep(1)
            st.rerun()


def cadastro_componente():

    # ======================================== CONSULTA PARA OS WIDGETS ================================================
    # ======================================== CONSULTA PARA OS WIDGETS ================================================

    with connection() as conn:
        cursor = conn.cursor()
        fabricantes = cursor.execute('SELECT NOME FROM FABRICANTES').fetchall()
        tipo_componente = cursor.execute('SELECT NOME FROM TIPO_COMPONENTE').fetchall()
        estados = cursor.execute('SELECT NOME FROM ESTADO').fetchall()

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
    tipo = form_componente.selectbox('Tipo', (tipo_comp[0] for tipo_comp in tipo_componente))
    data_aquisicao = form_componente.date_input('Data de Aquisição')
    estado = form_componente.selectbox('Estado', (state[0] for state in estados))
    preco = form_componente.number_input('Preço unitário')
    submit = form_componente.form_submit_button('Cadastrar')

    if submit:
        insert_componente(nome, fabricante, tipo, data_aquisicao, estado, preco)
        for c in range(3):
            time.sleep(c)
        st.rerun()


def cadastro_equipamento():

    # ======================================== CONSULTA PARA OS WIDGETS ================================================
    # ======================================== CONSULTA PARA OS WIDGETS ================================================

    with connection() as conn:
        cursor = conn.cursor()
        fabricantes = cursor.execute('SELECT NOME FROM FABRICANTES').fetchall()
        tipo_equipamento = cursor.execute('SELECT NOME FROM TIPO_EQUIPAMENTO').fetchall()
        estados = cursor.execute('SELECT NOME FROM ESTADO').fetchall()

        gabinetes = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Gabinete' AND STATUS = 'ATIVO'").fetchall()
        gabinetes.insert(0, ('None',))
        fontes = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Fonte' AND STATUS='ATIVO'").fetchall()
        fontes.insert(0, ('None',))
        placas_mae = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Placa-mãe' AND STATUS='ATIVO'").fetchall()
        placas_mae.insert(0, ('None',))
        cpus = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Processador' AND STATUS='ATIVO'").fetchall()
        cpus.insert(0, ('None',))
        memorias = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Memória RAM' AND STATUS='ATIVO'").fetchall()
        memorias.insert(0, ('None',))
        hds = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'HD' AND STATUS='ATIVO'").fetchall()
        hds.insert(0, ('None',))
        ssds = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'SSD' AND STATUS='ATIVO'").fetchall()
        ssds.insert(0, ('None',))
        placas_video = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Placa de vídeo' AND STATUS='ATIVO'").fetchall()
        placas_video.insert(0, ('None',))

        id = cursor.execute(f"SELECT MAX(ID) FROM EQUIPAMENTOS").fetchone()
        id = id[0]
        if id is None:
            id = '1'
        else:
            id = int(id) + 1
            id = str(id)

    # ================================================= FORMULÁRIO =====================================================
    # ================================================= FORMULÁRIO =====================================================

    id_input = st.text_input('ID', value=id, disabled=True)
    nome = st.text_input('Nome')
    fabricante = st.selectbox('Fabricante', (fabricante[0] for fabricante in fabricantes))
    tipo = st.selectbox('Tipo', (tipo_equip[0] for tipo_equip in tipo_equipamento))
    if tipo == 'Desktop':
        gabinete_desktop = st.selectbox('Gabinete do Desktop', (gabinete[0] for gabinete in gabinetes))
        fonte_desktop = st.selectbox('Fonte do Desktop', (fonte[0] for fonte in fontes))
        placas_mae_desktop = st.selectbox('Placa-mãe do Desktop', (placa_mae[0] for placa_mae in placas_mae))
        cpu_desktop = st.selectbox('Processador do Desktop', (cpu[0] for cpu in cpus))
        memoria_desktop = st.selectbox('Memória RAM do Desktop', (memoria[0] for memoria in memorias))
        hd_desktop = st.selectbox('HD do Desktop', (hd[0] for hd in hds))
        ssd_desktop = st.selectbox('SSD do Desktop', (ssd[0] for ssd in ssds))
        placa_video_desktop = st.selectbox('Placa de Vídeo do Desktop', (placa_video[0] for placa_video in placas_video))

    data_aquisicao = st.date_input('Data de Aquisição')
    estado = st.selectbox('Estado', (state[0] for state in estados))
    preco = st.number_input('Preço unitário')
    submit = st.button('Cadastrar')

    if submit:
        if tipo == 'Desktop':
            lista_componentes = [gabinete_desktop, fonte_desktop, placas_mae_desktop, cpu_desktop, memoria_desktop, hd_desktop, ssd_desktop, placa_video_desktop]
        else:
            lista_componentes = []

        insert_equipamento(nome, fabricante, tipo, data_aquisicao, estado, preco, lista_componentes)
        for c in range(3):
            time.sleep(c)
        st.rerun()


def cadastro_manutencao():
    # ======================================== CONSULTA PARA OS WIDGETS ================================================
    # ======================================== CONSULTA PARA OS WIDGETS ================================================

    with connection() as conn:
        cursor = conn.cursor()
        fabricantes = cursor.execute('SELECT NOME FROM FABRICANTES').fetchall()
        tipo_equipamento = cursor.execute('SELECT NOME FROM TIPO_EQUIPAMENTO').fetchall()
        estados = cursor.execute('SELECT NOME FROM ESTADO').fetchall()

        id = cursor.execute(f"SELECT MAX(ID) FROM MANUTENCAO").fetchone()
        id = id[0]
        if id is None:
            id = '1'
        else:
            id = int(id) + 1
            id = str(id)

    form_manutencao = st.form('Formulário de Manutenção', clear_on_submit=True)
    id_input = form_manutencao.text_input('ID', value=id, disabled=True)
    tipo = form_manutencao.selectbox('Tipo', ['Componente', 'Equipamento'])
    id_coe = form_manutencao.text_input('ID do Componente ou Equipamento')
    custo_coe = form_manutencao.text_input('Custo do Reparo')
    tecnico_responsavel = form_manutencao.text_input('Técnico Responsável')
    descricao = form_manutencao.text_area('Descrição do problema')
    data_entrada = form_manutencao.date_input('Data de entrada')
    cadastrar = form_manutencao.form_submit_button('Cadastrar')
    if cadastrar:
        parametros = [id_input, tipo, id_coe, data_entrada, descricao, custo_coe, tecnico_responsavel]
        insert_manutencao(parametros)

    # ================= DATAFRAME PARA CONSULTAR ID COMPONENTE OU EQUIPAMENTO PARA CADASTRAR MANUTENÇÃO ================

    df_componentes = pd.read_sql_query(f"SELECT COMPONENTES.ID, COMPONENTES.NOME, COMPONENTES.FABRICANTE, COMPONENTES.TIPO, UltimaMov.SALDO AS QUANTIDADE, COMPONENTES.DATA_AQUISICAO, COMPONENTES.ESTADO, COMPONENTES.PRECO_UNIT FROM COMPONENTES JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_COMPONENTES = COMPONENTES.ID JOIN (SELECT ID_COMPONENTES, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_COMPONENTES) AS UltimaMov ON MOV_ESTOQUE.ID_COMPONENTES = UltimaMov.ID_COMPONENTES AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY COMPONENTES.ID ASC;", conn)
    st.subheader('Componentes')
    st.dataframe(df_componentes)
    df_equipamentos = pd.read_sql_query(f"SELECT EQUIPAMENTOS.ID, EQUIPAMENTOS.NOME, EQUIPAMENTOS.FABRICANTE, EQUIPAMENTOS.TIPO, UltimaMov.SALDO AS QUANTIDADE, EQUIPAMENTOS.DATA_AQUISICAO, EQUIPAMENTOS.ESTADO, EQUIPAMENTOS.PRECO_UNIT, (SELECT NOME FROM COMPONENTES WHERE ID = Equipamentos.GABINETE) as GABINETE , (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.FONTE) as FONTE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_MAE) as PLACA_MAE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.CPU) AS PROCESSADOR, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.RAM) AS RAM, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.HD) AS HD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.SSD) AS SSD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_VIDEO) AS PLACA_VIDEO FROM EQUIPAMENTOS JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_EQUIPAMENTOS = EQUIPAMENTOS.ID JOIN (SELECT ID_EQUIPAMENTOS, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_EQUIPAMENTOS) AS UltimaMov ON MOV_ESTOQUE.ID_EQUIPAMENTOS = UltimaMov.ID_EQUIPAMENTOS AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY EQUIPAMENTOS.ID ASC;", conn)
    st.subheader('Equipamentos')
    st.dataframe(df_equipamentos)


def cadastro_fte():
    form_fte = st.form('Cadastro FTE', clear_on_submit=True)
    form_fte.subheader('Insira somente o que deseja cadastrar')
    fabricante = form_fte.text_input('Fabricante')
    tipo_componente = form_fte.text_input('Tipos de Componente')
    tipo_equipamento = form_fte.text_input('Tipos de Equipamento')
    estado = form_fte.text_input('Estado')
    form_fte_submit = form_fte.form_submit_button()
    if form_fte_submit:
        insert_fte(fabricante, tipo_componente, tipo_equipamento, estado)
        for c in range(3):
            time.sleep(c)
        st.rerun()


def cadastro():
    st.title('Módulo de Cadastro')
    modulos_cadastro = st.selectbox('Selecione o cadastro', ['Componente', 'Equipamento', 'Manutenção', 'Fabricante, Tipo e Estado'])

    if modulos_cadastro == 'Componente':
        cadastro_componente()
    if modulos_cadastro == 'Equipamento':
        cadastro_equipamento()
    if modulos_cadastro == 'Manutenção':
        cadastro_manutencao()
    if modulos_cadastro == 'Fabricante, Tipo e Estado':
        cadastro_fte()
