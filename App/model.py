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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
import datetime
assert config

#
"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def arbol_inicial_ACC():
    analizador={"a-fecha":om.newMap(omaptype="BST",comparefunction=comparaFechas)}
    return analizador
    
# Funciones para agregar informacion al catalogo
def add_accident(arbol,accidente):
    cargar_fecha(arbol["a-fecha"],accidente)
    return arbol

def cargar_fecha(map,accidente):
    fecha=accidente["Start_Time"]
    acc_date = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, acc_date.date())
    if entry is None:
        datentry = indice_severidad(accidente)
        om.put(map, acc_date.date(), datentry)
    else:
        datentry = me.getValue(entry)
        agregar_fecha_map(datentry,accidente)
    return map

def agregar_fecha_map(date_entry,accidente):
    index_fecha=date_entry["indices_severidad"]
    busca_severidad=mp.get(index_fecha,accidente["Severity"])
    if(busca_severidad is None):
        entry=lista_severidad(accidente["Severity"])
        lt.addLast(entry["lista_accidentes_severidad"],accidente)
        mp.put(index_fecha,accidente["Severity"],entry)
    else:
        entry=me.getValue(busca_severidad)
        lt.addLast(entry["lista_accidentes_severidad"],accidente)
    return date_entry



def indice_severidad(acc):
    entry={"indices_severidad":None}
    entry["indices_severidad"]=mp.newMap(numelements=7,maptype="CHAINING",comparefunction=comparaSeveridad)
    return entry
def lista_severidad(severidad):
    ofentry = {'severidad': None, 'lista_accidentes_severidad': None}
    ofentry['severidad'] = severidad
    ofentry['lista_accidentes_severidad'] = lt.newList('SINGLE_LINKED', comparaSeveridad)
    return ofentry

def transformador_fecha(fecha):
    fecha=datetime.datetime.strptime(fecha, '%Y-%m-%d')
    xd=fecha.date()
    return xd

# ==============================
# Funciones de consulta
# ==============================

def cantidad_acc_severidad(arbol,fecha):
    asd=om.get(arbol["a-fecha"],transformador_fecha(fecha))
    asd=me.getValue(asd)
    mapretorno=mp.newMap(numelements=7,maptype="PROBING",comparefunction=comparaSeveridad)
    for i in range(1,5):
        if(mp.get(asd["indices_severidad"],str(i)) != None):
            retornox=mp.get(asd["indices_severidad"],str(i))
            tamaño=me.getValue(retornox)
            tamaño=lt.size(tamaño["lista_accidentes_severidad"])
            mp.put(mapretorno,str(i),tamaño)
    return mapretorno

# ==============================
# Funciones de Comparacion
# ==============================
def comparaFechas(fecha1, fecha2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (fecha1 == fecha2):
        return 0
    elif (fecha1 > fecha2):
        return 1
    else:
        return -1
def comparaSeveridad(severidad1,severidad2):
    severidad2=me.getKey(severidad2)
    if (int(severidad1) == int(severidad2)):
        return 0
    elif (int(severidad1) > int(severidad2)):
        return 1
    else:
        return -1
