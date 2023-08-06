import cma

from Supplychain.Protocol.protocol import AbstractOptimizationAlgorithm


class CMAESOptimization(AbstractOptimizationAlgorithm):

    def __init__(self, parameter_count=0, max_vals=None, **kwargs):
        # Bounds are exclusive so 0 and 1 were impossible values
        def_min_bound, def_max_bound = -0.000000001, 1.000000001
        if max_vals is not None:
            bounds = [(def_min_bound, max_vals[i]) for i in range(parameter_count)]
        else:
            bounds = [(def_min_bound, def_max_bound)] * parameter_count

        # Update the inopts dict with bounds
        inopts = kwargs.get("inopts", {})
        inopts["bounds"] = list(zip(*bounds))
        kwargs["inopts"] = inopts

        self.es = cma.CMAEvolutionStrategy(**kwargs)

    def generate_decision_variables(self):
        return self.es.ask()

    def update_algorithm(self, dv_list, result_list):
        self.es.tell(dv_list, result_list)
        self.es.disp()

    def is_not_finished(self):
        return not self.es.stop()

    def generate_optimal_solution(self):
        return self.es.result[0]
