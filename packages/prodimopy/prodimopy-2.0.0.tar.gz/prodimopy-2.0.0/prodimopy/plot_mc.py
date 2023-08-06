"""
.. module:: plot_mc
   :synopsis: Plotting routines for molecular cloud |prodimo| models (0D chemistry).

.. moduleauthor:: Ch. Rab
"""

from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import prodimopy.plot as pplt


# That crashes in the bash on Mac OS X.. maybe because of installation
class PlotMcModel(object):
  """
  Plot routines for a single molecular cloud |prodimo| model (0D chemistry).

  TODO: Redesign this. it is not very usefull to have this dokwargs legend ...
  etc. routines copied all the time

  """

  def __init__(self,pdf,
               colors=None,
               styles=None,
               markers=None,
               fs_legend=6,  # TODO: init it with the system default legend fontsize
               ncol_legend=0):
    """
    Parameters
    ----------
    name : pdf
      a :class:`matplotlib.backends.backend_pdf.PdfPages` object used to save the plot.

    colors : list
      a list of matplotlib colors used for different models. (default: None)

    styles : list
      a list of matplotlib styles used for different models. (default: None)

    markers : list
      a list of matplotlib markers used for different models. (default: None)

    Attributes
    ----------
    """
    self.pdf=pdf
    if colors==None:
      self.colors=["b","g","r","c","m","y","k","sienna","lime","pink","DarkOrange","Olive"]
    else:
      self.colors=colors

    if styles==None:
      self.styles=["-"]*len(self.colors)
    else:
      self.styles=styles

    if markers==None:
      self.markers=[None]*len(self.colors)
    else:
      self.markers=markers

    self.fs_legend=fs_legend
    self.ncol_legend=ncol_legend

  def _dokwargs(self,ax,**kwargs):
    """
    Handles the passed kwargs elements (assumes that defaults are already set)
    """
    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])

    if "xlim" in kwargs:
      ax.set_xlim(kwargs["xlim"])

    if "xlog" in kwargs:
      if kwargs["xlog"]: ax.semilogx()

    if "ylog" in kwargs:
      if kwargs["ylog"]: ax.semilogy()

  def _legend(self,ax):
    '''
    plots the legend, deals with multiple columns
    '''
    handles,labels=ax.get_legend_handles_labels()
    ncol=1
    if self.ncol_legend>1 and len(labels)>self.ncol_legend:
      ncol=int(len(labels)/self.ncol_legend)
    ax.legend(handles,labels,loc="best",fancybox=False,framealpha=0.75,ncol=ncol,fontsize=self.fs_legend)

  def _closefig(self,fig):
    '''
    Save and close the plot (Figure).

    If self.pdf is None than nothing is done and the figure is returned

    #set the transparent attribut (used rcParam savefig.transparent)
    '''

    # trans=mpl.rcParams['savefig.transparent']
    if self.pdf is not None:
      self.pdf.savefig(figure=fig,transparent=False)
      plt.close(fig)
      return None
    else:
      return fig

  def plot_species(self,model,spnames,**kwargs):
    '''
    Plot the species abundances as function of age (time).

    Parameters
    ----------
    model : :class:`prodimopy.read_mc.Data_mc`
      a :class:`prodimopy.read_mc.Data_mc` object used to save the plot.

    spnames : list or str
      The names of the species that should be plotted. Can also be a single
      string.

    .. todo::

      the x axis (ages) is always plotted in log-scale so the zero age (
      initial abundance) is not shown. Needs more flexibility.
    '''
    if type(spnames)==str: spnames=[spnames]

    fig,ax=plt.subplots(1,1)

    i=0
    xmax=1.e-99
    xmin=1.e99
    for spname in spnames:
      if (spname in model.species):
        ax.plot(model.ages,model.abundances[:,model.species.index(spname)],
              self.styles[i],
              marker=self.markers[i],
              color=self.colors[i],label=spname)
        xmax=max([max(model.ages),xmax])
        # exclude zero because of log plot
        # nozeros=
        xmin=min([min(model.ages[model.ages>0.0]),xmin])

        i=i+1
      else:
        print("Species "+spname+" not found.")

    # no data to plot just return
    if i==0:
      return

    ax.set_xlim(xmin,xmax)
    ax.semilogx()
    ax.semilogy()
    self._dokwargs(ax,**kwargs)

    ax.set_xlabel(r"years")

    ax.set_ylabel(r" species abundance")

    self._legend(ax)

    # if "title" in kwargs and kwargs["title"] != None:
    #  ax.set_title(kwargs["title"])

    return self._closefig(fig)


class PlotMcModels(object):
  """
  Plot routines for a molecular cloud |prodimo| models (0D chemistry).
  """

  def __init__(self,pdf,
               colors=None,
               styles=None,
               markers=None,
               fs_legend=6,  # TODO: init it with the system default legend fontsize
               ncol_legend=0):
    """
    Parameters
    ----------
    name : pdf
      a :class:`matplotlib.backends.backend_pdf.PdfPages` object used to save the plot.

    colors : list
      a list of matplotlib colors used for different models. (default: None)

    styles : list
      a list of matplotlib styles used for different models. (default: None)

    markers : list
      a list of matplotlib markers used for different models. (default: None)

    Attributes
    ----------
    """
    self.pdf=pdf
    if colors==None:
      self.colors=["b","g","r","c","m","y","k","sienna","lime","pink","DarkOrange","Olive"]
    else:
      self.colors=colors

    if styles==None:
      self.styles=["-"]*len(self.colors)
    else:
      self.styles=styles

    if markers==None:
      self.markers=[None]*len(self.colors)
    else:
      self.markers=markers

    self.fs_legend=fs_legend
    self.ncol_legend=ncol_legend

  def _dokwargs(self,ax,**kwargs):
    """
    Handles the passed kwargs elements (assumes that defaults are already set)
    """
    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])

    if "xlim" in kwargs:
      print(kwargs["xlim"])
      ax.set_xlim(kwargs["xlim"])

    if "xlog" in kwargs:
      if kwargs["xlog"]: ax.semilogx()

    if "ylog" in kwargs:
      if kwargs["ylog"]: ax.semilogy()

  def _legend(self,ax):
    '''
    plots the legend, deals with multiple columns
    '''
    handles,labels=ax.get_legend_handles_labels()
    ncol=1
    if self.ncol_legend>1 and len(labels)>self.ncol_legend:
      ncol=int(len(labels)/self.ncol_legend)
    ax.legend(handles,labels,loc="best",fancybox=False,framealpha=0.75,ncol=ncol,fontsize=self.fs_legend)

  def _closefig(self,fig):
    '''
    Save and close the plot (Figure).

    If self.pdf is None than nothing is done and the figure is returned

    #set the transparent attribut (used rcParam savefig.transparent)
    '''

    # trans=mpl.rcParams['savefig.transparent']
    if self.pdf is not None:
      self.pdf.savefig(figure=fig,transparent=False)
      plt.close(fig)
      return None
    else:
      return fig

  def plot_species(self,models,spname,ice=False,ax=None,**kwargs):
    """
    Plot the given species (spname) for all the given models.

    Parameters
    ----------

    models : array_like(:class:`prodimopy.read_mc.Data_mc`,ndim=1)
      list of molecular cloud models

    spname : str
      The name fo the species to plot


    """
    if ax is not None:
      fig=ax.get_figure()
    else:
      fig,ax=plt.subplots(1,1)

    i=0
    xmax=1.e-99
    xmin=1.e99
    ymax=1.e-99
    ymin=1.e99
    for model in models:
      if (spname in model.species):
        abun=model.abundances[:,model.species.index(spname)]
        line,=ax.plot(model.ages,abun,
              self.styles[i],
              marker=self.markers[i],
              color=self.colors[i],label=model.name)

        ymax=max([max(abun),ymax])
        ymin=min([min(abun[model.ages>0.0]),ymin])

        if ice and (spname+"#" in model.species):
          abun=model.abundances[:,model.species.index(spname+"#")]
          line,=ax.plot(model.ages,abun,
              "--",
              marker=self.markers[i],
              color=line.get_color())

          ymax=max([max(abun),ymax])
          ymin=min([min(abun[model.ages>0.0]),ymin])

        xmax=max([max(model.ages),xmax])
        # exclude zero because of log plot
        # nozeros=
        xmin=min([min(model.ages[model.ages>0.0]),xmin])

        i=i+1

    # no data to plot just return
    if i==0:
      print("Species "+spname+" not found.")
      return

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin*0.9,ymax*1.1)

    ax.semilogx()
    ax.semilogy()
    self._dokwargs(ax,**kwargs)

    ax.set_xlabel(r"years")

    ylabel=r" $\mathrm{\epsilon("+pplt.spnToLatex(spname)+")}$"
    if ice and (spname+"#" in model.species):
      ylabel+=r", $\mathrm{\epsilon("+pplt.spnToLatex(spname+"#")+") dashed}$"

    ax.set_ylabel(ylabel)

    self._legend(ax)

    # if "title" in kwargs and kwargs["title"] != None:
    #  ax.set_title(kwargs["title"])

    return self._closefig(fig)

  def plot_species_diff(self,models,spname,ax=None,**kwargs):
    """
    Plot the difference of the species abundance relative to the last model.
    The relative diffferencie is definded as abs(modelval/modelrefval-1.0)

    Parameters
    ----------

    models : array_like(:class:`prodimopy.read_mc.Data_mc`,ndim=1)
      list of molecular cloud models

    spname : str
      The name fo the species to plot


    """
    if ax is not None:
      fig=ax.get_figure()
    else:
      fig,ax=plt.subplots(1,1)

    i=0
    xmax=1.e-99
    xmin=1.e99
    ymax=1.e-99
    ymin=1.e99

    for model in models[:-1]:
      if (spname in model.species):
        # FIXME: add small number to avoid problems with zero
        diff=np.absolute((model.abundances[1:,model.species.index(spname)]+1.e-200)/
                         (models[-1].abundances[1:,models[-1].species.index(spname)]+1.e-200)-1.0)
        # print(diff)
        ax.plot(model.ages[1:],diff,
              self.styles[i],
              marker=self.markers[i],
              color=self.colors[i],label=model.name)
        xmax=max([max(model.ages),xmax])
        xmin=min([min(model.ages[1:]),xmin])

        ymax=max([max(diff),ymax])
        ymin=min([min(diff),ymin])

        i=i+1

    # no data to plot just return
    if i==0:
      print("Species "+spname+" not found.")
      return

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin*0.9,ymax*1.1)

    ax.semilogx()
    ax.semilogy()
    self._dokwargs(ax,**kwargs)

    ax.set_xlabel(r"years")
    ax.set_ylabel(r" rel. diff $\mathrm{\epsilon("+pplt.spnToLatex(spname)+")}$")

    self._legend(ax)

    # if "title" in kwargs and kwargs["title"] != None:
    #  ax.set_title(kwargs["title"])

    return self._closefig(fig)

  def plot_abunratio(self,models,spname1,spname2,**kwargs):
    fig,ax=plt.subplots(1,1)

    i=0
    xmax=1.e-99
    xmin=1.e99
    for model in models:
      if (spname1 in model.species and spname2 in model.species):
        ratio=model.abundances[:,model.species.index(spname1)]/model.abundances[:,model.species.index(spname2)]
        ax.plot(model.ages,ratio,
              self.styles[i],
              marker=self.markers[i],
              color=self.colors[i],label=model.name)
        xmax=max([max(model.ages),xmax])
        # exclude zero because of log plot
        # nozeros=
        xmin=min([min(model.ages[model.ages>0.0]),xmin])

        i=i+1

    if i==0:
      print("Species "+spname1+"and/or "+spname2+" not found.")
      return

    ax.set_xlim(xmin,xmax)
    ax.semilogx()
    ax.semilogy()
    self._dokwargs(ax,**kwargs)

    ax.set_xlabel(r"years")

    ax.set_ylabel(r" $\mathrm{\epsilon("+pplt.spnToLatex(spname1)+")/"
                  +"\epsilon("+pplt.spnToLatex(spname2)+")}$")

    self._legend(ax)

    # if "title" in kwargs and kwargs["title"] != None:
    #  ax.set_title(kwargs["title"])

    return self._closefig(fig)

