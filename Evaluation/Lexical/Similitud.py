#Calculo de Similitud
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL
from rdflib.plugins.sparql import prepareQuery

from scipy import spatial
import numpy as np
import editdistance as ed
import math

def getEntities(nameOntology):
    g = Graph()
    g.parse(nameOntology, format='turtle')
    print("Analizing :", nameOntology)

    qent = prepareQuery("""SELECT ?lab
                        WHERE {
                            VALUES ?tipo { owl:Class owl:DatatypeProperty owl:ObjectProperty }
                            ?s a ?tipo ;
                                rdfs:label ?lab ;                                
                            }""",
                            initNs= {"owl": OWL} )

    entities = g.query(qent)
    entities = set(entities)
    return entities


def stringSim(str1,str2):
    edVal = ed.eval(str1,str2)
    mod = np.absolute(len(str1)+len(str2) - edVal)
    return 1/(math.exp(edVal/mod))

def calcStringSim(list1, list2, ro):
    dupEnt = 0
    simEnt = 0
    for i in range(0,len(list1)):
        for j in range(0,len(list2)):
            if list1[i] == list2[j]:
                dupEnt = dupEnt+1
            if stringSim(list1[i],list2[j]) > ro:
                simEnt = simEnt+1
    print("Entidades similares ",simEnt)
    print("Entidades duplicadas ",dupEnt)
    simm = simEnt / (len(list1)+len(list2)-dupEnt)
    return simm

def cosineSimilarity():
    with open("Erlangen_TURTLE.owl" ,"r+", encoding="utf8") as file:
        file_string = file.read()
        mat1 = np.zeros((len_bag))
        for i in range(0,len_bag):
            mat1[i] = file_string.count(bag[i])
        file.close()

    with open("Curiocity_Time.ttl","r+", encoding="utf8") as file:
        file_string = file.read()
        mat2 = np.zeros( (len_bag)) 
        for i in range(0,len_bag):
            mat2[i] = file_string.count(bag[i])
        file.close()

    mattf1 = np.zeros( (len_bag)) 
    mattf2 = np.zeros( (len_bag))
    for i in range(0,len_bag):
        if mat1[i] > mat2[i]:
            mattf1[i] =  mat1[i]/ mat1[i]
            mattf2[i] =  mat2[i]/ mat1[i]
        else:
            mattf1[i] =  mat1[i]/ mat2[i]
            mattf2[i] =  mat2[i]/ mat2[i]


    matidf = np.zeros((len_bag))
    for i in range(0,len_bag):
        if mat1[i] > 0 and mat2[i] > 0:
            matidf[i] =  0.5* (1+np.log2(1)) #Aparece en 2 docs
        else:
            matidf[i] =  0.5* (1+np.log2(2)) #Aparece en 1 doc

    matW1 = np.zeros((len_bag))
    matW2 = np.zeros((len_bag))
    for i in range(0,len_bag):
        matW1[i] = mattf1[i] * matidf[i]
        matW2[i] = mattf2[i] * matidf[i]

  
    dist_cosine = 1 -spatial.distance.cosine(matW1, matW2)
    print ("Similaridad Cosine", dist_cosine)
    sim = 0.7* dist_cosine + 0.3*finSimm
    print ("Similaridad Lexica "+str(sim))


if __name__ == "__main__":
    
    curiocity = [i[0].value for i in getEntities("Curiocity_Time.ttl") ]
    print (len(curiocity))

    erlangen = [i[0].value for i in getEntities("Erlangen_TURTLE.owl") ]
    print (len(erlangen))


    finSimm = calcStringSim(curiocity, erlangen, 0.99 )
    print("Similaridad:", finSimm)
 
    set_curio = set(curiocity)
    set_erlangen = set(erlangen)

    bag = set_curio.union(set_erlangen)
    bag = list(bag)
    len_bag = len(bag)
    print("Numero de Terminos ", len(bag))

    cosineSimilarity()

    
