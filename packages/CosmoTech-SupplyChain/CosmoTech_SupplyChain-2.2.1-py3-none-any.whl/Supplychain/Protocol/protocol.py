from abc import ABCMeta, abstractmethod


class AbstractOptimizationAlgorithm(object):
    """
    Abstract class allowing the encapsulation of an optimization algorithm
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_decision_variables(self):
        pass

    @abstractmethod
    def update_algorithm(self, dv_list, result_list):
        pass

    @abstractmethod
    def is_not_finished(self):
        pass

    @abstractmethod
    def generate_optimal_solution(self):
        pass


class AbstractObjectiveFunction(object):
    """
    Abstract class allowing the computation of an Objective function using the output of a simulation
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def applies(self, results):
        pass


class AbstractParameterTransformation(object):
    """
    Abstract class allowing the transformation of an Optimization Algorithm output to an input for the simulation
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def applies(self, variables):
        pass


class AbstractOptimization(object):

    __metaclass__ = ABCMeta

    def __init__(self,
                 optimization_algorithm,
                 objective_function,
                 parameter_transformation,
                 simulation_id):

        if not isinstance(optimization_algorithm, AbstractOptimizationAlgorithm):
            raise ValueError("optimization_algorithm must be an OptimizationAlgorithm")

        if not isinstance(objective_function, AbstractObjectiveFunction):
            raise ValueError("objective_function must be an ObjectiveFunction")

        if not isinstance(parameter_transformation, AbstractParameterTransformation):
            raise ValueError("parameter_transformation must be an ParameterTransformation")

        self.opt_algo = optimization_algorithm
        self.obj_func = objective_function
        self.par_tran = parameter_transformation

        self.simulation_id = simulation_id

    @abstractmethod
    def optimize_parameters(self):
        pass
