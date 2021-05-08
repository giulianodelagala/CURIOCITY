#Procesamiento de Data
from poblar_onto import Populate
from rdflib import RDF, OWL, URIRef, Graph
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


#Logfile name
log = open("log_catalina.txt", "w")

#Database CSV file Name
data = LeerDatos("catalina")
num_filas = data.shape[0] #total de filas

#Column index from csv
#col_codigo = data.columns.get_loc('Código único en la database')
col_codigo = data.columns.get_loc('Código único en la database para el objeto')
col_alt_code = data.columns.get_loc('Número/código asignado por el museo desde ingreso a ser expuesto')

col_titulo = data.columns.get_loc('Título principal del objeto u obra de arte')
col_descripcion = data.columns.get_loc('Descripción o nota asociada al objeto')

col_creador = data.columns.get_loc('Creador del objeto')

#col_uso = data.columns.get_loc('Uso que se le dio al objeto')
col_uso = data.columns.get_loc('Uso que se le dio al objeto') #Museo Municipal
col_duenio = data.columns.get_loc('Dueño actual')
col_estado = data.columns.get_loc('Estado actual del objeto')
col_material = data.columns.get_loc('Material del objeto (TECNICA USADA)') #Museo Municipal
#col_material = data.columns.get_loc('Material del objeto (tècnica usada)')

col_id_periodo = data.columns.get_loc('Código del Período o evento') #Museo Municipal
#col_id_periodo = data.columns.get_loc('Código Período')
col_periodo = data.columns.get_loc('Periodo, evento')

col_date_creation = data.columns.get_loc('Fecha de creación del objeto/obra de arte') #Museo Municipal
#col_date_creation = data.columns.get_loc('Fecha de creación del objeto/obra de arte o Código de la Fecha')

#col_adquisicion = data.columns.get_loc('Forma como fue adquirido el objeto') #Museo Municipal
col_adquisicion = data.columns.get_loc('Forma como fue adquirido el objeto (por el museo)')
col_donor = data.columns.get_loc('Identifica y da crédito a la persona, fundación o método por el cual el objeto fue adquirido  (del/a cual fue adquirido el objeto)')
#col_desc_donor = data.columns.get_loc('Descripción de donación')
#TODO probable organizacion de descripciones

col_localizacion = data.columns.get_loc('Localización del objeto dentro del museo')
col_department = data.columns.get_loc('Departamento dentro del museo responsable por el objeto')

col_alto = data.columns.get_loc('Dimensión: Alto') #Museo Municipal
#col_alto = data.columns.get_loc('Dimensión: Alto en centímetros')
col_ancho = data.columns.get_loc('Dimensión: Ancho') #Museo Municipal
#col_ancho = data.columns.get_loc('Dimensión: Ancho en centímetros')
col_largo = data.columns.get_loc('Dimensión: Largo') #Museo Municipal
#col_largo = data.columns.get_loc('Dimensión: Largo en centímetros') 
col_diametro = data.columns.get_loc('Dimensión: Diámetro') #Museo Municipal
col_profundidad = data.columns.get_loc('Profundidad') #Museo Municipal
#col_profundidad = data.columns.get_loc('Dimensión: Profundidad en centímetros') 
col_peso = data.columns.get_loc('Peso')

#Load Ontology
Popu = Populate()
#Load Period Graph
period_graph = Graph()
period_graph.parse("periodos.ttl", format="turtle")

#Verificar si campo es legal TODO agregar otras condiciones
def Verificar(cadena: str):
    if (str(cadena) != "No asignado" and 
        str(cadena) != 'nan' and 
        str(cadena) != 'No aplicable' and 
        str(cadena) != 'Desconocida' and
        str(cadena) != 'Desconocido' and
        str(cadena) != 'No definido'):
        return True
    else:
        return False

def VerificarActorv2(actor: str):
    #Verificar si actor existe y devolver URI
    actor = URIRef(Popu.cit + Popu.Formato(actor))
    qactor = prepareQuery("""SELECT ?s
                        WHERE {
                            VALUES ?type { ecrm:E21_Person ecrm:E74_Group }
                            ?s a ?type .                                
                            }""",
                            initNs= {"ecrm" : Popu.ecrm,
                                "cit": Popu.cit,
                                "owl": OWL} )

    actor_q = Popu.g.query(qactor, initBindings={'s': actor})
    return actor_q

def VerificarActor(actor : str, tipo:str):
    if ( Verificar(actor)):
        actor_uri = URIRef(Popu.cit + Popu.Formato(actor))

        if ( (actor_uri, RDF.type, Popu.ecrm.E21_Person) in Popu.g): #existe como persona
            print("Person existente ... omitiendo")
            return actor_uri
        elif ( (actor_uri, RDF.type, Popu.ecrm.E74_Group) in Popu.g): #existe como grupo
            print("Group existente ... omitiendo")
            return actor_uri
        else: #Pedir confirmacion
            while (True):
                actor_type = input(f"¿{actor} es [p]erson o [g]roup?")
                if (actor_type == 'p'):
                    return Popu.AddSubject(actor, "E21_Person")
                elif (actor_type == 'g'):
                    return Popu.AddSubject(actor, "E74_Group")
                else:
                    continue   
    else: #No hay info de Actor
        if (tipo == "creator"):
            log.write(f"WARNING:Fila {row+2} -> Creador No identificado\n")
            return creator_unknown
        elif (tipo == "donor"):
            log.write(f"WARNING:Fila {row+2} -> Donador No identificado\n")
            return donor_unknown
        elif (tipo == "owner"):
            log.write(f"WARNING:Fila {row+2} -> Propietario No identificado\n")
            return owner_unknown

                   
def MainID(id_text : str):
    subject = URIRef(Popu.cit + id_text)
    if ( (subject, RDF.type, Popu.ecrm.E42_Identifier) in Popu.g):
        log.write(f"ERROR:Fila {row+2} -> Codigo existente: {id_text}, Fila ignorada\n")
        return "ERROR -> Codigo existente", True
    else:    
        conc_id = Popu.AddSubject(id_text, "E42_Identifier")
        Popu.AddLiteralFromURI(conc_id, "P190_has_symbolic_content", id_text, "string")
        return conc_id, False

def AltId(alt_id_text):
    if (Verificar(alt_id_text) ):
        alt_id = Popu.AddSubjectFromURI(conc_id, "/IDalternativo", "E42_Identifier")
        Popu.AddLiteralFromURI(alt_id, "P190_has_symbolic_content", alt_id_text, "string")
        return alt_id
    else:
        log.write(f"WARNING:Fila {row+2} -> Codigo alternativo No Asignado\n")
        return alt_id_unknown

def MainTitle(title : str):
    if (Verificar(title)):
        return title #TODO Crear Title Concept
    else:
        log.write(f"WARNING:Fila {row+2} -> Titulo no asignado\n")
        return "Sin título"

def VerificarManMadeOrNatural(object: str):
    while (True):
        object_type = input(f"¿{object} es [h]uman made o [n]atural?")
        if (object_type == 'h'):
            return Popu.AddSubjectFromURI(conc_id, "/Object", "E22_Man-Made_Object")
        elif (object_type == 'n'):
            return Popu.AddSubjectFromURI(conc_id, "/Object", "E19_Physical_Object")
        else:
            continue

def Utility(utility_text: str):
    if (Verificar(utility_text) ):
        utility = Popu.AddSubjectFromURI(conc_id, "/Utility", "E55_Type")
        Popu.AddLabel(utility, utility_text)
        return utility
    else:
        log.write(f"WARNING:Fila {row+2} -> Utilidad desconocidad\n")
        return utility_unknown

def ObjectCondition(condition: str):
    if ( Verificar(condition)):
        condition_uri = URIRef(Popu.cit + Popu.Formato(condition))
        if ( (condition_uri, RDF.type, Popu.ecrm.E55_Type) in Popu.g): #tipo condicion existente
            print("Tipo Condición existente ... omitiendo")
            return condition_uri
        else: #add condition        
           return Popu.AddSubject(condition, "E55_Type")                
    else: #No condition info
        log.write(f"WARNING:Fila {row+2} -> Condición No identificada\n")
        return condition_unknown
      
def Material(material: str):
    if ( Verificar(material)):
        material_uri = URIRef(Popu.cit + Popu.Formato(material))
        if ( (material_uri, RDF.type, Popu.ecrm.E55_Type) in Popu.g): #material existente
            print("Material existente ... omitiendo")
            return material_uri
        else: #add material        
           return Popu.AddSubject(material, "E57_Material")                
    else: #No material info
        log.write(f"WARNING:Fila {row+2} -> Material No identificado\n")
        return material_unknown

def Place( place: str):
    if ( Verificar(place)):
        place_uri = URIRef(Popu.cit + Popu.Formato(place))
        if ( (place_uri, RDF.type, Popu.ecrm.E55_Type) in Popu.g): #place existente
            print("Lugar(place) existente ... omitiendo")
            return place_uri
        else: #add place        
           return Popu.AddSubject(place, "E53_Place")                
    else: #No place info
        log.write(f"WARNING:Fila {row+2} -> Lugar No identificado\n")
        return place_unknown

def ExtractNumber(dim : str):
    #Eliminar unidades de dim cm por defecto
    dim = str(dim).replace("cm", "")
    dim = dim.strip()
    return dim

def Dimensions():
    dimen = Popu.AddSubjectFromURI(conc_id, "/Measurements", "E54_Dimension")
    
    height = ExtractNumber(data.iloc[row,col_alto])
    width = ExtractNumber(data.iloc[row,col_ancho])
    length = ExtractNumber(data.iloc[row,col_largo])
    diameter = ExtractNumber(data.iloc[row,col_diametro]) #Museo Municipal
    depth = ExtractNumber(data.iloc[row,col_profundidad])
    weigth = ExtractNumber(data.iloc[row,col_peso])

    temp_log = ""

    if (height.isnumeric() ):
        Popu.AddLiteralFromURI(dimen, "T3_has_height", height, "decimal")
    else:
        temp_log += "altura "

    if (width.isnumeric() ):
        Popu.AddLiteralFromURI(dimen, "T4_has_width", width, "decimal")
    else:
        temp_log += "ancho "

    if (length.isnumeric() ):
        Popu.AddLiteralFromURI(dimen, "T5_has_length", length, "decimal")
    else:
        temp_log += "largo "

    #Museo Municipal
    if (diameter.isnumeric() ):
       Popu.AddLiteralFromURI(dimen, "T6_has_diameter", diameter, "decimal")
    else:
       temp_log += "diametro "

    if (depth.isnumeric() ):
        Popu.AddLiteralFromURI(dimen, "T7_has_depth", depth, "decimal")
    else:
        temp_log += "profundidad "

    if (weigth.isnumeric() ):
        Popu.AddLiteralFromURI(dimen, "T8_has_weigth", weigth, "decimal")
    else:
        temp_log += "peso"

    if (temp_log != ""):
        log.write(f"WARNING:Fila {row+2} -> Dimensiones no identificadas: {temp_log}.\n")
    
    return dimen

def ProcPeriods(period : str):
    period_uri = URIRef(Popu.cit + Popu.Formato(period))
    if ( (period_uri, RDF.type, Popu.ecrm.E4_Period) in period_graph): #material existente
        prop_uri = URIRef(Popu.ecrm + "P4_has_time-span")
        period_span = period_graph.value(period_uri, prop_uri)    
        
        return period_uri, period_span
    else:
        log.write(f"WARNING:Fila {row+2} -> Periodo desconocido.\n")
        return periodo_unknown, periodo_span_unknown

########################
# Unknown Concepts
########################
alt_id_unknown = Popu.AddSubject("ID_alternativo_desconocido", "E42_Identifier", ins_label=False)
utility_unknown = Popu.AddSubject("Utilidad_desconocida", "E55_Type", ins_label=False)
creator_unknown = Popu.AddSubject("Creador_desconocido", "E39_Actor", ins_label=False)
donor_unknown = Popu.AddSubject("Donador_desconocido", "E39_Actor", ins_label=False)
owner_unknown = Popu.AddSubject("Propietario_desconocido", "E39_Actor", ins_label=False)
condition_unknown = Popu.AddSubject("Condicion_desconocida", "E55_Type", ins_label=False)
material_unknown = Popu.AddSubject("Material_desconocido", "E57_Material", ins_label=False)
place_unknown = Popu.AddSubject("Lugar_desconocido", "E53_Place", ins_label=False)
periodo_unknown = Popu.AddSubject("Periodo_desconocido", "E4_Period", ins_label=False)
periodo_span_unknown = Popu.AddSubject("Lapso_de_Tiempo_desconocido", "SP10_Declarative_Time-Span", name_space="cit" ,ins_label=False)

##################
# General Concepts
##################
#ID Type
type_id = Popu.AddSubject("ID-RUTAS", "E55_Type")

#Measurement Unit
meas_cm = Popu.AddSubject("cm","E58_Measurement_Unit")

for row in range(0, num_filas):

    #Verificar que es una fila con un objeto valido
    #MainID and Title non empty
    print ("Procesando: ", row + 2)
    if ( str(data.iloc[row, col_codigo]) == 'nan' or str(data.iloc[row,col_titulo]) == 'nan'):
        log.write(f"WARNING:Fila {row+2} -> no válida, no existe id/title\n")
    
    else:     
        #############
        # Concepts
        #############

        #Main ID
        conc_id, existe = MainID(data.iloc[row,col_codigo].strip())
        print (conc_id)
        if (existe): #No procesar fila
            continue

        alt_id = AltId (data.iloc[row,col_alt_code].strip()) #Alternative ID
        
        title_text = MainTitle( data.iloc[row,col_titulo].strip()) #Main Tile
        #Object are classified E22 by default, verify for problems
        obj = Popu.AddSubjectFromURI(conc_id, "/Object" , "E22_Man-Made_Object")
        Popu.AddLabel(obj, title_text)

        utility = Utility( data.iloc[row,col_uso].strip() ) #Type Utility

        creator = VerificarActor(data.iloc[row,col_creador].strip(), "creator") #Object Creator
        donor = VerificarActor( data.iloc[row,col_donor].strip(), "donor") #Object Donor
        owner = VerificarActor ( data.iloc[row,col_duenio].strip(), "owner") #Object Owner

        dimen = Dimensions() #Artifact measurements

        type_condition = ObjectCondition(data.iloc[row,col_estado].strip() ) #artifact condition type
        condition = Popu.AddSubjectFromURI(conc_id, "/Current_Condition", "E3_Condition_State")

        material = Material(data.iloc[row,col_material].strip() ) #artifact material

        period, period_span = ProcPeriods(data.iloc[row,col_id_periodo].strip()) #Period
        
        #Localization
        localization = Place( data.iloc[row, col_localizacion].strip() )
        department = Place ( data.iloc[row, col_department].strip() )
   
        #Default concepts, check for problems
        production = Popu.AddSubjectFromURI(conc_id, "/Production", "E12_Production") #Production/Creation Event E12 by default
        adquisition = Popu.AddSubjectFromURI(conc_id, "/Adquisition", "E10_Transfer_of_Custody") #Adquisition event E10 y default
              
        ############
        # Properties
        ############

        #of the Artifact
        Popu.AddRelationFromURI(obj, 'P48_has_preferred_identifier', conc_id)
        Popu.AddRelationFromURI(obj, 'P2_has_type', utility)
        Popu.AddRelationFromURI(obj, 'P50_has_current_keeper', owner)
        Popu.AddRelationFromURI(obj, 'P50_has_current_owner', owner)
        Popu.AddRelationFromURI(obj, 'P44_has_condition', condition)
        Popu.AddRelationFromURI(obj, 'P45_consists_of', material)
        Popu.AddLiteralFromURI(obj, 'P3_has_note', data.iloc[row, col_descripcion], dtype="string", name_space="ecrm")
        Popu.AddRelationFromURI(obj, 'P55_has_current_location', localization)

        #of the Condition
        Popu.AddRelationFromURI(condition, 'P44_has_type', type_condition)

        #of the ID
        Popu.AddRelationFromURI(conc_id, "P2_has_type", type_id)
        if (alt_id):
            Popu.AddRelationFromURI(conc_id, "P139_has_alternative_form", alt_id)

        # Dimension
        Popu.AddRelationFromURI(dimen, "P91_has_unit", meas_cm)

        # Production
        Popu.AddRelationFromURI(production, "P108_has_produced", obj)
        Popu.AddRelationFromURI(production, "P14_carried_out_by", creator)
        #Popu.AddLiteralFromURI(production, "P4_has_time-span", data.iloc[row, col_date_creation],
        #                        dtype="string", name_space="ecrm")
        #TODO Se esta considerando fecha de produccion igual a periodo ACTUALIZAR
        Popu.AddRelationFromURI(production, "P4_has_time-span", period_span)

        #Adquisition
        #Popu.AddLiteralFromURI(adquisition, 'P3_has_note', data.iloc[row,col_desc_donor], dtype="string", name_space="ecrm") #Museo Municipal
        Popu.AddRelationFromURI(adquisition, 'P30_transferred_custody_of', obj)
        Popu.AddRelationFromURI(adquisition, "P29_custody_received_by", owner)
        Popu.AddRelationFromURI(adquisition, "P28_custody_surrendered_by", donor)

        #Localization
        Popu.AddRelationFromURI(localization, 'P89_falls_within', department)


log.close()

#############################
# Save individuals
Popu.SaveTriples("museo_santa_catalina.ttl")

