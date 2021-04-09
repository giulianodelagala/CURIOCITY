#Procesamiento de Data
from poblar_onto import Populate
from rdflib import RDF, OWL, URIRef, Graph
from rdflib.plugins.sparql import prepareQuery

#from numpy import nan
import math
import pandas as pd 
import urllib.parse

import json

class DataProcess:
    def __init__(self, logf, ontof, csvf, periodf, invalid = [], sender = None):
        
        self.onto_filename = ontof
        
        self.log = open(logf, "w") #log file
        self.data = self.LeerDatos(csvf) #data from csv
        self.num_filas = self.data.shape[0] #total rows from csv

        self.Popu = Populate() #Populate tools
        self.period_graph = Graph() #Periods instantiation
        self.period_graph.parse(periodf, format="turtle")
        self.sender = sender

        if (invalid == []):
            self.invalid = ['No asignado',
                'nan',
                'No aplicable',
                'Desconocida', 'Desconocido',
                'Sin información',
                'No definido']
        else:
            self.invalid = invalid

        self.row = 0 #current processing row
    
    def __del__(self):
        self.log.close()

    def __ScreenLog(self, message):
        if (self.sender == None):
            print (message)
        else:
            self.sender.Logger(message)

    def LeerDatos(self, filename : str, header = True):
        #Return pandas dataframe with csv data
        return pd.read_csv(filename, sep ='\t', encoding='utf8', header = 0)
        
    def __ReadColumnIndex(self):
        #Column index from csv
        with open("name_columns.json", 'r') as name_columns_file :
            name_columns = json.load(name_columns_file)

        self.__col_codigo = self.data.columns.get_loc(name_columns['ID'])
        self.__col_alt_code = self.data.columns.get_loc(name_columns['Alternative ID'])
        self.__col_titulo = self.data.columns.get_loc(name_columns['Title'])
        self.__col_descripcion = self.data.columns.get_loc(name_columns['Description'])
        self.__col_creador = self.data.columns.get_loc(name_columns['Author'])

        self.__col_uso = self.data.columns.get_loc(name_columns['Utility'])
        self.__col_duenio = self.data.columns.get_loc(name_columns['Owner'])
        self.__col_estado = self.data.columns.get_loc(name_columns['Condition State'])
        self.__col_material = self.data.columns.get_loc(name_columns['Material'])

        self.__col_id_periodo = self.data.columns.get_loc(name_columns['Period ID'])
        self.__col_periodo = self.data.columns.get_loc(name_columns['Period'])

        self.__col_date_creation = self.data.columns.get_loc(name_columns['Creation date'])

        self.__col_adquisicion = self.data.columns.get_loc(name_columns['Acquisition'])
        self.__col_donor = self.data.columns.get_loc(name_columns['Donor'])
        self.__col_desc_donor = self.data.columns.get_loc(name_columns['Donor description'])
        #TODO probable organizacion de descripciones

        self.__col_localizacion = self.data.columns.get_loc(name_columns['Location in Museum'])
        self.__col_department = self.data.columns.get_loc(name_columns['Museum Department'])

        self.__col_alto = self.data.columns.get_loc(name_columns['Artifact height'])
        self.__col_ancho = self.data.columns.get_loc(name_columns['Artifact width'])
        self.__col_largo = self.data.columns.get_loc(name_columns['Artifact length'])
        self.__col_diametro = self.data.columns.get_loc(name_columns['Artifact diameter'])
        self.__col_profundidad = self.data.columns.get_loc(name_columns['Artifact depth'])
        self.__col_peso = self.data.columns.get_loc(name_columns['Artifact weight'])

    def __InitUnknownConcepts(self):
        ########################
        # Unknown Concepts
        ########################
        self.__alt_id_unknown = self.Popu.AddSubject("ID_alternativo_desconocido", "E42_Identifier", ins_label=False)
        self.__utility_unknown = self.Popu.AddSubject("Utilidad_desconocida", "E55_Type", ins_label=False)
        self.__creator_unknown = self.Popu.AddSubject("Creador_desconocido", "E39_Actor", ins_label=False)
        self.__donor_unknown = self.Popu.AddSubject("Donador_desconocido", "E39_Actor", ins_label=False)
        self.__owner_unknown = self.Popu.AddSubject("Propietario_desconocido", "E39_Actor", ins_label=False)
        self.__condition_unknown = self.Popu.AddSubject("Condicion_desconocida", "E55_Type", ins_label=False)
        self.__material_unknown = self.Popu.AddSubject("Material_desconocido", "E57_Material", ins_label=False)
        self.__place_unknown = self.Popu.AddSubject("Lugar_desconocido", "E53_Place", ins_label=False)
        self.__periodo_unknown = self.Popu.AddSubject("Periodo_desconocido", "E4_Period", ins_label=False)
        self.__periodo_span_unknown = self.Popu.AddSubject("Lapso_de_Tiempo_desconocido", "SP10_Declarative_Time-Span",
            name_space="cit" ,ins_label=False)

    
    def __Verificar(self, cadena: str):
        #Verify legal field
        if (str(cadena) in self.invalid):
            return False
        else:
            return True

    def VerificarActorv2(self, actor: str):
        #Verificar si actor existe y devolver URI
        actor = URIRef(self.Popu.cit + self.Popu.Formato(actor))
        qactor = prepareQuery("""SELECT ?s
                            WHERE {
                                VALUES ?type { ecrm:E21_Person ecrm:E74_Group }
                                ?s a ?type .                                
                                }""",
                                initNs= {"ecrm" : self.Popu.ecrm,
                                    "cit": self.Popu.cit,
                                    "owl": OWL} )

        actor_q = self.Popu.g.query(qactor, initBindings={'s': actor})
        return actor_q

    def __VerifyActor(self, actor : str, tipo:str):
        if ( self.__Verificar(actor)):
            actor = actor.strip()
            actor_uri = URIRef(self.Popu.cit + self.Popu.Formato(actor))

            if ( (actor_uri, RDF.type, self.Popu.ecrm.E21_Person) in self.Popu.g): #existe como persona
                self.__ScreenLog("Person existente ... omitiendo")
                return actor_uri
            elif ( (actor_uri, RDF.type, self.Popu.ecrm.E74_Group) in self.Popu.g): #existe como grupo
                self.__ScreenLog("Group existente ... omitiendo")
                return actor_uri
            else: #Pedir confirmacion
                while (True):
                    if (self.sender != None):
                        actor_type = self.sender.Choose(actor)
                    else:
                        actor_type = input(f"¿{actor} is [p]erson\n or [g]roup?")
                    if (actor_type == 'p'):
                        return self.Popu.AddSubject(actor, "E21_Person")
                    elif (actor_type == 'g'):
                        return self.Popu.AddSubject(actor, "E74_Group")
                    else:
                        continue   
        else: #No Actor info
            if (tipo == "creator"):
                self.log.write(f"WARNING:Fila {self.row+2} -> Creador No identificado\n")
                return self.__creator_unknown
            elif (tipo == "donor"):
                self.log.write(f"WARNING:Fila {self.row+2} -> Donador No identificado\n")
                return self.__donor_unknown
            elif (tipo == "owner"):
                self.log.write(f"WARNING:Fila {self.row+2} -> Propietario No identificado\n")
                return self.__owner_unknown

                   
    def __VerifyMainID(self, id_text : str):
        id_text = id_text.strip()
        subject = URIRef(self.Popu.cit + id_text)
        if ( (subject, RDF.type, self.Popu.ecrm.E42_Identifier) in self.Popu.g):
            self.log.write(f"ERROR:Fila {self.row+2} -> Codigo existente: {id_text}, Fila ignorada\n")
            return "ERROR -> Codigo existente", True
        else:    
            self.__conc_id = self.Popu.AddSubject(id_text, "E42_Identifier")
            self.Popu.AddLiteralFromURI(self.__conc_id, "P190_has_symbolic_content", id_text, "string")
            return False

    def __VerifyAltId(self, alt_id_text:str):
        if (self.__Verificar(alt_id_text) ):
            alt_id_text = alt_id_text.strip()
            alt_id = self.Popu.AddSubjectFromURI(self.__conc_id, "/IDalternativo", "E42_Identifier")
            self.Popu.AddLiteralFromURI(alt_id, "P190_has_symbolic_content", alt_id_text, "string")
            return alt_id
        else:
            self.log.write(f"WARNING:Fila {self.row+2} -> Codigo alternativo No Asignado\n")
            return self.__alt_id_unknown

    def __VerifyMainTitle(self, title : str):
        if (self.__Verificar(title)):
            title = title.strip()
            return title #TODO Crear Title Concept
        else:
            self.log.write(f"WARNING:Fila {self.row+2} -> Titulo no asignado\n")
            return "Sin título"

    def VerificarManMadeOrNatural(self, object: str):
        while (True):
            object_type = input(f"¿{object} es [h]uman made o [n]atural?")
            if (object_type == 'h'):
                return self.Popu.AddSubjectFromURI(self.__conc_id, "/Object", "E22_Man-Made_Object")
            elif (object_type == 'n'):
                return self.Popu.AddSubjectFromURI(self.__conc_id, "/Object", "E19_Physical_Object")
            else:
                continue

    def __VerifyUtility(self, utility_text: str):
        if (self.__Verificar(utility_text) ):
            utility_text = utility_text.strip()
            utility = self.Popu.AddSubjectFromURI(self.__conc_id, "/Utility", "E55_Type")
            self.Popu.AddLabel(utility, utility_text)
            return utility
        else:
            self.log.write(f"WARNING:Fila {self.row+2} -> Utilidad desconocidad\n")
            return self.__utility_unknown

    def __VerifyObjectCondition(self, condition: str):
        if ( self.__Verificar(condition)):
            condition = condition.strip()
            condition_uri = URIRef(self.Popu.cit + self.Popu.Formato(condition))
            if ( (condition_uri, RDF.type, self.Popu.ecrm.E55_Type) in self.Popu.g): #tipo condicion existente
                self.__ScreenLog("Tipo Condición existente ... omitiendo")
                return condition_uri
            else: #add condition        
                return self.Popu.AddSubject(condition, "E55_Type")                
        else: #No condition info
            self.log.write(f"WARNING:Fila {self.row+2} -> Condición No identificada\n")
            return self.__condition_unknown
      
    def __VerifyMaterial(self, material: str):
        if ( self.__Verificar(material)):
            material = material.strip()
            material_uri = URIRef(self.Popu.cit + self.Popu.Formato(material))
            if ( (material_uri, RDF.type, self.Popu.ecrm.E55_Type) in self.Popu.g): #material existente
                self.__ScreenLog("Material existente ... omitiendo")
                return material_uri
            else: #add material        
                return self.Popu.AddSubject(material, "E57_Material")                
        else: #No material info
            self.log.write(f"WARNING:Fila {self.row+2} -> Material No identificado\n")
            return self.__material_unknown

    def __VerifyPlace(self, place: str):
        if ( self.__Verificar(place)):
            place = place.strip()
            place_uri = URIRef(self.Popu.cit + self.Popu.Formato(place))
            if ( (place_uri, RDF.type, self.Popu.ecrm.E55_Type) in self.Popu.g): #place existente
                self.__ScreenLog("Lugar(place) existente ... omitiendo")
                return place_uri
            else: #add place        
                return self.Popu.AddSubject(place, "E53_Place")                
        else: #No place info
            self.log.write(f"WARNING:Fila {self.row+2} -> Lugar No identificado\n")
            return self.__place_unknown

    def __ExtractNumber(self, dim : str):
        #Eliminar unidades de dim cm por defecto
        dim = str(dim).replace("cm", "")
        dim = dim.strip()
        return dim

    def __VerifyDimensions(self):
        dimen = self.Popu.AddSubjectFromURI(self.__conc_id, "/Measurements", "E54_Dimension")

        height = self.__ExtractNumber(self.data.iloc[self.row,self.__col_alto])
        width = self.__ExtractNumber(self.data.iloc[self.row,self.__col_ancho])
        length = self.__ExtractNumber(self.data.iloc[self.row,self.__col_largo])
        diameter = self.__ExtractNumber(self.data.iloc[self.row,self.__col_diametro]) #Museo Municipal
        depth = self.__ExtractNumber(self.data.iloc[self.row,self.__col_profundidad])
        weigth = self.__ExtractNumber(self.data.iloc[self.row,self.__col_peso])

        temp_log = ""

        if (height.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T3_has_height", height, "decimal")
        else:
            temp_log += "altura "

        if (width.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T4_has_width", width, "decimal")
        else:
            temp_log += "ancho "

        if (length.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T5_has_length", length, "decimal")
        else:
            temp_log += "largo "

        if (diameter.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T6_has_diameter", diameter, "decimal")
        else:
            temp_log += "diametro "

        if (depth.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T7_has_depth", depth, "decimal")
        else:
            temp_log += "profundidad "

        if (weigth.isnumeric() ):
            self.Popu.AddLiteralFromURI(dimen, "T8_has_weigth", weigth, "decimal")
        else:
            temp_log += "peso"

        if (temp_log != ""):
            self.log.write(f"WARNING:Fila {self.row+2} -> Dimensiones no identificadas: {temp_log}.\n")
        
        return dimen

    def __VerifyPeriods(self, period : str):
        
        def warning():
            self.log.write(f"WARNING:Fila {self.row+2} -> Periodo desconocido.\n")
            return self.__periodo_unknown, self.__periodo_span_unknown

        if ( self.__Verificar(period)):
            period = period.strip()
            period_uri = URIRef(self.Popu.cit + self.Popu.Formato(period))
         
            if ( (period_uri, RDF.type, self.Popu.ecrm.E4_Period) in self.period_graph):
                prop_uri = URIRef(self.Popu.ecrm + "P4_has_time-span")
                period_span = self.period_graph.value(period_uri, prop_uri)              
                return period_uri, period_span
            else:
                return warning()
        else:
            return warning()
            
        
            

    def __InitGeneralConcepts(self):
        # General Concepts
        #ID Type
        self.__type_id = self.Popu.AddSubject("ID-RUTAS", "E55_Type")
        #Measurement Unit
        self.__meas_cm = self.Popu.AddSubject("cm","E58_Measurement_Unit")

    def __InvalidRow(self):
        #Verify current row is valid: MainID and Title non empty
        if ( str(self.data.iloc[self.row, self.__col_codigo]) == 'nan' or
            str(self.data.iloc[self.row, self.__col_titulo]) == 'nan'):
            self.log.write(f"WARNING:Fila {self.row+2} -> no válida, no existe id/title\n")
            return True
        else:
            return False

    def __ProcessConcepts(self):
        #Main ID
        exist = self.__VerifyMainID(self.data.iloc[self.row,self.__col_codigo])
        self.__ScreenLog(self.__conc_id)
        if (exist): #Dont process row
            return
        #Alternative ID
        self.__alt_id = self.__VerifyAltId(self.data.iloc[self.row,self.__col_alt_code])
        #Main Tile
        self.__title_text = self.__VerifyMainTitle(self.data.iloc[self.row,self.__col_titulo])
        #Object are classified E22 by default, verify for problems
        self.__obj = self.Popu.AddSubjectFromURI(self.__conc_id, "/Object" , "E22_Man-Made_Object")
        self.Popu.AddLabel(self.__obj, self.__title_text)
        #Type Utility
        self.__utility = self.__VerifyUtility(self.data.iloc[self.row,self.__col_uso])
        #Object Creator, Donor, Owner
        self.__creator = self.__VerifyActor(self.data.iloc[self.row,self.__col_creador], "creator") 
        self.__donor = self.__VerifyActor(self.data.iloc[self.row,self.__col_donor], "donor")
        self.__owner = self.__VerifyActor(self.data.iloc[self.row,self.__col_duenio], "owner")
        #Artifact measurements
        self.__dimen = self.__VerifyDimensions() 
        #artifact condition type, material
        self.__type_condition = self.__VerifyObjectCondition(self.data.iloc[self.row,self.__col_estado])
        self.__condition = self.Popu.AddSubjectFromURI(self.__conc_id, "/Current_Condition", "E3_Condition_State")
        self.__material = self.__VerifyMaterial(self.data.iloc[self.row,self.__col_material])
        #Period
        self.__period, self.__period_span = self.__VerifyPeriods(self.data.iloc[self.row,self.__col_id_periodo]) 
        #Localization
        self.__localization = self.__VerifyPlace(self.data.iloc[self.row,self.__col_localizacion])
        self.__department = self.__VerifyPlace(self.data.iloc[self.row,self.__col_department])
        #Default concepts, check for problems
        #Production/Creation Event E12 by default
        self.__production = self.Popu.AddSubjectFromURI(self.__conc_id, "/Production", "E12_Production") 
        #Adquisition event E10 by default
        self.__adquisition = self.Popu.AddSubjectFromURI(self.__conc_id, "/Adquisition", "E10_Transfer_of_Custody") 

    def __ProcessProperties(self):
        #of the Artifact
        self.Popu.AddRelationFromURI(self.__obj, 'P48_has_preferred_identifier', self.__conc_id)
        self.Popu.AddRelationFromURI(self.__obj, 'P2_has_type', self.__utility)
        self.Popu.AddRelationFromURI(self.__obj, 'P50_has_current_keeper', self.__owner)
        self.Popu.AddRelationFromURI(self.__obj, 'P50_has_current_owner', self.__owner)
        self.Popu.AddRelationFromURI(self.__obj, 'P44_has_condition', self.__condition)
        self.Popu.AddRelationFromURI(self.__obj, 'P45_consists_of', self.__material)
        self.Popu.AddLiteralFromURI(self.__obj, 'P3_has_note', self.data.iloc[self.row, self.__col_descripcion], dtype="string", name_space="ecrm")
        self.Popu.AddRelationFromURI(self.__obj, 'P55_has_current_location', self.__localization)

        #of the Condition
        self.Popu.AddRelationFromURI(self.__condition, 'P44_has_type', self.__type_condition)

        #of the ID
        self.Popu.AddRelationFromURI(self.__conc_id, "P2_has_type", self.__type_id)
        if (self.__alt_id):
            self.Popu.AddRelationFromURI(self.__conc_id, "P139_has_alternative_form", self.__alt_id)

        # Dimension
        self.Popu.AddRelationFromURI(self.__dimen, "P91_has_unit", self.__meas_cm)

        # Production
        self.Popu.AddRelationFromURI(self.__production, "P108_has_produced", self.__obj)
        self.Popu.AddRelationFromURI(self.__production, "P14_carried_out_by", self.__creator)
        #self.Popu.AddLiteralFromURI(production, "P4_has_time-span", data.iloc[row, col_date_creation],
        #                        dtype="string", name_space="ecrm")
        #TODO Se esta considerando fecha de produccion igual a periodo ACTUALIZAR
        self.Popu.AddRelationFromURI(self.__production, "P4_has_time-span", self.__period_span)

        #Adquisition
        self.Popu.AddLiteralFromURI(self.__adquisition, 'P3_has_note', self.data.iloc[self.row,self.__col_desc_donor], dtype="string", name_space="ecrm")
        self.Popu.AddRelationFromURI(self.__adquisition, 'P30_transferred_custody_of', self.__obj)
        self.Popu.AddRelationFromURI(self.__adquisition, "P29_custody_received_by", self.__owner)
        self.Popu.AddRelationFromURI(self.__adquisition, "P28_custody_surrendered_by", self.__donor)

        #Localization
        self.Popu.AddRelationFromURI(self.__localization, 'P89_falls_within', self.__department)

    def Execute(self):
        try:
            self.__ReadColumnIndex()
        except KeyError as key:
            self.__ScreenLog(f"CSV column not found: {key}")
            return

        self.__InitUnknownConcepts()
        self.__InitGeneralConcepts()
        
        for self.row in range(0, self.num_filas):
            self.__ScreenLog("Procesando línea: " + str(self.row + 2))
            if (self.__InvalidRow()):
                continue
            else:     
                self.__ProcessConcepts()
                self.__ProcessProperties()
                    
        # Save individuals
        self.Popu.SaveTriples(self.onto_filename)

if __name__ == "__main__":
    Proceso = DataProcess(logf="log_prueba.txt",
        ontof="museo_prueba.ttl", csvf="municipal.csv", periodf="Instances/periodos.ttl")
    Proceso.Execute()