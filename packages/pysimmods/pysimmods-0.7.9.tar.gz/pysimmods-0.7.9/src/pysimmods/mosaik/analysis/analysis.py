import os

import pandas as pd
from midas.util import report_util

from .power import analyze_power


def analyze(
    name: str,
    data: pd.HDFStore,
    output_folder: str,
    start: int,
    end: int,
    step_size: int,
    full: bool,
):
    der_sim_keys = [
        sim_key for sim_key in data.keys() if "Pysimmods" in sim_key
    ]

    for sim_key in der_sim_keys:
        der_data = data[sim_key]
        if start > 0:
            der_data = der_data.iloc[start:]
        if end > 0:
            der_data = der_data.iloc[:end]

        analyze_der(
            der_data,
            step_size,
            f"{name}-{sim_key.replace('/','')}",
            output_folder,
            full,
        )


def analyze_der(data, step_size, name, output_path, full_report):
    plot_path = os.path.join(
        output_path, name.rsplit("-", 1)[1].replace("__", "_")
    )
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

    report_util.convert_markdown(report_path)
