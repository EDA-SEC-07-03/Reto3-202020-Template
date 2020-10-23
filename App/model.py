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
    analizador={"a-fecha":om.newMap(omaptype="RBT",comparefunction=comparaFechas),"a-horas":om.newMap(omaptype="RBT",comparefunction=comparaFechas)}
    return analizador
    
# Funciones para agregar informacion al catalogo
def add_accident(arbol,accidente):
    cargar_fecha(arbol["a-fecha"],accidente)
    cargar_hora(arbol["a-horas"],accidente)
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
def cargar_hora(omap,accidente):
    hora=accidente["Start_Time"]
    hora=hora[11:16]
    hora=datetime.datetime.strptime(hora,"%H:%M")
    hora=hora.time()
    entry= om.get(omap,hora)
    if entry is None:
        datentry = indice_severidad2()
        agregar_hora_map(datentry,accidente)
        om.put(omap,hora,datentry)
    else:
        datentry=me.getValue(entry)
        agregar_hora_map(datentry,accidente)
    return omap


def agregar_hora_map(datentry,accidente):
    index_hora=datentry["indices_severidad"]
    if(lt.size(index_hora) == 0):
        for i in range(1,5):
            lt.addLast(index_hora,lista_severidad(i))
    if(accidente["Severity"] == "1"):
        add1=lt.getElement(index_hora,1)
        lt.addLast(add1["lista_accidentes_severidad"],accidente)
    elif(accidente["Severity"] == "2"):
        add1=lt.getElement(index_hora,2)
        lt.addLast(add1["lista_accidentes_severidad"],accidente)
    elif(accidente["Severity"] == "3"):
        add1=lt.getElement(index_hora,3)
        lt.addLast(add1["lista_accidentes_severidad"],accidente)
    elif(accidente["Severity"] == "4"):
        add1=lt.getElement(index_hora,4)
        lt.addLast(add1["lista_accidentes_severidad"],accidente)

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
    index_state=date_entry["accidentes_estado"]
    busca_estado=mp.get(index_state,accidente["State"])
    if(busca_estado is None):
        lista_acc_sta=lt.newList("ARRAY_LIST")
        lt.addLast(lista_acc_sta,accidente)
        mp.put(index_state,accidente["State"],lista_acc_sta)
    else:
        lista_acc_sta=me.getValue(busca_estado)
        lt.addLast(lista_acc_sta,accidente)
    lt.addLast(date_entry["accidentes_en_esta_fecha"],accidente)

def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['a-fecha'])

def indice_severidad():
    entry={"indices_severidad":None,"accidentes_en_esta_fecha":None,"accidentes_estado":None}
    entry["indices_severidad"]=mp.newMap(numelements=7,maptype="CHAINING",comparefunction=comparaSeveridad)
    entry["accidentes_estado"]=mp.newMap(maptype="CHAINING",comparefunction=compara_mapa_string)
    entry["accidentes_en_esta_fecha"]=lt.newList("ARRAY_LIST")
    return entry
def indice_severidad2():
    entry={"indices_severidad":None,}
    entry["indices_severidad"]=lt.newList("ARRAY_LIST")
    return entry

def lista_severidad(severidad):
    ofentry = {'severidad': None, 'lista_accidentes_severidad': None}
    ofentry['severidad'] = severidad
    ofentry['lista_accidentes_severidad'] = lt.newList('ARRAY_LIST', comparaSeveridad)
    return ofentry

def transformador_fecha(fecha):
    fecha=datetime.datetime.strptime(fecha, '%Y-%m-%d')
    xd=fecha.date()
    return xd

def transformador_hora(hora):
    hora=datetime.datetime.strptime(hora,"%H:%M")
    hora=hora.time()
    return hora



def aproximafechas(fecha1):
    xd=fecha1.split(":")
    if(xd[0] == "23" and int(xd[1])> 45):
        return "23:59"
    else:
        xd[1]=int(xd[1])
        if(xd[1] < 15):
            xd[1]="00"
        elif((xd[1]>= 15 and xd[1] <= 30) or (xd[1] <= 45 and xd[1]> 30)):
            xd[1]="30"
        elif(xd[1]>45):
            xd[0]=str(int(xd[0])+1)
            xd[1]="00"
    xd=":".join(xd)
    return xd




# ==============================
# Funciones de consulta
# ==============================

def rango_horas(mapa,hora_inicial,hora_final):
    tipos={"Tipo 1":0,"Tipo 2":0,"Tipo 3":0,"Tipo 4":0}
    hora_inicial=transformador_hora(aproximafechas(hora_inicial))
    hora_final=transformador_hora(aproximafechas(hora_final))

    a_iterar=om.values(mapa["a-horas"],hora_inicial,hora_final)
    for i in range(1,lt.size(a_iterar)+1):
        elementox=lt.getElement(a_iterar,i)
        elemento=elementox["indices_severidad"]
        for e in range(1,lt.size(elemento)+1):
            if(e == 1):
                total_tipo1=lt.size((lt.getElement(elemento,e))["lista_accidentes_severidad"])
                tipos["Tipo 1"]+=total_tipo1
            if(e == 2):
                total_tipo2=lt.size((lt.getElement(elemento,e))["lista_accidentes_severidad"])
                tipos["Tipo 2"]+=total_tipo2
            if(e == 3):
                total_tipo3=lt.size((lt.getElement(elemento,e))["lista_accidentes_severidad"])
                tipos["Tipo 3"]+=total_tipo3
            if(e == 4):
                total_tipo4=lt.size((lt.getElement(elemento,e))["lista_accidentes_severidad"])
                tipos["Tipo 4"]+=total_tipo4
    total=0
    for i in tipos:
        total+=tipos[i]
    tipos["porcen1"]=round((tipos["Tipo 1"]*100)/total,4)
    tipos["porcen2"]=round((tipos["Tipo 2"]*100)/total,4)
    tipos["porcen3"]=round((tipos["Tipo 3"]*100)/total,4)
    tipos["porcen4"]=round((tipos["Tipo 4"]*100)/total,4)
    return tipos
        


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
    for i in range(1,lt.size(rango)+1):
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
    for i in range(1,lt.size(accidentes_rango)+1):
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

def accidente_estado(mapa,fecha_inicial,fecha_final):
    fecha_inicial=transformador_fecha(fecha_inicial)
    fecha_final=transformador_fecha(fecha_final)
    states={}
    fecha_mas={"Fecha":None,"Cantidad":0}
    total=0
    a_iterar=om.values(mapa["a-fecha"],fecha_inicial,fecha_final)
    for i in range(1,lt.size(a_iterar)+1):
        itera=(lt.getElement(a_iterar,i))["accidentes_estado"]
        llaves=mp.keySet(itera)
        for e in range(1,lt.size(llaves)+1):
            asd=lt.getElement(llaves,e)
            states[asd]=0
    for i in range(1,lt.size(a_iterar)+1):
        itera=(lt.getElement(a_iterar,i))["accidentes_estado"]
        for e in states:
            if(mp.get(itera,e) != None):
                al=lt.size(me.getValue(mp.get(itera,e)))
                states[e]+=al
                total+=lt.size(me.getValue(mp.get(itera,e)))
        itera2=(lt.getElement(a_iterar,i))["accidentes_en_esta_fecha"]
        if(lt.size(itera2) > fecha_mas["Cantidad"] ):
            fecha=lt.getElement(itera2,1)
            fecha_mas["Fecha"]=fecha["Start_Time"]
            fecha_mas["Cantidad"]=lt.size(itera2)
    maximo1=max(states.values())
    for i in states:
        if(states[i] == maximo1):
            fecha_mas["Estado"]=i
            fecha_mas["Cantidad estado"]=maximo1
    return fecha_mas




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
        
def compara_mapa_string(str1,str2):
    str2=me.getKey(str2)
    if(str1 == str2):
        return 0
    elif(str1 > str2):
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