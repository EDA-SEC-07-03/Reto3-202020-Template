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


accfile = "us_accidents_dis_2017.csv"

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

    else:
        sys.exit(0)
sys.exit(0)
