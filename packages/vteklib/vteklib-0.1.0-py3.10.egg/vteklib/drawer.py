import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from vteklib.plot_data import PlotData

markers = ['o', 'v', '.', '^']

colors = ['black', 'grey', 'red', 'blue']


class Drawer:
    def __init__(self):
        plt.style.use('/Users/new/PycharmProjects/vteklib/vteklib/vtek_style.mplstyle')
        self.figures = []
        self.subplots: list[matplotlib.figure.Figure] = []

    def add_figure(self,
                   ud: PlotData,
                   errors: bool = False,
                   fill_between: bool = False,
                   connect_pts: bool = False):
        fig = plt.figure(figsize=[9.6, 7.2])
        ax = fig.add_subplot()
        fig.set(facecolor='white')
        self.add_subplot_to_fig(ax,
                                ud,
                                errors=errors,
                                fill_between=fill_between,
                                connect_pts=connect_pts)
        self.figures.append(fig)
        return ax

    def add_subplot_to_fig(self,
                           ax,
                           ud: PlotData,
                           errors: bool = False,
                           fill_between: bool = False,
                           connect_pts: bool = False
                           ):
        ax.grid()
        ax.set_title(ud.title)
        ax.set_xlabel(ud.x_name)
        ax.set_ylabel(ud.y_name)
        ax.scatter(ud.df[ud.x_name],
                   ud.df[ud.y_name],
                   marker=markers[len(self.subplots)],
                   s=50,
                   c=colors[len(self.subplots)],
                   label=ud.label,
                   zorder=3)
        if connect_pts:
            ax.plot(ud.df[ud.x_name],
                    ud.df[ud.y_name],
                    linestyle='-',
                    linewidth=2.5,
                    c=colors[len(self.subplots)],
                    zorder=2)
        if errors:
            ax.errorbar(ud.df[ud.x_name],
                        ud.df[ud.y_name],
                        xerr=ud.df['x_error'],
                        yerr=ud.df['y_error'],
                        ls='none',
                        capsize=2,
                        elinewidth=1,
                        capthick=1,
                        c=colors[len(self.subplots)],
                        zorder=3
                        )
        if ud.approximated:
            ax.plot(ud.df[ud.x_name],
                    ud.df[ud.approx_col_name],
                    linestyle='-',
                    linewidth=2.5,
                    c=colors[len(self.subplots)],
                    zorder=2
                    )
            if fill_between:
                ymin, ymax = ax.get_ylim()
                integral = np.trapz(ud.df[ud.x_name], ud.df[ud.y_name])
                print(integral)
                ax.fill_between(ud.df[ud.x_name],
                                ud.df[ud.approx_col_name],
                                color='gray',
                                label=f"integral={abs(integral)}",
                                zorder=1)
                ax.set_ylim(ymin, ymax)
        if ud.theoretical:
            ax.plot(ud.df['x_theoretical'], ud.df['y_theoretical'],
                    linestyle='-',
                    linewidth=2.5,
                    c=colors[len(self.subplots)],
                    zorder=2
                    )
        self.subplots.append(ax)
        return ax

    def save(self, filename):
        pp = PdfPages(filename)
        for fig in self.figures:
            fig.savefig(pp, format='pdf')
        pp.close()

    def save_pic(self, name):
        plt.legend()
        for i, fig in enumerate(self.figures):
            fig.savefig(f"{name}_{i}.png")
            plt.close(fig)
