#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from collections import namedtuple
# environ change to avoid a crash on multiple simulations: PROD-5387
os.environ['CSM_METRICS_MODE'] = "off"

import pandas

import csm.engine as CosmoEngine


def register_into_simulatorinterface(method):
    if hasattr(method, "fget"):
        name = method.fget.__name__
    else:
        name = method.__name__
    setattr(CosmoEngine.SimulatorInterface, name, method)
    return method


@register_into_simulatorinterface
@property
def machine_list(self):
    return [
        e.GetName()
        for e in self.GetModel().FindEntitiesByType("Machine")
    ]


@register_into_simulatorinterface
@property
def _decision_variables(self):
    if self.FindAttribute("{Model}Model::{Attribute}AllowPartRetention").GetAsBool():
        entities_by_name = self.get_entities_by_name()
        (_, pair_to_sto) = self.get_stocks_to_operations_pairs()
        stock_list_sto = dict()
        for pair, sto in pair_to_sto.items():
            stock_list_sto.setdefault(pair[0], []).append(sto.GetName())
        for stock, stos in stock_list_sto.items():
            stock_groups = set()
            for sto_name in stos:
                sto = entities_by_name[sto_name]
                groups = CosmoEngine.DataTypeMapInterface_Cast(sto.GetAttribute("Groups"))
                name = sto.GetName()
                for k in map(str, groups.GetKeys()):
                    yield (
                        "StockToOperation",
                        name,
                        None,
                        "PropStockForOperation",
                        groups.GetAttribute(k).GetAttributeAsString("StartCycle"),
                        groups.GetAttribute(k).GetAttributeAsString("EndCycle"),
                        k
                    )
                    stock_groups.add((k, groups.GetAttribute(k).GetAttributeAsString("StartCycle"), groups.GetAttribute(k).GetAttributeAsString("EndCycle")))
            for key, start_cycle, end_cycle in stock_groups:
                yield (
                    "Stock",
                    stock,
                    None,
                    None,
                    start_cycle,
                    end_cycle,
                    key
                )
    else:
        for sto in self.GetModel().FindEntitiesByType("StockToOperation"):
            groups = CosmoEngine.DataTypeMapInterface_Cast(sto.GetAttribute("Groups"))
            name = sto.GetName()
            for k in map(str, groups.GetKeys()):
                yield (
                    "StockToOperation",
                    name,
                    None,
                    "PropStockForOperation",
                    groups.GetAttribute(k).GetAttributeAsString("StartCycle"),
                    groups.GetAttribute(k).GetAttributeAsString("EndCycle"),
                    k
                )
    for machine in self.GetModel().FindEntitiesByType("Machine"):
        groups = CosmoEngine.DataTypeMapInterface_Cast(machine.GetAttribute("Groups"))
        for operation in CosmoEngine.CompoundEntity_Cast(machine).FindEntitiesByType("Operation"):
            name = machine.GetName()
            op_name = operation.GetName()
            for k in map(str, groups.GetKeys()):
                yield (
                    "Machine",
                    name,
                    op_name,
                    "StockTypeProportions",
                    groups.GetAttribute(k).GetAttributeAsString("StartCycle"),
                    groups.GetAttribute(k).GetAttributeAsString("EndCycle"),
                    k
                )


@register_into_simulatorinterface
@property
def decision_variables_df(self):
    df = pandas.DataFrame(
        self._decision_variables,
        columns=[
            "Type",
            "Entity",
            "Operation",
            "Attribute",
            "StartCycle",
            "EndCycle",
            "Group",
        ]
    )
    df["StartCycle"] = df["StartCycle"].astype(int)
    df["EndCycle"] = df["EndCycle"].astype(int)
    df["Group"] = df["Group"].astype(int)
    return df


@register_into_simulatorinterface
@property
def _constraints(self):
    for stock in self.GetModel().FindEntitiesByType("Stock"):
        demand = CosmoEngine.DataTypeMapInterface_Cast(stock.GetAttribute("Demand"))
        for k in map(str, demand.GetKeys()):
            yield (
                stock.GetName(),
                demand.GetAttribute(k).GetAttributeAsString("ExternalDemand"),
                demand.GetAttribute(k).GetAttributeAsString("InternalDemand"),
                k,
                demand.GetAttribute(k).GetAttributeAsString("ExternalWeight"),
                demand.GetAttribute(k).GetAttributeAsString("InternalWeight"),
                demand.GetAttribute(k).GetAttributeAsString("WeightMax"),
                demand.GetAttribute(k).GetAttributeAsString("BacklogWeight"),
                demand.GetAttribute(k).GetAttributeAsString("MaxVal")
            )


@register_into_simulatorinterface
@property
def constraints_df(self):
    return pandas.DataFrame(self._constraints, columns=[
        "name",
        "demand_extern",
        "demand_intern",
        "cycle",
        "weight_extern",
        "weight_intern",
        "weighto",
        "max_val",
        "weight_backlog",
    ])


setattr(CosmoEngine.SimulatorInterface, '_model_parameters', None)


@register_into_simulatorinterface
def get_model_parameters(self, force=False):
    if force or self._model_parameters is None:
        model = self.GetModel()
        parameters = model.GetParameters()
        self._model_parameters = {
            parameter: (
                parameters.GetAttribute(parameter).Get()
                if parameter_type not in ('Duration', 'DateTime')
                else parameters.GetAttribute(parameter).GetAsString()
            )
            for parameter, parameter_type in model.GetParametersDefinition()
        }
    return self._model_parameters


setattr(CosmoEngine.SimulatorInterface, '_number_of_time_steps', None)


@register_into_simulatorinterface
def get_number_of_time_steps(self, force=False):
    if force or self._number_of_time_steps is None:
        model_parameters = self.get_model_parameters(force=force)
        self._number_of_time_steps = model_parameters['TimeStepPerCycle'] * model_parameters['NumberOfCycle']
    return self._number_of_time_steps


setattr(CosmoEngine.SimulatorInterface, '_entities_by_name', None)


@register_into_simulatorinterface
def get_entities_by_name(self, force=False):
    if force or self._entities_by_name is None:
        self._entities_by_name = {
            entity.GetName(): entity
            for entity in self.GetModel().GetSubEntities()
        }
    return self._entities_by_name


setattr(CosmoEngine.SimulatorInterface, '_entities_by_type', None)


@register_into_simulatorinterface
def get_entities_by_type(self, entity_type=None, force=False):
    if force or self._entities_by_type is None:
        model = self.GetModel()
        self._entities_by_type = {
            entity_type: []
            for entity_type in model.GetEntityTypeList()
        }
        for entity in model.GetSubEntities():
            self._entities_by_type[entity.GetTypeName()].append(entity)
    return (
        self._entities_by_type
        if entity_type is None
        else self._entities_by_type[entity_type]
    )


@register_into_simulatorinterface
def get_typed_entities_by_name(self, entity_type, force=False):
    return {
        entity.GetName(): entity
        for entity in self.get_entities_by_type(entity_type=entity_type, force=force)
    }


setattr(CosmoEngine.SimulatorInterface, '_entities_names_by_type', None)


@register_into_simulatorinterface
def get_entities_names_by_type(self, entity_type=None, force=False):
    if force or self._entities_names_by_type is None:
        self._entities_names_by_type = {
            entities_type: {
                entity.GetName()
                for entity in entities
            }
            for entities_type, entities in self.get_entities_by_type(force=force).items()
        }
    return (
        self._entities_names_by_type
        if entity_type is None
        else self._entities_names_by_type[entity_type]
    )


setattr(CosmoEngine.SimulatorInterface, '_pairs_by_stock_to_operation', None)
setattr(CosmoEngine.SimulatorInterface, '_stocks_to_operations_by_pair', None)


@register_into_simulatorinterface
def get_stocks_to_operations_pairs(self, force=False):
    if force or self._pairs_by_stock_to_operation is None or self._stocks_to_operations_by_pair is None:
        self._pairs_by_stock_to_operation = {}
        self._stocks_to_operations_by_pair = {}
        for stock_to_operation in self.get_entities_by_type('StockToOperation', force=force):
            edge = CosmoEngine.Edge_Cast(stock_to_operation)
            stock = edge.GetLeft()
            operation = edge.GetRight()
            self._pairs_by_stock_to_operation[stock_to_operation.GetName()] = (stock, operation)
            self._stocks_to_operations_by_pair[(stock.GetName(), operation.GetName())] = stock_to_operation
    return self._pairs_by_stock_to_operation, self._stocks_to_operations_by_pair


setattr(CosmoEngine.SimulatorInterface, '_entities_neighbors_by_type', None)


@register_into_simulatorinterface
def get_entities_neighbors_by_type(self, entity_type=None, force=False):
    if force or self._entities_neighbors_by_type is None:
        industrial_network, = self.get_entities_by_type('IndustrialNetwork', force=force)
        environment = self.GetModel().GetCompoundEntity(industrial_network.GetId()).GetEnvironment()
        self._entities_neighbors_by_type = {
            entities_type: {}
            for entities_type in ('Stock', 'Operation', 'TransportOperation')
        }
        for entities_type, typed_entities_neighbors in self._entities_neighbors_by_type.items():
            for entity in self.get_entities_by_type(entities_type, force=force):
                if not environment.GetNeighborsCount(entity):
                    continue
                entity_neighbors = typed_entities_neighbors.setdefault(entity.GetName(), {})
                for neighbor in environment.GetNeighbors(entity):
                    entity_neighbors.setdefault(neighbor.GetTypeName(), set()).add(neighbor.GetName())
    return (
        self._entities_neighbors_by_type
        if entity_type is None
        else self._entities_neighbors_by_type[entity_type]
    )


setattr(CosmoEngine.SimulatorInterface, '_stocks_by_operation', None)


@register_into_simulatorinterface
def get_stocks_by_operation(self, force=False):
    if force or self._stocks_by_operation is None:
        self._stocks_by_operation = {}
        entities_neighbors_by_type = self.get_entities_neighbors_by_type(force=force)
        stocks_neighbors = entities_neighbors_by_type['Stock']
        operations_neighbors = entities_neighbors_by_type['Operation'].copy()
        operations_neighbors.update(entities_neighbors_by_type['TransportOperation'])
        for operation_name, operation_neighbors in operations_neighbors.items():
            input_stocks = operation_neighbors['Stock']
            output_stocks = set(
                stock_name
                for stock_name, stock_neighbors in stocks_neighbors.items()
                if any(
                    neighbor_operation_name == operation_name
                    for entity_type in ('Operation', 'TransportOperation')
                    for neighbor_operation_name in stock_neighbors.get(entity_type, set())
                )
            )
            output_stocks -= input_stocks
            self._stocks_by_operation[operation_name] = (input_stocks, output_stocks)
    return self._stocks_by_operation


setattr(CosmoEngine.SimulatorInterface, '_typed_operations_by_output_stock', None)


@register_into_simulatorinterface
def get_typed_operations_by_output_stock(self, force=False):
    if force or self._typed_operations_by_output_stock is None:
        entities_neighbors_by_type = self.get_entities_neighbors_by_type(force=force)
        stocks_neighbors = {
            stock_name: stock_neighbors.get('Operation', set()) | stock_neighbors.get('TransportOperation', set())
            for stock_name, stock_neighbors in entities_neighbors_by_type['Stock'].items()
        }
        operations_neighbors = entities_neighbors_by_type['Operation'].copy()
        operations_neighbors.update(entities_neighbors_by_type['TransportOperation'])
        input_stocks_by_operation = {
            operation_name: operation_neighbors['Stock']
            for operation_name, operation_neighbors in operations_neighbors.items()
        }
        self._typed_operations_by_output_stock = {}
        entities_by_name = self.get_entities_by_name(force=force)
        for stock_name, stock_neighbors in stocks_neighbors.items():
            upstream_operations_names = [
                operation_name
                for operation_name in stock_neighbors
                if stock_name not in input_stocks_by_operation[operation_name]
            ]
            if upstream_operations_names:
                output_stock_typed_operations = self._typed_operations_by_output_stock.setdefault(stock_name, {})
                for operation_name in upstream_operations_names:
                    output_stock_typed_operations.setdefault(entities_by_name[operation_name].GetTypeName(), set()).add(operation_name)
    return self._typed_operations_by_output_stock


setattr(CosmoEngine.SimulatorInterface, '_transports_by_stocks', None)


@register_into_simulatorinterface
def get_transports_by_stocks(self, force=False):
    if force or self._transports_by_stocks is None:
        self._transports_by_stocks = {}
        entities_by_name = self.get_entities_by_name(force=force)
        stocks_neighbors = self.get_entities_neighbors_by_type('Stock', force=force)
        for transport_name, transport_neighbors in self.get_entities_neighbors_by_type('TransportOperation', force=force).items():
            input_stock_name, = transport_neighbors['Stock']
            for output_stock_name, output_stock_neighbors in stocks_neighbors.items():
                if output_stock_name != input_stock_name and transport_name in output_stock_neighbors.get('TransportOperation', set()):
                    break
            self._transports_by_stocks[input_stock_name, output_stock_name] = entities_by_name[transport_name]
    return self._transports_by_stocks


setattr(CosmoEngine.SimulatorInterface, '_machines_by_operation', None)


@register_into_simulatorinterface
def get_machines_by_operation(self, force=False):
    if force or self._machines_by_operation is None:
        self._machines_by_operation = {
            operation.GetName(): machine
            for machine in self.get_entities_by_type('Machine', force=force)
            for operation in self.GetModel().GetCompoundEntity(machine.GetId()).GetSubEntities()
        }
    return self._machines_by_operation


setattr(CosmoEngine.SimulatorInterface, '_operations_by_machine', None)


@register_into_simulatorinterface
def get_operations_by_machine(self, force=False):
    if force or self._operations_by_machine is None:
        self._operations_by_machine = {
            machine.GetName(): [operation for operation in self.GetModel().GetCompoundEntity(machine.GetId()).GetSubEntities()]
            for machine in self.get_entities_by_type('Machine', force=force)
        }
    return self._operations_by_machine


@register_into_simulatorinterface
def get_scheduled_values(self, entity, schedulable_parameter_name, force=False):
    number_of_time_steps = self.get_number_of_time_steps(force=force)
    default_value = entity.GetAttribute(schedulable_parameter_name).Get()
    scheduled_values = [default_value] * number_of_time_steps
    changes = CosmoEngine.DataTypeMapInterface_Cast(entity.GetAttribute(f'{schedulable_parameter_name}Schedule')).Get()
    if changes:
        time_steps = sorted(time_step for time_step in changes)
        next_time_steps = [*time_steps[1:], number_of_time_steps]
        for t1, t2 in zip(time_steps, next_time_steps):
            scheduled_values[t1:t2] = [changes[t1]] * (t2 - t1)
    return scheduled_values


setattr(CosmoEngine.SimulatorInterface, '_schedulable_parameters_names', None)


@register_into_simulatorinterface
def get_schedulable_parameters_names(self, force=False):
    if force or self._schedulable_parameters_names is None:
        self._schedulable_parameters_names = {}
        suffix = 'Schedule'
        suffix_length = len(suffix)
        for entity_type, entities in self.get_entities_by_type(force=force).items():
            entity = entities[0]
            attributes_names = set(attribute_name for attribute_name, _ in entity.GetStateDefinition())
            entity_schedulable_parameters = [
                schedulable_parameter_name
                for schedulable_parameter_name in (
                    attribute_name[:-suffix_length]
                    for attribute_name in attributes_names
                    if attribute_name.endswith(suffix)
                )
                if schedulable_parameter_name in attributes_names
            ]
            if entity_schedulable_parameters:
                self._schedulable_parameters_names[entity_type] = entity_schedulable_parameters
    return self._schedulable_parameters_names


Demand = namedtuple('Demand', ['stock', 'time_step', 'external_demand', 'internal_demand', 'maximum_quantity', 'external_weight', 'internal_weight', 'backlog_weight', 'maximization_weight'])


@register_into_simulatorinterface
def get_demands(self, force=False):
    for stock in self.get_entities_by_type('Stock', force=force):
        demands = CosmoEngine.DataTypeMapInterface_Cast(stock.GetAttribute("Demand"))
        stock_name = stock.GetName()
        for time_step in demands.GetKeys():
            demand = demands.GetAt(time_step)
            yield Demand(
                stock_name,
                time_step.Get(),
                demand.GetAttribute("ExternalDemand").Get(),
                demand.GetAttribute("InternalDemand").Get(),
                demand.GetAttribute("MaxVal").Get(),
                demand.GetAttribute("ExternalWeight").Get(),
                demand.GetAttribute("InternalWeight").Get(),
                demand.GetAttribute("BacklogWeight").Get(),
                demand.GetAttribute("WeightMax").Get(),
            )
