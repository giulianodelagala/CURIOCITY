# How to set Pellet Reasoner in Docker Jena Fuseki to use with CURIOCITY

This is a little instructive to set Pellet Reasoner in Jena Fuseki using docker image. If you have any suggestion, feel free to contact me.

## Configure Openllet with Jena Fuseki image Docker

### Get Docker image

Get a Jena Fuseki docker image (*stain/jena-fuseki*) trying: 

>docker run -d --name fuseki -p 3030:3030 -v /host/data/fuseki:/fuseki stain/jena-fuseki

* ` -d ` : detached mode 
* ` --name ` : assign a name to the container (*fuseki*)
* ` -p ` : local/container ports
* ` -v ` : mounts a specify directory on the host (*/host/data/fuseki*) inside the container at the specified path (*/fuseki*)

More info about this docker image can be found <a href="https://hub.docker.com/r/stain/jena-fuseki" target="_blank">here</a>.

### Get Openllet JAR files

Download and extract Openllet Jena JAR files with all dependencies from [here](https://jar-download.com/artifacts/com.github.galigator.openllet/openllet-jena/2.6.5).

More info about Openllet Reasoner can be found <a href="https://github.com/Galigator/openllet" target="_blank">here</a>.

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

### Copy Openllet JAR files to container

The docker image has a convenient script to facilitate adding custom code to Fuseki Server. The script can be found in */jena-fuseki* directory on the container under the name *fuseki-server*. The script recognizess if exists a *../extra/* directory in *FUSEKI-BASE* path, and configure Jena Fuseki execution (classpath). For our case *FUSEKI_BASE=host/data/fuseki*, so we have to create a *extra* directory, and copy all the extracted Openllet JAR files into it.

>cp /openllet_extracted_dir/*.jar /host/data/fuseki/extra/

Up to this point, we have configured Jena Fuseki to use Openllet as a reasoner, so we can restart the container:

>docker restart fuseki

## Get CURIOCITY in Docker container

Docker image stain/jena-fuseki includes script to load data to TDB, but we use *tdbloader* command from inside the container instead.

### Copying ontology and instantiation files

Copy to *host/data/fuseki* directory all needed CURIOCITY files, for example:
* CURIOCITY_base.ttl
* Period.ttl
* Instantiation_files.ttl
* Digitizing_files.ttl

### Get ontology data in TDB

First we get a bash shell inside the container.

> docker exec -it fuseki /bin/bash

We can see our prompt has changed, showing we are inside the container. Find tdbloader command, for our case is located in */jena-fuseki/*. Also we can find that previous CURIOCITY files are in */fuseki/* container directory indeed. Now we can load the data to TDB database to the */fuseki/databases/* directory specified in *config.ttl*. Supposing we are in */fuseki/* directory:

> ../jena-fuseki/./tdbloader All_CURIOCITY_files.ttl databases/

When the loading finishes we can restart the container.

> exit </br>
> docker restart fuseki

Go the Jena Fuseki web service, and check everything works fine.





