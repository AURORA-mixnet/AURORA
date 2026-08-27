# -*- coding: utf-8 -*-

"""
Publication-figure plotting utilities.

The ``Plotter`` class generates the figures reproduced by ``Experiments.py``.

This version keeps the original plotting behavior, except that zoom insets in
``simple_plot20`` are constrained to the parent axes and no longer draw the
long ``mark_inset`` connector lines that could extend outside the plot.
"""

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, X, Y, Descriptions, X_label, Y_label, name,
                 Titles=None, condition=False, shadow_margin=0.05):
        self.X = X
        self.Y = Y
        self.Desc = Descriptions
        self.XL = X_label
        self.YL = Y_label
        self.name = name
        self.condition = condition
        self.markers = ['o', 's', 'D', 'v', '^', '<', '>', 'p', 'h', '*']
        self.Line_style = ['-', '--', '-', '--']
        self.colors = [
            'blue', 'black', 'darkgreen', 'purple', 'red', 'fuchsia',
            'indigo', 'teal', 'lime', 'blue', 'black', 'orange',
            'violet', 'lightblue'
        ]
        self.shadow_margin = shadow_margin
        self.Titles = Titles
        self.LEN = len(Y[0])
        self.loc1 = 'lower right'
        self.loc2 = 'lower left'
        self.loc3 = 'upper right'
        self.loc4 = 'upper left'

    def simple_plot(self, y_max=None, x_tight=False, xx=False):
        if not xx:
            loc_1 = 'upper right'
        else:
            loc_1 = 'upper left'
        loc_1 = 'upper right'

        plt.figure(figsize=(10, 6))
        for i, y in enumerate(self.Y):
            color = self.colors[i % len(self.colors)]
            marker = self.markers[i % len(self.markers)]
            line_style = self.Line_style[i % len(self.Line_style)]
            plt.plot(
                self.X, y, color=color, linestyle=line_style,
                marker=marker, markersize=16,
                markerfacecolor='none', markeredgewidth=3,
                markeredgecolor=color, linewidth=3,
                label=self.Desc[i]
            )

        plt.xlabel(self.XL, fontsize=30, fontweight='bold')
        plt.ylabel(self.YL, fontsize=30, fontweight='bold')
        plt.legend(
            fontsize=20, loc=loc_1, frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        plt.grid(linestyle='--', alpha=0.7, linewidth=0.8)

        if y_max is None:
            y_max = max([max(y) for y in self.Y])
        plt.ylim(0, y_max)

        if x_tight:
            plt.xlim(min(self.X) - 0.1, max(self.X) + 0.1)

        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(5))
        plt.xticks(fontsize=25, fontweight='bold')
        plt.yticks(fontsize=25, fontweight='bold')

        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def simple_plot_B(self, y_max=None, x_tight=False, xx=False):
        if not xx:
            loc_1 = 'upper right'
        else:
            loc_1 = 'upper left'
        loc_1 = 'upper left'

        plt.figure(figsize=(10, 6))
        for i, y in enumerate(self.Y):
            color = self.colors[i % len(self.colors)]
            marker = self.markers[i % len(self.markers)]
            line_style = self.Line_style[i % len(self.Line_style)]
            plt.plot(
                self.X, y, color=color, linestyle=line_style,
                marker=marker, markersize=15,
                markerfacecolor='none', markeredgewidth=3,
                markeredgecolor=color, linewidth=3,
                label=self.Desc[i]
            )

        plt.xlabel(self.XL, fontsize=40, fontweight='bold')
        plt.ylabel(self.YL, fontsize=40, fontweight='bold')
        plt.legend(
            fontsize=26, loc=loc_1, frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        plt.grid(linestyle='--', alpha=0.7, linewidth=0.8)

        if y_max is None:
            y_max = max([max(y) for y in self.Y])
        plt.ylim(0, y_max)

        if x_tight:
            plt.xlim(min(self.X) - 0.1, max(self.X) + 0.1)

        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(5))
        plt.xticks(fontsize=35, fontweight='bold')
        plt.yticks(fontsize=35, fontweight='bold')

        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def merged_plot(self, Y_1max=None, Y_2max=None):
        c_color1 = ['blue', 'red']
        c_color2 = ['green', 'black']
        fig, ax1 = plt.subplots(figsize=(10, 6))

        for i, y in enumerate(self.Y[0]):
            color = c_color2[i % 2]
            marker = self.markers[i % len(self.markers)]
            line_style = self.Line_style[i % 2]
            ax1.plot(
                self.X, y, color=color, linestyle=line_style,
                marker=marker, markersize=16,
                markerfacecolor='none', markeredgewidth=3,
                markeredgecolor=color, linewidth=3,
                label=self.Desc[0][i]
            )

        ax1.set_xlabel(self.XL, fontsize=30, fontweight='bold')
        ax1.set_ylabel(
            self.YL[0], fontsize=30, fontweight='bold', color='black'
        )
        ax1.tick_params(axis='y', labelsize=25, colors='black')
        ax1.tick_params(axis='x', labelsize=25)
        if Y_1max is not None:
            ax1.set_ylim(0, Y_1max)

        left_legend = ax1.legend(
            fontsize=12, loc='upper left', frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        ax1.add_artist(left_legend)
        ax1.text(0.05, 0.85, 'data1', fontsize=12, ha='left', transform=ax1.transAxes)

        ax2 = ax1.twinx()
        for i, z in enumerate(self.Y[1]):
            color = c_color1[i % 2]
            marker = self.markers[i % len(self.markers)]
            line_style = self.Line_style[i % 2]
            ax2.plot(
                self.X, z, color=color, linestyle=line_style,
                marker=marker, markersize=16,
                markerfacecolor='none', markeredgewidth=3,
                markeredgecolor=color, linewidth=3,
                label=self.Desc[1][i]
            )

        ax2.set_ylabel(
            self.YL[1], fontsize=30, fontweight='bold', color='black'
        )
        ax2.tick_params(axis='y', labelsize=25, colors='black')
        if Y_2max is not None:
            ax2.set_ylim(0, Y_2max)

        ax2.legend(
            fontsize=12, loc='upper right', frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        ax2.text(0.95, 0.85, 'data2', fontsize=12, ha='right', transform=ax2.transAxes)
        ax1.grid(linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def cdf_plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(
            self.X, self.Y[0], color=self.colors[0],
            linestyle=self.Line_style[0], linewidth=2.5,
            label=self.Desc[0]
        )

        middle_idx = len(self.Y) // 2
        plt.plot(
            self.X, self.Y[middle_idx], color=self.colors[1],
            linestyle=self.Line_style[1], linewidth=3,
            label=self.Desc[middle_idx]
        )
        plt.plot(
            self.X, self.Y[-1], color=self.colors[2],
            linestyle=self.Line_style[2], linewidth=3,
            label=self.Desc[-1]
        )

        y1 = np.array(self.Y[0])
        y_last = np.array(self.Y[-1])
        shadow_margin = 0.05 * (np.max(self.Y) - np.min(self.Y))
        plt.fill_between(
            self.X, y1 - shadow_margin, y_last + shadow_margin,
            color='gray', alpha=0.35, label=r'$0<\alpha<1$'
        )

        plt.xlabel(self.XL, fontsize=30, fontweight='bold')
        plt.ylabel(self.YL, fontsize=30, fontweight='bold')
        plt.xticks(fontsize=25, fontweight='bold')
        plt.yticks(fontsize=25, fontweight='bold')
        plt.legend(
            fontsize=18, loc='upper left', frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        plt.grid(linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def extended_cdf_plot(self, tick_step=None):
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        axes = axes.flatten()
        for i, (Y_i, ax) in enumerate(zip(self.Y, axes)):
            ax.plot(
                self.X, Y_i[0], color=self.colors[0],
                linestyle=self.Line_style[0], linewidth=3,
                label=self.Desc[0]
            )
            ax.plot(
                self.X, Y_i[-1], color=self.colors[1],
                linestyle=self.Line_style[1], linewidth=3,
                label=self.Desc[self.LEN - 1]
            )

            y1 = np.array(Y_i[0], dtype=float)
            y_last = np.array(Y_i[-1], dtype=float)
            ax.fill_between(
                self.X, y1 - self.shadow_margin,
                y_last + self.shadow_margin,
                color='gray', alpha=0.3
            )

            ax.set_title(self.Titles[i], fontsize=25, fontweight='bold')
            ax.grid(linestyle='--', alpha=0.7)
            ax.tick_params(axis='both', which='major', labelsize=20)

            if tick_step:
                x_values = np.asarray(self.X, dtype=float)
                ax.set_xticks(np.arange(x_values.min(), x_values.max() + tick_step, tick_step))
                ax.set_yticks(np.arange(y1.min(), y_last.max() + tick_step, tick_step))

            ax.legend(
                fontsize=20, loc='lower right', frameon=True,
                framealpha=0.6, edgecolor='gray'
            )

        fig.text(
            0.04, 0.5, self.YL, va='center', rotation='vertical',
            fontsize=25, fontweight='bold'
        )
        fig.text(
            0.5, 0.02, self.XL, ha='center', fontsize=22,
            fontweight='bold'
        )
        plt.tight_layout(rect=[0.05, 0.05, 1, 1])
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def box_plot(self, y_max=None):
        plt.figure(figsize=(10, 5))
        num_categories = len(self.Y)
        group_width = 0.4
        category_width = group_width / num_categories

        for i in range(len(self.X)):
            positions = [
                self.X[i] * 2.8 + j * category_width
                for j in range(num_categories)
            ]
            data = [self.Y[j][i] for j in range(num_categories)]

            for j in range(num_categories):
                edge_color = self.colors[j % len(self.colors)]
                plt.boxplot(
                    data[j], positions=[positions[j]],
                    widths=category_width * 0.8, patch_artist=True,
                    boxprops=dict(
                        facecolor='white', edgecolor=edge_color,
                        linewidth=3
                    ),
                    medianprops=dict(color='black', linewidth=3),
                    whiskerprops=dict(color=edge_color, linewidth=3),
                    capprops=dict(color=edge_color, linewidth=3),
                    flierprops=dict(marker='o', color='gray', alpha=0.1)
                )

        plt.xlabel(self.XL, fontsize=30, fontweight='bold')
        plt.ylabel(self.YL, fontsize=30, fontweight='bold')
        legend_elements = [
            plt.Line2D(
                [0], [0], color=self.colors[i % len(self.colors)],
                lw=4, label=desc
            )
            for i, desc in enumerate(self.Desc)
        ]
        plt.legend(
            handles=legend_elements, fontsize=20,
            loc='upper right', frameon=True
        )
        plt.xticks(
            [
                self.X[i] * 2.8 +
                (num_categories - 1) * category_width / 2
                for i in range(len(self.X))
            ],
            [x for x in self.X], fontsize=25
        )

        if y_max is not None:
            plt.ylim(0, y_max)
        plt.tick_params(axis='y', labelsize=25)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def box_plot_(self, y_max=None):
        plt.figure(figsize=(10, 5))
        num_categories = len(self.Y)
        group_width = 0.4
        category_width = group_width / num_categories

        for i in range(len(self.X)):
            positions = [
                (i + 1) * 0.5 + j * category_width
                for j in range(num_categories)
            ]
            data = [self.Y[j][i] for j in range(num_categories)]
            for j in range(num_categories):
                edge_color = self.colors[j % len(self.colors)]
                plt.boxplot(
                    data[j], positions=[positions[j]],
                    widths=category_width * 0.8, patch_artist=True,
                    boxprops=dict(
                        facecolor='white', edgecolor=edge_color,
                        linewidth=3
                    ),
                    medianprops=dict(color='black', linewidth=3),
                    whiskerprops=dict(color=edge_color, linewidth=3),
                    capprops=dict(color=edge_color, linewidth=3),
                    flierprops=dict(marker='o', color='gray', alpha=0.01)
                )

        plt.xlabel(self.XL, fontsize=30, fontweight='bold')
        plt.ylabel(self.YL, fontsize=30, fontweight='bold')
        legend_elements = [
            plt.Line2D(
                [0], [0], color=self.colors[i % len(self.colors)],
                lw=4, label=desc
            )
            for i, desc in enumerate(self.Desc)
        ]
        plt.legend(
            handles=legend_elements, fontsize=20,
            loc='upper right', frameon=True
        )
        plt.xticks(
            [
                (i + 1) * 0.5 +
                (num_categories - 1) * category_width / 2
                for i in range(len(self.X))
            ],
            [x for x in self.X], fontsize=25
        )

        if y_max is not None:
            plt.ylim(0, y_max)
        plt.tick_params(axis='y', labelsize=25)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()

    def simple_plot20(self, y_max=None, x_tight=False, xx=0, inset_zoom=False):
        """
        Draw the main line plot and, when requested, a zoom inset.

        The inset is deliberately positioned in axes coordinates so that it is
        always fully contained within the main plotting box.  The old version
        used a fixed 5-inch inset plus ``mark_inset`` connector lines; those
        connectors could be drawn far outside the figure and produced the
        long diagonal shapes seen in some generated figures.
        """
        if int(xx) == 0:
            loc_1 = self.loc2
        elif int(xx) == 1:
            loc_1 = self.loc1
        elif int(xx) == 3:
            loc_1 = self.loc4
        elif int(xx) == 2:
            loc_1 = self.loc3
        else:
            loc_1 = 'upper left'

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, y in enumerate(self.Y):
            color = self.colors[i % len(self.colors)]
            marker = self.markers[i % len(self.markers)]
            line_style = self.Line_style[i % len(self.Line_style)]
            ax.plot(
                self.X, y, color=color, linestyle=line_style,
                marker=marker, markersize=12,
                markerfacecolor='none', markeredgewidth=3,
                markeredgecolor=color, linewidth=3,
                label=self.Desc[i]
            )

        ax.set_xlabel(self.XL, fontsize=30, fontweight='bold')
        ax.set_ylabel(self.YL, fontsize=30, fontweight='bold')
        ax.legend(
            fontsize=20, loc='upper left', frameon=True,
            framealpha=0.9, edgecolor='gray'
        )
        ax.grid(linestyle='--', alpha=0.7, linewidth=0.8)

        if y_max is None:
            y_max = max([max(y) for y in self.Y])
        ax.set_ylim(0, y_max)

        if x_tight:
            ax.set_xlim(min(self.X) - 0.1, max(self.X) + 0.1)

        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax.tick_params(axis='both', labelsize=25)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        if inset_zoom:
            # FIX: inset rectangle is in parent-axis coordinates, therefore it
            # cannot extend outside the main plotting box.
            # [left, bottom, width, height] are fractions of the main axes.
            axins = ax.inset_axes([0.35, 0.36, 0.58, 0.46])

            for i, y in enumerate(self.Y):
                color = self.colors[i % len(self.colors)]
                marker = self.markers[i % len(self.markers)]
                line_style = self.Line_style[i % len(self.Line_style)]
                axins.plot(
                    self.X, y, color=color, linestyle=line_style,
                    marker=marker, markersize=5,
                    markerfacecolor='none', markeredgewidth=1.5,
                    markeredgecolor=color, linewidth=1.7,
                    clip_on=True
                )

            # Keep the original zoom rule: alpha plots zoom over 0.2 <= x < 1.
            zoom_start = 0.2
            x_zoom = [x for x in self.X if x >= zoom_start and x < 1]

            if len(x_zoom) >= 2:
                x1, x2 = x_zoom[0], x_zoom[-1]
                axins.set_xlim(x1, x2)

                y_vals = [
                    y[ix]
                    for y in self.Y
                    for ix, x in enumerate(self.X)
                    if x1 <= x <= x2
                ]
                if y_vals:
                    y_min = float(min(y_vals))
                    y_max_zoom = float(max(y_vals))
                    span = y_max_zoom - y_min
                    # Add a small vertical margin so markers/lines do not sit
                    # directly on the inset border.
                    pad = 0.08 * span if span > 0 else max(abs(y_min) * 0.02, 1e-6)
                    axins.set_ylim(y_min - pad, y_max_zoom + pad)

            axins.grid(linestyle='--', alpha=0.35, linewidth=0.6)
            axins.tick_params(axis='both', labelsize=10)
            for label in axins.get_xticklabels() + axins.get_yticklabels():
                label.set_fontweight('bold')

            # Make the inset box visually distinct without connector lines.
            axins.patch.set_alpha(0.97)
            axins.set_zorder(5)

            # IMPORTANT: intentionally no mark_inset(...) call here.  The old
            # connector artists were the source of the long gray diagonal
            # lines extending beyond the plot.

        plt.tight_layout()
        plt.savefig(self.name, format='png', dpi=600)
        plt.show()


def fun(y, x):
    a1 = 1 - x[0] / 6.3
    a2 = 1 - x[1] / 7.6
    b1 = 1000 * (1 - a1) / y[0]
    b2 = 1000 * (1 - a2) / y[1]
    return [a1, a2], [b1, b2]
