import os
from os import path
import matplotlib.pyplot as plt
from pandapower import plotting


CIGRE_CFG = {
    "slack_size": 0.25,
    "slack_color": "black",
    "slack_zorder": 3,
    "trafo_plot": True,
    "trafo_size": 0.2,
    "trafo_color": "black",
    "trafo_zorder": 0,
    "bus_size": 0.2,
    "bus_color": "blue",
    "bus_zorder": 2,
    "line_size": 2,
    "line_color": "black",
    "line_zorder": 1,
}

SIMBENCH_CFG = {
    "slack_size": 0.00025,
    "slack_color": "black",
    "slack_zorder": 3,
    "trafo_plot": False,
    "trafo_size": 0.0002,
    "trafo_color": "black",
    "trafo_zorder": 0,
    "bus_size": 0.0002,
    "bus_color": "blue",
    "bus_zorder": 2,
    "line_size": 1,
    "line_color": "black",
    "line_zorder": 1,
}


class Plotter:
    """Midas grid plotting class"""

    def __init__(self):
        self.grid = None
        self.grid_type = None
        self.plot_path = "."
        self.plot_name = "DefaultName"
        self.cfg = CIGRE_CFG

    def simple_plot(self):
        """Plot the grid without heatmap"""
        plotting.simple_plot(self.grid)

    def _get_plot(self, figsize):
        cmaps, norms = self._create_cmaps(self.cfg)

        gridplot = plotting.draw_collections(
            self._create_collections(self.cfg, cmaps, norms), figsize
        )

        return gridplot

    def plot(self, name, current_idx=0, figsize=(16, 9)):
        """Plot the grid with heatmaps"""

        if self.grid_type is None or self.grid_type == "cigre":
            self.cfg = CIGRE_CFG
        elif self.grid_type == "simbench":
            self.cfg = SIMBENCH_CFG

        self._get_plot(figsize)
        os.makedirs(self.plot_path, exist_ok=True)
        output = path.join(
            self.plot_path, f"{self.plot_name}-{name}-{current_idx:05d}.png"
        )

        plt.savefig(output)
        plt.close()

    def _create_cmaps(self, cfg):
        """Create pandapower cmaps for plotting."""

        if cfg["trafo_plot"]:
            # Create color map for trafo
            colors_trafo = [(0, "green"), (50, "yellow"), (100, "red")]
            cmap_trafos, norm_trafos = plotting.cmap_continuous(colors_trafo)
        else:
            cmap_trafos = None
            norm_trafos = None

        # Create color map for node voltage
        colors_buses = [(0.935, "blue"), (1.0, "green"), (1.065, "red")]
        cmap_buses, norm_buses = plotting.cmap_continuous(colors_buses)

        # Create color map for line loadings
        colors_lines = [(0, "green"), (40, "yellow"), (80, "red")]
        cmap_lines, norm_lines = plotting.cmap_continuous(colors_lines)

        return (cmap_trafos, cmap_buses, cmap_lines), (
            norm_trafos,
            norm_buses,
            norm_lines,
        )

    def _create_collections(
        self, cfg, cmaps=(None, None, None), norms=(None, None, None)
    ):
        """Create pandapower collections."""

        slack = plotting.create_bus_collection(
            self.grid,
            self.grid.ext_grid.bus.values,
            size=cfg["slack_size"],
            color=cfg["slack_color"],
            zorder=cfg["slack_zorder"],
            patch_type="rect",
        )

        trafo_sec, trafo_prim = self._create_trafo_collection(
            cfg, cmaps[0], norms[0]
        )

        buses = self._create_bus_collection(cfg, cmaps[1], norms[1])

        lines, open_lines = self._create_line_collection(
            cfg, cmaps[2], norms[2]
        )

        cols = [slack, trafo_sec, trafo_prim, buses, lines]

        if open_lines is not None:
            cols.append(open_lines)
        return cols

    def _create_trafo_collection(self, cfg, cmap, norm):
        """Return pandapower trafo collection."""
        if cmap is not None and norm is not None:
            trafo_sec, trafo_prim = plotting.create_trafo_collection(
                self.grid,
                self.grid.trafo.index,
                cmap=cmap,
                norm=norm,
                size=cfg["trafo_size"],
                zorder=cfg["trafo_zorder"],
            )
        else:
            trafo_sec, trafo_prim = plotting.create_trafo_collection(
                self.grid,
                self.grid.trafo.index,
                color=cfg["trafo_color"],
                size=cfg["trafo_size"],
                zorder=cfg["trafo_zorder"],
            )

        return trafo_sec, trafo_prim

    def _create_bus_collection(self, cfg, cmap, norm):
        """Return pandapower bus collection."""
        if cmap is not None and norm is not None:
            buses = plotting.create_bus_collection(
                self.grid,
                self.grid.bus.index,
                size=cfg["bus_size"],
                cmap=cmap,
                norm=norm,
                z=self.grid.res_bus.vm_pu,
                zorder=cfg["bus_zorder"],
            )
        else:
            buses = plotting.create_bus_collection(
                self.grid,
                self.grid.bus.index,
                size=cfg["bus_size"],
                zorder=cfg["bus_zorder"],
            )

        return buses

    def _create_line_collection(self, cfg, cmap, norm):
        """Return pandapower line collection."""

        open_switch_index = self.grid.switch.loc[
            (self.grid.switch["et"] == "1") & ~(self.grid.switch["closed"])
        ]["element"]

        closed_ids = self.grid.line.loc[
            ~self.grid.line.index.isin(open_switch_index)
        ]
        open_ids = self.grid.line.loc[
            self.grid.line.index.isin(open_switch_index)
        ]

        if cmap is not None and norm is not None:
            lines = plotting.create_line_collection(
                self.grid,
                closed_ids.index,
                use_bus_geodata=True,
                cmap=cmap,
                norm=norm,
                linewidths=cfg["line_size"],
                zorder=cfg["line_zorder"],
            )
        else:
            lines = plotting.create_line_collection(
                self.grid,
                closed_ids.index,
                use_bus_geodata=True,
                color=cfg["line_color"],
                linewidths=cfg["line_size"],
                zorder=cfg["line_zorder"],
            )

        open_lines = plotting.create_line_collection(
            self.grid,
            open_ids.index,
            use_bus_geodata=True,
            line_style=":",
            color=cfg["line_color"],
            linewidths=cfg["line_size"],
            zorder=cfg["line_zorder"],
        )

        return lines, open_lines
