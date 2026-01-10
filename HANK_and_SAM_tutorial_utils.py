"""
Plotting utilities for HANK-and-SAM-tutorial.ipynb

This module contains plotting functions extracted from the tutorial notebook
to reduce clutter and keep focus on economic content.

Functions:
    plot_multipliers_three_experiments: Compare multipliers across monetary regimes
    plot_consumption_irfs_three_experiments: Compare consumption IRFs across regimes
    plot_consumption_irfs_three: Simple consumption IRF comparison
    plot_consumption_irf: Single consumption IRF plot
    plot_consumption_multipliers: Single multiplier plot
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_multipliers_three_experiments(
    multipliers_transfers,
    multipliers_transfers_fixed_nominal_rate,
    multipliers_transfers_fixed_real_rate,
    multipliers_UI_extend,
    multipliers_UI_extensions_fixed_nominal_rate,
    multipliers_UI_extensions_fixed_real_rate,
    multipliers_tax_cut,
    multipliers_tax_cut_fixed_nominal_rate,
    multipliers_tax_cut_fixed_real_rate,
    horizon_length=None,
):
    """
    Plot fiscal multipliers for three policies under three monetary regimes.
    
    Parameters
    ----------
    multipliers_*: array-like
        Multiplier time series for each policy/monetary regime combination
    horizon_length: int, optional
        Number of periods to plot. If None, uses length of input arrays.
    """
    if horizon_length is None:
        horizon_length = len(multipliers_transfers)
    
    green = "darkorange"
    red = "red"

    Length = len(multipliers_transfers_fixed_nominal_rate) + 1
    fontsize = 10
    width = 2
    label_size = 8
    legend_size = 11
    ticksize = 8
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    y_max1 = max(multipliers_transfers_fixed_nominal_rate) * 1.5
    y_max2 = max(multipliers_UI_extensions_fixed_real_rate) * 1.5
    y_max = max([y_max1, y_max2])
    for i in range(3):
        axs[i].set_ylim(-0.2, y_max)

    # Panel 1: Stimulus Check (labeled as UI Extension in original - keeping consistent)
    axs[1].plot(
        np.arange(horizon_length) + 1,
        multipliers_transfers,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[1].plot(
        np.arange(horizon_length) + 1,
        multipliers_transfers_fixed_nominal_rate,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[1].plot(
        np.arange(horizon_length) + 1,
        multipliers_transfers_fixed_real_rate,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[1].set_title("Stimulus Check", fontdict={"fontsize": fontsize})

    # Panel 0: UI Extension
    axs[0].plot(
        np.arange(horizon_length) + 1,
        multipliers_UI_extend,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[0].plot(
        np.arange(horizon_length) + 1,
        multipliers_UI_extensions_fixed_nominal_rate,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[0].plot(
        np.arange(horizon_length) + 1,
        multipliers_UI_extensions_fixed_real_rate,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[0].set_title("UI Extension", fontdict={"fontsize": fontsize})
    axs[0].legend(prop={"size": legend_size}, loc="upper left")

    # Panel 2: Tax Cut
    axs[2].plot(
        np.arange(horizon_length) + 1,
        multipliers_tax_cut,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[2].plot(
        np.arange(horizon_length) + 1,
        multipliers_tax_cut_fixed_nominal_rate,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[2].plot(
        np.arange(horizon_length) + 1,
        multipliers_tax_cut_fixed_real_rate,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[2].set_title("Tax Cut", fontdict={"fontsize": fontsize})

    for i in range(3):
        axs[i].plot(np.zeros(Length), "k")
        axs[i].tick_params(axis="both", labelsize=ticksize)
        axs[i].set_ylabel("Multipliers", fontsize=label_size)
        axs[i].set_xlabel("Quarters", fontsize=label_size)
        axs[i].locator_params(axis="both", nbins=7)
        axs[i].grid(alpha=0.3)

    fig.tight_layout()
    plt.show()


def plot_consumption_irfs_three_experiments(
    irf_UI1, irf_UI2, irf_UI3,
    irf_SC1, irf_SC2, irf_SC3,
    irf_TC1, irf_TC2, irf_TC3,
    C_ss,
):
    """
    Plot consumption IRFs for three policies under three monetary regimes.
    
    Parameters
    ----------
    irf_*: dict
        IRF dictionaries with 'C' key for consumption
    C_ss: float
        Steady state consumption for normalization
    """
    green = "darkorange"
    red = "red"

    Length = 12
    fontsize = 10
    width = 2
    label_size = 8
    legend_size = 11
    ticksize = 8
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    y_max1 = max(100 * irf_TC2["C"][:Length] / C_ss) * 1.05
    y_max2 = max(100 * irf_SC2["C"][:Length] / C_ss) * 1.05
    y_max = max([y_max1, y_max2])
    for i in range(3):
        axs[i].set_ylim(-0.2, y_max)

    # Panel 1: UI Extension
    axs[1].plot(
        100 * irf_UI1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[1].plot(
        100 * irf_UI2["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[1].plot(
        100 * irf_UI3["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[1].set_title("UI Extension", fontdict={"fontsize": fontsize})

    # Panel 0: Stimulus Check
    axs[0].plot(
        100 * irf_SC1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[0].plot(
        100 * irf_SC2["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[0].plot(
        100 * irf_SC3["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[0].set_title("Stimulus Check", fontdict={"fontsize": fontsize})
    axs[0].legend(prop={"size": legend_size})

    # Panel 2: Tax Cut
    axs[2].plot(
        100 * irf_TC1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[2].plot(
        100 * irf_TC2["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    axs[2].plot(
        100 * irf_TC3["C"][:Length] / C_ss,
        linewidth=width,
        label="Fixed Real ",
        linestyle=":",
        color=red,
    )
    axs[2].set_title("Tax Cut", fontdict={"fontsize": fontsize})

    for i in range(3):
        axs[i].plot(np.zeros(Length), "k")
        axs[i].tick_params(axis="both", labelsize=ticksize)
        axs[i].set_ylabel("% consumption deviation", fontsize=label_size)
        axs[i].set_xlabel("Quarters", fontsize=label_size)
        axs[i].locator_params(axis="both", nbins=7)
        axs[i].grid(alpha=0.3)

    fig.tight_layout()
    plt.show()


def plot_consumption_irfs_three(irf_SC1, irf_UI1, irf_TC1, C_ss):
    """
    Plot consumption IRFs for three policies under standard Taylor rule.
    
    Parameters
    ----------
    irf_*: dict
        IRF dictionaries with 'C' key
    C_ss: float
        Steady state consumption
    """
    Length = 12
    fontsize = 10
    width = 2
    label_size = 8
    legend_size = 8
    ticksize = 8
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    y_max1 = max(100 * irf_TC1["C"][:Length] / C_ss) * 1.05
    y_max2 = max(100 * irf_SC1["C"][:Length] / C_ss) * 1.05
    y_max = max([y_max1, y_max2])
    for i in range(3):
        axs[i].set_ylim(-0.1, y_max)

    axs[1].plot(
        100 * irf_UI1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[1].set_title("UI Extension", fontdict={"fontsize": fontsize})

    axs[0].plot(
        100 * irf_SC1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[0].set_title("Stimulus Check", fontdict={"fontsize": fontsize})
    axs[0].legend(prop={"size": legend_size})

    axs[2].plot(
        100 * irf_TC1["C"][:Length] / C_ss,
        linewidth=width,
        label="Standard Taylor Rule",
    )
    axs[2].set_title("Tax Cut", fontdict={"fontsize": fontsize})

    for i in range(3):
        axs[i].plot(np.zeros(Length), "k")
        axs[i].tick_params(axis="both", labelsize=ticksize)
        axs[i].set_ylabel("% consumption deviation", fontsize=label_size)
        axs[i].set_xlabel("Quarters", fontsize=label_size)
        axs[i].locator_params(axis="both", nbins=7)
        axs[i].grid(alpha=0.3)
    
    fig.tight_layout()
    plt.show()


def plot_consumption_irf(irf1, irf2, irf3, C_ss, y_max, title="", legend=False):
    """
    Plot a single consumption IRF comparison across monetary regimes.
    
    Parameters
    ----------
    irf1, irf2, irf3: dict
        IRF dictionaries for Taylor rule, fixed nominal, fixed real
    C_ss: float
        Steady state consumption
    y_max: float
        Y-axis maximum
    title: str
        Plot title
    legend: bool
        Whether to show legend
    """
    green = "darkorange"
    red = "red"

    Length = 12
    plt.figure(figsize=(4, 4))
    x_axis = np.arange(1, Length + 1)

    plt.plot(x_axis, 100 * irf1["C"][:Length] / C_ss, label="Active Taylor Rule")
    plt.plot(
        x_axis,
        100 * irf2["C"][:Length] / C_ss,
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    plt.plot(
        x_axis,
        100 * irf3["C"][:Length] / C_ss,
        label="Fixed Real",
        linestyle=":",
        color=red,
    )

    plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, 1.0))
    plt.xlabel("quarter")
    plt.ylim(0, y_max)
    if title:
        plt.title(title)
    if legend:
        plt.legend(loc="best")
        plt.ylabel("% consumption deviation")
    plt.show()


def plot_consumption_multipliers(
    multiplier1, multiplier2, multiplier3, y_max, title="", legend=False
):
    """
    Plot a single multiplier comparison across monetary regimes.
    
    Parameters
    ----------
    multiplier1, multiplier2, multiplier3: array-like
        Multiplier series for Taylor rule, fixed nominal, fixed real
    y_max: float
        Y-axis maximum
    title: str
        Plot title
    legend: bool
        Whether to show legend
    """
    green = "darkorange"
    red = "red"

    Length = 12
    plt.figure(figsize=(4, 4))
    x_axis = np.arange(1, Length + 1)

    plt.plot(x_axis, multiplier1[0:Length], label="Active Taylor Rule")
    plt.plot(
        x_axis,
        multiplier2[0:Length],
        label="Fixed Nominal Rate",
        linestyle="--",
        color=green,
    )
    plt.plot(
        x_axis, multiplier3[0:Length], label="Fixed Real", linestyle=":", color=red
    )

    plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, 1.0))
    plt.xlabel("quarter")
    plt.ylim(0, y_max)
    if title:
        plt.title(title)
    if legend:
        plt.legend(loc="best")
    plt.show()
