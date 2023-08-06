"""This module contains the load estimator of the grid operator."""

from midas.core import DLPSimulator


class LoadEstimator:
    """The load estimator class of the grid operator."""

    def __init__(self, params, entity_map):
        self.config = params
        self.entity_map = entity_map

        sim = DLPSimulator()
        sim.init(
            "",
            step_size=1,
            interpolate=True,
            seed=0,
            start_date=self.config["start_date"],
            data_path=self.config["data_path"],
        )
        self.models = dict()

        # Create estimators for household models
        # for bus_id, loads in self.config['land_mapping'].items():
        #     self.models.setdefault(bus_id, list())
        #     for (_, p_mwh_per_a) in loads:
        #         entity = sim.create(1, 'DefaultLoadH0',
        #                             p_mwh_per_a=p_mwh_per_a*0.1)[0]
        #         self.models[bus_id].append(sim.models[entity['eid']])

        for bus_id, loads in self.config["load_mapping"].items():
            self.models.setdefault(bus_id, list())
            for (_, p_mwh_per_a) in loads:
                entity = sim.create(
                    1, "DefaultLoadH0", p_mwh_per_a=p_mwh_per_a
                )[0]
                self.models[bus_id].append(sim.models[entity["eid"]])

        self.now_dt = None
        self.setpoints = None

    def step(self):
        """Perform a simulation step."""

        self.setpoints = {"Load": dict()}
        for bus_id, models in self.models.items():
            for info in self.entity_map.values():
                if info["etype"] != "Load":
                    continue
                static = info["static"]
                if static["bus"] != bus_id:
                    continue
                idx = info["idx"]

                p_mws = list()
                q_mvars = list()

                for model in models:
                    model.now_dt = self.now_dt
                    model.cos_phi = 0.9
                    model.step()
                    p_mws.append(model.p_mw)
                    q_mvars.append(model.q_mvar)

                self.setpoints["Load"].setdefault(
                    idx,
                    {
                        "static": static,
                        "attrs": {"p_mw": sum(p_mws), "q_mvar": sum(q_mvars)},
                    },
                )
