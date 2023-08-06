from Supplychain.Generic.folder_io import FolderReader, FolderWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.simulator_files_description import simulator_format
from Supplychain.Schema.default_values import variables_default_values
from Supplychain.Generic.duration import seconds_to_iso_8061_duration
from datetime import datetime, tzinfo, timedelta
from Supplychain.Wrappers.environment_variables import SECONDS_IN_MINUTE

from collections import defaultdict, deque


class simple_utc(tzinfo):
    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)


def convert_dict(key_type, value_type, dict_item) -> dict:
    if dict_item is None:
        return dict()
    return {key_type(k): value_type(v)
            for k, v
            in sorted(dict_item.items(), key=lambda i: key_type(i[0]))}


def find_effective_value_for_time_step(time_step: int,
                                       schedule: dict) -> float:
    if time_step in schedule:
        return schedule[time_step]

    effective_time_step = max(int(k) for k in schedule.keys() if int(k) <= time_step)
    return schedule.get(str(effective_time_step), 0.0)


class FromDictToSimulatorConverter(Timer):

    def __init__(self,
                 reader: FolderReader,
                 writer: FolderWriter):
        Timer.__init__(self, prefix="[Convert]")

        self.reader = reader
        self.writer = writer

        self.configuration = self.reader.files.get('Configuration', [])[0]

        self.total_time_steps = self.configuration['StepsPerCycle'] * self.configuration['SimulatedCycles']

        self.files_content = dict()

        self.current_group = 0

        for key in simulator_format.keys():
            self.files_content[key] = list()

        self.entity_order = dict()

        self.lead_times = {}

    def __scheduler(self):
        inputs = self.reader.files.get('input', [])
        outputs = self.reader.files.get('output', [])
        contains = self.reader.files.get('contains', [])
        transports = self.reader.files.get('Transport', [])
        stocks = self.reader.files.get('Stock', [])

        operations_names = set(i['target'] for i in inputs)
        transports_names = set(t['Label'] for t in
                               transports)  # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector

        stocks_names = set(stock['id'] for stock in stocks)
        _input_stocks = set(i['source'] for i in inputs) | set(t['source'] for t in transports)
        _output_stocks = set(o['target'] for o in outputs) | set(t['target'] for t in transports)

        start_stocks = _input_stocks - _output_stocks
        final_stocks = _output_stocks - _input_stocks

        scheduled_elements = []
        for stock in sorted(start_stocks):
            scheduled_element = dict(Type='Rule',
                                     Name=stock,
                                     TaskName='Dispatch')
            scheduled_elements.append(scheduled_element)
        self.files_content['IndustrialNetworkScheduler'].extend(scheduled_elements)

        stocks_queue = deque()

        contractors = set(op['id']
                          for op in self.reader.files.get('ProductionOperation', [])
                          if op['IsContractor'])

        for st in final_stocks:
            stocks_queue.append(st)
            self.entity_order[st] = 0

        parents = defaultdict(set)

        # While we have stocks to treat we continue
        for links in [inputs, outputs]:
            for link in links:
                parents[link['source']].add(link['target'])
        for tr in transports:
            parents[tr['source']].add(tr['Label'])
            parents[tr['Label']].add(tr['target'])

        for production_resource in [c['source'] for c in contains]:
            brotherhood = [c['target'] for c in contains if c['source'] == production_resource]
            first_child = brotherhood.pop()
            for child in brotherhood:
                parents[first_child] |= parents[child]
            for child in brotherhood:
                parents[child] = parents[first_child]

        max_depth = 0

        def get_entity_order(_entity):
            if _entity not in self.entity_order:
                self.entity_order[_entity] = 1 + max(map(get_entity_order, parents[_entity]))
            return self.entity_order[_entity]

        for entity in parents.keys():
            o = get_entity_order(entity)
            max_depth = max(max_depth, o)

        operation_order = [[] for _ in range(max_depth)]
        for k, v in self.entity_order.items():
            if k in transports_names or k in operations_names:
                operation_order[v].append(k)

        operation_order.reverse()
        operation_order = [i for i in operation_order if len(i) > 0]

        scheduled_ComputeStockToTransfer_stocks = set()

        for list_operations in operation_order:
            # For each rank of operation, every operation can be done in parallel, so order is not important

            # To schedule we need some entities and information about them:

            fixed_ee = set()
            # StockToOperation edge entities linked to the contractor Operation
            # entites considered at this rank.

            prop_ee = set()
            # StockToOperation edge entities linked to the regular Operation
            # entites considered at this rank.

            all_fixed_ee = set()
            # StockToOperation edge entities linked to the Stock entities which
            # are taken as input by the contractor Operation entities considered
            #  at this rank and for which ComputeStockToTransfer processes were
            # not scheduled yet.

            all_prop_ee = set()
            # StockToOperation edge entities linked to the Stock entities which
            #  are taken as input by the regular Operation entities considered at
            # this rank and for which ComputeStockToTransfer processes were not
            # scheduled yet.

            input_stocks = set()
            # Stock entities taken as input by the Operation entities considered
            # at this rank and for which ComputeStockToTransfer processes were
            # not scheduled yet.

            machines = set()
            # Machine entities containing the non transport Operation entities
            #  considered at this rank.

            operation_ee = set()
            # StockToOperation edge entities for the non transport Operation
            # entities considered at this rank.

            transport_ops = set()
            # Operation entities considered at this rank which are transports.

            end_stocks = set()
            # Stock entities outputed by the Operation entities considered at
            # this rank.

            for operation in list_operations:
                if operation in operations_names:
                    edge_entities = set(i['source'] + '_to_' + i['target']
                                        for i in inputs
                                        if i['target'] == operation)
                    machines.add(next(c['source']
                                      for c in contains
                                      if c['target'] == operation))
                    stock = next(o['target']
                                 for o in outputs
                                 if o['source'] == operation)
                    operation_ee.update(edge_entities)
                    input_stocks |= set((i['source']
                                         for i in inputs
                                         if i['target'] == operation))
                else:
                    edge_entities = set(t['source'] + '_to_' + t['Label']
                                        for t in transports
                                        if t['Label'] == operation)
                    transport_ops.add(operation)
                    stock = next(t['target']
                                 for t in transports
                                 if t['Label'] == operation)
                    input_stocks |= set((t['source']
                                         for t in transports
                                         if t['Label'] == operation))

                if operation in contractors:
                    fixed_ee.update(edge_entities)
                else:
                    prop_ee.update(edge_entities)

                end_stocks.add(stock)

            input_stocks -= scheduled_ComputeStockToTransfer_stocks
            if input_stocks:
                scheduled_ComputeStockToTransfer_stocks |= input_stocks
                for i in inputs:
                    if i['source'] in input_stocks:
                        operation = i['target']
                        (all_fixed_ee if operation in contractors else all_prop_ee).add(
                            i['source'] + '_to_' + operation)
                for t in transports:
                    if t['source'] in input_stocks:
                        operation = t['Label']
                        (all_fixed_ee if operation in contractors else all_prop_ee).add(
                            t['source'] + '_to_' + operation)

            # Names must be sorted to stabilize the output schedule.
            all_fixed_ee = sorted(all_fixed_ee)
            fixed_ee = sorted(fixed_ee)
            all_prop_ee = sorted(all_prop_ee)
            prop_ee = sorted(prop_ee)
            machines = sorted(machines)
            operation_ee = sorted(operation_ee)
            transport_ops = sorted(transport_ops)
            end_stocks = sorted(end_stocks)

            # Now we can create our scheduled Processes / Rules
            scheduled_elements = []

            # As soon as a ComputeStockToTransfer process is scheduled for a
            # particular stock, all ComputeStockToTransfer processes for the
            # said stock should be scheduled at the same time. Moreover, they
            # should be scheduled only once.
            for EE in all_fixed_ee:
                scheduled_element = dict(Type='Process',
                                         Name=EE,
                                         TaskName='ComputeStockToTransfer')
                scheduled_elements.append(scheduled_element)

            for EE in fixed_ee:
                scheduled_element = dict(Type='Process',
                                         Name=EE,
                                         TaskName='TransferStock')
                scheduled_elements.append(scheduled_element)

            for EE in all_prop_ee:
                scheduled_element = dict(Type='Process',
                                         Name=EE,
                                         TaskName='ComputeStockToTransfer')
                scheduled_elements.append(scheduled_element)

            for EE in prop_ee:
                scheduled_element = dict(Type='Process',
                                         Name=EE,
                                         TaskName='TransferStock')
                scheduled_elements.append(scheduled_element)

            for mac in machines:
                scheduled_element = dict(Type='Rule',
                                         Name=mac,
                                         TaskName='SelectStock')
                scheduled_elements.append(scheduled_element)

            for EE in operation_ee:
                scheduled_element = dict(Type='Process',
                                         Name=EE,
                                         TaskName='SendBackStockIfNecessary')
                scheduled_elements.append(scheduled_element)

            for mac in machines:
                scheduled_element = dict(Type='Process',
                                         Name=mac,
                                         TaskName='LaunchProcessing')
                scheduled_elements.append(scheduled_element)

            for transport in transport_ops:
                scheduled_element = dict(Type='Rule',
                                         Name=transport,
                                         TaskName='SelectStock')
                scheduled_elements.append(scheduled_element)

            for transport in transport_ops:
                scheduled_element = dict(Type='Process',
                                         Name=transport,
                                         TaskName='Process')
                scheduled_elements.append(scheduled_element)

            for stock in end_stocks:
                scheduled_element = dict(Type='Rule',
                                         Name=stock,
                                         TaskName='ReceiveStock')
                scheduled_elements.append(scheduled_element)

            for stock in end_stocks:
                scheduled_element = dict(Type='Rule',
                                         Name=stock,
                                         TaskName='Dispatch')
                scheduled_elements.append(scheduled_element)

            self.files_content['IndustrialNetworkScheduler'].extend(scheduled_elements)
        self.files_content['IndustrialNetworkScheduler'].append(dict(
            Type='Process',
            Name='IndustrialNetwork',
            TaskName='MesoResolveDemands'
        ))
        self.files_content['IndustrialNetworkScheduler'].extend((
            dict(
                Type='Rule',
                Name=stock,
                TaskName='CheckLevelAndOrderIfNecessary'
            )
            for stock in sorted(sorted(stocks_names), key=lambda e: self.entity_order.get(e, -1))
        ))
        self.writer.write_from_list(self.files_content['IndustrialNetworkScheduler'], 'IndustrialNetworkScheduler',
                                    ordering_key=None)

    def __lead_times(self):
        inputs = self.reader.files.get('input', [])
        operations = self.reader.files.get('ProductionOperation', [])
        outputs = self.reader.files.get('output', [])
        stocks = self.reader.files.get('Stock', [])
        transports = self.reader.files.get('Transport', [])

        stock_names = set(stock['id'] for stock in stocks)

        non_input_stock_names = (
            stock_names
            - set(i['source'] for i in inputs)
            - set(transport['source'] for transport in transports)
        )
        non_output_stock_names = (
            stock_names
            - set(output['target'] for output in outputs)
            - set(transport['target'] for transport in transports)
        )

        parents = defaultdict(set)
        for links in [inputs, outputs]:
            for link in links:
                parents[link['target']].add(link['source'])
        for transport in transports:
            parents[transport['Label']].add(transport['source'])
            parents[transport['target']].add(transport['Label'])

        durations = {
            stock['id']: 0
            for stock in stocks
        } | {
            operation['id']: operation['Duration']
            for operation in operations
        } | {
            transport['Label']: transport['Duration']
            for transport in transports
        }

        for stock_name in non_output_stock_names:
            self.lead_times[stock_name] = 0

        def get_lead_time(entity):
            if entity not in self.lead_times:
                self.lead_times[entity] = max(get_lead_time(parent) for parent in parents[entity]) + durations[entity]
            return self.lead_times[entity]

        for stock_name in non_input_stock_names:
            get_lead_time(stock_name)

    def __operation(self):

        operations_csv = self.reader.files.get('ProductionOperation', [])
        contains_csv = self.reader.files.get('contains', [])
        outputs = self.reader.files.get('output', [])
        stock_csv = self.reader.files.get('Stock', [])

        for operation in operations_csv:
            parent_resource = next(c['source']
                                   for c in contains_csv
                                   if c['target'] == operation['id'])
            output_stock = next(
                link['target']
                for link in outputs
                if link['source'] == operation['id']
            )
            follows_stock_policy = next(
                stock['StockPolicy'] != 'None'
                for stock in stock_csv
                if stock['id'] == output_stock
            )
            operation_item = {
                "Name": operation['id'],
                "ParentName": parent_resource,
                "OperatingPerformanceSchedule": convert_dict(int,
                                                             float,
                                                             operation['OperatingPerformances']),
                "CycleTimeSchedule": convert_dict(int,
                                                  float,
                                                  operation['CycleTimes']),
                "RejectRateSchedule": convert_dict(int,
                                                   float,
                                                   operation['RejectRates']),
                "OperatingPerformanceUncertaintySchedule": convert_dict(int,
                                                                        float,
                                                                        operation['OperatingPerformanceUncertainties']),
                "ProductionUnitCostSchedule": convert_dict(int,
                                                           float,
                                                           operation['ProductionUnitCosts']),
                "CO2UnitEmissionsSchedule": convert_dict(int,
                                                         float,
                                                         operation['CO2UnitEmissions']),
                "ProductionPlanSchedule": convert_dict(int,
                                                       float,
                                                       operation['QuantitiesToProduce']),
                "InvestmentCost": operation['InvestmentCost'],
                "IsContractor": operation['IsContractor'],
                "Priority": operation['Priority'],
                "SchedulingStep": self.entity_order.get(operation['id'], -1),
                "FollowsStockPolicy": follows_stock_policy,
                "Duration": operation['Duration'],
                "LeadTime": self.lead_times[operation['id']],
            }
            self.files_content['BE_Operation'].append(operation_item)
        self.writer.write_from_list(self.files_content['BE_Operation'], 'BE_Operation', ordering_key='Name')

    def __model_parameters(self):

        production_plan_is_available = all(bool(po['QuantitiesToProduce'])
                                           for po in self.reader.files.get('ProductionOperation', []))
        model_parameters = {
            "TimeStepDuration":
                seconds_to_iso_8061_duration(self.configuration['TimeStepDuration'] * SECONDS_IN_MINUTE),
            "TimeStepPerCycle":
                self.configuration['StepsPerCycle'],
            "NumberOfCycle":
                self.configuration['SimulatedCycles'],
            "StartingDate":
                datetime.fromisoformat(self.configuration['StartingDate']).replace(tzinfo=simple_utc()).isoformat(),
            "ManageBacklogQuantities":
                self.configuration['ManageBacklogQuantities'],
            "OptimizationObjective":
                self.configuration['OptimizationObjective'],
            "ActivateUncertainties":
                self.configuration['ActivateUncertainties'],
            "EmptyObsoleteStocks":
                self.configuration['EmptyObsoleteStocks'],
            "UncertaintiesProbabilityDistribution":
                self.configuration['UncertaintiesProbabilityDistribution'],
            "ActivateVariableMachineOpeningRate":
                self.configuration['ActivateVariableMachineOpeningRate'],
            "ImmobilizedCashRelativeCost":
                self.configuration['FinancialCostOfStock'],
            "BatchSize":
                self.configuration['BatchSize'],
            "ExtraProductionPlanIsAvailable":
                production_plan_is_available,
            "EnforceProductionPlan":
                self.configuration['EnforceProductionPlan'],
            "AllowPartRetention":
                self.configuration['IntermediaryStockDispatchPolicy'] == 'AllowRetention',
        }

        self.files_content['ModelParameters'].append(model_parameters)
        self.writer.write_from_list(self.files_content['ModelParameters'], 'ModelParameters', ordering_key=None)

    def __stock(self):
        stock_csv = self.reader.files.get('Stock', [])
        for stock in stock_csv:
            maximal_stock = stock['MaximalStock']
            stock_item = {"Name": stock['id'],
                          "CurrentStock": stock['InitialStock'],
                          "MinimalStock": stock['MinimalStock'],
                          "MaximalStock": maximal_stock if maximal_stock is not None else -1,
                          "Value": stock['InitialValue'],
                          "PurchasingUnitCost": stock['PurchasingUnitCost'],
                          "CO2UnitEmissions": stock['CO2UnitEmissions'],
                          "UnitIncome": stock['UnitIncome'],
                          "Demand": dict(),
                          "StorageUnitCostSchedule": convert_dict(int, float, stock['StorageUnitCosts']),
                          "IsInfinite": stock['IsInfinite'],
                          "StockPolicy": stock['StockPolicy'],
                          "SourcingPolicy": stock['SourcingPolicy'],
                          "DispatchPolicy": stock['DispatchPolicy'],
                          "ReviewPeriod": stock['ReviewPeriod'],
                          "NextReview": stock['NextReview'],
                          "Advance": stock['Advance'],
                          "LeadTime": self.lead_times[stock['id']],
                          "SalesForecasts": convert_dict(int, float, stock['SalesForecasts']),
                          "OrderPointSchedule": convert_dict(int, float, stock['OrderPoints']),
                          "OrderQuantitySchedule": dict(),
                          "SafetyQuantitySchedule": convert_dict(int, float, stock['SafetyQuantities']),
                          "SchedulingStep": self.entity_order.get(stock['id'], -1)}

            if stock_item['StockPolicy'] == 'OrderPointFixedQuantity':
                stock_item['OrderQuantitySchedule'] = convert_dict(int, float, stock['OrderQuantities'])
            elif stock_item['StockPolicy'] == 'OrderPointVariableQuantity':
                stock_item['OrderQuantitySchedule'] = convert_dict(int, float, stock['OrderUpToLevels'])

            backlog_weight = stock['BacklogWeight']
            last_uncertainty = 0

            if stock['Demands']:
                demands = convert_dict(int, float, stock['Demands'])
                demands_weight = convert_dict(int, float, stock['DemandWeights'])
                demands_uncertainties = convert_dict(int, float, stock['DemandUncertainties'])

                last_weight = 0

                for time_step in range(self.total_time_steps):
                    if time_step in demands_weight:
                        last_weight = demands_weight[time_step]
                    if time_step in demands_uncertainties:
                        last_uncertainty = demands_uncertainties[time_step]
                    if time_step in demands and demands[time_step]:
                        current_demand = dict(ExternalDemand=demands[time_step],
                                              InternalDemand=0.0,
                                              BacklogWeight=backlog_weight,
                                              ExternalWeight=last_weight,
                                              InternalWeight=0.0,
                                              WeightMax=0.0,
                                              MaxVal=0.0,
                                              DemandRelativeUncertainty=last_uncertainty)
                        stock_item['Demand'][time_step] = current_demand

            maximization_weight = stock['MaximizationWeight']
            if maximization_weight:
                total_max_production = 0
                for time_step in range(self.total_time_steps):
                    total_max_production += self.compute_theoretical_maximum_production(stock['id'],
                                                                                      time_step)
                if self.total_time_steps - 1 not in stock_item['Demand']:
                    current_demand = dict(ExternalDemand=0.0,
                                          InternalDemand=0.0,
                                          BacklogWeight=backlog_weight,
                                          ExternalWeight=0.0,
                                          InternalWeight=0.0,
                                          WeightMax=0.0,
                                          MaxVal=0.0,
                                          DemandRelativeUncertainty=last_uncertainty)
                    stock_item['Demand'][self.total_time_steps - 1] = current_demand
                stock_item['Demand'][self.total_time_steps - 1]['WeightMax'] = maximization_weight
                stock_item['Demand'][self.total_time_steps - 1]['MaxVal'] = total_max_production

            self.files_content['BE_Stock'].append(stock_item)
        self.writer.write_from_list(self.files_content['BE_Stock'], 'BE_Stock', ordering_key='Name')

    def compute_theoretical_maximum_production(self, stock_id: str, time_step: int) -> float:
        stock = next(
            s
            for s in self.reader.files.get('Stock', [])
            if s['id'] == stock_id
        )
        theoretical_maximum = stock['InitialStock'] if time_step == 0 else 0.0
        transports = [
            transport
            for transport in self.reader.files.get('Transport', [])
            if transport['target'] == stock_id
        ]
        for transport in transports:
            origin = transport['source']
            duration = transport['Duration']
            if time_step >= duration:
                theoretical_maximum += self.compute_theoretical_maximum_production(origin, time_step - duration)
            else:
                theoretical_maximum += transport['InitialTransportedQuantities'].get(str(duration - time_step - 1), 0.0)
        operation_names = set(
            output['source']
            for output in self.reader.files.get('output', [])
            if output['target'] == stock_id
        )
        operations = [
            operation
            for operation in self.reader.files.get('ProductionOperation', [])
            if operation['id'] in operation_names
        ]
        for operation in operations:
            if operation['IsContractor']:
                theoretical_maximum += find_effective_value_for_time_step(time_step,
                                                                        operation['QuantitiesToProduce'])
            else:
                pr_name = next(
                    contains['source']
                    for contains in self.reader.files.get('contains', [])
                    if contains['target'] == operation['id']
                )
                pr_data = next(
                    pr
                    for pr in self.reader.files.get('ProductionResource', [])
                    if pr['id'] == pr_name
                )
                max_opening_time = find_effective_value_for_time_step(time_step, pr_data['OpeningTimes'])
                ct = (
                    find_effective_value_for_time_step(time_step, operation['CycleTimes'])
                    if operation['CycleTimes']
                    else variables_default_values['ProductionOperation']['CycleTimes']
                )
                rr = (
                    find_effective_value_for_time_step(time_step, operation['RejectRates'])
                    if operation['RejectRates']
                    else variables_default_values['ProductionOperation']['RejectRates']
                )
                op = (
                    find_effective_value_for_time_step(time_step, operation['OperatingPerformances'])
                    if operation['OperatingPerformances']
                    else variables_default_values['ProductionOperation']['OperatingPerformances']
                )
                theoretical_maximum += (max_opening_time / ct) * op * (1.0 - rr)
        return theoretical_maximum

    def __machine(self):
        pr_csv = self.reader.files.get('ProductionResource', [])
        contains_csv = self.reader.files.get('contains', [])

        for pr in pr_csv:
            target_operations = [c['target']
                                 for c in contains_csv
                                 if c['source'] == pr['id']]
            operations_count = len(target_operations)
            target_propotions = {op: 1.0 / operations_count
                                 for op in sorted(target_operations)}

            group = {}
            if operations_count > 1:
                group = {self.current_group: {"StartCycle": 0,
                                              "EndCycle": self.configuration['SimulatedCycles'] - 1}}
                self.current_group += 1

            pr_item = {"Name": pr['id'],
                       "StockTypeProportion": [target_propotions] * self.configuration['SimulatedCycles'],
                       "Groups": group,
                       "OpeningRates": [1] * self.configuration['SimulatedCycles'],
                       "OpeningTimeSchedule": convert_dict(int,
                                                           float,
                                                           pr['OpeningTimes']),
                       "ProductionCostSchedule": convert_dict(int,
                                                              float,
                                                              pr['FixedProductionCosts']),
                       "ProductionPolicy": pr['ProductionPolicy']}
            self.files_content['CE_Machine'].append(pr_item)
        self.writer.write_from_list(self.files_content['CE_Machine'], 'CE_Machine', ordering_key='Name')

    def __op_to_stock(self):
        output_csv = self.reader.files.get('output', [])
        for o in output_csv:
            op_to_stock_item = {"StockName": o['target'],
                                "OperationName": o['source']}
            self.files_content['Arcs_OperationToStock'].append(op_to_stock_item)
        output_csv = self.reader.files.get('Transport', [])
        for o in output_csv:
            op_to_stock_item = {"StockName": o['target'],
                                "OperationName": o['Label']}
            self.files_content['Arcs_OperationToStock'].append(op_to_stock_item)
        self.writer.write_from_list(self.files_content['Arcs_OperationToStock'], 'Arcs_OperationToStock',
                                    ordering_key='StockName')

    def __transport(self):
        transport_csv = self.reader.files.get('Transport', [])
        stock_csv = self.reader.files.get('Stock', [])

        def dict_to_list(duration: int, data: dict):
            if data:
                return [data.get(str(t), 0.0) for t in range(duration)]
            return [0.0 for _ in range(duration)]

        for transport in transport_csv:
            follows_stock_policy = next(
                stock['StockPolicy'] != 'None'
                for stock in stock_csv
                if stock['id'] == transport['target']
            )
            transport_item = {
                "Name": transport['Label'],
                # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                "Duration": transport['Duration'],
                "InitialTransportQuantity": dict_to_list(transport['Duration'],
                                                         transport['InitialTransportedQuantities']),
                "InitialTransportValue": dict_to_list(transport['Duration'],
                                                      transport['InitialTransportedValues']),
                "TransportUnitCostSchedule": convert_dict(int,
                                                          float,
                                                          transport['TransportUnitCosts']),
                "CustomsUnitCostSchedule": convert_dict(int,
                                                        float,
                                                        transport['CustomFees']),
                "CO2UnitEmissionsSchedule": convert_dict(int,
                                                         float,
                                                         transport['CO2UnitEmissions']),
                "Priority": transport['Priority'],
                "SchedulingStep": self.entity_order.get(transport['Label'], -1),
                "FollowsStockPolicy": follows_stock_policy,
                "LeadTime": self.lead_times[transport['Label']],
            }
            self.files_content['BE_TransportOperation'].append(transport_item)

        self.writer.write_from_list(self.files_content['BE_TransportOperation'], 'BE_TransportOperation',
                                    ordering_key='Name')

    def __stock_to_operation(self):
        input_csv = self.reader.files.get('input', [])
        transport_csv = self.reader.files.get('Transport', [])

        number_of_edges_by_stock = defaultdict(int)

        for i in input_csv:
            number_of_edges_by_stock[i['source']] += 1

        for t in transport_csv:
            number_of_edges_by_stock[t['source']] += 1

        groups = dict()

        stock_has_demand = {s['id']: bool(s['Demands'])  # DS
                            for s in self.reader.files.get('Stock', [])}

        for stock in sorted(number_of_edges_by_stock.keys()):
            groups[stock] = {}
            if number_of_edges_by_stock[stock] > 1 or stock_has_demand[stock]:
                groups[stock] = {self.current_group: {"StartCycle": 0,
                                                      "EndCycle": self.configuration['SimulatedCycles'] - 1}}
                self.current_group += 1

        contractors = set(op['id']
                          for op in self.reader.files.get('ProductionOperation', [])
                          if op['IsContractor'])

        for i in input_csv:
            prop_sto = [1 / number_of_edges_by_stock[i['source']]] * self.configuration['SimulatedCycles']
            sto_item = {"Name": i['source'] + "_to_" + i['target'],
                        "OperationName": i['target'],
                        "StockName": i['source'],
                        "PropStockForOperation": prop_sto,
                        "IsProportion": i['target'] not in contractors,
                        "Groups": groups[i['source']],
                        "Cardinality": i['InputQuantity']}
            self.files_content['EE_StockToOperation'].append(sto_item)

        for i in transport_csv:
            prop_sto = [1 / number_of_edges_by_stock[i['source']]] * self.configuration['SimulatedCycles']
            sto_item = {"Name": i['source'] + "_to_" + i['Label'],
                        "OperationName": i['Label'],
                        # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                        "StockName": i['source'],
                        "PropStockForOperation": prop_sto,
                        "IsProportion": True,
                        "Groups": groups[i['source']],
                        "Cardinality": 1}
            self.files_content['EE_StockToOperation'].append(sto_item)

        self.writer.write_from_list(self.files_content['EE_StockToOperation'], 'EE_StockToOperation',
                                    ordering_key='Name')

    def transform(self):
        self.__scheduler()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - IndustrialNetworkScheduler")
        self.__lead_times()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Lead times")
        self.__stock()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_Stock")
        self.__operation()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_Operation")
        self.__transport()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_TransportOperation")
        self.__machine()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - CE_Machine")
        self.__op_to_stock()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Arcs_OperationToStock")
        self.__stock_to_operation()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - EE_StockToOperation")
        self.__model_parameters()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - ModelParameters")
