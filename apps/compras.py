import streamlit as st
from hydralit import HydraHeadApp
import pytz
from datetime import datetime
from db_fxns import * 
import pandas as pd 
import os

class compras(HydraHeadApp):
    def __init__(self, title = 'Hydralit Explorer', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    def run(self):
        try:
            timezone = pytz.timezone("Europe/Madrid")
            now = str(datetime.now().astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"))
            now_time = datetime.now().astimezone(timezone)

            user=st.session_state['user']

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
                    st.experimental_rerun()
            st.markdown("---")
            c1, c2 = st.columns((1,1))
            historic = view_all_data_compra()
            clean_historic_df = pd.DataFrame(historic,columns=["Artículo","Descripción","Número","Inscripción_Fecha",'Inscripción_User','Modificación_Fecha','Modificación_User',"Activo"])
            if c1.button("Histórico"):
                c1.dataframe(clean_historic_df)
            c2.download_button(label="Descargar CSV",data=clean_historic_df.to_csv().encode('utf-8'), file_name='Compras_historico.csv', mime='text/csv', )

        except Exception as e:
            st.image(os.path.join(".","/home/raul/Escritorio/Proyectos Dev/App Alvaro/hydralit-example-main/resources","failure.png"),width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))