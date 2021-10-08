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
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">App de Álvaro</h1>
    </div>
    """
stc.html(HTML_BANNER)

ListMenu = ['Compra','Calendario']
ChoiceMenu = st.radio('Menú',ListMenu)
if ChoiceMenu == 'Compra':
	ListCompra = ['Ver','Añadir','Borrar']
	ChoiceCompra = st.radio('Artículo',ListCompra)
	create_table_compra()
	if ChoiceCompra == 'Ver':
		result = view_all_data_compra()
		clean_df = pd.DataFrame(result,columns=["articulo","fecha"])
		st.dataframe(clean_df)
	if ChoiceCompra == 'Añadir':
		Artículo = st.text_area("Añadir Artículo")
		if st.button("Crear"):
			add_data_compra(Artículo,now)
			st.success("Añadido el Aartículo ::{} ::".format(Artículo))
	if ChoiceCompra == 'Borrar':
		unique_list = [i[0] for i in view_all_task_names_compra()]
		delete_by_task_name = st.multiselect('Selecciona Artículos para Borrar', unique_list)
		if st.button("Borrar"):
			for Artículos in delete_by_task_name:
				delete_data_compra(Artículos)
			st.warning("Borrados los Artículos: '{}'".format(delete_by_task_name))
if ChoiceMenu == 'Calendario':
	ListCalendar = ['Ver','Añadir','Borrar']
	ChoiceCalendar = st.radio('Artículo',ListCalendar)
	create_table_calendar()
	if ChoiceCalendar == 'Ver':
		result = view_all_data_calendar()
		clean_df = pd.DataFrame(result,columns=["articulo","fecha"])
		st.dataframe(clean_df)
	if ChoiceCalendar == 'Añadir':
		date = st.date_input('Fecha')
		hour = st.time_input('Hora')
		fecha = str(date) +' '+ str(hour)
		evento = st.text_area("Evento")
		if st.button("Crear"):
			add_data_calendar(evento,fecha)
			st.success("Añadido el Aartículo ::{} ::".format(evento))
	if ChoiceCalendar == 'Borrar':
		unique_list = [i[0] for i in view_all_task_names_calendar()]
		delete_by_task_name = st.multiselect('Selecciona Artículos para Borrar', unique_list)
		if st.button("Borrar"):
			for Artículos in delete_by_task_name:
				delete_data_calendar(Artículos)
			st.warning("Borrados los Artículos: '{}'".format(delete_by_task_name))




