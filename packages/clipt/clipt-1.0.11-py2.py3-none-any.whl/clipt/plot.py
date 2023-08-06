# -*- coding: utf-8 -*-

# Copyright (c) 2018 Stephen Wasilewski
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""functions for plotting with matplotlib"""

from __future__ import print_function
from __future__ import division

from builtins import str
from builtins import zip
from builtins import range
from builtins import object
from past.utils import old_div
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Circle, Patch
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.transforms import Bbox
import clasp.script_tools as mgr
from hdrstats import hdrstats as hs

daycount = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def tick_from_arg(ax, xs, ys, a4, kwargs):
    """sets ticks based on standard argument parsing

    Parameters
    ----------
    ax: matplotlib subplot
    a4: kwargs for ticks
    kwargs: input arguments
    Returns
    -------
    ax: matplotlib subplot
    """
    if 'pery' not in kwargs:
        pery = False
    else:
        pery = kwargs['pery'] is not None
    try:
        if kwargs['xlog']:
            a4['xscale'] = 'log'
    except Exception:
        pass
    try:
        if kwargs['ylog']:
            a4['yscale'] = 'log'
    except Exception:
        pass
    try:
        if kwargs['weax'] is not None:
            a4['annualx'] = True
    except Exception:
        pass
    try:
        a4['tcol'] = kwargs['fg']
    except Exception:
        pass
    for i in ['polar', 'stacked', 'polarauto']:
        try:
            kwargs[i] = kwargs[i]
        except Exception:
            kwargs[i] = False
    try:
        a4.update(get_axes(kwargs['axes'], xs, ys, kwargs['polar'],
                           kwargs['polarauto'], kwargs['stacked'], pery=pery))
    except Exception as ex:
        try:
            a4.update(get_axes(kwargs['axes'], xs, ys, kwargs['polar'], stacked=kwargs['stacked'], pery=pery))
        except Exception as ex: 
            raise
            pass
    ax = ticks(ax, **a4)
    return ax


def get_user_labels(labels, mlab):
    """returns data based on standard argument parsing

    Parameters
    ----------
    labels: list
        labels returned by read_all_data
    mlab: list
        manual labels for data
    Returns
    -------
    labels: list
        list of labels for each y_val
    """
    if mlab is not None:
        for i, l in enumerate(mlab):
            try:
                labels[i] = l
            except Exception:
                labels.append(l)
    return labels


def get_labels(dataf, labs, a1, ycnt, xheader=False, xlabels=None,
               labels=None, rows=False, drange=None, y_vals=[-1,],
               **kwargs):
    if xheader:
        a1['y_vals'] = [0]
        a1['x_vals'] = []
        a1['coerce'] = False
        a1['xheader'] = False
        a1['drange'] = None
        a1['rows'] = False
        _, xlabs, _ = mgr.read_data(dataf[0], **a1)
        xlabs = xlabs[0]
    else:
        xlabs = []
    xlabs = get_user_labels(xlabs, xlabels)
    labs = get_user_labels(labs, labels)
    if rows:
        # if drange is not None:
        #     try:
        #         la = [labs[i] for i in drange]
        #     except IndexError:
        #         la = []
        # else:
        la = labs[:ycnt]
        labs = []
        for i in y_vals:
            try:
                labs.append(xlabs[i[1]])
            except TypeError:
                try:
                    labs.append(xlabs[i])
                except IndexError:
                    pass
                
        xlabs = la
    # elif drange is not None:
    #     try:
    #         xlabs = [xlabs[i] for i in drange]
    #     except IndexError:
    #         xlabs = []
    return labs, xlabs

def ax_limits(x):
    def smin(x):
        try:
            return min(x)
        except Exception:
            return None

    def smax(x):
        try:
            return max(x)
        except Exception:
            return None
    return smin(x), smax(x)


def get_axes(arg, xs, ys, polar=False, polarauto=True, stacked=False, pery=False, **kwargs):
    """parse axes string argument xname,xmin,xmax,yname,ymin,ymax"""
    x = flat(xs)
    if stacked:
        try:
            y = [sum([i[j] for i in ys]) for j in range(len(ys[0]))]
        except:
            y = []
    else:
        y = flat(ys)
    axes = ['X', *ax_limits(x), 'Y', *ax_limits(y)]
    try:
        ax = arg.split(",")
        for i, v in enumerate(ax):
            if i in [0, 3]:
                axes[i] = v
            else:
                try:
                    axes[i] = float(v)
                except Exception:
                    pass
    except Exception:
        raise ValueError(arg)
    naxes = {'labels': [axes[0], axes[3]],
             'xdata': [axes[1], axes[2]],
             'ydata': [axes[4], axes[5]]}
    if pery:
        naxes['ydata'] = y
    if polar and polarauto:
        naxes['xdata'] = [0, 2*math.pi]
    elif polar:
        naxes['xdata'] = [old_div(axes[1]*math.pi,180), old_div(axes[2]*math.pi,180)]
    return naxes


def plot_setup(fg='black', bg='white', polar=False, areaonly=False, params={}, **kwargs):
    """
    setup plot with uniform styling and create axes for plot

    Parameters
    ----------
    fg: color
        foreground color
    bg: color
        background color
    polar: bool
        if true make polar plot
    params: dict
        rcParams to update
    Returns
    -------
    ax: matplotlib sublot
    fig: matplotlib figure
    """
    defparam = {
        'font.weight': 'ultralight',
        'font.family': 'sans-serif',
        'font.size': 7,
        'axes.linewidth': 0.5,
        'axes.edgecolor': fg
    }
    rcParams.update(defparam)
    fig = plt.figure()
    if areaonly:
        ax = fig.add_subplot(1, 1, 1, position=[0, 0, 1, 1], facecolor=bg,
                             polar=polar, frame_on=polar)
    else:
        ax = fig.add_subplot(1, 1, 1, facecolor=bg, polar=polar)
    return ax, fig


def series_ticks(ax, locs, xlabels, xrotate='a'):
    ax.set_xticks(locs)
    rots = dict(a='auto', h='horizontal', v='vertical')
    ro = rots[xrotate]
    if ro == 'auto':
        if max([len(i) for i in xlabels]) > 10:
            ro = 'vertical'
        else:
            ro = 'horizontal'
    ax.set_xticklabels(xlabels, rotation=ro)
    for t in ax.xaxis.get_ticklines():
        t.set_visible(False)

def ticks(ax, xdata=[0, 1], ydata=[0, 1], tcol='black', labels=['X', 'Y'],
          xgrid=True, ygrid=True, xscale='linear', yscale='linear',
          annualx=False, dayy=False, pery=False, ticklines=False, pph=1,
          bottom=None, bg='white', xlabels=None, dpy=365, hpd=24, sh=0,
          polar=False, xticks=None, yticks=None, labelweight='ultralight',
          matchxy=False, xrotate='a', **kwargs):
    """
    setup ticks/axes for plot

    Parameters
    ----------
    ax: matplotlib sublot
    xdata: list
        x data (or min and max)
    ydata: list
        y data (or min and max)
    tcol: color
        tick color
    labels: list
        x and y axis labels
    xgrid: bool
        show x grid
    ygrid: bool
        show y grid
    xscale: str
        linear or log
    yscale: str
        linear or log
    annualx: bool
        plot xaxis as full year with month labels
    dayy: bool
        plot yaxis as day with hour labels
    pery: bool/int
        if > 1 label y axis according to percentile of data with pery bins
    ticklines: bool
        if not grid, show ticklines
    """
    xmin = min(xdata)
    xmax = max(xdata)
    ymin = min(ydata)
    ymax = max(ydata)
    if matchxy:
        xmin = min(xmin, ymin)
        xmax = max(xmax, ymax)
        ymin = xmin
        ymax = xmax
    tcol = colors.to_rgba(tcol)
    ax.xaxis.grid(linestyle="-", linewidth=0.3, color=tcol)
    ax.yaxis.grid(linestyle="-", linewidth=0.3, color=tcol, zorder=1)
    ax.xaxis.grid(linestyle="--", linewidth=0.3, color=tcol, alpha=.2, which='minor')
    ax.yaxis.grid(linestyle="--", linewidth=0.3, color=tcol, alpha=.2, zorder=1, which='minor')
    ax.xaxis.grid(xgrid)
    ax.yaxis.grid(ygrid)
    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(bottom=ymin, top=ymax)
    ax.set_yscale(yscale)
    ax.set_xscale(xscale)
    ax.set_axisbelow(True)
    ax.axes.set_xlabel(labels[0], weight=labelweight, size=9, color=tcol)
    ax.axes.set_ylabel(labels[1], weight=labelweight, size=9, color=tcol)
    if annualx:
        ax = ticks_x_annual(ax, tcol, dpy)
    if dayy:
        ax = ticks_y_day(ax, tcol, pph, hpd, sh)
    elif pery:
        ax = ticks_y_per(ax, ydata, pery, tcol)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(7)
        tick.label1.set_color(tcol)
    for t in ax.yaxis.get_ticklines() + ax.yaxis.get_ticklines(minor=True):
        t.set_visible(ticklines and not ygrid)
        t.set_color(tcol)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(7)
        tick.label1.set_color(tcol)
    for t in ax.xaxis.get_ticklines() + ax.xaxis.get_ticklines(minor=True):
        t.set_visible(ticklines and not xgrid)
        t.set_color(tcol)
    if bottom is None:
        bottom = 0
    if bottom > 0:
        ylim = [ymin, ymax]
        ylimb = [i+bottom for i in ylim]
        ax.set_ylim(bottom=ylim[0], top=ylimb[1])
        ax.get_yaxis().get_major_formatter().set_useOffset(bottom)
    if xlabels is not None and len(xlabels) > 0:
        inc = old_div((xmax-xmin),len(xlabels))
        if polar:
            ax.set_xticks(np.arange(xmin, xmax, inc))
            ax.set_xticklabels(xlabels)
            ax.set_xlim(left=xmin, right=xmax)
        else:
            locs = np.arange(xmin+old_div(inc,2), xmax+old_div(inc,2), inc)
            series_ticks(ax, locs, xlabels, xrotate=xrotate)
    if polar:
        if bottom > 0:
            ci = Circle((0, 0), zorder=2, radius=bottom, fill=True,
                        linewidth=0.3, edgecolor=tcol, facecolor=bg,
                        transform=ax.transData._b)
            ax.add_artist(ci)
        ci = Circle((0, 0), zorder=-200, radius=(bottom+ymax-ymin),
                    fill=False, linewidth=0, edgecolor='blue',
                    facecolor='blue', transform=ax.transData._b)
        ax.add_artist(ci)
        if not ygrid:
            ax.yaxis.set_ticklabels([])
        ax.axes.set_ylabel("")
    if yticks is not None:
        if yscale != 'log':
            ax.set_yticks(np.append(np.arange(bottom+ymin, ymax+bottom,
                          (ymax-ymin)/yticks),ymax+bottom))
        else:
            decs = np.ceil(np.log10(ymax) - np.log10(ymin))
            maj = np.power(10, np.log10(ymin) + np.arange(decs+1))
            minors = np.meshgrid(1 + np.arange(yticks-1)*10/yticks, maj[:-1])
            minors = (minors[0] * minors[1]).flatten()
            ax.set_yticks(maj)
            ax.set_yticks(minors, minor=True)
            ax.yaxis.grid(ygrid, which='minor')
    if xticks is not None:
        if xscale != 'log':
            if xticks == 0:
                ax.set_xticks([])
            else:
                ax.set_xticks(np.append(np.arange(xmin, xmax, (xmax-xmin)/xticks),xmax))
        else:
            decs = np.ceil(np.log10(xmax) - np.log10(xmin))
            maj = np.power(10, np.log10(xmin) + np.arange(decs+1))
            minors = np.meshgrid(1 + np.arange(xticks-1)*10/xticks, maj[:-1])
            minors = (minors[0] * minors[1]).flatten()
            ax.set_xticks(maj)
            ax.set_xticks(minors, minor=True)
            ax.xaxis.grid(xgrid, which='minor')
    return ax


def plot_legend(ax, handles, bbox_to_anchor=(1.05, 1), loc=2,
                fg='black', bg='white', title=None):
    """add legend to figure"""
    leg = ax.legend(handles=handles, frameon=False, title=title,
                     bbox_to_anchor=bbox_to_anchor, loc=loc, facecolor=bg)
    for text in leg.get_texts():
        text.set_color(fg)


def add_colorbar(fig, pc, axes=[0.3, 0.0, 0.4, 0.02],
                 ticks=None, ticklabels=None, orientation='horizontal'):
    """add colorbar scale to figure below plot"""
    cbaxes = fig.add_axes(axes, label='colorbar')
    if ticklabels is not None:
        if ticks is None:
            vmin, vmax = pc.get_clim()
            ticks = np.linspace(vmin, vmax, len(ticklabels))
        cb = fig.colorbar(pc, orientation=orientation,
                          cax=cbaxes, ticks=ticks)
        if ticklabels is not None:
            cb.ax.set_xticklabels(ticklabels)
    else:
        cb = fig.colorbar(pc, orientation=orientation, cax=cbaxes)
    cb.ax.tick_params(labelsize=8, width=.5)
    cb.outline.set_linewidth(.5)
    for t in cb.ax.get_xticklines():
        t.set_visible(False)


def plot_graph(fig, saveimage, width=5, height=5, bg='white', fg='black',
               handles=[], handles2=[], dpi=200, bbox_to_anchor=(1.05, 1),
               loc=2, legend=False, background=None,
               front=False, alpha=.5, areaonly=False, polar=False, **kwargs):
    """add legend and save image of plot"""
    fig.set_size_inches(width, height)
    if legend and not areaonly:
        try:
            if isinstance(fig.axes[1], matplotlib.axes.SubplotBase):
                plot_legend(fig.axes[1], handles=handles2,
                            bbox_to_anchor=(bbox_to_anchor[0], 0),
                            loc=3, bg=bg, fg=fg, title='right axis')
        except IndexError:
            pass
        plot_legend(fig.axes[0], handles=handles, bbox_to_anchor=bbox_to_anchor,
                    loc=loc, bg=bg, fg=fg)
    ax = fig.axes[0]
    if areaonly:
        ax.axes.set_xlabel("")
        ax.axes.set_ylabel("")
        ax.xaxis.set_ticklabels([])
        ax2 = fig.add_axes([0, 0, 1, 1])
        plargs = dict(bbox_inches=0, aspect='auto', pad_inches=0)
    else:
        ax2 = fig.add_subplot(1, 1, 1, label='background')
        plargs = dict(bbox_inches='tight')
    extent = ax2.get_xlim() + ax2.get_ylim()
    if background is not None:
        im = plt.imread(background)
        plt.imshow(im, extent=extent, alpha=alpha, aspect='auto')
    if front:
        ax.set_zorder(ax2.get_zorder()-1)
    else:
        ax.set_zorder(ax2.get_zorder()+1)
        ax.patch.set_visible(False)
    ax2.axis('off')
    plt.savefig(saveimage, dpi=dpi, facecolor=bg, **plargs)
    plt.close()


def get_colors(cmap, step=None, positions=None, funcs=[], **kwargs):
    """get colormap from cmap name, color list or CliptColors spec

    Parameters
    ----------
    cmap: str or list of color tuples
        cmap selector
    positions: list
        if cmap is a list positions are the mapping points
        else positions are the sample points used to remap
    step: int or None
        # of steps to map colors using step function
    funcs: list of custom color map functions to try before standard 
        matplotlib cmap name check and cmap_from_list
        func should accept a cmap argument, and step and position
        (call cmap_tune within to utilize) and return a 
        matplotlib.cm.ScalarMappable

    Returns
    -------
    colormap: matplotlib.colors.LinearSegmentedColormap
    """
    efuncs = funcs + [cmap_from_mpl, cmap_from_clipt, cmap_from_list]
    e = []
    try:
        alpha = int(cmap.rsplit('_', 1)[1])
    except (IndexError, ValueError, AttributeError):
        alpha = None
    else:
        cmap0 = cmap
        cmap = cmap.rsplit('_', 1)[0]
    for func in efuncs:
        try:
            colormap = func(cmap, step, positions)
            break
        except Exception as err:
            e.append(str(err))
            continue
    else:
        raise ValueError("\n\n".join(e))
    if alpha is not None:
        clist = colormap.cmap(np.arange(colormap.cmap.N))
        clist[:,-1] = alpha/100
        cmap = colors.LinearSegmentedColormap.from_list(cmap0, clist)
        colormap.cmap = cmap
    return colormap


def plot_cmaps(ru=False):
    """plot predefined colormaps showing impact of step and position

    Returns
    -------

    fig: matplotlib graph
        can be saved using plt.savefig(...) or plotutil.plot_graph(...)
    """
    if ru:
        cmaps = [('hues', ['blu', 'org', 'pur', 'red', 'blg',
                  'mag', 'brn', 'grn', 'yel', 'ggr']),
                 ('shades', ['dark', 'med', 'light', 'xlight'])
                 ]
    else:
        cmaps = [('Perceptually Uniform Sequential', [
                    'viridis', 'plasma', 'inferno', 'magma']),
                 ('Sequential', [
                    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
                 ('Sequential (2)', [
                    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
                    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
                    'hot', 'afmhot', 'gist_heat', 'copper']),
                 ('Diverging', [
                    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr',
                    'seismic']),
                 ('Qualitative', [
                    'Pastel1', 'Pastel2', 'Paired', 'Accent',
                    'Dark2', 'Set1', 'Set2', 'Set3',
                    'tab10', 'tab20', 'tab20b', 'tab20c']),
                 ('Miscellaneous', [
                    'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                    'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix',
                    'brg', 'hsv', 'gist_rainbow', 'rainbow', 'jet',
                    'nipy_spectral', 'gist_ncar'])]
    nrows = sum(len(cmap_list)
                for cmap_category, cmap_list in cmaps) + len(cmaps)
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    fig, axes = plt.subplots(nrows=nrows)
    fig.set_size_inches(3, 10)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    if ru:
        axes[0].set_title('clipt colors', fontsize=14)
    else:
        axes[0].set_title('matplotlib colors', fontsize=14)
    i = 0
    for cmap_category, cmap_list in cmaps:
        ax = axes[i]
        pos = list(ax.get_position().bounds)
        y_text = pos[1] + pos[3]/2.
        fig.text(.6, y_text, cmap_category, va='center',
                 ha='center', fontsize=6)
        i += 1
        if cmap_category == 'hues':
            step = 4
        elif cmap_category == 'shades':
            step = 10
        else:
            step = None
        for name in cmap_list:
            ax = axes[i]
            colorbar = get_colors(name, step=step)
            ax.imshow(gradient, aspect='auto', cmap=colorbar.cmap)
            pos = list(ax.get_position().bounds)
            x_text = pos[0] - 0.01
            y_text = pos[1] + pos[3]/2.
            fig.text(x_text, y_text, name, va='center', ha='right', fontsize=6)
            i += 1
    for ax in axes:
        ax.set_axis_off()
    return fig


def plot_criteria(ax, x, y, criteria, flipxy=False,
                  kwargs={'linewidth': 0, 'marker': "o", 'markersize': 4,
                          'mew': 0}):
    """add dot on line matching criteria to scatter plot"""
    filtx = []
    filty = []
    val = [float(criteria.split("=")[-1])]
    if criteria[0] == 'x':
        filtx = val
        filty = np.interp(val, x, y)
    elif criteria[0] == 'y':
        xs = [ix for _, ix in sorted(zip(y, x))]
        ys = sorted(y)
        filtx = np.interp(val, ys, xs)
        filty = val
    if flipxy:
        ax.plot(filty, filtx, **kwargs)
    else:
        ax.plot(filtx, filty, **kwargs)


def color_inc_i(fcol, i, n, step):
    if step is not None:
        try:
            fcol = int(step*fcol % step)/step
        except ZeroDivisionError:
            fcol = 0
        cinc = (fcol + (i+.5)/step) % 1
    else:
        try:
            inc = old_div((1.-fcol),(n-1))
            cinc = fcol + i*inc
        except ZeroDivisionError:
            cinc = fcol + i
    return cinc


class WedgeMark(object):

    def __init__(self, wedge, d):
        self.mrk = wedge
        self.scale = np.max(np.abs(np.concatenate((np.sin(d*np.pi/180), np.cos(d*np.pi/180)))))


def plot_scatter(fig, ax, xs, ys, labels, colormap, criteria=None, lw=2, ms=0,
                 mrk='o', step=None, fcol=0.0, mew=0.0, emap=None, estep=None,
                 flipxy=False, cs=None, cmin=None, cmax=None, y2=None,
                 msd=None, mmin=None, mmax=None, legend=True,
                 polar=False, areas=[], falpha=0.5, **kwargs):
    """adds scatterplots/lines to ax and returns ax and handles for legend"""
    nlab = len(labels)
    for i in range(len(ys)):
        if i >= nlab:
            labels.append("series{:02d}".format(i))
    if emap is None:
        emap = colormap
    if y2 is None:
        y2 = []
    else:
        ax2 = fig.axes[1]
    if cs is None:
        cvals = (None,) * len(xs)
    else:
        if cmax is None:
            cmax = max(flat(cs))
        if cmin is None:
            cmin = min(flat(cs))
        j = 0
        cvals = []
        for i in range(len(ys)):
            try:
                cvals.append(cs[i])
            except IndexError:
                cvals.append(None)
    for i, (x, y, l, cs) in enumerate(zip(xs, ys, labels, cvals)):
        if i in y2:
            axT = ax2
            ax2.set_zorder(ax.get_zorder()+1)
        else:
            axT = ax
            try:
                ax.set_zorder(ax2.get_zorder()+1)
            except UnboundLocalError:
                pass
        lwa = get_nth(lw, i)
        if msd is not None:
            if mmax is None:
                mmax = max(flat(msd))
            if mmin is None:
                mmin = min(flat(msd))
            msa = np.array([min(mmax,max(mi,mmin)) for mi in msd[i]])
        else:
            msa = get_nth(ms, i)
        mka = get_nth_loop(mrk, i)
        mewa = get_nth_loop(mew, i)
        cinc = color_inc_i(fcol, i, len(ys), step)
        c = colormap.to_rgba(cinc)
        ecinc = color_inc_i(fcol, i, len(ys), estep)
        mec = emap.to_rgba(ecinc)
        if hasattr(mka, "scale"):
            msa = msa * mka.scale
            mkt = mka.mrk
        else:
            mkt = mka
        if i < len(areas):
            if len(areas[i]) < 2:
                ya2 = axT.axes.get_ylim()[0]
            else:
                ya2 = areas[i][1]
            axT.fill_between(x, areas[i][0], ya2, alpha=falpha, color=c, zorder=-1,
                            linestyle='--', linewidth=lwa/2)
        if cs is not None:
            colormap.norm.vmax = cmax
            colormap.norm.vmin = cmin
            plotargs = {'linewidth': lwa, 's': msa**2, 'label': l,
                        'marker': mkt, 'cmap': colormap.cmap, 'linewidth': mewa,
                        'c': cs, 'edgecolors': mec,
                        'norm': colormap.norm}
            plotargs.update(kwargs)
            axT.scatter(x, y, **plotargs)
        elif msd is not None:
            plotargs = {'linewidth': lwa, 's': msa**2, 'label': l,
                        'marker': mkt, 'linewidth': mewa, 'c': [c],
                        'edgecolors': mec}
            plotargs.update(kwargs)
            axT.scatter(x, y, **plotargs)
        else:
            plotargs = {'linewidth': lwa, 'markersize': msa, 'label': l,
                        'marker': mkt, 'color': c, 'mfc': c, 'mec': mec,
                        'mew': mewa}
            plotargs.update(kwargs)
            if flipxy:
                axT.plot(y, x, **plotargs)
            else:
                axT.plot(x, y, **plotargs)
        if criteria:
            copts = {'linewidth': 0, 'mfc': c, 'mew': 0,
                     'markersize': lwa*2.5, 'marker': 'o'}
            plot_criteria(ax, x, y, criteria, flipxy, copts)
    if legend and cs is not None:
        if polar:
            add_colorbar(fig, colormap, axes=[1, 0.11, .02, 0.77],
                         orientation='vertical')
        else:
            add_colorbar(fig, colormap, axes=[.92, 0.11, .02, 0.77],
                         orientation='vertical')
    handles, _ = ax.get_legend_handles_labels()
    try:
        handles2, _ = ax2.get_legend_handles_labels()
    except UnboundLocalError:
        handles2 = []
    return ax, handles, handles2


def plot_heatmap(fig, ax, data, colormap, vmin=None, vmax=None,
                 dst=False, ticks=None, labels=None, legend=True, hpd=24,
                 dpy=365, sh=0, **kwargs):
    """adds heatmap and colorbar to ax returns ax"""
    xlim = ax.axes.get_xlim()
    xrng = abs(xlim[1]-xlim[0])
    ppd = int(old_div(len(data),xrng))
    if dst:
        data = shift_data(data, old_div(ppd,hpd), hpd=hpd, dpy=dpy, sh=sh)
    try:
        mtx = np.reshape(data, (int(xrng), ppd))
        tmtx = np.transpose(mtx)
    except Exception:
        raise ValueError('expected {} data points got {}'.format(
                         int(xrng)*ppd, len(data)))
    if vmax is None:
        vmax = max(data)
    if vmin is None:
        vmin = min(data)
    pc = ax.pcolor(tmtx, cmap=colormap.cmap, vmax=vmax, vmin=vmin, snap=True,
                   **kwargs)
    if legend:
        add_colorbar(fig, pc, ticks=ticks, ticklabels=labels)
    return ax


def plot_bar(ax, xs, ys, labels, colormap, stacked=False, rwidth=.8, step=None, estep=None,
             bwidth=.9, fcol=0.0, brng=[0, 1], bottom=0, polar=False, polar0=False,
             emap=None, ew=[0], **kwargs):
    """adds bar plots to ax and returns ax and handles for legend"""
    nlab = len(labels)
    if emap is None:
        emap = colormap
    for i in range(len(ys)):
        if i >= nlab:
            labels.append("series{:02d}".format(i))
    if stacked:
        nlab = 1
    else:
        nlab = len(labels)
    xl = ax.axes.get_xlim()
    xlim = [xl[0]+brng[0]*(xl[1]-xl[0]), xl[0]+brng[1]*(xl[1]-xl[0])]
    xrng = abs(xlim[1]-xlim[0])/float(len(xs[0]))
    lxs = len(xs[0])
    width = old_div(xrng,nlab)*rwidth
    try:
        xsc = old_div((lxs - 1.0),lxs)
    except ZeroDivisionError:
        xsc = 1
    xsc = xsc * (brng[1] - brng[0])
    if polar and polar0:
        off0 = brng[0] * abs(xl[1]-xl[0])
    else:
        off0 = old_div(xrng,2)-old_div(width*(nlab-1),2) + xlim[0]
    w2 = width*bwidth
    bot = 0
    n = len(ys)
    for i, (x, y, l) in enumerate(zip(xs, ys, labels)):
        cinc = color_inc_i(fcol, i, n, step)
        c = colormap.to_rgba(cinc)
        einc = color_inc_i(fcol, i, n, estep)
        e = emap.to_rgba(einc)
        ewa = get_nth_loop(ew, i)
        plotargs = {'label': l, 'color': c, 'linewidth': ewa, 'edgecolor': e}
        plotargs.update(kwargs)
        if stacked:
            if i > 0:
                bot = np.array(ys[i-1]) + bot
            ax.bar(np.array(x)*xsc+off0, y, w2, bottom=bot+bottom, **plotargs)
        else:
            offset = i*width
            ax.bar(np.array(x)*xsc+offset+off0, y, w2, bottom=bottom,
                   **plotargs)
    handles, labels = ax.get_legend_handles_labels()
    return ax, handles


def plot_box(ax, data, labels, colormap, ylim, rwidth=.8, step=None, mark='x', whis=1.5,
             mew=0.5, ms=3.0, lw=1.0, fcol=0.0, clw=1.0, clbg=True, fillalpha=1.0, notch=False,
             series=1, sgap=0.5, bg='white', inline=False, mean=False,
             fliers=True, xlabels=None, **kwargs):
    """adds box plots to ax and returns ax and handles for legend"""
    nlab = len(labels)
    for i in range(series):
        if i >= nlab:
            labels.append("series{:02d}".format(i))
    nlab = len(labels)
    chunksize = int(len(data)/series)
    handles = []
    if series == 1:
        sgap = 0
    for i in range(series):
        cinc = color_inc_i(fcol, i, nlab, step)
        c = colormap.to_rgba(cinc)
        if clbg:
            medianc = bg
        else:
            medianc = c
        facecolor = c[0:3] + (fillalpha,)
        plotargs = {
            'boxprops' : {'linewidth':lw,'facecolor':facecolor, 'color':c},
            'capprops' : {'color':c,'linewidth':lw,'solid_capstyle':'butt'},
            'whiskerprops' : {'color':c,'linewidth':lw,'solid_capstyle':'butt'},
            'medianprops' : {'linewidth':clw*(not mean),'color':medianc,'solid_capstyle':'butt'},
            'meanprops' : {'linewidth':clw,'color':medianc,
                           'solid_capstyle':'butt', 'ls':'-', 'marker':'o',
                           'ms':clw*2, 'mfc':medianc, 'mew':0},
            'flierprops' : {'marker':mark, 'markeredgecolor':c, 'markeredgewidth':mew, 'markersize':ms}
        }
        plotargs.update(kwargs)
        if inline:
            x = np.arange(2, len(data), series)
            sw = series
        else:
            x = np.arange(i, len(data), series) + np.linspace(0, sgap*(chunksize - 1), chunksize)
            sw = 1
        if fliers:
            whis = whis
        else:
            whis = (0, 100)
        boxplot = ax.boxplot(data[i*chunksize:i*chunksize+chunksize], notch=notch,
                             patch_artist=True, widths=rwidth*sw, bootstrap=1000, whis=whis,
                             positions=x , manage_ticks=False, showmeans=mean, meanline=not notch,
                             **plotargs)
        handles.append(Patch(color=c, label=labels[i]))
    if inline:
        ax.set_xlim(left=-.5, right=len(data)-.5)
        tickx = np.arange(chunksize) - .5
    else:
        ax.set_xlim(left=-.5 - sgap/2, right=len(data) + (chunksize - .5) * sgap - .5)
        tickx = np.linspace(series/2, len(data) + (chunksize - 1) * sgap - series/2, chunksize) - .5
    if xlabels is None or len(xlabels) == 0:
        xlabels = np.arange(chunksize).astype(str)
    series_ticks(ax, tickx, xlabels, xrotate='a')
    return ax, handles


def plot_violin(ax, data, labels, colormap, ylim, rwidth=.8, step=None, lw=1.0, kernelwidth=.5,
                clw=1.0, clbg=True, fcol=0.0, fillalpha=1.0, median=True, conf=None, confm=None,
                series=1, bg='white', inline=False, mean=False, weights=None, weightlimit=0.0,
                fliers=False, **kwargs):
    """adds violin plots to ax and returns ax and handles for legend"""
    nlab = len(labels)
    for i in range(series):
        if i >= nlab:
            labels.append("series{:02d}".format(i))
    nlab = len(labels)
    chunksize = int(len(data)/series)
    handles = []
    for i in range(series):
        cinc = color_inc_i(fcol, i, nlab, step)
        c = colormap.to_rgba(cinc)
        if clbg:
            medianc = bg
        else:
            medianc = c
        if inline:
            x = np.arange(1, len(data), series)
            sw = series
        else:
            bwidth = 1 - (1-rwidth)/2
            x = np.arange(i*bwidth + 1 - bwidth, len(data), series)
            sw = 1
        ds = np.array(data[i*chunksize:i*chunksize+chunksize])
        if weights is not None:
            ws = np.array(weights[i*chunksize:i*chunksize+chunksize])
        else:
            ws = (None,) * len(ds)
        vstats = []
        flies = []
        for d, w in zip(ds, ws):
            vs = hs.kernel(d, w=w, n=1000, bws=kernelwidth, t=weightlimit)
            if fliers:
                qr = np.quantile(d, (.25, .75))
                iqr = (qr[1] - qr[0]) * 1.5
                filt = np.logical_and(d >= qr[0] - iqr, d <= qr[1] + iqr)
                # df = np.maximum(np.minimum(d, qr[1] + iqr), qr[0] - iqr)
                df = d[filt]
                vs['min'] = np.min(df)
                vs['max'] = np.max(df)
                flies.append(d[np.logical_not(filt)])
                # print(np.stack((np.arange(len(d))[np.logical_not(filt)], flies[-1])).T)
            vstats.append(vs)
        vplot = ax.violin(vstats, showmeans=mean, showmedians=median,
                          widths=rwidth*sw, positions=x)
        if confm is not None:
            bstats = hs.conf_box(ds, ws, confm)
            plotargs = {
                'boxprops' : {'linewidth':clw, 'color':c, 'linestyle':'--', 'dash_joinstyle':'miter'},
                'medianprops' : {'linewidth': 0},
                'whiskerprops': {'linewidth': 0},
            }
            ax.bxp(bstats, widths=rwidth*sw/4, positions=x, showfliers=False, showcaps=False, **plotargs)
        if conf is not None:
            bstats = hs.quant_box(ds, ws, conf)
            if fliers:
                for j in range(len(bstats)):
                    bstats[j]['fliers'] = flies[j]
            plotargs = {
                'boxprops' : {'linewidth':lw, 'color':c},
                'medianprops' : {'linewidth':0,},
                'whiskerprops': {'linewidth':0,},
                'flierprops': {'marker': 'x', 'markeredgecolor': c,
                               'markeredgewidth': lw*0.5,
                               'markersize': lw*4
                               }
            }
            ax.bxp(bstats, widths=rwidth*sw/2, positions=x, showfliers=fliers, showcaps=False, **plotargs)
        for vp in vplot['bodies']:
            vp.set_facecolor(c)
            vp.set_alpha(fillalpha)
        for j in ['cmins', 'cmaxes', 'cbars', 'cmeans', 'cmedians']:
            try:
                vp = vplot[j]
            except KeyError:
                pass
            else:
                if j == 'cmedians':
                    vp.set_edgecolor(medianc)
                    vp.set_linewidth(clw)
                else:
                    vp.set_edgecolor(c)
                    vp.set_linewidth(lw)
                
                if j == 'cmeans':
                    vp.set_linestyle(':')
                    vp.set_linewidth(clw)
        handles.append(Patch(color=c, label=labels[i]))
    ax.set_xlim(left=-.5, right=len(data)-.5)
    return ax, handles


def plot_histo(ax, data, labels, colormap, ylim, stacked=False, rwidth=.8,
               step=None, fcol=0.0, bwidth=.9, bins='auto', brange=None,
               tails=False, ylog=False, density=False, weights=None, **kwargs):
    """adds histo plots to ax and returns ax and handles for legend"""
    nlab = len(labels)
    for i in range(len(data)):
        if i >= nlab:
            labels.append("series{:02d}".format(i))
    n = len(data)
    c = [colormap.to_rgba(color_inc_i(fcol, i, n, step)) for i in range(n)]
    if brange and tails:
        data = [np.clip(np.array(y), brange[0], brange[1]) for y in data]
    plotargs = {'linewidth': 0}
    plotargs.update(kwargs)
    histo = plt.hist(data, bins=bins, log=ylog, range=brange, label=labels, weights=weights,
                     color=c, rwidth=rwidth, stacked=stacked, density=density, **plotargs)
    handles, labels = ax.get_legend_handles_labels()
    if ylim[1] is None:
        ymax = max(flat(histo[0]))*1.1
    else:
        ymax = ylim[1]
    ymin = ylim[0]
    ax.set_ylim(bottom=ymin, top=ymax)
    ax.set_xlim(left=min(histo[1]), right=max(histo[1]))
    return ax, handles


def dayhour(mo, day, ho=0, hpd=24, dpy=365, sh=0):
    """returns hour of year (no DST)"""
    # return daycount[mo-1]*24+(day-1)*24+ho
    return hpd*daycount[mo-1]*dpy/365. + hpd*(day-1)*dpy/365. + ho*hpd/24.


def shift_data(data, pph=1, sa=(3, 10), fb=(11, 2), hpd=24, dpy=365, sh=0):
    """
    shift annual data for DST for correct hour axis on heatmap

    Parameters
    ----------
    data: list
        length 8760*pph
    pph: int
        data points per hour in data.
    sa: tuple of ints
        (month, day) for spring ahead
    fb: tuple of ints
        (month, day) for fall back

    Returns
    -------
    data2: list
        data with 2AM on "spring ahead" duplicated and 1AM on "fall back"
        deleted
    """
    spr = int(dayhour(*sa, ho=2, hpd=hpd, dpy=dpy, sh=sh))*pph
    fal = int(dayhour(*fb, ho=1, hpd=hpd, dpy=dpy, sh=sh))*pph
    if hpd != 24:
        spr = spr - spr % hpd + hpd
        fal = fal - fal % hpd + hpd
    data2 = data[:spr] + data[spr:spr+pph] + data[spr:fal] + data[fal+pph:]
    return data2


def get_tick_distribution(data, divisions):
    """
    returns values demarcating equal size bins on data

    Parameters
    ----------
    data: list
        list of float values
    divisions: int
        number of divisions to make (cannot exceed len(data))

    Returns
    -------
    ticks: list
        values from data at each division point
    """
    binsize = 100./divisions
    bins = np.arange(binsize, 100.+binsize, binsize)
    df = flat(data)
    dmin = min(df)
    dmax = max(df) 
    ticks = np.percentile([i for i in df if i > 0], bins)
    ticks = [int(round(i)) for i in ticks]
    return ticks


def flat(l):
    """flattens any depth iterable (except strings)"""
    a = []
    try:
        if type(l) != str:
            for i in l:
                a += flat(i)
        else:
            a.append(l)
    except Exception:
        a.append(l)
    return a


def pad_scale(data, n=8760, mult=1, missing=0.0):
    """scale and pad data returns numpy.array"""
    data = np.array(data)*mult
    if len(data) < n:
        missing = np.ones(n-len(data))*missing
        data = np.concatenate((data, missing))
    elif len(data) > n:
        data = data[:n]
    return data


def ticks_x_annual(ax, fg='black', dpy=365):
    """set xaxis to days in year with month labels"""
    ax.xaxis.set_ticks([i*dpy/365.0 for i in daycount[1:]])
    monthlabel = [(i+15)*dpy/365.0 for i in daycount]
    ax.set_xticks(monthlabel, minor=True)
    ax.set_xticklabels(
        labels=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        size=8, minor=True, color=fg)
    ax.set_xticklabels(labels=[])
    for t in ax.xaxis.get_ticklines(minor=True):
        t.set_visible(False)
    for t in ax.xaxis.get_ticklines():
        t.set_visible(False)
    ax.xaxis.set_tick_params(length=2.5)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlim([0, dpy])
    ax.axes.set_xlabel("Month", weight="bold", size=9, color=fg)
    return ax


def ticks_y_day(ax, tcol='black', pph=1, hpd=24, sh=0):
    """set yaxis to hours in day"""
    hlabels = ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM',
               '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM',
               '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM',
               '10PM', '11PM']
    ax.set_yticks(np.arange(0, hpd*pph, pph)+pph*0.5, minor=True)
    ax.set_yticks(np.arange(1, hpd*pph, pph), minor=False)
    ax.set_yticklabels(hlabels[sh:sh+hpd], size=8, minor=True, color=tcol)
    ax.set_yticklabels(labels=[])
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim([hpd*pph, 0])
    ax.axes.set_ylabel("Hour", weight="bold", size=9, color=tcol)
    return ax


def ticks_y_per(ax, ydata, tickdiv, tcol="black"):
    """label y axis according to percentile of data with pery bins"""
    tickinc = 100./tickdiv
    ticks = get_tick_distribution(ydata, tickdiv)
    ax.yaxis.set_ticks(ticks)
    yticklabels = []
    for i in range(len(ticks)):
        yticklabels.append("{0} ({1:.0f}%)".format(ticks[i], (i+1)*tickinc))
    ax.set_yticklabels(labels=yticklabels, size=7, color=tcol)
    return ax


class CliptColors(object):
    """class containing custom clipt colors"""

    def __getitem__(self, key):
        return self.cdict[key]

    def __init__(self):
        self.cdict255 = {
            'blu': [(23, 55, 93), (31, 73, 125),
                    (83, 142, 213), (141, 180, 227)],
            'org': [(151, 72, 7), (228, 109, 10),
                    (255, 153, 0), (250, 192, 144)],
            'pur': [(120, 0, 204), (180, 102, 255),
                    (204, 153, 255), (204, 192, 218)],
            'red': [(171, 21, 21), (204, 51, 0),
                    (255, 0, 0), (217, 151, 149)],
            'blg': [(33, 88, 103), (49, 132, 155),
                    (147, 205, 221), (181, 221, 232)],
            'mag': [(153, 0, 153), (204, 51, 153),
                    (255, 51, 153), (255, 153, 204)],
            'brn': [(74, 69, 42), (148, 139, 84),
                    (197, 190, 151), (221, 217, 195)],
            'grn': [(36, 140, 83), (0, 176, 80),
                    (146, 208, 80), (149, 253, 35)],
            'yel': [(188, 184, 0), (216, 220, 40),
                    (255, 255, 0), (255, 255, 153)],
            'ggr': [(79, 98, 40), (117, 146, 60),
                    (194, 214, 154), (215, 228, 188)],
            'pm3d': [(0,0,0), (0,0,0), (0,0,0), (0,0,0),
                     (66.0867532,7.96888909,104.060351),
                     (92.488467,14.9637761,187.732777),
                     (109.047472,14.9637761,233.803835),
                     (121.939217,14.9637761,252.950118),
                     (132.358234,14.9637761,253.40607),
                     (140.057572,14.9637761,241.683544),
                     (147.257293,14.9637761,221.341144),
                     (153.248603,14.9637761,196.634698),
                     (158.356722,10.920175,168.020405),
                     (163.076322,17.99353,138.40435),
                     (167.272654,17.99353,108.725664),
                     (170.97227,22.695682,78.6556833),
                     (174.59649,26.4459575,50.4598788),
                     (177.75777,29.6460755,22.695682),
                     (180.870487,32.4744741,10.920175),
                     (183.593905,35.045542,10.920175),
                     (186.421679,40.6276297,14.9637761),
                     (188.384223,40.6276297,14.9637761),
                     (190.963397,44.5014275,14.9637761),
                     (192.870679,48.0160978,14.9637761),
                     (195.379053,51.2462187,14.9637761),
                     (197.251041,54.2413161,14.9637761),
                     (199.086349,57.056982,14.9637761),
                     (200.901576,59.7150308,14.9637761),
                     (202.697332,64.6381163,14.9637761),
                     (203.883973,66.9356291,14.9637761),
                     (205.648552,71.2780323,14.9637761),
                     (207.409999,73.3293562,14.9637761),
                     (208.564557,77.2475565,14.9637761),
                     (209.711497,79.1152419,14.9637761),
                     (211.417928,82.7045137,14.9637761),
                     (212.546426,86.1202011,14.9637761),
                     (213.66778,89.3764982,14.9637761),
                     (214.782116,90.9464589,14.9637761),
                     (216.45484,94.0002246,14.9637761),
                     (217.552076,98.3695502,14.9637761),
                     (218.642712,101.192683,14.9637761),
                     (219.726858,103.890284,14.9637761),
                     (220.266531,106.506341,14.9637761),
                     (221.341144,109.047472,14.9637761),
                     (222.409533,112.731129,14.9637761),
                     (223.471799,115.108729,14.9637761),
                     (224.541542,118.568474,14.9637761),
                     (225.067395,120.837634,14.9637761),
                     (226.114702,124.107292,14.9637761),
                     (227.15622,127.276711,14.9637761),
                     (227.674836,130.354137,14.9637761),
                     (228.707839,132.358234,14.9637761),
                     (229.735272,135.297865,14.9637761),
                     (230.246927,138.186961,14.9637761),
                     (231.266164,140.981729,14.9637761),
                     (231.773767,143.711545,14.9637761),
                     (232.293004,146.380511,14.9637761),
                     (233.301529,148.992321,14.9637761),
                     (233.803835,152.413044,14.9637761),
                     (234.804582,154.903525,14.9637761),
                     (235.303041,157.34686,14.9637761),
                     (235.800236,159.745492,14.9637761),
                     (236.790871,162.877981,14.9637761),
                     (237.284328,165.200236,14.9637761),
                     (237.776557,167.464767,14.9637761),
                     (238.267566,170.428165,14.9637761),
                     (239.24596,172.610768,14.9637761),
                     (239.73336,175.48854,14.9637761),
                     (240.232026,178.292961,14.9637761),
                     (240.717033,180.362028,14.9637761),
                     (241.200869,183.077261,14.9637761),
                     (241.683544,185.74501,14.9637761),
                     (242.645439,188.384223,14.9637761),
                     (243.124675,190.963397,14.9637761),
                     (243.60278,193.501432,14.9637761),
                     (244.079761,196.000135,14.9637761),
                     (244.555627,198.476842,14.9637761),
                     (245.030384,200.901576,14.9637761),
                     (245.50404,203.291691,14.9637761),
                     (245.976602,205.648552,14.9637761),
                     (246.448077,207.988239,14.9637761),
                     (246.918472,210.282154,14.9637761),
                     (247.387794,213.107988,14.9637761),
                     (247.868042,215.350888,14.9637761),
                     (248.335212,217.552076,14.9637761),
                     (248.80133,220.266531,14.9637761),
                     (249.266402,222.409533,14.9637761),
                     (249.730435,224.541542,14.9637761),
                     (250.193436,227.15622,14.9637761),
                     (250.655411,229.222246,14.9637761),
                     (251.116366,231.773767,14.9637761),
                     (251.576308,234.30485,14.9637761),
                     (251.576308,236.296176,14.9637761),
                     (252.035243,238.757364,14.9637761),
                     (252.493178,241.200869,14.9637761),
                     (252.950118,243.124675,14.9637761),
                     (253.40607,245.50404,14.9637761),
                     (253.86104,247.868042,14.9637761),
                     (254.315033,250.193436,14.9637761),
                     (254.315033,252.035243,14.9637761),
                     (254.768055,254.315033,14.9637761)]
        }
        self.cdict = {}
        for k, v in self.cdict255.items():
            self.cdict[k] = [tuple(i/255. for i in j) for j in v]
        self.colors = ['blu', 'org', 'pur', 'red', 'blg',
                       'mag', 'brn', 'grn', 'yel', 'ggr']
        self.clist = [self.cdict[i] for i in self.colors]
        self.clist255 = [self.cdict255[i] for i in self.colors]
        self.shades = ['dark', 'med', 'light', 'xlight']
        for i, v in enumerate(self.shades):
            self.cdict[v] = [j[i] for j in self.clist]
            self.cdict255[v] = [j[i] for j in self.clist255]


def cmap_from_list(cmap, step=None, positions=None, name='custom'):
    """return colormap from list of colors"""
    try:
        if max(flat(cmap)) > 1:
            cmap = [tuple(i/255. for i in j) for j in cmap]
        if positions is not None and len(cmap) > 1:
            cmap = [(i, j) for i, j in zip(positions, cmap)]
            name += "_pos"
        if len(cmap) == 1:
            cmap.append(cmap[0])
        colorm = colors.LinearSegmentedColormap.from_list(name, cmap)
    except Exception:
        raise ValueError('cmap_from_list expected list of color tuples')
    norm = colors.Normalize(vmin=0, vmax=1)
    colormap = cmx.ScalarMappable(cmap=colorm, norm=norm)
    if step is not None:
        cmap2 = []
        cmap2.append((0, colormap.to_rgba(0)))
        pinc = 1/float(step-1)
        inc = 1/float(step)
        for i in range(step):
            t = i*inc
            t1 = min((i+1)*inc, 1)
            cmap2.append((t, colormap.to_rgba(i*pinc)))
            cmap2.append((t1, colormap.to_rgba(i*pinc)))
        name += "_step"
        colorm = colors.LinearSegmentedColormap.from_list(name, cmap2)
        colormap = cmx.ScalarMappable(cmap=colorm, norm=norm)
    return colormap


def cmap_tune(colormap, step=None, positions=None, name='custom'):
    if positions is not None:
        cmap2 = []
        pos2 = []
        segments = len(positions) - 1
        iperseg = int(2000/segments)
        for i,p in enumerate(positions[0:-1]):
            inc = (positions[i+1] - p)/iperseg
            incs = np.arange(p,positions[i+1] + inc, inc)
            cmap2 += list(colormap.to_rgba(incs))
        colormap = cmap_from_list(cmap2, step, None, name)
    elif step is not None:
        cmap2 = []
        for i in range(step):
            inc = i/float(step-1)
            cmap2.append(colormap.to_rgba(inc))
        colormap = cmap_from_list(cmap2, step, None, name)
    return colormap


def cmap_from_mpl(cmap, step=None, positions=None):
    """return colormap from matplotlib colormaps"""
    norm = colors.Normalize(vmin=0, vmax=1)
    colormap = cmx.ScalarMappable(cmap=cmap, norm=norm)
    colormap = cmap_tune(colormap, step, positions, cmap)
    return colormap


def cmap_from_clipt(cmap, step=None, positions=None):
    """return colormap from CliptColors key"""
    clcol = CliptColors()
    try:
        clist = clcol[cmap]
    except Exception:
        clopts = ", ".join(list(clcol.cdict.keys()))
        note = "Additional clipt colors values:"
        message = "{}\n\n{}".format(note, clopts)
        raise ValueError(message)
    else:
        colorm = colors.LinearSegmentedColormap.from_list(cmap, clist)
        norm = colors.Normalize(vmin=0, vmax=1)
        colormap = cmx.ScalarMappable(cmap=colorm, norm=norm)
        colormap = cmap_tune(colormap, step, positions, cmap)
    return colormap


def get_nth(li, i):
    """if i < len(l) returns l[i] else l[-1]"""
    try:
        return li[min(i, len(li)-1)]
    except Exception:
        return li


def get_nth_loop(li, i):
    """returns l[i % len(l)]"""
    try:
        return li[i % len(li)]
    except Exception:
        return li


def quick_scatter(xs, ys, ax=None, fig=None, outf=None, colors='viridis', tkwargs=None, ckwargs=None,
                  polar=False, labels=None, legend=False, width=5, height=5, areaonly=False, **kwargs):
    if tkwargs is None:
        tkwargs = {}
    if ckwargs is None:
        ckwargs = {}
    if labels is None:
        labels = []
    if ax is None or fig is None:
        ax, fig = plot_setup(polar=polar, areaonly=areaonly)
    cmap = get_colors(colors, **ckwargs)
    ax, handles, handles2 = plot_scatter(fig, ax, xs, ys, labels, cmap, polar=polar, legend=legend, **kwargs)
    if 'xdata' not in tkwargs:
        tkwargs['xdata'] = flat(xs)
    if 'ydata' not in tkwargs:
        tkwargs['ydata'] = flat(ys)
    tkwargs['polar'] = polar
    ticks(ax, **tkwargs)
    if outf is None:
        return ax, fig
    else:
        plot_graph(fig, outf, width=width, height=height, legend=legend, handles=handles, handles2=handles2, polar=polar, areaonly=areaonly)

