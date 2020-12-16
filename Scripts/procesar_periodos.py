#Procesar Periodos
from poblar_onto import Populate
from rdflib import RDF, OWL, URIRef
from rdflib.plugins.sparql import prepareQuery

#from numpy import nan
import math
import pandas as pd 
import urllib.parse

def LeerDatos(filename : str, header = True):
    if (header):
        data = pd.read_csv(filename + ".csv", sep ='\t', encoding='utf8', header = 0)
    else:
        data = pd.read_csv(filename+ ".csv", sep ='\t', header = None)
    return data

data = LeerDatos("CODIFICACION_PERIODOS")
num_filas = data.shape[0] #total de filas

#Column index from csv
col_codigo = data.columns.get_loc('CODIGO')
col_descripcion = data.columns.get_loc('DESCRIP2')
col_inicio = data.columns.get_loc('INICIO')
col_fin = data.columns.get_loc('FIN')

#Load Ontology
Popu = Populate()

#Verificar si campo es legal TODO agregar otras condiciones
def Verificar(cadena: str):
    if (str(cadena) != "No asignado" and 
        str(cadena) != 'nan' and 
        str(cadena) != 'No aplicable' and 
        str(cadena) != 'No definido'):
        return True
    else:
        return False

#row = 13
def FormatDate(date_text:str):
    #Verificar tipo de fecha
    if (date_text.count("-") == 2): #date
        #Suponiendo fecha bien formada
        return date_text, "in_XSD_date", "date"
    else: #gYear
        if (len(date_text) < 4 and date_text.count("-") == 0): #pad zeros
            for i in range(len(date_text), 4):
                date_text = "0" + date_text
            return date_text, "in_XSD_g-Year", "year"
        else:
            return date_text, "in_XSD_g-Year", "year"
            


for row in range(0, num_filas):
    #Verificar que es una fila con un objeto valido
    #MainID and Title non empty
    print ("Procesando: ", row + 2)
    if ( str(data.iloc[row, col_codigo]) == 'nan' or str(data.iloc[row,col_descripcion]) == 'nan'):
        #log.write(f"WARNING:Fila {row+2} -> no válida, no existe id/title\n")
        continue

    else:

        period = Popu.AddSubject(data.iloc[row, col_codigo].strip(), "E4_Period", ins_label=False)
        Popu.AddLabel(period, data.iloc[row,col_descripcion].strip())

        period_interval = Popu.AddSubjectFromURI(period, "-Interval", "Interval", name_space="time")

        begin_date, xsd_tipo, tipo = FormatDate(data.iloc[row,col_inicio])
        begin = Popu.AddSubjectFromURI(period_interval, "-Beginning", "Instant", name_space="time")
        Popu.AddLiteralFromURI(begin, xsd_tipo, begin_date ,dtype=tipo, name_space="time")

        end_date, xsd_tipo, tipo = FormatDate(data.iloc[row,col_fin])
        end = Popu.AddSubjectFromURI(period_interval, "-End", "Instant", name_space="time")
        Popu.AddLiteralFromURI(end, xsd_tipo, end_date ,dtype=tipo, name_space="time")

        period_span = Popu.AddSubjectFromURI(period, "-Span", "SP10_Declarative_Time-Span", name_space="cit")
        ############
        # Properties
        ############
        Popu.AddRelationFromURI(period, "P4_has_time-span", period_span)

        Popu.AddRelationFromURI(period_interval, "Q14_defines_time", period_span, name_space="cit")
        Popu.AddRelationFromURI(period_interval, 'hasBeginning', begin, name_space="time")
        Popu.AddRelationFromURI(period_interval, 'hasEnd', end, name_space="time")


#############################
# Save individuals
Popu.SaveTriples("periodos.ttl")

