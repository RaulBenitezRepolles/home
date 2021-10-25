import streamlit as st
st.set_page_config(page_title="App Álvaro",page_icon='👣',initial_sidebar_state="expanded")

import sys
sys.path.append('./apps')
import compras, calendario, db_fxns, hydralit
from  db_fxns import * 
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()
create_table_users()
import pandas as pd 
import hashlib
from hydralit import HydraApp

#ocultar menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#margenes
st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: {3000}px;
            padding-top: {1}rem;
            padding-right: {2.5}rem;
            padding-left: {2.5}rem;
            padding-bottom: {1}rem;
        }}
    </style>
    """,
            unsafe_allow_html=True)
#Barra lateral
st.sidebar.markdown("""
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">App de Álvaro</h1>
    </div>
    """,
    unsafe_allow_html=True)
st.sidebar.header('Login')
user = st.sidebar.text_input("User",'',key='user') 
password = st.sidebar.text_input("Password",'',type='password',key='password') 
st.sidebar.markdown("---")
password_admin_input = st.sidebar.text_input("Acceso Desarrollo",'',type='password',key='password_admin_input') 
if password_admin_input == st.secrets["password"]:
    if st.sidebar.button("Reseteo compra"):
        try:
            c.execute('DROP TABLE compra')
            st.experimental_rerun()
        except:
            pass
    if st.sidebar.button("Reseteo calendar"):
        try:
            c.execute('DROP TABLE calendar')
            st.experimental_rerun()
        except:
            pass
    if st.sidebar.button("Reseteo tickets"):
        try:
            c.execute('DROP TABLE tickets')
            st.experimental_rerun()
        except:
            pass
    st.sidebar.markdown("---")
    User_Name = st.sidebar.text_input('Añadir Usuario')
    Password_Name = st.sidebar.text_input('Añadir Password')
    if st.sidebar.button("Grabar Usuario"):
        if User_Name and Password_Name:
            add_data_users(User_Name,Password_Name)
        else:
            st.sidebar.write('Añadir usuario y/o contraseña')
    if st.sidebar.button("Listar usuarios"):
        result = view_all_users()
        usuarios_df = pd.DataFrame(result,columns=["Usuarios"])
        st.sidebar.dataframe(usuarios_df[["Usuarios"]])
    unique_list = [i[0] for i in view_all_users()]
    delete_by_user_name = st.sidebar.multiselect('Usuarios a borrar', unique_list)
    if st.sidebar.button("Borrar Usuarios"):
        for Usuarios in delete_by_user_name:
            delete_users(Usuarios)
        st.experimental_rerun()
        st.experimental_rerun()
    if st.sidebar.button("Reseteo usuarios"):
        try:
            c.execute('DROP TABLE usertable')
            create_table_users()
            st.experimental_rerun()
        except:
            pass


if view_active_username(user, hashlib.sha256(str.encode(password)).hexdigest())[0][0] >= 1:
    if 'user' not in st.session_state:
        st.session_state['user'] = user
        state.sync()

    over_theme = {'menu_background': '#FFFFFF','txc': '#111111','bgc_menu':'orange','txc_active':'white','txc_inactive': '#888888','option_active':'#464e5f'}
    app = HydraApp(
        hide_streamlit_markers=True,
        use_navbar=True, 
        navbar_sticky=True,
        navbar_animation=True,
        navbar_theme=over_theme
    )
    app.add_app("Compras", icon="🛒", app=compras.compras())
    app.add_app("Calendario", icon="📅", app=calendario.calendario())
    complex_nav = {
            'Compras': ['Compras','Calendario'],#['Compras','Calendario'],
            'Calendario': ['Calendario'],
        }
    app.run(complex_nav)