from typing import List
#from owlready2 import *
#from rdflib import graph

#from rdflib.plugins.sparql import prepareQuery
import requests
from requests.api import request
from requests.models import Response


class QueryProcess():
    def __init__(self):
        self.connection_path = 'http://localhost:3030/dataset/query'

        self.q_comb_base = """
            #Combination Query
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX cit: <http://curiocity.org/>
            SELECT ?id_l ?artifact_l ?author_l ?material_l ?location_l
            ?period_l ?begin_d ?end_d ?note ?donor_l ?note_donor
            WHERE {
            VALUES ?type { time:in_XSD_date time:in_XSD_g-Year }
            ?artifact a ecrm:E22_Man-Made_Object ;
                rdfs:label ?artifact_l ; #Title
                ecrm:P48_has_preferred_identifier ?id ;
                ecrm:P55_has_current_location ?location ;
                ecrm:P3_has_note ?note .
            ?id rdfs:label ?id_l .
            ?location rdfs:label ?location_l .
            ?prod ecrm:P108_has_produced ?artifact ;
                    ecrm:P14_carried_out_by ?author ;
                    ecrm:P4_has_time-span ?timespan .
            ?period a ecrm:E4_Period ;
                    ecrm:P4_has_time-span ?timespan ;
                    rdfs:label ?period_l .
            ?interval cit:Q14_defines_time ?timespan ;
                        time:hasBeginning ?begin ;
                        time:hasEnd ?end .
            ?begin ?type ?begin_d .
            ?end ?type ?end_d .
            ?author rdfs:label ?author_l .
            ?artifact ecrm:P45_consists_of ?material .
            ?material rdfs:label ?material_l .
            ?transfer a ecrm:E10_Transfer_of_Custody ;
                        ecrm:P30_transferred_custody_of ?artifact ;
                        ecrm:P28_custody_surrendered_by ?donor ;
                        ecrm:P29_custody_received_by ?receiver ;
                        ecrm:P3_has_note ?note_donor .
                ?donor rdfs:label ?donor_l .
                ?receiver rdfs:label ?receiver_l .
            FILTERS
            }"""

    def testConnection(self, endpoint):
        response = requests.post(endpoint,
            data={'query': 'ASK { ?s ?p ?o . }'})
        try:
            if ( response.json()['boolean']):
                self.connection_path = endpoint
                return True
            else:
                return False
        except:
            return False

        
    def LoadOnto(self, ontofile:str):
        #self.ontofile = ontofile
        try:
            #self.world.get_ontology("file://" + ontofile).load()
            #self.graph = self.world.as_rdflib_graph()
            #self.world.set_backend(filename = "Curiocity_backend.sqlite3", exclusive = False)
            #self.graph = self.world.as_rdflib_graph()
            #self.g.parse(ontofile)
            return True
        except:
            return False

    def combinedQuery(self, data:List):
        dic_query = {
            'Title'     : "?artifact_l",
            'Author'    : "?author_l",
            'Material'  : "?material_l",
            'Location'  : "?location_l",
            'Period'    : "?period_l"
        }
        q_filter = ""
        #Get list of querys and create appropiate Filter
        for i in range(0, len(data)):
            q_filter += "FILTER (regex(" + dic_query[data[i][1]] + ", \"" + data[i][0] + "\", \"i\"))\n"
        q_ready = self.q_comb_base.replace("FILTERS", q_filter)
       
        response = requests.post(self.connection_path,
            data={'query': q_ready}).json()
        row_return = []
        for item in response['results']['bindings']:
            row = []
            for field in item:
                row.append(item[field]['value'])
            row_return.append(row)
        return row_return

    def customQuery(self, query:str):
        response = requests.post(self.connection_path,
            data={'query': query}).json()
        return response['results']['bindings']