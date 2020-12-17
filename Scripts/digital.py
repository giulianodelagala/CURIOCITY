#Digital Representation
from poblar_onto import Populate
import urllib.parse
import pandas as pd

from rdflib import URIRef, Graph, Namespace

def LeerDatos(filename : str, header = True):
    if (header):
        data = pd.read_csv(filename + ".csv", sep ='\t', encoding='utf8', header = 0)
    else:
        data = pd.read_csv(filename+ ".csv", sep ='\t', header = None)
    #data = data.sample(frac = 1)
    #data = data.sort_values(data.columns[-1])
    #return np.array(data.iloc[:,:])
    return data

log = open("log_digital.txt", "w")

data = LeerDatos("ObjRGB")
num_filas = data.shape[0] #total de filas

#Column index from csv
col_codigo = data.columns.get_loc('Codigo')
col_file = data.columns.get_loc('Filename')

col_clasifica = data.columns.get_loc('Clasificacion')

col_R = data.columns.get_loc('R')
col_G = data.columns.get_loc('G')
col_B = data.columns.get_loc('B')
###############

#g = Graph()
#g.parse("../Curiocity_Turtle.owl", format="turtle")
#ecrm = Namespace("http://erlangen-crm.org/170309/")
#cit = Namespace("http://curiocity.org/")

#Load Ontology
Popu = Populate()
#Load Instances
instances = Graph()
instances.parse("museo.ttl", format = "turtle")

#########
# General Concepts
#########


#Add RGB Ranges TODO Confirmar si es necesario sino eliminar de ontologia
#a1 = Popu.AddSubject("A1_Range", "Range_RGB", "cit", False)
#Popu.AddLiteralFromURI(a1, "P3_has_note", "A1 Range: values of histogram from 0,0,0 to 20,20,20",
#                     "string", "ecrm")

#Add Concept Type (for Recognition purposes) TODO Llevarlo a todos los objetos
rec_type = Popu.AddSubject("Recognition_Concept", "E55_Type", ins_label=False)

ceramica = Popu.AddSubject("Ceramica como arte decorativo", "E55_Type", ins_label=True)
Popu.AddRelationFromURI(ceramica, "P_127_has_broader_term", rec_type)

pintura = Popu.AddSubject("Pintura de arte fino", "E55_Type", ins_label=True)
Popu.AddRelationFromURI(pintura, "P_127_has_broader_term", rec_type)

for row in range(0, num_filas):

    print ("Procesando: ", row + 2)

    if ( str(data.iloc[row, col_codigo]) == 'nan'):
        log.write(f"WARNING:Fila {row+2} -> no válida, no existe id/title\n")
        continue
    else:
        ##################
        #Search Repository 
        ##################

        pred = URIRef(Popu.ecrm + "P48_has_preferred_identifier")
        obj = URIRef(Popu.cit + data.iloc[row, col_codigo].strip())

        sub = instances.value( predicate=pred, object=obj)
        print(sub)
        ##########
        # Particular Concepts
        ##########
        #Digitization Process
        filename = data.iloc[row, col_file].strip()
        proc_rutas = Popu.AddSubject("Process_" + filename, "D2_Digitization_Process",
             name_space="cit", ins_label=False)
        #Image
        img = Popu.AddSubject( filename, "D9_Data_Object", name_space="cit", ins_label=False)
        #Popu.AddRelationFromURI(img, "P43_has_dimension", a1)
        Popu.AddLiteralFromURI(img, "T1_has_red_value", data.iloc[row,col_R], dtype="integer", name_space="cit")
        Popu.AddLiteralFromURI(img, "T1_has_green_value", data.iloc[row,col_G], dtype="integer", name_space="cit")
        Popu.AddLiteralFromURI(img, "T1_has_blue_value", data.iloc[row,col_B], dtype="integer", name_space="cit")

        Popu.AddLiteralFromURI(img, "T2_has_file_name", filename, dtype="string", name_space="cit")

        #Digitization Event Buscar en Repositorio el ID y asociar a concepto
        Popu.AddRelationFromURI(proc_rutas, "L1_digitized", sub) 
        Popu.AddRelationFromURI(proc_rutas, "L20_has_created", img)

        #Add Concept Type to Object (for Recognition purposes) TODO 
        if (data.iloc[row, col_clasifica].strip() == "Ceramica como arte decorativo"):
            Popu.AddRelationFromURI(sub, "P2_has_type", ceramica)
        elif (data.iloc[row, col_clasifica].strip() == "Pintura de arte fino"):
            Popu.AddRelationFromURI(sub, "P2_has_type", pintura)

#Save Instantiation
Popu.SaveTriples("digital.ttl")