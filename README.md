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
        ├── Instances               # Instanced triplets 
        │   ├── *.ttl               # Instances from museum data
        │   ├── InstancesCombined   
        │   │   ├── *_combined      # Instances + ontology + periods
        │   │   ├── *_infer         # Instances + ontology + periods + inferred
        │   └── ...
        ├── Scripts                 # Application 'n Data processing layers scripts (under development)
        │   ├── curiocity_gui.py    # admin app interface
        │   ├── data_process.py     # script data processing (CSV->CURIOCITY)
        │   ├── query_process.py    # script data processing (Sparql)
        │   ├── period_process.py   # script data processing (CSV periods data->CURIOCITY)
        │   ├── poblar_onto.py      # instantiation utilities
        │   └── ...
        ├── data                    # museum datasets (D-RUTAS) Arequipa, Peru
        │   ├── catalina.csv        # "Santa Catalina" museum dataset
        │   ├── municipal.csv       # Municipal museum dataset
        │   ├── recoleta.csv        # "La Recoleta" museum dataset
        │   └── ...
        ├── Manuals                 # Documentation files
        ├── docs                    # front-end web service files
        └── ...

## References

More info about OQuaRE ontology evaluation framework [here](http://miuras.inf.um.es/oquarewiki/index.php5/Quality_metrics), and [here](https://github.com/atibaut/ontology-evaluation).

