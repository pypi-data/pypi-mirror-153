from Supplychain.Generic.cosmo_api_parameters import CosmoAPIParameters
from Supplychain.Generic.folder_io import FolderWriter, FolderReader
from Supplychain.Wrappers.environment_variables import SECONDS_IN_MINUTE
from Supplychain.Generic.excel_folder_reader import ExcelReader
from Supplychain.Generic.csv_folder_reader import CSVReader
from Supplychain.Generic.memory_folder_io import MemoryFolderIO
from Supplychain.Transform.from_table_to_dict import write_transformed_data
from Supplychain.Generic.timer import Timer
from dateutil import parser
import math
from typing import Union

GRANULARITIES = {
    'minute':
        1,
    'hour':
        60,
    'day':
        60 * 24,
    'week':
        60 * 24 * 7,
    'month':
        60 * 24 * 30,
    'quarter':
        60 * 24 * 90,
    'year':
        60 * 24 * 365
}


def object_to_bool(item: Union[object, str]) -> bool:
    if type(item) is str:
        return item.lower() == 'true'
    return bool(item)


class DictPatcher(Timer):

    def __write_updated_files(self):
        to_use_reader = self.memory

        # ADT column names to be replaced for post ADT simulation
        name_replacements = {"$sourceId": "source",
                             "$targetId": "target",
                             "$id": "id"}

        for file_name, file_content in to_use_reader.files.items():
            self.writer.write_from_list(dict_list=[
                {
                    name_replacements.get(item_k, item_k): item_v
                    for item_k, item_v in item.items()
                }
                for item in file_content], file_name=file_name)

    def __init__(self,
                 reader: FolderReader,
                 writer: FolderWriter,
                 parameters: CosmoAPIParameters):
        Timer.__init__(self, "[ParameterHandler]")
        self.parameters = parameters
        self.writer = writer
        self.reader = reader

        self.memory = MemoryFolderIO()
        for file_name, file_content in self.reader.files.items():
            self.memory.write_from_list(dict_list=file_content, file_name=file_name)
        if 'Configuration' not in self.memory.files:
            self.memory.files['Configuration'] = [dict(),]

    def handle_mass_action_lever(self):
        try:
            lever_folder = self.parameters.get_dataset_path("mass_lever_excel_file")
        except ValueError:
            self.display_message("No mass action lever found - skipping")
            return False, 0
        lever_reader = ExcelReader(lever_folder, keep_nones=False)
        self.memory.reset()

        reading_errors = write_transformed_data(
            reader=lever_reader,
            writer=self.memory
        )
        if reading_errors:
            return True, reading_errors
        if not self.memory.files.setdefault('Configuration', []):
            self.memory.files['Configuration'].append({})

        self.__write_updated_files()
        return True, 0

    def handle_simple_simulation(self):
        configuration = self.memory.files['Configuration'][0]

        start_date = parser.isoparse(self.parameters.get_named_parameter('start_date').value)
        end_date = parser.isoparse(self.parameters.get_named_parameter('end_date').value)
        simulation_granularity = GRANULARITIES.get(self.parameters.get_named_parameter('simulation_granularity').value,
                                                   GRANULARITIES['day'])

        duration = (end_date - start_date).total_seconds() // SECONDS_IN_MINUTE

        steps = int(math.ceil(duration / simulation_granularity))

        self.display_message(f"Starting Date: {start_date.isoformat()}")
        self.display_message(f"Simulated Cycles: {steps}")
        self.display_message(f"Steps per Cycle: {1}")
        self.display_message(f"TimeStep Duration: {simulation_granularity} minutes")

        configuration['StartingDate'] = start_date.isoformat()
        configuration['SimulatedCycles'] = steps
        configuration['StepsPerCycle'] = 1
        configuration['TimeStepDuration'] = simulation_granularity

        self.__handle_demand_plan()
        self.__handle_transport_duration()
        self.__handle_production_resource_opening_time()

        self.__write_updated_files()

    def handle_optimization_parameter(self):
        parameters = (('optimization_objective', 'OptimizationObjective', 'Optimization Objective', None),)
        for name, config_name, display_name, type_f in parameters:
            self.__handle_configuration_parameter(name, config_name, display_name, type_f)
        self.__write_updated_files()

    def handle_flow_management_policies(self):
        parameters = (('stock_policy', 'Stock', 'StockPolicy'),
                      ('sourcing_policy', 'Stock', 'SourcingPolicy'),
                      ('stock_dispatch_policy', 'Stock', 'DispatchPolicy'),
                      ('production_policy', 'ProductionResource', 'ProductionPolicy'))
        for parameter_name, entity_type, entity_parameter_name in parameters:
            try:
                parameter_value = self.parameters.get_named_parameter(parameter_name).value
            except ValueError:
                self.display_message(f"{parameter_name} is not defined - skipping")
                continue
            if parameter_value == 'FromDataset':
                continue
            if entity_type not in self.memory.files:
                continue
            entities = self.memory.files[entity_type]
            for entity in entities:
                entity[entity_parameter_name] = parameter_value
            entities_count = len(entities)
            self.display_message(f'Set {entity_parameter_name} to {parameter_value} for all {entity_type} '
                                 f'({entities_count} entit{"ies" if entities_count > 1 else "y"})')
        self.__write_updated_files()

    def handle_model_behavior(self):
        parameters = (('manage_backlog_quantities', 'ManageBacklogQuantities', 'Manage Backlog Quantities',
                       object_to_bool),
                      ('empty_obsolete_stocks', 'EmptyObsoleteStocks', 'Empty Obsolete Stocks',
                       object_to_bool),
                      ('batch_size', 'BatchSize', 'Batch Size',
                       int),
                      ('financial_cost_of_stocks', 'FinancialCostOfStock', 'Financial Cost Of Stock',
                       float),
                      ('intermediary_stock_dispatch', 'IntermediaryStockDispatchPolicy',
                       'Intermediary Stock Dispatch Policy', None))
        for name, config_name, display_name, type_f in parameters:
            self.__handle_configuration_parameter(name, config_name, display_name, type_f)
        self.__write_updated_files()

    def handle_uncertainties_settings(self):
        if self.__handle_configuration_parameter('uncertainties_probability_distribution',
                                                 'UncertaintiesProbabilityDistribution',
                                                 'Uncertainties Probability Distribution',
                                                 None):
            self.__write_updated_files()

    def __handle_configuration_parameter(self,
                                         parameter_name: str,
                                         configuration_parameter_name: str,
                                         display_name: str,
                                         type_function) -> bool:
        configuration = self.memory.files['Configuration'][0]
        try:
            parameter_value = self.parameters.get_named_parameter(parameter_name).value
        except ValueError:
            self.display_message(f"{parameter_name} is not defined - skipping")
            return False
        param_value = (parameter_value
                       if type_function is None
                       else type_function(parameter_value))
        self.display_message(f"{display_name}: {param_value}")
        configuration[configuration_parameter_name] = param_value
        return True


    def __handle_demand_plan(self):
        try:
            demand_plan_folder = self.parameters.get_dataset_path("demand_plan")
        except ValueError:
            self.display_message("No demand plan found - skipping")
            return
        reader = CSVReader(demand_plan_folder)
        stock_changes = dict()
        for k, demand_plan in reader.files.items():
            for _demand in demand_plan:
                stock_id = _demand.get('id')
                timestep = str(_demand.get('Timestep'))
                stock_changes.setdefault(stock_id, dict())
                for key in ['Demands', 'DemandUncertainties', 'DemandWeights']:
                    stock_changes[stock_id].setdefault(key, dict())
                    if key in _demand:
                        stock_changes[stock_id][key][timestep] = _demand.get(key)

        stocks = self.memory.files['Stock']
        for stock in stocks:
            _id = stock['id']
            for key in ['Demands', 'DemandUncertainties', 'DemandWeights']:
                if _id in stock_changes:
                    stock[key] = stock_changes[_id][key]
                else:
                    stock[key] = {}

    def __handle_transport_duration(self):
        try:
            transport_duration_folder = self.parameters.get_dataset_path("transport_duration")
        except ValueError:
            self.display_message("No lever for transport duration found - skipping")
            return
        reader = CSVReader(transport_duration_folder)

        duration_changes = dict()
        for k, transport_durations in reader.files.items():
            for _td in transport_durations:
                source = _td.get('source')
                target = _td.get('target')
                duration = int(_td.get('Duration'))
                duration_changes[(source, target)] = duration
        for e in self.memory.files['Transport']:
            duration = duration_changes.get((e.get('source'), e.get('target')))
            if duration:
                e['Duration'] = duration

    def __handle_production_resource_opening_time(self):
        try:
            pr_opening_time_folder = self.parameters.get_dataset_path("production_resource_opening_time")
        except ValueError:
            self.display_message("No lever for production resource opening time found - skipping")
            return
        reader = CSVReader(pr_opening_time_folder)

        opening_changes = dict()
        for k, changes in reader.files.items():
            for _td in changes:
                _id = _td.get('id')
                timestep = _td.get('Timestep')
                opening_time = float(_td.get('OpeningTimes'))
                opening_changes.setdefault(_id, dict())
                opening_changes[_id][timestep] = opening_time
        for e in self.memory.files.get('ProductionResource',[]):
            change = opening_changes.get(e['id'])
            if change:
                e['OpeningTimes'] = change
