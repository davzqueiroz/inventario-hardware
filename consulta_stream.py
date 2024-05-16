import streamlit as st
import pandas as pd
import sqlite3
import datetime

from functions_stream import *


def consulta_componentes(parametros, considerar_data, cons_or_edit, df, inativar):
    df = df.copy()
    # ============================================ MODO DE CONSULTA ====================================================
    # ============================================ MODO DE CONSULTA ====================================================
    if cons_or_edit == 'Consulta':
        consulta = f"SELECT COMPONENTES.ID, COMPONENTES.NOME, COMPONENTES.FABRICANTE, COMPONENTES.TIPO, UltimaMov.SALDO AS QUANTIDADE, COMPONENTES.DATA_AQUISICAO, COMPONENTES.ESTADO, COMPONENTES.PRECO_UNIT FROM COMPONENTES JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_COMPONENTES = COMPONENTES.ID JOIN (SELECT ID_COMPONENTES, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_COMPONENTES) AS UltimaMov ON MOV_ESTOQUE.ID_COMPONENTES = UltimaMov.ID_COMPONENTES AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' "
        for chave, valor in parametros.items():
            if valor == '' or valor == 'None' or valor == 0.0:
                continue
            elif type(valor) == datetime.date and considerar_data == False:
                continue
            else:
                if type(valor) == str and chave == 'NOME':
                    consulta = consulta + f"AND COMPONENTES.{chave} LIKE '%{valor}%' "
                elif type(valor) == str and chave != 'SALDO':
                    consulta = consulta + f"AND COMPONENTES.{chave} = '{valor}' "
                elif type(valor) == datetime.date and considerar_data == True:
                    consulta = consulta + f"AND COMPONENTES.{chave} = '{valor}' "
                elif chave == 'SALDO':
                    if valor == 'Menor que 10':
                        consulta = consulta + f"AND UltimaMov.SALDO < 10 "
                    elif valor == 'Entre 10 e 50':
                        consulta = consulta + f"AND UltimaMov.Saldo Between 10 and 50 "
                    elif valor == 'Maior que 50':
                        consulta = consulta + f"AND UltimaMov.Saldo >= 50 "
                else:
                    consulta = consulta + f"AND COMPONENTES.{chave} = {valor} "
        with connection() as conn:
            df = pd.read_sql_query(consulta, conn)

    # ============================================= MODO DE EDIÇÃO =====================================================
    # ============================================= MODO DE EDIÇÃO =====================================================

    elif cons_or_edit == 'Edição':
        for chave, valor in parametros.items():
            # ==================================== IGNORAR VALORES NAO DIGITADOS =======================================
            # ==================================== IGNORAR VALORES NAO DIGITADOS =======================================
            if valor == '' or valor == 'None' or valor == 0.0 or chave == 'ID':
                continue
            elif type(valor) == datetime.date and considerar_data == False:
                continue
            # ====================================== EDITAR VALORES DIGITADOS ==========================================
            # ====================================== EDITAR VALORES DIGITADOS ==========================================
            else:
                with connection() as conn:
                    cursor = conn.cursor()
                    if type(valor) == str and chave != 'SALDO':
                        cursor.execute(f"UPDATE COMPONENTES SET {chave} = '{valor}' WHERE ID = '{parametros['ID']}'")
                    elif type(valor) == datetime.date and considerar_data == True:
                        cursor.execute(f"UPDATE COMPONENTES SET {chave} = '{valor}' WHERE ID = '{parametros['ID']}'")
                    elif chave == 'SALDO':
                        saldo = cursor.execute(f"SELECT SALDO FROM MOV_ESTOQUE WHERE ID_COMPONENTES = '{parametros['ID']}' ORDER BY DATA_MOV DESC LIMIT 1").fetchone()[0]
                        nome = cursor.execute(f"SELECT NOME FROM COMPONENTES WHERE ID = {parametros['ID']}").fetchone()[0]
                        if int(saldo) + int(parametros['SALDO']) < 0:
                            st.error(f"{nome} não possui estoque suficiente para retirada.")
                            exit()
                        else:
                            cursor.execute(f"INSERT INTO MOV_ESTOQUE (ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA_MOV, QUANTIDADE, SALDO) VALUES (NULL, {parametros['ID']}, '{nome}', DATETIME('now'), {parametros['SALDO']}, {int(saldo) + int(parametros['SALDO'])})")
                    else:
                        cursor.execute(f"UPDATE COMPONENTES SET {chave} = {valor} WHERE ID = '{parametros['ID']}'")
        if inativar:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE COMPONENTES SET STATUS = 'INATIVO' WHERE ID = {parametros['ID']}")
        conn.commit()
        st.rerun()
    return df


def consulta_equipamentos(parametros, considerar_data, cons_or_edit, df, inativar):
    # =========================================== CASO O MODO SEJA CONSULTA ============================================
    # ============================================ IGNORA OS CAMPOS VAZIOS =============================================
    if cons_or_edit == 'Consulta':
        if parametros['TIPO'] == 'Desktop' or parametros['TIPO'] == 'None':
            consulta = f"SELECT EQUIPAMENTOS.ID, EQUIPAMENTOS.NOME, EQUIPAMENTOS.FABRICANTE, EQUIPAMENTOS.TIPO, UltimaMov.SALDO AS QUANTIDADE, EQUIPAMENTOS.DATA_AQUISICAO, EQUIPAMENTOS.ESTADO, EQUIPAMENTOS.PRECO_UNIT, (SELECT NOME FROM COMPONENTES WHERE ID = Equipamentos.GABINETE) as GABINETE , (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.FONTE) as FONTE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_MAE) as PLACA_MAE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.CPU) AS PROCESSADOR, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.RAM) AS RAM, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.HD) AS HD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.SSD) AS SSD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_VIDEO) AS PLACA_VIDEO FROM EQUIPAMENTOS JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_EQUIPAMENTOS = EQUIPAMENTOS.ID JOIN (SELECT ID_EQUIPAMENTOS, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_EQUIPAMENTOS) AS UltimaMov ON MOV_ESTOQUE.ID_EQUIPAMENTOS = UltimaMov.ID_EQUIPAMENTOS AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' "
        else:
            consulta = f"SELECT EQUIPAMENTOS.ID, EQUIPAMENTOS.NOME, EQUIPAMENTOS.FABRICANTE, EQUIPAMENTOS.TIPO, UltimaMov.SALDO AS QUANTIDADE, EQUIPAMENTOS.DATA_AQUISICAO, EQUIPAMENTOS.ESTADO, EQUIPAMENTOS.PRECO_UNIT FROM EQUIPAMENTOS JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_EQUIPAMENTOS = EQUIPAMENTOS.ID JOIN (SELECT ID_EQUIPAMENTOS, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_EQUIPAMENTOS) AS UltimaMov ON MOV_ESTOQUE.ID_EQUIPAMENTOS = UltimaMov.ID_EQUIPAMENTOS AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' "
        for chave, valor in parametros.items():
            if valor == '' or valor == 'None' or valor == 0.0:
                continue
            elif type(valor) == datetime.date and considerar_data == False:
                continue

    # =========================================== CASO O MODO SEJA CONSULTA ============================================
    # ======================================= FILTRA CONSULTA PELOS PARAMETROS =========================================

            else:
                if type(valor) == str and chave == 'NOME':
                    consulta = consulta + f"AND EQUIPAMENTOS.{chave} LIKE '%{valor}%' "

                elif type(valor) == str and chave != 'SALDO':
                    with connection() as conn:
                        cursor = conn.cursor()
                        if chave == 'GABINETE' or chave == 'FONTE' or chave == 'PLACA_MAE' or chave == 'CPU' or chave == 'RAM' or chave == 'HD' or chave == 'SSD' or chave == 'PLACA_VIDEO':
                            id_comp = cursor.execute(f"SELECT ID FROM COMPONENTES WHERE NOME = '{valor}'").fetchone()[0]
                            consulta = consulta + f"AND EQUIPAMENTOS.{chave} = {id_comp} "
                        else:
                            consulta = consulta + f"AND EQUIPAMENTOS.{chave} = '{valor}' "
                elif type(valor) == datetime.date and considerar_data == True:
                    consulta = consulta + f"AND EQUIPAMENTOS.{chave} = '{valor}' "

                elif chave == 'SALDO':
                    if valor == 'Menor que 10':
                        consulta = consulta + f"AND UltimaMov.SALDO < 10 "
                    elif valor == 'Entre 10 e 50':
                        consulta = consulta + f"AND UltimaMov.Saldo Between 10 and 50 "
                    elif valor == 'Maior que 50':
                        consulta = consulta + f"AND UltimaMov.Saldo >= 50 "

                else:
                    consulta = consulta + f"AND EQUIPAMENTOS.{chave} = {valor} "
        with connection() as conn:
            df = pd.read_sql_query(consulta, conn)

    # ============================================ CASO O MODO SEJA EDIÇÃO =============================================
    # ============================================ IGNORA OS CAMPOS VAZIOS =============================================

    elif cons_or_edit == 'Edição':
        for chave, valor in parametros.items():
            # ==================================== IGNORAR VALORES NAO DIGITADOS =======================================
            # ==================================== IGNORAR VALORES NAO DIGITADOS =======================================
            if valor == '' or valor == 'None' or valor == 0.0 or chave == 'ID':
                continue
            elif type(valor) == datetime.date and considerar_data == False:
                continue
            # ====================================== EDITAR VALORES DIGITADOS ==========================================
            # ====================================== EDITAR VALORES DIGITADOS ==========================================
            else:
                with connection() as conn:
                    cursor = conn.cursor()
                    if type(valor) == str and chave != 'SALDO':
                        cursor.execute(f"UPDATE EQUIPAMENTOS SET {chave} = '{valor}' WHERE ID = '{parametros['ID']}'")
                    #===================================================================================================
                    #===================================================================================================
                    elif type(valor) == datetime.date and considerar_data == True:
                        cursor.execute(f"UPDATE EQUIPAMENTOS SET {chave} = '{valor}' WHERE ID = '{parametros['ID']}'")
                    #===================================================================================================
                    # ===================================================================================================
                    elif chave == 'SALDO':
                        # SE O TIPO DO EQUIPAMENTO QUE IRÁ ADICIONAR FOR DESKTOP CONSULTA PARA SABER SE CADA COMPONENTE POSSUI ESTOQUE
                        # SE O TIPO DO EQUIPAMENTO QUE IRÁ ADICIONAR FOR DESKTOP CONSULTA PARA SABER SE CADA COMPONENTE POSSUI ESTOQUE
                        if parametros['SALDO'] < 0:
                            pass
                        elif parametros['SALDO'] > 0:
                            if cursor.execute(f"SELECT TIPO FROM EQUIPAMENTOS WHERE ID = '{parametros['ID']}'").fetchone()[0] == 'Desktop':
                                gabinete = cursor.execute(f"SELECT GABINETE FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                fonte = cursor.execute(f"SELECT FONTE FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                placa_mae = cursor.execute(f"SELECT PLACA_MAE FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                cpu = cursor.execute(f"SELECT CPU FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                ram = cursor.execute(f"SELECT RAM FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                hd = cursor.execute(f"SELECT HD FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                ssd = cursor.execute(f"SELECT SSD FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                                placa_video = cursor.execute(f"SELECT PLACA_VIDEO FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]

                                lista_componentes = [gabinete, fonte, placa_mae, cpu, ram, hd, ssd, placa_video]
                                for index, id_comp in enumerate(lista_componentes):
                                    if id_comp == 'NULL':
                                        continue
                                    saldo_comp = cursor.execute(f"SELECT SALDO FROM MOV_ESTOQUE WHERE ID_COMPONENTES = {id_comp} ORDER BY DATA_MOV DESC LIMIT 1").fetchone()[0]
                                    nome_comp = cursor.execute(f"SELECT NOME FROM COMPONENTES WHERE ID = {id_comp}").fetchone()[0]
                                    if int(saldo_comp) - int(parametros['SALDO']) < 0:
                                        st.error(f"{nome_comp} não possui estoque suficiente para retirada.")
                                        exit()
                                    else:
                                        cursor.execute(f"INSERT INTO MOV_ESTOQUE (ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA_MOV, QUANTIDADE, SALDO) VALUES (NULL, {id_comp}, '{nome_comp}', DATETIME('now'), {parametros['SALDO']}, {int(saldo_comp) - int(parametros['SALDO'])})")

                        # ======= DEPOIS DE CONSULTADO CADA COMPONENTE, FAZ ALTERAÇÃO NO ESTOQUE DO EQUIPAMENTO ========
                        # ======= DEPOIS DE CONSULTADO CADA COMPONENTE, FAZ ALTERAÇÃO NO ESTOQUE DO EQUIPAMENTO ========

                        saldo = cursor.execute(f"SELECT SALDO FROM MOV_ESTOQUE WHERE ID_EQUIPAMENTOS = '{parametros['ID']}' ORDER BY DATA_MOV DESC LIMIT 1").fetchone()[0]
                        nome = cursor.execute(f"SELECT NOME FROM EQUIPAMENTOS WHERE ID = {parametros['ID']}").fetchone()[0]
                        if int(saldo) + int(parametros['SALDO']) < 0:
                            st.error(f"{nome} não possui estoque suficiente para retirada.")
                            exit()
                        else:
                            cursor.execute(f"INSERT INTO MOV_ESTOQUE (ID_EQUIPAMENTOS, ID_COMPONENTES, NOME, DATA_MOV, QUANTIDADE, SALDO) VALUES ({parametros['ID']}, NULL, '{nome}', DATETIME('now'), {parametros['SALDO']}, {int(saldo) + int(parametros['SALDO'])})")
                    else:
                        cursor.execute(f"UPDATE EQUIPAMENTOS SET {chave} = {valor} WHERE ID = '{parametros['ID']}'")
        if inativar:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE EQUIPAMENTOS SET STATUS = 'INATIVO' WHERE ID = {parametros['ID']}")
        conn.commit() # COMMIT NAS ALTERAÇÕES SOMENTE SE TODAS DEREM CERTO
        st.rerun()
    return df


def consulta():
    st.title('Módulo de Consulta')
    modulos_consulta = st.selectbox('Selecione a consulta', ['Componentes', 'Equipamentos', 'Manutenção', 'Fabricantes', 'Movimentação de Estoque'])

    # ============================================ CONSULTAS PARA PREENCHIMENTOS =======================================
    # ============================================ CONSULTAS PARA PREENCHIMENTOS =======================================

    with connection() as conn:
        inativar = False

        cursor = conn.cursor()
        fabricantes = cursor.execute('SELECT NOME FROM FABRICANTES').fetchall()
        for index, fabricante in enumerate(fabricantes):
            fabricantes[index] = str(fabricante)[2:-3]
        fabricantes.insert(0, 'None')

        tipo_componente = cursor.execute('SELECT NOME FROM TIPO_COMPONENTE').fetchall()
        for index, tip_comp in enumerate(tipo_componente):
            tipo_componente[index] = str(tip_comp)[2:-3]
        tipo_componente.insert(0, 'None')

        tipo_equipamento = cursor.execute('SELECT NOME FROM TIPO_EQUIPAMENTO').fetchall()
        for index, tip_equip in enumerate(tipo_equipamento):
            tipo_equipamento[index] = str(tip_equip)[2:-3]
        tipo_equipamento.insert(0, 'None')

        estados = cursor.execute('SELECT NOME FROM ESTADO').fetchall()
        for index, estado in enumerate(estados):
            estados[index] = str(estado)[2:-3]
        estados.insert(0, 'None')

        gabinetes = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Gabinete' AND STATUS = 'ATIVO'").fetchall()
        for index, gabinete in enumerate(gabinetes):
            gabinetes[index] = str(gabinete)[2:-3]
        gabinetes.insert(0, 'None')

        fontes = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Fonte' AND STATUS='ATIVO'").fetchall()
        for index, fonte in enumerate(fontes):
            fontes[index] = str(fonte)[2:-3]
        fontes.insert(0, 'None')

        placas_mae = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Placa-mãe' AND STATUS='ATIVO'").fetchall()
        for index, placa_mae in enumerate(placas_mae):
            placas_mae[index] = str(placa_mae)[2:-3]
        placas_mae.insert(0, 'None')

        cpus = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Processador' AND STATUS='ATIVO'").fetchall()
        for index, cpu in enumerate(cpus):
            cpus[index] = str(cpu)[2:-3]
        cpus.insert(0, 'None')

        memorias = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Memória RAM' AND STATUS='ATIVO'").fetchall()
        for index, memoria in enumerate(memorias):
            memorias[index] = str(memoria)[2:-3]
        memorias.insert(0, 'None')

        hds = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'HD' AND STATUS='ATIVO'").fetchall()
        for index, hd in enumerate(hds):
            hds[index] = str(hd)[2:-3]
        hds.insert(0, 'None')

        ssds = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'SSD' AND STATUS='ATIVO'").fetchall()
        for index, ssd in enumerate(ssds):
            ssds[index] = str(ssd)[2:-3]
        ssds.insert(0, 'None')

        placas_video = cursor.execute("SELECT NOME FROM COMPONENTES WHERE TIPO = 'Placa de vídeo' AND STATUS='ATIVO'").fetchall()
        for index, placa_video in enumerate(placas_video):
            placas_video[index] = str(placa_video)[2:-3]
        placas_video.insert(0, 'None')

    # ============================================== CONSULTA DE COMPONENTES ===========================================
    # ============================================== CONSULTA DE COMPONENTES ===========================================

    if modulos_consulta == 'Componentes':
        with connection() as conn:
            cursor = conn.cursor()
            # ========================================== DATAFRAME PRINCIPAL ===========================================
            # ========================================== DATAFRAME PRINCIPAL ===========================================
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10) # CRIA AS COLUNAS PARA CRIAR OS WIDGETS UM AO LADO DO OUTRO
            with col1:
                cons_or_edit = st.selectbox('Modo', ['Consulta', 'Edição'])
                if cons_or_edit == 'Edição':
                    inativar = st.checkbox('Inativar')
            with col2:
                id = st.text_input('ID')
            with col3:
                nome = st.text_input('Nome')
            with col4:
                fabricante = st.selectbox('Fabricante', (fabricante for fabricante in fabricantes))
            with col5:
                tipo = st.selectbox('Tipo', (tip_comp for tip_comp in tipo_componente))
            with col6:
                if cons_or_edit == 'Consulta':
                    quantidade = st.selectbox('Quantidade', ['None', 'Menor que 10', 'Entre 10 e 50', 'Maior que 50'])
                elif cons_or_edit == 'Edição':
                    quantidade = st.number_input('Quantidade', step=1)
            with col7:
                st.write('')
                st.write('')
                considerar_data = st.checkbox('Data')
            with col8:
                data_aquisicao = st.date_input('Data de aquisição')
            with col9:
                estado = st.selectbox('Estado', (state for state in estados))
            with col10:
                preco = st.number_input('Preço unitário')

            container = st.empty() # CRIA UM CONTAINER PARA CASO QUEIRA APAGAR WIDGETS QUE ESTEJAM DENTRO
            df = pd.read_sql_query(f"SELECT COMPONENTES.ID, COMPONENTES.NOME, COMPONENTES.FABRICANTE, COMPONENTES.TIPO, UltimaMov.SALDO AS QUANTIDADE, COMPONENTES.DATA_AQUISICAO, COMPONENTES.ESTADO, COMPONENTES.PRECO_UNIT FROM COMPONENTES JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_COMPONENTES = COMPONENTES.ID JOIN (SELECT ID_COMPONENTES, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_COMPONENTES) AS UltimaMov ON MOV_ESTOQUE.ID_COMPONENTES = UltimaMov.ID_COMPONENTES AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY COMPONENTES.ID ASC;", conn)
            container.dataframe(df)

            # ==================================== DATAFRAME COM CONSULTA FILTRADA =====================================
            # ==================================== DATAFRAME COM CONSULTA FILTRADA =====================================
            if cons_or_edit == 'Consulta':
                mudar_consulta = st.button('Consultar')
            elif cons_or_edit == 'Edição':
                mudar_consulta = st.button('Confirmar')

            if mudar_consulta:
                parametros = {'ID': id, 'NOME': nome, 'FABRICANTE': fabricante, 'TIPO': tipo, 'SALDO': quantidade, 'DATA_AQUISICAO': data_aquisicao, 'ESTADO': estado, 'PRECO_UNIT': preco}
                df = consulta_componentes(parametros, considerar_data, cons_or_edit, df, inativar)
                container.empty()
                container.dataframe(df)

    # ========================================== CONSULTA DE EQUIPAMENTOS ==============================================
    # ========================================== CONSULTA DE EQUIPAMENTOS ==============================================

    elif modulos_consulta == 'Equipamentos':
        with connection() as conn:
            cursor = conn.cursor()
            # ========================================== DATAFRAME PRINCIPAL ===========================================
            # ========================================== DATAFRAME PRINCIPAL ===========================================
            gabinete_desktop = 'None'
            fonte_desktop = 'None'
            placas_mae_desktop = 'None'
            cpu_desktop = 'None'
            memoria_desktop = 'None'
            hd_desktop = 'None'
            ssd_desktop = 'None'
            placa_video_desktop = 'None'

            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)  # CRIA AS COLUNAS PARA CRIAR OS WIDGETS UM AO LADO DO OUTRO
            with col1:
                cons_or_edit = st.selectbox('Modo', ['Consulta', 'Edição'])
                if cons_or_edit == 'Edição':
                    inativar = st.checkbox('Inativar')
            with col2:
                id = st.text_input('ID')
            with col3:
                nome = st.text_input('Nome')
            with col4:
                fabricante = st.selectbox('Fabricante', (fabricante for fabricante in fabricantes))
            with col5:
                tipo = st.selectbox('Tipo', (tip for tip in tipo_equipamento))
                if tipo == 'Desktop':
                    with col1:
                        gabinete_desktop = st.selectbox('Gabinete', (gabinete for gabinete in gabinetes))
                    with col2:
                        fonte_desktop = st.selectbox('Fonte', (fonte for fonte in fontes))
                    with col3:
                        placas_mae_desktop = st.selectbox('Placa-mãe', (placa_mae for placa_mae in placas_mae))
                    with col4:
                        cpu_desktop = st.selectbox('Processador', (cpu for cpu in cpus))
                    memoria_desktop = st.selectbox('Memória RAM', (memoria for memoria in memorias))
            with col6:
                if cons_or_edit == 'Consulta':
                    quantidade = st.selectbox('Quantidade', ['None', 'Menor que 10', 'Entre 10 e 50', 'Maior que 50'])
                elif cons_or_edit == 'Edição':
                    quantidade = st.number_input('Quantidade', step=1)
            with col7:
                st.write('')
                st.write('')
                considerar_data = st.checkbox('Data')
                if tipo == 'Desktop':
                    st.write('')
                    hd_desktop = st.selectbox('HD', (hd for hd in hds))
            with col8:
                data_aquisicao = st.date_input('Data de aquisição')
                if tipo == 'Desktop':
                    ssd_desktop = st.selectbox('SSD', (ssd for ssd in ssds))
            with col9:
                estado = st.selectbox('Estado', (state for state in estados))
                if tipo == 'Desktop':
                    placa_video_desktop = st.selectbox('Placa de Vídeo', (placa_video for placa_video in placas_video))
            with col10:
                preco = st.number_input('Preço unitário')

            container = st.empty()  # CRIA UM CONTAINER PARA CASO QUEIRA APAGAR WIDGETS QUE ESTEJAM DENTRO
            df = pd.read_sql_query(f"SELECT EQUIPAMENTOS.ID, EQUIPAMENTOS.NOME, EQUIPAMENTOS.FABRICANTE, EQUIPAMENTOS.TIPO, UltimaMov.SALDO AS QUANTIDADE, EQUIPAMENTOS.DATA_AQUISICAO, EQUIPAMENTOS.ESTADO, EQUIPAMENTOS.PRECO_UNIT, (SELECT NOME FROM COMPONENTES WHERE ID = Equipamentos.GABINETE) as GABINETE , (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.FONTE) as FONTE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_MAE) as PLACA_MAE, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.CPU) AS PROCESSADOR, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.RAM) AS RAM, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.HD) AS HD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.SSD) AS SSD, (SELECT NOME FROM COMPONENTES WHERE ID = EQUIPAMENTOS.PLACA_VIDEO) AS PLACA_VIDEO FROM EQUIPAMENTOS JOIN MOV_ESTOQUE ON MOV_ESTOQUE.ID_EQUIPAMENTOS = EQUIPAMENTOS.ID JOIN (SELECT ID_EQUIPAMENTOS, MAX(DATA_MOV) AS UltimaMovimentacao, SALDO FROM MOV_ESTOQUE GROUP BY ID_EQUIPAMENTOS) AS UltimaMov ON MOV_ESTOQUE.ID_EQUIPAMENTOS = UltimaMov.ID_EQUIPAMENTOS AND MOV_ESTOQUE.DATA_MOV = UltimaMov.UltimaMovimentacao AND STATUS = 'ATIVO' ORDER BY EQUIPAMENTOS.ID ASC;", conn)
            container.dataframe(df)

            # ========================================== CONSULTA FILTRADA =============================================
            # ========================================== CONSULTA FILTRADA =============================================
            if cons_or_edit == 'Consulta':
                mudar_consulta = st.button('Consultar')
            if cons_or_edit == 'Edição':
                mudar_consulta = st.button('Confirmar')
            if mudar_consulta:
                parametros = {'ID': id, 'NOME': nome, 'FABRICANTE': fabricante, 'TIPO': tipo, 'SALDO': quantidade, 'DATA_AQUISICAO': data_aquisicao, 'ESTADO': estado, 'PRECO_UNIT': preco, 'GABINETE': gabinete_desktop, 'FONTE': fonte_desktop, 'PLACA_MAE': placas_mae_desktop, 'CPU': cpu_desktop, 'RAM': memoria_desktop, 'HD': hd_desktop, 'SSD': ssd_desktop, 'PLACA_VIDEO': placa_video_desktop}
                df = consulta_equipamentos(parametros, considerar_data, cons_or_edit, df, inativar)
                container.empty()
                container.dataframe(df)

    # ========================================== CONSULTA DE MANUTENÇOES ===============================================
    # ========================================== CONSULTA DE MANUTENÇOES ===============================================

    elif modulos_consulta == 'Manutenção':
        with connection() as conn:
            df = pd.read_sql_query('SELECT * FROM MANUTENCAO', conn)
            st.dataframe(df)

    # ========================================== CONSULTA DE FABRICANTES ===============================================
    # ========================================== CONSULTA DE FABRICANTES ===============================================

    elif modulos_consulta == 'Fabricantes':
        with connection() as conn:
            df = pd.read_sql_query('SELECT * FROM FABRICANTES', conn)
            st.table(df)

    # ========================================== CONSULTA DE MOV_ESTOQUE ===============================================
    # ========================================== CONSULTA DE MOV_ESTOQUE ===============================================

    elif modulos_consulta == 'Movimentação de Estoque':
        with connection() as conn:
            df = pd.read_sql_query('SELECT * FROM MOV_ESTOQUE', conn)
            st.dataframe(df)
