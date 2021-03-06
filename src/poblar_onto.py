#Script para Poblamiento de Ontologia

from rdflib import Graph, Literal, RDF, URIRef, Namespace, term
from rdflib.namespace import RDF, OWL, FOAF, RDFS, XSD, TIME
import urllib.parse

#WARNING Rdflib gYear workaround
term._toPythonMapping.pop(XSD['gYear'])

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
        self.g.bind("time", TIME)

        #self.map_entidad = {"place" : self.ecrm.E53_Place }

    #Carga de Ontologia NO UTILIZAR
    # def getEntities(self, nameOntology: str, format: str):
    #     g = Graph()
    #     g.parse(nameOntology, format= format)
    #     print("Loading :", nameOntology)

    #     # loop through each triple in the graph (subj, pred, obj)
    #     for subj, pred, obj in g:
    #         # check if there is at least one triple in the Graph
    #         if (subj, pred, obj) not in g:
    #             raise Exception("It better be!")

    #     print( f"graf has {len(g)} statements")

    #     save_file = g.serialize(format="turtle").decode("utf-8")
    #     f = open("archivo.ttl", "w")
    #     f.write(save_file)
    #     f.close()

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
    
    def AddSubjectFromURI(self, root, name:str, concept:str, name_space = "ecrm"):
        var_ = URIRef(root + name)
        if (name_space == "ecrm"):
            space = self.ecrm
        elif (name_space == "cit"):
            space = self.cit
        elif (name_space == "time"):
            space = TIME

        conc = URIRef(space + concept)
        
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

    def AddRelationFromURI(self, subject, predicate, object, name_space = "ecrm"):
        if (name_space == "ecrm"):
            pre = URIRef(self.ecrm + predicate)
        elif (name_space == "cit"):
            pre = URIRef(self.cit + predicate)
        elif (name_space == "time"):
            pre = URIRef(TIME + predicate )
        
        #pre = URIRef(self.ecrm + predicate)
        self.g.add((subject, pre, object))

    def AddLiteralFromURI(self, subject, predicate, object, dtype, name_space = "cit"):
        
        if (name_space == "ecrm"):
            pre = URIRef(self.ecrm + predicate)
        elif (name_space == "cit"):
            pre = URIRef(self.cit + predicate)
        elif (name_space == "time"):
            pre = URIRef(TIME + predicate )

        if (dtype == "string"):
            dt = XSD.string
        elif (dtype == "decimal"):
            dt = XSD.decimal
        elif (dtype == "year"):
            dt = URIRef(u'http://www.w3.org/2001/XMLSchema#gYear')
        elif (dtype == "date"):
            dt = XSD.date
        elif (dtype == "integer"):
            dt = XSD.integer

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