import streamlit as st
from hydralit import HydraHeadApp
import pytz
from datetime import datetime
import pandas as pd 
from db_fxns import * 
import os

class calendario(HydraHeadApp):
    def __init__(self, title = 'calendario', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    def run(self):
        try:
            timezone = pytz.timezone("Europe/Madrid")
            now = str(datetime.now().astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"))
            now_time = datetime.now().astimezone(timezone)

            user=st.session_state['user']

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
                hour = st.time_input('Hora',value=now_time)
                Fecha = str(date) +' '+ str(hour)
                if st.button("Añadir",''):
                    add_data_calendar(Evento,Comentarios,Fecha,now,user)
                    st.experimental_rerun()
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
        except Exception as e:
            st.image(os.path.join(".","/home/raul/Escritorio/Proyectos Dev/App Alvaro/hydralit-example-main/resources","failure.png"),width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))