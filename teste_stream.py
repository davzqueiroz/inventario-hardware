import streamlit as st
import streamlit_authenticator as stauth
import sqlite3

from cadastro_stream import cadastro
from consulta_stream import consulta
from usuarios_stream import usuarios

st.set_page_config(page_title='Controle de Inventário de Hardware', page_icon='💾', layout='wide')


def connection(bank_rad):
    conn = sqlite3.connect(bank_rad)
    return conn


# =============================================== TESTE BANCO DE DADOS =================================================
# =============================================== TESTE BANCO DE DADOS =================================================

config = {"credentials": {'usernames': {}}, "cookie": {'expiry_days': 1, 'key': 'some_signature_key', 'name': 'some_cookie_name'}}

with connection('bank_rad') as conn:
    cursor = conn.cursor()
    usernames = cursor.execute(f"SELECT USERNAME FROM USUARIOS_STREAMLIT").fetchall()

    for index, usuario in enumerate(usernames):
        email = cursor.execute(f"SELECT EMAIL FROM USUARIOS_STREAMLIT WHERE USERNAME = '{usuario[0]}'").fetchone()
        failed_login_attempts = cursor.execute(f"SELECT FAILED_LOGIN_ATTEMPTS FROM USUARIOS_STREAMLIT WHERE USERNAME = '{usuario[0]}'").fetchone()
        logged_in = cursor.execute(f"SELECT LOGGED_IN FROM USUARIOS_STREAMLIT WHERE USERNAME = '{usuario[0]}'").fetchone()
        name = cursor.execute(f"SELECT NAME FROM USUARIOS_STREAMLIT WHERE USERNAME = '{usuario[0]}'").fetchone()
        password = cursor.execute(f"SELECT PASSWORD FROM USUARIOS_STREAMLIT WHERE USERNAME = '{usuario[0]}'").fetchone()

        config['credentials']['usernames'][usuario[0]] = {'email': email[0], 'failed_login_attempts': failed_login_attempts[0], 'logged_in': logged_in[0], 'name': name[0], 'password': password[0]}

# Criando objeto autenticador
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

# ============================================== SIDEBAR + TELA DE LOGIN ===============================================
# ============================================== SIDEBAR + TELA DE LOGIN ===============================================

# Criando widget login
try:
    authenticator.login()
except stauth.utilities.exceptions.LoginError as e:
    st.error(e)

# ========================================== HOME CASO LOGIN ESTEJA FEITO ==============================================
# ========================================== HOME CASO LOGIN ESTEJA FEITO ==============================================

if st.session_state["authentication_status"]:
    if st.session_state['username'] == 'davi':
        modulos = ['Home', 'Cadastro', 'Consulta', 'Usuários', 'Configurações']
    else:
        modulos = ['Home', 'Cadastro', 'Consulta']

    sidebar = st.sidebar.selectbox('Selecione o módulo', modulos)

    if sidebar == 'Home':
        st.title('Serviço de Controle de Inventário de Hardware')
        st.subheader(f'Bem-vindo *{st.session_state["name"]}*')

        authenticator.logout()

# ========================================= MODULOS CASO LOGIN ESTEJA FEITO ============================================
# ========================================= MODULOS CASO LOGIN ESTEJA FEITO ============================================

    elif sidebar == 'Cadastro':
        cadastro()

    elif sidebar == 'Consulta':
        consulta()

    elif sidebar == 'Movimentação de Estoque':
        pass

    elif sidebar == 'Usuários':
        usuarios()






























# ============================= MENSAGENS CASO LOGIN ESTEJA ERRADO OU NAO TENHA SIDO INSERIDO ==========================
# ============================= MENSAGENS CASO LOGIN ESTEJA ERRADO OU NAO TENHA SIDO INSERIDO ==========================

if st.session_state["authentication_status"] is False:
    st.error('Usuário e/ou senha incorretos')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor insira usuário e senha')
