"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from App import controller
from App import model
from time import process_time
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accfile = "us_accidents_dis_2016.csv"

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Requerimento 4")
    print("7- Requerimento 5")
    print("8- Requerimento 6")
    print("9- Requerimento 7")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        time_1 = process_time()
        datos_acc=controller.carga_info(cont,accfile)
        print(controller.consultar_altura(datos_acc["a-fecha"]))
        print(controller.consultar_numero_elementos(datos_acc))
        time_2 = process_time()
        x = model.indexSize(datos_acc)
        print(time_2-time_1, "segundos")

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        xd= input("Digite la Fecha que desea consultar en este formato (YYYY-MM-DD): \n")
        asd=controller.consultar_acc_severidad(datos_acc,xd)
        print("----------------------------------------")
        for i in range(1,5):
            if(mp.get(asd,str(i))!= None):
                print("Accidentes severidad",str(i)+":",me.getValue(mp.get(asd,str(i))))
            else:
                print("Accidentes severidad",str(i)+":",0)

        print("-----------------------------------------")
    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        xd=input("Digite la Fecha que desea consultar en este formato (YYYY-MM-DD): \n")
        asd=controller.consultar_accidentes_anteriores_fecha(datos_acc,xd,3)
        print("--------------------------------------")
        print("Total accidentes antes de ",xd)
        print("Total:",asd[1])
        print("--------------------------------------")
        print("Fecha con más accidentes:",asd[0]["fecha_mas"])
        print("Cantidad de accidentes:",asd[0]["cantidad"])
        print("--------------------------------------")
    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        xd1=input("Digite el límite inferior en el formato (YYYY-MM-DD): \n")
        xd2=input("Digite el límite superior en el formato (YYYY-MM-DD): \n")
        asd=controller.consultar_accidentes_rango_fechas(datos_acc,xd1,xd2)
        print("-------------------------------------------------")
        print("Total de accidentes en este rango:",asd["Total"])
        print("-------------------------------------------------")
        print("Tipo de accidente más recurrente")
        for i in range(1,lt.size(asd["Tipo_dominante"])+1):
            elemento=lt.getElement(asd["Tipo_dominante"],i)
            if(elemento == "tipo1"):
                print("Categoria 1")
            elif(elemento == "tipo2"):
                print("Categoria 2")
            elif(elemento == "tipo3"):
                print("Categoria 3")
            elif(elemento == "tipo4"):
                print("Categoria 4")
        print("-------------------------------------------------")
    
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        xd1=input("Digite el límite inferior en el formato (YYYY-MM-DD): \n")
        xd2=input("Digite el límite superior en el formato (YYYY-MM-DD): \n")
        Intervalo=controller.consultar_state(datos_acc, xd1,xd2)
        print("-------------------------------------------------------------------------")
        print("Fecha con más accidentes reportados en el intervalo:",Intervalo["fecha mas accidentada"])
        print("-------------------------------------------------------------------------")
        print("Estado con más accidentes en el intervalo:",Intervalo["Estado mas accidentado"])
        print("-------------------------------------------------------------------------")
    
    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        xd1=input("Digite el límite inferior en el formato (HH:MM) (H= Hora, M= Minutos): \n")
        xd2=input("Digite el límite superior en el formato (HH:MM) (H= Hora, M= Minutos): \n")
        orden=controller.consultar_por_hora(datos_acc,xd1,xd2)
        total=0
        print("-------------------------------------------------------------------------")
        print("Intervalo:",xd1,"A",xd2)
        print("-------------------------------------------------------------------------")
        for i in orden:
            if(i != "porcen1" and i != "porcen2" and i != "porcen3" and i != "porcen4"):
                print(i,":",orden[i],)
                total+=orden[i]
        print("-------------------------------------------------------------------------")
        print("Total:",total)
        print("-------------------------------------------------------------------------")
        for i in orden:
            if(i != "Tipo 1" or i != "Tipo 2" or i != "Tipo 3" or i != "Tipo 4"):
                if(i == "porcen1"):
                    print("Porcentaje 1:",orden[i])
                elif(i == "porcen2"):
                    print("Porcentaje 2:",orden[i])
                elif(i == "porcen3"):
                    print("Porcentaje 3:",orden[i])
                elif(i == "porcen4"):
                    print("Porcentaje 4:",orden[i])
        print("-------------------------------------------------------------------------")
    



    else:
        sys.exit(0)
sys.exit(0)
