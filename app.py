import streamlit as st
st.set_page_config(page_title="App Álvaro",page_icon='👣',initial_sidebar_state="expanded")
import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute())+'/apps')
import compras, calendario, ocr#, db_fxns, hydralit
#from  db_fxns import * 
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()
import pandas as pd 
import hashlib
#import hydralit
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
#Espacio minimo
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
#Barra lateral
st.sidebar.markdown("""
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">App de Álvaro</h1>
    </div>
    """,
    unsafe_allow_html=True)
st.sidebar.header('Login')

def create_table_users():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,userhash TEXT)')

def add_data_users(username, password):
    c.execute('INSERT INTO usertable(username,userhash) VALUES (?,?)',(username, hashlib.sha256(str.encode(password)).hexdigest()))
    conn.commit()

def view_active_username(username, userhash):
	c.execute('SELECT Count(username) FROM usertable WHERE username = "{}" and userhash = "{}" '.format(username,userhash))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT username FROM usertable')
	data = c.fetchall()
	return data

def delete_users(username):
	c.execute('DELETE FROM usertable WHERE username = "{}"'.format(username))
	conn.commit()

create_table_users()

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
#APPS
if view_active_username(user, hashlib.sha256(str.encode(password)).hexdigest())[0][0] >= 1:
    if 'user' not in st.session_state:
        st.session_state['user'] = user
        state.sync()
        st.experimental_rerun()

    over_theme = {'menu_background': '#e0e0e0','txc': '#111111','bgc_menu':'orange','txc_active':'white','txc_inactive': '#888888','option_active':'#464e5f'}
    app = HydraApp(
        hide_streamlit_markers=True,
        use_navbar=True, 
        navbar_sticky=True,
        navbar_animation=True,
        navbar_theme=over_theme
    )
    app.add_app("Compras", icon="🛒", app=compras.compras())
    app.add_app("Calendario", icon="📅", app=calendario.calendario())
    #app.add_app("OCR", icon="👓", app=ocr.ocr())
    complex_nav = {
            'Compras': ['Compras'],#['Compras','Calendario'],
            'Calendario': ['Calendario'],
     #       'OCR': ['OCR']
        }
    app.run(complex_nav)