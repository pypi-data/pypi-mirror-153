import os

from natsort import natsorted
import matplotlib.pyplot as plt
import numpy as np


def analyze_power(
    data, step_size, report_file, output_path, full_report, config
):
    ef = step_size / 3_600
    name = config["name"]
    report_file.append(f"## {config['topic']} Analysis\n")
    p_stats = dict()
    q_stats = dict()
    data = data[natsorted(data.columns)]
    for colo in data.columns:
        col = colo.replace("___", ".").replace("__", "-")
        key, attr = col.split(".")
        if full_report:
            _plot_series(data[col], ef, col, name, output_path)
        stats = {
            "Min": data[colo].min(),
            "Max": data[colo].max(),
            "Mean": data[colo].mean(),
            "Std": data[colo].std(),
            "Sum": data[colo].sum(),
            "Energy": data[colo].sum() * ef,
        }
        if attr == "p_mw":
            p_stats[key] = stats
        else:
            q_stats[key] = stats

    # Aggregated analyis
    total_p = data[[col for col in data.columns if "p_mw" in col]].sum(axis=1)
    pfile = _plot_series(
        total_p, ef, f"{config['total_name']}.p_mw", name, output_path
    )
    total_q = data[[col for col in data.columns if "q_mvar" in col]].sum(
        axis=1
    )
    qfile = _plot_series(
        total_q, ef, f"{config['total_name']}.q_mvar", name, output_path
    )
    p_stats["total"] = {
        "Min": total_p.min(),
        "Max": total_p.max(),
        "Mean": total_p.mean(),
        "Std": total_p.std(),
        "Sum": total_p.sum(),
        "Energy": total_p.sum() * ef,
    }
    q_stats["total"] = {
        "Min": total_q.min(),
        "Max": total_q.max(),
        "Mean": total_q.mean(),
        "Std": total_q.std(),
        "Sum": total_q.sum(),
        "Energy": total_q.sum() * ef,
    }

    _create_report(p_stats, "MW", config["topic"], report_file)
    report_file.append("")
    _create_report(q_stats, "MVAr", config["topic"], report_file)

    report_file.append(
        f"\n![Total_{config['topic']}_P]({pfile})" + "{width=100%}\n"
    )
    report_file.append(
        f"\n![Total_{config['topic']}_Q]({qfile})" + "{width=100%}\n"
    )

    total_s = np.sqrt(
        np.square(total_p.sum() * ef) + np.square(total_q.sum() * ef)
    )
    return (
        total_p,
        total_q,
        total_s,
        np.ceil(np.max(total_p)),
    )


def _plot_series(data, ef, col, name, output_path):
    series = data.values
    key, attr = col.split(".")
    if attr == "p_mw":
        active = "active"
        unit = "MW"
    else:
        active = "reactive"
        unit = "MVAr"

    annual = np.sort(series)[::-1]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    ax1.plot(series)
    ax1.set_title(f"{key} {active} power")
    # ax1.set_xlabel("time (15 minute steps")
    ax1.set_ylabel(unit)

    ax2.plot(annual)
    ax2.set_title(f"{key} annual curve {active} power")
    ax2.set_ylabel(unit)

    ax3.plot(np.cumsum(ef * series))
    ax3.set_title(f"{key} cummulated {active} power")
    ax3.set_xlabel("time (15 minute steps")
    ax3.set_ylabel(unit)

    filename = os.path.join(output_path, f"{name}_{key}_{active}_power.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    return filename


def _create_report(stats, unit, topic, report_file):
    report_file.append(
        f"| {topic} | Min ({unit}) | Max ({unit}) | Mean ({unit}) |"
        f" StD ({unit}) | Sum ({unit}) | Energy ({unit}h) |"
    )
    report_file.append(
        "|:---------|---------:|---------:|----------:|"
        "---------:|---------:|-------------:|"
    )
    for key, vals in stats.items():
        report_file.append(
            f"| {key} | {vals['Min']:.3f} "
            f"| {vals['Max']:.3f} "
            f"| {vals['Mean']:.3f} "
            f"| {vals['Std']:.3f} "
            f"| {vals['Sum']:.3f} "
            f"| {vals['Energy']:.3f} |"
        )

    report_file.append("")
