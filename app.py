import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd 
from db_fxns import * 
import sqlite3
from datetime import datetime
from datetime import date
import pytz
import base64
#import streamlit.components.v1 as components
import hashlib
import os
new_timezone = pytz.timezone("Europe/Madrid")
now = str(datetime.now().astimezone(new_timezone).strftime("%Y-%m-%d %H:%M:%S"))
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()
create_table_users()

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

user = st.sidebar.text_input("User",'',key='user') 
password = st.sidebar.text_input("Password",'',type='password',key='password') 
with st.sidebar.expander('Desarrollador', expanded=False):
	password_admin_input = st.text_input("Password",'',type='password',key='password_admin_input') 
	if password_admin_input == st.secrets["password"]:
		if st.button("Reseteo compra"):
			try:
				c.execute('DROP TABLE compra')
				st.experimental_rerun()
			except:
				pass
		if st.button("Reseteo calendar"):
			try:
				c.execute('DROP TABLE calendar')
				st.experimental_rerun()
			except:
				pass
		if st.button("Reseteo tickets"):
			try:
				c.execute('DROP TABLE tickets')
				st.experimental_rerun()
			except:
				pass
		st.markdown("---")
		User_Name = st.text_input('Añadir Usuario')
		Password_Name = st.text_input('Añadir Password')
		if st.button("Grabar Usuario"):
			if User_Name and Password_Name:
				add_data_users(User_Name,Password_Name)
			else:
				st.write('Añadir usuario y/o contraseña')
		if st.button("Reseteo usuarios"):
			try:
				c.execute('DROP TABLE usertable')
				create_table_users()
				st.experimental_rerun()
			except:
				pass

if view_active_username(user, hashlib.sha256(str.encode(password)).hexdigest())[0][0] >= 1:
	st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	ListMenu = ['Compras','Calendario']
	ChoiceMenu = st.radio('Menú',ListMenu)

	if ChoiceMenu == 'Compras':
		create_table_compra()
		result = view_active_data_compra()
		clean_df = pd.DataFrame(result,columns=["Artículo","Descripción","Número","Inscripción_Fecha",'Inscripción_User','Modificación_Fecha','Modificación_User',"Activo"])
		st.dataframe(clean_df[["Artículo","Descripción","Número"]])
		c1, c2 = st.columns((1,1))
		with c1.container():
			st.markdown("---")
			Artículo = st.text_input("Añadir Artículo")
			Descripción = st.text_input("Descripción")
			Número = st.number_input("Número de Artículos",value=1)
			if st.button("Añadir",''):
				add_data_compra(Artículo,Descripción,Número,now,user)
				st.experimental_rerun()
		with c2.container():
			st.markdown("---")
			unique_list = [i for i in view_all_task_names_compra()]
			delete_by_task_name = st.multiselect('Borrar Artículos', unique_list)
			if st.button("Borrar"):
				for Artículos in delete_by_task_name:
					deactivate_data_compra(Artículos[0],Artículos[1],Artículos[2],now,user)
				st.experimental_rerun()
			st.markdown("")
			st.markdown("")
			st.markdown("")
			unique_list = [i for i in view_all_deleted_task_names_compra()]
			delete_by_task_name = st.multiselect('Reactivar Artículos', unique_list)
			if st.button("Reactivar"):
				for Artículos in delete_by_task_name:
					reactivate_data_compra(Artículos[0],Artículos[1],Artículos[2],now,user)
				st.experimental_rerun()
		st.markdown("---")
		c1, c2 = st.columns((1,1))
		historic = view_all_data_compra()
		clean_historic_df = pd.DataFrame(historic,columns=["Artículo","Descripción","Número","Inscripción_Fecha",'Inscripción_User','Modificación_Fecha','Modificación_User',"Activo"])
		if c1.button("Histórico"):
			c1.dataframe(clean_historic_df)
		c2.download_button(label="Descargar CSV",data=clean_historic_df.to_csv().encode('utf-8'), file_name='Compras_historico.csv', mime='text/csv', )

	if ChoiceMenu == 'Calendario':
		create_table_calendar()
		result = view_active_data_calendar()
		clean_df = pd.DataFrame(result,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
		st.dataframe(clean_df[["Evento","Comentarios","Fecha"]])
		c1, c2 = st.columns((1,1))
		with c1.container():
			st.markdown("---")
			Evento = st.text_input("Añadir Evento")
			Comentarios = st.text_input("Comentarios")
			date = st.date_input('Fecha')
			hour = st.time_input('Hora')
			Fecha = str(date) +' '+ str(hour)
			if st.button("Añadir",''):
				add_data_calendar(Evento,Comentarios,Fecha,now,user)
				st.experimental_rerun()
		with c2.container():
			st.markdown("---")
			unique_list = [i for i in view_all_task_names_calendar()]
			delete_by_task_name = st.multiselect('Borrar Eventos', unique_list)
			if st.button("Borrar"):
				for Evento in delete_by_task_name:
					deactivate_data_calendar(Evento[0],Evento[1],Evento[2])
				st.experimental_rerun()
			st.markdown("")
			st.markdown("")
			st.markdown("")
			unique_list = [i for i in view_all_deleted_task_names_calendar()]
			delete_by_task_name = st.multiselect('Reactivar Eventos', unique_list)
			if st.button("Reactivar"):
				for Evento in delete_by_task_name:
					reactivate_data_calendar(Evento[0],Evento[1],Evento[2])
				st.experimental_rerun()
		st.markdown("---")
		c1, c2 = st.columns((1,1))
		historic = view_all_data_calendar()
		clean_historic_df = pd.DataFrame(historic,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
		if c1.button("Histórico"):
			c1.dataframe(clean_historic_df)
		c2.download_button(label="Descargar CSV",data=clean_historic_df.to_csv().encode('utf-8'), file_name='Calendario_historico.csv', mime='text/csv', )




from plyer.utils import platform
from plyer import notification

notification.notify(
    title='Here is the title',
    message='Here is the message',
    app_name='Here is the application name',
    app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
)