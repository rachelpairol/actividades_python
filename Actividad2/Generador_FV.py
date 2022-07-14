# -*- coding: utf-8 -*-
from tabla_anual import tabla 
from fechas_tabla_anual import datos2
from matplotlib import use
import matplotlib.pyplot as plt 
from datos1 import tabla2 
use ( 'Qt5Agg' )


class Generador_FV:


    def __init__( self, tabla, N, Ppico, eta, kp ):
        self.N=N
        self.Ppico= Ppico
        self.eta=eta
        self.kp=kp
        self.mu=2
        self.__Gstd=1000
        self.__Tr=25
        self.tabla=tabla
    

    def __str__(self):
        """ Mensaje a mostrar con print()
        """
        mensaje = "Generador fotovoltaico con " f'{self.N} paneles de ' f'{self.Ppico} W-pico. ' +\
        "Coef. de potencia-temperatura: " f'{self.kp} 1/Celsius. ' +\
        "Rendimiento global de la instalación: " f'{self.eta} (por unidad). ' +\
        "Umbral mínimo de generación: " f'{self.mu} (%). ' +\
        "(Irrad. estándar:" f'{self.__Gstd} W/m2 ; Temp. de referencia: ' f'{self.__Tr} °C)'
        return mensaje

   
    fecha=''

    def irrad_temp(self, d, m, a, h, mi):

        fecha ='%s/%s/%s %s:%s' %(d, m, a, h, mi)
        print('ESTA ES LA FECHA',fecha)
        #for i in datos2:
        if (fecha not in datos2):
            print('NO HAY MEDICIONES PARA LA FECHA INGRESADA O LA FECHA ES INCORRECTA')
        else:
            global indice
            indice= datos2.tolist().index(fecha)
            print ('Este es el indice', indice)
            print ('Esta es la irradiancia', self.tabla[indice])

    def irrad_temp_rango(self,tupla1 , tupla2):
    
        d1, m1, a1, h1, mi1 = tupla1
        d2, m2, a2, h2, mi2 = tupla2
        fecha1 ='%s/%s/%s %s:%s' %(d1, m1, a1, h1, mi1)
        fecha2 ='%s/%s/%s %s:%s' %(d2, m2, a2, h2, mi2)
        indice1= datos2.tolist().index(fecha1)
        indice2= datos2.tolist().index(fecha2)
        global indices
        indices = list(range(indice1, indice2+1))
        print('A continuación se presenta la fecha y la medición de irradiancia y temperatura')
        for i in indices:
            print ('Para la fecha', datos2[i],', la irradiancia es', self.tabla[i][0], 'y la temperatura ambiente es', self.tabla[i][1])

    
    def pot_modelo_GFV(self,G,T):
        Tc=T-0.031*G
        P=(self.N*G/self.__Gstd*self.Ppico*(1+self.kp*(Tc-self.__Tr))*self.eta*1e-3)
        #print("Esta es la potencia", P)
        return P
       
    def pot_generada(self,tupla_instante):
        d, m, a, h, mi = tupla_instante
        self.irrad_temp(d, m, a, h, mi)
        Gi=self.tabla[indice][0]
        Ti=self.tabla[indice][1]
        print("esto es G ", Gi)
        print("esto es T ", Ti)
        potencia_generada=round(self.pot_modelo_GFV(Gi,Ti),2)
        print("la potencia generada es",potencia_generada)
        return potencia_generada
        
    def pot_generada_rango(self,tupla1,tupla2):
        global potenciagenerada
        global potenciasrango
        potenciasrango=[]
        self.irrad_temp_rango(tupla1 , tupla2)
        for i in indices:
            potenciagenerada=self.pot_modelo_GFV(self.tabla[i][0],self.tabla[i][1])
            potenciasrango.append(potenciagenerada)
            print ('Para la fecha', datos2[i],', la irradiancia es', self.tabla[i][0], 'y la temperatura ambiente es', self.tabla[i][1], 'y su potencia es: ',  potenciagenerada)
        
    def pot_media_mes(self,mes):
        cont=0
        global potenciames
        global horas 
        horas=0
        potenciames=0   
        global potencia 
        potencia=[]
        if(mes>="01" and mes<="12"):
          for valor in datos2:
            if(valor[3]==mes[0] and valor[4]==mes[1]):
                cont+=1
                #print("Hora", valor[11], valor[12])
                #print (valor)
                indice= datos2.tolist().index(valor)
                #print (indice)
                potencia.append(self.pot_modelo_GFV(self.tabla[indice][0], self.tabla[indice][1]))
                potenciames= sum(potencia)
        else:
            return print ("Debe ingresar un mes valido")
    
        potenciamedia=potenciames/cont
        horas=(cont/144)*24
        #print("total horas por dias: ", horas)
        #print("la potencia media es: ", potenciamedia)
        return potenciamedia

    def pot_media_anual(self):
        global potenciaanual
        potenciaanual=0
        for i in range(len(self.tabla)):
            potenciaanual+= self.pot_modelo_GFV(self.tabla[i][0], self.tabla[i][1])
                    
        print(potenciaanual)
        potenciamedia=potenciaanual/len(self.tabla)
        #print("tamaño de la tabla ", len(self.tabla))
        #print("la potencia anual media es: ", potenciamedia)
        return potenciamedia

    def energia_mes(self,mes):
        self.pot_media_mes(mes)
        energia_mes=potenciames*horas
        #print (" Para el mes:", mes,", la energia entregada es: ", round(energia_mes,2), "KWh" )
        return energia_mes

    def energia_anual(self):
        self.pot_media_anual()
        energia_anual=potenciaanual*(len(self.tabla))/144*24
        #print ("La energia entregada para el año es: ", round(energia_anual,2), "KWh")
        return energia_anual

    def max_energia_mes(self):
        max=0
        pot=0
        mes=""
        meses=['01','02','03','04','05','07','08','09','10','11','12']
        for i in meses:
            pot=self.energia_mes(i)
            if(max<pot):
                mes=i
                #print("este mes ", mes)
                max=pot
                #print("Este es el maximo", max)
        print('El mes de mayor energia es :', mes , 'y la energia obtenida es :', max, "kwH")
        return (mes, max)     

    def factor_de_utilizacion(self):
        """ La función factor_de_utilizacion indica el factor de utilización anual de la instalación."""

        global factor
        self.energia_anual()
        pot_promedio_anual=self.pot_media_anual()
        horas_anuales=365*24
        ener_anual_GFV_real = pot_promedio_anual*horas_anuales
        ener_anual_GFV_nominal = round(2.88*horas_anuales, 2)
        print(ener_anual_GFV_real, ener_anual_GFV_nominal)
        factor=round(ener_anual_GFV_real/ener_anual_GFV_nominal, 2)
        print(factor)
        return factor

    def max_pot_mes(self):
        meses=['01','02','03','04','05','07','08','09','10','11','12']
        max=0
        pot=0
        mes=""
        for i in meses:
            self.pot_media_mes(i)
            if(max<potenciames):
                mes=i
                #print("este mes ", mes)
                max=potenciames
                #print("Este es el maximo", max)
        print('El mes de mayor potencia es :', mes , 'y la potencia obtenida es :', max,)
        return (mes, max)     

    def graficar_pot_rango(self,tupla1,tupla2):
        x=[]
        self.pot_generada_rango(tupla1,tupla2)
        for i in indices:
            x.append(datos2[i])
            y=potenciasrango
       # print("Fechas ", x)
        #print("Potencias ", y)
        
        plt.title("Potencia generada entre: " f'{tupla1[0]}/' f'{tupla1[1]} a las ' f'{tupla1[3]}:' f'{tupla1[4]} hs y ' f'{tupla2[0]}/' f'{tupla2[1]} a las ' f'{tupla2[3]}:' f'{tupla2[4]} hs')
        plt.xticks([])
        plt.plot(x, y)
        plt.xlabel('Fecha')
        plt.ylabel('Potencia')
        plt.show()

    def graficar_energia_mensual(self):
        meses=['01','02','03','04','05','07','08','09','10','11','12']
        y=[]
        for i in meses:
            energia=self.energia_mes(i)
            print("Esta es la energia por mes",energia)
            y.append(round(energia,2))
        print("Meses ", meses)
        print("Energia ", y)

        plt.bar(meses, y)
        plt.xlabel('Meses')
        plt.ylabel('Energia')
        plt.show()

    def graficar_meses(self,tupla_meses):
        x=[]
        y_energia=[]
        y_potencia=[]

        for i in tupla_meses:
            #print("Estos son los meses", i)
            energia=self.energia_mes(i)
            y_energia.append(energia)
            self.pot_media_mes(i)
            y_potencia.append(potencia)
            x.append(i)
        
        plt.figure()
        print(y_potencia)
             
       
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


# clase heredada

class Generador_FV_Sta_Fe(Generador_FV):
    def __init__(self):
        Generador_FV.__init__(self,tabla2, 240,260,0.85,-0.0042)

    def __str__(self):
            """ Mensaje a mostrar con print()
            """
            mensaje = "Generador fotovoltaico con " f'{self.N} paneles de ' f'{self.Ppico} W-pico en la ciudad de Santa Fe. ' +\
            "Coef. de potencia-temperatura: " f'{self.kp} 1/Celsius. ' +\
            "Rendimiento global de la instalación: " f'{self.eta} (por unidad). ' +\
            "Umbral mínimo de generación: " f'{self.mu} (%). ' +\
            "(Irrad. estándar: 1000 W/m2 ; Temp. de referencia: 25  °C)"
            return mensaje 


gen = Generador_FV(tabla, 500, 260, 0.85, -0.0042)
#print(gen)

gen_UTN=Generador_FV_Sta_Fe()
print(gen_UTN)
if __name__=='__main__':
    #gen.irrad_temp ('01', '01', '2019', '00', '20')
    #gen.irrad_temp_rango(('01', '01', '2019', '00', '10'), ('01', '01', '2019', '02', '10'))
    #gen.pot_modelo_GFV(635,32.5)
    #gen.pot_generada(('01', '07', '2019', '10', '00'))
    #gen.pot_generada_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50')) 
    #gen.pot_media_mes('02')
    #gen.pot_media_anual()
    #gen.energia_mes('02')
    #gen.energia_anual()
    #gen.max_energia_mes()
    gen.factor_de_utilizacion()
    #gen.max_pot_mes()
    #gen.graficar_pot_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50'))
    #gen.graficar_energia_mensual()   
    #gen.graficar_meses(('01','03','04','07'))
    
    #Instancias de Generador_FV_Sta_Fe 
    gen_UTN.irrad_temp ('01', '01', '2019', '00', '20')
    #gen_UTN.irrad_temp_rango(('01', '01', '2019', '00', '10'), ('01', '01', '2019', '02', '10'))
    #gen_UTN.pot_modelo_GFV(635,32.5)
    #gen_UTN.pot_generada(('01', '07', '2019', '10', '00'))
    #gen_UTN.pot_generada_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50')) 
    #gen_UTN.pot_media_mes('02')
    #gen_UTN.pot_media_anual()
    #gen_UTN.energia_mes('02')
    #gen_UTN.energia_anual()
    #gen_UTN.max_energia_mes()
    #gen_UTN.factor_de_utilizacion()
    #gen_UTN.max_pot_mes()
    #gen_UTN.graficar_pot_rango(('01', '07', '2019', '10', '00'), ('01', '07', '2019', '10', '50'))
    #gen_UTN.graficar_energia_mensual()   
    #gen_UTN.graficar_meses(('01','03','04','07')) 
