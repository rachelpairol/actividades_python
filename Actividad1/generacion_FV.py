# -*- coding: utf-8 -*-
from datos import tabla
from fechas import datos2
from matplotlib import use
import matplotlib.pyplot as plt
use ('Qt5Agg')

meses=['01','02','03','03','04','05','07','08','09','10','11','12']
fecha=''
def irrad_temp(d, m, a, h, mi):

    fecha ='%s/%s/%s %s:%s' %(d, m, a, h, mi)
    print('ESTA ES LA FECHA',fecha)
    #for i in datos2:
    if (fecha not in datos2):
        print('NO HAY MEDICIONES PARA LA FECHA INGRESADA O LA FECHA ES INCORRECTA')
    else:
        global indice
        indice= datos2.index(fecha)
        print ('Este es el indice', indice)
        print ('Esta es la irradiancia', tabla[indice])

def irrad_temp_rango(tupla1 , tupla2):

    d1, m1, a1, h1, mi1 = tupla1
    d2, m2, a2, h2, mi2 = tupla2
    fecha1 ='%s/%s/%s %s:%s' %(d1, m1, a1, h1, mi1)
    fecha2 ='%s/%s/%s %s:%s' %(d2, m2, a2, h2, mi2)
    indice1= datos2.index(fecha1)
    indice2= datos2.index(fecha2)
    global indices
    indices = list(range(indice1, indice2+1))
    print('A continuación se presenta la fecha y la medición de irradiancia y temperatura')
    for i in indices:
        print ('Para la fecha', datos2[i],', la irradiancia es', tabla[i][0], 'y la temperatura ambiente es', tabla[i][1])


def pot_modelo_GFV(G,T,N,Ppico, eta, kp,mu=2, Gstd=1000, Tr=25):
    Tc=T-0.031*G
    P=(N*G/Gstd*Ppico*(1+kp*(Tc-Tr))*eta*1e-3)
    return P
    

def pot_generada(tupla_instante, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    d, m, a, h, mi = tupla_instante
    irrad_temp(d, m, a, h, mi)
    Gi=tabla[indice][0]
    Ti=tabla[indice][1]
    print("esto es G ", Gi)
    print("esto es T ", Ti)
    print("la potencia generada es",pot_modelo_GFV(Gi,Ti,N, Ppico, eta, kp, mu, Gstd, Tr))


def pot_generada_rango(tupla1,tupla2, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    global potenciagenerada
    global potenciasrango
    potenciasrango=[]
    irrad_temp_rango(tupla1 , tupla2)
    for i in indices:
        potenciagenerada=pot_modelo_GFV(tabla[i][0],tabla[i][1],N, Ppico, eta, kp, mu, Gstd, Tr)
        potenciasrango.append(potenciagenerada)
        print ('Para la fecha', datos2[i],', la irradiancia es', tabla[i][0], 'y la temperatura ambiente es', tabla[i][1], 'y su potencia es: ',  potenciagenerada)

def pot_media_mes(mes, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    global cont
    cont=0
    global potenciames
    global horas
    global indice
    global potencia
    potencia=[]
    horas=0
    potenciames=0
    if(mes>="01" and mes<="12"):
        for valor in datos2:
          if(valor[3]==mes[0] and valor[4]==mes[1]):
            cont+=1
            #print("Hora", valor[11], valor[12])
            #print (valor)
            indice= datos2.index(valor)
            #print (indice)
            potencia.append(pot_modelo_GFV(tabla[indice][0], tabla[indice][1], N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25))
            potenciames= sum(potencia)
            #print("es la potencia",potencia)
    else:
        return print ("Debe ingresar un mes valido")


    potenciamedia=potenciames/cont
    horas=(cont/144)*24
    #print("total horas por dias: ", horas)
    #print("la potencia media es: ", potenciamedia)
    return potenciamedia

def pot_media_anual(N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    global potenciaanual
    potenciaanual=0
    for i in tabla:
        indi= tabla.index(i)
        potenciaanual+= pot_modelo_GFV(tabla[indi][0], tabla[indi][1], N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25)

    potenciamedia=potenciaanual/len(tabla)
    print(potenciaanual)
    print("tamaño de la tabla ", len(tabla))
    print("la potencia anual media es: ", potenciamedia)
    return potenciamedia

def energia_mes(mes, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    pot_media_mes(mes, 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    energia_mes=potenciames*horas
    print (" Para el mes:", mes,", la energia entregada es: ", round(energia_mes,2), "KWh" )
    return energia_mes

def energia_anual( N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    pot_media_anual(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    energia_anual=potenciaanual*(len(tabla))/144*24
    print ("La energia entregada para el año es: ", round(energia_anual,2), "KWh")
    return energia_anual

def factor_de_utilizacion():
        """ La función factor_de_utilizacion indica el factor de utilización anual de la instalación."""

        global factor
        energia_anual(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
        pot_promedio_anual=pot_media_anual(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
        horas_anuales=365*24
        ener_anual_GFV_real = pot_promedio_anual*horas_anuales
        ener_anual_GFV_nominal = round(2.88*horas_anuales, 2)
        print(ener_anual_GFV_real, ener_anual_GFV_nominal)
        factor=round(ener_anual_GFV_real/ener_anual_GFV_nominal, 2)
        print(factor)
        return factor

def max_energia_mes(N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    max=0
    pot=0
    mes=""
    for i in meses:
        pot=energia_mes(i, 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
        if(max<pot):
            mes=i
            #print("este mes ", mes)
            max=pot
            #print("Este es el maximo", max)
    print('El mes de mayor energia es :', mes , 'y la energia obtenida es :', max, "kwH")
    return (mes, max)

def max_pot_mes(N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):

    max=0
    pot=0
    mes=""
    for i in meses:
        pot_media_mes(i, 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
        if(max<potenciames):
            mes=i
            #print("este mes ", mes)
            max=potenciames
            #print("Este es el maximo", max)
    print('El mes de mayor potencia es :', mes , 'y la potencia obtenida es :', max,)
    return (mes, max)

def graficar_pot_rango(tupla1,tupla2, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    x=[]
    pot_generada_rango(tupla1,tupla2, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25)
    for i in indices:
        x.append(datos2[i])
        y=potenciasrango
    print("Fechas ", x)
    print("Potencias ", y)


    plt.plot(x, y)
    plt.xlabel('Fecha')
    plt.ylabel('Potencia')
    plt.show()

def graficar_energia_mensual(N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    y=[]
    for i in meses:
        energia=energia_mes(i, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25)
        print("Esta es la energia por mes",energia)
        y.append(round(energia,2))
    print("Meses ", meses)
    print("Energia ", y)

    plt.bar(meses, y)
    plt.xlabel('Meses')
    plt.ylabel('Energia')
    plt.show()

def graficar_meses(tupla_meses, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25):
    x=[]
    y_energia=[]
    y_potencia=[]

    

    for i in tupla_meses:
        #print("Estos son los meses", i)
        energia=energia_mes(i, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25)
        y_energia.append(energia)
        pot_media_mes(i, N, Ppico, eta, kp, mu=2, Gstd=1000, Tr=25)
        y_potencia.append(potencia)
        x.append(i)
    
    plt.figure()
    
             
    
    
    
# Grafico de Potencias
    plt.subplot(1,2,1)
    for j in y_potencia:
        plt.plot(range(len(j)),j)
    plt.xlabel('Tiempo')
    plt.ylabel('Potencia KW')
    plt.legend(tupla_meses)
# Grafico de energias
    plt.subplot(1,2,2)
    plt.bar(x, y_energia)
    plt.xlabel('Meses')
    plt.ylabel('Energia KWH')
    
    plt.show()

if __name__=='__main__':
    irrad_temp ('01', '07', '2019', '10', '00')
    # irrad_temp_rango(('01', '01', '2019', '00', '10'), ('01', '01', '2019', '02', '10'))
    # pot_modelo_GFV(0,28.2,12,240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # pot_generada(('01', '07', '2019', '10', '00'), 12, 240, 0.97, -0.0044, 2, 1000, 25)
    # pot_generada_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50'), 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # pot_media_mes('02', 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    #pot_media_anual(500, 260, 0.85, -0.0042, mu=2, Gstd=1000, Tr=25)
    # energia_mes('02', 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # energia_anual(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    factor_de_utilizacion()
    # max_energia_mes(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # max_pot_mes(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # graficar_pot_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50'), 12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    # graficar_energia_mensual(12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)
    #graficar_meses(('01','02','05'),12, 240, 0.97, -0.0044, mu=2, Gstd=1000, Tr=25)

