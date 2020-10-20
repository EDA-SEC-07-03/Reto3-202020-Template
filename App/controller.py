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

import config as cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""


# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    return  model.arbol_inicial_ACC()


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    acc_file = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(acc_file, encoding="windows-1252"),
                                delimiter=",")
    for acc in input_file:
        model.add_accident(analyzer, acc)
    return analyzer
def carga_info(analyzer,accidentsfile):
    x=loadData(analyzer,accidentsfile)
    return x

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def consultar_acc_severidad(arbol,fecha):
    xd=model.cantidad_acc_severidad(arbol,fecha)
    return xd
def consultar_altura(mapa):
    altura=om.height(mapa)
    return altura
def consultar_numero_elementos(mapa):
    num=model.numero_elementos(mapa)
    return num
def consultar_accidentes_anteriores_fecha(mapa,limite_superior):
    return model.accidentes_anteriores_fecha(mapa,limite_superior)

"""probador=model.arbol_inicial_ACC()
mapa_cargado_alternativo=loadData(probador,"us_accidents_dis_2016.csv")
xd=model.accidentes_anteriores_fecha(mapa_cargado_alternativo,"2016-06-22")
mapa_cargado=loadData(probador,"us_accidents_dis_2016.csv")["a-fecha"]
fecha=model.transformador_fecha("2016-06-22")
valor_en_esta_fecha=me.getValue(om.get(mapa_cargado,fecha))
lista_en_fecha=valor_en_esta_fecha["accidentes_en_esta_fecha"]"""
