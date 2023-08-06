# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:27:31 2016

@author: lockhart
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


# *****************************************************************************
# Fundametal plotting class to be used by all the other plotting functions
# *****************************************************************************
class Grp_2D:
    """
    Class for printing 2D plots in linear and semilog (y) scale with the proper
    formatting for printing or to put directly in slides.

    Parameters
    ----------
    x: list of np.array[]
        Contain the values to be used for the x scale of the figure. The
        dimenssion of the vector array have to be the same of the data for
        the y axis. The input needs to be a list of 1D np.array.

    y: list of np.array[]
        Values of for the y axis of the graph. It has to be of the same
        dimensions of the x scale vectors.

    ox_th: float
        Thickness of the gate oxide in nanometers.

    k_val: float
        Value of the relative permittivity (k) of the the gate dielectric.

    style: string
        Use to choose the type of plot required. The value can be 'log' for
        a graph with the y axis in log scale or 'lin' for a graph with both
        axis in linear scale.

    eng_units: Boolean
        Use to choose if the Y axis has to use scienfic notation or engineering
        style notation (f, p, n, µ or m). The values can be True or False.

    y_prec: integer
        Amount of digits after the decimal point to be displayed in case the
        the y axis ticks have values different to 0 after the decimal point.

    x_prec: integer
        Amount of digits after the decimal point to be displayed in case the
        the x axis ticks have values different to 0 after the decimal point.

    d_prec: integer
        Amount of digits after the decimal point to be displayed in case the
        the d axis ticks have values different to 0 after the decimal point.

    units: list of string
        List with 3 strings for defining the units for the X, y and x upper
        axis.

    col: list of string
        List of string for defining the color and the symbol used for ploting
        the data. For defining normally a normal matlab string can be used
        like color blue is 'b' and if square is required then 's' have to be
        used, if 'bs' is used then the line is blue and with square.

    legend: list of tring
        List with string to for the legend of each of the graphs.

    linewidth: float
        Width of the line to be used for ploting.

    title: string
        String with the title of the graph.

    y_label: string
        String with the label of the y axis.

    x_label: string
        String with the label of the x axis.
    
    d_label: string
        String for the label of the top axis

    cmnt_1: string
        String for the comment of the first line of comment.

    cmnt_2: string
        String for the comment of the second line of comment.

    cmnt_3: string
        String for the comment of the third line of comment.

    D_Top_Axis: Boolean
        Used for selecting whether or not to print the values of the
        displacement field using hte equation D = 3.9*Vgs/th(nm). This only
        needed for the graphs where the x axis is Vgs.

    log_skip : int
        Specify how many tick labels to skip when using log scale graphics.
        By default the value is 1 thus it will skip one 1K - 100K (not 10K).

    dx_max (dy_max) : float
        To specify and additional increase for the x (y) max limit. it must be
        in the same units of the x (y) axis. It can be negative.

    dx_min (dy_min) : float
        To specify and additional increase for the x (y) min limit. it must be
        in the same units of the x (y) axis. It can be negative.
    
    x_limits : list
        list of floats with the limiting axis values for the graphs, if value
        is "" (default) it will chose the limits automatically. [min_x, max_x]
    
    y_limits : list
        list of floats with the limiting axis values for the graphs, if value
        is "" (default) it will chose the limits automatically. [min_y, max_y]
    
    plot: bool
        To choose if the graph have to be plot or not, by default it is plot.

    Attributes
    ----------
    (All the parameters are also attribute)

    title_font: dictionary
        Used for defining font, size, color, weight and verticalalignment.

    axis_font: dictionary
        Used for defining the properties of all the axis.

    comment_font: dictionary
        For defining font for the comments.

    ticks_text_size: float
        For defining the text size of the values of the ticks.

    border_width: float
        Thickness of the border of the figure.

    fig_size: tuple
        Tuple with the dimensions (width, height) in inches.

    logVals: tuple
        tuple with the units that can be used for the axis when semilog type
        is selected.

    EngUnitLog: Dictionary
        For setting the values used in the y axis when the axis is in log and
        with engineering units.

    EngUnits: Dictionary
        Convertion for engineering units for the linear regime.

    eng_units_bool: Boolean
        Flag used to select whether or not to plot engineering unist for the y
        axis.

    log_skip : int
        Specify how many tick labels to skip when using log scale graphics.
        By default the value is 1 thus it will skip one 1K - 100K (not 10K).

    dx_max (dy_max) : float
        To specify and additional increase for the x (y) max limit. it must be
        in the same units of the x (y) axis. It can be negative.

    dx_min (dy_min) : float
        To specify and additional increase for the x (y) min limit. it must be
        in the same units of the x (y) axis. It can be negative.

    Methods
    -------

    plot():
        re-plot the figure again if any of the variable has been changed. This
        method is run once when an object is instanciated.

    """
    def __init__(self, x, y, ox_th, k_val, style='log', eng_units=True,
                 y_prec=2, x_prec=2, d_prec=2, units=["V", "A", "V/nm"],
                 col=[''], legend=[""],
                 linewidth=2, title="", y_label="", x_label="", d_label="D",
                 cmmt_1="", cmmt_2="", cmmt_3="", D_Top_Axis=True,
                 log_skip=1, dx_min=0, dx_max=0, dy_min=0, dy_max=0,
                 x_limits=["",""], y_limits=["",""], x_cmt_lin = -7,
                 x_cmt_log = -12, y_cmt_lin = 4, y_cmt_log = -10,
                 plot=True):

        # Set color procession in case color is not specified.
        if col[0] == '':
            self.col = ['b', 'r', 'k', 'g', 'c', 'm', 'y']
        else:
            self.col = col

        # Set the font dictionaries (for plot title and axis titles)
        self.title_font = {'fontname': 'Arial', 'size': '14', 'color': 'black',
                           'weight': 'normal', 'verticalalignment': 'bottom'}
        self.lines=[]
        # Bottom vertical alignment for more space

        self.axis_font = {'fontname': 'Arial', 'size': '14'}
        self.comment_font = {'fontname': 'Arial', 'size': '12'}
        self.ticks_text_size = 12

        self.border_width = 2
        self.fig_size = (6, 5)
        
        self.x_limits = x_limits
        self.y_limits = y_limits

        self.D_Top_Axis = D_Top_Axis
        self.title = title
        self.y_label = y_label
        self.x_label = x_label
        self.d_label = d_label
        self.dx_max = dx_max
        self.dx_min = dx_min
        self.dy_max = dy_max
        self.dy_min = dy_min
        self.cmmt_1 = cmmt_1
        self.cmmt_2 = cmmt_2
        self.cmmt_3 = cmmt_3
        
        self.x_cmt_lin = x_cmt_lin
        self.x_cmt_log = x_cmt_log
        
        self.y_cmt_lin = y_cmt_lin
        self.y_cmt_log = y_cmt_log
        
        
        self.x = x
        self.y = y
        
        listwidth = []
        if not(type(linewidth) == list):
            for index in range(len(self.x)):
                listwidth.append(linewidth)
            linewidth = listwidth
        
        self.linewidth = linewidth
        self.d_prec = d_prec
        self.x_prec = x_prec
        self.y_prec = y_prec

        self.units = units
        self.ox_th = ox_th
        self.k_val = k_val
        self.style = style
        self.legend = legend
        self.log_skip = log_skip

        self.logVals = (1e-15, 10e-15, 100e-15, 1e-12, 10e-12, 100e-12,
                        1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3,
                        1e0, 10e0, 100e0, 1e3, 10e3, 100e3,
                        1e6, 10e6, 100e6, 1e9, 10e9, 100e9,
                        1e12, 10e12, 100e12)

        self.EngUnitLog = {1e-15: '1f', 10e-15: '10f', 100e-15: '100f',
                           1e-12: '1p', 10e-12: '10p', 100e-12: '100p',
                           1e-9: '1n', 10e-9: '10n', 100e-9: '100n',
                           1e-6: '1µ', 10e-6: '10µ', 100e-6: '100µ',
                           1e-3: '1m', 10e-3: '10m', 100e-3: '100m',
                           1e0: '1', 10e0: '10', 100e0: '100',
                           1e3: '1k', 10e3: '10k', 100e3: '100k',
                           1e6: '1M', 10e6: '10M', 100e6: '100M',
                           1e9: '1G', 10e9: '10G', 100e9: '100G',
                           1e12: '1T', 10e12: '10T', 100e12: '100T'}

        self.EngUnit = {1e-15: 'f', 1e-12: 'p', 1e-9: 'n', 1e-6: 'µ',
                        1e-3: 'm', 1e0: '', 1e3: 'k', 1e6: 'M', 1e9: 'G',
                        1e12: 'T'}

        self.linVals = (1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e0, 1e3, 1e6, 1e9,
                        1e12)

        self.eng_units_bool = eng_units
        
        if plot:
            self.plot()
        

    def plot(self):

        # Setting figure size and getting the first axis handlers
        self.fig = plt.figure(figsize=self.fig_size)
        self.ax = self.fig.add_subplot(111)
        ax = self.ax
        self.fig.patch.set_facecolor('none')

        # ---------------------------------------------------------------------
        # Starting for ploting in the case of log graph
        # ---------------------------------------------------------------------

        if (self.style == "log"):

            # Obtantion axis limits for the case of log plot
            min_y = np.amin(np.abs(self.y[0]))
            min_x = np.amin(self.x[0])

            max_y = np.amax(np.abs(self.y[0]))
            max_x = np.amax(self.x[0])

            for i_plt in range(len(self.x)):
                val_y = np.amin(np.abs(self.y[i_plt]))
                val_x = np.amin(self.x[i_plt])

                if min_y > val_y:
                    min_y = val_y

                if max_y < val_y:
                    max_y = val_y

                if min_x > val_x:
                    min_x = val_x

                if max_x < val_x:
                    max_x = val_x

            min_y = min_y + self.dy_min
            max_y = max_y + self.dy_max

            min_x = min_x + self.dx_min
            max_x = max_x + self.dx_max
        
            if self.x_limits[0] == "":
                min_x = min_x
            else:
                min_x = self.x_limits[0]
                
            if self.x_limits[1] == "":
                max_x = max_x
            else:
                max_x = self.x_limits[1]

            if self.y_limits[0] == "":
                min_y = (min_y)/10
            else:
                min_y = self.y_limits[0]

            if self.y_limits[1] == "":
                max_y = (max_y)*10
            else:
                max_y = self.y_limits[1]
            
            y_lim = [min_y, max_y]
            x_lim = [min_x, max_x]

            ax.set_ylim(y_lim)
            ax.set_xlim(x_lim)

            # -------------------------------------------------------------
            # For plotting the data

            for i_plt in range(len(self.x)):
                if self.legend[0] == "":
                    self.lines.append(plt.semilogy(self.x[i_plt], self.y[i_plt],
                                                   self.col[i_plt], linewidth=self.linewidth[i_plt],
                                                   markeredgewidth = 2,
                                                   markeredgecolor = 'k',
                                                   markersize = self.linewidth[i_plt],
                                                   markerfacecolor=self.col[i_plt][-1]))
                else:
                    self.lines.append(plt.semilogy(self.x[i_plt], self.y[i_plt],
                                                   self.col[i_plt], linewidth=self.linewidth[i_plt],
                                                   markeredgewidth = 1,
                                                   markersize = self.linewidth[i_plt],
                                                   markeredgecolor = 'k',
                                                   label=self.legend[i_plt],
                                                   markerfacecolor=self.col[i_plt][-1]))

            # Set graph title and labels for x and ID axes
            if self.D_Top_Axis:
                plt.title(str(self.title), y=1.1, **self.title_font)
            else:
                plt.title(str(self.title), y=1, **self.title_font)
                
            plt.xlabel(self.x_label+r" $({0})$".format(self.units[0]),
                       **self.axis_font)
            plt.ylabel(self.y_label+r" $({0})$".format(self.units[1]),
                       **self.axis_font)

            # for setting the tick label font for the x and Id axes
            for label in (ax.get_xticklabels() + ax.get_yticklabels()):
                label.set_fontname('Arial')
                label.set_fontsize(self.ticks_text_size)
                label.set_color('k')

            # For setting ticks line width
            ticklines = ax.get_xticklines() + ax.get_yticklines()

            for line in ticklines:
                line.set_linewidth(3)

            # For setting the ticks position for x
            x_ticks = np.linspace(x_lim[0], x_lim[1], 6).tolist()

            # To choose if digits after the point are required or not.
            dig = 0
            for val in x_ticks:
                if val % 1 != 0:
                    dig = self.x_prec

            # For plotting fixed digits after decimal point in x labels
            xticks_labels = []
            for val in x_ticks:
                xticks_labels.append('{:.{prec}f}'.format(val, prec=dig))

            # For setting the ticks position for Y
            y_ticks = []
            red_logVals = []

            index = np.arange(1, len(self.logVals), self.log_skip+1)  # ticks
            self.index = index

            for val in index:
                red_logVals.append(self.logVals[val])

            for val in red_logVals:
                if (val > y_lim[0]) and (val < y_lim[1]):
                    y_ticks.append(val)  # Only values from logVals selected

            # For plotting engineering labels for y axis
            if self.eng_units_bool is True:
                yticks_labels = []

                for val in y_ticks:
                    yticks_labels.append(self.EngUnitLog[val])
            else:
                yticks_labels = y_ticks

            plt.yticks(y_ticks, yticks_labels)
            plt.xticks(x_ticks, xticks_labels)

            # Setting y axis nicely in scientific format
            if self.eng_units_bool is False:
                ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

            # For plotting the grid
            plt.grid(b=True, which='major', color='tab:gray', linestyle='--')

            # For setting the thicknes of the borders and borders visible
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
            ax.spines['left'].set_visible(True)

            l_width = self.border_width

            ax.spines['top'].set_linewidth(l_width)
            ax.spines['right'].set_linewidth(l_width)
            ax.spines['bottom'].set_linewidth(l_width)
            ax.spines['left'].set_linewidth(l_width)

            # -----------------------------------------------------------------
            # Comments plotting
            index = len(x_ticks)
            index_x = index*2//4
            index = len(y_ticks)
            index_y = index*2//6

            x_margin = x_ticks[index_x]+(max_x-x_ticks[index_x])/self.x_cmt_log

            final_cmmt = str(self.cmmt_1 + "\n" + self.cmmt_2 + "\n" +
                             self.cmmt_3)

            plt.text(x_margin, y_ticks[index_y]/self.y_cmt_log, final_cmmt,
                     self.comment_font)

            # Legend set up
            if self.legend[0]!="" :
                plt.legend(loc='upper left')

        # ---------------------------------------------------------------------
        # Starting for ploting in the case of linear graph
        # ---------------------------------------------------------------------
        elif self.style == "lin":

            # Obtantion axis limits for the case of linear plot
            min_y = np.amin(self.y[0])
            min_x = np.amin(self.x[0])

            max_y = np.amax(self.y[0])
            max_x = np.amax(self.x[0])

            for i_plt in range(len(self.x)):
                val_y = np.amin(np.abs(self.y[i_plt]))
                val_x = np.amin(self.x[i_plt])

                if min_y > val_y:
                    min_y = val_y

                if max_y < val_y:
                    max_y = val_y

                if min_x > val_x:
                    min_x = val_x

                if max_x < val_x:
                    max_x = val_x

            min_y = min_y + self.dy_min
            max_y = max_y + self.dy_max

            min_x = min_x + self.dx_min
            max_x = max_x + self.dx_max

            if self.x_limits[0] == "":
                min_x = min_x
            else:
                min_x = self.x_limits[0]
                
            if self.x_limits[1] == "":
                max_x = max_x
            else:
                max_x = self.x_limits[1]

            if self.y_limits[0] == "":
                min_y = min_y-(0.1*max_y)
            else:
                min_y = self.y_limits[0]

            if self.y_limits[1] == "":
                max_y = max_y+(0.1*max_y)
            else:
                max_y = self.y_limits[1]

            y_lim = [min_y, max_y]
            x_lim = [min_x, max_x]

            ax.set_ylim(y_lim)
            ax.set_xlim(x_lim)

            # -------------------------------------------------------------
            # For plotting the data

            for i_plt in range(len(self.x)):
                if self.legend[0] == "":
                    plt.plot(self.x[i_plt], self.y[i_plt],
                             self.col[i_plt], linewidth=self.linewidth[i_plt],
                             markeredgewidth = 2,
                             markeredgecolor = 'k',
                             markersize = self.linewidth[i_plt],
                             markerfacecolor=self.col[i_plt][-1])
                else:
                    plt.plot(self.x[i_plt], self.y[i_plt],
                             self.col[i_plt], linewidth=self.linewidth[i_plt],
                             markeredgewidth = 1,
                             markersize = self.linewidth[i_plt],
                             markeredgecolor = 'k',
                             label=self.legend[i_plt],
                             markerfacecolor=self.col[i_plt][-1])

            # Set graph title and labels for x and ID axes
            if self.D_Top_Axis:
                plt.title(str(self.title), y=1.1, **self.title_font)
            else:
                plt.title(str(self.title), y=1, **self.title_font)
            plt.xlabel(self.x_label+r" $({0})$".format(self.units[0]),
                       **self.axis_font)
            plt.ylabel(self.y_label+r" $({0})$".format(self.units[1]),
                       **self.axis_font)

            # for setting the tick label font for the x and Id axes
            for label in (ax.get_xticklabels() + ax.get_yticklabels()):
                label.set_fontname('Arial')
                label.set_fontsize(self.ticks_text_size)
                label.set_color('k')

            # For setting ticks line width
            ticklines = ax.get_xticklines() + ax.get_yticklines()

            for line in ticklines:
                line.set_linewidth(3)

            # For setting the ticks position for x
            x_ticks = np.linspace(min_x, max_x, 6).tolist()

            # To choose if digits after the point are required or not.
            dig = 0
            for val in x_ticks:
                if val % 1 != 0:
                    dig = self.x_prec

            # For plotting fixed digits after decimal point in x labels
            xticks_labels = []
            for val in x_ticks:
                xticks_labels.append('{:.{prec}f}'.format(val, prec=dig))

            # For setting the ticks position for Y
            y_ticks = np.linspace(min_y, max_y, 6).tolist()
            self.y_ticks = y_ticks

            # To choose if digits after the point are required or not.
            dig = 0
            for val in y_ticks:
                if val % 1 != 0:
                    dig = self.y_prec

            # For converting to engineering units

            values = []
            units = []
            self.yticks = y_ticks
            for i_tick in y_ticks:
                if i_tick == 0.00:
                    units.append("")
                    values.append(0)
                    continue
                for key in self.linVals:
                    val = i_tick/key
                    if np.abs(val) < 1:
                        break
                    temp_units = self.EngUnit[key]
                    temp_values = val
                units.append(temp_units)
                values.append(temp_values)

            for i_val in range(len(values)):
                if (values[i_val] == 0) and (i_val+1 < len(units)):
                    units[i_val] = units[i_val+1]

                if (values[i_val] == 0) and (i_val+1 > len(units)):
                    units[i_val] = units[i_val+1]

            # for deciding wether or not to put digits after the point in eng
            dig_eng = 0
            for val in values:
                if val % 1 != 0:
                    dig_eng = self.y_prec

            # Definition of official labels for y axis
            yticks_labels = []

            if self.eng_units_bool is True:
                for i_val in range(0, len(values)):
                    string = '{:.{prec}f}{unit}'.format(values[i_val],
                                                        prec=dig_eng,
                                                        unit=units[i_val])
                    yticks_labels.append(string)
            else:
                for val in y_ticks:
                    yticks_labels.append('{0}'.format(val))

            # For plotting official labels
            plt.yticks(y_ticks, yticks_labels)
            plt.xticks(x_ticks, xticks_labels)

            # Setting y axis nicely in scientific format
            if self.eng_units_bool is False:
                ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

            # For plotting the grid
            plt.grid(b=True, which='major', color='tab:gray', linestyle='--')

            # For setting the thicknes of the borders and borders visible
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
            ax.spines['left'].set_visible(True)

            l_width = self.border_width

            ax.spines['top'].set_linewidth(l_width)
            ax.spines['right'].set_linewidth(l_width)
            ax.spines['bottom'].set_linewidth(l_width)
            ax.spines['left'].set_linewidth(l_width)

            # -----------------------------------------------------------------
            # Comments plotting
            index = len(x_ticks)
            index_x = index*2//4
            index = len(y_ticks)
            index_y = 1

            delta_y = y_ticks[index_y] - y_ticks[index_y-1]
            space = delta_y/4.4

            x_margin = x_ticks[index_x]+(max_x-x_ticks[index_x])/self.x_cmt_lin

            final_cmmt = str(self.cmmt_1 + "\n" + self.cmmt_2 + "\n" +
                             self.cmmt_3)

            plt.text(x_margin,y_ticks[index_y]-self.y_cmt_lin*space,final_cmmt,
                     self.comment_font)

            # Legend set up
            if self.legend != [""]:
                plt.legend(loc='upper left')

        # -----------------------------------------------------------------
        # For setting top x axis for displaying the D = x/ox_th * K
        if self.D_Top_Axis is True:
            ax_2 = ax.twiny()
            ax_2.set_xlim(ax.get_xlim())
            ax_2.set_xticks(x_ticks)
            D = [x/self.ox_th*self.k_val for x in x_ticks]
            D_format = []

            for i in range(len(D)):
                D_format.append('{:.{prec}f}'.format(D[i],
                                prec=self.d_prec))

            ax_2.set_xticklabels(D_format)
            ax_2.set_xlabel(self.d_label + r'$\,({0})$'.format(self.units[2]),
                            self.axis_font)

            for label in (ax_2.get_xticklabels() + ax_2.get_yticklabels()):
                label.set_fontname('Arial')
                label.set_fontsize(self.ticks_text_size)

        self.fig.tight_layout()
        plt.show()
        

# *****************************************************************************
# Function for ploting surface plot
# *****************************************************************************
class Grp_surface:
    """
    Class for plotting surfaces
    """
    def __init__(self, x, y, z,
                 style='lin', eng_units=True, y_prec=2, x_prec=2, z_prec=2,
                 units=["um", "eV", "A/cm^2"], clrMap="rainbow",
                 linewidth=2, title="", y_label="", x_label="", z_label="",
                 cmmt_1="", cmmt_2="", cmmt_3="", log_skip=1, 
                 x_limits=["",""], y_limits=["",""], color_limits = ["", ""],
                 x_cmt_lin = -7, x_cmt_log = -12, y_cmt_lin = 4,
                 y_cmt_log = -10, shading = "gouraud", contour=True,
                 amnt_x_ticks=6, amnt_contour=8, amnt_zticks=8):
        
        self.amnt_x_ticks = amnt_x_ticks
        self.amnt_contour = amnt_contour
        self.amnt_zticks = amnt_zticks
        self.x = x
        self.y = y
        self.z = np.ma.masked_invalid(z)
        self.style = style
        self.units = units
        self.clrMap = clrMap
        self.linewidth = linewidth
        self.title = title
        self.y_label = y_label
        self.x_label = x_label
        self.z_label = z_label

        self.vmin = color_limits[0]
        self.vmax = color_limits[1]
        self.contour = contour
        self.shading = shading
        
        self.x_limits = x_limits
        self.y_limits = y_limits
        
        # Set the font dictionaries (for plot title and axis titles)
        #----------------------------------------------------------------------
        self.title_font = {'fontname': 'Arial', 'size': '14', 'color': 'black',
                           'weight': 'normal', 'verticalalignment': 'bottom'}
        #----------------------------------------------------------------------
        
        #Formating of the graph
        #----------------------------------------------------------------------
        self.axis_font = {'fontname': 'Arial', 'size': '14'}
        self.comment_font = {'fontname': 'Arial', 'size': '12'}
        self.ticks_text_size = 12

        self.border_width = 2
        self.fig_size = (6, 5)
        self.z_prec = z_prec
        self.x_prec = x_prec
        self.y_prec = y_prec

        self.units = units
        self.log_skip = log_skip

        self.logVals = (1e-15, 10e-15, 100e-15, 1e-12, 10e-12, 100e-12,
                        1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3,
                        1e0, 10e0, 100e0, 1e3, 10e3, 100e3,
                        1e6, 10e6, 100e6, 1e9, 10e9, 100e9,
                        1e12, 10e12, 100e12)

        self.EngUnitLog = {1e-15: '1f', 10e-15: '10f', 100e-15: '100f',
                           1e-12: '1p', 10e-12: '10p', 100e-12: '100p',
                           1e-9: '1n', 10e-9: '10n', 100e-9: '100n',
                           1e-6: '1µ', 10e-6: '10µ', 100e-6: '100µ',
                           1e-3: '1m', 10e-3: '10m', 100e-3: '100m',
                           1e0: '1', 10e0: '10', 100e0: '100',
                           1e3: '1k', 10e3: '10k', 100e3: '100k',
                           1e6: '1M', 10e6: '10M', 100e6: '100M',
                           1e9: '1G', 10e9: '10G', 100e9: '100G',
                           1e12: '1T', 10e12: '10T', 100e12: '100T'}

        self.EngUnit = {1e-15: 'f', 1e-12: 'p', 1e-9: 'n', 1e-6: 'µ',
                        1e-3: 'm', 1e0: '', 1e3: 'k', 1e6: 'M', 1e9: 'G',
                        1e12: 'T'}

        self.linVals = (1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e0, 1e3, 1e6, 1e9,
                        1e12)

        self.eng_units_bool = eng_units
        #----------------------------------------------------------------------
        
                
        self.plot_im()
        
    def plot_im(self):
        
        # Setting figure size and getting the first axis handlers
        self.fig = plt.figure(figsize=self.fig_size)
        self.ax = self.fig.add_subplot(111)
        ax = self.ax
        self.fig.patch.set_facecolor('none')
        
        
        #Plotting surface data
        #----------------------------------------------------------------------
        
        #Defining limits for x and y axis
        
        # Obtantion axis limits for the case of linear plot
        min_y = np.amin(self.y)
        min_x = np.amin(self.x)

        max_y = np.amax(self.y)
        max_x = np.amax(self.x)
        
        if self.x_limits[0] == "":
            min_x = min_x
        else:
            min_x = self.x_limits[0]
            
        if self.x_limits[1] == "":
            max_x = max_x
        else:
            max_x = self.x_limits[1]

        if self.y_limits[0] == "":
            min_y = min_y
        else:
            min_y = self.y_limits[0]

        if self.y_limits[1] == "":
            max_y = max_y
        else:
            max_y = self.y_limits[1]
        
        y_lim = [min_y, max_y]
        x_lim = [min_x, max_x]

        #ax.set_ylim(y_lim)
        #ax.set_xlim(x_lim)
        
        
        
        #defining the gama of values to be covered by the colors
        if self.vmax == "":
            self.vmax = self.z.max()
        
        if self.vmin == "":
            self.vmin = self.z.min()
        
        #Creating plot
        self.im = plt.pcolormesh(self.x, self.y, self.z, vmin=self.vmin,
                                 vmax=self.vmax,
                                 cmap = plt.get_cmap(self.clrMap),
                                 shading = self.shading,
                                 antialiased = True)
        
        # Set graph title and labels for x and ID axes
        plt.title(self.title, **self.title_font)
        plt.xlabel(self.x_label+r" $({0})$".format(self.units[0]),
                   **self.axis_font)
        plt.ylabel(self.y_label+r" $({0})$".format(self.units[1]),
                   **self.axis_font)

        # for setting the tick label font for the x and Id axes
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(self.ticks_text_size)
            label.set_color('k')
        
        # For setting ticks line width
        ticklines = ax.get_xticklines() + ax.get_yticklines()

        for line in ticklines:
            line.set_linewidth(3)

        # For setting the ticks position for x
        x_ticks = np.linspace(min_x, max_x, self.amnt_x_ticks).tolist()

        # To choose if digits after the point are required or not.
        dig = 0
        for val in x_ticks:
            if val % 1 != 0:
                dig = self.x_prec

        # For plotting fixed digits after decimal point in x labels
        xticks_labels = []
        for val in x_ticks:
            xticks_labels.append('{:.{prec}f}'.format(val, prec=dig))

        # For setting the ticks position for Y
        y_ticks = np.linspace(round(min_y), max_y, 6).tolist()
        self.y_ticks = y_ticks

        # To choose if digits after the point are required or not.
        dig = 0
        for val in y_ticks:
            if val % 1 != 0:
                dig = self.y_prec        
        
        # For converting to engineering units

        values = []
        units = []
        self.yticks = y_ticks
        for i_tick in y_ticks:
            if i_tick == 0.00:
                units.append("")
                values.append(0)
                continue
            for key in self.linVals:
                val = i_tick/key
                if np.abs(val) < 1:
                    break
                temp_units = self.EngUnit[key]
                temp_values = val
            units.append(temp_units)
            values.append(temp_values)

        for i_val in range(len(values)):
            if (values[i_val] == 0) and (i_val+1 < len(units)):
                units[i_val] = units[i_val+1]

            if (values[i_val] == 0) and (i_val+1 > len(units)):
                units[i_val] = units[i_val+1]

        # for deciding wether or not to put digits after the point in eng
        dig_eng = 0
        for val in values:
            if val % 1 != 0:
                dig_eng = self.y_prec

        # Definition of official labels for y axis
        yticks_labels = []

        if self.eng_units_bool is True:
            for i_val in range(0, len(values)):
                string = '{:.{prec}f}{unit}'.format(values[i_val],
                                                    prec=dig_eng,
                                                    unit=units[i_val])
                yticks_labels.append(string)
        else:
            for val in y_ticks:
                yticks_labels.append('{0}'.format(val))

        # For plotting official labels
        plt.yticks(y_ticks, yticks_labels)
        plt.xticks(x_ticks, xticks_labels)

        # Setting y axis nicely in scientific format
        if self.eng_units_bool is False:
            sFormat = '%.{0}f'.format(self.y_prec)
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter(sFormat))

        # For plotting the grid
        plt.grid(b=True, which='major', color='#5E5962', linestyle='--')

        # For setting the thicknes of the borders and borders visible
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)

        l_width = self.border_width

        ax.spines['top'].set_linewidth(l_width)
        ax.spines['right'].set_linewidth(l_width)
        ax.spines['bottom'].set_linewidth(l_width)
        ax.spines['left'].set_linewidth(l_width)

        # ---------------------------------------------------------------------    
        

        #Creating color bar
        self.cb = self.fig.colorbar(self.im)
        self.cb.outline.set_linewidth(l_width)
        self.cb.set_label(self.z_label+r" ${0}$".format(self.units[2]),
                          **self.axis_font)

        if self.contour:
            self.cnt = plt.contour(self.x, self.y, self.z, self.amnt_contour,
                                   linewidths = self.linewidth, colors = 'k')

            #self.cnt = plt.contour(self.z, vmin=self.vmin, vmax=self.vmax, extent=axis_margins)
            
        #Setting interpolation 
        #if self.inter != "":
            #self.im.set_interpolation(self.inter)
         
# *****************************************************************************
# Function for ploting surface plot
# *****************************************************************************
class Grp_scatter:
    """
    Class for plotting surfaces
    """
    def __init__(self, x, y, z_color, diameter,
                 style='lin', eng_units=True, y_prec=2, x_prec=2, z_prec=2,
                 units=["(V)", "[log_{10}(I_{ON}/I_{OFF})]", "eV", "nm"],
                 clrMap="rainbow", linewidth=2, title="", y_label="",
                 x_label="", z_label="", cmmt_1="", cmmt_2="", cmmt_3="",
                 log_skip=1, 
                 x_limits=["",""], y_limits=["",""], color_limits = ["", ""],
                 x_cmt_lin = -7, x_cmt_log = -12, y_cmt_lin = 4,
                 y_cmt_log = -10, amnt_x_ticks=6, min_area=20,
                 amnt_zticks=8, power=2, amnt_y_ticks=7,
                 alpha=0.5, area_label = "$T_{semi}$", scale_area = 1000):
        
        self.scale_area = scale_area
        self.amnt_x_ticks = amnt_x_ticks
        self.amnt_y_ticks = amnt_y_ticks
        self.min_area = min_area
        self.power_area = power
        self.alpha = alpha
        self.amnt_zticks = amnt_zticks
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.z = np.asarray(z_color)
        self.diameter = np.asarray(diameter)
        self.style = style
        self.units = units
        self.clrMap = clrMap
        self.linewidth = linewidth
        self.title = title
        self.y_label = y_label
        self.x_label = x_label
        self.z_label = z_label
        self.area_label = area_label

        self.vmin = color_limits[0]
        self.vmax = color_limits[1]
        
        self.x_limits = x_limits
        self.y_limits = y_limits
        
        # Set the font dictionaries (for plot title and axis titles)
        #----------------------------------------------------------------------
        self.title_font = {'fontname': 'Arial', 'size': '14', 'color': 'black',
                           'weight': 'normal', 'verticalalignment': 'bottom'}
        #----------------------------------------------------------------------
        
        #Formating of the graph
        #----------------------------------------------------------------------
        self.axis_font = {'fontname': 'Arial', 'size': '14'}
        self.comment_font = {'fontname': 'Arial', 'size': '12'}
        self.ticks_text_size = 12

        self.border_width = 2
        self.fig_size = (6, 5)
        self.z_prec = z_prec
        self.x_prec = x_prec
        self.y_prec = y_prec

        self.units = units
        self.log_skip = log_skip

        self.logVals = (1e-15, 10e-15, 100e-15, 1e-12, 10e-12, 100e-12,
                        1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3,
                        1e0, 10e0, 100e0, 1e3, 10e3, 100e3,
                        1e6, 10e6, 100e6, 1e9, 10e9, 100e9,
                        1e12, 10e12, 100e12)

        self.EngUnitLog = {1e-15: '1f', 10e-15: '10f', 100e-15: '100f',
                           1e-12: '1p', 10e-12: '10p', 100e-12: '100p',
                           1e-9: '1n', 10e-9: '10n', 100e-9: '100n',
                           1e-6: '1µ', 10e-6: '10µ', 100e-6: '100µ',
                           1e-3: '1m', 10e-3: '10m', 100e-3: '100m',
                           1e0: '1', 10e0: '10', 100e0: '100',
                           1e3: '1k', 10e3: '10k', 100e3: '100k',
                           1e6: '1M', 10e6: '10M', 100e6: '100M',
                           1e9: '1G', 10e9: '10G', 100e9: '100G',
                           1e12: '1T', 10e12: '10T', 100e12: '100T'}

        self.EngUnit = {1e-15: 'f', 1e-12: 'p', 1e-9: 'n', 1e-6: 'µ',
                        1e-3: 'm', 1e0: '', 1e3: 'k', 1e6: 'M', 1e9: 'G',
                        1e12: 'T'}

        self.linVals = (1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e0, 1e3, 1e6, 1e9,
                        1e12)

        self.eng_units_bool = eng_units
        #----------------------------------------------------------------------
        
                
        self.plot_im()
        
    def plot_im(self):
        
        # Setting figure size and getting the first axis handlers
        self.fig = plt.figure(figsize=self.fig_size)
        self.ax = self.fig.add_subplot(111)
        ax = self.ax
        self.fig.patch.set_facecolor('none')
        
        
        #Plotting surface data
        #----------------------------------------------------------------------
        
        #Defining limits for x and y axis
        
        # Obtantion axis limits for the case of linear plot
        min_y = np.amin(self.y)
        min_x = np.amin(self.x)

        max_y = np.amax(self.y)
        max_x = np.amax(self.x)
        
        if self.x_limits[0] == "":
            min_x = min_x
        else:
            min_x = self.x_limits[0]
            
        if self.x_limits[1] == "":
            max_x = max_x
        else:
            max_x = self.x_limits[1]

        if self.y_limits[0] == "":
            min_y = min_y
        else:
            min_y = self.y_limits[0]

        if self.y_limits[1] == "":
            max_y = max_y
        else:
            max_y = self.y_limits[1]
        
        y_lim = [min_y, max_y]
        x_lim = [min_x, max_x]

        ax.set_ylim(y_lim)
        ax.set_xlim(x_lim)
        
        
        
        #defining the gama of values to be covered by the colors
        if self.vmax == "":
            self.vmax = self.z.max()
        
        if self.vmin == "":
            self.vmin = self.z.min()
        
        #Creating plot
        
        min_t = self.diameter.min()*self.scale_area #nm
        max_t = self.diameter.max()*self.scale_area #nm
        
        area = (500*self.diameter)**self.power_area
        
        factor = self.min_area/area.min()
        self.area = area*factor
        
        
        self.im = plt.scatter(x=self.x, y=self.y, s=self.area,
                               c=self.z, 
                               cmap = plt.get_cmap(self.clrMap), 
                               alpha=self.alpha)
        
        self.faceColor = self.im.get_facecolors()
        
        #Set legend
        b_idx = area.argmax()
        s_idx = area.argmin()

        
        plt.scatter(x=[self.x[b_idx]], y=[self.y[b_idx]], s=[self.area[b_idx]],
                    c=[self.z[b_idx]],cmap = plt.get_cmap(self.clrMap),
                    label=r'${:.1f}\,$'.format(max_t)+self.units[3],
                    alpha=self.alpha)
        
        plt.scatter(x=[self.x[s_idx]], y=[self.y[s_idx]], s=[self.area[s_idx]],
                    c=[self.z[s_idx]], cmap = plt.get_cmap(self.clrMap),
                    label=r'${:.1f}\,$'.format(min_t)+self.units[3],
                    alpha=self.alpha)
        
        plt.legend(title = self.area_label, loc='lower right')
        
                
        # Set graph title and labels for x and y axes
        plt.title(self.title, **self.title_font)
        plt.xlabel(self.x_label+r" ${0}$".format(self.units[0]),
                   **self.axis_font)
        plt.ylabel(self.y_label+r" ${0}$".format(self.units[1]),
                   **self.axis_font)

        # for setting the tick label font for the x and Id axes
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(self.ticks_text_size)
            label.set_color('k')
        
        # For setting ticks line width
        ticklines = ax.get_xticklines() + ax.get_yticklines()

        for line in ticklines:
            line.set_linewidth(3)

        # For setting the ticks position for x
        x_ticks = np.linspace(min_x, max_x, self.amnt_x_ticks).tolist()

        # To choose if digits after the point are required or not.
        dig = 0
        for val in x_ticks:
            if val % 1 != 0:
                dig = self.x_prec

        # For plotting fixed digits after decimal point in x labels
        xticks_labels = []
        for val in x_ticks:
            xticks_labels.append('{:.{prec}f}'.format(val, prec=dig))

        # For setting the ticks position for Y
        y_ticks = np.linspace(min_y, max_y, self.amnt_y_ticks).tolist()
        self.y_ticks = y_ticks

        # To choose if digits after the point are required or not.
        dig = 0
        for val in y_ticks:
            if val % 1 != 0:
                dig = self.y_prec        
        
        # For converting to engineering units

        values = []
        units = []
        self.yticks = y_ticks
        for i_tick in y_ticks:
            if i_tick == 0.00:
                units.append("")
                values.append(0)
                continue
            for key in self.linVals:
                val = i_tick/key
                if np.abs(val) < 1:
                    break
                temp_units = self.EngUnit[key]
                temp_values = val
            units.append(temp_units)
            values.append(temp_values)

        for i_val in range(len(values)):
            if (values[i_val] == 0) and (i_val+1 < len(units)):
                units[i_val] = units[i_val+1]

            if (values[i_val] == 0) and (i_val+1 > len(units)):
                units[i_val] = units[i_val+1]

        # for deciding wether or not to put digits after the point in eng
        dig_eng = 0
        for val in values:
            if val % 1 != 0:
                dig_eng = self.y_prec

        # Definition of official labels for y axis
        yticks_labels = []

        if self.eng_units_bool is True:
            for i_val in range(0, len(values)):
                string = '{:.{prec}f}{unit}'.format(values[i_val],
                                                    prec=dig_eng,
                                                    unit=units[i_val])
                yticks_labels.append(string)
        else:
            for val in y_ticks:
                yticks_labels.append('{0}'.format(val))

        # For plotting official labels
        plt.yticks(y_ticks, yticks_labels)
        plt.xticks(x_ticks, xticks_labels)

        # Setting y axis nicely in scientific format
        if self.eng_units_bool is False:
            sFormat = '%.{0}f'.format(self.y_prec)
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter(sFormat))

        # For plotting the grid
        plt.grid(b=True, which='major', color='#5E5962', linestyle='--')

        # For setting the thicknes of the borders and borders visible
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)

        l_width = self.border_width

        ax.spines['top'].set_linewidth(l_width)
        ax.spines['right'].set_linewidth(l_width)
        ax.spines['bottom'].set_linewidth(l_width)
        ax.spines['left'].set_linewidth(l_width)

        # ---------------------------------------------------------------------    
        

        #Creating color bar
        self.cb = self.fig.colorbar(self.im)
        self.cb.outline.set_linewidth(l_width)
        self.cb.set_label(self.z_label+r" ${0}$".format(self.units[2]),
                          **self.axis_font)      
    

# *****************************************************************************
# Function for saving a graph in pdf format
# *****************************************************************************


def save(fig, file_name, width=20, height=15, units='cm', format="png"):
    if width != 0:
        if units == 'cm':
            fig.set_size_inches(width/2.54, height/2.54)
        elif units == 'in':
            fig.set_size_inches(width, height)

    fig.tight_layout()
    fig.savefig(fname=file_name, format=format)

# *****************************************************************************
# Function for electrochemistry plots
# *****************************************************************************

#Function for plating CV measurements
#-----------------------------------------------------------------------------
def plotCV(vwc, iw, vwr=[], iw_std=[], ranges=["auto","auto"], style="lin",
           title = "Cyclic Voltammetry Plot", label_x = "Voltage",
           label_y = "Current", units_x="V", units_y = "A", plot=True):
    """
    Function to plot a CV measurement.

    Parameters
    ----------
    vwc : list float
        Value of the potencial of the working eletrode with respect to the
        counter electrode in volts.
    iw : list float
        Value of the current flowing though the working electrode in amperes.
    vwr : list float, optional
        Values of the potential in the working electrode measured with respect
        to the reference electrode. The default is []. In such case Reference
        is not considered.
    ranges : list, optional
        List with the ranges as [["Xmin", "Xmax"'], ["Ymin", "Ymax"]].
        The default is ["auto","auto"].

    Returns
    -------
    fig: handler to the created figure.

    """
    comment = ["", "", ""]

  

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n\n"

    cmt = ""
    units_rh = ""
    cmt2 = ""
    comment[0] = str(cmt + cmt2 + units_rh)

    cmt = ""
    cmt2 = ""
    comment[2] = str(cmt + cmt2 + spaces)

    fig = Grp_2D([vwc],
                 [iw],
                 col=['b'],
                 style=style, eng_units=True,
                 D_Top_Axis=False, log_skip=0,
                 title=title,
                 x_label=label_x,
                 y_label=label_y,
                 cmmt_1=comment[0],
                 cmmt_2=comment[1],
                 cmmt_3=comment[2],
                 legend=[""],
                 ox_th=1, k_val=1,
                 x_prec=2, y_prec=1, d_prec=2,
                 units=[units_x, units_y, "V/nm"],
                 y_limits=["", ""],
                 x_limits=["", ""],
                 plot=plot)

    # Plot triangle in the maximum point of mobility
    # Print the marker in the position where Rsh is minimum
    """
    fig_rh.ax.plot(vgs_vth[i_min_rh], min_rh, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_rh.ax.fill_between(vgs_vth, rh-error, rh+error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)
    
    fig_rh.ax.legend(loc='upper right')
    """
    plt.show()

    return fig
    

def plotSAMP(time, iw, vwr=[], iw_std=[], ranges=["auto","auto"], style="lin",
           title = "Voltage hold", label_x = "Time",
           label_y = "Current", units_x="s", units_y = "A", plot=True):
    """
    Function to plot a CV measurement.

    Parameters
    ----------
    vwc : list float
        Value of the potencial of the working eletrode with respect to the
        counter electrode in volts.
    iw : list float
        Value of the current flowing though the working electrode in amperes.
    vwr : list float, optional
        Values of the potential in the working electrode measured with respect
        to the reference electrode. The default is []. In such case Reference
        is not considered.
    ranges : list, optional
        List with the ranges as [["Xmin", "Xmax"'], ["Ymin", "Ymax"]].
        The default is ["auto","auto"].

    Returns
    -------
    fig: handler to the created figure.

    """
    comment = ["", "", ""]

  

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n\n"

    cmt = ""
    units_rh = ""
    cmt2 = ""
    comment[0] = str(cmt + cmt2 + units_rh)

    cmt = ""
    cmt2 = ""
    comment[2] = str(cmt + cmt2 + spaces)

    fig = Grp_2D([time],
                 [iw],
                 col=['b'],
                 style=style, eng_units=True,
                 D_Top_Axis=False, log_skip=0,
                 title=title,
                 x_label=label_x,
                 y_label=label_y,
                 cmmt_1=comment[0],
                 cmmt_2=comment[1],
                 cmmt_3=comment[2],
                 legend=[""],
                 ox_th=1, k_val=1,
                 x_prec=2, y_prec=1, d_prec=2,
                 units=[units_x, units_y, "V/nm"],
                 y_limits=["", ""],
                 x_limits=["", ""],
                 plot=plot)

    # Plot triangle in the maximum point of mobility
    # Print the marker in the position where Rsh is minimum
    """
    fig_rh.ax.plot(vgs_vth[i_min_rh], min_rh, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_rh.ax.fill_between(vgs_vth, rh-error, rh+error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)
    
    fig_rh.ax.legend(loc='upper right')
    """
    plt.show()

    return fig

# def plotSAMP(vwc, iw, time, vwr=[], ranges=["auto","auto"]):
#     """
#     Function to plot a CV measurement.

#     Parameters
#     ----------
#     vwc : list float
#         Value of the potencial of the working eletrode with respect to the
#         counter electrode in volts.
#     iw : list float
#         Value of the current flowing though the working electrode in amperes.
#     vwr : list float, optional
#         Values of the potential in the working electrode measured with respect
#         to the reference electrode. The default is []. In such case Reference
#         is not considered.
#     ranges : list, optional
#         List with the ranges as [["Xmin", "Xmax"'], ["Ymin", "Ymax"]].
#         The default is ["auto","auto"].

#     Returns
#     -------
#     figHandler: handler to the created figure.

#     """
#     #Otaining parameters:
#     if type(vwc) == list:
#         vwc = np.asarray(vwc)
    
#     if type(iw) == list:
#         iw = np.asarray(iw)
    
#     if type(time) == list:
#         time = np.asarray(time)
    
#     if type(vwr) == list:
#         vwr = np.asarray(vwr)
    
#     last_halve = int(len(iw)/2) 
#     iw_mean_last_halve = iw[last_halve:].mean()

#     #Ploting int he case nor reference electrode is used.
#     #comment = ["", "", ""]
#     #cmt = "$I_{ON/OFF}$  = "
#     #cmt2 = "${:.1e}$".format(device.non_lin)
#     #comment[0]= str(cmt + cmt2)
#     #comment[0] = ""

#     #cmt = "$I_{ON}$  = "
#     #cmt2 = "${:.1e}\\, A/cm^2$".format(device.i_on)
#     #comment[1] = str(cmt + cmt2)

#     #cmt = "$V_{ON} (V_{OFF})$  = "
#     #cmt2 = "${:.1f}$ $V$".format(device.v_on)
#     #cmt3 = " (${:.1f}$ $V$)".format(device.v_off)
#     #comment[2] = str(cmt + cmt2 + cmt3)

#     comment = [1, 2, 3]
    
#     fig_iv_lin = Grp_2D(time,
#                            iw,
#                            col=['b', 'r'],
#                            style='lin', eng_units=True,
#                            D_Top_Axis=True,
#                            title="IV curve MSM Diode",
#                            x_label=r"$V_{BIAS}$",
#                            y_label="$I$",
#                            d_label="E",                           
#                            cmmt_1=comment[0],
#                            cmmt_2=comment[1],
#                            cmmt_3=comment[2],
#                            legend=["Original", "Smoothed"],
#                            #ox_th=device.s_th*1e3, k_val=1,
#                            x_prec=2, y_prec=1, d_prec=2,
#                            units=["V", "A/cm^2", "V/nm"],
#                            x_limits = x_limits, y_limits = y_limits, 
#                            x_cmt_lin = -7, y_cmt_lin = 4)

#     return fig_iv_lin
        


# *****************************************************************************
# Functions for plotting iv diode graphs
# *****************************************************************************

def plot_MIM_iv_lin(device, x_limits=["", ""], y_limits=["", ""]):

    # Plotting of the iv characteristics in linear scale
    
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.non_lin)
    comment[0]= str(cmt + cmt2)
    #comment[0] = ""

    cmt = "$I_{ON}$  = "
    cmt2 = "${:.1e}\\, A/cm^2$".format(device.i_on)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{ON} (V_{OFF})$  = "
    cmt2 = "${:.1f}$ $V$".format(device.v_on)
    cmt3 = " (${:.1f}$ $V$)".format(device.v_off)
    comment[2] = str(cmt + cmt2 + cmt3)

    fig_iv_lin = Grp_2D([device.v],
                           [device.i_norm],
                           col=['b', 'r'],
                           style='lin', eng_units=True,
                           D_Top_Axis=True,
                           title="IV curve MSM Diode",
                           x_label=r"$V_{BIAS}$",
                           y_label="$I$",
                           d_label="E",                           
                           cmmt_1=comment[0],
                           cmmt_2=comment[1],
                           cmmt_3=comment[2],
                           legend=["Original", "Smoothed"],
                           ox_th=device.s_th*1e3, k_val=1,
                           x_prec=2, y_prec=1, d_prec=2,
                           units=["V", "A/cm^2", "V/nm"],
                           x_limits = x_limits, y_limits = y_limits, 
                           x_cmt_lin = -7, y_cmt_lin = 4)

    return fig_iv_lin

def plot_MIM_iv_log(device, x_limits=["", ""], y_limits=["", ""]):

    # Plotting of the iv characteristics in linear scale
    
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.non_lin)
    comment[0]= str(cmt + cmt2)
    #comment[0] = ""

    cmt = "$I_{ON}$  = "
    cmt2 = "${:.1e}\\, A/cm^2$".format(device.i_on)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{ON} (V_{OFF})$  = "
    cmt2 = "${:.1f}$ $V$".format(device.v_on)
    cmt3 = " (${:.1f}$ $V$)".format(device.v_off)
    comment[2] = str(cmt + cmt2 + cmt3)

    fig_iv_log = Grp_2D([device.v],
                           [device.i_norm_abs],
                           col=['b', 'r'],
                           style='log', eng_units=True,
                           D_Top_Axis=True,
                           title="IV curve MSM Diode",
                           x_label=r"$V_{BIAS}$",
                           y_label="$I$",
                           d_label="E",
                           cmmt_1=comment[0],
                           cmmt_2=comment[1],
                           cmmt_3=comment[2],
                           legend=["Original", "Smoothed"],
                           ox_th=device.s_th*1e3, k_val=1,
                           x_prec=2, y_prec=1, d_prec=2,
                           units=["V", "A/cm^2", "V/nm"],
                           x_limits = x_limits, y_limits = y_limits,
                           log_skip=0, x_cmt_log = -12, y_cmt_log = 70)

    return fig_iv_log
# *****************************************************************************
# Function for plotting transfer graph with booth sweep (pn and np)
# *****************************************************************************


def plot_trans_both(device):

    comment = ["", "", ""]

    cmt = "$W_{CH}$  = "
    cmt2 = "${:.1f}$".format(device.ch_width)
    comment[0] = str(cmt + cmt2)

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.np_vds[0])
    comment[2] = str(cmt + cmt2)

    fig_tran = Grp_2D([device.np_vgs, device.pn_vgs],
                      [device.np_idw, device.pn_idw], col=['b', 'r'],
                      style='log', eng_units=True, D_Top_Axis=True,
                      title="Transfer Characteristics",
                      x_label=r"$V_{GS}$",
                      y_label="$I_D$",
                      cmmt_1=comment[0],
                      cmmt_2=comment[1],
                      cmmt_3=comment[2],
                      legend=["- to +", "+ to -"],
                      ox_th=device.ox_thickness, k_val=device.k_value,
                      x_prec=2, y_prec=1, d_prec=2,
                      units=["V", "A/\mu m", "V/nm"])

    return fig_tran


# *****************************************************************************
# Function for plotting transfer graph in linear scale (np or pn)
# *****************************************************************************

def plot_trans_lin(device):
    comment = ["", "", ""]

    # Plotting of the transfer characteristics in linear scale np
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.on_off.val)
    # comment[0]= str(cmt + cmt2)
    comment[0] = ""

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])
    comment[2] = str(cmt + cmt2)

    fig_trans_lin = Grp_2D([device.vgs],
                           [device.idw],
                           col=['b'],
                           style='lin', eng_units=True,
                           D_Top_Axis=True,
                           title="Transfer Characteristics",
                           x_label=r"$V_{GS}$",
                           y_label="$I_D$",
                           cmmt_1=comment[0],
                           cmmt_2=comment[1],
                           cmmt_3=comment[2],
                           legend=["- to +"],
                           ox_th=device.ox_thickness, k_val=device.k_value,
                           x_prec=2, y_prec=1, d_prec=2,
                           units=["V", "A/\mu m", "V/nm"])

    return fig_trans_lin

# *****************************************************************************
# Function for plotting transfer graph in linear scale gsh not id
# *****************************************************************************

def plot_trans_lin_gsh(device):
    comment = ["", "", ""]

    # Plotting of the transfer characteristics in linear scale np
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.on_off.val)
    # comment[0]= str(cmt + cmt2)
    comment[0] = ""

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])
    comment[2] = str(cmt + cmt2)

    unit_gsh = "S / \u25a1"
    
    fig_trans_lin_gsh = Grp_2D([device.vgs],
                               [device.gsh],
                               col=['b'],
                               style='lin', eng_units=True,
                               D_Top_Axis=True,
                               title="Transfer Characteristics",
                               x_label=r"$V_{GS}$",
                               y_label="$G_{SH}$",
                               cmmt_1=comment[0],
                               cmmt_2=comment[1],
                               cmmt_3=comment[2],
                               legend=["- to +"],
                               ox_th=device.ox_thickness, k_val=device.k_value,
                               x_prec=2, y_prec=1, d_prec=2,
                               units=["V", unit_gsh, "V/nm"])

    return fig_trans_lin_gsh
# *****************************************************************************
# Function for plotting transfer graph in log scale ID
# *****************************************************************************


def plot_trans_log(device):
    comment = ["", "", ""]

    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.on_off.val)
    cmt3 = "\n$SS_{MIN}$ = "
    cmt4 = "${:.2f}\\, V/dec$".format(device.ss.val)
    comment[0] = str(cmt + cmt2 + cmt3 + cmt4)

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])

    comment[2] = str(cmt + cmt2)

    i_good = np.where(device.idw != 0)

    fig_trans_log = Grp_2D([device.vgs[i_good]],
                           [device.idw[i_good]],
                           col=['b'],
                           style='log', eng_units=True,
                           D_Top_Axis=True,
                           title="Transfer Characteristics",
                           x_label=r"$V_{GS}$",
                           y_label="$I_D$",
                           cmmt_1=comment[0],
                           cmmt_2=comment[1],
                           cmmt_3=comment[2],
                           legend=["- to +"],
                           ox_th=device.ox_thickness, k_val=device.k_value,
                           x_prec=2, y_prec=1, d_prec=2,
                           units=["V", "A/\mu m", "V/nm"])

    # Plotting of line to indicate ig average

    i_vgs = list(np.where(device.vgs < device.vth.val)[0])
    x_val = device.vgs[i_vgs]
    # y_val = np.abs(device.np_ig[i_vgs])
    y_val = np.ones(len(x_val)) * device.on_off.avrg_ig

    fig_trans_log.ax.legend_.remove()
    fig_trans_log.ax.plot(x_val, y_val, 'r--', linewidth=2,
                          label = "Average $I_G$")

    handles = fig_trans_log.ax.get_legend_handles_labels()
    plt.legend(handles[0], handles[1], loc='upper left', fontsize='12')


    plt.show()

    return fig_trans_log

# *****************************************************************************
# Function for plotting transfer graph in log scale Gsh
# *****************************************************************************

def plot_trans_log_gsh(device):
    comment = ["", "", ""]

    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1e}$".format(device.on_off.val)
    cmt3 = "\n$SS_{MIN}$ = "
    cmt4 = "${:.2f}\\, V/dec$".format(device.ss.val)
    comment[0] = str(cmt + cmt2 + cmt3 + cmt4)

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])

    comment[2] = str(cmt + cmt2)

    i_good = np.where(device.gsh != 0)

    unit_gsh = "S / \u25a1"

    fig_trans_log_gsh = Grp_2D([device.vgs[i_good]],
                               [device.gsh[i_good]],
                               col=['b'],
                               style='log', eng_units=True,
                               D_Top_Axis=True,
                               title="Transfer Characteristics",
                               x_label=r"$V_{GS}$",
                               y_label="$G_{SH}$",
                               cmmt_1=comment[0],
                               cmmt_2=comment[1],
                               cmmt_3=comment[2],
                               legend=["- to +"],
                               ox_th=device.ox_thickness, k_val=device.k_value,
                               x_prec=2, y_prec=1, d_prec=2,
                               units=["V", unit_gsh, "V/nm"])

    # Plotting of line to indicate ig average

    plt.show()

    return fig_trans_log_gsh

# *****************************************************************************
# Function for plotting transconductance (gm) graph in linear scale (np or pn)
# *****************************************************************************


def plot_gm(device):
    comment = ["", "", ""]

    gm_w_val = np.amax(device.gm.val_w)

    cmt = "$gm_{pk}$  = "
    cmt2 = "${:.1e}\\, \\, S/\\mu m$".format(gm_w_val)
    comment[0] = str(cmt + cmt2)

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS} (V_{TH})$ = "
    cmt2 = "${:.1f}\\,V$".format(device.vds[0])
    cmt3 = "$({:.1f}\\,V$)".format(device.vth.val)
    comment[2] = str(cmt + cmt2 + cmt3)

    fig_gm = Grp_2D([device.vgs],
                    [device.gm.val_w],
                    col=['b'],
                    style='lin', eng_units=True,
                    D_Top_Axis=True,
                    title="Transconductance",
                    x_label=r"$V_{GS}$",
                    y_label="$gm$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=["- to +"],
                    ox_th=device.ox_thickness, k_val=device.k_value,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", "S/\\mu m", "V/nm"])
 
    return fig_gm

# *****************************************************************************
# Function for plotting transconductance (gm) with details for Vth and gm_max
# *****************************************************************************


def plot_gm_details(device , x_val='vgs', meas_type='2p_fet'):
    comment = ["", "", ""]

    # For selecting the value to be used for x axis
    if (x_val == 'vgs'):
        np_vgs = device.vgs
        x_label = r'$V_{GS}$'

    elif (x_val == 'vgs-vth'):
        np_vgs = device.vgs_vth
        x_label = r'$V_{GS}$ - $V_{TH}$'

    gm_w_val = np.amax(device.gm.val_w)

    cmt = "$gm_{pk}$  = "
    cmt2 = "${:.1e}\\, \\, S/\\mu m$".format(gm_w_val)
    comment[0] = str(cmt + cmt2)

    if (meas_type == '2p_fet'):
        ox_thickness = device.ox_thickness
        k_value = device.k_value
        ch_width = device.ch_width

        cmt = "$L_{CH}$  = "
        cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
        comment[1] = str(cmt + cmt2)

        cmt = "$V_{DS} (V_{TH})$ = "
        cmt2 = "${:.1f}\\,V$".format(device.vds[0])
        cmt3 = "$({:.1f}\\,V$)".format(device.vth.val)
        comment[2] = str(cmt + cmt2 + cmt3)

    elif (meas_type == 'tlm'):
        ox_thickness = device.ox_thickness_avrg
        k_value = device.k_value_avrg
        ch_width = 1.0

        cmt = "$V_{TH}$ = "
        cmt2 = "${:.1f}\\,V$".format(device.vth.val)
        comment[2] = str(cmt + cmt2)

        comment[1] = ''

    elif (meas_type == '4p_fet'):
        ox_thickness = device.ox_thickness
        k_value = device.k_value
        ch_width = 1

        cmt = "$L_{CH}$  = "
        cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
        comment[1] = str(cmt + cmt2)

        cmt = "$V_{DS} (V_{TH})$ = "
        cmt2 = "${:.1f}\\,V$".format(device.vds[0])
        cmt3 = "$({:.1f}\\,V$)".format(device.vth.val)
        comment[2] = str(cmt + cmt2 + cmt3)

    fig_gm_details = Grp_2D([np_vgs],
                            [device.gm.val_w],
                            col=['b'],
                            style='lin', eng_units=True,
                            D_Top_Axis=True,
                            title="Transconductance",
                            x_label=x_label,
                            y_label="$gm$",
                            cmmt_1=comment[0],
                            cmmt_2=comment[1],
                            cmmt_3=comment[2],
                            legend=["- to +"],
                            ox_th=ox_thickness,
                            k_val=k_value,
                            x_prec=2, y_prec=1, d_prec=2,
                            units=["V", "S/\\mu m", "V/nm"])

    # Plot triangle in the maximum poinr of gm and draw a line
    gm_max = np.amax(device.gm.val_w)
    gm_max_x = np_vgs[np.where(device.gm.val_w == gm_max)]
    gm_max_list = []

    size_gm_x = len(gm_max_x)

    for i in range(size_gm_x):
        gm_max_list.append(gm_max)

    # Print the marker in the position where gm is reported
    fig_gm_details.ax.plot(gm_max_x, gm_max_list, 'r^',
                           markeredgecolor='k',
                           markeredgewidth=2,
                           markerfacecolor='r',
                           markersize=9)

    # Print the markers for the points used to obtain the Vth
    vgs_win = device.vth.vgs_win
    gmw_win = device.vth.gms_win/ch_width

    fig_gm_details.ax.plot(vgs_win, gmw_win, 'rs',
                           markeredgecolor='k',
                           markeredgewidth=2,
                           markerfacecolor='g',
                           markersize=7)

    # Plotting of line fitted to aproximate Vth
    y = np.polyval(device.vth.pol, np_vgs)/ch_width
    index = []
    for i_y in range(0, len(y)):
        if (y[i_y] >= 0) and (y[i_y] <= gm_max):
            index.append(i_y)

    vgs_line = np_vgs[index]

    fig_gm_details.ax.plot(vgs_line, y[index], 'r',
                           linewidth=2)
    plt.show()

    return fig_gm_details

# *****************************************************************************
# Function for plotting mobility from linear regime for pn and np
# *****************************************************************************


def plot_mu(device, x_val='vgs', meas_type='2p_fet'):

    comment = ["", "", ""]

    # For selecting the value to be used for x axis
    if (x_val == 'vgs'):
        np_vgs = device.vgs
        x_label = r'$V_{GS}$'
    elif (x_val == 'vgs-vth'):
        x_label = r'$V_{GS}$ - $V_{TH}$'
        np_vgs = device.vgs_vth

    mu_val = device.mu.val
    cmt = "$\\mu$  = "
    units_mu = "$cm^2V^{-1}s^{-1}$"
    cmt2 = "${:.1f}\\,$".format(mu_val)
    comment[0] = str(cmt + cmt2 + units_mu)

    if (meas_type == '2p_fet'):
        ox_thickness = device.ox_thickness
        k_value = device.k_value

        cmt = "$L_{CH}$  = "
        cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
        comment[1] = str(cmt + cmt2)

        cmt = "$V_{DS}$  = "
        cmt2 = "${:.1f}$ $V$".format(device.vds[0])
        comment[2] = str(cmt + cmt2)

    elif (meas_type == 'tlm'):
        ox_thickness = device.ox_thickness_avrg
        k_value = device.k_value_avrg

        comment[1] = ''
        comment[1] = ''

    fig_mu = Grp_2D([np_vgs],
                    [device.mu.val_vgs],
                    col=['b'],
                    style='lin', eng_units=False,
                    D_Top_Axis=True,
                    title="Mobility Linear Regime",
                    x_label=x_label,
                    y_label=str("$\\mu_{Lin}$"),
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=["- to +"],
                    ox_th=ox_thickness, k_val=k_value,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", "cm^2V^{-1}s^{-1}", "V/nm"])

    # Plot triangle in the maximum point of mobility
    mu_max = device.mu.val
    mu_max_x = np_vgs[device.mu.val_index]

    # Print the marker in the position where gm is reported
    fig_mu.ax.plot(mu_max_x, mu_max, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    plt.show()

    return fig_mu

# *****************************************************************************
# Function for plotting Rs (lin or semilog) for pn and np
# *****************************************************************************


def plot_rs(vgs_vth, rs, rs_std=[0], overdrive_pt="", ox_th=50, k_val=3.9,
            legend_line="", err=True, style='lin',
            x_label=r"$V_{GS} - V_{TH}$"):
    """
    Function to plot the sheet resistance.

    Parameters
    ----------
    vgs_vth : np.array (float)
        X axis of the graph that must be normally related to vgs.

    rs : np.array (float)
        Sheet resistance as a function of vgs_vth. they must be the same size.
        units are in ohm/sq.

    rs_std : np.array (float)
        Standard deviation from the fitting used for obtaining rs. This is only
        compulsory if err is True, otherwhise is not required.

    ox_th : float
        Thickness of the oxide in nm. To be used to calculate D for the top
        axis.

    k_val : float
        Relative permittivity of the gate dielectric. to be used to calculate
        D for the top axis.

    lengend : string
        To be used as the legend of the plotting curve.

    err : boolean
        To be use to select wether or not to plot the error.

    style : string
        Can be 'lin' or 'log'. Used to select whether to plot in linear or log
        scale.

    x_label : string
        Used to specify the name of the x label, normally Vgs-Vth, but in some
        cases it can be useful to plot Vgs for instance. Default is Vgs-Vth.

    Return
    ------

    fig_rs : Grp_2D class instance
        Instance to the class containing all the information related to the
        created figure.
    """

    comment = ["", "", ""]

    index = np.where(vgs_vth > 0)

    rs = rs[index]
    vgs_vth = vgs_vth[index]
    if (err is True):
        error = rs_std[index]

    if overdrive_pt == "":
        min_rs = np.amin(rs)  # Units are ohm*µm
        i_min_rs = np.where(rs == min_rs)
        if (err is True):
            min_rs_std = float(error[i_min_rs])
    else:
        i_min_rs = int(np.where(vgs_vth == overdrive_pt)[0])
        min_rs = rs[i_min_rs]  # Units are ohm*µm
        if (err is True):
            min_rs_std = float(error[i_min_rs])

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n"

    cmt = "$R_{SH}$  = "
    units_rs = "\N{GREEK CAPITAL LETTER OMEGA} / \u25a1"
    cmt2 = "${:.1e}\\,$ ".format(min_rs)
    comment[0] = str(cmt + cmt2 + units_rs)

    if (err is True):
        cmt = r"$E_{rr}\,$= $\pm$"
        cmt2 = "${:.1e}\\,$ ".format(min_rs_std)
        comment[1] = str(cmt + cmt2 + units_rs)
    else:
        comment[1] = ""

    cmt = "$V_{GS}$ $@$ $min$ $R_{SH}$ = "
    cmt2 = "${:.1f}$ $V$".format(float(vgs_vth[i_min_rs]))
    comment[2] = str(cmt + cmt2 + spaces)

    fig_rs = Grp_2D([vgs_vth],
                    [rs],
                    col=['b'],
                    style=style, eng_units=True,
                    D_Top_Axis=True, log_skip=0,
                    title="Sheet Resistance From TLM",
                    x_label=x_label,
                    y_label=r"$R_{SH}$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=[legend_line],
                    ox_th=ox_th, k_val=k_val,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", units_rs, "V/nm"])

    # Print the marker in the position where Rsh is minimum
    fig_rs.ax.plot(vgs_vth[i_min_rs], min_rs, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_rs.ax.fill_between(vgs_vth, rs-error, rs+error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)

    plt.show()

    return fig_rs

# *****************************************************************************
# Function for plotting Rc (lin or semilog) for pn and np
# *****************************************************************************


def plot_rc(vgs_vth, rc, rc_std=[0], overdrive_pt="", ox_th=50, k_val=3.9,
            legend_line="", err=True, style='lin',
            x_label=r"$V_{GS} - V_{TH}$"):
    """
    Function to plot the sheet resistance.

    Parameters
    ----------
    vgs_vth : np.array (float)
        X axis of the graph that must be normally related to vgs.

    rc : np.array (float)
        Contact resistance as a function of vgs_vth. Must be the same size as
        Vgs-Vth units are in ohm*µm.

    rc_std : np.array (float)
        Standard deviation from the fitting used for obtaining rc. This is only
        compulsory if err is True, otherwhise is not required.

    ox_th : float
        Thickness of the oxide in nm. To be used to calculate D for the top
        axis.

    k_val : float
        Relative permittivity of the gate dielectric. to be used to calculate
        D for the top axis.

    lengend : string
        To be used as the legend of the plotting curve.

    err : boolean
        To be use to select wether or not to plot the error.

    style : string
        Can be 'lin' or 'log'. Used to select whether to plot in linear or log
        scale.

    x_label : string
        Used to specify the name of the x label, normally Vgs-Vth, but in some
        cases it can be useful to plot Vgs for instance. Default is Vgs-Vth.

    Return
    ------

    fig_rc : Grp_2D class instance
        Instance to the class containing all the information related to the
        created figure.
    """

    comment = ["", "", ""]

    index = np.where(vgs_vth > 0)

    rc = rc[index]
    vgs_vth = vgs_vth[index]
    if (err is True):
        error = rc_std[index]

    if overdrive_pt == "":
        #min_rc = np.amin(rc)  # Units are ohm*µm
        min_rc = rc[len(rc)-1]        
        i_min_rc = np.where(rc == min_rc)
        if (err is True):
            min_rc_std = float(error[i_min_rc])
    else:
        i_min_rc = int(np.where(vgs_vth == overdrive_pt)[0])
        min_rc = rc[i_min_rc]  # Units are ohm*µm
        if (err is True):
            min_rc_std = float(error[i_min_rc])

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n"

    cmt = "$R_{C}$  = "
    units_rc = "\N{GREEK CAPITAL LETTER OMEGA} * \N{GREEK SMALL LETTER Mu}m"
    cmt2 = "${:.1e}\\,$ ".format(min_rc)
    comment[0] = str(cmt + cmt2 + units_rc)

    if (err is True):
        cmt = r"$E_{rr}\,$= $\pm$"
        cmt2 = "${:.1e}\\,$ ".format(min_rc_std)
        comment[1] = str(cmt + cmt2 + units_rc)
    else:
        comment[1] = ""

    cmt = "$V_{GS}$ $@$ $min$ $R_{SH}$ = "
    cmt2 = "${:.1f}$ $V$".format(float(vgs_vth[i_min_rc]))
    comment[2] = str(cmt + cmt2 + spaces)

    fig_rc = Grp_2D([vgs_vth],
                    [rc],
                    col=['b'],
                    style=style, eng_units=True,
                    D_Top_Axis=True, log_skip=0,
                    title="Contact Resistance From TLM",
                    x_label=x_label,
                    y_label=r"$R_{C}$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=[legend_line],
                    ox_th=ox_th, k_val=k_val,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", units_rc, "V/nm"])

    # Plot triangle in the maximum point of mobility
    # Print the marker in the position where Rc error is minimum
    fig_rc.ax.plot(vgs_vth[i_min_rc], min_rc, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_rc.ax.fill_between(vgs_vth, rc-error, rc+error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)

    plt.show()

    return fig_rc

# *****************************************************************************
# Function for plotting Lt (lin or semilog) for pn and np
# *****************************************************************************


def plot_lt(vgs_vth, lt, lt_std=[0], overdrive_pt="", ox_th=50, k_val=3.9,
            legend_line="", err=True, style='lin',
            x_label=r"$V_{GS} - V_{TH}$"):
    """
    Function to plot the sheet resistance.

    Parameters
    ----------
    vgs_vth : np.array (float)
        X axis of the graph that must be normally related to vgs.

    lt : np.array (float)
        Transfer length as a function of vgs_vth. Must be the same size as
        Vgs-Vth units are in µm.

    lt_std : np.array (float)
        Standard deviation from the fitting used for obtaining lt. This is only
        compulsory if err is True, otherwhise is not required.

    ox_th : float
        Thickness of the oxide in nm. To be used to calculate D for the top
        axis.

    k_val : float
        Relative permittivity of the gate dielectric. to be used to calculate
        D for the top axis.

    lengend : string
        To be used as the legend of the plotting curve.

    err : boolean
        To be use to select wether or not to plot the error.

    style : string
        Can be 'lin' or 'log'. Used to select whether to plot in linear or log
        scale.

    x_label : string
        Used to specify the name of the x label, normally Vgs-Vth, but in some
        cases it can be useful to plot Vgs for instance. Default is Vgs-Vth.

    Return
    ------

    fig_lt : Grp_2D class instance
        Instance to the class containing all the information related to the
        created figure.
    """

    comment = ["", "", ""]

    index = np.where(vgs_vth > 0)

    lt = lt[index]
    lt_plt = np.multiply(lt, 1e-6)

    vgs_vth = vgs_vth[index]

    if (err is True):
        error = lt_std[index]
        error_plt = np.multiply(error, 1e-6)

    if overdrive_pt == "":
        min_error = np.amin(error)  # Units are µm
        i_min_error = np.where(error == min_error)[0]
    else:
        #i_min_error = int(np.where(vgs_vth == overdrive_pt)[0])
        i_min_error = 20
        min_error = error[i_min_error]  # Units are ohm*µm

    # Selection of the i_min_error taken at the highest Vg in case several
    i_min_error = np.where(vgs_vth == np.amax(vgs_vth[i_min_error]))[0]

    # Lt where the error is minimum
    min_lt = float(lt[i_min_error])
    min_lt_plt = np.multiply(min_lt, 1e-6)

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n"

    cmt = "$L_{T}$  = "
    units_lt = "\N{GREEK SMALL LETTER Mu}m"
    cmt2 = "${:.3f}\\,$ ".format(min_lt)
    comment[0] = str(cmt + cmt2 + units_lt)

    if (err is True):
        cmt = r"$E_{rr}\,$= $\pm$"
        cmt2 = "${:.3f}\\,$ ".format(min_error)
        comment[1] = str(cmt + cmt2 + units_lt)
    else:
        comment[1] = ""

    cmt = "$V_{GS}$ $@$ $min$ $R_{SH}$ = "
    cmt2 = "${:.1f}$ $V$".format(float(vgs_vth[i_min_error]))
    comment[2] = str(cmt + cmt2 + spaces)

    max_lt_plt = np.amax(lt_plt)

    fig_lt = Grp_2D([vgs_vth],
                    [lt_plt],
                    col=['b'],
                    style=style, eng_units=True,
                    D_Top_Axis=True, log_skip=0,
                    title="Transfer Length From TLM",
                    x_label=x_label,
                    y_label=r"$L_{T}$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=[legend_line],
                    ox_th=ox_th, k_val=k_val,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", "m", "V/nm"],
                    dy_max=0.3*max_lt_plt)

    # Print the marker in the position where lt is reported
    fig_lt.ax.plot(vgs_vth[i_min_error], min_lt_plt, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_lt.ax.fill_between(vgs_vth, lt_plt-error_plt, lt_plt+error_plt,
                               alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)

    plt.show()

    return fig_lt

# *****************************************************************************
# Function for plotting rho (contact resistivity) (lin or semilog)
# *****************************************************************************

def plot_rh(vgs_vth, rh, rh_std=[0], ox_th=50, k_val=3.9,
            legend_line="", err=True, style='lin',
            x_label=r"$V_{GS} - V_{TH}$"):
    """
    Function to plot the sheet resistance.

    Parameters
    ----------
    vgs_vth : np.array (float)
        X axis of the graph that must be normally related to vgs.

    rh : np.array (float)
        Contact resistivity as a function of vgs_vth. Must be the same size as
        Vgs-Vth units are in ohm*cm^2.

    rh_std : np.array (float)
        Standard deviation from the fitting used for obtaining rh. This is only
        compulsory if err is True, otherwhise is not required.

    ox_th : float
        Thickness of the oxide in nm. To be used to calculate D for the top
        axis.

    k_val : float
        Relative permittivity of the gate dielectric. To be used to calculate
        D for the top axis.

    legend : string
        To be used as the legend of the plotting curve.

    err : boolean
        To be use to select wether or not to plot the error.

    style : string
        Can be 'lin' or 'log'. Used to select whether to plot in linear or log
        scale.

    x_label : string
        Used to specify the name of the x label, normally Vgs-Vth, but in some
        cases it can be useful to plot Vgs for instance. Default is Vgs-Vth.

    Return
    ------

    fig_rc : Grp_2D class instance
        Instance to the class containing all the information related to the
        created figure.
    """

    comment = ["", "", ""]

    index = np.where(vgs_vth > 0)

    rh = rh[index]
    vgs_vth = vgs_vth[index]
    if (err is True):
        error = rh_std[index]

    min_rh = np.amin(rh)  # Units are ohm*µm
    i_min_rh = np.where(rh == min_rh)
    if (err is True):
        min_rh_std = float(error[i_min_rh])

    # For creating the spaces for the correct positioning of the comments.
    if (style == 'log'):
        spaces = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    else:
        spaces = "\n\n\n"

    cmt = "$\N{GREEK SMALL LETTER RHO}_{C}$  = "
    units_rh = "\N{GREEK CAPITAL LETTER OMEGA} * " + r'$cm^{2}$'
    cmt2 = "${:.1e}\\,$ ".format(min_rh)
    comment[0] = str(cmt + cmt2 + units_rh)

    if (err is True):
        cmt = r"$E_{rr}\,$=$\pm$"
        cmt2 = "${:.1e}\\,$ ".format(min_rh_std)
        comment[1] = str(cmt + cmt2 + units_rh)
    else:
        comment[1] = ""

    cmt = "$V_{GS}$ $@$ $min$ $\N{GREEK SMALL LETTER RHO}_{C}$ = "
    cmt2 = "${:.1f}$ $V$".format(float(vgs_vth[i_min_rh]))
    comment[2] = str(cmt + cmt2 + spaces)

    fig_rh = Grp_2D([vgs_vth],
                    [rh],
                    col=['b'],
                    style=style, eng_units=False,
                    D_Top_Axis=True, log_skip=0,
                    title="Contact Resistivity From TLM",
                    x_label=x_label,
                    y_label="\N{GREEK SMALL LETTER RHO}$_{C}$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=[legend_line],
                    ox_th=ox_th, k_val=k_val,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", "\N{GREEK CAPITAL LETTER OMEGA}\,*\,cm^{2}",
                           "V/nm"])

    # Plot triangle in the maximum point of mobility
    # Print the marker in the position where Rsh is minimum
    fig_rh.ax.plot(vgs_vth[i_min_rh], min_rh, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Plotting of the error

    if (err is True):
        fig_rh.ax.fill_between(vgs_vth, rh-error, rh+error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)

    fig_rh.ax.legend(loc='upper right')

    plt.show()

    return fig_rh

# *****************************************************************************
# Function to plot one set of points for showing the method.
# *****************************************************************************

def plot_tlm_expl(vgs_vth, rt_vth_matrix, Lch):

    comment = ["", "", ""]

    vgs_vth = float(vgs_vth)
    Lch = np.asarray(Lch)


    pol = np.polyfit(Lch, rt_vth_matrix, 1)
    min_x = -1*pol[1]/pol[0]
    max_x = np.amax(Lch)

    line_x = np.linspace(min_x, max_x, 30)
    line_y = np.polyval(pol, line_x)

    line_x1 = np.array([0, 0])
    line_y1 = np.array([0, np.amax(line_y)])

    line_x2 = np.array([min_x, max_x])
    line_y2 = np.array([0, 0])

    spaces = "\n\n"

    cmt = "$R_{C}$  = "
    units_rc = "\N{GREEK CAPITAL LETTER OMEGA} * \N{GREEK SMALL LETTER Mu}m"
    cmt2 = "${:.3f}\\,$ ".format(pol[1]/2)
    comment[0] = str(cmt + cmt2 + units_rc)

    cmt = "$L_{T}$  = "
    units_lt = "\N{GREEK SMALL LETTER Mu}m"
    cmt2 = "${:.3f}\\,$ ".format(np.abs(min_x/2))
    comment[1] = str(cmt + cmt2 + units_lt)

    cmt = "$V_{GS} - V_{TH}$ = "
    cmt2 = "${:.1f}$ $V$".format(float(vgs_vth))
    comment[2] = str(cmt + cmt2 + spaces)


    fig_lt = Grp_2D([line_x],
                    [line_y],
                    col=['b'],
                    style='lin', eng_units=True,
                    D_Top_Axis=False, log_skip=0,
                    title="TLM demonstration",
                    x_label=r'$L_{CH}$',
                    y_label=r"$R_{T}$",
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    ox_th=50, k_val=3.9,
                    legend=[''],
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["\mu m", "\Omega * \mu m", "V/nm"],
                    dx_min=0.5*min_x, dx_max=np.abs(0.5*min_x),
                    dy_min=0, dy_max=0)

    # Print the marker in the position where lt is reported
    fig_lt.ax.plot(line_x1, line_y1, 'k', linewidth=2.0)

    fig_lt.ax.plot(line_x2, line_y2, 'k', linewidth=2.0)

    # Print the marker in the position where lt is reported
    fig_lt.ax.plot(Lch, rt_vth_matrix, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)

    # Print the marker in the position where rc is reported
    fig_lt.ax.plot(0, pol[1], 'ys',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='y',
                   markersize=9)

    # Print the marker in the position where lt is reported
    fig_lt.ax.plot(min_x, 0, 'gs',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='g',
                   markersize=9)
    plt.show()

    return fig_lt

# *****************************************************************************
# Function for plotting mobility graph of graphene devices
# *****************************************************************************


def plot_mu_gr(device, cmt_enable=True):
    comment = ["", "", ""]
    
    # Plotting of the transfer characteristics in linear scale np
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1f}$".format(device.on_off.val)
    cmt3 = "$\\mu_e$  = "
    units_mu = r'$cm^2V^{-1}s^{-1}$'
    cmt4 = "${:.1f}\\,$".format(device.mu.max_e)
    cmt5 = "$\\mu_h$  = "
    cmt6 = "${:.1f}\\,$".format(device.mu.max_h)
    cmt7 = "$V_K$  = "
    cmt8 = "${:.1f}$ $V$".format(device.vk.val)
    cmt9 = "$n_{2D} @ V_K$  = "
    cmt10 = "${:.1f}$".format(device.n2d_k/1e12)
    units_n2d = r'$\,\times\,10^{12}\,cm^{-2}$'
    comment[0]= str(cmt + cmt2 + "\n" + cmt3 + cmt4 + units_mu + "\n" + 
                    cmt5 + cmt6 + units_mu + "\n" + 
                    cmt7 + cmt8 + "\n" +
                    cmt9 + cmt10 + units_n2d)
    #comment[0] = ""

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    cmt3 = "$W_{CH}$  = "
    cmt4 = "${:.1f}\\, \\mu m$".format(device.ch_width)
    comment[1] = str(cmt + cmt2 + "\n" + cmt3 + cmt4)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])
    comment[2] = str(cmt + cmt2)
    
    if cmt_enable == False:
        comment[0] = ""
        comment[1] = ""
        comment[2] = ""
        

    fig_mu_lin_gr = Grp_2D([device.vgs],
                           [np.abs(device.mu.val_vgs)],
                           col=['b'],
                           style='lin', eng_units=True,
                           D_Top_Axis=True,
                           title="Field Effect Mobility",
                           x_label=r"$V_{GS}$",
                           y_label="$\\mu_e$",
                           cmmt_1=comment[0],
                           cmmt_2=comment[1],
                           cmmt_3=comment[2],
                           legend=[""],
                           ox_th=device.ox_thickness, k_val=device.k_value,
                           x_prec=2, y_prec=1, d_prec=2,
                           units=["V", "cm^2V^{-1}s^{-1}", "V/nm"],
                           dx_min=0, dx_max=0, dy_min=0, dy_max=0)

    return fig_mu_lin_gr


# *****************************************************************************
# Function for plotting transfer graph in linear scale
# *****************************************************************************

def plot_trans_lin_gr(device, cmt_enable=True):
    comment = ["", "", ""]
    
    # Plotting of the transfer characteristics in linear scale np
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1f}$".format(device.on_off.val)
    cmt3 = "$\\mu_e$  = "
    units_mu = r'$cm^2V^{-1}s^{-1}$'
    cmt4 = "${:.1f}\\,$".format(device.mu.max_e)
    cmt5 = "$\\mu_h$  = "
    cmt6 = "${:.1f}\\,$".format(device.mu.max_h)
    cmt7 = "$V_K$  = "
    cmt8 = "${:.1f}$ $V$".format(device.vk.val)
    cmt9 = "$n_{2D} @ V_K$  = "
    cmt10 = "${:.1f}$".format(device.n2d_k/1e12)
    units_n2d = r'$\,\times\,10^{12}\,cm^{-2}$'
    comment[0]= str(cmt + cmt2 + "\n" + cmt3 + cmt4 + units_mu + "\n" + 
                    cmt5 + cmt6 + units_mu + "\n" + 
                    cmt7 + cmt8 + "\n" +
                    cmt9 + cmt10 + units_n2d)
    #comment[0] = ""

    cmt = "$L_{CH}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.ch_length)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])
    comment[2] = str(cmt + cmt2)
    
    if cmt_enable == False:
        comment[0] = ""
        comment[1] = ""
        comment[2] = ""
        

    fig_trans_lin_gr = Grp_2D( [device.vgs],
                               [device.rt.val],
                               col=['b'],
                               style='lin', eng_units=True,
                               D_Top_Axis=True,
                               title="Transfer Characteristics",
                               x_label=r"$V_{GS}$",
                               y_label="$R_T$",
                               cmmt_1=comment[0],
                               cmmt_2=comment[1],
                               cmmt_3=comment[2],
                               legend=[""],
                               ox_th=device.ox_thickness, k_val=device.k_value,
                               x_prec=2, y_prec=1, d_prec=2,
                               units=["V", "Ohm", "V/nm"],
                               dx_min=0, dx_max=0, dy_min=0, dy_max=0)

    return fig_trans_lin_gr

# *****************************************************************************
# Function for plotting transfer graph in linear scale
# *****************************************************************************

def plot_trans_lin_4p(device, cmt_enable=True):
    comment = ["", "", ""]
    
    # Plotting of the transfer characteristics in linear scale np
    comment = ["", "", ""]
    cmt = "$I_{ON/OFF}$  = "
    cmt2 = "${:.1f}$".format(device.on_off.val)
    cmt3 = "$\\mu_e$  = "
    units_mu = r'$cm^2V^{-1}s^{-1}$'
    cmt4 = "${:.1f}\\,$".format(device.mu.max_e)
    cmt5 = "$\\mu_h$  = "
    cmt6 = "${:.1f}\\,$".format(device.mu.max_h)
    cmt7 = "$V_K$  = "
    cmt8 = "${:.1f}$ $V$".format(device.vk.val)
    cmt9 = "$n_{2D} @ V_K$  = "
    cmt10 = "${:.1f}$".format(device.n2d_k/1e12)
    units_n2d = r'$\,\times\,10^{12}\,cm^{-2}$'
    comment[0]= str(cmt + cmt2 + "\n" + cmt3 + cmt4 + units_mu + "\n" + 
                    cmt5 + cmt6 + units_mu + "\n" + 
                    cmt7 + cmt8 + "\n" +
                    cmt9 + cmt10 + units_n2d)
    #comment[0] = ""

    cmt = "$L_{4P}$  = "
    cmt2 = "${:.1f}\\, \\mu m$".format(device.l4p)
    comment[1] = str(cmt + cmt2)

    cmt = "$V_{DS}$  = "
    cmt2 = "${:.1f}$ $V$".format(device.vds[0])
    comment[2] = str(cmt + cmt2)
    
    if cmt_enable == False:
        comment[0] = ""
        comment[1] = ""
        comment[2] = ""
        

    fig_trans_lin_4p = Grp_2D( [device.vgs],
                               [device.rsh],
                               col=['b'],
                               style='lin', eng_units=True,
                               D_Top_Axis=True,
                               title="Transfer Characteristics 4P",
                               x_label=r"$V_{GS}$",
                               y_label="$R_T$",
                               cmmt_1=comment[0],
                               cmmt_2=comment[1],
                               cmmt_3=comment[2],
                               legend=[""],
                               ox_th=device.ox_thickness, k_val=device.k_value,
                               x_prec=2, y_prec=1, d_prec=2,
                               units=["V", "Ohm", "V/nm"],
                               dx_min=0, dx_max=0, dy_min=0, dy_max=0)

    return fig_trans_lin_4p
# -----------------------------------------------------------------------------
# Potential plots
# -----------------------------------------------------------------------------

def plot_potentials(device):

    fig_potential = Grp_2D([device.vgs, device.vgs, device.vgs, device.vgs],
                           [device.vds, device.vp2, device.vp1, device.vgs*0],
                           ox_th=device.ox_thickness, k_val=device.k_value,
                           style='lin', eng_units=True, 
                           units=['V', 'V', 'V/nm'],
                           col=['--b', 'r', 'g', '--k'],
                           linewidth=[4,2,2,4],
                           title="Measured Potentials",
                           y_label="$V_{SS}\,-\,V_{P1}\,-\,V_{P2}\,-\,V_{DS}$",
                           x_label="$V_{GS}$",
                           cmmt_1="", cmmt_2="",
                           cmmt_3="",
                           D_Top_Axis=True,
                           log_skip=1,
                           x_prec=2, y_prec=1, d_prec=2,
                           dx_min=0, dx_max=0, dy_min=0, dy_max=0,
                           legend=[""])
    return fig_potential

#------------------------------------------------------------------------------

def plot_msm_err(vgs_vth, rc, rc_std=[0], overdrive_pt="", ox_th=50, k_val=1,
            legend_line="", err=True, style='lin',d_label="E",
            x_label=r"$V_{GS} - V_{TH}$", x_limits=["",""], y_limits=["",""]):
    """
    Function to plot the sheet resistance.

    Parameters
    ----------
    vgs_vth : np.array (float)
        X axis of the graph that must be normally related to vgs.

    rc : np.array (float)
        Contact resistance as a function of vgs_vth. Must be the same size as
        Vgs-Vth units are in ohm*µm.

    rc_std : np.array (float)
        Standard deviation from the fitting used for obtaining rc. This is only
        compulsory if err is True, otherwhise is not required.

    ox_th : float
        Thickness of the oxide in nm. To be used to calculate D for the top
        axis.

    k_val : float
        Relative permittivity of the gate dielectric. to be used to calculate
        D for the top axis.

    lengend : string
        To be used as the legend of the plotting curve.

    err : boolean
        To be use to select wether or not to plot the error.

    style : string
        Can be 'lin' or 'log'. Used to select whether to plot in linear or log
        scale.

    x_label : string
        Used to specify the name of the x label, normally Vgs-Vth, but in some
        cases it can be useful to plot Vgs for instance. Default is Vgs-Vth.

    Return
    ------

    fig_rc : Grp_2D class instance
        Instance to the class containing all the information related to the
        created figure.
    """

    comment = ["", "", ""]

    index = [x for x in range(len(vgs_vth))]

    rc = rc[index]
    vgs_vth = vgs_vth[index]
    if (err is True):
        error = rc_std[index]


   
    cmt = ""
    cmt2 = ""
    comment[0] = str(cmt + cmt2)

    cmt = ""
    cmt2 = ""
    comment[2] = str(cmt + cmt2)

    fig_rc = Grp_2D([vgs_vth],
                    [rc],
                    col=['b'],
                    style=style, eng_units=True,
                    D_Top_Axis=True, log_skip=0,
                    title="MSM IV Curve",
                    x_label=x_label,
                    x_limits=x_limits,
                    y_label=r"$J$",
                    y_limits=y_limits,
                    d_label=d_label,
                    cmmt_1=comment[0],
                    cmmt_2=comment[1],
                    cmmt_3=comment[2],
                    legend=[legend_line],
                    ox_th=ox_th, k_val=k_val,
                    x_prec=2, y_prec=1, d_prec=2,
                    units=["V", "A/cm^2", "V/nm"])

    # Plot triangle in the maximum point of mobility
    # Print the marker in the position where Rc error is minimum
    """
    fig_rc.ax.plot(vgs_vth[i_min_rc], min_rc, 'r^',
                   markeredgecolor='k',
                   markeredgewidth=2,
                   markerfacecolor='r',
                   markersize=9)
    """
    # Plotting of the error

    if (err is True):
        fig_rc.ax.fill_between(vgs_vth, rc*error, rc/error, alpha=0.2,
                               edgecolor='#1B2ACC', facecolor='#089FFF',
                               linewidth=4, linestyle='dashdot',
                               antialiased=True)

    plt.show()

    return fig_rc