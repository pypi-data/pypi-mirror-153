from Supplychain.Generic.folder_io import FolderReader
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.validation_schemas import ValidationSchemas
from Supplychain.Schema.default_values import parameters_default_values

from collections import Counter

import itertools
import jsonschema


class DictValidator(Timer):

    def __init__(self,
                 reader: FolderReader,
                 run_type: str = "None"):
        Timer.__init__(self, prefix="[Validation]")

        self.reader = reader

        self.schema = ValidationSchemas()

        self.run_type = run_type

        self.errors = []

        self.lookup_memory = dict()

    def validate(self) -> bool:
        checks = [self.validate_files(), self.validate_graph(), self.specific_validations()]
        if all(checks):
            self.display_message("Dataset is valid")
            return True
        else:
            self.display_message("Dataset is invalid")
            return False

    def validate_graph(self) -> bool:
        self.errors = []
        self.display_message("Validate graph")
        for file_to_validate in sorted(self.schema.graph.keys()):
            self.__validate_graph(file_to_validate)
        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
            return False
        self.__validate_acyclicity()
        if self.errors:
            self.display_message("1 error found in the files")
            self.display_message(self.errors[0])
            return False
        self.display_message("Graph is valid")
        return True

    def validate_files(self) -> bool:
        self.errors = []
        self.display_message("Validate file content")
        for file_to_validate in sorted(self.schema.schemas.keys()):
            self.__validate_file(file_to_validate)

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                message = err.message.replace("{", "{{").replace("}", "}}")
                self.display_message(f" - {filename}: {item_id}: {'/'.join(err.path)}: {message}")
        else:
            self.display_message("Individual files are valid")
            return True
        return False

    def __validate_file(self, file_name: str):
        for item in self.reader.files[file_name]:
            validator = jsonschema.Draft7Validator(schema=self.schema.schemas[file_name])
            errors = validator.iter_errors(item)
            item_id = item['id'] if 'id' in item else item.get("Label",
                                                               None)  # TODO specific for relationship here transport (only Transport relationship is validated) to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
            if item_id is None:
                item_id = item.get('source', "") + " -> " + item.get('target', "")
            for error in errors:
                self.errors.append((file_name, item_id, error))
        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_graph(self, file_name: str):
        config = self.schema.graph[file_name]
        source = config['source']
        target = config['target']
        source_file, source_id = config['links']['source']
        target_file, target_id = config['links']['target']
        cardinality_target, cardinality_source = config['cardinalities'].split(':')
        all_target = config['all_target_present']
        all_source = config['all_source_present']

        source_file_ids = [i[source_id] for i in self.reader.files[source_file]]
        target_file_ids = [i[target_id] for i in self.reader.files[target_file]]

        arcs = [(i[source], i[target]) for i in self.reader.files[file_name]]
        if arcs:
            sources, targets = zip(*arcs)

            # Check required existences
            for check, file_ids, ids in [(all_source, source_file_ids, sources),
                                         (all_target, target_file_ids, targets)]:
                if check:
                    for item_id in file_ids:
                        if item_id not in ids:
                            self.errors.append((file_name, item_id, "has no relations"))

            for file_ids, ids, current_file in [(source_file_ids, sources, source_file),
                                                (target_file_ids, targets, target_file)]:
                for item_id in ids:
                    if item_id not in file_ids:
                        self.errors.append((file_name, item_id, f"does not exist in {current_file}"))

            # Check cardinalities
            for entities, cardinality in [(sources, cardinality_source), (targets, cardinality_target)]:
                for e in set(entities):
                    if cardinality == "1" and entities.count(e) > 1:
                        self.errors.append((file_name, e, "has more than one relation"))

        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_acyclicity(self):
        arcs_by_file_name = {
            file_name: [
                (i[config['source']], i[config['target']])
                for i in self.reader.files[file_name]
            ]
            for file_name, config in self.schema.graph.items()
        }
        arcs = [
            arc
            for arcs_of_file in arcs_by_file_name.values()
            for arc in arcs_of_file
        ]
        if arcs:
            vertices = set(itertools.chain(*arcs))
            targets_by_source = {
                vertex: set()
                for vertex in vertices
            }
            for source, target in arcs:
                targets_by_source[source].add(target)
            visited = set()
            loop = []

            def visit(vertex):
                if vertex in visited:
                    return False
                if vertex in loop:
                    loop.append(vertex)
                    return True
                vertices.discard(vertex)
                loop.append(vertex)
                for next_vertex in targets_by_source[vertex]:
                    if visit(next_vertex):
                        return True
                visited.add(loop.pop())

            while vertices:
                if visit(vertices.pop()):
                    break
            if loop:
                loop = loop[loop.index(loop[-1]):]
                vertex_types = []
                file_names = []
                for arc in zip(loop[:-1], loop[1:]):
                    for file_name, arcs_of_file in arcs_by_file_name.items():
                        if arc in arcs_of_file:
                            break
                    vertex_types.append(self.schema.graph[file_name]['links']['source'][0])
                    file_names.append(file_name)
                spacing = max(
                    max(map(len, vertex_types)),
                    max(map(len, file_names)) - 2,
                )
                vertex_types.append(vertex_types[0])
                sep = '\n\t'
                relations = [sep] + [
                    f'{file_name:>{spacing + 2}} ↓{sep}'
                    for file_name in file_names
                ]
                loop_links = [
                    f"{relation}[{vertex_type:^{spacing}}] {vertex}"
                    for relation, vertex_type, vertex in zip(relations, vertex_types, loop)
                ]
                self.errors.append(f"The graph contains at least one loop:{sep.join(loop_links)} (same as first)")

    def specific_validations(self) -> bool:
        # If specific validations are required add them here
        self.errors = []
        self.display_message("Specific validations")

        self.__transports_specific_checks()
        self.split("\ttransports_specific_checks: {time_since_last_split:6.4f}s")
        for filename, id_column in [('Transport', 'Label'),  # TODO replace by
                                    ('ProductionOperation', 'id'),
                                    ('ProductionResource', 'id'),
                                    ('Stock', 'id')]:
            self.__unique_id_validation(filename, id_column)
        self.split("\tunique_id_validation: {time_since_last_split:6.4f}s")

        if self.run_type != "Simulation":
            self.__part_retention_validation()
            self.split("\tpart_retention_validation: {time_since_last_split:6.4f}s")

        self.__no_infinite_stocks_to_transport()
        self.split("\tno_infinite_stocks_to_transport: {time_since_last_split:6.4f}s")

        self.__obsolescence_check()
        self.split("\tobsolescence_check: {time_since_last_split:6.4f}s")

        self.__check_resource_dependencies()
        self.split("\tcheck_resource_dependencies: {time_since_last_split:6.4f}s")

        self.__mandatory_attributes_check()
        self.split("\tmandatory_attributes_check: {time_since_last_split:6.4f}s")

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
        else:
            self.display_message("Specific checks are valid")
            return True
        return False

    def __part_retention_validation(self):
        stocks = self.reader.files['Stock']
        transports = self.reader.files['Transport']
        outputs = self.reader.files['input']
        isdp = None
        if self.reader.files['Configuration']:
            isdp = self.reader.files['Configuration'][0].get('IntermediaryStockDispatchPolicy')
        if isdp is None:
            isdp = parameters_default_values['Configuration']['IntermediaryStockDispatchPolicy']
        if isdp == 'DispatchAll':
            non_final_stocks = set()
            for t in transports:
                non_final_stocks.add(t['source'])
            for o in outputs:
                non_final_stocks.add(o['source'])
            for stock in stocks:
                if stock['id'] not in non_final_stocks:
                    continue
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                if any(stock_demands.values()):
                    self.errors.append(("Stock",
                                        stock['id'],
                                        "has demands and is not a final stock,"
                                        " set IntermediaryStockDispatchPolicy to AllowRetention"))

    def __unique_id_validation(self, filename: str, id_column: str):
        _file = self.reader.files[filename]

        _ids = Counter(item[id_column] for item in _file)

        for _id, count in _ids.items():
            if count > 1:
                self.errors.append((filename,
                                    _id,
                                    f"{id_column} is not unique, found {count} times"))

    def __transports_specific_checks(self):
        transports = self.reader.files['Transport']
        for transport in transports:
            duration = transport.get('Duration')
            if 'InitialTransportQuantities' in transport:
                if duration is not None:
                    key_errors = [k for k in transport['InitialTransportedQuantities'] if int(k) >= duration]
                    for k in key_errors:
                        self.errors.append(("Transports",
                                            transport.get('Label'),
                                            f"InitialTransportedQuantities: key {k} >= {duration}"))
            if 'InitialTransportValues' in transport:
                if duration is not None:
                    key_errors = [k for k in transport['InitialTransportedValues'] if int(k) >= duration]
                    for k in key_errors:
                        self.errors.append(("Transports",
                                            transport.get('Label'),
                                            f"InitialTransportedValues: key {k} >= {duration}"))
                key_errors = [k
                              for k in transport['InitialTransportedValues']
                              if k not in transport['InitialTransportedQuantities']]
                for k in key_errors:
                    self.errors.append(("Transports",
                                        transport.get('Label'),
                                        f"InitialTransportedValues: key {k} has no quantities associated"))

    def __no_infinite_stocks_to_transport(self):
        transports = self.reader.files['Transport']
        stocks = self.reader.files['Stock']

        infinite_stocks = [stock['id'] for stock in stocks if stock.get('IsInfinite')]

        transports_from_infinite_stocks = [transport
                                           for transport in transports
                                           if transport['source'] in infinite_stocks]

        for transport in transports_from_infinite_stocks:
            self.errors.append(("Stock",
                                transport.get('source'),
                                f"Is infinite and has outgoing transport: {transport.get('Label')}"))

    def __obsolescence_check(self):
        empty_obsolete_stocks = None
        if self.reader.files['Configuration']:
            empty_obsolete_stocks = self.reader.files['Configuration'][0].get('EmptyObsoleteStocks')
        if empty_obsolete_stocks is None:
            empty_obsolete_stocks = parameters_default_values['Configuration']['EmptyObsoleteStocks']
        if empty_obsolete_stocks:
            stocks = self.reader.files['Stock']
            for stock in stocks:
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                has_demands = any(stock_demands.values())
                stock_policy = stock.get('StockPolicy')
                if stock_policy is None:
                    stock_policy = parameters_default_values['Configuration']['StockPolicy']
                has_stock_policy = stock_policy != 'None'
                if has_demands and has_stock_policy:
                    self.errors.append(('Configuration',
                                        'EmptyObsoleteStocks',
                                        'The stock obsolescence option is not compatible with stock policies.'))
                    break


    def find_relations_by_id(self, relation_name: str, looked_id: str, relation_column: str):
        if (relation_name, looked_id, relation_column) not in self.lookup_memory:
            self.lookup_memory[(relation_name, looked_id, relation_column)] = [
                row
                for row in self.reader.files[relation_name]
                if row.get(relation_column) == looked_id
            ]
        return self.lookup_memory[(relation_name, looked_id, relation_column)]

    parent_operations_mem = dict()

    def __find_parent_operations(self, stock_id: str):
        if stock_id in self.parent_operations_mem:
            return self.parent_operations_mem[stock_id]

        _ret = []
        self.parent_operations_mem[stock_id] = _ret
        # transports won't increment the current level
        for _transport in self.find_relations_by_id('Transport', stock_id, 'target'):
            for operation in self.__find_parent_operations(_transport.get('source')):
                _ret.append(operation)

        for _output in self.find_relations_by_id('output', stock_id, 'target'):
            _operation_id = _output.get('source')
            _ret.append(_operation_id)
        return _ret


    def __check_resource_dependencies(self):
        # A resource should not have a "loop" dependency
        # It means if any operation in the resource is dependant on another operation in the same resource
        # the dataset validation should fail
        # A dependency is either a direct parent operation, or an operation in the same resource as a parent

        contains = self.reader.files['contains']

        direct_dependencies = dict()
        operations_per_resource = dict()
        resource_per_operation = dict()

        # fill dependencies
        for contain in contains:
            operation_id = contain.get('target')
            resource_id = contain.get('source')
            operations_per_resource.setdefault(resource_id, [])
            operations_per_resource[resource_id].append(operation_id)
            resource_per_operation[operation_id] = resource_id
            direct_dependencies.setdefault(operation_id, set())
            for _input in self.find_relations_by_id('input', operation_id, 'target'):
                direct_dependencies[operation_id].update(self.__find_parent_operations(_input.get('source')))

        for operations in operations_per_resource.values():
            dependencies = set()
            for operation_id in operations:
                dependencies.update(direct_dependencies[operation_id])
                direct_dependencies[operation_id] = dependencies

        full_dependencies = dict()

        def find_dependencies(operation_id: str):
            if operation_id in full_dependencies:
                return full_dependencies[operation_id]
            _ret = set()
            full_dependencies[operation_id] = _ret
            _dependencies = direct_dependencies.get(operation_id, set())
            for dependency in _dependencies:
                _ret.add(dependency)
                _ret.update(find_dependencies(dependency))
            return _ret

        for operation_id, resource_id in resource_per_operation.items():
            if operation_id in find_dependencies(operation_id):
                self.errors.append(('Graph',
                                    'Resource dependency',
                                    f'In resource {resource_id}, the operation {operation_id} requires itself'))
                return

    def __mandatory_attributes_check(self):
        demand = any(
            len(stock_demands.values())
            for stock in self.reader.files['Stock']
            for stock_demands in (stock.get('Demands'),)
            if stock_demands
        )
        if not demand:
            self.errors.append(('Stock',
                                'Demands',
                                'There is no demand.'))
        # for future warnings:
        """
        for resource in self.reader.files['ProductionResource']:
            if 'OpeningTimes' not in resource:
                self.display_message(f"Production resource {resource['id']} has no opening time.")
        for operation in self.reader.files['ProductionOperation']:
            if 'CycleTimes' not in operation:
                self.display_message(f"Production operation {operation['id']} has no opening time.")
        for transport in self.reader.files['Transport']:
            if 'Duration' not in transport:
                self.display_message(f"Transport {transport['Label']} has no duration.")
        """
