import csv
import numpy as np
from typing import Union

from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Protocol.cmaes_optimization_algorithm import CMAESOptimization
from Supplychain.Protocol.default_transformation import DefaultTransformation
from Supplychain.Protocol.multiprocessing_optimization import MultiprocessingOptimization
from Supplychain.Protocol.objective_functions import DefaultObjectiveFunction, ProfitMaximizationObjectiveFunction

from Supplychain.Generic.timer import Timer

import json


def get_optimization_objective(input_folder: str = "Input"):
    default_value = "ServiceLevelMaximization"
    with open(input_folder + "/Configuration.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            return line.get("OptimizationObjective", default_value)
    return default_value


def run_cmaes_optimization(simulation_name: str,
                           sigma0: float,
                           tol_x: float,
                           tol_fun: float,
                           max_f_evals: int,
                           pop_size: int,
                           amqp_consumer_adress: Union[str, None] = None,
                           optimization_objective: str = "ServiceLevelMaximization"):
    with Timer("[Optimization Runner]") as t:
        simulator = CosmoEngine.LoadSimulator('Simulation')
        time_prefix = "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - "
        t.split(time_prefix + "Load Simulator")

        # Reduce log level to Error during optimization
        logger = CosmoEngine.LoggerManager_GetInstance().GetLogger()
        logger.SetLogLevel(logger.eAssertion)

        # Get data from the simulator
        df_decision_vars = simulator.decision_variables_df
        _end_cycle = simulator.GetModel().GetParameter('NumberOfCycle').GetAsInt()

        nb_pars = 0

        if simulator.FindAttribute("{Model}Model::{Attribute}ActivateVariableMachineOpeningRate").GetAsBool():
            machines = list(sorted(simulator.machine_list))
            nb_pars += len(machines) * simulator.FindAttribute("{Model}Model::{Attribute}NumberOfCycle").GetAsInt()
        else:
            machines = list()

        for group in set(df_decision_vars['Group']):
            nb_var = df_decision_vars[df_decision_vars['Group'] == group].shape[0]
            nb_cycles = (df_decision_vars[df_decision_vars['Group'] == group].reset_index()['EndCycle'][0]
                         - df_decision_vars[df_decision_vars['Group'] == group].reset_index()['StartCycle'][0]
                         + 1)
            nb_pars += nb_cycles * (nb_var if nb_var > 2 else 1)

        nb_pars = max(2, nb_pars)

        specs = dict()
        specs['x0'] = [np.random.random() for _ in range(nb_pars)]
        specs['sigma0'] = sigma0
        specs['inopts'] = dict()
        specs['inopts']['tolx'] = tol_x
        specs['inopts']['tolfun'] = tol_fun
        specs['inopts']['maxfevals'] = max_f_evals
        specs['inopts']['popsize'] = pop_size

        # Initialization of 'bricks'
        # Initialization of CMAES: the optimization alogrithm used
        algorithm = CMAESOptimization(parameter_count=nb_pars,
                                      **specs)
        t.split(time_prefix + "Prepare CMAES")

        # Initialization of the transformation which takes CMAES results and transform them on map: datapath -> value
        transformation = DefaultTransformation(df_decision_vars,
                                               machines,
                                               _end_cycle)
        t.split(time_prefix + "Prepare transformation")

        objective_function = DefaultObjectiveFunction()

        if optimization_objective == "ProfitMaximization":
            objective_function = ProfitMaximizationObjectiveFunction()
        t.split(time_prefix + "Prepare Objective Function")

        optim = MultiprocessingOptimization(algorithm,
                                            objective_function,
                                            transformation,
                                            simulation_name,
                                            pop_size,
                                            amqp_consumer_adress)
        t.split(time_prefix + "Prepare Optimization")

        optim.optimize_parameters()

        # Get optimized results for the algorithm after optimization
        optim_dvs = transformation.applies(algorithm.generate_optimal_solution(), 0)
        t.split(time_prefix + "Optimal solution found")

        # Applies optimized results to the simulator
        for datapath, stringvalue in optim_dvs.items():
            simulator.FindAttribute(datapath).SetAsString(stringvalue)

        if amqp_consumer_adress is not None:
            # Remove old consumers
            for consumer in simulator.GetConsumers():
                simulator.DestroyConsumer(consumer)

            # Instantiate consumers using AMQP to send data to the cloud service
            simulator.InstantiateAMQPConsumers(simulation_name, amqp_consumer_adress)

        # Put back log level to Info for final simulation
        logger.SetLogLevel(logger.eInfo)
        t.split(time_prefix + "Optimal simulation ready")

        # Run final simulation
        simulator.Run()
        t.split(time_prefix + "Optimal simulation done")
