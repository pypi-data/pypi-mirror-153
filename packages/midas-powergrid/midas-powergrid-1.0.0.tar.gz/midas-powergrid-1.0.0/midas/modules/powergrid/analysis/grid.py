import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from midas.util import report_util

from .bus import analyze_buses
from .power import analyze_power


def analyze_grid(data, step_size, name, output_path, full_report):
    plot_path = os.path.join(output_path, name.rsplit("-", 1)[1]).replace(
        "__", "_"
    )
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
    load_data = data[[col for col in data.columns if "load__" in col]]
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

    report_path = os.path.join(
        output_path, f"{name.replace('__', '_')}_report.md"
    )
    report_file = open(report_path, "w")

    if load_totals[0].sum() == 0:
        energy_suffiency = 0
    else:
        energy_suffiency = 100 * sgen_totals[0].sum() / load_totals[0].sum()

    if sgen_totals[3] == 0:
        full_load_hours = 0
    else:
        full_load_hours = sgen_totals[0].sum() * ef / sgen_totals[3]

    report_file.write(
        f"# Analysis of {name}\n\n## Summary\n\n"
        f"* bus health: {score:.2f} %\n"
        f"* active energy sufficiency: {energy_suffiency:.2f} %\n"
        # "* reactive energy sufficiency: "
        # f"{100*sgen_totals[1].sum()/load_totals[1].sum():.2f} %\n"
        f"\n## Demand and Supply\n\n"
        f"* total active energy demand: {load_totals[0].sum() * ef:.2f} MWh\n"
        f"* total active energy supply: {sgen_totals[0].sum() * ef:.2f} MWh "
        f"or about {full_load_hours:.2f} full load hours\n"
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

    report_util.convert_markdown(report_path)


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
