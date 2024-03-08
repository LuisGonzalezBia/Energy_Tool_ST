#streamlit run energy_tool_main.py

# Importamos las librerías
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from pydataxm import *
#from pydataxm.pydataxm import ReadDB as apiXM
import warnings
import requests
import json
import openpyxl 

# Creación del sidebar
st.sidebar.image("logo_bia_completo.jpg")
add_sidebar = st.sidebar.selectbox('Menú principal:', ('Inicio', 
                                                       'Energy OKRs', 
                                                       'Demand Planing (Aeropuerto)', 
                                                       'Spot Price Forecaste', 
                                                       'Demand Forecast', 
                                                       'Situación de mercado',
                                                       'Consulta de información', 
                                                       'Energy Team'))

# Función para fijar el encabezado de las secciones/módulos
def header_logo(modulo1, modulo2):
    col1, col2 = st.columns(2)
    with col2:
        header = st.container()
        header.title(modulo1)
        header.title(modulo2)
        header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

        ## Custom CSS for the sticky header
        st.markdown(
            """
        <style>
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                position: sticky;
                top: 2.875rem;
                background-color: #0b0c1e;
                z-index: 999;
            }
            .fixed-header {
                border-bottom: 1px solid black;
            }
        </style>
            """,
            unsafe_allow_html=True
        )
    with col1:
        logo = st.container()
        logo.image("logo_bia_rayo.jpg", width = 20)

#  Cargar archivo ".xlsx" con la información necesaria
def load_excel(archivo, sheet_name):
    df = pd.read_excel(archivo, sheet_name=sheet_name) # Lo pasamos a formato dataframe
    return df
    
# Definición de fechas de visualización inicial
fecha_inicio = '2023-12-15'
fecha_fin = '2024-06-15'

#------------------------------------------------------------------------------------------------------------------------------Inicio
if add_sidebar == 'Inicio':
    modulo1 = 'Energy Tool'
    modulo2 = ''
    header_logo(modulo1, modulo2)
    st.text('Bienvenidos al Bia Energy Tool.')

#------------------------------------------------------------------------------------------------------------------------------Energy OKRs
elif add_sidebar == 'Energy OKRs':
    modulo1 = 'Energy Tool'
    modulo2 = 'OKRs'
    header_logo(modulo1, modulo2)

    st.text('Bienvenidos al Bia Energy Tool.')

    # OKR de competitividad
    st.title('OKR Competitividad: >8%')
    st.text('Este indicador refleja qué tan competitivos somos en tarifa.')

    # OKR de cobertura
    st.title('OKR Cobertura: >90%')
    st.text('Este indicador refleja qué tan competitivos somos en tarifa.')
    
    # OKR de venta de excedentes
    st.title('OKR Rentabilidad de Venta de Excedentes: >0%')
    st.text('Este indicador refleja la rentabilidad mínima de cada venta de excedentes.')

#------------------------------------------------------------------------------------------------------------------------------Aeropuerto
elif add_sidebar == 'Demand Planing (Aeropuerto)':
    modulo1 = 'Energy Tool'
    modulo2 = 'Aeropuerto'
    header_logo(modulo1, modulo2)
        
    archivo_aeropuerto = 'Cronograma_Activaciones_2024-03-05.xlsx' # Cambiamos la ruta porqu no pude crear una carpeta en git hub
    
    # Leemos el archivo
    df_aeropuerto = load_excel(archivo_aeropuerto, 'Aeropuerto')
    df_aeropuerto = df_aeropuerto.set_index(['Fecha'])

    st.text('En este módulo encontrarás el Aeropuerto en resolución mensual.')

    # Selección de mercado
    aeropuerto_select_box = st.selectbox('Escoge el mercado:', ('Selecciona el mercado que desees ver', 'Mercado Regulado', 'Mercado No Regulado', 'Global'))

    # Visualizaciones
    if aeropuerto_select_box == 'Mercado Regulado':    
                        
        #--------------------------------------------------------------------------------------------------------------Creación del gráfico para Mercado Regulado
        fig1 = make_subplots(rows=1, cols=1)

        # Demanda Activable
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda activable MR'], name = 'Demanda activable MR', 
                text = round(df_aeropuerto['Demanda activable MR'],1), textposition='outside', 
                textfont=dict(size=45, color="#ab63fa"), insidetextanchor = "middle", offsetgroup=0, marker_color="#ab63fa"),
            secondary_y=False, row=1, col=1)
            
        # Demanda facturada real y futura
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda facturada MR'], name = 'Demanda facturada MR', 
                text = round(df_aeropuerto['Demanda facturada MR'],1), textposition='inside', insidetextanchor = "middle",
                textfont=dict(size=40, color="white"), marker_color="#0068c9", offsetgroup=0),
            secondary_y=False, row=1, col=1)
        # Demanda por activar
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['demanda total por activar MR'], name = 'Demanda facturada x activaciones MR', 
                text = round(df_aeropuerto['demanda total por activar MR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ad4065",
                textfont=dict(size=30, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR']),
            secondary_y=False, row=1, col=1)
        # Ventas Derivex
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Ventas Derivex MR'], name = 'Ventas Derivex MR', 
                text = round(df_aeropuerto['Ventas Derivex MR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#34a853",
                textfont=dict(size=35, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['demanda total por activar MR']),
            secondary_y=False, row=1, col=1)
        # Energía disponible MR
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = -df_aeropuerto['Energía Disponible MR'], name = 'Energía disponible MR', 
                text = round(df_aeropuerto['Energía Disponible MR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ff6d01",
                textangle=0, textfont=dict(size=35, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda activable MR']),
            secondary_y=False, row=1, col=1)
        # Déficit de energía
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Deficit MR'], name = 'Deficit MR', 
                text = round(df_aeropuerto['Deficit MR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ff0000",
                textfont=dict(size=35, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda activable MR']),
            secondary_y=False, row=1, col=1)
        # Activaciones por agendar
        fig1.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Activaciones en revisión MR'], name = 'Activaciones en revisión MR', 
                text = round(df_aeropuerto['Activaciones en revisión MR'],1), textposition='inside', insidetextanchor = "middle", marker_color="Yellow",
                textangle=0, textfont=dict(size=35, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['demanda total por activar MR']),
            secondary_y=False, row=1, col=1)
            
            
        # Configuración del gráfico
        fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_color='#b6b9d3'))
        fig1.update_yaxes(title_text = '[GWh/mes]', secondary_y=False, showline=False, showgrid=True, gridwidth=1, 
                            gridcolor='#b6b9d3', color='#b6b9d3', )
        fig1.update_layout(paper_bgcolor='#0b0c1e', plot_bgcolor='#0b0c1e', autosize=False, 
                            width=950, height=500, margin=dict( l=30, r=30, b=30, t=30, pad=4), 
                            yaxis_range=[0,60],
                            xaxis_range=[fecha_inicio, fecha_fin])
        fig1.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                            range=[fecha_inicio, fecha_fin])
        fig1.update_traces(textangle=0)

        #--------------------------------------------------------------------------------------------------------------Comparativo para GMV
        fig5 = make_subplots(rows=1, cols=1)
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])

        # Demanda Límite GMV GWh MR
        fig5.add_trace(
            go.Scatter(x = df_aeropuerto.index, y = df_aeropuerto['Demanda Límite GMV GWh MR'], name = 'Límite temporal BBVA GWh MR',
                    text = round(df_aeropuerto['Demanda Límite GMV GWh MR'],1), marker_color="Green",),
            secondary_y=False, row=1, col=1)

        # Demanda GMV GWh MR
        fig5.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda GMV GWh MR'], name = 'Demanda a facturar para garantías GWh MR', 
                text = round(df_aeropuerto['Demanda GMV GWh MR'],1), marker_color="Orange",
                textangle=0, textfont=dict(size=20, color="white")), 
            secondary_y=False, row=1, col=1)
        
        # Demanda activable MR
        fig5.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda activable GWh MR qc100'], name = 'Demanda activable MR Qc=100%', 
                text = round(df_aeropuerto['Demanda activable GWh MR qc100'],1), marker_color="Purple",
                textangle=0, textfont=dict(size=20, color="White")), 
            secondary_y=False, row=1, col=1)

        # Configuración del gráfico
        fig5.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_color='#b6b9d3'))
        fig5.update_yaxes(title_text = '[GWh/mes]', secondary_y=False, showline=False, showgrid=True, gridwidth=1, 
                        gridcolor='#b6b9d3', color='#b6b9d3', )
        fig5.update_layout(paper_bgcolor='#0b0c1e', plot_bgcolor='#0b0c1e', autosize=False, 
                        width=950, height=500, margin=dict( l=50, r=30, b=30, t=30, pad=4), 
                        yaxis_range=[0,df_aeropuerto['Demanda activable MR'] + df_aeropuerto['Demanda activable MNR'].iloc[-1]+3],
                        xaxis_range=[fecha_inicio, fecha_fin])
        fig5.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                        range=[fecha_inicio, fecha_fin])

        fig5.update_yaxes(title_text="GWh/mes", range = [8,40], secondary_y=False)

        # Gráfico MR
        st.header('Gráfico de Aeropuerto Mercado Regulado') # Tercer encabezado
        st.plotly_chart(fig1, use_container_width=True) # Plot del gráfico
        # Gráfico GMV
        st.header('Limitación por garantías BBVA para el MR')
        st.text('Límite GMV MR = 3.9 MUSD')
        st.text('Límite Demanda Activable MR = 17.5 GWh/mes')
        st.plotly_chart(fig5, use_container_width=True) # Plot del gráfico GMV energía

        #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MR
        # Utilizamos el mismo archivo cargado anteriormente archivo ".xlsx" con la información en la pestaña llamada "Cronograma"
        df_leads = load_excel(archivo_aeropuerto, 'Cronograma')
        #df_leads = pd.read_excel(archivo, sheet_name='Cronograma') # Lo pasamos a formato dataframe
        estado = 'stand by: Devolver Sales'
        df_leads_revision_sales_MR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['Regulado'] == 'SI')]
        listado_leads_revision_sales_MR = df_leads_revision_sales_MR['Compañia'].unique()
        listado_leads_revision_sales_MR.sort()
        numero_leads_revision_sales_MR = len(listado_leads_revision_sales_MR)

        # Leads en revisión MR
        st.header('Leads en revisión MR: ' + str(numero_leads_revision_sales_MR)) # Segundo encabezado
        st.write('Estado(' + estado + ')')
        st.write(listado_leads_revision_sales_MR)

    elif aeropuerto_select_box == 'Mercado No Regulado':
        # Gráfico MNR
        st.header('Gráfico de Aeropuerto Mercado No Regulado') # Cuarto encabezado

        #--------------------------------------------------------------------------------------------------------------Creación del gráfico para Mercado No Regulado
        fig2 = make_subplots(rows=1, cols=1)

        # Demanda Activable
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda activable MNR'], name = 'Demanda activable MNR', 
                text = round(df_aeropuerto['Demanda activable MNR'],1), textposition='outside', 
                textfont=dict(size=45, color="#ab63fa"), insidetextanchor = "middle", offsetgroup=0, marker_color="#ab63fa"),
            secondary_y=False, row=1, col=1)
            
        # Demanda facturada real y futura
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda facturada MNR'], name = 'Demanda facturada MNR', 
                text = round(df_aeropuerto['Demanda facturada MNR'],1), textposition='inside', insidetextanchor = "middle",
                textfont=dict(size=40, color="white"), marker_color="#0068c9", offsetgroup=0),
            secondary_y=False, row=1, col=1)
        # Demanda por activar
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['demanda total por activar MNR'], name = 'Demanda facturada x activaciones MNR', 
                text = round(df_aeropuerto['demanda total por activar MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ad4065",
                textfont=dict(size=30, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MNR']),
            secondary_y=False, row=1, col=1)
        # Ventas Derivex
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Ventas Derivex MNR'], name = 'Ventas Derivex MNR', 
                text = round(df_aeropuerto['Ventas Derivex MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#34a853",
                textfont=dict(size=35, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MNR'] + df_aeropuerto['demanda total por activar MNR']),
            secondary_y=False, row=1, col=1)
        # Energía por vender MR
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = -df_aeropuerto['Energía Disponible MNR'], name = 'Energía por vender MNR', 
                text = round(df_aeropuerto['Energía Disponible MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ff6d01",
                textangle=0, textfont=dict(size=35, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda activable MNR']),
            secondary_y=False, row=1, col=1)
        # Déficit de energía
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Deficit MNR'], name = 'Deficit MNR', 
                text = round(df_aeropuerto['Deficit MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ff0000",
                textfont=dict(size=35, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda activable MNR']),
            secondary_y=False, row=1, col=1)
        # Activaciones por agendar
        fig2.add_trace(
            go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Activaciones en revisión MNR'], name = 'Activaciones en revisión MNR', 
                text = round(df_aeropuerto['Activaciones en revisión MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="Yellow",
                textangle=0, textfont=dict(size=35, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MNR'] + df_aeropuerto['demanda total por activar MNR']),
            secondary_y=False, row=1, col=1)
            
            
        # Configuración del gráfico
        fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_color='#b6b9d3'))
        fig2.update_yaxes(title_text = '[GWh/mes]', secondary_y=False, showline=False, showgrid=True, gridwidth=1, 
                            gridcolor='#b6b9d3', color='#b6b9d3', )
        fig2.update_layout(paper_bgcolor='#0b0c1e', plot_bgcolor='#0b0c1e', autosize=False, 
                            width=950, height=500, margin=dict( l=30, r=30, b=30, t=30, pad=4), 
                            yaxis_range=[0,10],
                            xaxis_range=[fecha_inicio, fecha_fin])
        fig2.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                            range=[fecha_inicio, fecha_fin])
        fig2.update_traces(textangle=0)

        #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MNR
        estado = 'stand by: Devolver Sales'
        try: 
            df_leads_revision_sales_MNR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['Regulado'] == 'NO')]
            listado_leads_revision_sales_MNR = df_leads_revision_sales_MNR['Compañia'].unique()
            listado_leads_revision_sales_MNR.sort()
        except:
            listado_leads_revision_sales_MNR = []
        numero_leads_revision_sales_MNR = len(listado_leads_revision_sales_MNR)


        # Ploteamos el gráfico
        st.plotly_chart(fig2, use_container_width=True) # Plot del gráfico

        # Leads en revisión MNR
        st.header('Leads en revisión MNR: ' + str(numero_leads_revision_sales_MNR)) # Segundo encabezado
        st.write('Estado(' + estado + ')')
        st.write(listado_leads_revision_sales_MNR)

    elif aeropuerto_select_box == 'Global':
        #--------------------------------------------------------------------------------------------------------------Creación del gráfico Global
        fig3 = make_subplots(rows=1, cols=1)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        # Demanda Activable
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda activable MR'] + df_aeropuerto['Demanda activable MNR'], name = 'Demanda activable', 
            text = round(df_aeropuerto['Demanda activable MR'] + df_aeropuerto['Demanda activable MNR'],1), textposition='outside', 
            textfont=dict(size=35, color="#ab63fa"), insidetextanchor = "middle", offsetgroup=0, marker_color="#ab63fa"),
        secondary_y=False, row=1, col=1)

        # Demanda facturada real y futura
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['Demanda facturada MNR'], name = 'Demanda facturada', 
            text = round(df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['Demanda facturada MNR'],1), textposition='inside', insidetextanchor = "middle",
            textfont=dict(size=30, color="white"), marker_color="#0068c9", offsetgroup=0),
        secondary_y=False, row=1, col=1)
        # Demanda por activar
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['demanda total por activar MR'] + df_aeropuerto['demanda total por activar MNR'], name = 'Demanda facturada x activaciones', 
            text = round(df_aeropuerto['demanda total por activar MR'] + df_aeropuerto['demanda total por activar MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ad4065",
            textfont=dict(size=25, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['Demanda facturada MNR']),
        secondary_y=False, row=1, col=1)
        # Ventas Derivex
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Ventas Derivex MR'] + df_aeropuerto['Ventas Derivex MNR'], name = 'Ventas Derivex', 
            text = round(df_aeropuerto['Ventas Derivex MR'] + df_aeropuerto['Ventas Derivex MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#34a853",
            textfont=dict(size=30, color="white"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['demanda total por activar MR'] + df_aeropuerto['Demanda facturada MNR'] + df_aeropuerto['demanda total por activar MNR']),
        secondary_y=False, row=1, col=1)
        
        # Energía por vender MR
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = -df_aeropuerto['Energía Disponible MR']-df_aeropuerto['Energía Disponible MNR'], name = 'Energía disponible', 
            text = round(df_aeropuerto['Energía Disponible MR'] + df_aeropuerto['Energía Disponible MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="#ff6d01",
            textangle=0, textfont=dict(size=30, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda activable MR'] + df_aeropuerto['Demanda activable MNR']),
        secondary_y=False, row=1, col=1)

        # Activaciones en revisión
        fig3.add_trace(
        go.Bar(x = df_aeropuerto.index, y = df_aeropuerto['Activaciones en revisión MR'] + df_aeropuerto['Activaciones en revisión MNR'], name = 'Activaciones en revisión', 
            text = round(df_aeropuerto['Activaciones en revisión MR'] + df_aeropuerto['Activaciones en revisión MNR'],1), textposition='inside', insidetextanchor = "middle", marker_color="Yellow",
            textangle=0, textfont=dict(size=30, color="black"), offsetgroup=0, base=df_aeropuerto['Demanda facturada MR'] + df_aeropuerto['demanda total por activar MR'] + df_aeropuerto['Demanda facturada MNR'] + df_aeropuerto['demanda total por activar MNR']),
        secondary_y=False, row=1, col=1)
        
        # Arreglamos la horientación 
        fig3.update_traces(textangle=0)

        # Firmados inorganico
        fig3.add_trace(
        go.Scatter(x = df_aeropuerto.index, y = df_aeropuerto['Firmados inorganico'], name = 'Inorganico', fill='tozeroy',
            text = round(df_aeropuerto['Firmados inorganico'],1), marker_color="Gray", opacity=0.1,
            textfont=dict(size=35, color="black")),
        secondary_y=True, row=1, col=1)

        # Firmados Sales
        fig3.add_trace(
        go.Scatter(x = df_aeropuerto.index, y = df_aeropuerto['Firmados Sales'], name = 'Firmados', fill='tonexty',
            text = round(df_aeropuerto['Firmados Sales'],1), marker_color="Green", opacity=0.1,
            textfont=dict(size=35, color="black")),
        secondary_y=True, row=1, col=1)


        # Configuración del gráfico
        fig3.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_color='#b6b9d3'))
        fig3.update_yaxes(title_text = '[GWh/mes]', secondary_y=False, showline=False, showgrid=True, gridwidth=1, 
                        gridcolor='#b6b9d3', color='#b6b9d3', )
        fig3.update_layout(paper_bgcolor='#0b0c1e', plot_bgcolor='#0b0c1e', autosize=False, 
                        width=950, height=500, margin=dict( l=30, r=30, b=30, t=30, pad=4), 
                        yaxis_range=[0,df_aeropuerto['Demanda activable MR'] + df_aeropuerto['Demanda activable MNR'].iloc[-1]+3],
                        xaxis_range=[fecha_inicio, fecha_fin])
        fig3.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                        range=[fecha_inicio, fecha_fin])
        fig3.update_yaxes(range = [0,60])

        # Gráfico Global
        st.header('Gráfico de Aeropuerto MR y MNR') # Cuarto encabezado
        st.plotly_chart(fig3, use_container_width=True) # Plot del gráfico global

        #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MR
        # Utilizamos el mismo archivo cargado anteriormente archivo ".xlsx" con la información en la pestaña llamada "Cronograma"
        #df_leads = pd.read_excel(archivo, sheet_name='Cronograma') # Lo pasamos a formato dataframe
        df_leads = load_excel(archivo_aeropuerto, 'Cronograma')
        estado = 'stand by: Devolver Sales'
        df_leads_revision_sales_MR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['Regulado'] == 'SI')]
        listado_leads_revision_sales_MR = df_leads_revision_sales_MR['Compañia'].unique()
        listado_leads_revision_sales_MR.sort()
        numero_leads_revision_sales_MR = len(listado_leads_revision_sales_MR)

        #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MNR
        estado = 'stand by: Devolver Sales'
        try: 
            df_leads_revision_sales_MNR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['Regulado'] == 'NO')]
            listado_leads_revision_sales_MNR = df_leads_revision_sales_MNR['Compañia'].unique()
            listado_leads_revision_sales_MNR.sort()
        except:
            listado_leads_revision_sales_MNR = []
        numero_leads_revision_sales_MNR = len(listado_leads_revision_sales_MNR)


        # Leads en revisión MNR
        st.header('Leads en revisión MR y MNR: ' + str(numero_leads_revision_sales_MR + numero_leads_revision_sales_MNR)) # Segundo encabezado
        st.write('Estado(' + estado + ')')
        try: st.write(listado_leads_revision_sales_MR + listado_leads_revision_sales_MNR)
        except: st.write(listado_leads_revision_sales_MR)

        # Crearemos el botón de descarga
        # Función para convertir a csv el dataframe
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        # Convertimos en csv el dataframe de aeropuerto
        aeropuerto_exportable = convert_df(df_aeropuerto)

        # Creamos el botón de descarga
        st.download_button(
            label="Descarga un .csv con los datos de Aeropuerto.",
            data=aeropuerto_exportable,
            file_name='aeropuerto.csv',
            mime='text/csv',
        )

#------------------------------------------------------------------------------------------------------------------------------Spot Price Digital Twin
elif add_sidebar == 'Spot Price Forecaste':
    modulo1 = 'Energy Tool'
    modulo2 = 'SP Forecaste'
    header_logo(modulo1, modulo2)

    archivo = 'precio_bolsa_2024_03_05.xlsx' # Cambiamos la ruta porqu no pude crear una carpeta en git hub

    # Leemos el archivo
    df_precio_bolsa = load_excel(archivo, sheet_name='precio_bolsa')
    df_precio_bolsa = df_precio_bolsa.set_index(['Fecha'])

    # Definición de fechas de visualización inicial
    fecha_inicio = '2023-12-30'
    fecha_fin = '2024-07-31'
    #--------------------------------------------------------------------------------------------------------------Creación del gráfico Global
    fig4 = make_subplots(rows=1, cols=1)
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    # Pronóstico ENERSINC min
    fig4.add_trace(
        go.Scatter(x = df_precio_bolsa.index, y = df_precio_bolsa['Forecast min'], name = 'Bia B1 min', fill = None, mode='lines'),
        secondary_y=False, row=1, col=1)
    # Pronóstico ENERSINC max
    fig4.add_trace(
        go.Scatter(x = df_precio_bolsa.index, y = df_precio_bolsa['Forecast max'], name = 'Bia B1 max', fill='tonexty', mode='lines'),
        secondary_y=False, row=1, col=1)
    # Pronóstico ENERSINC ave
    fig4.add_trace(
        go.Scatter(x = df_precio_bolsa.index, y = df_precio_bolsa['Forecast esperado'], name = 'Forecast esperado'),
        secondary_y=False, row=1, col=1)
    # Pronóstico BIA B1
    fig4.add_trace(
        go.Scatter(x = df_precio_bolsa.index, y = df_precio_bolsa['Forecast esperado ponderado'], name = 'Forecast esperado ponderado'),
        secondary_y=False, row=1, col=1)
    # # Pronóstico REAL
    fig4.add_trace(
        go.Scatter(x = df_precio_bolsa.index, y = df_precio_bolsa['Precio Bolsa Nacional'], name = 'Real'),
        secondary_y=False, row=1, col=1)
    
    # Configuración del gráfico
    fig4.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_color='#b6b9d3'))
    fig4.update_yaxes(title_text = '$/KWh]', secondary_y=False, showline=False, showgrid=True, gridwidth=1, 
                    gridcolor='#b6b9d3', color='#b6b9d3', )
    fig4.update_layout(paper_bgcolor='#0b0c1e', plot_bgcolor='#0b0c1e', autosize=True, 
                    width=950, height=500, margin=dict( l=30, r=30, b=30, t=30, pad=4),
                    xaxis_range=[fecha_inicio, fecha_fin])
    fig4.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3')
    
    st.text('Pronóstico de precio de bolsa.')
    # Ploteamos el gráfico
    st.plotly_chart(fig4, use_container_width=True) # Plot del gráfico
    st.text('El modelo Bia B1 se corrió el 15/02/2024.')
    st.text('El modelo ENERSINC se corrió en noviembre del 2023.')
    st.text('Gemelo digital actualmente en desarrollo.')

#------------------------------------------------------------------------------------------------------------------------------Demand Forecast
elif add_sidebar == 'Demand Forecast':
    modulo1 = 'Energy Tool'
    modulo2 = 'Demand Forecast'
    header_logo(modulo1, modulo2)

    #st.title('Demand Forecast')
    st.text('En este módulo encontrarás la proyección de demanda.')
    st.text('Actualmente en desarrollo.')

#------------------------------------------------------------------------------------------------------------------------------Demand Forecast
elif add_sidebar == 'Situación de mercado':
    modulo1 = 'Energy Tool'
    modulo2 = 'Situación lde mercado'
    header_logo(modulo1, modulo2)
    #st.text('Demanda y precio de bolsa')
    # Ploteamos el gráfico
    #st.plotly_chart(fig1, use_container_width=True) # Plot del gráfico
    st.text('Actualmente en desarrollo.')

#------------------------------------------------------------------------------------------------------------------------------Consulta de información
elif add_sidebar == 'Consulta de información':
    modulo1 = 'Energy Tool'
    modulo2 = 'Consulta de información'
    header_logo(modulo1, modulo2)
    #st.text('En este módulo podrás descargar información.')
    
    descargas_select_box = st.selectbox('Qué consulta deseas hacer:', ('Escoge aquí', 'Proyección de MC'))

    # Visualizaciones
    if descargas_select_box == 'Proyección de MC':    
        # Gráfico MR
        st.text('Fuente: SIMEM')
        
        
        datasetId_mr = '48e773' # Precio promedio ponderado MR https://www.simem.co/datadetail/48E773BD-2117-40C5-829E-1DE05D51378E
        url_simem = 'https://www.simem.co/backend-files/api/PublicData?'

        # Creamos una función para interrogar SIMEM
        def request_mc(ini, fin):
            url_request_mr = url_simem + 'startdate=' + ini + '&enddate=' + fin + '&datasetId=' + datasetId_mr
            # Request
            response_mr = requests.get(url_request_mr)
            # Extracción de datos del json original a formato dataframe para MR
            json_request_mr = response_mr.json()
            df_request_mr = pd.DataFrame.from_dict(json_request_mr) # Transformamos a dataframe el json original
            dict_records_mr = df_request_mr.loc['records']['result'] # Buscamos los resultados en formato dict
            df_records_mr = pd.DataFrame.from_dict(dict_records_mr) # Buscamos los resultados y los transformamos a dataframe
            df_ppp_mr_3 = df_records_mr[['FechaPublicacion', 'FechaProyectada', 'PPP']] # Nos quedamos con las columnas que queremos
            return df_ppp_mr_3
        
        # Parámetros de la consulta
        fecha_inicio = ['2024-01-01', '2026-01-01', '2028-01-01']
        fecha_fin = ['2025-12-31', '2027-12-01', '2029-12-01']

        # Realizamos las tres consultas
        request1 = request_mc(fecha_inicio[0], fecha_fin[0])
        request2 = request_mc(fecha_inicio[1], fecha_fin[1])
        request3 = request_mc(fecha_inicio[2], fecha_fin[2])

        # Concatenamos las tres consultas
        mc_completo = pd.concat([request1, request2, request3])
        # Cambiamos el formato de las columnas de fecha
        mc_completo['FechaPublicacion'] = pd.to_datetime(mc_completo['FechaPublicacion'])
        mc_completo['FechaProyectada'] = pd.to_datetime(mc_completo['FechaProyectada'])

        # Definimos las fechas de las que tenemos proyecciones
        fechas_proyeccion = mc_completo['FechaProyectada'].unique()
        # Definimos las columnas que tendrá en nuevo dataframe
        variables = ['fecha', 'fecha_actualización', 'MC']
        # Creación de dataframe en ceros
        zero_data = np.zeros(shape=(len(fechas_proyeccion), len(variables)))
        mc_final = pd.DataFrame(zero_data, columns = variables) # Tarifas BIA
        # Traemos las fechas al dataframe
        mc_final['fecha'] = fechas_proyeccion
        # Ordenamos por fechas
        mc_final = mc_final.sort_values(by = ['fecha'])
        # Seleccionamos la fecha como indice
        mc_final = mc_final.set_index('fecha')

        # Recorramos el nuevo dataframe
        # Recorramos el nuevo dataframe
        for f in range(0, len(fechas_proyeccion)):
            # Seleccionamos la fecha a trabajar
            fecha = fechas_proyeccion[f]
            # Nos traemos el dato más actualizado
            mc = mc_completo[mc_completo['FechaProyectada'] == fecha].sort_values(by = ['FechaPublicacion']).iloc[-1]['PPP']
            fecha_actualizacion = mc_completo[mc_completo['FechaProyectada'] == fecha]['FechaPublicacion'].max()
            mc_final.loc[fecha] = fecha_actualizacion, mc 

        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        
        # Transformamos el dataframe a csv
        mc_exportable = convert_df(mc_final)

        # Buscamos la fecha de actualización
        fecha_actualizacion = mc_completo.FechaPublicacion.max()
        st.text('Última fecha de actualización: ' + str(fecha_actualizacion))

        # Creamos el botón de descarga
        st.download_button(
            label="Descargar el archivo",
            data=mc_exportable,
            file_name='mc.csv',
            mime='text/csv',
        )
  
#------------------------------------------------------------------------------------------------------------------------------Energy Team
elif add_sidebar == 'Energy Team':
    modulo1 = 'Energy Tool'
    modulo2 = 'Team'
    header_logo(modulo1, modulo2)


    #st.title('Energy Team')
    st.image('guillermo_cajamarca.png', caption='VP of Energy: Guillermo Cajamarca', width=200)
    st.image('nohora_mesa.jpg', caption='Head of Energy Trading: Nohora Mesa', width=200)
    st.image('juliana_bonilla.jpg', caption='Energy Trading Analyst: Juliana Bonilla', width=200)
    st.image('luis_gonzalez.png', caption='Energy Data Analyst: Luis González', width=200)    
