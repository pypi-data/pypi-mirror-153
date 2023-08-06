# Supplychain Python Library


![Linter](https://github.com/Cosmo-Tech/supplychain-python-library/actions/workflows/linter.yml/badge.svg)
![Tests](https://github.com/Cosmo-Tech/supplychain-python-library/actions/workflows/tests.yml/badge.svg)

This library was made to have an accessible way to use the supplychain python code


# Getting Started

```bash
git clone https://github.com/Cosmo-Tech/supplychain-python-library
pip install -e supplychain-python-library
```


## Code structure

```bash
.	
├── LICENSE	
├── README.md	
├── setup.py                                         # Python library setup file
├── Supplychain	
│   ├── Generic	                                     # Generic components and helpers
│   │   ├── adt_writer.py 
│   │   ├── adx_and_file_writer.py
│   │   ├── ...

│   ├── Protocol	                                 # Optimization protocol and CMAES implementation
│   │   ├── cmaes_optimization_algorithm.py	
│   │   ├── ...
│   │   ├── README.md	
│   ├── Run	                                         # Callable entry points for handlers
│   │   ├── cmaes_optimization.py                    # CMAES optimization run entry point
│   │   ├── simulation.py                            # single simulation entry point
│   │   └── uncertainty_analysis.py                  # uncertainty analysis entry point
│   ├── Schema                                       # describes the domain model
│   │   ├── adt_column_description.py                # defines the domain schema
│   │   ├── default_values.py                        # domain model default values definition
│   │   ├── simulator_files_description.py           # simulator files definition
│   │   └── validation_schemas.py                    # defines the domain model (json definition) : schema and graph relationships
│   ├── Transform	
│   │   ├── complete_dict.py                         # apply default values to the domain model 
│   │   ├── from_dict_to_simulator.py                # transforms domain model data to simulator model 
│   │   ├── from_dict_to_table.py                    # transforms domain model to tabular data to be stored in database ( and transfoms time step based values stored as map to tabular values)
│   │   ├── from_table_to_dict_old.py                # obsolete
│   │   ├── from_table_to_dict.py                    # obsolete
│   │   ├── patch_dict_with_parameters.py            # apply parameters to domain model
│   │   ├── production_route.py                      # compute the production routes based on the graph for the differents products (to be sent to adx by the prerun step)
│   │   └── requirements.txt	
│   ├── Validate                                     # domain model validator definition
│   │   └── validate_dict.py                         # validates the data against the domain schema and graph
│   └── Wrappers	
│       ├── environment_variables.py                 # wrapper for platform environment variables
│       └── simulator.py                             # cosml model wrapper
└── Tests	
└── test.py	
```

## Detailed Documentation

- [Protocol](Supplychain/Protocol/README.md)

