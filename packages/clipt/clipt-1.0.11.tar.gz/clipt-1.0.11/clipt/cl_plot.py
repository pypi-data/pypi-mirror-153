# -*- coding: utf-8 -*-

# Copyright (c) 2018 Stephen Wasilewski
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""console script for graphing data."""

from __future__ import print_function
from __future__ import division

import re
import numpy as np

from past.utils import old_div
from clasp import click
import matplotlib.colors as mplc
from matplotlib.patches import Wedge

import clasp.click_ext as clk

from clipt import get_root, __version__
import clasp.script_tools as mgr
import clipt.plot as ruplot


@click.group()
@clk.shared_decs(clk.main_decs(__version__))
def plot(ctx, config, outconfig, configalias, inputalias):
    """scripts for plotting data from the command line."""
    template = get_root() + "/templates/master.cfg"
    clk.get_config(ctx, config, outconfig, configalias, inputalias, template)

main = plot # backwards compatibility


coloropt = [
          click.option('-fcol', default=0.0, type=float,
                       help="colormap position for first color"),
          click.option('-colors', default='viridis',
                       callback=clk.color_inp,
                       help="cmap name or space seperated list of rgb tuples "
                       "0,0,0 120,120,120 etc. if fewer than # series picks ."
                       "from gradient includes ru_colors: 'blu', 'org', 'pur'"
                       ", 'red', 'blg', 'mag', 'brn', 'grn', 'yel', 'ggr', "
                       "'dark', 'med', 'light', 'xlight'"),
          click.option('-positions', default=None,
                       callback=clk.split_float,
                       help="if cmap is a list positions are the mapping "
                       "points else positions are the sample points used to "
                       "remap"),
          click.option('-step', default=None, type=int,
                       help="steps for color map"),
]

# used by all
shared = coloropt + [
          click.option('-drange', callback=clk.split_int,
                       help="index range for data series, if None gets all"),
          click.option('--ticklines/--no-ticklines', default=False,
                       help="plot tick lines"),
          click.option('--areaonly/--no-areaonly', default=False,
                       help="only plot plot area, no legend or axes, for use "
                       "as background"),
          click.option('-fg', default="black",
                       help="foreground color"),
          click.option('-bg', default="white",
                       help="background color"),
          click.option('--legend/--no-legend', default=False,
                       help="include legend in plot"),
          click.option('-xrotate', default='auto', callback=clk.char0, type=click.Choice(['auto', 'horiz', 'vert', 'a', 'h', 'v'], case_sensitive=False),
                       help="orientation of x-axis labels"),
          click.option('-comment', default='#',
                       help='regex "^[{}].*" indicating comment line '
                       'indicator'),
          click.option('-labelweight', default='ultralight', type=click.Choice(['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']),
                       help="text weight for axes labels"),
          click.option('-width', default=5.0, type=float,
                       help="image width"),
          click.option('-height', default=5.0, type=float,
                       help="image height"),
          click.option('-dpi', default=200, type=int,
                       help="image dpi"),
          click.option('-background', type=click.Path(exists=True),
                       help="background image for graph area"),
          click.option('-alpha', type=float, default=.5,
                       help="transparency for background"),
          click.option('-format', default='.png',
                       help="output file format for default naming (overridden by outf)"),
          click.option('--front/--no-front', default=False,
                       help="plot background in front of data"),
          click.option('--opts', '-opts', is_flag=True,
                       help="check parsed options"),
          click.option('--debug', is_flag=True,
                       help="show traceback on exceptions"),
          click.option('-outf',
                       help="graph output file (defaults to basename of first "
                       "dataf)"),
          click.option('--weatherfile/--no-weatherfile', default=False,
                       help="input files will be read as weather files: "
                       "0 month, 1 day, 2 hour, 3 dirnorn, 4 difhoriz, 5 "
                       "globhoriz, 6 skycover")
]


# used by bar, scatter, histo
sharedA = [
           click.option('--xgrid/--no-xgrid', default=True,
                        help="plot x grid lines"),
           click.option('--ygrid/--no-ygrid', default=True,
                        help="plot y grid lines"),
           click.option('-yticks', type=int,
                        help="number of y-ticks/gridlines"),
           click.option('-xticks', type=int,
                        help="number of x-ticks/gridlines"),
           click.option('--polar/--no-polar', default=False,
                        help="plot on polar axes"),
           click.option('-labels', callback=clk.split_str,
                        help="input custom series labels, by default uses "
                        "file name and index or --header option"),
           click.option('--rows/--no-rows', default=False,
                        help="get data rows instead of columns"),
           click.option('-ecolors', default="viridis", callback=clk.color_inp,
                        help="marker edge colors"),
           click.option('-epositions', default=None,
                        callback=clk.split_float,
                        help="if cmap is a list positions are the mapping "
                        "pointselse positions are the sample points used to "
                        "remap"),
           click.option('-estep', default=None, type=int,
                        help="steps for color map"),
           click.option('--ylog/--no-ylog', default=False,
                        help="plot y on log scale"),
           click.option('--header/--no-header', default=False,
                        help="indicates that data has a header row to get "
                        "series labels (overridden by labels)"),
           click.option('-bottom', type=float, default=0.0,
                        help="use with polar to set bottom of y-axis same "
                        "units as axes")
]


# used by scatter, heatmap
sharedB = [
]


@plot.command('bar')
@click.argument('dataf', callback=clk.are_files)
@click.option('-rwidth', default=0.95, type=float,
              help="relative width of bar clusters")
@click.option('-bwidth', default=.8, type=float,
              help="relative width of bars")
@click.option('--stacked/--no-stacked', default=False,
              help="make stacked bars")
@click.option('-ew', default="0", callback=clk.split_float,
              help="bar edge width")
@click.option('-brng', default="0 1", callback=clk.split_float,
              help="range within axes limits that bars are plotted")
@click.option('--polar0/--no-polar0', default=True,
              help="plot center of first bar at xmin")
@click.option('--polarauto/--no-polarauto', default=True,
              help="ignore x-axis min,max and plot 0-360")
@click.option('-y_vals', default="-1", callback=clk.split_int,
              help="index for yvals")
@click.option('-axes', default="X,0,10,Y,0,ymax",
              help="enter as xname,xmin,xmax,yname,ymin,ymax - default uses"
              "min and max of data enter xmin etc to maintain autoscale")
@click.option('-xlabels', callback=clk.split_str,
              help="input custom xaxis labels, by default uses file name and"
              "row number or --xheader option")
@click.option('--xheader/--no-xheader', default=False,
              help="indicates that data has a header column to get x-axis "
              "labels (overridden by xlabels)")
@clk.shared_decs(shared + sharedA)
@click.pass_context
def bar(ctx, dataf, **kwargs):
    '''
    dataf should be a tsv or csv with the following format: xaxis label,
    series1 ,series2, etc.. category1, 0,0,... category2, 0,0,... etc...,...

    arguments:

    * dataf: data file to plot
    '''
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            axext = ruplot.get_axes(kwargs['axes'], [], [], kwargs['polar'],
                                    kwargs['polarauto'])
            a1 = mgr.kwarg_match(mgr.read_data, kwargs)
            a1['autox'] = axext['xdata']
            xs, ys, labels = mgr.read_all_data(dataf, **a1)
            labels, xlabels = ruplot.get_labels(dataf, labels, a1, len(ys[0]), **kwargs)
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            a4['xlabels'] = xlabels
            ax = ruplot.tick_from_arg(ax, xs, ys, a4, kwargs)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            cmap = ruplot.get_colors(kwargs['colors'], **a5)
            a5['positions'] = kwargs['epositions']
            a5['step'] = kwargs['estep']
            emap = ruplot.get_colors(kwargs['ecolors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_bar, kwargs)
            a6['emap'] = emap
            a6.pop('labels', None)
            ax, handles = ruplot.plot_bar(ax, xs, ys, labels, cmap, **a6)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf[0].rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            ruplot.plot_graph(fig, outf, handles=handles, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'bar', kwargs, ctx


@plot.command('heatmap')
@click.argument('dataf', callback=clk.is_file)
@click.option('-pph', default=1, type=int,
              help="data points per hour in annual data")
@click.option('-hpd', default=24, type=int,
              help="hours per day (y axis shape)")
@click.option('-dpy', default=365, type=int,
              help="days per year (x axis shape)")
@click.option('-sh', default=0, type=int,
              help="start hour (24 hour time)")
@click.option('-plotidx', default=-1, type=int,
              help="column idx of data to plot")
@click.option('-vmax', type=float,
              help="scale max")
@click.option('-vmin', type=float,
              help="scale max")
@click.option('-lw', default=.5, type=float,
              help="lineweight of grid around cells (try .5)")
@click.option('-gridc', default=.5, type=float,
              help="opacity of gridlines (color is bg)")
@click.option('--dst/--no-dst', default=False,
              help="shift data for DST")
@click.option('-labels', callback=clk.split_str,
              help="labels for legend")
@click.option('-ticks', callback=clk.split_float,
              help="locations for legend labels (must be same # of items)")
@clk.shared_decs(shared + sharedB)
@click.pass_context
def heatmap(ctx, dataf, **kwargs):
    '''def plot_heatmap(fig, ax, data, colormap, vmin=None, vmax=None,
                 DST=False, ticks=None, labels=None, **kwargs)'''
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            if (dataf.split('.')[-1] in ['epw', 'wea'] and
                kwargs['comment'] == '#'):
                kwargs['comment'] = '^\-\d'
            y_vals = [kwargs['plotidx']]
            _, ys, _ = mgr.read_data(dataf, y_vals=y_vals,
                                     comment=kwargs['comment'],
                                     autox=(0, kwargs['dpy']),
                                     weatherfile=kwargs['weatherfile'])
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            ax = ruplot.ticks(ax, annualx=True, dayy=True, **a4)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            colormap = ruplot.get_colors(kwargs['colors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_heatmap, kwargs)
            a6['legend'] = a6['legend'] and not kwargs['areaonly']
            edgecolor = list(mplc.to_rgba(kwargs['bg']))
            edgecolor[3] = kwargs['gridc']
            a6.update({'lw': kwargs['lw'], 'edgecolors': edgecolor})
            ax = ruplot.plot_heatmap(fig, ax, ys[0], colormap, **a6)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf.rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            ruplot.plot_graph(fig, outf, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'heatmap', kwargs, ctx


@plot.command('histo')
@click.argument('dataf', callback=clk.are_files)
@click.option('-y_vals', default="-1", callback=clk.tup_int,
              help="index for yvals")
@click.option('-weights', default=None, callback=clk.tup_int,
              help="index for weights (if given, must be 1:1 match with y_vals)")
@click.option('-axes', default="X,0,1,Y,0,ymax",
              help="enter as xname,xmin,xmax,yname,ymin,ymax - default uses"
              "min and max of data enter xmin etc to maintain autoscale")
@click.option('-bins', default=None, callback=clk.split_float,
              help="bins can be 'auto' an integer or a sequence"
              "1 2 3 4:12:2 14:16 = 1,2,3,4,6,8,10,14,15")
@click.option('-autobin', default='auto',
              help="see numpy.histogram_bin_edges for options"
              "1 2 3 4:12:2 14:16 = 1,2,3,4,6,8,10,14,15")
@click.option('-brange', default=None, callback=clk.split_float,
              help="defaults to min and max")
@click.option('--tails/--no-tails', default=False,
              help="include values below and above range in first and last bin"
              "(requires -brange)")
@click.option('-rwidth', default=0.95, type=float,
              help="relative width of bars")
@click.option('-bwidth', default=.8, type=float,
              help="relative width of bars")
@click.option('--stacked/--no-stacked', default=False,
              help="make stacked bars")
@click.option('--density/--no-density', default=False,
              help="plot as probability density (area sums to 1)")
@click.option('-xlabels', callback=clk.split_str,
              help="input custom xaxis labels, by default uses file name and"
              "row number or --xheader option")
@click.option('--xheader/--no-xheader', default=False,
              help="indicates that data has a header column to get x-axis "
              "labels (overridden by xlabels)")
@clk.shared_decs(shared + sharedA)
@click.pass_context
def histo(ctx, dataf, **kwargs):
    '''
    plot histogram bar plot
'''
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            axext = ruplot.get_axes(kwargs['axes'], [], [])
            a1 = mgr.kwarg_match(mgr.read_data, kwargs)
            a1['autox'] = axext['xdata']
            xs, ys, labels = mgr.read_all_data(dataf, **a1)
            labels, xlabels = ruplot.get_labels(dataf, labels, a1, len(ys[0]), **kwargs)
            if kwargs['weights'] is not None:
                a1['y_vals'] = kwargs['weights']
                _, weights, _ = mgr.read_all_data(dataf, **a1)
            else:
                weights = None
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            a4['xlabels'] = xlabels
            ax = ruplot.tick_from_arg(ax, xs, ys, a4, kwargs)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            cmap = ruplot.get_colors(kwargs['colors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_histo, kwargs)
            a6.pop('labels', None)
            if kwargs['bins'] is None:
                a6['bins'] = kwargs['autobin']
            elif len(kwargs['bins']) == 1:
                a6['bins'] = int(kwargs['bins'][0])
            a6['weights'] = weights
            ax, handles = ruplot.plot_histo(ax, ys, labels, cmap,
                                            axext['ydata'], **a6)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf[0].rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            ruplot.plot_graph(fig, outf, handles=handles, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'histo', kwargs, ctx


def wedge_mark(d, s):
    t1 = d - s/2
    t2 = d + s/2
    wd = Wedge(0, 1, t1, t2).get_path()
    return ruplot.WedgeMark(wd, np.array([t1, d, t2]))


def parse_mark(ctx, param, s):
    if s in [None, 'None', 'none']:
        result = None
    else:
        result = []
        for part in s.split():
            try:
                a = int(part)
            except ValueError:
                if re.match(r"w\.\d+\.\d+", part):
                    a = wedge_mark(*[int(i) for i in part.split(".")[1:]])
                else:
                    a = part
            result.append(a)
    return result


@plot.command('scatter')
@click.argument('dataf', callback=clk.are_files)
@click.option('-autox', default=None,
              callback=clk.split_float,
              help="auto assign xvals between min,max from axes")
@click.option('-weax', default=None, callback=clk.split_int,
              help="use months as x-axis (8760 data) give idx for month and"
              "day ex: 1 2 for epw 0 1 for wea"
              "when using --weatherfile use 0 1 for both")
@click.option('-x_vals', default="0,0",
              callback=clk.tup_int, help="index for xvals")
@click.option('-y_vals', default="-1", callback=clk.tup_int,
              help="index for yvals")
@click.option('-area', default=None, callback=clk.tup_int, multiple=True,
              help="give as single value (fills to y-min) or 2 values "
              "(fills between) order given should match y_vals. colors"
              " match line colors, but use the -falpha option")
@click.option('-c_vals', default=None, callback=clk.tup_int,
              help="optional index for color vals")
@click.option('-falpha', type=float, default=0.5,
              help="alpha for -area(s)")
@click.option('-m_vals', default=None, callback=clk.tup_int,
              help="optional index for marker size vals, only uses 1 index"
                   " values should be prescaled to marker size output")
@click.option('-cmax', type=float,
              help="scale max for color")
@click.option('-cmin', type=float,
              help="scale min for color")
@click.option('-mmax', type=float,
              help="max for marker size")
@click.option('-mmin', type=float,
              help="min for marker size")
@click.option('--flipxy/--no-flipxy', default=False,
              help="plot x on vertical axis")
@click.option('--polarauto/--no-polarauto', default=True,
              help="ignore x-axis min,max and plot 0-360")
@click.option('-axes', default="X,xmin,xmax,Y,ymin,ymax",
              help="enter as xname,xmin,xmax,yname,ymin,ymax - default uses"
              "min and max of data enter xmin etc to maintain autoscale")
@click.option('--xlog/--no-xlog', default=False,
              help="plot x on log scale")
@click.option('--diagonal/--no-diagonal', default=False,
              help="add diagonal gridline")
@click.option('--matchxy/--no-matchxy', default=False,
              help="use same range for x and y")
@click.option('-pery', default=None, type=int,
              help="label y-axis by percentile with N bins")
@click.option('--reverse/--no-reverse', default=False,
              help="reverse order of y data (sometimes useful with -autox)")
@click.option('-ms', default="2", callback=clk.split_float,
              help="marker size if fewer than # series uses last")
@click.option('-mew', default="0", callback=clk.split_float,
              help="marker edge width")
@click.option('-mrk', default='o', callback=parse_mark,
              help="marker style if fewer than # series loops")
@click.option('-criteria',
              help="plot markers based on criteria (either x=VAL or y=VAL)"
              "assumes single solution")
@click.option('-y2', callback=clk.split_int,
              help="idx positions (order from -y_vals) to plot on secondary y-axis")
@click.option('-axes2', default="y,ymin,ymax",
              help="enter as ymin,ymax - default uses"
              "min and max of data from y2")
@click.option('-lw', default="2", callback=clk.split_float,
              help="line weight if fewer than # series uses last")
@clk.shared_decs(shared + sharedA + sharedB)
@click.pass_context
def scatter(ctx, dataf, **kwargs):
    '''arguments for x_vals and y_vals are a space seperated list of indices or
    index pairs. A single number is applied to all files, a comma seperated
    pair: i,j gets the jth column from the ith file. if a tuple x_val is given
    all y_data will share, else x will be index value from each file.  for
    y_val entry a single number will grab from all files, a comma pair gets one
    column of data.  use the argument -rows to get data by rows instead.'''
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            a1 = mgr.kwarg_match(mgr.read_data, kwargs)
            if kwargs['weax'] is not None:
                a1['x_vals'] = [0]
            xs, ys, labels = mgr.read_all_data(dataf, **a1)
            if kwargs['c_vals'] is not None:
                a1['y_vals'] = kwargs['c_vals']
                _, cs, _ = mgr.read_all_data(dataf, **a1)
            else:
                cs = None
            if kwargs['m_vals'] is not None:
                a1['y_vals'] = kwargs['m_vals']
                msd = mgr.read_all_data(dataf, **a1)[1]
            else:
                msd = None
            areas = []
            if kwargs['area'] is not None:
                a1['x_vals'] = []
                for a in kwargs['area']:
                    a1['y_vals'] = a
                    areas.append(mgr.read_all_data(dataf, **a1)[1])
            labels = ruplot.get_user_labels(labels, kwargs['labels'])
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            if kwargs['y2'] is not None:
                axes = kwargs['axes']
                kwargs['axes'] = axes.rsplit(',', 3)[0] + ',' + kwargs['axes2']
                ax2 = ax.twinx()
                ax2 = ruplot.tick_from_arg(ax2, xs, [ys[i] for i in kwargs['y2']], a4, kwargs)
                fig.sca(ax2)
                kwargs['axes'] = axes
                ax = ruplot.tick_from_arg(ax, xs, [ys[i] for i in range(len(ys)) if i not in kwargs['y2']] + areas, a4, kwargs)
            else:
                ax = ruplot.tick_from_arg(ax, xs, ys + areas, a4, kwargs)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            cmap = ruplot.get_colors(kwargs['colors'], **a5)
            a5['positions'] = kwargs['epositions']
            a5['step'] = kwargs['estep']
            emap = ruplot.get_colors(kwargs['ecolors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_scatter, kwargs)
            a6.pop('labels', None)
            a6['legend'] = kwargs['legend'] and not kwargs['areaonly']
            ax, handles, handles2 = ruplot.plot_scatter(fig, ax, xs, ys, labels, cmap,
                                                        emap=emap, cs=cs, msd=msd,
                                                        areas=areas, **a6)
            if kwargs['diagonal']:
                ax.plot(ax.get_xlim(), ax.get_ylim(), lw=0.6, ls='--', color='black', ms=0)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf[0].rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            if cs is not None:
                a7['legend'] = False
            if len(handles2) > 0:
                bba = (1.1, 1)
            else:
                bba = (1.05, 1)
            ruplot.plot_graph(fig, outf, handles=handles, handles2=handles2, bbox_to_anchor=bba, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'scatter', kwargs, ctx


@plot.command('box')
@click.argument('dataf', callback=clk.are_files)
@click.option('-y_vals', default="-1", callback=clk.tup_int,
              help="index for yvals")
@click.option('-axes', default="X,0,1,Y,0,ymax",
              help="enter as xname,xmin,xmax,yname,ymin,ymax - default uses"
              "min and max of data enter xmin etc to maintain autoscale")
@click.option('-rwidth', default=0.95, type=float,
              help="relative width of boxs")
@click.option('-xlabels', callback=clk.split_str,
              help="input custom xaxis labels, by default uses file name and"
              "row number or --xheader option")
@click.option('-mark', default='x',
              help="mark for flyers")
@click.option('-ms', default=3.0,
              help="size for flyers")
@click.option('-mew', default=.5,
              help="edge weight for flyers")
@click.option('-lw', default=1.,
              help="linewidth for box and whiskers")
@click.option('-clw', default=1.,
              help="linewidth for median line")
@click.option('-series', default=1,
              help="number of series to plot data in")
@click.option('-whis', default='1.5', callback=clk.split_float,
              help="adapted from matplotlib documentation: As a single number,"
                   "determines the reach of the whiskers to the beyond the "
                   "first and third quartiles. In other words, where IQR is "
                   "the interquartile range (Q3-Q1), the upper whisker will "
                   "extend to last datum less than Q3 + whis*IQR). "
                   "Similarly, the lower whisker will extend to the first "
                   "datum greater than Q1 - whis*IQR. Beyond the whiskers, "
                   "data are considered outliers and are plotted as individual "
                   "points. As two numbers, set this to an ascending sequence "
                   "of percentile (e.g., [5, 95]) to set the whiskers at "
                   "specific percentiles of the data. ignored if --no-fliers")
@click.option('--clbg/--no-clbg', default=True,
              help="median line uses -bg")
@click.option('-fillalpha', default=1.0,
              help="alpha for fill color (matches line color)")
@click.option('--xheader/--no-xheader', default=False,
              help="indicates that data has a header column to get x-axis "
              "labels (overridden by xlabels)")
@click.option('--xgrid/--no-xgrid', default=False,
              help="plot x grid lines")
@click.option('--ygrid/--no-ygrid', default=False,
              help="plot y grid lines")
@click.option('-yticks', type=int,
              help="number of y-ticks/gridlines")
@click.option('-labels', callback=clk.split_str,
              help="input custom x-axis labels, by default uses "
              "file name and index or --header option")
@click.option('--rows/--no-rows', default=False,
              help="get data rows instead of columns")
@click.option('--ylog/--no-ylog', default=False,
              help="plot y on log scale")
@click.option('--mean/--median', default=False,
              help="plot mean line or median line")
@click.option('--notch/--no-notch', default=False,
              help="plot notch for 95\% confidence interval")
@click.option('--fliers/--no-fliers', default=True,
              help="plot notch for 95\% confidence interval")
@click.option('--inline/--no-inline', default=False,
              help="keep boxes inline")
@click.option('--header/--no-header', default=False,
              help="indicates that data has a header row to get "
              "series labels (overridden by labels)")
@clk.shared_decs(shared)
@click.pass_context
def box(ctx, dataf, **kwargs):
    """
    create boxplot from data files.
    """
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            axext = ruplot.get_axes(kwargs['axes'], [], [])
            a1 = mgr.kwarg_match(mgr.read_data, kwargs)
            a1['autox'] = [0, 1]
            xs, ys, labels = mgr.read_all_data(dataf, **a1)
            labels, xlabels = ruplot.get_labels(dataf, labels, a1, len(ys[0]), **kwargs)
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            a4['xlabels'] = xlabels
            ax = ruplot.tick_from_arg(ax, [0, len(ys[0])], ys, a4, kwargs)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            cmap = ruplot.get_colors(kwargs['colors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_box, kwargs)
            a6.pop('labels', None)
            a6['xlabels'] = xlabels
            if len(a6['whis']) == 1:
                a6['whis'] = a6['whis'][0]
            else:
                a6['whis'] = (a6['whis'][0], a6['whis'][-1])
            ax, handles = ruplot.plot_box(ax, ys, labels, cmap,
                                            axext['ydata'], **a6)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf[0].rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            ruplot.plot_graph(fig, outf, handles=handles, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'box', kwargs, ctx


@plot.command('violin')
@click.argument('dataf', callback=clk.are_files)
@click.option('-y_vals', default="-1", callback=clk.tup_int,
              help="index for yvals")
@click.option('-weights', default=None, callback=clk.tup_int,
              help="index for weights (if given, must be 1:1 match with y_vals)")
@click.option('-axes', default="X,0,1,Y,ymin,ymax",
              help="enter as xname,xmin,xmax,yname,ymin,ymax - default uses"
              "min and max of data enter xmin etc to maintain autoscale")
@click.option('-rwidth', default=0.95, type=float,
              help="relative width of boxs")
@click.option('-xlabels', callback=clk.split_str,
              help="input custom xaxis labels, by default uses file name and"
              "row number or --xheader option")
@click.option('-lw', default=1.,
              help="linewidth for extrema and vertical line")
@click.option('-clw', default=1.,
              help="linewidth for median line")
@click.option('-series', default=1,
              help="number of series to pl ot data in")
@click.option('--clbg/--no-clbg', default=True,
              help="median line uses -bg")
@click.option('-conf', default=None, type=float,
              help="plot confidence interval on data")
@click.option('-confm', default=None, type=float,
              help="plot confidence interval on mean of data")
@click.option('-kernelwidth', '-kw', default=.5,
              help="scale factor to apply to kernel bandwidth selector (1 uses scotts rule)")
@click.option('-fillalpha', default=.5,
              help="alpha for fill color (matches line color)")
@click.option('-weightlimit', default=0.0,
              help="exclude values below weight limit from plot (useful to remove artificial whiskers)")
@click.option('--xheader/--no-xheader', default=False,
              help="indicates that data has a header column to get x-axis "
              "labels (overridden by xlabels)")
@click.option('--xgrid/--no-xgrid', default=False,
              help="plot x grid lines")
@click.option('--ygrid/--no-ygrid', default=False,
              help="plot y grid lines")
@click.option('-yticks', type=int,
              help="number of y-ticks/gridlines")
@click.option('-labels', callback=clk.split_str,
              help="input custom x-axis labels, by default uses "
              "file name and index or --header option")
@click.option('--rows/--no-rows', default=False,
              help="get data rows instead of columns")
@click.option('--ylog/--no-ylog', default=False,
              help="plot y on log scale")
@click.option('--mean/--no-mean', default=False,
              help="plot mean dot")
@click.option('--median/--no-median', default=True,
              help="plot median line")
@click.option('--fliers/--no-fliers', default=False,
              help="plot outliers as fliers")
@click.option('--inline/--no-inline', default=False,
              help="keep violins inline")
@click.option('--header/--no-header', default=False,
              help="indicates that data has a header row to get "
              "series labels (overridden by labels)")
@clk.shared_decs(shared)
@click.pass_context
def violin(ctx, dataf, **kwargs):
    """
    create violinplot from data files.
    """
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(dataf, **kwargs)
    else:
        try:
            axext = ruplot.get_axes(kwargs['axes'], [], [])
            a1 = mgr.kwarg_match(mgr.read_data, kwargs)
            a1['autox'] = [0, 1]
            xs, ys, labels = mgr.read_all_data(dataf, **a1)
            labels, xlabels = ruplot.get_labels(dataf, labels, a1, len(ys[0]), **kwargs)
            if kwargs['weights'] is not None:
                a1['y_vals'] = kwargs['weights']
                _, weights, _ = mgr.read_all_data(dataf, **a1)
            else:
                weights = None
            a3 = mgr.kwarg_match(ruplot.plot_setup, kwargs)
            ax, fig = ruplot.plot_setup(**a3)
            a4 = mgr.kwarg_match(ruplot.ticks, kwargs)
            a4.pop('labels', None)
            a4['xlabels'] = xlabels
            ax = ruplot.tick_from_arg(ax, [0, len(ys[0])], ys, a4, kwargs)
            a5 = mgr.kwarg_match(ruplot.get_colors, kwargs)
            cmap = ruplot.get_colors(kwargs['colors'], **a5)
            a6 = mgr.kwarg_match(ruplot.plot_violin, kwargs)
            a6.pop('labels', None)
            a6['weights'] = weights
            ax, handles = ruplot.plot_violin(ax, ys, labels, cmap,
                                             axext['ydata'], **a6)
            a4['xdata'] = ax.get_xlim()
            a4['ydata'] = ax.get_ylim()
            ax = ruplot.ticks(ax, **a4)
            if kwargs['outf']:
                outf = kwargs['outf']
            else:
                outf = dataf[0].rsplit(".", 1)[0] + kwargs['format']
            a7 = mgr.kwarg_match(ruplot.plot_graph, kwargs)
            ruplot.plot_graph(fig, outf, handles=handles, **a7)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'violin', kwargs, ctx


@plot.command('previewpal')
@click.option('-n', default=4,
              help="number of series to draw from colormap")
@click.option('--colorbar/--series', default=False,
              help="whether to preview colorbar (continuous) or series"
              " (category) scale)")
@click.option('-outf', default='previewpal.png')
@click.option('--opts', '-opts', is_flag=True,
             help="check parsed options")
@click.option('--debug', is_flag=True,
             help="show traceback on exceptions")
@clk.shared_decs(coloropt)
def previewpal(**kwargs):
    """
    create plot color palettes and formatted rgbs
    """
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(**kwargs)
    else:
        try:
            step = kwargs['step']
            positions = kwargs['positions']
            fcol = kwargs['fcol']
            n = kwargs['n']
            colors = kwargs['colors']
            cmap = ruplot.get_colors(colors, step=step, positions=positions)
            ax, fig = ruplot.plot_setup(areaonly=True)
            if kwargs['colorbar']:
                ruplot.add_colorbar(fig, cmap, axes = [0, 0, 1, 1])
                ax.remove()
            else:
                inc = ruplot.color_inc(fcol, step, n)
                for i in range(n):
                    cinc = ruplot.color_inc_i(fcol, i, n, step)
                    c = cmap.to_rgba(cinc)
                    try:
                        p = .05 + i * .9/(n-1)
                    except ZeroDivisionError:
                        p = .5
                    ax.plot([p,p], [0,1], color=c, lw=4)
            ruplot.plot_graph(fig, kwargs['outf'], width=4, height=2,
                              areaonly=True)
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'previewpal', kwargs


@plot.command('colors')
@click.option('-outf',
              help="output file")
@click.option('--ru/--mat', default=True,
              help="plot radutil colors (--mat plots matplotlib)")
@click.option('--rgb/--no-tgb', default=True,
              help="print rgb values for radutil")
@click.option('--radf/--no-radf', default=False,
              help="print rgb values on 0-1 scale")
@click.option('-mpal',
              help="matplotlib palette to print r,g,b vals")
@click.option('-mpaldiv', default=10,
              help="number of segments")
@click.option('--opts', '-opts', is_flag=True,
              help="check parsed options")
@click.option('--debug', is_flag=True,
              help="show traceback on exceptions")
@clk.shared_decs(coloropt)
def colors(**kwargs):
    """
    create plot color palettes and formatted rgbs
    """
    if kwargs['opts']:
        kwargs['opts'] = False
        clk.echo_args(**kwargs)
    else:
        try:
            if kwargs['outf'] is not None:
                fig = ruplot.plot_cmaps(kwargs['ru'])
                ruplot.plot_graph(fig, kwargs['outf'], width=5, height=10)
            else:
                click.echo("specify -outf to generate image", err=True)
            if kwargs['rgb'] and kwargs['ru']:
                rucol = ruplot.CliptColors()
                click.echo("      " + "".join(["{: <13}".format(i)
                                               for i in rucol.shades]))
                for k in rucol.colors:
                    v = rucol.cdict255[k]
                    fmt = [",".join(["{:03d}".format(j) for j in i])
                           for i in v]
                    click.echo("{}:  {}".format(k, "  ".join(fmt)))
                click.echo("\n         " + "".join(["{: <13}".format(i)
                                                    for i in rucol.colors]))
                for k in rucol.shades:
                    v = rucol.cdict255[k]
                    fmt = [",".join(["{:03d}".format(j) for j in i])
                           for i in v]
                    click.echo("{: >6}:  {}".format(k, "  ".join(fmt)))
                if kwargs['radf']:
                    click.echo("      " + "".join(["{: <28}".format(i)
                                                   for i in rucol.shades]))
                    for k in rucol.colors:
                        v = rucol.cdict255[k]
                        fmt = [" ".join(["{:06f}".format(old_div(j,255.)**2.2)
                                         for j in i]) for i in v]
                        click.echo("{}:  {}".format(k, "  ".join(fmt)))
            if kwargs['mpal'] is not None:
                cmap = ruplot.get_colors(kwargs['mpal'])
                click.echo("\ncolor palette: {} in {} steps:".format(kwargs['mpal'], kwargs['mpaldiv']))
                mpc = []
                for i in range(kwargs['mpaldiv']):
                    c = cmap.to_rgba(i/(kwargs['mpaldiv'] - 1.0))
                    mpc.append("({},{},{})".format(*[int(j*255) for j in c[0:3]]))
                print(f"[{','.join(mpc)}]")
                print(" ".join(mpc).replace("(", "").replace(")", ""))
                if kwargs['radf']:
                    click.echo("\n ungammad 0-1:")
                    for i in range(kwargs['mpaldiv']):
                        c = cmap.to_rgba(i/(kwargs['mpaldiv'] - 1.0))
                        click.echo("{:06f} {:06f} {:06f}".format(*[j**2.2 for j in c[0:3]]))
                    
        except click.Abort:
            raise
        except Exception as ex:
            clk.print_except(ex, kwargs['debug'])
    return 'colors', kwargs


@plot.resultcallback()
@click.pass_context
def printconfig(ctx, opts, **kwargs):
    """callback to save config file"""
    try:
        clk.tmp_clean(opts[2])
    except Exception:
        pass
    if kwargs['outconfig']:
        clk.print_config(ctx, opts, kwargs['outconfig'], kwargs['config'],
                         kwargs['configalias'])


if __name__ == '__main__':
    main()