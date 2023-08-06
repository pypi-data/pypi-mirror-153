import os
import subprocess

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .bus_analysis import analyze_buses
from .power_analysis import analyze_power


def analyze(
    name,
    db_path,
    output_path,
    db_style="mosaik",
    start=0,
    end=-1,
    step_size=900,
    full=False,
):
    mosaik_style = db_style.lower() == "mosaik"
    data = load_db(db_path, mosaik_style)

    os.makedirs(output_path, exist_ok=True)

    # Grids
    if mosaik_style:
        grid_sim_keys = ["Powergrid-0"]
        der_sim_keys = ["Pysimmods-0"]
    else:
        grid_sim_keys = [
            sim_key for sim_key in data.keys() if "Powergrid" in sim_key
        ]
        der_sim_keys = [
            sim_key for sim_key in data.keys() if "Pysimmods" in sim_key
        ]

    for sim_key in grid_sim_keys:
        grid_data = data[sim_key]
        if start > 0:
            grid_data = grid_data.iloc[start:]
        if end > 0:
            grid_data = grid_data.iloc[:end]

        analyze_grid(
            grid_data,
            step_size,
            f"{name}_{sim_key.replace('/', '')}",
            output_path,
            full,
            mosaik_style,
        )

    for sim_key in der_sim_keys:
        der_data = data[sim_key]
        if start > 0:
            der_data = der_data.iloc[start:]
        if end > 0:
            der_data = der_data.iloc[:end]

        analyze_der(
            der_data,
            step_size,
            f"{name}_{sim_key.replace('/','')}",
            output_path,
            full,
        )
    if not mosaik_style:
        data.close()


def load_db(filename, mosaik_style):
    if mosaik_style:
        data = dict()
        with h5py.File(filename, "r") as data_file:

            for tsd in data_file["Series"]:
                sid, eid = tsd.split(".")
                data.setdefault(sid, dict())
                data[sid].setdefault(eid, dict())
                for attr in data_file["Series"][tsd]:
                    data[sid][eid][attr] = np.array(
                        data_file["Series"][tsd][attr]
                    )

        return data
    else:
        return pd.HDFStore(filename)


def analyze_grid(
    data, step_size, name, output_path, full_report, mosaik_style
):
    plot_path = os.path.join(output_path, name.rsplit("_", 1)[1])
    os.makedirs(plot_path, exist_ok=True)

    ef = step_size / 3_600
    report_content = list()
    bus_data = data[[col for col in data.columns if "bus" in col]]
    score = analyze_buses(
        bus_data, report_content, name, plot_path, full_report
    )

    def is_ext_grid(col):
        return "ext_grid" in col or "slack" in col

    ext_grid_data = data[[col for col in data.columns if is_ext_grid(col)]]
    extgrid_totals = analyze_power(
        ext_grid_data,
        step_size,
        report_content,
        plot_path,
        full_report,
        {"name": name, "topic": "ExtGrid", "total_name": "0-extgrids"},
    )
    load_data = data[[col for col in data.columns if "load-" in col]]
    load_totals = analyze_power(
        load_data,
        step_size,
        report_content,
        plot_path,
        full_report,
        {"name": name, "topic": "Load", "total_name": "0-loads"},
    )

    sgen_data = data[[col for col in data.columns if "sgen" in col]]
    sgen_totals = analyze_power(
        sgen_data,
        step_size,
        report_content,
        plot_path,
        full_report,
        {"name": name, "topic": "Sgen", "total_name": "0-sgens"},
    )

    storage_data = data[[col for col in data.columns if "storage" in col]]
    if not storage_data.empty:
        storage_totals = analyze_power(
            storage_data,
            step_size,
            report_content,
            plot_path,
            full_report,
            {"name": name, "topic": "Storage", "total_name": "0-storages"},
        )
        # Storages work in consumer system,
        # i.e., charging > 0, discharging < 0
        load_sgen_diff = pd.DataFrame(
            {
                "load+storage-sgen.p_mw": load_totals[0]
                + storage_totals[0]
                - sgen_totals[0],
                "load+storage-sgen.q_mvar": load_totals[1]
                + storage_totals[1]
                - sgen_totals[1],
            }
        )
    else:
        load_sgen_diff = pd.DataFrame(
            {
                "load-sgen.p_mw": load_totals[0] - sgen_totals[0],
                "load-sgen.q_mvar": load_totals[1] - sgen_totals[1],
            }
        )

    analyze_power(
        load_sgen_diff,
        step_size,
        report_content,
        plot_path,
        False,
        {"name": name, "topic": "Load-Balance", "total_name": "0-load-sgen"},
    )

    report_path = os.path.join(output_path, f"{name}_report.md")
    report_file = open(report_path, "w")

    report_file.write(
        f"# Analysis of {name}\n\n## Summary\n\n"
        f"* bus health: {score:.2f} %\n"
        "* active energy sufficiency: "
        f"{100*sgen_totals[0].sum()/load_totals[0].sum():.2f} %\n"
        # "* reactive energy sufficiency: "
        # f"{100*sgen_totals[1].sum()/load_totals[1].sum():.2f} %\n"
        f"\n## Demand and Supply\n\n"
        f"* total active energy demand: {load_totals[0].sum() * ef:.2f} MWh\n"
        f"* total active energy supply: {sgen_totals[0].sum() * ef:.2f} MWh "
        f"or about {sgen_totals[0].sum()*ef/sgen_totals[3]:.2f} "
        "full load hours\n"
        "* extg. active energy supply: "
        f"{extgrid_totals[0].sum()*ef:.2f} MWh\n"
        "* total reactive energy demand: "
        f"{load_totals[1].sum()*ef:.2f} MVArh\n"
        "* total reactive energy supply: "
        f"{sgen_totals[1].sum()*ef:.2f} MVArh\n"
        f"* extg. reactive energy supply: {extgrid_totals[1].sum()*ef:.2f} "
        "MVArh\n"
        f"* total apparent energy demand: {load_totals[2]:.2f} MVAh\n"
        f"* total apparent energy supply: {sgen_totals[2]:.2f} MVAh\n"
        f"* extg. apparent energy supply: {extgrid_totals[2]:.2f} MVAh\n\n"
    )

    for line in report_content:
        report_file.write(f"{line}\n")
    report_file.close()

    try:
        subprocess.check_output(
            [
                "pandoc",
                "--template",
                "eisvogel",
                "--listings",
                # "-s",
                # "-t",
                # "odt",
                "-o",
                f"{report_path[:-3]}.pdf",
                report_path,
            ]
        )
    except FileNotFoundError:
        # pandoc or eisvogel template not available
        try:
            subprocess.check_output(
                [
                    "pandoc",
                    "-s",
                    "-t",
                    "odt",
                    "-o",
                    f"{report_path[:-3]}.odt",
                    report_path,
                ]
            )
        except FileNotFoundError:
            # no pandoc available
            pass


def analyze_line(data, report_file, name, output_path):
    load_percent = np.array([data[key]["loading_percent"] for key in data])

    data["line_avg"] = {"loading_percent": load_percent.mean(axis=0)}

    for key, vals in data.items():
        load_percent = np.array(vals["loading_percent"])

        annual = np.sort(load_percent)[::-1]
        too_high10 = (annual > 120).sum()
        too_high4 = (annual > 60).sum()

        if too_high10 > 0:
            report_file.write(f"[{key}] {too_high10} values > 120\n")
        if too_high4 > 0:
            report_file.write(f"[{key}] {too_high4} values > 60\n")

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.plot(annual)
        ax.axhline(y=120, color="red")
        ax.axhline(y=60, linestyle="--", color="red")
        ax.set_title(f"{key}")
        ax.set_ylabel("Line load percentage")
        ax.set_xlabel("time (15 minute steps)")
        plt.savefig(
            os.path.join(
                output_path, f"{name}_{key}_load_percentage_annual.png"
            ),
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()


def analyze_der(data, step_size, name, output_path, full_report):
    plot_path = os.path.join(output_path, name.rsplit("_", 1)[1])
    os.makedirs(plot_path, exist_ok=True)

    ef = step_size / 3_600
    report_content = list()

    gens = ["Photovoltaic", "CHP", "Biogas", "DieselGenerator"]
    loads = ["HVAC"]
    bufs = ["Battery"]

    model_totals = dict()
    for model in gens + loads + bufs:
        mod_data = data[[col for col in data.columns if model in col]]
        if not mod_data.empty:
            model_totals[model] = analyze_power(
                mod_data,
                step_size,
                report_content,
                plot_path,
                full_report,
                {"name": name, "topic": model, "total_name": f"{model}s"},
            )

    report_path = os.path.join(output_path, f"{name}_report.md")
    report_file = open(report_path, "w")

    total_gen_p = 0
    total_gen_q = 0
    total_load_p = 0
    total_load_q = 0
    for model, totals in model_totals.items():
        if model in gens:
            total_gen_p += totals[0].sum()
            total_gen_q += totals[1].sum()
        if model in loads:
            total_load_p += totals[0].sum()
            total_load_q += totals[1].sum()
        if model in bufs:
            total_gen_p -= totals[0][totals[0] < 0].sum()
            total_gen_q -= totals[1][totals[1] < 0].sum()
            total_load_p += totals[0][totals[0] > 0].sum()
            total_load_q += totals[1][totals[1] > 0].sum()

    report_file.write(
        f"# Analysis of {name}\n\n## Summary\n\n"
        f"* total active generation: {total_gen_p*ef:.2f} MWh\n"
        f"* total reactive generation: {total_gen_q*ef:.2f} MVArh\n"
        f"* total active consumption: {total_load_p*ef:.2f} MWh\n"
        f"* total reactive consumption: {total_load_q*ef:.2f} MVArh\n\n"
    )

    for line in report_content:
        report_file.write(f"{line}\n")
    report_file.close()

    try:
        subprocess.check_output(
            [
                "pandoc",
                "-s",
                "-t",
                "odt",
                "-o",
                f"{report_path[:-3]}.odt",
                report_path,
            ]
        )
    except FileNotFoundError:
        # no pandoc available
        pass


if __name__ == "__main__":
    analyze(
        name="midasmv_der",
        db_path="_outputs/midasmv_der.hdf5",
        db_style="midas",
    )
