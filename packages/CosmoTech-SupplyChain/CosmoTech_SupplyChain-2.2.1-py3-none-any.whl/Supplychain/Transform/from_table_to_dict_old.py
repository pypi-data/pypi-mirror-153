import argparse
from collections import defaultdict
import io
import json
import os
import pandas as pd
import re

from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient, TextBase64EncodePolicy

from Supplychain.Generic.adt_writer import ADTWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Generic.csv_folder_writer import CSVWriter


def df_add_composite_id(df, id_name, columns):
    if len(df):
        df[id_name] = df.apply(lambda r: "_".join([r[column] for column in columns]), axis=1)
    else:
        df[id_name] = pd.Series(dtype=str)


class FromTableToDictConverter(Timer):

    def __init__(self,
                 input_path: str = '',
                 output_path: str = '',
                 queue_name: str = '',
                 blob_name: str = '',
                 origin: str = '',
                 target: str = '',
                 connect_str: str = ''):

        Timer.__init__(self, "[ADT Connection]")

        self.last_time = self.start_time

        self.input_path = input_path
        self.output_path = output_path
        self.queue_name = queue_name
        self.blob_name = blob_name
        self.origin = origin
        self.target = target
        self.connect_str = connect_str

        self.adt_writer = None

        self.optional_sheet_names = ['Transports',
                                     'InitialTransports',
                                     'DataTransport',
                                     'CustomsCosts',
                                     'InitialStocks',
                                     'StorageCosts',
                                     'Incomes',
                                     'DataPurchasedParts',
                                     'DemandWeights',
                                     'Maximization',
                                     'StockMaxima',
                                     'StockMinima',
                                     'FixedProductionCosts',
                                     'VariableProductionCosts',
                                     'DataContractor',
                                     'InvestmentCosts']

        self.required_sheet_names = ['Inputs',
                                     'DataMachine',
                                     'DataOperation',
                                     'Demands',
                                     'Configuration']

        self.sheet_names = self.required_sheet_names + self.optional_sheet_names

        self.sheets = None
        if self.origin == 'local_files':
            excel_path = os.path.join(self.input_path, 'Dataset.xlsx')
            if os.path.exists(excel_path):
                excel_file = pd.ExcelFile(excel_path)
                self.sheets = dict()
                for sheet_name in self.sheet_names:
                    try:
                        self.sheets[sheet_name] = pd.read_excel(excel_file, sheet_name)
                    except ValueError:
                        pass
            else:
                self.sheets = {sheet_name: pd.read_csv(os.path.join(self.input_path,
                                                                    sheet_name + ".csv"))
                               for sheet_name in self.sheet_names if os.path.exists(os.path.join(self.input_path,
                                                                                                 sheet_name + ".csv"))}
        elif self.origin == 'blob':
            blob_service_client = BlobServiceClient.from_connection_string(self.connect_str)
            container_client = blob_service_client.get_container_client(container=self.blob_name)

            self.sheets = dict()
            for blob in container_client.list_blobs():
                if ".xlsx" in blob.name:
                    blob_client = blob_service_client.get_blob_client(container=self.blob_name, blob=blob.name)
                    blob_data = blob_client.download_blob().readall()
                    file_io = io.BytesIO(blob_data)
                    excel_file = pd.ExcelFile(file_io)
                    for sheet_name in self.sheet_names:
                        try:
                            self.sheets[sheet_name] = pd.read_excel(excel_file, sheet_name)
                        except ValueError:
                            self.sheets[sheet_name] = None
                elif ".csv" in blob.name:
                    sheet_name = blob.name[:-4]
                    if sheet_name in self.sheet_names:
                        blob_client = blob_service_client.get_blob_client(container=self.blob_name, blob=blob.name)
                        blob_data = blob_client.download_blob().readall()
                        file_io = io.BytesIO(blob_data)
                        sheet_content = pd.read_csv(file_io)
                        self.sheets[sheet_name] = sheet_content
        else:
            exit(1)

        self.machines = list()
        self.operations = list()
        self.stocks = list()
        self.relations = list()
        self.configuration = dict()

    def __select_sheet(self,
                       sheet_name,
                       columns,
                       validation,
                       optionals=tuple(),
                       str_columns=tuple()):
        """
        Select a sheet in an excel file and returns a pandas dataframe
        :param sheet_name: the name of the selected sheet
        :param columns: a list of columns to be used in the dataframe
        :param validation: a column name where Null values implies the line is not needed
        :param optionals: a list of optionals columns
        :return: a pandas dataframe with the excel file data
        """

        if sheet_name not in self.sheets:
            return pd.DataFrame(columns=columns)

        frame = self.sheets[sheet_name]
        cols = columns + [col for col, _ in optionals if col in frame]

        for col, default in optionals:
            if col not in cols:
                frame[col] = frame.apply(lambda r: default, axis=1)
                cols.append(col)

        f = frame[columns + [col for col, _ in optionals]]
        df = f[pd.notnull(f[validation])].copy()

        for col in str_columns:
            df[col] = df[col].astype(str)
        return df

    def __set_configuration(self,
                            starting_date: str,
                            simulated_cycles: int,
                            steps_per_cycle: int,
                            time_step_duration: int,
                            manage_backlog_quantities: bool,
                            optimization_objective: str,
                            activate_uncertainties: bool,
                            uncertainties_probability_distribution: str,
                            immobilized_cash_relative_cost: float,
                            batch_size: int,
                            enforce_production_plan: bool,
                            empty_obsolete_stocks: bool,
                            activate_machine_variable_opening_rate: bool):
        self.configuration['$metadata'] = {"$model": 'dtmi:com:cosmotech:supplychain:Configuration;1'}
        self.configuration['$id'] = 'Configuration'
        if type(starting_date) is pd.Timestamp:
            self.configuration['StartingDate'] = pd.Timestamp(starting_date).strftime("%Y-%m-%d")
        else:
            self.configuration['StartingDate'] = starting_date
        self.configuration['SimulatedCycles'] = int(simulated_cycles)
        self.configuration['StepsPerCycle'] = int(steps_per_cycle)
        self.configuration['TimeStepDuration'] = int(time_step_duration)
        self.configuration['ManageBacklogQuantities'] = bool(manage_backlog_quantities)
        self.configuration['OptimizationObjective'] = optimization_objective
        self.configuration['ActivateUncertainties'] = bool(activate_uncertainties)
        self.configuration['UncertaintiesProbabilityDistribution'] = uncertainties_probability_distribution
        self.configuration['FinancialCostOfStock'] = float(immobilized_cash_relative_cost)
        self.configuration['BatchSize'] = int(batch_size)
        self.configuration['EnforceProductionPlan'] = bool(enforce_production_plan)
        self.configuration['EmptyObsoleteStocks'] = bool(empty_obsolete_stocks)
        self.configuration['ActivateVariableMachineOpeningRate'] = bool(activate_machine_variable_opening_rate)

    def read_configuration(self):
        configuration_df = self.sheets['Configuration']

        if 'OptimizationObjective' not in configuration_df.columns:
            configuration_df['OptimizationObjective'] = 'ServiceLevelMaximization'
        if 'Activate Uncertainties' not in configuration_df.columns:
            configuration_df['Activate Uncertainties'] = False
        if 'Empty Obsolete Stocks' not in configuration_df.columns:
            configuration_df['Empty Obsolete Stocks'] = False
        if 'Uncertainties Probability Distribution' not in configuration_df.columns:
            configuration_df['Uncertainties Probability Distribution'] = 'Uniform'
        if 'Activate Variable Machine Opening Rate' not in configuration_df.columns:
            configuration_df['Activate Variable Machine Opening Rate'] = False
        if 'Immobilized Cash Relative Cost' not in configuration_df.columns:
            configuration_df['Immobilized Cash Relative Cost'] = 0.0
        if 'Batch Size' not in configuration_df.columns:
            configuration_df['Batch Size'] = 0
        if 'Enforce Production Plan' not in configuration_df.columns:
            configuration_df['Enforce Production Plan'] = False

        starting_date = configuration_df['Starting Date'][0]
        number_of_cycles = configuration_df['Simulated Cycles'][0]
        time_unit_per_cycle = configuration_df['Steps Per Cycle'][0]
        timestep_duration = configuration_df['TimeStep Duration'][0]
        manage_backlog_quantities = configuration_df['Manage backlog quantities'][0]
        optimization_objective = configuration_df['OptimizationObjective'][0]
        activate_uncertainties = configuration_df['Activate Uncertainties'][0]
        probability_distribution = configuration_df['Uncertainties Probability Distribution'][0]
        immobilized_cash_relative_cost = configuration_df['Immobilized Cash Relative Cost'][0]
        batch_size = configuration_df['Batch Size'][0]
        enforce_production_plan = configuration_df['Enforce Production Plan'][0]
        empty_obsolete_stocks = configuration_df['Empty Obsolete Stocks'][0]
        activate_machine_variable_opening_rate = configuration_df['Activate Variable Machine Opening Rate'][0]

        self.__set_configuration(starting_date,
                                 number_of_cycles,
                                 time_unit_per_cycle,
                                 timestep_duration,
                                 manage_backlog_quantities,
                                 optimization_objective,
                                 activate_uncertainties,
                                 probability_distribution,
                                 immobilized_cash_relative_cost,
                                 batch_size,
                                 enforce_production_plan,
                                 empty_obsolete_stocks,
                                 activate_machine_variable_opening_rate)

    def read_production_resource(self):
        data_machine = self.__select_sheet('DataMachine',
                                           ['Plant',
                                            'ProductionStep',
                                            'Machine',
                                            'TimeStep',
                                            'OpeningTime'],
                                           'Machine',
                                           str_columns=('Plant',
                                                        'ProductionStep',
                                                        'Machine'))
        production_costs = self.__select_sheet('FixedProductionCosts',
                                               ['Plant',
                                                'ProductionStep',
                                                'Machine',
                                                'TimeStep',
                                                'ProductionCost'],
                                               'Machine',
                                               str_columns=('Plant',
                                                            'ProductionStep',
                                                            'Machine'))

        df_add_composite_id(data_machine, 'Machine_ID', ['Plant', 'Machine', 'ProductionStep'])
        df_add_composite_id(production_costs, 'Machine_ID', ['Plant', 'Machine', 'ProductionStep'])

        machine_ids = sorted(set(data_machine['Machine_ID'].values))

        for machine_id in machine_ids:
            data_current_machine = data_machine[data_machine['Machine_ID'] == machine_id]
            prod_current_machine = production_costs[production_costs['Machine_ID'] == machine_id]

            plant, production_step, machine, *_ = data_current_machine.values[0]
            opening_times = dict()
            for _, _, _, timestep, opening_time, _ in data_current_machine.values:
                opening_times[str(timestep)] = opening_time

            fixed_production_costs = dict()
            for _, _, _, timestep, production_cost, _ in prod_current_machine.values:
                fixed_production_costs[str(timestep)] = production_cost

            self.machines.append({"$metadata": {"$model": "dtmi:com:cosmotech:supplychain:ProductionResource;1"},
                                  "$id": self.__sanitize_adt_id(machine_id),
                                  "Label": machine,
                                  "PlantName": plant,
                                  "ProductionStep": production_step,
                                  "OpeningTimes": opening_times,
                                  "FixedProductionCosts": fixed_production_costs})

    def read_production_operations(self):
        data_operations = self.__select_sheet('DataOperation',
                                              ['Plant',
                                               'OutputStep',
                                               'Machine',
                                               'OutputPartType',
                                               'OutputPartName',
                                               'TimeStep',
                                               'OperatingPerformance',
                                               'CycleTime',
                                               'RejectRate'],
                                              'Machine',
                                              optionals=(('OperatingPerformanceUncertainty', 0.0),
                                                         ('ProductionPlanning', 0.0),),
                                              str_columns=('Plant',
                                                           'OutputStep',
                                                           'Machine',
                                                           'OutputPartType',
                                                           'OutputPartName',))
        var_production_costs = self.__select_sheet('VariableProductionCosts',
                                                   ['Plant',
                                                    'OutputStep',
                                                    'Machine',
                                                    'OutputPartType',
                                                    'OutputPartName',
                                                    'TimeStep',
                                                    'ProductionUnitCost'],
                                                   'Machine',
                                                   optionals=(('CO2UnitEmissions', 0.0),),
                                                   str_columns=('Plant',
                                                                'OutputStep',
                                                                'Machine',
                                                                'OutputPartType',
                                                                'OutputPartName',))
        data_contractors = self.__select_sheet('DataContractor',
                                               ['Plant',
                                                'OutputStep',
                                                'Machine',
                                                'OutputPartType',
                                                'OutputPartName',
                                                'TimeStep',
                                                'ProductionPlanning'],
                                               'Machine',
                                               str_columns=('Plant',
                                                            'OutputStep',
                                                            'Machine',
                                                            'OutputPartType',
                                                            'OutputPartName',))
        investment_costs = self.__select_sheet('InvestmentCosts',
                                               ['Plant',
                                                'OutputStep',
                                                'Machine',
                                                'OutputPartType',
                                                'OutputPartName',
                                                'InvestmentCost'],
                                               'Machine',
                                               str_columns=('Plant',
                                                            'OutputStep',
                                                            'Machine',
                                                            'OutputPartType',
                                                            'OutputPartName',))

        df_add_composite_id(data_operations,
                            'Operation_ID',
                            ['Plant',
                             'Machine',
                             'OutputPartType',
                             'OutputPartName',
                             'OutputStep'])
        df_add_composite_id(var_production_costs,
                            'Operation_ID',
                            ['Plant',
                             'Machine',
                             'OutputPartType',
                             'OutputPartName',
                             'OutputStep'])
        df_add_composite_id(data_contractors,
                            'Operation_ID',
                            ['Plant',
                             'Machine',
                             'OutputPartType',
                             'OutputPartName',
                             'OutputStep'])
        df_add_composite_id(investment_costs,
                            'Operation_ID',
                            ['Plant',
                             'Machine',
                             'OutputPartType',
                             'OutputPartName',
                             'OutputStep'])

        investment_costs = investment_costs[['Operation_ID', 'InvestmentCost']]
        investment_costs = investment_costs.set_index('Operation_ID')
        investment_costs = investment_costs['InvestmentCost']
        investment_costs = investment_costs.to_dict()

        operations_ids = sorted(set(data_operations['Operation_ID'].values))
        contractors_ids = sorted(set(data_contractors['Operation_ID'].values))

        for operations in [operations_ids, contractors_ids]:
            for operation_id in operations:
                data_current_operation = data_operations[data_operations['Operation_ID'] == operation_id]
                prod_current_operation = var_production_costs[var_production_costs['Operation_ID'] == operation_id]
                data_current_contractor = data_contractors[data_contractors['Operation_ID'] == operation_id]
                investment_cost = investment_costs.get(operation_id, 0.0)

                try:
                    plant, production_step, machine, part_type, part_name, *_ = data_current_operation.values[0]
                except IndexError:
                    plant, production_step, machine, part_type, part_name, *_ = data_current_contractor.values[0]

                current_pp = dict()
                current_op = dict()
                current_ct = dict()
                current_rr = dict()
                current_op_uncertainty = dict()
                for (_, _, _, _, _,
                     timestep,
                     op, ct, rr, op_uncertainty, prod_planning, _) in data_current_operation.values:
                    current_pp[str(int(timestep))] = prod_planning
                    current_op[str(int(timestep))] = op
                    current_ct[str(int(timestep))] = ct
                    current_rr[str(int(timestep))] = rr
                    current_op_uncertainty[str(int(timestep))] = op_uncertainty

                current_prod_unit_cost = dict()
                current_co2_emissions = dict()
                for _, _, _, _, _, timestep, production_cost, co2_unit_emissions, _ in prod_current_operation.values:
                    current_prod_unit_cost[str(int(timestep))] = production_cost
                    current_co2_emissions[str(int(timestep))] = co2_unit_emissions

                is_contractor = False
                for (_, _, _, _, _, timestep, prod_planning, _) in data_current_contractor.values:
                    current_pp[str(int(timestep))] = prod_planning
                    is_contractor = True

                self.operations.append({"$metadata": {"$model": "dtmi:com:cosmotech:supplychain:ProductionOperation;1"},
                                        "$id": self.__sanitize_adt_id(operation_id),
                                        "Label": operation_id,
                                        "PlantName": plant,
                                        "IsContractor": is_contractor,
                                        "QuantitiesToProduce": current_pp,
                                        "OperatingPerformances": current_op,
                                        "CycleTimes": current_ct,
                                        "RejectRates": current_rr,
                                        "OperatingPerformanceUncertainties": current_op_uncertainty,
                                        "ProductionUnitCosts": current_prod_unit_cost,
                                        "CO2UnitEmissions": current_co2_emissions,
                                        "InvestmentCost": investment_cost})

                machine_id = "_".join([plant, machine, production_step])

                relation = {"$sourceId": self.__sanitize_adt_id(machine_id),
                            "$targetId": self.__sanitize_adt_id(operation_id),
                            "$relationshipId": self.__sanitize_adt_id(operation_id + '_in_' + machine_id),
                            "$relationshipName": "contains"}

                self.relations.append(relation)

    def read_stocks(self):
        inputs = self.__select_sheet('Inputs',
                                     ['Plant',
                                      'OutputStep',
                                      'Machine',
                                      'OutputPartType',
                                      'OutputPartName',
                                      'InputStep',
                                      'InputPartType',
                                      'InputPartName',
                                      'InputQuantity'],
                                     'Plant',
                                     str_columns=('Plant',
                                                  'OutputStep',
                                                  'Machine',
                                                  'OutputPartType',
                                                  'OutputPartName',
                                                  'InputStep',
                                                  'InputPartType',
                                                  'InputPartName'))

        df_add_composite_id(inputs, 'OutputStock_ID', ['Plant', 'OutputPartType', 'OutputPartName', 'OutputStep'])
        df_add_composite_id(inputs, 'InputStock_ID', ['Plant', 'InputPartType', 'InputPartName', 'InputStep'])
        df_add_composite_id(inputs, 'OutputPart_ID', ['OutputPartType', 'OutputPartName'])
        df_add_composite_id(inputs, 'InputPart_ID', ['InputPartType', 'InputPartName'])
        df_add_composite_id(inputs, 'Operation_ID',
                            ['Plant', 'Machine', 'OutputPartType', 'OutputPartName', 'OutputStep'])

        transports = self.__select_sheet('Transports',
                                         ['Plant',
                                          'OutputStep',
                                          'OutputPartType',
                                          'OutputPartName',
                                          'DestinationPlant',
                                          'Duration'],
                                         'Plant',
                                         str_columns=('Plant',
                                                      'OutputStep',
                                                      'OutputPartType',
                                                      'OutputPartName',
                                                      'DestinationPlant'))

        df_add_composite_id(transports, 'OutputStock_ID',
                            ['DestinationPlant', 'OutputPartType', 'OutputPartName', 'OutputStep'])
        df_add_composite_id(transports, 'InputStock_ID', ['Plant', 'OutputPartType', 'OutputPartName', 'OutputStep'])
        df_add_composite_id(transports, 'Transport_ID',
                            ['OutputPartType', 'OutputPartName', 'OutputStep', 'Plant', 'DestinationPlant'])
        df_add_composite_id(transports, 'Part_ID', ['OutputPartType', 'OutputPartName'])
        transports.set_index(['Transport_ID'], inplace=True)

        transports_init = self.__select_sheet('InitialTransports',
                                              ['Plant',
                                               'OutputStep',
                                               'OutputPartType',
                                               'OutputPartName',
                                               'DestinationPlant',
                                               'TimeStep',
                                               'Quantity'],
                                              'Plant',
                                              optionals=(('Value', 0),),
                                              str_columns=('Plant',
                                                           'OutputStep',
                                                           'OutputPartType',
                                                           'OutputPartName',
                                                           'DestinationPlant'))
        df_add_composite_id(transports_init, 'Transport_ID',
                            ['OutputPartType', 'OutputPartName', 'OutputStep', 'Plant', 'DestinationPlant'])

        transports_costs = self.__select_sheet('DataTransport',
                                               ['Plant',
                                                'OutputStep',
                                                'OutputPartType',
                                                'OutputPartName',
                                                'DestinationPlant',
                                                'TimeStep',
                                                'TransportUnitCost'],
                                               'Plant',
                                               optionals=(('CO2UnitEmissions', 0.0),),
                                               str_columns=('Plant',
                                                            'OutputStep',
                                                            'OutputPartType',
                                                            'OutputPartName',
                                                            'DestinationPlant'))
        df_add_composite_id(transports_costs, 'Transport_ID',
                            ['OutputPartType', 'OutputPartName', 'OutputStep', 'Plant', 'DestinationPlant'])

        customs_costs = self.__select_sheet('CustomsCosts',
                                            ['Plant',
                                             'OutputStep',
                                             'OutputPartType',
                                             'OutputPartName',
                                             'DestinationPlant',
                                             'TimeStep',
                                             'CustomsUnitCost'],
                                            'Plant',
                                            str_columns=('Plant',
                                                         'OutputStep',
                                                         'OutputPartType',
                                                         'OutputPartName',
                                                         'DestinationPlant'))
        df_add_composite_id(customs_costs, 'Transport_ID',
                            ['OutputPartType', 'OutputPartName', 'OutputStep', 'Plant', 'DestinationPlant'])

        stocks_init = self.__select_sheet('InitialStocks',
                                          ['Plant',
                                           'ProductionStep',
                                           'PartType',
                                           'PartName',
                                           'Quantity'],
                                          'Plant',
                                          optionals=(('Value', 0.0),),
                                          str_columns=('Plant',
                                                       'ProductionStep',
                                                       'PartType',
                                                       'PartName'))
        df_add_composite_id(stocks_init, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        stocks_init.set_index(['Stock_ID'], inplace=True)

        stocks_maxi = self.__select_sheet('StockMaxima',
                                          ['Plant',
                                           'ProductionStep',
                                           'PartType',
                                           'PartName',
                                           'MaximalStock'],
                                          'Plant',
                                          str_columns=('Plant',
                                                       'ProductionStep',
                                                       'PartType',
                                                       'PartName'))
        df_add_composite_id(stocks_maxi, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        stocks_maxi.set_index(['Stock_ID'], inplace=True)

        stocks_mini = self.__select_sheet('StockMinima',
                                          ['Plant',
                                           'ProductionStep',
                                           'PartType',
                                           'PartName',
                                           'MinimalStock'],
                                          'Plant',
                                          str_columns=('Plant',
                                                       'ProductionStep',
                                                       'PartType',
                                                       'PartName'))
        df_add_composite_id(stocks_mini, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        stocks_mini.set_index(['Stock_ID'], inplace=True)

        storage_costs = self.__select_sheet('StorageCosts',
                                            ['Plant',
                                             'ProductionStep',
                                             'PartType',
                                             'PartName',
                                             'TimeStep',
                                             'StorageUnitCost'],
                                            'Plant',
                                            str_columns=('Plant',
                                                         'ProductionStep',
                                                         'PartType',
                                                         'PartName'))
        df_add_composite_id(storage_costs, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])

        purchasing_costs = self.__select_sheet('DataPurchasedParts',
                                               ['Plant',
                                                'ProductionStep',
                                                'PartType',
                                                'PartName', ],
                                               'Plant',
                                               optionals=(('PurchasingUnitCost', 0.0),
                                                          ('CO2UnitEmissions', 0.0)),
                                               str_columns=('Plant',
                                                            'ProductionStep',
                                                            'PartType',
                                                            'PartName'))
        df_add_composite_id(purchasing_costs, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        purchasing_costs.set_index(['Stock_ID'], inplace=True)

        incomes = self.__select_sheet('Incomes',
                                      ['Plant',
                                       'ProductionStep',
                                       'PartType',
                                       'PartName',
                                       'UnitIncome'],
                                      'Plant',
                                      str_columns=('Plant',
                                                   'ProductionStep',
                                                   'PartType',
                                                   'PartName'))
        df_add_composite_id(incomes, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        incomes.set_index(['Stock_ID'], inplace=True)

        demands = self.__select_sheet('Demands',
                                      ['Plant',
                                       'ProductionStep',
                                       'PartType',
                                       'PartName',
                                       'TimeStep',
                                       'Demand'],
                                      'Plant',
                                      optionals=(('DemandRelativeUncertainty', 0.0),
                                                 ('Weight', 1.0)),
                                      str_columns=('Plant',
                                                   'ProductionStep',
                                                   'PartType',
                                                   'PartName'))
        df_add_composite_id(demands, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])

        demand_weights = self.__select_sheet('DemandWeights',
                                             ['Plant',
                                              'ProductionStep',
                                              'PartType',
                                              'PartName'],
                                             'Plant',
                                             optionals=(('WeightDemand', 1.0),
                                                        ('WeightBacklog', 1.0)),
                                             str_columns=('Plant',
                                                          'ProductionStep',
                                                          'PartType',
                                                          'PartName'))
        df_add_composite_id(demand_weights, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        demand_weights.set_index(['Stock_ID'], inplace=True)

        maximization = self.__select_sheet('Maximization',
                                           ['Plant',
                                            'ProductionStep',
                                            'PartType',
                                            'PartName'],
                                           'Plant',
                                           optionals=(('Weight', 1.0),),
                                           str_columns=('Plant',
                                                        'ProductionStep',
                                                        'PartType',
                                                        'PartName'))
        df_add_composite_id(maximization, 'Stock_ID', ['Plant', 'PartType', 'PartName', 'ProductionStep'])
        maximization.set_index(['Stock_ID'], inplace=True)

        input_stocks = set(inputs['InputStock_ID'].values)
        output_stocks = set(inputs['OutputStock_ID'].values)
        input_transports = set(transports['InputStock_ID'].values)
        output_transports = set(transports['OutputStock_ID'].values)

        pure_outputs = output_stocks.union(output_transports)

        stocks = sorted(input_stocks
                        .union(output_stocks)
                        .union(input_transports)
                        .union(output_transports))

        for stock_id in stocks:
            if stock_id in input_stocks:
                plant, step, part_id = inputs[inputs['InputStock_ID'] == stock_id][['Plant',
                                                                                    'InputStep',
                                                                                    'InputPart_ID']].values[0]
            elif stock_id in output_stocks:
                plant, step, part_id = inputs[inputs['OutputStock_ID'] == stock_id][['Plant',
                                                                                     'OutputStep',
                                                                                     'OutputPart_ID']].values[0]
            elif stock_id in input_transports:
                plant, step, part_id = transports[transports['InputStock_ID'] == stock_id][['Plant',
                                                                                            'OutputStep',
                                                                                            'Part_ID']].values[0]
            elif stock_id in output_transports:
                plant, step, part_id = transports[transports['OutputStock_ID'] == stock_id][['DestinationPlant',
                                                                                             'OutputStep',
                                                                                             'Part_ID']].values[0]
            else:
                break

            minimal_stock = 0.0
            if stock_id in stocks_mini.index:
                minimal_stock = float(stocks_mini.loc[stock_id].MinimalStock)

            maximal_stock = -1
            if stock_id in stocks_maxi.index:
                maximal_stock = float(stocks_maxi.loc[stock_id].MaximalStock)

            initial_stock = 0.0
            initial_value = 0.0
            if stock_id in stocks_init.index:
                initial_stock = float(stocks_init.loc[stock_id].Quantity)
                initial_value = float(stocks_init.loc[stock_id].Value)

            current_storage_costs = dict()
            for _, _, _, _, timestep, cost, _ in storage_costs[storage_costs['Stock_ID'] == stock_id].values:
                current_storage_costs[str(int(timestep))] = float(cost)

            income = 0.0
            if stock_id in incomes.index:
                income = float(incomes.loc[stock_id].UnitIncome)

            purchasing_cost = 0.0
            co2_emission = 0.0
            if stock_id in purchasing_costs.index:
                purchasing_cost = float(purchasing_costs.loc[stock_id].PurchasingUnitCost)
                co2_emission = float(purchasing_costs.loc[stock_id].CO2UnitEmissions)

            current_demands = dict()
            current_demands_uncertainties = dict()
            current_demands_weights = dict()
            for _, _, _, _, timestep, demand, uncertainty, weight, _ in demands[demands['Stock_ID'] == stock_id].values:
                current_demands[str(int(timestep))] = float(demand)
                current_demands_uncertainties[str(int(timestep))] = float(uncertainty)
                current_demands_weights[str(int(timestep))] = float(weight)

            backlog_weight = 0.0
            if stock_id in demand_weights.index:
                backlog_weight = float(demand_weights.loc[stock_id].WeightBacklog)
                if "0" not in current_demands_weights:
                    current_demands_weights["0"] = float(demand_weights.loc[stock_id].WeightDemand)

            maxim = 0.0
            if stock_id in maximization.index:
                maxim = float(maximization.loc[stock_id].Weight)

            is_infinite = stock_id not in pure_outputs and stock_id not in stocks_init.index

            self.stocks.append({"$metadata": {"$model": "dtmi:com:cosmotech:supplychain:Stock;1"},
                                "$id": self.__sanitize_adt_id(stock_id),
                                "Label": stock_id,
                                "PlantName": plant,
                                "Step": step,
                                "PartId": part_id,
                                "MinimalStock": minimal_stock,
                                "MaximalStock": maximal_stock,
                                "InitialStock": initial_stock,
                                "InitialValue": initial_value,
                                "StorageUnitCosts": current_storage_costs,
                                "PurchasingUnitCost": purchasing_cost,
                                "CO2UnitEmissions": co2_emission,
                                "UnitIncome": income,
                                "Demands": current_demands,
                                "DemandUncertainties": current_demands_uncertainties,
                                "DemandWeights": current_demands_weights,
                                "BacklogWeight": backlog_weight,
                                "MaximizationWeight": maxim,
                                "IsInfinite": is_infinite})

        for transport_id in transports.index:
            current_transport = transports.loc[transport_id]

            init_transport = dict()
            init_transport_values = dict()
            for *_, timestep, quantity, value, _ in transports_init[transports_init['Transport_ID']
                                                                    == transport_id].values:
                init_transport[str(int(timestep))] = float(quantity)
                init_transport_values[str(int(timestep))] = float(value)

            current_transport_costs = dict()
            current_co2_emissions = dict()
            for *_, timestep, cost, co2, _ in transports_costs[transports_costs['Transport_ID'] == transport_id].values:
                current_transport_costs[str(int(timestep))] = float(cost)
                current_co2_emissions[str(int(timestep))] = float(co2)

            current_customs_costs = dict()
            for *_, timestep, cost, _ in customs_costs[customs_costs['Transport_ID'] == transport_id].values:
                current_customs_costs[str(int(timestep))] = float(cost)

            self.relations.append({"$sourceId": self.__sanitize_adt_id(current_transport.InputStock_ID),
                                   "$targetId": self.__sanitize_adt_id(current_transport.OutputStock_ID),
                                   "$relationshipId": self.__sanitize_adt_id(transport_id),
                                   "$relationshipName": "Transport",
                                   "Label": transport_id,  # TODO to be removed when RelationshipId when available from azure-digital-twins-simulator-connector
                                   "Duration": int(current_transport.Duration),
                                   "InitialTransportedQuantities": init_transport,
                                   "InitialTransportedValues": init_transport_values,
                                   "TransportUnitCosts": current_transport_costs,
                                   "CO2UnitEmissions": current_co2_emissions,
                                   "CustomFees": current_customs_costs})

        for stock_id in input_stocks:
            for operation_id, input_quantity in inputs[inputs['InputStock_ID']
                                                       == stock_id][['Operation_ID',
                                                                     'InputQuantity']].values:
                self.relations.append({"$sourceId": self.__sanitize_adt_id(stock_id),
                                       "$targetId": self.__sanitize_adt_id(operation_id),
                                       "$relationshipId": self.__sanitize_adt_id(stock_id + "_to_" + operation_id),
                                       "$relationshipName": "input",
                                       "InputQuantity": input_quantity})
        for stock_id in output_stocks:
            for operation_id in sorted(set(inputs[inputs['OutputStock_ID'] == stock_id]['Operation_ID'].values)):
                self.relations.append({"$sourceId": self.__sanitize_adt_id(operation_id),
                                       "$targetId": self.__sanitize_adt_id(stock_id),
                                       "$relationshipId": self.__sanitize_adt_id(operation_id + "_to_" + stock_id),
                                       "$relationshipName": "output"})

    def generate_jsons(self):
        # Write configuration :
        self.split("{time_since_last_split:6.6} - Generating twins and relationships")
        self.read_configuration()
        self.read_production_resource()
        self.read_production_operations()
        self.read_stocks()
        self.split("{time_since_last_split:6.6} - Sending twins")
        self.write_json([self.configuration], "Configuration")
        self.write_json(self.machines, "ProductionResource")
        self.write_json(self.stocks, "Stock")
        self.write_json(self.operations, "ProductionOperation")
        self.split("{time_since_last_split:6.6} - Sending relationships")
        self.write_json(self.relations, "Relationships", False)

    def write_json(self, items, file_name: str = 'item.json', is_twin: bool = True):
        self.display_message(f"{file_name}: writing {len(items)} items")
        messages = [json.dumps(item, separators=(',', ':')) for item in items]

        if self.target == 'queue':
            queue_client = QueueClient.from_connection_string(self.connect_str,
                                                              self.queue_name,
                                                              message_encode_policy=TextBase64EncodePolicy())
            for send_message in messages:
                queue_client.send_message(send_message)
            count_messages = len(messages)
            self.display_message(f"Sending {count_messages} message{'s' if count_messages > 1 else ''} "
                                 f"of total size {sum(map(len, messages))} to {self.queue_name}")
        elif self.target == 'local_files':
            with open(self.output_path + "/" + file_name + ".json", "w") as configuration_file:
                if len(messages) > 1:
                    configuration_file.write(f'[{",".join(messages)}]')
                else:
                    configuration_file.write(messages[0])
        elif self.target == "local_csv":
            writer = CSVWriter(self.output_path)
            if is_twin:
                m = {"$id": "id"}
                new_items = [{(m[k] if k in m else k): json.dumps(v) for k, v in i.items()} for i in items]
                writer.write_from_list(new_items, file_name)
            else:
                separate_csvs = defaultdict(list)
                for item in items:
                    m = {"$sourceId": "source",
                         "$targetId": "target"}
                    separate_csvs[item['$relationshipName']].append({(m[k] if k in m else k): json.dumps(v)
                                                                     for k, v in item.items()})
                for csv_name, content in separate_csvs.items():
                    writer.write_from_list(content, csv_name)
        elif self.target == 'adt':
            if self.adt_writer is None:
                self.adt_writer = ADTWriter()
            self.adt_writer.send_items(items=items)

    def __sanitize_adt_id(selef, input: str) -> str:
        """
        Replace any non alphanumeric character by a '_' character
        This method is used to avoid limitations with identifiers in ADT
        :param input: input string
        :return: output string
        """
        return re.sub("[^0-9a-zA-Z]+", "_", input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SupplyChain Cosmo dataset to ADT converter')
    parser.add_argument('--input', type=str, required=False,
                        help='Input folder containing the dataset. Default to "./Input"', default='Input')
    parser.add_argument('--output', type=str, required=False,
                        help='Output folder to write the generated converted files. Default to "."', default='.')
    parser.add_argument('--queue_name', type=str, required=False,
                        help='Name of the queue used to upload the json generated for ADT injection',
                        default='adt-injector-communicator')
    parser.add_argument('--blob_name', type=str, required=False,
                        help='Name of the blob used to read original dataset',
                        default='datasetinput')
    parser.add_argument('--origin', type=str, required=False,
                        help='Origin of the data to transform',
                        choices=['blob', 'local_files'],
                        default='blob')
    parser.add_argument('--target', type=str, required=False,
                        help='Origin of the data to transform',
                        choices=['queue', 'local_files', 'adt', 'local_csv'],
                        default='local_files')
    args = parser.parse_args()
    with FromTableToDictConverter(input_path=args.input,
                                  output_path=args.output,
                                  queue_name=args.queue_name,
                                  blob_name=args.blob_name,
                                  origin=args.origin,
                                  target=args.target,
                                  connect_str=os.getenv("AZURE_STORAGE_CONNECTION_STRING")) as converter:
        converter.generate_jsons()
