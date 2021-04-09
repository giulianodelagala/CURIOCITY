#Procesar Periodos
from poblar_onto import Populate
from rdflib import RDF, OWL, URIRef
from rdflib.plugins.sparql import prepareQuery

#from numpy import nan
import math
import pandas as pd 
import urllib.parse

import json

class PeriodProcess():
    def __init__(self, csvf, ontof):

        self.onto_filename = ontof
        self.data = self.LeerDatos(csvf)
        self.num_filas = self.data.shape[0] #total de filas
        self.Popu = Populate() #Populate Tools
        self.row = 0 #current processing row

    def LeerDatos(self, filename : str, header = True):
        #Return pandas dataframe with csv data
        return pd.read_csv(filename, sep ='\t', encoding='utf8', header = 0)
        
    def __ReadColumnIndex(self):
        #Column index from csv
        with open("name_period_columns.json", 'r') as name_columns_file :
            name_columns = json.load(name_columns_file)

        self.__col_codigo = self.data.columns.get_loc(name_columns['ID'])
        self.__col_descripcion = self.data.columns.get_loc(name_columns['Description'])
        self.__col_inicio = self.data.columns.get_loc(name_columns['Period begin'])
        self.__col_fin = self.data.columns.get_loc(name_columns['Period end'])

    def __Verificar(self, cadena: str):
        #Verify legal field
        if (str(cadena) != "No asignado" and 
            str(cadena) != 'nan' and 
            str(cadena) != 'No aplicable' and 
            str(cadena) != 'Desconocida' and
            str(cadena) != 'Desconocido' and
            str(cadena) != 'Sin información' and
            str(cadena) != 'No definido'):
            return True
        else:
            return False

    def FormatDate(self, date_text:str):
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

    def __InvalidRow(self):
        #Verify current row is valid: MainID and Title non empty
        if ( str(self.data.iloc[self.row, self.__col_codigo]) == 'nan' or
            str(self.data.iloc[self.row, self.__col_descripcion]) == 'nan'):
            #self.log.write(f"WARNING:Fila {self.row+2} -> no válida, no existe id/title\n") #TODO
            return True
        else:
            return False

    def __ProcessConcepts(self):
        self.__period = self.Popu.AddSubject(self.data.iloc[self.row, self.__col_codigo].strip(), "E4_Period", ins_label=False)
        self.Popu.AddLabel(self.__period, self.data.iloc[self.row,self.__col_descripcion].strip())

        self.__period_interval = self.Popu.AddSubjectFromURI(self.__period, "-Interval", "Interval", name_space="time")

        begin_date, xsd_tipo, tipo = self.FormatDate(self.data.iloc[self.row,self.__col_inicio])
        self.__begin = self.Popu.AddSubjectFromURI(self.__period_interval, "-Beginning", "Instant", name_space="time")
        self.Popu.AddLiteralFromURI(self.__begin, xsd_tipo, begin_date ,dtype=tipo, name_space="time")

        end_date, xsd_tipo, tipo = self.FormatDate(self.data.iloc[self.row,self.__col_fin])
        self.__end = self.Popu.AddSubjectFromURI(self.__period_interval, "-End", "Instant", name_space="time")
        self.Popu.AddLiteralFromURI(self.__end, xsd_tipo, end_date ,dtype=tipo, name_space="time")

        self.__period_span = self.Popu.AddSubjectFromURI(self.__period, "-Span", "SP10_Declarative_Time-Span", name_space="cit")

    def __ProcessProperties(self):
        self.Popu.AddRelationFromURI(self.__period, "P4_has_time-span", self.__period_span)

        self.Popu.AddRelationFromURI(self.__period_interval, "Q14_defines_time", self.__period_span, name_space="cit")
        self.Popu.AddRelationFromURI(self.__period_interval, 'hasBeginning', self.__begin, name_space="time")
        self.Popu.AddRelationFromURI(self.__period_interval, 'hasEnd', self.__end, name_space="time")


    def Execute(self):
        self.__ReadColumnIndex()

        for self.row in range(0, self.num_filas):
            #Verificar que es una fila con un objeto valido
            #MainID and Title non empty
            print ("Procesando: ", self.row + 2)
            if ( self.__InvalidRow()):
                continue
            else:
                self.__ProcessConcepts()    
                self.__ProcessProperties()        
                
        # Save individuals
        self.Popu.SaveTriples(self.onto_filename)

if __name__ == "__main__":
    Proceso = PeriodProcess(ontof="periodo_prueba.ttl", csvf="data/CODIFICACION_PERIODOS.csv")
    Proceso.Execute()