#streamlit run c:/Users/User/Desktop/Aeropuerto/Aeropuerto_web_page/aeropuerto_web_page_3_ux.py
#streamlit run aeropuerto_web_page_3_ux.py

# Importamos las lipbrerías
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import openpyxl 

st.title('Energy Tool')

add_sidebar = st.sidebar.selectbox('Escoge el modelo:', ('Demand Planing (Aeropuerto)', 'Spot Price Forecaste', 'Demand Forecast'))
if add_sidebar == 'Demand Planing (Aeropuerto)':
    #archivo = 'data\Aeropuerto\Cronograma de Activaciones 2024-01-26.xlsx'
    archivo = 'Cronograma de Activaciones 2024-01-26.xlsx' # Cambiamos la ruta porqu no pude crear una carpeta en git hub
    #archivo = 's3://bia-bucket-public/Energy/Cronograma de Activaciones 2024-01-26.xlsx' #pruebak de conexión a S3
    #  Cargar archivo ".xlsx" con la información en la pestaña llamada "Aeropuerto"
    def load_aeropuerto():
        df_aeropuerto = pd.read_excel(archivo, sheet_name='Aeropuerto') # Lo pasamos a formato dataframe
        df_aeropuerto = df_aeropuerto.set_index(['Fecha'])
        return df_aeropuerto

    df_aeropuerto = load_aeropuerto()

    st.title('Demand Planing (Aeropuerto)')
    st.text('En este módulo encontrarás el Aeropuerto en resolución mensual.')

    # Fechas a visualizar
    fecha_inicio = '2023-12-15'
    fecha_fin = '2024-06-15'

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
    # Energía por vender MR
    fig1.add_trace(
        go.Bar(x = df_aeropuerto.index, y = -df_aeropuerto['Energía Disponible MR'], name = 'Energía por vender MR', 
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
                        yaxis_range=[0,df_aeropuerto['Demanda activable MR'].iloc[-1]+3],
                        xaxis_range=[fecha_inicio, fecha_fin])
    fig1.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                        range=[fecha_inicio, fecha_fin])
    fig1.update_traces(textangle=0)


    #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MR
    # Utilizamos el mismo archivo cargado anteriormente archivo ".xlsx" con la información en la pestaña llamada "Cronograma"
    df_leads = pd.read_excel(archivo, sheet_name='Cronograma') # Lo pasamos a formato dataframe
    estado = 'stand by: Devolver Sales'
    df_leads_revision_sales_MR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['TIPO MERCADO'] == 'SI')]
    listado_leads_revision_sales_MR = df_leads_revision_sales_MR['Compañia'].unique()
    listado_leads_revision_sales_MR.sort()
    numero_leads_revision_sales_MR = len(listado_leads_revision_sales_MR)


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
                        yaxis_range=[0,df_aeropuerto['Demanda activable MNR'].iloc[-1]+3],
                        xaxis_range=[fecha_inicio, fecha_fin])
    fig2.update_xaxes(title_text= '', showgrid=True, gridwidth=1, gridcolor='#0b0c1e', color='#b6b9d3',
                        range=[fecha_inicio, fecha_fin])
    fig2.update_traces(textangle=0)

    #--------------------------------------------------------------------------------------------------------------Desagregación leads de activaciones en revisión MR
    # Utilizamos el mismo archivo cargado anteriormente archivo ".xlsx" con la información en la pestaña llamada "Cronograma"
    #df_leads = pd.read_excel('Cronograma de Activaciones 2024-01-26.xlsx', sheet_name='Cronograma') # Lo pasamos a formato dataframe
    estado = 'stand by: Devolver Sales'
    try: 
        df_leads_revision_sales_MNR = df_leads[(df_leads['Validación aeropuerto'] == estado) & (df_leads['TIPO MERCADO'] == 'NO')]
        listado_leads_revision_sales_MNR = df_leads_revision_sales_MNR['Compañia'].unique()
        listado_leads_revision_sales_MNR.sort()
    except:
        listado_leads_revision_sales_MNR = []
    numero_leads_revision_sales_MNR = len(listado_leads_revision_sales_MNR)


    aeropuerto_select_box = st.selectbox('Escoge el mercado:', ('Mercado Regulado', 'Mercado No Regulado', 'Total'))

    # Visualizaciones
    if aeropuerto_select_box == 'Mercado Regulado':    
        # Gráfico MR
        st.header('Gráfico de Aeropuerto Mercado Regulado') # Tercer encabezado
        st.plotly_chart(fig1, use_container_width=False) # Plot del gráfico

        # Leads en revisión MR
        st.header('Leads en revisión MR: ' + str(numero_leads_revision_sales_MR)) # Segundo encabezado
        st.write('Estado: ' + estado + ')')
        st.write(listado_leads_revision_sales_MR)

    elif aeropuerto_select_box == 'Mercado No Regulado':
        # Gráfico MNR
        st.header('Gráfico de Aeropuerto Mercado No Regulado') # Cuarto encabezado
        st.plotly_chart(fig2, use_container_width=False) # Plot del gráfico

        # Leads en revisión MNR
        st.header('Leads en revisión MNR: ' + str(numero_leads_revision_sales_MNR)) # Segundo encabezado
        st.write('Estado: ' + estado + ')')
        st.write(listado_leads_revision_sales_MNR)


#------------------------------------------------------------------------------------------------------------------------------Spot Price Digital Twin
elif add_sidebar == 'Spot Price Forecaste':
    st.title('Spot Price Forecast - Ideal Dispatch Digital Twin')
    st.text('En este módulo encontrarás el gemelo digital del despacho ideal.')
    st.text('Actualmente en desarrollo.')


#------------------------------------------------------------------------------------------------------------------------------Spot Price Digital Twin
elif add_sidebar == 'Spot Price Forecaste':
    st.title('Demand Forecast')
    st.text('En este módulo encontrarás la proyección de demanda.')
    st.text('Actualmente en desarrollo.')
    'Demand Planing (Aeropuerto)', 'Spot Proce Digital Twin', 'Demand Forecast'
