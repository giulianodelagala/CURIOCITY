#Digital Representation
from poblar_onto import Populate
import urllib.parse
import pandas as pd

from rdflib import URIRef, Graph, Namespace

def LeerDatos(filename : str, header = True):
    if (header):
        data = pd.read_csv(filename + ".csv", sep =';', encoding='utf8', header = 0)
    else:
        data = pd.read_csv(filename+ ".csv", sep ='\t', header = None)
    #data = data.sample(frac = 1)
    #data = data.sort_values(data.columns[-1])
    #return np.array(data.iloc[:,:])
    return data

g = Graph()
g.parse("../Curiocity_Turtle.owl", format="turtle")
ecrm = Namespace("http://erlangen-crm.org/170309/")
cit = Namespace("http://curiocity.org/")

Popu = Populate()

##################
#Search Repository
##################

pred = URIRef(ecrm + "P48_has_preferred_identifier")
obj = URIRef(cit + "m_01_s01_002")

sub = g.value( predicate=pred, object=obj)

#########
# General Concepts
#########

proc_rutas = Popu.AddSubject("Procesamiento_RUTAS", "D2_Digitization_Process",
             name_space="cit", ins_label=False)

#Add RGB Ranges
a1 = Popu.AddSubject("A1_Range", "Range_RGB", "cit", False)
Popu.AddLiteralFromURI(a1, "P3_has_note", "A1 Range: values of histogram from 0,0,0 to 20,20,20",
                     "string", "ecrm")

#Add Concept Type (for Recognition purposes)
rec_type = Popu.AddSubject("Recognition_Concept", "E55_Type", ins_label=False)

armamento = Popu.AddSubject("Armamento", "E55_Type", ins_label=False)
Popu.AddRelationFromURI(armamento, "P_127_has_broader_term", rec_type)

##########
# Particular Concepts
##########

#Main ID
#conc_id = Popu.AddSubject("m01_s01_002", "E42_Identifier", ins_label=False)
#Popu.AddLiteralFromURI(conc_id, "P190_has_symbolic_content", "m01_s01_002", "string")

#Image
img = Popu.AddSubject("imagen_01_m01_s01_002", "D9_Data_Object", name_space="cit", ins_label=False)
Popu.AddRelationFromURI(img, "P43_has_dimension", a1)
Popu.AddLiteralFromURI(img, "T1_has_rgb_value", "200,200,200", dtype="string", name_space="cit")
Popu.AddLiteralFromURI(img, "T2_has_file_name", "m01_s01_002.jpg", dtype="string", name_space="cit")

#Digitization Event Buscar en Repositorio el ID y asociar a concepto
Popu.AddRelationFromURI(proc_rutas, "L1_digitized", sub) 
Popu.AddRelationFromURI(proc_rutas, "L20_has_created", img)

#Add Concept Type to Object (for Recognition purposes)
Popu.AddRelationFromURI(sub, "P2_has_type", armamento)

#Save Instantiation
Popu.SaveTriples("digital.ttl")