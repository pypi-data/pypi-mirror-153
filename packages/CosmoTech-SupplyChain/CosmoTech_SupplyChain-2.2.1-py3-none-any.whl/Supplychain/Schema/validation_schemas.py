class ValidationSchemas:
    schemas = {
        "Configuration": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "StartingDate": {
                    "type": "string",
                    "format": "date"
                },
                "SimulatedCycles": {
                    "type": "integer",
                    "minimum": 1
                },
                "StepsPerCycle": {
                    "type": "integer",
                    "minimum": 1
                },
                "TimeStepDuration": {
                    "type": "integer",
                    "minimum": 1
                },
                "ManageBacklogQuantities": {
                    "type": "boolean"
                },
                "OptimizationObjective": {
                    "type": "string",
                    "enum": ["ServiceLevelMaximization",
                             "ProfitMaximization"]
                },
                "ActivateUncertainties": {
                    "type": "boolean"
                },
                "UncertaintiesProbabilityDistribution": {
                    "type": "string",
                    "enum": ["Uniform",
                             "Gaussian"]
                },
                "FinancialCostOfStock": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "BatchSize": {
                    "type": "integer",
                    "minimum": 0
                },
                "EmptyObsoleteStocks": {
                    "type": "boolean"
                },
                "ActivateVariableMachineOpeningRate": {
                    "type": "boolean"
                },
                "EnforceProductionPlan": {
                    "type": "boolean"
                },
                "IntermediaryStockDispatchPolicy": {
                    "type": "string",
                    "enum": ["DispatchAll",
                             "AllowRetention"]
                },
            }
        },
        "input": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "InputQuantity": {
                    "type": "number",
                    "exclusiveMinimum": 0
                }
            }
        },
        "ProductionOperation": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "QuantitiesToProduce": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "OperatingPerformances": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}

                },
                "CycleTimes": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "RejectRates": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "OperatingPerformanceUncertainties": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "ProductionUnitCosts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "CO2UnitEmissions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "IsContractor": {
                    "type": "boolean"
                },
                "InvestmentCost": {
                    "type": "number",
                    "minimum": 0,
                },
                "Priority": {
                    "type": "integer",
                    "minimum": 0
                },
                "Duration": {
                    "type": "integer",
                    "minimum": 0
                },
            },
            "required": ["CycleTimes"],
            "dependencies": {
                "OperatingPerformanceUncertainties": ["OperatingPerformances"]
            }
        },
        "ProductionResource": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "ProductionPolicy": {
                    "type": "string",
                    "enum": ["None",
                             "Equidistribution",
                             "GreatestWorkload",
                             "SmallestWorkload",
                             "HighestPriority"]
                },
                "OpeningTimes": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "FixedProductionCosts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                }
            },
            "required": ["OpeningTimes"]
        },
        "Stock": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "StorageCosts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "IsInfinite": {
                    "type": "boolean"
                },
                "MinimalStock": {
                    "type": "number",
                    "if": {"maximum": -1},
                    "then": {"minimum": -1},
                    "else": {"minimum": 0}
                },
                "MaximalStock": {
                    "type": "number",
                    "if": {"maximum": -1},
                    "then": {"minimum": -1},
                    "else": {"minimum": 0}
                },
                "InitialStock": {
                    "type": "number",
                    "minimum": 0
                },
                "InitialValue": {
                    "type": "number",
                    "minimum": 0
                },
                "PurchasingUnitCost": {
                    "type": "number",
                    "minimum": 0
                },
                "CO2UnitEmissions": {
                    "type": "number",
                    "minimum": 0
                },
                "UnitIncome": {
                    "type": "number",
                    "minimum": 0
                },
                "Demands": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    }
                },
                "DemandUncertainties": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        }
                    }
                },
                "DemandWeights": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    }
                },
                "BacklogWeight": {
                    "type": "number",
                    "minimum": 0
                },
                "MaximizationWeight": {
                    "type": "number",
                    "minimum": 0
                },
                "StockPolicy": {
                    "type": "string",
                    "enum": ["None",
                             "OrderPointFixedQuantity",
                             "OrderPointVariableQuantity",
                             "MakeToForecast"]
                },
                "SourcingPolicy": {
                    "type": "string",
                    "enum": ["Equidistribution",
                             "HighestStock",
                             "HighestPriority"]
                },
                "DispatchPolicy": {
                    "type": "string",
                    "enum": ["None",
                             "Equidistribution",
                             "GreatestQuantity",
                             "SmallestQuantity",
                             "HighestPriority"]
                },
                "ReviewPeriod": {
                    "type": "integer",
                    "minimum": 1
                },
                "NextReview": {
                    "type": "integer",
                    "minimum": 0
                },
                "OrderPoints": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "OrderQuantities": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "OrderUpToLevels": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "Advance": {
                    "type": "integer",
                    "minimum": 0
                },
                "SafetyQuantities": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "SalesForecasts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    }
                },
            },
            "dependencies": {
                "InitialValue": ["InitialStock"]
            }
        },
        "Transport": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "Duration": {
                    "type": "integer",
                    "minimum": 0
                },
                "Priority": {
                    "type": "integer",
                    "minimum": 0
                },
                "InitialTransportedQuantities": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    }
                },
                "InitialTransportedValues": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    }
                },
                "CustomFees": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "TransportUnitCosts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                },
                "CO2UnitEmissions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]}
                }
            },
            "required": ["Duration"],
            "dependencies": {
                "InitialTransportedValues": ["InitialTransportedQuantities"]
            }
        }
    }
    graph = {
        "contains": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["ProductionResource", "id"],
                "target": ["ProductionOperation", "id"]
            },
            "cardinalities": "1:N",
            "all_target_present": True,
            "all_source_present": True
        },
        "input": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["Stock", "id"],
                "target": ["ProductionOperation", "id"]
            },
            "cardinalities": "N:N",
            "all_target_present": True,
            "all_source_present": False
        },
        "output": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["ProductionOperation", "id"],
                "target": ["Stock", "id"]
            },
            "cardinalities": "N:1",
            "all_target_present": False,
            "all_source_present": True
        },
        "Transport": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["Stock", "id"],
                "target": ["Stock", "id"]
            },
            "cardinalities": "N:N",
            "all_target_present": False,
            "all_source_present": False
        }
    }
