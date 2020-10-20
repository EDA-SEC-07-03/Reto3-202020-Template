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
    analizador={"a-fecha":om.newMap(omaptype="RBT",comparefunction=comparaFechas)}
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
        datentry = indice_severidad()
        agregar_fecha_map(datentry,accidente)
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
    lt.addLast(date_entry["accidentes_en_esta_fecha"],accidente)
    return date_entry

def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['a-fecha'])

def indice_severidad():
    entry={"indices_severidad":None,"accidentes_en_esta_fecha":None}
    entry["indices_severidad"]=mp.newMap(numelements=7,maptype="CHAINING",comparefunction=comparaSeveridad)
    entry["accidentes_en_esta_fecha"]=lt.newList("ARRAY_LIST")
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
def numero_elementos(mapa):
    return om.size(mapa['a-fecha'])

def accidentes_anteriores_fecha(analyzer,accidente_limite_superior):
    limite_inferior=om.minKey(analyzer["a-fecha"])
    limite_superior=transformador_fecha(accidente_limite_superior)
    rango=om.values(analyzer["a-fecha"],limite_inferior,limite_superior)
    total=0
    llave_con_mas_accidentes={"fecha_mas":None,"cantidad":None}
    for i in range(1,lt.size(rango)):
        elemento=lt.getElement(rango,i)
        total+=lt.size(elemento["accidentes_en_esta_fecha"])
        fecha=lt.getElement(elemento["accidentes_en_esta_fecha"],1)["Start_Time"]
        acc_date = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        acc_date = acc_date.date()
        fecha=acc_date.strftime('%d de %m de %Y')
        if(llave_con_mas_accidentes["cantidad"] == None ):
            llave_con_mas_accidentes["fecha_mas"]=fecha
            llave_con_mas_accidentes["cantidad"]=lt.size(elemento["accidentes_en_esta_fecha"])
        elif(llave_con_mas_accidentes["cantidad"] != None):
            if(lt.size(elemento["accidentes_en_esta_fecha"]) >= llave_con_mas_accidentes["cantidad"]):
                llave_con_mas_accidentes["cantidad"]=lt.size(elemento["accidentes_en_esta_fecha"])
                llave_con_mas_accidentes["fecha_mas"]=fecha
    return (llave_con_mas_accidentes,total)
def accidentes_durante_rango(analyzer,fecha_lim_inferior,fecha_lim_superior):
    mas_reportadas={"tipo1":0,"tipo2":0,"tipo3":0,"tipo4":0}
    total=0
    fecha_lim_inferior=transformador_fecha(fecha_lim_inferior)
    fecha_lim_superior=transformador_fecha(fecha_lim_superior)
    accidentes_rango=om.values(analyzer["a-fecha"],fecha_lim_inferior,fecha_lim_superior)
    for i in range(1,lt.size(accidentes_rango)):
        elemento=lt.getElement(accidentes_rango,i)
        total+=lt.size(elemento["accidentes_en_esta_fecha"])
        if(mp.get(elemento["indices_severidad"],"1") != None):
            mas_reportadas["tipo1"]+=lt.size(me.getValue(mp.get(elemento["indices_severidad"],"1"))['lista_accidentes_severidad'])
        if(mp.get(elemento["indices_severidad"],"2") != None):
            mas_reportadas["tipo2"]+=lt.size(me.getValue(mp.get(elemento["indices_severidad"],"2"))['lista_accidentes_severidad'])
        if(mp.get(elemento["indices_severidad"],"3") != None):
            mas_reportadas["tipo3"]+=lt.size(me.getValue(mp.get(elemento["indices_severidad"],"3"))['lista_accidentes_severidad'])
        if(mp.get(elemento["indices_severidad"],"4") != None):
            mas_reportadas["tipo4"]+=lt.size(me.getValue(mp.get(elemento["indices_severidad"],"4"))['lista_accidentes_severidad'])
    valores=mas_reportadas.values()
    maximo=max(valores)
    retorno={"Total":total,"Tipo_dominante":None}
    tipos_dominantes=lt.newList("ARRAY_LIST")
    for i in mas_reportadas:
        if(mas_reportadas[i] == maximo):
            lt.addLast(tipos_dominantes,i)
    retorno["Tipo_dominante"]=tipos_dominantes
    return retorno


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

"""
        """