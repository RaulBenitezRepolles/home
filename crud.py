import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd 
from db_fxns import * 
import sqlite3
from datetime import datetime
from datetime import date

now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

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

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">App de Álvaro</h1>
    </div>
    """
stc.html(HTML_BANNER)

password = st.sidebar.text_input("Password",type='password') 
if password == st.secrets["password"]:
	#botones radio horizontal
	st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	ListMenu = ['Compra','Calendario']
	ChoiceMenu = st.radio('Menú',ListMenu)

	if ChoiceMenu == 'Compra':
		create_table_compra()
		result = view_active_data_compra()
		clean_df = pd.DataFrame(result,columns=["Artículo","Fecha","Activo"])
		st.dataframe(clean_df[["Artículo"]])
		c1, c2, c3 = st.columns((1,1,1))
		Artículo = c1.text_area("Añadir Artículo")
		if c1.button("Añadir",''):
			add_data_compra(Artículo,now)
			st.experimental_rerun()
		unique_list = [i[0] for i in view_all_task_names_compra()]
		delete_by_task_name = c2.multiselect('Selecciona Artículos para Borrar', unique_list)
		if c2.button("Borrar"):
			for Artículos in delete_by_task_name:
				deactivate_data_compra(Artículos)
			st.experimental_rerun()
		if c3.button("Histórico"):
			historic = view_all_data_compra()
			clean_historic_df = pd.DataFrame(historic,columns=["Artículo","Fecha","Activo"])
			c3.dataframe(clean_historic_df)

	if ChoiceMenu == 'Calendario':
		create_table_calendar()
		result = view_active_data_calendar()
		clean_df = pd.DataFrame(result,columns=["Evento","Fecha","Activo"])
		st.dataframe(clean_df[["Evento","Fecha"]])
		c1, c2, c3 = st.columns((1,1,1))
		Evento = c1.text_area("Añadir Evento")
		date = c1.date_input('Fecha')
		hour = c1.time_input('Hora')
		Fecha = str(date) +' '+ str(hour)
		if c1.button("Añadir"):
			add_data_calendar(Evento,Fecha)
			st.experimental_rerun()
		unique_list = [i for i in view_all_task_names_calendar()]
		delete_by_task_name = c2.multiselect('Selecciona Eventos a Borrar', unique_list)
		if c2.button("Borrar"):
			for Artículos in delete_by_task_name:
				deactivate_data_calendar(Artículos[0])
			st.experimental_rerun()
		if c3.button("Histórico"):
			historic = view_all_data_calendar()
			clean_historic_df = pd.DataFrame(historic,columns=["evento","Fecha","Activo"])
			c3.dataframe(clean_historic_df)


