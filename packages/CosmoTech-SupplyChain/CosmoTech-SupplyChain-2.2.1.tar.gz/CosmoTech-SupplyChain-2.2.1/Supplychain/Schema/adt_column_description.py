class ADTColumnDescription:
    """
    This class contains a descriptor of the format of a dataset in ADT
    It allows the description of each column and how it should be considered during a transformation
    - fixed : means that the data is a non changing value that stay constant through time,
      or can be used as an initialization
    - change : represent a change over time which means it needs a timestep for when it takes effect,
      and the new value for the subsequent time steps
    - event : represent a ponctual event over time, the change is not permanent and on subsequent timestep
      without other values nothing happens
    """
    format = {
        "Stock": {
            "fixed": [
                "id",
                "Label",
                "PlantName",
                "Step",
                "PartId",
                "MinimalStock",
                "MaximalStock",
                "InitialStock",
                "InitialValue",
                "IsInfinite",
                "PurchasingUnitCost",
                "CO2UnitEmissions",
                "UnitIncome",
                "BacklogWeight",
                "MaximizationWeight",
                "StockPolicy",
                "SourcingPolicy",
                "DispatchPolicy",
                "ReviewPeriod",
                "NextReview",
                "Advance",
            ],
            "change": [
                "StorageUnitCosts",
                "OrderPoints",
                "OrderQuantities",
                "OrderUpToLevels",
                "SafetyQuantities",
            ],
            "event": {
                "Demands": [
                    "Demands",
                    "DemandUncertainties",
                    "DemandWeights",
                ],
                "SalesForecasts": [
                    "SalesForecasts",
                ],
            }
        },
        "Transport": {
            "fixed": [
                "Label",  # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                "source",
                "target",
                "Duration",
                "Priority",
            ],
            "change": [
                "CustomFees",
                "TransportUnitCosts",
                "CO2UnitEmissions",
            ],
            "event": {
                "InitialTransports": [
                    "InitialTransportedQuantities",
                    "InitialTransportedValues",
                ]
            },
        },
        "Configuration": {
            "fixed": [
                "ActivateUncertainties",
                "ActivateVariableMachineOpeningRate",
                "BatchSize",
                "EmptyObsoleteStocks",
                "EnforceProductionPlan",
                "FinancialCostOfStock",
                "ManageBacklogQuantities",
                "OptimizationObjective",
                "SimulatedCycles",
                "StartingDate",
                "StepsPerCycle",
                "TimeStepDuration",
                "UncertaintiesProbabilityDistribution",
                "IntermediaryStockDispatchPolicy",
            ],
            "change": [],
            "event": {}
        },
        "contains": {
            "fixed": [
                "source",
                "target",
            ],
            "change": [],
            "event": {}
        },
        "output": {
            "fixed": [
                "source",
                "target",
            ],
            "change": [],
            "event": {}
        },
        "input": {
            "fixed": [
                "source",
                "target",
                "InputQuantity",
            ],
            "change": [],
            "event": {}
        },
        "ProductionResource": {
            "fixed": [
                "id",
                "Label",
                "PlantName",
                "ProductionStep",
                "ProductionPolicy",
            ],
            "change": [
                "FixedProductionCosts",
                "OpeningTimes",
            ],
            "event": {}
        },
        "ProductionOperation": {
            "fixed": [
                "id",
                "Label",
                "PlantName",
                "IsContractor",
                "InvestmentCost",
                "Priority",
                "Duration",
            ],
            "change": [
                "QuantitiesToProduce",
                "OperatingPerformances",
                "CycleTimes",
                "RejectRates",
                "OperatingPerformanceUncertainties",
                "ProductionUnitCosts",
                "CO2UnitEmissions",
            ],
            "event": {}
        }
    }
