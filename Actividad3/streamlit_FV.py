# -*- coding: utf-8 -*-

import datetime  # Para especificación de fechas y horas
from io import BytesIO  # Se utiliza para ajustar mejor la resolución de los gráficos con matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px  # Para crear una figura de Plotly (en lugar de usar Matplotlib)
from Generador_FV_Streamlit import Generador_FV  # Archivo generado en clase

import pandas as pd
import numpy as np
df=pd.read_excel('Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)
#------------------------------------------------------------------------------------------------------------------------
# Creo panel lateral (sidebar) para configurar los parámetros del generador (N, Ppico, kp, eta)...
with st.sidebar:
    st.title('Parámetros de la instalación')  # Una forma de crear un título principal

    col1, col2 = st.columns(2)  # Genero 2 columnas
    with col1:
        # Campo de entrada numérica:
        N = st.number_input('Cantidad de módulos fotovoltaicos', min_value=10, max_value=100, value=12, step=1)

    with col2:
        # Slider con opciones prefijadas (select slider):
        Ppico = st.select_slider('Potencia pico por módulo (W)', [160, 180, 200, 240, 260, 320], value=240)

    # Fuera de las columnas, por razones de espacio...
    kp = st.number_input('Coef. de potencia-temperatura (1/°C)', min_value=-0.0070, max_value=-0.0010,
                        value=-0.0044, step=0.0001, format='%f')  # la especificación de formato es importante
                                                                  # cuando el número es tipo float
                                                                  # (caso contrario, se asumen tipo int)
                                                                  #
                                                                  # Esto es lo que me falló durante la clase :)
    eta = st.slider('Rendimiento global de la instalación', min_value=0.6, max_value=1.,
                value=0.97, step=0.01)


#------------------------------------------------------------------------------------------------------------------------
"""
# Modelo Simplificado de un Generador Fotovoltaico

Se utiliza el siguiente modelo de un GFV para estimar la potencia eléctrica producida:

$ P\, [kW] = N \cdot P_{\mathit{pico}} \cdot \cfrac{G}{G_{std}} \cdot [ 1 + k_p \cdot (T - T_r) ] \cdot \eta \cdot 10^{-3} $

donde:
- $ P $: Potencia eléctrica entregada.
- $ N $: Cantidad de módulos de la instalación.
- $ G $: Irradiancia global incicidente de forma normal sobre los paneles, en $ W/m^2 $.
- $ G_{std} $: Irradiancia estándar ($ 1000\, W/m^2 $).
- $ k_p $: Coeficiente de potencia-temperatura, en _Celsius_.
- $ T $: Temperatura de los paneles, en _Celsius_.
- $ T_r $: Temperatura de referencia ($ 25 $ _Celsius_).
- $ \eta $: Rendimiento global de la instalación (adimensional, entre 0 y 1).
"""

#------------------------------------------------------------------------------------------------------------------------
st.write('## Cálculos')  # Subtítulo (título de 2do nivel)

# Instancia de Generador_Fotovoltaico (archivo generado en clase)
gen = Generador_FV(df, N, Ppico, kp, eta)

# Formulario HTML: Conjunto de campos con un botón de acción
with st.form('Ejemplo conocer irradiancia y temperatura para un instante'):
    st.write('__Conocer Irradiancia y Temperatura para un día e instante determinado__')

   
    col7, col8, col9 = st.columns(3)
    with col7:
        # Widget de calendario:
        dia = st.date_input('Fecha', value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1),
                    max_value=datetime.date(2019, 12, 31))
    with col8:
        h = st.selectbox('Hora', range(24), index=00)
    with col9:
        mi = st.selectbox('Minuto', range(0, 60, 10))

        
        
        d= dia.strftime('%d')
        m= dia.strftime('%m')
        a= dia.strftime('%Y')


    # Botón de acción del formulario:
    boton_calcular = st.form_submit_button('Calcular')
    if boton_calcular:
        irr_temp=gen.irrad_temp(d, m, a, h, mi)
        st.success(f'Irradiancia {irr_temp[0]} $W/m^2$ y Temperatura: {irr_temp[1]} $°C$')  # Mensaje emergente

#-------------------------------------------------------------------------------------------------------------------------

with st.form('Ejemplo conocer irradiancia y temperatura para un rango de fechas'):
    st.write('__Conocer Irradiancia y Temperatura para un rango de fechas determinadas__')

   
    col7, col8, col9 = st.columns(3)
    with col7:
        # Widget de calendario:
        fecha1 = st.date_input('Fecha Inicio', value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1),
                    max_value=datetime.date(2019, 12, 31))
        fecha2 = st.date_input('Fecha Fin', value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1),
                    max_value=datetime.date(2019, 12, 31))
    with col8:
        h1 = st.selectbox('Hora inicio', range(24), index=00)
        h2 = st.selectbox('Hora  fin', range(24), index=00)
    with col9:
        mi1 = st.selectbox('Minuto inicio', range(0, 60, 10))
        mi2 = st.selectbox('Minuto fin', range(0, 60, 10))
        
        d= fecha1.strftime('%d')
        m= fecha1.strftime('%m')
        a= fecha1.strftime('%Y')

        d1= fecha2.strftime('%d')
        m1= fecha2.strftime('%m')
        a1= fecha2.strftime('%Y')

        tupla1=(d,m,a,h1,mi1)
        tupla2=(d1,m1,a1,h2,mi2)

    # Botón de acción del formulario:
    boton_calcular = st.form_submit_button('Calcular')
    if boton_calcular:
        st.table(gen.irrad_temp_rango(tupla1,tupla2))
        
        
#------------------------------------------------------------------------------------------------------------------------
with st.form('Ejemplo calcular potencia generada para una fecha'):
    st.write('__Potencia generada para una fecha determinada__')

   
    col7, col8, col9 = st.columns(3)
    with col7:
        # Widget de calendario:
        fecha1 = st.date_input('Fecha Inicio', value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1),
                    max_value=datetime.date(2019, 12, 31))
    with col8:
        h1 = st.selectbox('Hora inicio', range(24), index=00)
       
    with col9:
        mi1 = st.selectbox('Minuto inicio', range(0, 60, 10))
        
        d= fecha1.strftime('%d')
        m= fecha1.strftime('%m')
        a= fecha1.strftime('%Y')

        tupla1=(d,m,a,h1,mi1)
       

    # Botón de acción del formulario:
    boton_calcular = st.form_submit_button('Calcular')
    if boton_calcular:
        st.success(gen.pot_generada(tupla1))
#----------------------------------------------------------------------------------------------------------------------------------

with st.form('Calcular potencia media para un mes'):
    st.write('__Calcular la potencia media y la energia entregada para un mes__')

    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")

    m = st.selectbox('Seleccione un mes', months)
    month = months.index(m)
   
# Botón de acción del formulario:
    
    boton_calcular = st.form_submit_button('Calcular')
    if boton_calcular:
        potencia=gen.pot_media_mes(format((month+1),'02d'))
        energia=gen.energia_mes(format((month+1),'02d'))
        st.success((f'La potencia media es: {potencia:.3f} (kW) y la energia entregada es: ' f'{energia:.3f} (KWh)'))

    st.write('__Calcular la potencia y energia anual__')

    boton_calcular1 = st.form_submit_button('Calcular PotenciaEnergía')
    if boton_calcular1:
        potenciaanual=gen.pot_media_anual()
        energiaanual=gen.energia_anual()
        st.success((f'La potencia media anual es: {potenciaanual:.3f} (kW) y la energía anual es: ' f'{energiaanual:.3f} (KWh)'))

#------------------------------------------------------------------------------------------------------------------------------------------
with st.form('Graficar energía mensual'):
    st.write('__Graficar energía mensual__')

    
# Botón de acción del formulario:
    
    boton_calcular = st.form_submit_button('Graficar')
    if boton_calcular:
        f=gen.graficar_energia_mensual()
        st.bar_chart(f)



# st.write('## Ejemplo de cálculo con una tabla de valores')

# # Datos de ejemplo en un diccionario
# datos = {'G (W/m2)': [1200, 800, 750, 900, 950, 1100, 1300, 1000, 992],
#     'T (°C)': [25.3, 23.1, 20, 19.2, 22.3, 24, 26.1, 21.8, 18.6]}

# df = pd.DataFrame(datos)  # Genero un DataFrame a partir del diccinario
# df.index.name = 'Registro'
# potencias = gen.generado(df['G (W/m2)'], df['T (°C)'])
# df['P (kW)'] = potencias  # Agrego columna de potencias

# col3, col4 = st.columns(2)
# with col3:
#     st.write('#### Datos y potencias calculadas')  # Título de 3er nivel
#     st.dataframe(df)  # Muestro el DataFrame
# with col4:
#     st.write('#### Resumen estadístico')  # Título de 3er nivel
#     st.dataframe(df.describe(), width=600)  # Ajusto ancho


# #------------------------------------------------------------------------------------------------------------------------
# st.write('## Gráficos')
# st.write('### Gráfico sencillo con Matplotlib (sin ajustes de resolución)')

# f, ax = plt.subplots()  # Obtengo figura y axes

# df.plot.scatter(x='G (W/m2)', y='P (kW)', title='Potencia VS Irradiancia', label='Calculado', ax=ax)

# # Recta de ajuste lineal por mínimos cuadrados: Grafico sobre el axes anterior
# coefs_polinomio = np.polyfit(df['G (W/m2)'], df['P (kW)'], 1)  # Ajuste lineal
# G_barrido = np.linspace(df['G (W/m2)'].min(), df['G (W/m2)'].max(), 300)  # 300 puntos de irradiancia entre el mín. y el máx.
# P_barrido_pol = np.polyval(coefs_polinomio, G_barrido)  # Ordenadas de la recta de ajuste
# ax.plot(G_barrido, P_barrido_pol, lw=1, c='r', label='Ajuste lineal')
# ax.grid()
# ax.legend()
# f  # Muestro figura


# st.write('### Gráfico con ajustes de resolución')

# buf = BytesIO()  # Buffer para almacenar el contenido de una imagen
# f2, ax2 = plt.subplots(figsize=(8, 4))  # figsize: Ancho y alto de la figura en pulgadas
# df.plot.scatter(x='G (W/m2)', y='P (kW)', title='Potencia VS Irradiancia', label='Calculado', ax=ax2)
# ax2.plot(G_barrido, P_barrido_pol, lw=1, c='r', label='Ajuste lineal')
# ax2.grid()
# ax2.legend()
# f2.savefig(buf, format='png', dpi=150)  # Guardo la imagen en el buffer (dpi: pixeles por pulgada)
# st.image(buf)  # Muestro buffer como si de una imagen se tratase


# st.write('### Gráficos con el paquete Vega Lite')
# col5, col6 = st.columns(2)
# with col5:
#     st.line_chart(df['P (kW)'])
# with col6:
#     st.bar_chart(df['P (kW)'])


# st.write('### Gráficos con el paquete Plotly')
# f3 = px.scatter(df, x='G (W/m2)', y='P (kW)', title='Potencia VS Irradiancia')
# st.plotly_chart(f3)

# f4 = px.bar(df, y='P (kW)', title='Potencia por registro')
# st.plotly_chart(f4)


# #------------------------------------------------------------------------------------------------------------------------
# st.write('## Datos climatológicos desde un archivo')

# arch = st.file_uploader('Subir archivo de datos (ej.: Datos_climatologicos_Santa_Fe_2019.xlsx)', type='xlsx')
# if arch is not None:
#     tabla_arch = pd.read_excel(arch, index_col=0)
#     tabla_arch['Potencia (kW)'] = gen.generado(tabla_arch['Irradiancia (W/m²)'], tabla_arch['Temperatura (°C)'])
#     tabla_1000 = tabla_arch.head(1000)

#     st.write('#### Primeras 1000 filas')

#     st.dataframe(tabla_1000, width=700)

#     # Grafico potencias con Plotly:
#     f5 = px.line(tabla_1000, y=tabla_1000['Potencia (kW)'])
#     st.plotly_chart(f5)


# #------------------------------------------------------------------------------------------------------------------------
# st.write('### Cálculo para un día y horario específico')

# col7, col8, col9 = st.columns(3)
# with col7:
#     # Widget de calendario:
#     dia = st.date_input('Día', value=datetime.date(2019, 4, 14), min_value=datetime.date(2019, 1, 1),
#                 max_value=datetime.date(2019, 12, 31))
# with col8:
#     hora = st.selectbox('Hora', range(24), index=11)
# with col9:
#     minuto = st.selectbox('Minuto', range(0, 60, 10))

# instante = f'{str(dia)} {hora}:{minuto}' # Año-Mes-Día Hora:Minuto (en formato tipo str)

# if arch is not None:
#     st.dataframe(tabla_arch.loc[instante, :])
# else:
#     st.error('Subir archivo para proceder con los cálculos')  # Mensaje emergente de error
