import numpy
import random
import multiprocessing
from typing import Union
from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
import pandas as pd
from Supplychain.Generic.timer import Timer
from math import sqrt
from Supplychain.Wrappers.environment_variables import EnvironmentVariables
from Supplychain.Run.simulation import run_simple_simulation


def run_simulation_with_seed(simulation_name: str,
                             seed: int,
                             amqp_consumer_adress: Union[str, None] = None,
                             output_list=None) -> bool:
    # Reduce log level to Error during optimization
    logger = CosmoEngine.LoggerManager_GetInstance().GetLogger()
    logger.SetLogLevel(logger.eAssertion)
    simulator = CosmoEngine.LoadSimulator('Simulation')

    simulator.FindAttribute("{Model}Model::{Attribute}Seed").SetAsString(
        str(seed)
    )

    used_probes = ['PerformanceIndicators', 'Stocks']
    used_consumers = ['CSVPerformanceIndicatorsConsumer', 'CSVStocksConsumer']

    # Delete all probes expect for the one we use
    for probe in simulator.GetProbes():
        if probe.GetType() not in used_probes:
            simulator.DestroyProbe(probe)

    if amqp_consumer_adress is not None:
        # Instantiate consumers using AMQP to send data to the cloud service
        simulator.InstantiateAMQPConsumers(simulation_name, amqp_consumer_adress)

        used_consumers = ['PerformanceIndicatorsAMQP']

    # Remove unused consumers
    for consumer in simulator.GetConsumers():
        if consumer.GetName() not in used_consumers:
            simulator.DestroyConsumer(consumer)

    class StockConsumer(CosmoEngine.Consumer):
        memory = list()

        def Consume(self, p_data):
            probe_output = CosmoEngine.StocksProbeOutput.Cast(p_data)
            f = probe_output.GetFacts()
            timestep = int(probe_output.GetProbeRunDimension().GetProbeOutputCounter())
            for data in f:
                fact = [str(data.GetAttributeAsString('ID')),
                        timestep,
                        float(data.GetAttributeAsFloat64('Demand')),
                        float(data.GetAttributeAsFloat64('RemainingQuantity')),
                        float(data.GetAttributeAsFloat64('ServedQuantity')),
                        float(data.GetAttributeAsFloat64('UnservedQuantity'))]
                self.memory.append(fact)

    consumer = StockConsumer("LocalConsumer")
    consumer.Connect(simulator.GetProbe("Stocks"))

    # Run simulation
    simulator.Run()

    if output_list is not None:
        output_list.extend(StockConsumer.memory)

    # Remove all the consumers in case that amqp consumers are still connected to ADX
    for consumer in simulator.GetConsumers():
        simulator.DestroyConsumer(consumer)

    return simulator.IsFinished()


def uncertainty_analysis(simulation_name: str,
                         amqp_consumer_adress: Union[str, None] = None,
                         sample_size: int = 1000,
                         batch_size: int = 100,
                         adx_writer: Union[ADXAndFileWriter, None] = None):
    with Timer('[Run Uncertainty]') as t:
        if batch_size > sample_size:
            batch_size = sample_size

        maxint = numpy.iinfo(numpy.int32).max
        seedlist = random.sample(range(maxint), sample_size)
        processes_size = min(multiprocessing.cpu_count(), batch_size)
        manager = multiprocessing.Manager()
        probe_data = manager.list()
        t.display_message("Starting simulations")
        with multiprocessing.Pool(processes_size) as p:
            for i in range(0, len(seedlist), batch_size):
                subseedlist = seedlist[i:i + batch_size]
                params = list(map(lambda seed: (simulation_name, seed, amqp_consumer_adress, probe_data), subseedlist))
                p.starmap(run_simulation_with_seed, params)
        t.split("Ended simulations : {time_since_start}")

        df = pd.DataFrame((l for l in probe_data))
        df.columns = ['StockId', 'TimeStep', 'Demand', 'RemainingQuantity', 'ServedQuantity', 'UnservedQuantity']
        t.split("Create dataframes for stats computation: {time_since_last_split}")

        quantile_list = [0.05, 0.25, 0.5, 0.75, 0.95]
        groups = df.groupby(['StockId', 'TimeStep'])
        df_quantiles = groups.quantile(quantile_list)
        df_average = groups.mean()
        df_error = groups.agg(lambda x: x.std() / sqrt(x.count()))
        t.split("Compute stats : {time_since_last_split}")

        # since use of pivot to have 1 column per tuple (quantile, valuetype)
        # then use of stack to have 1 line per (stock, timestep, valuetype)
        df3 = df_quantiles.reset_index().pivot(index=['StockId',
                                                      'TimeStep'],
                                               columns='level_2',
                                               values=['Demand',
                                                       'RemainingQuantity',
                                                       'ServedQuantity',
                                                       'UnservedQuantity']).stack(level=0)
        df3.reset_index(inplace=True)
        df3.columns = ['StockId',
                       'TimeStep',
                       'Category'] + [f'Percentile{int(v * 100)}'
                                      for v in quantile_list]

        # use of stack to have 1 line per (stock, timestep, valuetype)
        df4 = df_average.stack(level=0)
        df4 = df4.reset_index()
        df4.columns = ['StockId',
                       'TimeStep',
                       'Category',
                       'Mean']

        # use of stack to have 1 line per (stock, timestep, valuetype)
        df5 = df_error.stack(level=0)
        df5 = df5.reset_index()
        df5.columns = ['StockId',
                       'TimeStep',
                       'Category',
                       'SE']

        # Merge of dfs to final df
        final_df = pd.merge(df3, df4, on=['StockId',
                                          'TimeStep',
                                          'Category'])
        final_df = pd.merge(final_df, df5, on=['StockId',
                                               'TimeStep',
                                               'Category'])

        final_df['SimulationRun'] = EnvironmentVariables.simulation_id
        final_df = final_df[['TimeStep',
                             'SimulationRun',
                             'StockId',
                             'Percentile5',
                             'Percentile25',
                             'Percentile50',
                             'Percentile75',
                             'Percentile95',
                             'Mean',
                             'SE',
                             'Category']]
        adx_writer.write_target_file(final_df.to_dict('records'), 'StockUncertaintiesStatistics', EnvironmentVariables.simulation_id)

        t.split("Sent stats to ADX : {time_since_last_split}")
        t.display_message("Running simple simulation to fill ADX")
        # Put back log level to Info for final simulation
        # Reduce log level to Error during optimization
        logger = CosmoEngine.LoggerManager_GetInstance().GetLogger()
        logger.SetLogLevel(logger.eInfo)

        stop_uncertainty = {
            "Model::@ActivateUncertainties": "false"
        }

        run_simple_simulation(simulation_name=simulation_name,
                              amqp_consumer_adress=amqp_consumer_adress,
                              modifications=stop_uncertainty)
