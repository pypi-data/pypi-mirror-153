"""This module contains the collector for palaestrai."""
import collections
from pprint import pprint
import mosaik_api


META = {
    "models": {
        "Database": {
            "public": True,
            "any_inputs": True,
            "params": ["filename", "verbose"],
            "attrs": [],
        }
    }
}


class ARLCollector(mosaik_api.Simulator):
    """THE one and only collector.

    This version is perfectly suited for the usage with the palaestrAI
    framework. It replaces the mosaikHDF5 database (which is currently
    not working with palaestrai caused by an yet unknown bug) and is
    connected to each and every output that otherwise would output to
    the database.

    If a filename is provided, all collected outputs will be written to
    that file as plain text. If verbose is set to True, all outputs
    will be printed to the console after the simulation.

    Why bothering with the collection of outputs at all? Because
    palaestrai relies on so called sensors that are basically one
    simulator's outputs. These sensors can only be accessed if mosaik
    has registered some receiver for the output of a simulator.

    """

    def __init__(self):
        super().__init__(META)

        self.sid = None
        self.eid = None
        self.data = collections.defaultdict(
            lambda: collections.defaultdict(list)
        )

        self.step_size = None
        self.finalized = False
        self.filename = None
        self.verbose = None

    def init(self, sid, **sim_params):

        self.sid = sid
        self.step_size = sim_params.get("step_size", 900)
        self.verbose = sim_params.get("verbose", False)

        return self.meta

    def create(self, num, model, **model_params):
        errmsg = (
            "You should really not try to instantiate more than one ",
            "database.",
        )
        assert num == 1 and self.eid is None, errmsg

        self.eid = "Database"
        self.filename = model_params.get("filename", None)

        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs):
        data = inputs[self.eid]
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr].append(value)

        return time + self.step_size

    def get_data(self, outputs):

        return {}

    def finalize(self):
        if self.finalized:
            return
        else:
            self.finalized = True

        if self.verbose:
            pprint("Collected data:")
            for sim, sim_data in sorted(self.data.items()):
                pprint(f"-{sim}:")
                for attr, values in sorted(sim_data.items()):
                    pprint(f"  -{attr}: {values}")

        if self.filename is not None:
            path = f"{self.filename}.txt"
            with open(path, "w") as dbfile:
                dbfile.write("Collected data:\n")
                for sim, sim_data in sorted(self.data.items()):
                    dbfile.write(f"-{sim}:\n")
                    for attr, values in sorted(sim_data.items()):
                        dbfile.write(f"  -{attr}: {values}\n")
                    dbfile.write("\n")
                dbfile.write("Complete! See you next time. :)\n")

        self.data = None


if __name__ == "__main__":
    mosaik_api.start_simulation(ARLCollector())
