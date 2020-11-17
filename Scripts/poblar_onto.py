#Script para Poblamiento de Ontologia

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDF, OWL, FOAF, RDFS, XSD
import urllib.parse

class Populate():
    def __init__ (self):
        self.g = Graph()
        #Default namespace
        self.g.namespace_manager.bind('', URIRef('http://curiocity.org/'))
        self.cit = Namespace("http://curiocity.org/")
        #Namespaces
        self.ecrm = Namespace("http://erlangen-crm.org/170309/")

        

        #Prefijos
        self.g.bind("owl", OWL)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("ecrm", self.ecrm)

        #self.map_entidad = {"place" : self.ecrm.E53_Place }

    #Carga de Ontologia NO UTILIZAR
    def getEntities(self, nameOntology: str, format: str):
        g = Graph()
        g.parse(nameOntology, format= format)
        print("Loading :", nameOntology)

        # loop through each triple in the graph (subj, pred, obj)
        for subj, pred, obj in g:
            # check if there is at least one triple in the Graph
            if (subj, pred, obj) not in g:
                raise Exception("It better be!")

        print( f"graf has {len(g)} statements")

        save_file = g.serialize(format="turtle").decode("utf-8")
        f = open("archivo.ttl", "w")
        f.write(save_file)
        f.close()

    '''
    def AddPerson(self, name:str):     
        person = self.cit[name]    
        #Add triple
        self.g.add((person, RDF.type, OWL.NamedIndividual))
        self.g.add((person, RDF.type, self.ecrm.E21_Person))

    def AddType(self, name:str):     
        var_ = self.cit[name]    
        #Add triple
        self.g.add((var_, RDF.type, OWL.NamedIndividual))
        self.g.add((var_, RDF.type, self.ecrm.E55_Type))

    def AddPlace(self, name:str):     
        var_ = self.cit[name]    
        #Add triple
        self.g.add((var_, RDF.type, OWL.NamedIndividual))
        self.g.add((var_, RDF.type, self.ecrm.E53_Place))

    def AddManMadeObject(self, name:str): #TODO    
        var_ = self.cit[name]    
        #Add triple
        e22 = URIRef(self.ecrm + "E22_Man-Made_Object")  
        self.g.add((var_, RDF.type, OWL.NamedIndividual))
        self.g.add((var_, RDF.type, e22))
        
    def AddHasType(self, name:str, type_:str =""): #TODO    
        var_ = self.cit[name]    
        #Add triple
        #self.g.add((var_, RDF.type, OWL.NamedIndividual))
        tipo = URIRef(self.cit + type_)
        self.g.add((var_, self.ecrm.P2_has_type, tipo))
    '''
    def Formato(self, cadena: str):
        #Converse to required URI format
        cadena = cadena.replace(" ", "_")
        return urllib.parse.quote(cadena)

    def AddSubject(self, name:str, concept:str, name_space = "ecrm", ins_label = True):
        #ins_label Insert Label
        #name_format = self.Formato(name) 
        var_ = self.cit[self.Formato(name)]
        if (name_space == "ecrm"):
            space = self.ecrm
        elif (name_space == "cit"):
            space = self.cit
        conc = URIRef(space + concept)  
        #Add triple
        self.g.add((var_, RDF.type, OWL.NamedIndividual))
        self.g.add((var_, RDF.type, conc))
        if (ins_label):
            self.AddLabel(var_, name)
        return var_
    
    def AddSubjectFromURI(self, root, name:str, concept:str):
        #TODO modificar para aceptar namespace
        var_ = URIRef(root + name)
        conc = URIRef(self.ecrm + concept)
        self.g.add((var_, RDF.type, OWL.NamedIndividual))
        self.g.add((var_, RDF.type, conc))
        return var_

    def AddLabel(self, root, label_:str):
        self.g.add((root, RDFS.label, Literal(label_, datatype=XSD.string)))
      
    def AddRelation(self, subject:str, predicate:str, object:str):
        var_ = self.cit[subject]
        obj = URIRef(self.ecrm + object)
        pre = URIRef(self.ecrm + predicate)
        self.g.add((var_, pre, obj))

    def AddRelationFromURI(self, subject, predicate, object):
        pre = URIRef(self.ecrm + predicate)
        self.g.add((subject, pre, object))

    def AddLiteralFromURI(self, subject, predicate, object, dtype, name_space = "cit"):
        
        if (name_space == "ecrm"):
            pre = URIRef(self.ecrm + predicate)
        elif (name_space == "cit"):
            pre = URIRef(self.cit + predicate)

        if (dtype == "string"):
            dt = XSD.string
        self.g.add((subject, pre, Literal(object, datatype=dt)))

    def SaveTriples(self, file_name:str, format:str = "turtle"):
        save_file = self.g.serialize(format=format).decode('utf-8') #decode("unicode-escape")
        f = open(file_name, "w")
        f.write(save_file)
        f.close()

if __name__ == "__main__":
    #getEntities("Curiocity_Turtle.owl", "turtle")
    Popu = Populate()
    #Popu.AddPerson("Juan-Perez")
    #Popu.AddType("Copy")

    #Popu.AddManMadeObject("Lacoon")
    #Popu.AddHasType("Lacoon", "Copy")
    #Popu.AddHasType("Lacoon", "Hellenistic")
    Popu.AddSubject("Anna-Maria_Meyer", "E21_Person")
    Popu.AddSubject("Lacoon_Group", "E22_Man-Made_Object")
    Popu.AddSubject("History_of_the_Art_of_Antiquity", "E73_Information_Object")

    Popu.AddRelation("History_of_the_Art_of_Antiquity", "P67_refers_to", "Lacoon_Group")

    Popu.SaveTriples("archivo.ttl")