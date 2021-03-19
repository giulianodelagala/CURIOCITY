# CURIOCITY
Repository of CURIOCITY Ontology

## INTRODUCTION

CURIOCITY (Cultural Heritage for Urban Tourism in Indoor/Outdoor environments of the CITY) is an ontology for cultural heritage in Urban Tourism based on several ontologies, mainly on [CIDOC CRM](http://www.cidoc-crm.org/) - [ERLANGEN CRM](http://erlangen-crm.org/).

## Folder Structure


    ├── ...
        ├── Curiocity_Time.*        # CURIOCITY base ontology
        ├── Evaluation              # Scripts to evaluate ontologies
        │   ├── OquaRE              # OQuaRE metrics
        │   ├── Lexical             # Lexical 
        │   └── ...
        ├── Scripts                 # Data processing layer scripts
        ├── data                    # museum datasets (D-RUTAS) Arequipa, Peru
        │   ├── catalina.csv        # "Santa Catalina" museum dataset
        │   ├── municipal.csv       # Municipal museum dataset
        │   ├── recoleta.csv        # "La Recoleta" museum dataset
        │   └── ...
        ├── Manuals                 # Documentation files   
        └── ...

More info about OQuaRE ontology evaluation framework [here](http://miuras.inf.um.es/oquarewiki/index.php5/Quality_metrics), and [here](https://github.com/atibaut/ontology-evaluation).

Oquare Evaluation Python Script
