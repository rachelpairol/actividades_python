
import pandas as pd

df3 = pd.read_excel ('Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0 )
# print(df3.head(5))


tabla2 =  df3.to_numpy()
#print(tabla2) 