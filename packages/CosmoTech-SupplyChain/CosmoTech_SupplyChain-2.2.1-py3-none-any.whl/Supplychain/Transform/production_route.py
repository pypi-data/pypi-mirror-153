from csm.engine import SimulatorInterface
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
import pandas as pd


def send_production_route_data(writer: ADXAndFileWriter,
                               simulation_id: str,
                               simulator: SimulatorInterface):
    df = get_sorted_production_resource(simulator)
    df['SimulationRun'] = simulation_id
    dict_list = df.to_dict('records')
    writer.write_target_file(dict_list, 'ProductionRoute', simulation_id)


def get_operations_for_stocks(output_op, op_input, stocks):
    operations = set()
    
    for stock in stocks:
        if output_op.get(stock):
            operations.update(output_op.get(stock).get('Operation', {}))            
            transports = output_op.get(stock).get('TransportOperation', {})
            
            # Transports are ignored in the production route
            # If there are transports for the stocks, we will recursively research the previous operations
            if transports:
                previous_stocks = get_stocks_for_operations(op_input, transports)
                previous_operations = get_operations_for_stocks(output_op, op_input, previous_stocks)
                operations.update(previous_operations)
                
    return operations


def get_stocks_for_operations(op_input, operations):
    stocks = set()
    for operation in operations:
        stock = op_input.get(operation)
        if stock:
            stocks.update(set(stock[0]))
    return stocks


def get_machines_for_operations(op_machines, operations):
    machines = {}
    for op in operations:
        machine = op_machines.get(op)
        if machine:
            machines[op] = machine.GetName()
    return machines


def get_sorted_production_resource(simulator):
    # Return sorted Production Resource by Production Step Order by Stock
    stocks = [stock.GetName() for stock in simulator.get_entities_by_type('Stock')]
    op_input = simulator.get_stocks_by_operation()
    output_op = simulator.get_typed_operations_by_output_stock()
    op_machines = simulator.get_machines_by_operation()
    record = []

    for stock in stocks:
        operations = get_operations_for_stocks(output_op, op_input, [stock])
        machines_by_step = []

        while operations:
            machines = get_machines_for_operations(op_machines, operations)
            if machines:
                machines_by_step.append(machines)
            previous_input_stocks = get_stocks_for_operations(op_input, operations)
            previous_operations = get_operations_for_stocks(output_op, op_input, previous_input_stocks)
            operations = previous_operations

        machines_by_step.reverse()

        for i in range(len(machines_by_step)):
            for op, machine in machines_by_step[i].items():
                record.append({'ProductionStepOrder': i + 1, 'ProductionOperationId': op,
                               'ProductionResourceId': machine, 'StockId': stock})

        df = pd.DataFrame(record)
    return df
