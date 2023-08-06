from Supplychain.Protocol.protocol import AbstractObjectiveFunction


class ProfitMaximizationObjectiveFunction(AbstractObjectiveFunction):
    """
    Profit Maximization objective function :
    We compute the maximal profit for the model.
    """
    def applies(self, simulation_result):

        objective = -sum(map(lambda r: float(r.get('Profit', 0)), simulation_result))

        return objective


class DefaultObjectiveFunction(AbstractObjectiveFunction):
    """
    Default objective function for SupplyChain :
    We compute a distance to demand valuation of the results
    """
    def applies(self, simulation_result):

        objective = sum(map(lambda r: float(r.get('ServiceLevelIndicator', 0)), simulation_result))

        return objective
