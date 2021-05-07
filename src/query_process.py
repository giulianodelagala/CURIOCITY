from typing import List
#from owlready2 import *
from urllib import parse as url

#from rdflib.plugins.sparql import prepareQuery
import requests
from requests.api import request
from requests.models import Response
from requests.auth import HTTPBasicAuth


class QueryProcess():
    def __init__(self):
        self.connection_path = 'http://localhost:3030/dataset/query'
        self.update_path = 'http://localhost:3030/dataset/update'

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
            'Author'    : "?author_lab",
            'Material'  : "?material_l",
            'Location'  : "?location_l",
            'Period'    : "?period_l"
        }
        
        FILTERS = ""
        #Get list of querys and create appropiate Filter
        for i in range(0, len(data)):
            FILTERS += "FILTER (regex(" + dic_query[data[i][1]] + ", \"" + data[i][0] + "\", \"i\"))\n"
        #q_ready = q_comb_base.replace("FILTERS", q_filter)

        query_comb = f"""
            #Combination Query
            PREFIX : <http://curiocity.org/>
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX cit: <http://curiocity.org/>
            SELECT DISTINCT ?id_l ?artifact_l 
            (COALESCE (?author_lab, "UNKNOWN") AS ?author_l)
            ?material_l ?location_l
            (COALESCE (?donor_lab, "UNKNOWN") AS ?donor_l)
            (COALESCE (?period_lab, "UNKNOWN") AS ?period_l)
            (COALESCE (?begin_date, "UNKNOWN") AS ?begin_d)
            (COALESCE (?end_date, "UNKNOWN") AS ?end_d)
            ?note 
            (COALESCE (?note_donor_, "UNKNOWN") AS ?note_donor)
            (BOUND (?tag) AS ?verified)
            WHERE {{
            #VALUES ?type {{ time:in_XSD_date time:in_XSD_g-Year }}
            ?artifact a ecrm:E22_Man-Made_Object ;
                rdfs:label ?artifact_l ; #Title
                ecrm:P48_has_preferred_identifier ?id ;
                ecrm:P55_has_current_location ?location ;
                ecrm:P3_has_note ?note ;
                ecrm:P45_consists_of ?material .
            ?material rdfs:label ?material_l .
            ?id rdfs:label ?id_l .
            ?location rdfs:label ?location_l .
            ?prod ecrm:P108_has_produced ?artifact .
            OPTIONAL {{ ?prod ecrm:P14_carried_out_by ?author .
                        ?author rdfs:label ?author_lab . }}
            OPTIONAL {{ ?prod ecrm:P4_has_time-span/(^ecrm:P4_has_time-span) ?period .
                        ?period ecrm:P4_has_time-span/(^cit:Q14_defines_time) ?interval.

                        ?period a ecrm:E4_Period ;
                            rdfs:label ?period_lab .

                        ?interval  time:hasBeginning/(time:in_XSD_date|time:in_XSD_g-Year) ?begin_date .
                        ?interval  time:hasEnd/(time:in_XSD_date|time:in_XSD_g-Year) ?end_date .				
                }}
            OPTIONAL {{ ?artifact ecrm:P2_has_type ?tag . FILTER (?tag = :Verified)}}
            {FILTERS}
            }}"""
       
        response = requests.post(self.connection_path,
            data={'query': query_comb}).json()
        # print (response)
        return response['results']['bindings']

    def instanceQuery(self, types, filtro):
        
        FILTRO = filtro
        if (types == 'author'):
            TYPES = 'ecrm:E21_Person ecrm:E74_Group'
        elif (types == 'material'):
            TYPES = 'ecrm:E57_Material'
        elif (types == 'location'): #TODO Place according museum
            TYPES = 'ecrm:E53_Place'

        ins_query = f'''PREFIX : <http://curiocity.org/>
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX cit: <http://curiocity.org/>

            SELECT ?subject ?subject_l
            WHERE {{
            VALUES ?type {{ {TYPES} }}
            ?subject  a ?type ;
                    rdfs:label ?subject_l .
            FILTER (regex(str(?subject_l) , "{FILTRO}" , "i") ) 
            }}'''

        response = requests.post(self.connection_path,
            data={'query': ins_query}).json()
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

    def updateQuery(self, field:str, ID:str, BEFORE:str, AFTER:str):      
        auth = HTTPBasicAuth('admin', 'pw123') #TODO

        if (field == 'title'):
            PROPERTY = '?artifact rdfs:label'
        elif (field == 'author'):
            PROPERTY = '?prod ecrm:P14_carried_out_by'
        elif (field == 'material'):
            PROPERTY = '?artifact ecrm:P45_consists_of'
        elif (field == 'location'):
            PROPERTY = '?artifact  ecrm:P55_has_current_location'
        elif (field == 'description'):
            PROPERTY = '?artifact  ecrm:P3_has_note'
        elif (field == 'validated'):
            PROPERTY = '?artifact ecrm:P2_has_type'

        upd_query = f'''PREFIX : <http://curiocity.org/>
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX cit: <http://curiocity.org/>
            DELETE {{{PROPERTY} {BEFORE}}}
            INSERT {{{PROPERTY} {AFTER}}}
            WHERE  {{ 
                ?artifact ecrm:P48_has_preferred_identifier/rdfs:label "{ID}" .
                ?artifact a ecrm:E22_Man-Made_Object ;
                            rdfs:label ?artifact_l ;                            
                            ecrm:P55_has_current_location ?location ;
                            ecrm:P3_has_note ?note ;
                            ecrm:P45_consists_of ?material .                        
                ?prod ecrm:P108_has_produced ?artifact .
                OPTIONAL {{
                ?prod ecrm:P14_carried_out_by ?author .
                ?author rdfs:label ?author_l . }}
            }}'''     
        print(upd_query)
        response = requests.post(self.update_path,
            data={'update': upd_query}, auth=auth)
        print (response)

    def checkID(self, id:str):
        id = url.quote(id)
        query_id = f'''PREFIX : <http://curiocity.org/>
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            ASK {{ :{id} a ecrm:E42_Identifier .}}'''
        # print (query_id)
        response = requests.post(self.connection_path, data={'query': query_id })
        # print(response)
        try:
            if ( response.json()['boolean']):
                return True
            else:
                return False
        except:
            return False
            
    def insertQuery(self, id:str, title:str, author:str,
        material:str, location:str, description:str):
        id_url = url.quote(id)
        auth = HTTPBasicAuth('admin', 'pw123') #TODO
      
        query_insert = f'''PREFIX : <http://curiocity.org/>
            PREFIX ecrm: <http://erlangen-crm.org/170309/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX cit: <http://curiocity.org/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            INSERT DATA {{
                :{id_url} a ecrm:E42_Identifier ,
                            owl:NamedIndividual ;
                            rdfs:label "{id}"^^xsd:string ;
                            :P190_has_symbolic_content "{id}"^^xsd:string ;
                            ecrm:P2_has_type :ID-RUTAS .
                <http://curiocity.org/{id_url}/Object> a ecrm:E22_Man-Made_Object,
                            owl:NamedIndividual ;
                            rdfs:label "{title}"^^xsd:string ;
                            ecrm:P3_has_note """{description}"""^^xsd:string ;
                            ecrm:P45_consists_of {material} ;
                            ecrm:P48_has_preferred_identifier :{id} ;
                            ecrm:P55_has_current_location {location} .
                <http://curiocity.org/{id_url}/Production> a ecrm:E12_Production;
                            ecrm:P108_has_produced <http://curiocity.org/{id_url}/Object> ;
                            ecrm:P14_carried_out_by {author} .
            }}
            '''
        # print (query_insert)
        response = requests.post(self.update_path,
            data={'update': query_insert}, auth=auth)
        if (response.ok):
            return True
        else:
            return False

    def deleteQuery(self, id:str):
        auth = HTTPBasicAuth('admin', 'pw123') #TODO      
        delete_query = f'''###### Delete artifact triples
        PREFIX : <http://curiocity.org/>
        PREFIX ecrm: <http://erlangen-crm.org/170309/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX time: <http://www.w3.org/2006/time#>
        PREFIX cit: <http://curiocity.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        DELETE {{
        ?artifact ?p ?o .
        ?s_art ?p_art ?artifact .
        ?production ?p2 ?o2 .
        ?s_pro ?p_pro ?production .
        ?acquisition ?p1 ?o1 .
        ?s_acq ?p_acq ?acquisition .
        ?id ?p6 ?o6 .
        ?s_id ?p_id ?id .
        ?dimension ?p3 ?o3 .
        ?s_dim ?p_dim ?dimension .
        ?utility ?p4 ?o4 . 
        ?s_util ?p_util ?utility .
        ?condition ?p5 ?o5 .
        ?s_con ?p_con ?condition .
        ?process ?p7 ?o7 .
        ?s_proc ?p_proc ?process .
        }}
        WHERE  {{
            BIND ( :{id} AS ?id)
            BIND ( <http://curiocity.org/{id}/Production> AS ?production)
            BIND ( <http://curiocity.org/{id}/Object> AS ?artifact)
            BIND ( <http://curiocity.org/{id}/Measurements> AS ?dimension)
            BIND ( <http://curiocity.org/{id}/Adquisition> AS ?acquisition)
            BIND ( <http://curiocity.org/{id}/Utility> AS ?utility)
            BIND ( <http://curiocity.org/{id}/Current_Condition> AS ?condition)
            {{
                ?artifact	ecrm:P48_has_preferred_identifier ?id ;
                            ?p ?o .
                ?s_art ?p_art ?artifact .}}
            UNION
            {{  ?production ecrm:P108_has_produced? ?artifact ;
                            ?p2 ?o2 .
                ?s_pro ?p_pro ?production .  }}
            UNION
            {{  ?acquisition ecrm:P30_transferred_custody_of ?artifact ;
                            ?p1 ?o1 .
                ?s_acq ?p_acq ?acquisition .  }}
            UNION
            {{  ?id a ecrm:E42_Identifier ;
                        ?p6 ?o6 .
                ?s_id ?p_id ?id .  }}
            UNION
            {{  ?artifact ecrm:P43_has_dimension ?dimension .
                        ?dimension ?p3 ?o3 .
                ?s_dim ?p_dim ?dimension .    }}
            UNION
            {{  ?artifact ecrm:P44_has_condition ?condition .
                    ?condition ?p5 ?o5 . 
                ?s_con ?p_con ?condition .     }}
            UNION
            {{  ?process :L1_digitized ?artifact ;
                            ?p7 ?o7 .
                ?s_proc ?p_proc ?process .     }}
            UNION
            {{  ?artifact	ecrm:P2_has_type ?utility . 
                ?utility ?p4 ?o4 .	
                ?s_util ?p_util ?utility .     }}
        }}''' 
        
        response = requests.post(self.update_path,
            data={'update': delete_query}, auth=auth)
        if (response.ok):
            return True
        else:
            return False

# upd_query = f'''PREFIX : <http://curiocity.org/>
#             PREFIX ecrm: <http://erlangen-crm.org/170309/>
#             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#             PREFIX time: <http://www.w3.org/2006/time#>
#             PREFIX cit: <http://curiocity.org/>
#             DELETE {{{PROPERTY} {BEFORE}}}
#             INSERT {{{PROPERTY} {AFTER}}}
#             WHERE  {{ ?artifact a ecrm:E22_Man-Made_Object ;
#                             rdfs:label ?artifact_l ;
#                             ecrm:P48_has_preferred_identifier ?id ;
#                             ecrm:P55_has_current_location ?location ;
#                             ecrm:P3_has_note ?note ;
#                             ecrm:P45_consists_of ?material .
#                         ?id  rdfs:label "{id}"^^xsd:string ;
#                 ?prod ecrm:P108_has_produced ?artifact .
#                 OPTIONAL {{
#                 ?prod ecrm:P14_carried_out_by ?author .
#                 ?author rdfs:label ?author_l . }}
#             FILTER (regex(str(?id) , "{ID}" , "i") ) }}'''  
