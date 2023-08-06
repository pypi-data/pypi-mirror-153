from abc import abstractmethod

# from midas.core.powergrid.c import constraints


class GridElement:
    @staticmethod
    @abstractmethod
    def pp_key() -> str:
        """
        Returns
        -------
        str
            Returns pandapower's identifier for self element type
        """
        pass

    @staticmethod
    @abstractmethod
    def res_pp_key() -> str:
        """
        Returns
        -------
        str
            Returns pandapower's identifier for self res_element type
        """
        pass

    def __init__(self, index, grid_model, log):
        self.grid = grid_model
        self.index = index
        self.log = log

        self._constraints = list()
        self._unsatisfied_constraints = list()
        self._manipulations = list()

    def add_constraint(self, constraint):
        self._constraints.append(constraint)

    def add_constraints(self, constraints):
        self._constraints.extend(constraints)

    def remove_constraint(self, constraint):
        self._constraints.remove(constraint)

    def parameters(self):
        # columns = list(self.grid.)
        pass

    def set_value(self, attribute, value):
        self.grid[self.pp_key()].loc[self.index, attribute] = value

    def step(self, time) -> bool:
        return False

    def _check(self, time):
        if self._constraints:
            self._unsatisfied_constraints = [
                constr
                for constr in self._constraints
                if constr.check(time) is False
            ]

            for constraint in self._unsatisfied_constraints:
                constraint.handle_violation()

            # if not self.parameters()["in_service"]:
            #     if self._can_reconnect():
            #         self.set_value("in_service", True)

    # def _can_reconnect(self) -> bool:
    # from grid.elements.PPBus import PPBus

    # bus = self.grid_model.grid_state[PPBus][self.bus]
    # voltage = bus.res_vm_pu
    # if self.unsatisfied_constraints or voltage < 0.95:
    #     return False
    # else:
    #     return True
    # pass
