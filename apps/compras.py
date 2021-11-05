from hydralit import HydraHeadApp

class compras(HydraHeadApp):
	def __init__(self, title = 'Hydralit Explorer', **kwargs):
		self.__dict__.update(kwargs)
		self.title = title
	def run(self):
		try:
			
			#################### VARIABLES ####################
			import pytz
			from datetime import datetime
			
			variables={}
			
			timezone = pytz.timezone("Europe/Madrid")
			now = str(datetime.now().astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"))
			now_time = datetime.now().astimezone(timezone)
			variables['now']='"'+now+'"'
			
			user='Raúl'
			variables['user']='"'+user+'"'
			
			def table_variables(table,fields_type):
				variables[table]={}
				variables[table]['fields_type']=fields_type
				variables[table]['fields_type_id']='id INTEGER PRIMARY KEY,'+fields_type
				variables[table]['fields_type_db']=fields_type+',Active_Date DATETIME,Active_User TEXT,Deactive_Date DATETIME,Deactive_User TEXT,Traza NUMBER,Active NUMBER'
				variables[table]['fields_type_id_db']=variables[table]['fields_type_id']+',Active_Date DATETIME,Active_User TEXT,Deactive_Date DATETIME,Deactive_User TEXT,Traza NUMBER,Active NUMBER'
			
				#variables[table]['fields']='"'+'","'.join([i.split(' ')[0] for i in variables[table]['fields_type'].split(',')])+'"'
				#variables[table]['fields_id']='"'+'","'.join([i.split(' ')[0] for i in variables[table]['fields_type_id'].split(',')])+'"'
				variables[table]['fields_db']='"'+'","'.join([i.split(' ')[0] for i in variables[table]['fields_type_db'].split(',')])+'"'
				variables[table]['fields_id_db']='"'+'","'.join([i.split(' ')[0] for i in variables[table]['fields_type_id_db'].split(',')])+'"'
				#variables[table]['fields_name']=variables[table]['fields'].replace('"','')
				#variables[table]['fields_id_name']=variables[table]['fields_id'].replace('"','')
				variables[table]['fields_db_name']=variables[table]['fields_db'].replace('"','')
				variables[table]['fields_id_db_name']=variables[table]['fields_id_db'].replace('"','')
				variables[table]['values_db']=',{},{},null,null,null,"1"'.format(variables['now'],variables['user'])
				return variables
			
			
			#################### db ####################
			import pandas as pd
			import streamlit as st
			from st_aggrid import AgGrid, GridOptionsBuilder,  GridUpdateMode#, DataReturnMode, JsCode
			import sqlite3
			conn = sqlite3.connect('data.db',check_same_thread=False)
			c = conn.cursor()
			
			def table_drop(table):
				c.execute('DROP TABLE IF EXISTS {}'.format(table))
			def table_create(table,variables=variables):
				c.execute('CREATE TABLE IF NOT EXISTS {}({});'.format(table,variables[table]['fields_type_id_db'])) 
			
			def table_view(table,active='1',view='fields_id',variables=variables):
				if active=='1':
					active='Where Active=1'
				elif active=='0':
					active='Where Active=0'
				elif active=='None':
					active=''
				if view=='fields':
					view=variables[table]['fields_type']
				elif view=='fields_id':
					view=variables[table]['fields_type_id']
				elif view=='fields_id_db':
					view=variables[table]['fields_type_id_db']
				c.execute('SELECT * FROM {} {}'.format(table,active))
				data = c.fetchall()
				df=pd.DataFrame(data,columns=variables[table]['fields_id_db_name'].split(','))
				df=df[[i.split(' ')[0] for i in view.split(',')]]
				return df
			
			def row_add(table,values,variables=variables):
				c.execute("INSERT INTO {} ({}) VALUES ({});".format(table,variables[table]['fields_db_name'],values+variables[table]['values_db']))
				conn.commit()
			def row_deactivate(table,id,variables):
				c.execute('UPDATE {} SET Active =0 , Deactive_Date = {} , Deactive_User = {} WHERE id ={} and Active = 1'.format(table,variables['now'],variables['user'],id))
				conn.commit()
			
			def row_activate_hist(table,id):
				c.execute('UPDATE {} SET Active =-1 WHERE id ={} and Active = 0'.format(table,id))
				conn.commit()
			def row_activate(table,fields_db_name,values_add):
				c.execute("INSERT INTO {} ({}) VALUES ({});".format(table,fields_db_name,values_add))
				conn.commit()
			
			def show_aggrid(df,checkbox=True):
				gb = GridOptionsBuilder.from_dataframe(df)
				#gb.configure_pagination()
				gb.configure_side_bar()
				gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
				gb.configure_selection(selection_mode="multiple", use_checkbox=checkbox)
				gridOptions = gb.build()
				grid_response = AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED,
					height=180,
					fit_columns_on_grid_load=True,
					#update_mode= 'MODEL_CHANGED',# 0:"NO_UPDATE"1:"MANUAL"2:"VALUE_CHANGED"3:"SELECTION_CHANGED"4:"FILTERING_CHANGED"5:"SORTING_CHANGED"6:"MODEL_CHANGED"
					data_return_mode= 'as_input' ,
					allow_unsafe_jscode=True,
					enable_enterprise_modules=True,
					#conversion_errors='coerce',
					reload_data=False,
					theme='blue'
					)
				return grid_response["selected_rows"]
			
			
			#################### init ####################
			variables = table_variables('compra','Artículo TEXT,Descripción TEXT,Número NUMBER')
			#table_drop(table)
			table_create('compra')
			
			c1, c2= st.columns((1,4))
			tipo_productos=c1.selectbox('Tipo de Productos', ['Activos','Inactivos','Todos'])
			if tipo_productos=='Activos':
				df_compra=table_view('compra')
				with st.form(key='Desactivar_id_activos'):
					selection = show_aggrid(df_compra)
					submit_button = st.form_submit_button(label='Desactivar')
					if submit_button:
						selection = [i for i in selection]					
						for id in selection:
							row_deactivate('compra',id['id'],variables)
						st.experimental_rerun()
				c1, c2, c3= st.columns((1,1,1))
				variables = table_variables('articulo','Localización TEXT,Artículo TEXT')
				table_create('articulo')
				df_artículos=table_view('articulo',active='1',view='fields_id')
				Artículo = c1.selectbox("Seleccionar Artículo",df_artículos[['Artículo']])#c1.text_input("Seleccionar Artículo")
				Descripción = c2.text_input("Descripción")
				Número = c3.number_input("Número de Artículos",value=1)
				values='"'+'","'.join(str(i) for i in [Artículo,Descripción,Número])+'"'
				if st.button("Añadir",key='añadir compra'):
					row_add('compra',values)
					st.experimental_rerun()
			
				with st.expander('Expandir para añadir Artículos no disponibles en la Selección'):
					c1, c2, c3= st.columns((1,1,1))
					with c2.container():
						Artículo = st.text_input("Artículos")
					with c1.container():
						Localización = st.selectbox("Localización",['Nevera','Desayunos','Conservas','Baño'])
						values='"'+'","'.join(str(i) for i in [Localización,Artículo])+'"'
						if st.button("Añadir",key='añadir Artículos'):
							row_add('articulo',values)
							st.experimental_rerun()
					with c3.container():
						show_aggrid(df_artículos,checkbox=False)
					
			if tipo_productos=='Inactivos':
				df_artículos=table_view('compra','0')
				with st.form(key='Activar_id_inactivos'):
					selection = show_aggrid(df_artículos)
					submit_button = st.form_submit_button(label='Activar')
					if submit_button:
						selection = [i for i in selection]					
						for id in selection:
							id['Traza']=id['id']
							id['Active_Date']=now.replace('"','')
							id['Active_User']=user.replace('"','')
							id['Deactive_Date']='None'
							id['Deactive_User']='None'
							id['Active']=1
							id.pop('id',None)
							fields_db_name=','.join(map(str,list(id.keys())))
							values_add='"'+'","'.join(map(str,list(id.values())))+'"'
							row_activate_hist('compra',id['Traza'])
							row_activate('compra',fields_db_name,values_add)
						st.experimental_rerun()
			
			if tipo_productos=='Todos':
				df_artículos=table_view('compra','None','fields_id_db')
				selection = show_aggrid(df_artículos,checkbox=False)
			
			#if st.button("B"):
			#	table_drop('compra')
			#	table_drop('articulo')
			#	st.experimental_rerun()
			
			
			
			#Borrar linea articulo con id



		except Exception as e:
			from pathlib import Path
			path = str(Path(__file__).parent.absolute())
			st.image(path+"/failure.png",width=100,)
			st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
			st.error('Error details: {}'.format(e))
		