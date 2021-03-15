# How to set Pellet Reasoner in Docker Jena Fuseki to use with CURIOCITY

This is a little instructive to set Pellet Reasoner in Jena Fuseki using docker image. If you have any suggestion, feel free to contact me.

## Steps

### Get Docker image

Get a Jena Fuseki docker image (*stain/jena-fuseki*) trying: 

>docker run -d --name fuseki -p 3030:3030 -v /host/data/fuseki:/fuseki stain/jena-fuseki

* ` -d ` : detached mode 
* ` --name ` : assign a name to the container (*fuseki*)
* ` -p ` : local/container ports
* ` -v ` : mounts a specify directory on the host (*/host/data/fuseki*) inside the container at the specified path (*/fuseki*)

More info about this image can be found [here](https://hub.docker.com/r/stain/jena-fuseki).

### Change Jena Fuseki config.ttl

Go to the *host/data/fuseki* directory and change the *config.ttl* configuration file to look like this:

```
## Fuseki Server configuration file.

@prefix :        <#> .
@prefix fuseki:  <http://jena.apache.org/fuseki#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ja:      <http://jena.hpl.hp.com/2005/11/Assembler#> .
@prefix tdb:     <http://jena.hpl.hp.com/2008/tdb#> .

[] rdf:type fuseki:Server ;
   fuseki:services (
     :service
   ) .

:service rdf:type fuseki:Service ;
   fuseki:name "dataset" ;
   fuseki:endpoint [ 
       fuseki:operation fuseki:query ;
       fuseki:name "sparql" 
   ];
   fuseki:endpoint [
       fuseki:operation fuseki:query ;
       fuseki:name "query" 
   ] ;
   fuseki:endpoint [
       fuseki:operation fuseki:update ;
       fuseki:name "update"
   ] ;
   fuseki:endpoint [
       fuseki:operation fuseki:gsp-r ;
       fuseki:name "get"
   ] ;
   fuseki:endpoint [ 
       fuseki:operation fuseki:gsp-rw ; 
       fuseki:name "data"
   ] ; 
   fuseki:endpoint [ 
       fuseki:operation fuseki:upload ;
       fuseki:name "upload"
   ] ; 
   fuseki:dataset :dataset ;
   .

# Transactional in-memory dataset.
# :dataset rdf:type ja:MemoryDataset ;
#     ## Optional load with data on start-up
#     ja:data "/fuseki/museo_municipal.ttl";
#     ja:data "/fuseki/museo_recoleta.ttl";
#     ja:data "/fuseki/museo_santa_catalina.ttl";
#     ja:data "/fuseki/periodos.ttl";
#     ja:data "/fuseki/Curiocity_Time.ttl";
#     ja:data "/fuseki/digital.ttl";
#     .

#---- RDFS Inference models
# These must be incorporate in a dataset in order to use them.
# All in one file.
:dataset a ja:RDFDataset ;
    ja:defaultGraph       :inf_model ;
   .

:inf_model a ja:InfModel ;
   rdfs:label "RDFS Inference Model" ;
   ja:baseModel :tdb_graph ;
   ja:reasoner
        [ ja:reasonerClass "openllet.jena.PelletReasonerFactory" ]
   .

:tdb_graph a tdb:GraphTDB ;
   tdb:dataset :tdb_dataset_readwrite .

# A TDB datset used for RDF storage
:tdb_dataset_readwrite a tdb:DatasetTDB;
   tdb:location "/fuseki/databases";
   .
```
