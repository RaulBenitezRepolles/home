import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd 
from db_fxns import * 
import sqlite3
from datetime import datetime
from datetime import date
import base64
import os


now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

st.set_page_config(page_title="App Álvaro")
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


user = st.sidebar.text_input("User",'Raúl',key='user') 
password = st.sidebar.text_input("Password",'',type='password',key='password') 
if password == st.secrets["password"]:
	#botones radio horizontal
	st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	ListMenu = ['Compras','Calendario']
	ChoiceMenu = st.radio('Menú',ListMenu)

	if ChoiceMenu == 'Compras':
		create_table_compra()
		result = view_active_data_compra()
		clean_df = pd.DataFrame(result,columns=["Artículo","Descripción","Número","Inscripción_Fecha",'Inscripción_User','Modificación_Fecha','Modificación_User',"Activo"])
		st.dataframe(clean_df[["Artículo","Descripción","Número"]])
		c1, c2, c3 = st.columns((1,1,1))
		Artículo = c1.text_input("Añadir Artículo")
		Descripción = c1.text_input("Descripción")
		Número = c1.number_input("Número de Artículos",value=0)
		if c1.button("Añadir",''):
			add_data_compra(Artículo,Descripción,Número,now,user)
			st.experimental_rerun()
		unique_list = [i for i in view_all_task_names_compra()]
		delete_by_task_name = c2.multiselect('Selecciona Artículos para Borrar', unique_list)
		if c2.button("Borrar"):
			for Artículos in delete_by_task_name:
				deactivate_data_compra(Artículos[0],Artículos[1],Artículos[2],now,user)
			st.experimental_rerun()
		unique_list = [i for i in view_all_deleted_task_names_compra()]
		delete_by_task_name = c2.multiselect('Selecciona Artículos para Reactivar', unique_list)
		if c2.button("Reactivar"):
			for Artículos in delete_by_task_name:
				reactivate_data_compra(Artículos[0],Artículos[1],Artículos[2],now,user)
			st.experimental_rerun()
		if c3.button("Histórico"):
			historic = view_all_data_compra()
			clean_historic_df = pd.DataFrame(historic,columns=["Artículo","Descripción","Número","Inscripción_Fecha",'Inscripción_User','Modificación_Fecha','Modificación_User',"Activo"])
			c3.dataframe(clean_historic_df)

	if ChoiceMenu == 'Calendario':
		create_table_calendar()
		result = view_active_data_calendar()
		clean_df = pd.DataFrame(result,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
		st.dataframe(clean_df[["Evento","Comentarios","Fecha"]])
		c1, c2, c3 = st.columns((1,1,1))
		Evento = c1.text_input("Añadir Evento")
		Comentarios = c1.text_input("Añadir Comentarios")

		unique_list = [i for i in view_all_task_names_calendar()]
		delete_by_task_name = c2.multiselect('Selecciona Eventos a Borrar', unique_list)
		if c2.button("Borrar"):
			for Evento in delete_by_task_name:
				deactivate_data_calendar(Evento[0],Evento[1],Evento[2])
			st.experimental_rerun()


		if c3.button("Histórico"):
			historic = view_all_data_calendar()
			clean_historic_df = pd.DataFrame(historic,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
			c3.dataframe(clean_historic_df)

		c1, c2, c3, c4 = st.columns((1,1,2,2))
		date = c1.date_input('Fecha')
		hour = c2.time_input('Hora')
		Fecha = str(date) +' '+ str(hour)
		if c1.button("Añadir",''):
			add_data_calendar(Evento,Comentarios,Fecha,now,user)
			st.experimental_rerun()

		unique_list = [i for i in view_all_deleted_task_names_calendar()]
		delete_by_task_name = c3.multiselect('Selecciona Eventos a Reactivar', unique_list)
		if c3.button("Reactivar Borrados"):
			for Evento in delete_by_task_name:
				reactivate_data_calendar(Evento[0],Evento[1],Evento[2])
			st.experimental_rerun()















#with st.sidebar.expander('Desarrollador', expanded=False):
#	password2 = st.text_input("Password",'admin',type='password',key='password2') 
#	if password2 == 'admin':
#		if st.button("Reseteo compra"):
#			c.execute('DROP TABLE compra')
#			st.experimental_rerun()
#		if st.button("Reseteo calendar"):
#			c.execute('DROP TABLE calendar')
#			st.experimental_rerun()
#		if st.button("Reseteo tickets"):
#			c.execute('DROP TABLE tickets')
#			st.experimental_rerun()