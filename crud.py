import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd 
from db_fxns import * 
import sqlite3
from datetime import datetime
from datetime import date
import base64



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
password = st.sidebar.text_input("Password",'29092021',type='password',key='password') 
if password == st.secrets["password"]:
	#botones radio horizontal
	st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	ListMenu = ['Compras','Calendario']
	ChoiceMenu = st.radio('Menú',ListMenu)

	if ChoiceMenu == 'Compras':
		create_table_compra()
		result = view_active_data_compra()
		clean_df = pd.DataFrame(result,columns=["Artículo","Descripción","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
		st.dataframe(clean_df[["Artículo","Descripción"]])
		c1, c2, c3 = st.columns((1,1,1))
		Artículo = c1.text_area("Añadir Artículo")
		Descripción = c1.text_area("Añadir Descripción")
		if c1.button("Añadir",''):
			add_data_compra(Artículo,Descripción,now,user)
			st.experimental_rerun()
		unique_list = [i for i in view_all_task_names_compra()]
		delete_by_task_name = c2.multiselect('Selecciona Artículos para Borrar', unique_list)
		if c2.button("Borrar"):
			for Artículos in delete_by_task_name:
				deactivate_data_compra(Artículos[0],Artículos[1])
			st.experimental_rerun()
		unique_list = [i for i in view_all_deleted_task_names_compra()]
		delete_by_task_name = c2.multiselect('Selecciona Artículos para Reactivar', unique_list)
		if c2.button("Reactivar"):
			for Artículos in delete_by_task_name:
				reactivate_data_compra(Artículos[0],Artículos[1])
			st.experimental_rerun()
		if c3.button("Histórico"):
			historic = view_all_data_compra()
			clean_historic_df = pd.DataFrame(historic,columns=["Artículo","Descripción","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
			c3.dataframe(clean_historic_df)

	if ChoiceMenu == 'Calendario':
		create_table_calendar()
		result = view_active_data_calendar()
		clean_df = pd.DataFrame(result,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
		st.dataframe(clean_df[["Evento","Comentarios","Fecha"]])
		c1, c2, c3 = st.columns((1,1,1))
		Evento = c1.text_area("Añadir Evento")
		Comentarios = c1.text_area("Añadir Comentarios")
		date = c1.date_input('Fecha')
		hour = c1.time_input('Hora')
		Fecha = str(date) +' '+ str(hour)
		if c1.button("Añadir",''):
			add_data_calendar(Evento,Comentarios,Fecha,now,user)
			st.experimental_rerun()
		unique_list = [i for i in view_all_task_names_calendar()]
		delete_by_task_name = c2.multiselect('Selecciona Eventos a Borrar', unique_list)
		if c2.button("Borrar"):
			for Evento in delete_by_task_name:
				deactivate_data_calendar(Evento[0],Evento[1],Evento[2])
			st.experimental_rerun()
		unique_list = [i for i in view_all_deleted_task_names_calendar()]
		delete_by_task_name = c2.multiselect('Selecciona Eventos a Reactivar', unique_list)
		if c2.button("Reactivar Borrados"):
			for Evento in delete_by_task_name:
				reactivate_data_calendar(Evento[0],Evento[1],Evento[2])
			st.experimental_rerun()
		if c3.button("Histórico"):
			historic = view_all_data_calendar()
			clean_historic_df = pd.DataFrame(historic,columns=["Evento","Comentarios","Fecha","Inscripción_Fecha",'Inscripción_User','Inscripción_ID_Actualizada',"Activo"])
			c3.dataframe(clean_historic_df)



#	if ChoiceMenu == 'Tickets2':
#		import keras_ocr
#		pipeline = keras_ocr.pipeline.Pipeline()
#
#		# Get a set of three example images
#		images = [
#			keras_ocr.tools.read(url) for url in [
#				'/home/raul/Escritorio/Proyectos Dev/test/nav/merca.jpg'
#			]
#		]
#
#		# Each list of predictions in prediction_groups is a list of
#		# (word, box) tuples.
#		prediction_groups = pipeline.recognize(images)
#
#		# Plot the predictions
#		fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
#		for ax, image, predictions in zip(axs, images, prediction_groups):
#    		keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
#
#		st.write(predictions)


#		import streamlit as st
#		from PIL import Image
#		import pytesseract
#
#		imagem = st.file_uploader("Ticket de mercadona", type=["png","jpg"])
#		if imagem:
#		    img = Image.open(imagem)
#		    texto = pytesseract.image_to_string(img, lang="spa")
#		    st.write("{}".format(texto))
#		    st.image(img, width=350)
#
#
#	if ChoiceMenu == 'Tickets':
#		import easyocr as ocr
#		import streamlit as st
#		from PIL import Image
#		import numpy as np
#		image = st.file_uploader(label= 'Ticket Mercadona')
#		@st.cache
#		def load_model():
#			reader = ocr.Reader(['es'],model_storage_directory='.')
#			return reader
#		reader = load_model()
#		if image is not None:
#			input_image = Image.open(image)
#			#Mostrar imagen
#			#st.image(input_image)
#			with st.spinner("Procesando"):
#				result = reader.readtext(np.array(input_image))
#			#st.write(result)



#			a=0
#			j=0
#			k=[]
#			len_anterior=0
#			for i in range(len(result)):
#			    if result[i][1]=='TARJETA':
#			        a=0
#			    if a==1:
#			        if (result[i][0][0][1]>=anterior-10 and result[i][0][0][1]<=anterior+10) or len_anterior==1:
#			            k[j-1]+=[result[i][1]]
#			            anterior=result[i][0][0][1]
#			            len_anterior = len(k[j-1])
#			        else:
#			            j+=1
#			            #print(j,result[i][1])
#			            k+=[[result[i][1]]]
#			            anterior=result[i][0][0][1]
#			            len_anterior = len(k[j-1]) 
#			    if result[i][1]=='Descripción':
#			        a=1
#			        anterior=result[i][0][0][1]
#			import pandas as pd
#			df = pd.DataFrame()
#			for i in range(len(k)):
#			    df.loc[i,'nombre']=k[i][0]
#			    df.loc[i,'total']=k[i][-1]
#			    if len(k[i])>=3:
#			        df.loc[i,'precio']=k[i][-2]
#			    if len(k[i])>=4:
#			        df.loc[i,'peso']=k[i][-3]
#			for i in range(df.shape[0]):
#				Articulo=df.loc[i,'nombre']
#				Total=df.loc[i,'total']
#				Precio=df.loc[i,'precio']
#				Peso=df.loc[i,'peso']
#				add_data_tickets('Mercadona',now,Articulo,Total,Precio,Peso,'1')
#			create_table_tickets()
#			result = view_active_data_tickets()
#			clean_df = pd.DataFrame(result,columns=['Supermercado','Fecha','Articulo','Total','Precio','Peso','Activo'])
#			st.dataframe(clean_df[['Supermercado','Fecha','Articulo','Total','Precio','Peso']])
#		else:			
#			create_table_tickets()
#			result = view_active_data_tickets()
#			clean_df = pd.DataFrame(result,columns=['Supermercado','Fecha','Articulo','Total','Precio','Peso','Activo'])
#			st.dataframe(clean_df[['Supermercado','Fecha','Articulo','Total','Precio','Peso']])
#
#
#		c1, c2, c3, c4, c5, c6, c7 = st.columns((1,1,1,1,1,1,1))
#		Indice = c1.number_input('Indice a modificar', min_value=0, max_value=None)
#		Supermercado = c2.text_area("Modificar supermercado")
#		Fecha = c3.text_area("Modificar Fecha")
#		Articulo = c4.text_area("Modificar Articulo")
#		Total = c5.text_area("Modificar Total")
#		Precio = c6.text_area("Modificar Precio")
#		Peso = c7.text_area("Modificar Peso")
#		st.write(Indice,Supermercado,Fecha,Articulo,Total,Precio,Peso)
#		st.write(view_index_tickets(Indice))
#		if st.button("Modificar"):
#			for Artículos in delete_by_task_name:
#				deactivate_data_tickets()
#			st.experimental_rerun()
#		if st.button("Histórico"):
#			historic = view_all_data_tickets()
#			clean_historic_df = pd.DataFrame(historic,columns=['Supermercado','Fecha','Articulo','Total','Precio','Peso','Activo'])
#			st.dataframe(clean_historic_df)



with st.sidebar.expander('Desarrollador', expanded=False):
	password2 = st.text_input("Password",'admin',type='password',key='password2') 
	if password2 == 'admin':
		if st.button("Reseteo compra"):
			c.execute('DROP TABLE compra')
			st.experimental_rerun()
		if st.button("Reseteo calendar"):
			c.execute('DROP TABLE calendar')
			st.experimental_rerun()
		if st.button("Reseteo tickets"):
			c.execute('DROP TABLE tickets')
			st.experimental_rerun()