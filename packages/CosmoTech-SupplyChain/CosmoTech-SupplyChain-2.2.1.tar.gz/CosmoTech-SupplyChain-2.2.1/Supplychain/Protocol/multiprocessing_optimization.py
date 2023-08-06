from Supplychain.Protocol.protocol import AbstractOptimization
from Supplychain.Protocol.protocol import AbstractOptimizationAlgorithm
from Supplychain.Protocol.protocol import AbstractObjectiveFunction
from Supplychain.Protocol.protocol import AbstractParameterTransformation
from Supplychain.Generic.timer import Timer
from Supplychain.Wrappers.simulator import CosmoEngine

import multiprocessing
import numpy as np
from typing import Union


class MultiprocessingOptimization(AbstractOptimization, Timer):

    def __init__(self,
                 optimization_algorithm: AbstractOptimizationAlgorithm,
                 objective_function: AbstractObjectiveFunction,
                 parameter_transformation: AbstractParameterTransformation,
                 simulation_name: str,
                 population_size: int,
                 amqp_consumer_adress: Union[str, None] = None):
        Timer.__init__(self, "[MultiprocessingOptimization]")
        AbstractOptimization.__init__(self,
                                      optimization_algorithm,
                                      objective_function,
                                      parameter_transformation,
                                      None)
        self.use_amqp = amqp_consumer_adress is not None
        self.amqp_consumer_adress = amqp_consumer_adress

        self.simulation_name = simulation_name
        self.population_size = population_size

    def run_simulation(self,
                       dv_input: dict):
        # Remove logs other than errors for the simulator
        _logger = CosmoEngine.LoggerManager_GetInstance().GetLogger()
        _logger.SetLogLevel(_logger.eAssertion)
        _simulator = CosmoEngine.LoadSimulator('Simulation')

        # Applies the modification to the simulator
        for datapath, stringvalue in dv_input.items():
            _simulator.FindAttribute(datapath).SetAsString(stringvalue)

        # Add a random seed in case uncertainties are activated
        _simulator.FindAttribute("{Model}Model::{Attribute}Seed").SetAsString(
            str(int(np.random.randint(np.iinfo(np.int32).max)))
        )

        # Destroy all old consumers
        for consumer in _simulator.GetConsumers():
            _simulator.DestroyConsumer(consumer)

        # Define a custom consumer for the optimization
        class PerformanceConsumer(CosmoEngine.Consumer):
            data = list()

            def Consume(self, p_data):
                f = CosmoEngine.PerformanceIndicatorsProbeOutput.Cast(p_data).GetFacts()
                for fact in f:
                    self.data.append({
                        "Profit": fact.GetProfit().GetAsFloat(),
                        "ServiceLevelIndicator": fact.GetServiceLevelIndicator().GetAsFloat()
                    })

        # Instantiate and link the new consumer to the model
        local_consumer = PerformanceConsumer()
        local_consumer.SetName("PerformanceConsumer")
        local_consumer.AddProbe("PerformanceIndicators")
        _simulator.AddConsumer(local_consumer)

        # Run the simulation
        _simulator.Run()

        # return the objective value
        return self.obj_func.applies(local_consumer.data)

    def optimize_parameters(self,
                            is_uncertainty_analysis=False):

        # During initial tests SLO found that forkserver was a viable solution for a multiprocess optim environment
        multiprocessing.set_start_method('forkserver')

        # Define a pool of processes
        self.display_message("Starting Optimization")
        with multiprocessing.Pool(self.population_size) as p:
            # Run the optim algorithm until it has the wanted results
            while self.opt_algo.is_not_finished():
                # Define a list of parameters to be send to the simulation
                parameters = self.opt_algo.generate_decision_variables()
                _params = [(self.par_tran.applies(x.tolist(), 0),)
                           for x in parameters]
                # Run the multiple simulations in the processes pool
                results = p.starmap(self.run_simulation, _params)
                # Update the algorithm
                self.opt_algo.update_algorithm(parameters, results)
        self.display_message("Optimization finished in {time_since_start}")
