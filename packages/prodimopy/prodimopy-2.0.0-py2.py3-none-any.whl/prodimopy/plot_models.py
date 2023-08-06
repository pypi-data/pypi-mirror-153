from __future__ import division
from __future__ import print_function

from math import pi

from matplotlib import lines
from matplotlib import patches

import astropy.constants as const
import astropy.units as u
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import prodimopy.extinction
import prodimopy.plot


# has to be this way because of circular imports
class PlotModels(object):

  def __init__(self,pdf,
               colors=None,
               styles=None,
               markers=None,
               fs_legend=None,  # TODO: init it with the system default legend font size
               ncol_legend=0):

    self.pdf=pdf
    if colors==None:
      # use system default colors not fixed ones.
      # FIXME: could be done more elegant (simply set colors to None, needs changes in the plot routines)
      self.colors=[None]*20
      # self.colors = ["b", "g", "r", "c", "m", "y", "k", "sienna", "lime", "pink", "DarkOrange", "Olive","brown"]
    else:
      self.colors=colors

    if styles==None:
      self.styles=["-"]*len(self.colors)
    else:
      self.styles=styles

    if markers==None:
      self.markers=["D"]*len(self.colors)
    else:
      self.markers=markers

    if fs_legend is None:
      self.fs_legend=mpl.rcParams['legend.fontsize']
    else:
      self.fs_legend=fs_legend
    self.ncol_legend=ncol_legend

  def _sfigs(self,**kwargs):
    '''
    Scale the figure size from matplotlibrc by the factors given in the
    array sfigs (in kwargs) the first element is for the width the second for
    the hieght
    '''
    figsize=mpl.rcParams['figure.figsize']

    if "sfigs" in kwargs:
      fac=kwargs["sfigs"]
      return (figsize[0]*fac[0],figsize[1]*fac[1])
    elif "wfac" in kwargs and "hfac" in kwargs:
      wfac=kwargs["wfac"]
      hfac=kwargs["hfac"]
      return (figsize[0]*wfac,figsize[1]*hfac)
    else:
      return (figsize[0],figsize[1])

  def _legend(self,ax,**kwargs):
    '''
    plots the legend, deals with multiple columns
    '''
    if "slegend" in kwargs:
      if not kwargs["slegend"]: return

    if "fs_legend" in kwargs:
      fs=kwargs["fs_legend"]
    else:
      fs=self.fs_legend  # TODO: maybe remove fs_legend from init and just use rcparams

    if "loc_legend" in kwargs:
      loc=kwargs["loc_legend"]
    else:
      loc="best"

    handles,labels=ax.get_legend_handles_labels()
    ncol=1
    if self.ncol_legend>1 and len(labels)>self.ncol_legend:
      ncol=int(len(labels)/self.ncol_legend)
    leg=ax.legend(handles,labels,loc=loc,fancybox=False,ncol=ncol,fontsize=fs)
    lw=mpl.rcParams['axes.linewidth']
    leg.get_frame().set_linewidth(lw)

  def _set_dashes(self,line):
    '''
    Utility routine to set the dashed stuff for a line.
    This routine should be used instead of using set_dashes directly, if the
    default value (still hardcoded) should be used.
    TODO: in matplotlib 2.0 is an option for this ... so this function can be removed
          in the future
    '''
    majver=int((mpl.__version__).split(".")[0])
    if majver<2:
      line.set_dashes((4,4))

  def _dokwargs(self,ax,**kwargs):
    '''
    Handles the passed kwargs elements (assumes that defaults are already set)
    '''
    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])

    if "xlim" in kwargs:
      ax.set_xlim(kwargs["xlim"])

    if "xlog" in kwargs:
      if kwargs["xlog"]:
        ax.semilogx()
      else:
        ax.set_xscale("linear")

    if "ylog" in kwargs:
      if kwargs["ylog"]:
        ax.semilogy()
      else:
        ax.set_yscale("linear")

    if "xlabel" in kwargs:
      ax.set_xlabel(kwargs["xlabel"])

    if "ylabel" in kwargs:
      ax.set_ylabel(kwargs["ylabel"])

    if "title" in kwargs:
      if  kwargs["title"]!=None and kwargs["title"].strip()!="":
        ax.set_title(kwargs["title"])

  def _initfig(self,ax=None,**kwargs):
    '''
    Inits Figure and Axes object.

    If an Axes object is passed, it is returned together with the Figure object.

    This is for a single plot (i.e. only one panel)

    Returns
    -------
    :class:`~matplotlib.figure.Figure`
    :class:`~matplotlib.axes.Axes`
    '''

    if ax is not None:
      fig=ax.get_figure()

    else:
      fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    return fig,ax

  def _closefig(self,fig):
    '''
    Save and close the plot (Figure).

    If self.pdf is None than nothing is done and the figure is returend

    Parameters
    ==========

    fig : :class:`~matplotlib.figure.Figure`
      A matplotliblib Figure object that will be saved in `self.pdf` if it exists
      or just returned again.

    '''

    # trans=mpl.rcParams['savefig.transparent']
    if self.pdf is not None:
      self.pdf.savefig(figure=fig,transparent=False)
      plt.close(fig)
      return None
    else:
      return fig

  def plot_lines(self,models,lineIdents,useLineEstimate=True,jansky=False,
                 showBoxes=True,lineObs=None,lineObsLabel="Obs.",peakFlux=False,
                 showCont=False,xLabelGHz=False,showGrid=True,**kwargs):
    """
    Plots the fluxes for a given selection of lines or lineEstimates.

    Parameters
    ----------
    models : array_like
      The list of models of type :class:`prodimopy.read.Data_ProDiMo`

    lineIdents : array_like
      a list of line identifiers. Each entry should contain `["ident",wl]`
      (e.g. `["CO",1300],["CO",800]]`. Those values are passed to
      :func:`~prodimopy.Data_ProDiMo.getLineEstimate`. The order of the lineIdents also
      defines the plotting order of the lines (from left to right)

    useLineEstimate : boolean
      if `True` the lines are selected from the lineEstimates otherwise
      the lines are taken from the full line radiative transfer.
      Default: `True`

    jansky : boolean
      plot the fluxes in units of Jansky
      Default: `True`

    showBoxes : boolean
      show boxes that indicate the the region within a factor of 3 to the line
      flux.
      Default: `True`

    lineObs : list(:class:`~prodimopy.read.DataLineObs`)
      a list of :class:`~prodimopy.read.DataLineObs` should include all the
      lines that were include in the line transfer and in the same order.
      The observations are plotted together with the model line fluxes.
      if `None` no observations are plotted.
      Default: `None`

    peakFlux : boolean
      If `True` use the peakFlux from the line profile instead of the total line
      fluex. Is sometimes usefull to make predictions for observations, as in that
      case the peakFlux is often used to estimate observing times.
      Only works with useLineEstimate=False and jansky=True

    TODO: split lines and lineEstimates plots

    TODO: if not FlineEstimates than it would be also possible to plot all lines for which line transfer is done
    """
    print("PLOT: plot_lines ...")

    if peakFlux is True and (useLineEstimate is True or jansky is False):
      print("WARN: ","peakFlux=True can only be used for useLineEstimate=False and jansky=True")
      peakFlux=False

    # FIXME: enable sfigs for both cases
    if len(lineIdents)>10:
      fig,ax=plt.subplots(1,1,figsize=self._sfigs(sfigs=[2.0,1.0]))
    else:
      fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    imodel=0
    lticks=list()
    # for some reason this dummy is require
    lticks.append("")

    ymin=1.e100
    ymax=1.e-100
    for model in models:
      iline=1
      x=list()
      y=list()
      yCont=list()
      for ident in lineIdents:
        line=None

        x.append(iline)

        if useLineEstimate:
          line=model.getLineEstimate(ident[0],ident[1])
        else:  # use the line fluxes, uses only the wavelength
          line=model.getLine(ident[1],ident=ident[0])
          # it can happen that one of the models does not contain a certain line

        # Convert lineflux to Jansky
        if line is not None:
          if jansky:
            if peakFlux:
              y.append(np.max(line.profile.flux)-line.fcont)
            else:
              y.append(line.flux_Jy)

            if showCont is True:
              yCont.append(line.fcont)
          else:
            y.append(line.flux)

        else:
            y.append(None)

        if imodel==0:
          if xLabelGHz is True:
            lticks.append(r"$\mathrm{"+line.ident+r"}$ "+r"{:.1f}".format(line.frequency)+r"$\,$GHz")
          else:
          # lticks.append(r"$\mathrm{"+prodimopy.plot.spnToLatex(ident[0])+r"}$ "+r"{:.2f}".format(line.wl))
          # FIXME: spnToLatex does not work here with all line names ...
            lticks.append(r"$\mathrm{"+line.ident+r"}$ "+r"{:.2f}".format(line.wl))

        iline=iline+1

      mew=None
      ms=4
      if self.markers[imodel]=="+" or self.markers[imodel]=="x":
        mew=1.5
        ms=4
      elif self.markers[imodel]=="*" or self.markers[imodel]=="p":
        ms=4

      ax.plot(x,y,marker=self.markers[imodel],linestyle='None',ms=ms,mew=mew,
              color=self.colors[imodel],markeredgecolor=self.colors[imodel],label=model.name,
              zorder=10)

      y=np.array(y)
      ymin=np.nanmin([np.nanmin(y[y is not None]),ymin])
      ymax=np.nanmax([np.nanmax(y[y is not None]),ymax])

      if showCont:
        # shift the continuum a bit
        ax.plot(x,yCont,marker="s",linestyle='None',ms=ms,mew=mew,
              color=self.colors[imodel],markeredgecolor=self.colors[imodel],
              zorder=12)

      imodel=imodel+1

    # boxes for factor 3 and 10 relative to the last model
    if showBoxes and lineObs is None:
      for i in range(len(x)):
        if y[i] is not None:
          xc=x[i]-0.3
          yc=y[i]/3.0
          height=y[i]*3.0-y[i]/3.0
          width=0.6
          ax.add_patch(patches.Rectangle((xc,yc),width,height,color="0.8"))

          height=y[i]*10.0-y[i]/10.0
          yc=y[i]/10.0
          ax.add_patch(patches.Rectangle((xc,yc),width,height,color="0.5",fill=False,linewidth=0.5))

    if lineObs!=None:

      # use the line idents, assumes that the lineobs are consistent
      # with the line transfer .... ist not really checked by ProDiMo, but
      # also does not make much sense otherwise. Cannot use the line estimates
      # here
      nlines=len(lineIdents)

      ylinesObs=np.zeros(shape=(nlines))
      ylinesObsErr=np.zeros(shape=(2,nlines))
      ylinesObsErr2=np.zeros(shape=(2,nlines))
      ylinesObsUl=list()

      i=0
      for ident in lineIdents:
        lineIdx=model._getLineIdx(ident[1],ident=ident[0])

        ylinesObs[i]=lineObs[lineIdx].flux
      # for the errors and errorbars

        ylinesObsErr[:,i]=lineObs[lineIdx].flux_err
        ylinesObsErr2[0,i]=(lineObs[lineIdx].flux)/2.0
        ylinesObsErr2[1,i]=lineObs[lineIdx].flux
        # print linesObs[i].flag
        if lineObs[lineIdx].flag=="ul":
          ylinesObsUl.append(ylinesObs[i]/0.5)
          ylinesObsErr[0,i]=ylinesObs[i]*0.4
          ylinesObsErr[1,i]=0.0
          ylinesObsErr2[0,i]=lineObs[lineIdx].flux*(1.0-1.e-10)
        else:
          ylinesObsUl.append(0.0)

        i+=1

      # the observations
      # takes the x from above
      if showBoxes:
        ax.errorbar(x,ylinesObs,yerr=ylinesObsErr2,fmt=".",ms=0.0,color="lightgrey",linewidth=10)
      ax.errorbar(x,ylinesObs,yerr=ylinesObsErr,uplims=ylinesObsUl,fmt="o",ms=4.0,color="black",capsize=2,label=lineObsLabel,zorder=5)

    ax.set_xlim(0.5,iline-0.5)

    loc=plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)

    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])
    else:
      ax.set_ylim(ymin/2,ymax*2)

    ax.semilogy()

    if jansky:
      if peakFlux:
        ax.set_ylabel(r" peak line flux [Jy]")
      else:
        ax.set_ylabel(r" line flux [Jy km$\,$s$^{-1}$]")
    else:
      ax.set_ylabel(r" line flux [W$\,$m$^{-2}$]")

    if showGrid:
      xgrid=np.array(x)
      # ygrid=ax.get_yticks()
      # print(ygrid)
      ax.vlines(xgrid-0.5,ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],linestyle="solid",linewidth=0.5,color="grey",zorder=-100)
      # ax.hlines(ygrid,xmin=ax.get_xlim()[0],xmax=ax.get_xlim()[1],linestyle="solid",linewidth=0.5,color="grey",zorder=100)
      ax.yaxis.grid(color="grey",zorder=-100)

    ax.set_xticklabels(lticks,rotation='70',minor=False)
    zed=[tick.label.set_fontsize(7) for tick in ax.xaxis.get_major_ticks()]

    self._legend(ax,**kwargs)

    if "title" in kwargs and kwargs["title"]!=None:
      ax.set_title(kwargs["title"])

    return self._closefig(fig)

  def plot_NH(self,models,sdscale=False,marker=None,**kwargs):
    '''
    Plots the total vertical hydrogen column density as a function of radius for
    all given models.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    sdscale : boolean
      set to `True` to show the scale in g/cm^2 for the second y axis
      Default : `False`

    marker : str
      if not None plot also the given marker symbol.
      Default : `None`

    '''
    print("PLOT: plot_NH ...")
    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    xmin=1.e100
    xmax=0

    iplot=0
    for model in models:
      x=model.x[:,0]
      y=model.NHver[:,0]

      # print y.min()
      line,=ax.plot(x,y,self.styles[iplot],marker=marker,ms=3.0,color=self.colors[iplot],label=model.name)
      if line.is_dashed(): self._set_dashes(line)

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)

    ax.set_xlim(xmin,xmax)

    ax.semilogy()
    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"N$_\mathrm{<H>}$ [cm$^{-2}]$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    if sdscale:
      ax2=ax.twinx()
      ax2.set_ylabel(r"$\Sigma\,\mathrm{[g\,cm^{-2}]}$")
      # ax2.set_xlim(xmin, xmax)

        # this needs to be done to get the correct scale
      ylim=np.array(ax.get_ylim())*model.muH
      ax2.set_ylim(ylim)

      # cannot do the full kwargs again but if ylog in kwargs I also have
      # to set this here again.
      ax2.semilogy()
      if "ylog" in kwargs:
        if kwargs["ylog"]:
          ax2.semilogy()
        else:
          ax2.set_yscale("linear")

    return self._closefig(fig)

  def plot_tcdspec(self,models,species,relToH=False,facGrayBox=3.0,ice=False,ax=None,**kwargs):
    '''
    Plots the total vertical columndensity for the given species for all the models
    as a function of the radius.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    species : str
      the name of the species to plot.

    relToH : boolean
      Plot the columnd density relative to the total hydrogen columne density.
      Which is essential equal to the average abundance at a certain radius.
      DEFAULT: `False`

    facGrayBox : float
      Plot a gray area for each column density line with  width given by
      `y / facGrayBox` and  `y * facGrayBox`. Uses matplotlib:fill_between.
      Set to `None` if it should not be plotted.
      DEFAULT: 3

    ice : boolean
      Plot also the ice phase column density if the ice species exists.

    '''
    print("PLOT: plot_tcdspec ...")
    fig,ax=self._initfig(ax,**kwargs)
    # fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    xmin=1.e100
    xmax=0

    iplot=0
    for model in models:
      if species in model.spnames:
        x=model.x[:,0]
        y=model.cdnmol[:,0,model.spnames[species]]
        if relToH==True:
          y=y/model.NHver[:,0]

        # FIXME: harcoded linewidths are not very nice
        linewidth=1.5
        if self.styles[iplot]=="--": linewidth=2.0
        if self.styles[iplot]==":": linewidth=2.0

        line,=ax.plot(x,y,self.styles[iplot],marker=None,linewidth=linewidth,
                color=self.colors[iplot],label=model.name)
        # FIXME: should only be applied for real dashed
        # However, there are other ways to set the dashed line style (in words ..)
        if line.get_linestyle()=="--":
          self._set_dashes(line)

        if ice and species+"#" in model.spnames:
          y=model.cdnmol[:,0,model.spnames[species+"#"]]
          if relToH==True:
            y=y/model.NHver[:,0]

          lineice,=ax.plot(x,y,"--",marker=None,linewidth=linewidth,
                  color=line.get_color())
          # FIXME: should only be applied for real dashed
          # However, there are other ways to set the dashed line style (in words ..)
          if lineice.get_linestyle()=="--":
            self._set_dashes(line)

        iplot=iplot+1

        if min(x)<xmin: xmin=min(x)
        if max(x)>xmax: xmax=max(x)

    if iplot==0:
      print("WARN: Species "+species+" not found in any model!")
      plt.close(fig)
      return

    # TODO: make a paremter so that it is possible to provide the index
    # of the reference model
    if facGrayBox is not None:
      # x = models[-2].x[:, 0]
      # y = models[-2].cdnmol[:, 0, model.spnames[species]]
      ax.fill_between(x,y/facGrayBox,y*facGrayBox,color='0.8')
    ax.set_xlim(xmin,xmax)
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    speclabel=prodimopy.plot.spnToLatex(species)
    if ice and species+"#" in model.spnames:
      speclabel=speclabel+","+prodimopy.plot.spnToLatex(species+"#")

    if relToH==True:
      ax.set_ylabel(r"average $\mathrm{\epsilon("+speclabel+")}$ ")
    else:
      ax.set_ylabel(r"N$_\mathrm{"+speclabel+"}$ "+"[cm$^{-2}$]")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_tauline(self,models,lineIdent,xlog=True,**kwargs):
    """
    Plots the line optical depths as a function of radius for a given line.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    lineIdent : array_like(ndim=1)
      two elment array. First item lineIdent (e.g. CO) second item wavelenght (mu m)
      see also :meth:`~prodimopy.read.Data_ProDiMo.getLineEstimate`


    FIXME: better treatment if no lines are found (should not crash).
    """
    print("PLOT: plot_tauline ...")
    fig,ax=plt.subplots(1,1)

    xmin=1.e100
    xmax=0

    iplot=0
    for model in models:
      x=model.x[:,0]
      lineEstimate=model.getLineEstimate(lineIdent[0],lineIdent[1])

      if lineEstimate is None: continue

      y=list()
      ytauDust=list()
      for rInfo in lineEstimate.rInfo:
        y.append(rInfo.tauLine)
        ytauDust.append(rInfo.tauDust)

      ax.axhline(y=1.0,linestyle="-",color="black",linewidth=0.5)
      ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
      # ax.plot(x,ytauDust,"--",marker=None,color="black")

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)

    # nothing to plot
    if iplot==0:
      print("WARN: no lineEstimates to plot ")
      return

    ax.set_xlim(xmin,xmax)

    if "xlim" in kwargs: ax.set_xlim(kwargs["xlim"])
    if "xmin" in kwargs: ax.set_xlim(xmin=kwargs["xmin"])
    if "ylim" in kwargs: ax.set_ylim(kwargs["ylim"])

    if xlog==True: ax.semilogx()

    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"$\mathrm{\tau_{line}}$")
    if lineEstimate is not None:
      ax.set_title(lineEstimate.ident+" "+"{:.2f}".format(lineEstimate.wl)+" $\mathrm{\mu m}$")

    self._legend(ax)

    return self._closefig(fig)

  def plot_avgabun(self,models,species,**kwargs):
    '''
    Plots the average abundance of the species as a function of radius.
    The avergae abundance is given by the vertical column density of the species
    divided by the total hydrogen column density.


    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      The models to plot.

    species : str
      The name of the species to plot.

    '''
    print("PLOT: plot_avgabun ...")

    fig,ax=plt.subplots(1,1)

    iplot=0
    for model in models:
      # get the species
      if (species in model.spnames):
        y=model.cdnmol[:,0,model.spnames[species]]
        y=y/model.NHver[:,0]
        x=model.x[:,0]

        ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)

        iplot=iplot+1

    if iplot==0:
      print("Species "+species+" not found in any model!")
      return

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"average $\epsilon(\mathrm{"+prodimopy.plot.spnToLatex(species)+"})$")

    # do axis style
    ax.semilogy()

    self._dokwargs(ax,**kwargs)
    self._legend(ax)

    return self._closefig(fig)

  def plot_abunvert(self,models,r,species,**kwargs):
    '''
    Plot abundances at the given radius `r` as a function of height.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      The models to plot.

    r : float
      The radius at which the plot should be made
      UNIT: `[au]`

    species : str
      The species name for which the abundance should be plotted.

    '''

    print("PLOT: plot_abunvert ...")

    rstr=r"r$\approx${:.2f} au".format(r)

    fig,ax=plt.subplots(1,1)

    iplot=0
    for model in models:
      # closed radial point to given radius
      ix=(np.abs(model.x[:,0]-r)).argmin()

      old_settings=np.seterr(divide='ignore')
      x=np.log10(model.NHver[ix,:])
      np.seterr(**old_settings)  # reset to default

      y=model.nmol[ix,:,model.spnames[species]]/model.nHtot[ix,:]

      line,=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
      if line.is_dashed(): self._set_dashes(line)

      iplot=iplot+1

    ax.set_xlim([17.5,x.max()])
    # print ax.get_xlim()

#     ax2 = ax.twiny()
#     ax2.set_xlabel("z/r")
#     ax2.set_xlim(ax.get_xlim())
#     #ax2.set_xticks(ax.get_xticks())
#     ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

    ax.set_xlabel(r"$\mathrm{\log N_{<H>} [cm^{-2}]}$ @"+rstr)
    ax.set_ylabel(r"$\mathrm{\epsilon("+prodimopy.plot.spnToLatex(species)+"})$")

    # do axis style
    ax.semilogy()

    self._dokwargs(ax,**kwargs)
    self._legend(ax)
    # ax.text(0.025, 0.025, rstr,
    #   verticalalignment='bottom', horizontalalignment='left',
    #   transform=ax.transAxes,alpha=0.75)

    return self._closefig(fig)

  def plot_radial(self,models,fields,ylabel,zidx=0,ax=None,showlegend=True,**kwargs):
    '''
    Plots a quantitiy in radial direction. Fields must have the same number
    of entries as models and must contain arrays with the dimension of nx.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot.

    fields : list(array_like(float,ndim=1))
      A list of the data to plot. Each entry in the list needs to be an array
      with dimension of `NX` and corresponds to one model. The order has to
      be the same as for the `models` list.

      Example to produce a proper fields list.

      .. code-block:: python

        zidx=5
        fields=[mod.rhog[:,zidx] for mod in models]

    ylabel : str
      The label for the y Axis of the plot.

    zidx : int
      The z index for which height the radial plot should be made.
      This is use to properly calculat the radius.
      DEFAULT: `z=0`

    '''
    print("PLOT: radial ...")
    fig,ax=self._initfig(ax)

    iplot=0
    xmin=1.e100
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:
      x=np.sqrt(model.x[:,zidx]**2+model.z[:,zidx]**2)
      y=fields[iplot]

      line,=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
      if line.is_dashed(): self._set_dashes(line)

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    if showlegend: self._legend(ax,**kwargs)

    return self._closefig(fig)

  # FIXME: plot radial and plot_midplane are more or less the same thing
  # extend plot_radial so that also a string can be used as a field name
  # e.g. that does not require to bould the fields array ...
  # however, also the species thing should still work ...
  # FIXME: xlim is difficult to set automatically if a field is given.
  #        however, in that case xlim can always be set manually
  def plot_midplane(self,models,fieldname,ylabel,
                    xfieldname=None,xlabel=None,species=None,patches=None,
                    scaleToRin=False,**kwargs):
    '''
    Plots a quantitiy in in the midplane as a function of radius.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    fieldname : str
      fieldname is any atrribute of :class:`~prodimopy.read.Data_ProDiMo`

    ylabel : str
      The label for the y axis of the plot.

    xfieldName : str
      xfieldName is any atrribute of :class:`~prodimopy.read.Data_ProDiMo` and
      will be used as the x coordinate in the plot. If `xfieldName=None` the
      x coordinate of the models is used. DEFAULT: `None`

    xlabel : str
      The label for teh x-coordinate of the plot.

    species : str
      The name of a chemical species. If set the abundance of this species is plotted.
      DEFAULT: `None`

    patches : matplotlib.patches object
      A matplotlib patches object that is overplotted on the figure.

    scaleToRin : boolean
      If `True` the `r-Rin` is used for the x-coordinate of the plot.

    '''
    print("PLOT: plot_midplane ...")
    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    iplot=0
    xmin=1.e100
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:
      if xfieldname is not None:
        x=getattr(model,xfieldname)[:,0]
      else:
        x=model.x[:,0]

      if scaleToRin:
        x=x-model.x[0,0]+1.e-5*model.x[0,0]

      if species!=None:
        y=getattr(model,fieldname)[:,0,model.spnames[species]]/model.nHtot[:,0]
      else:
        y=getattr(model,fieldname)[:,0]

      line,=ax.plot(x,y,self.styles[iplot],color=self.colors[iplot],label=model.name,ms=3)
      if self.styles[iplot]=="--": self._set_dashes(line)

      if "markradius" in kwargs:
        r=kwargs["markradius"]
        ix=(np.abs(model.x[:,0]-r)).argmin()
        ax.scatter(x[ix],y[ix],marker="o",color=self.colors[iplot],edgecolor="face")

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    # Some special stuff for the XRT paper, because it did not
    # work with patches
    # ax.axhline(1.e-17,linestyle="-",color="0.7",linewidth=1.0,zorder=-20)
    # ax.axhline(1.e-19,linestyle="--",color="0.7",linewidth=1.0,zorder=-20)

    # TODO: check this patches stuff again, it seems to cause problems
    # in some of the pdf viewers
    if patches is not None:
      for patch in patches:
        if type(patch) is lines.Line2D:
          ax.add_line(patch)
        else:
          ax.add_patch(patch)

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.semilogy()

    if xlabel is not None:
      ax.set_xlabel(xlabel)
    elif scaleToRin:
      ax.set_xlabel(r"r-R$_\mathrm{in}$ [au]")
    else:
      ax.set_xlabel(r"r [au]")

    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_vertical_nH(self,models,r,field,ylabel,species=None,patches=None,showR=True,**kwargs):
    '''
    Plots a quantity (field) as a function of height (column density) at a certain
    radius.
    If field is a string it is interpreted as a field name in the ProDiMo
    data structure. If field is a list the list is directly used.
    The list needs to contain 2D arrays with the same shape as other ProDiMo fields
    '''
    print("PLOT: plot_vertical_nH ...")
    rstr=r"r$\approx${:.0f} au".format(r)

    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    iplot=0
    xmin=1.e100
    xmax=-1.e100
    ymin=1.e100
    ymax=-1.e100
    for model in models:
      # closest radial point to given radius
      ix=(np.abs(model.x[:,0]-r)).argmin()

      old_settings=np.seterr(divide='ignore')
      x=np.log10(model.NHver[ix,:])
      np.seterr(**old_settings)  # reset to default

      if species==None:

        isstr=False
        # FIXME: the python 3 compiler shows an error here for basestring
        try:  # this is for pyhton 2/3 compatibility
          isstr=isinstance(field,basestring)
        except NameError:
          isstr=isinstance(field,str)

        if isstr:
          y=getattr(model,field)[ix,:]
        else:
          y=(field[iplot])[ix,:]

      else:
        y=getattr(model,field)[ix,:,model.spnames[species]]

      line,=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
      if self.styles[iplot]=="--":
        self._set_dashes(line)

      if "markmidplane" in kwargs:
        print(x)
        ax.scatter(x[0],y[0],marker="o",color=self.colors[iplot],edgecolor="face")

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    # TODO: check this patches stuff again, it seems to cause problems
    # in some of the pdf viewers
    if patches is not None:
      for p in patches:
        ax.add_patch(p)

    # some special stuff for the XRT paper
    # ax.axhline(1.e-17,linestyle="-",color="0.7",linewidth=1.0,zorder=-20)
    # ax.axhline(1.e-19,linestyle="--",color="0.7",linewidth=1.0,zorder=-20)
    # idxr=np.argmin(np.abs(model.x[:,0]-r))
    # idxNHrad=np.argmin(np.abs(model.NHrad[idxr,:]-2.e24))
    # nhVer=np.log10(model.NHver[idxr,idxNHrad])
    # ax.axvline(nhVer,color="0.7",zorder=-20,linewidth=1.0)

    # ax.semilogx()
    ax.semilogy()
    if showR:
      ax.set_xlabel(r"$\mathrm{log\,N_{<H>,ver}\,[cm^{-2}]}$ at "+rstr)
    else:
      ax.set_xlabel(r"$\mathrm{log\,N_{<H>,ver}\,[cm^{-2}]}$")
    ax.set_ylabel(ylabel)

    # TODO: that should be an option and not fixed, I also do not know what the 15 is
    ax.yaxis.set_major_locator(plticker.LogLocator(base=10.0,numticks=15))

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_vertical(self,models,r,fieldname,ylabel,fieldnameIdx=None,species=None,ylog=True,xlog=False,
                    zr=True,xfield="zr",showlegend=True,ax=None,**kwargs):
    '''
    Plots a quantity (fieldname) as a function of height (various options) at
    the given radius.

    The routine searches for the closest radial grid point for the given radius,
    no interpolation is done.

    Parameters
    ----------

    fieldname : str
      The name of a field(attribute) of the model data object (:class:`~prodimopy.read.Data_ProDiMo`)

    fieldnameIdx : int
      An additional index in case the quantity to plot has more than the two spatial dimensions.
      e.g. fiels[ix,iz,fieldnameIdx]

    species : str
      A species name. If provided the abundance of this species is plotted.
      `fieldname` has to be `nmol` in that case.

    xfield : str
      Chose the field/quantity that should be used for the x-axis (height).
      Options:

      * `zr` z/r, default
      * `NHver` vertial hydrogen column density.
      * `AVver` vertial visual extinction.
      * `tg` gas temperature.

      If none of those or an unknown value is given the `z` coordinate is used.

    '''
    print("PLOT: plot_vertical ...")
    rstr=r"r$\approx${:.1f} au".format(r)

    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    xmin=1.e100
    xmax=-1.e100
    ymin=1.e100
    ymax=-1.e100
    for model in models:
      # closest radial point to given radius
      ix=(np.abs(model.x[:,0]-r)).argmin()

      if zr and xfield=="zr":
        x=model.z[ix,:]/model.x[ix,0]
      #  xfield=="nH" is just for backward compatibility, should not be use
      elif xfield=="NHver" or xfield=="nH":
        old_settings=np.seterr(divide='ignore')
        x=np.log10(model.NHver[ix,:])
        np.seterr(**old_settings)  # reset to defaul
        zr=False
      elif xfield=="tg":
        x=model.tg[ix,:]
        zr=False
      elif xfield=="AVver":
        old_settings=np.seterr(divide='ignore')
        x=np.log10(model.AVver[ix,:])
        np.seterr(**old_settings)
        zr=False
      elif xfield=="grid":
        zr=False
        x=np.array(range(model.nz))
      else:
        zr=False
        x=model.z[ix,:]

      if species==None:
        getattr(model,fieldname)
        if fieldnameIdx is not None:
          y=getattr(model,fieldname)[ix,:,fieldnameIdx]
        else:
          y=getattr(model,fieldname)[ix,:]
      else:
        y=getattr(model,fieldname)[ix,:,model.spnames[species]]
        y=y/model.nHtot[ix,:]  # abundance"

      ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    if "xlim" in kwargs:
      ax.set_xlim(kwargs["xlim"])
    else:
      if not zr:
        ax.set_xlim(xmin,xmax)

    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])
    # else:
    #  ax.set_ylim(ymin,ymax)

    if ylog: ax.semilogy()
    if xlog: ax.semilogx()

    if zr:
      ax.invert_xaxis()
      ax.set_xlabel(r"z/r @ "+rstr)
    elif xfield=="NHver" or xfield=="nH":
      ax.set_xlabel(r"$\mathrm{\log\,N_{<H>}\,[cm^{-2}]}$ @"+rstr)
    elif xfield=="AVver":
      ax.set_xlabel(r"$\mathrm{\log\,A_{V,ver}}$ @"+rstr)
    elif xfield=="tg":
      ax.set_xlabel(r"$\mathrm{\log\,T_{gas}\,[K]}$ @"+rstr)
      ax.invert_xaxis()
    elif xfield=="grid":
      ax.set_xlabel(r"grididx z @"+rstr)
      ax.invert_xaxis()
    else:
      ax.set_xlabel(r"z [au] @ "+rstr)
      ax.invert_xaxis()

    ax.set_ylabel(ylabel)

    # FIXME: make it general
    self._dokwargs(ax,**kwargs)
    if showlegend: self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_abunradial(self,models,species,perH2=False,**kwargs):
    '''
    Plots the abundance of the given species as a function of radius for the
    midplane of the disk.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    species : str
      The name of the species to plot.

    perH2 : boolean
      Plot the abundance relative to molecular hydrogen number density instead of the total
      hydrogen number density.

    '''
    print("PLOT: plot_abunradial ...")
    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    iplot=0
    xmin=1.e100
    xmax=0
    for model in models:
      x=model.x[:,0]
      if not species in model.spnames: continue
      if perH2:
        y=model.nmol[:,0,model.spnames[species]]/model.nmol[:,0,model.spnames["H2"]]
      else:
        y=model.nmol[:,0,model.spnames[species]]/model.nHtot[:,0]

      # this is not general, removed it
      # if iplot==0 or iplot==(len(models)-1):
      #  line,=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name,linewidth=2.5)
      # else:
      line,=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
      if line.is_dashed(): self._set_dashes(line)

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)

    if iplot==0:
      print("Species: "+species+" not found.")
      return

    ax.set_xlim(xmin,xmax)
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"midplane $\epsilon(\mathrm{"+prodimopy.plot.spnToLatex(species)+"})$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_sed(self,models,plot_starSpec=True,sedObs=None,sedObsModels=False,unit="erg",
               reddening=False,**kwargs):
    '''
    Plots the Seds and the StarSpectrum (optionally).

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    plot_starSpec : boolean
      If `True` also plot the stellar spectrum.

    sedObs : :class:`~prodimopy.read.DataContinuumObs`
      One set of the SED observations to plot (photometry)

    sedObsModels : boolean
      If True use the :class:`~prodimopy.read.DataContinuumObs` object from
      each model individually. So for each model the provided observations are plotted.

    unit : str
      In which unit the SED should be plotted.
      Allowed values: `erg` [erg/s/cm^2], `W` [W/m^2], `Jy`.

    reddening : boolean
      If True also apply the reddening of the SED using the given A_V value from the
      provided observational data.

    '''
    print("PLOT: plot_sed ...")
    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    iplot=0
    xmin=1.e100
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:
      if model.sed==None:
        continue
      # only use every 5 element to speed up plotting
      x=model.sed.lam

      if unit=="W":
        y=model.sed.nuFnuW
      elif unit=="Jy":
        y=model.sed.fnuJy
      else:
        y=model.sed.nu*model.sed.fnuErg

      if reddening is True and model.sedObs is not None and model.sedObs.A_V is not None:
        # idx validity of extinction function
        ist=np.argmin(np.abs(x-0.0912))
        ien=np.argmin(np.abs(x-6.0))
        y[ist:ien]=y[ist:ien]/prodimopy.extinction.reddening(x[ist:ien]*1.e4,a_v=model.sedObs.A_V,r_v=model.sedObs.R_V,model="f99")

      dist=((model.sed.distance*u.pc).to(u.cm)).value
      pl=ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name,
                 linewidth=1.0)
      colsed=pl[0].get_color()
      lwsed=pl[0].get_linewidth()

      if plot_starSpec:
        # scale input Stellar Spectrum to the distance for comparison to the SED
        r=((model.starSpec.r*u.R_sun).to(u.cm)).value

        xStar=model.starSpec.lam[0::10]
        yStar=(model.starSpec.nu*model.starSpec.Inu)[0::10]
        yStar=yStar*(r**2.0*pi*dist**(-2.0))

        if unit=="W":
          yStar=(yStar*u.erg/(u.s*u.cm**2)).to(u.Watt/u.m**2).value
        elif unit=="Jy":
          yStar=(model.starSpec.Inu)[0::10]
          yStar=yStar*(r**2.0*pi*dist**(-2.0))
          yStar=(yStar*u.erg/(u.s*u.cm**2*u.Hz)).to(u.Jy).value

        ax.plot(xStar,yStar,self.styles[iplot],color=colsed,linewidth=0.5*lwsed,zorder=-1,linestyle="--")

        if max(yStar)>ymax: ymax=max(yStar)

#        ax.plot(xStar, yStar, self.styles[iplot], marker="*",ms=0.5,markeredgecolor=colsed,
#                color=colsed,linewidth=0.5*lwsed)

      if sedObsModels is True or (sedObs is not None and iplot==0):
        if sedObsModels is True:
          plSedObs=model.sedObs
          sedcolor=self.colors[iplot]

        else:
          plSedObs=sedObs
          sedcolor="0.5"

        if plSedObs is not None:
          okidx=np.where(plSedObs.flag=="ok")

          xsedObs=plSedObs.lam
          ysedObs=plSedObs.nu*plSedObs.fnuErg
          ysedObsErr=plSedObs.nu*plSedObs.fnuErgErr

          if unit=="W":
            ysedObs=plSedObs.nu*((plSedObs.fnuJy*u.Jy).si.value)
            ysedObsErr=plSedObs.nu*((sedObs.fnuJyErr*u.Jy).si.value)
          elif unit=="Jy":
            ysedObs=plSedObs.fnuJy
            ysedObsErr=plSedObs.fnuJyErr

          ax.errorbar(xsedObs[okidx],ysedObs[okidx],
                      yerr=ysedObsErr[okidx],markeredgecolor="0.3",
                    linestyle="",fmt="o",color=sedcolor,ms=2,linewidth=1.0,
                    markeredgewidth=0.5,zorder=1000,ecolor='0.3')
          # nokidx=np.where(plSedObs.flag!="ok")
          # ax.plot(xsedObs[nokidx],ysedObs[nokidx],linestyle="",
          #        marker=".",markeredgecolor="0.3",markeredgewidth=0.5,
          #        color=sedcolor)
          ulidx=np.where(plSedObs.flag=="ul")
          ax.plot(xsedObs[ulidx],ysedObs[ulidx],linestyle="",marker="v",color="0.5",ms=2.0)

          #            yerr=ysedObsErr[okidx],markeredgecolor="0.3",markeredgewidth=0.2,
          #          linestyle="",fmt="o",color=sedcolor,ms=1,linewidth=1.0,zorder=1000,ecolor='0.3')

          # ax.errorbar(xsedObs[ulidx],ysedObs[ulidx],uplims=True,
          #            yerr=ysedObsErr[okidx],markeredgecolor="0.3",markeredgewidth=0.2,
          #          linestyle="",fmt="o",color=sedcolor,ms=1,linewidth=1.0,zorder=1000,ecolor='0.3')

          if plSedObs.specs is not None:
            for spec in plSedObs.specs:
              nu=(spec[:,0]*u.micrometer).to(u.Hz,equivalencies=u.spectral()).value
              fnuerg=(spec[:,1]*u.Jy).cgs.value
              fnuergErr=(spec[:,2]*u.Jy).cgs.value

              ax.fill_between(spec[:,0],nu*(fnuerg-fnuergErr),nu*(fnuerg+fnuergErr),color='0.8')

              # ax.errorbar(,nu*fnuerg,
              #            yerr=nu*fnuergErr,ms=2,linewidth=0.4,
              #            markeredgewidth=0.5,zorder=1000,ecolor="0.5",
              #            linestyle="-",color="0.3")
              ax.plot(spec[:,0],nu*fnuerg,linestyle=":",linewidth=0.5,
                      color=sedcolor,zorder=2000)

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if y[-1]<ymin: ymin=y[-1]
      if max(y)>ymax: ymax=max(y)
      iplot=iplot+1

    if iplot==0: return

    # set defaults, can be overwritten by the kwargs
    ax.set_xlim(xmin,xmax)
    ax.set_ylim([ymin,None])
    ax.semilogx()
    ax.semilogy()
    ax.set_xlabel(r"wavelength [$\mu$m]")
    if unit=="W":
      ax.set_ylabel(r"$\mathrm{\lambda F_{\lambda}\,[W\,m^{-2}]}$")
    elif unit=="Jy":
      ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")
    else:
      ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")

    self._dokwargs(ax,**kwargs)

    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_dust_opac(self,models,xenergy=False,opactype="both",**kwargs):
    '''
    Plots the dust opacities, absorption, scattering or extinction.
    The pseudo anisotropic scattering is not plotted yet.

    Parameters
    ----------
    opactype : str
      `both` absorption and scattering (separately),
      `abs`  only absorption,
      `sca`  only scattering,
      `ext`  only extinction

    '''
    print("PLOT: plot_dust_opac ...")
    fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))

    iplot=0
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:

      # plot versus energy (keV), usefull for xrays
      if xenergy:
        x=((model.dust.lam*u.micron).to(u.keV,equivalencies=u.spectral()).value)
      else:
        x=model.dust.lam

      if opactype=="ext":
        y=model.dust.kabs+model.dust.ksca
        # TODO: this is not consistent with providing the linestyle via the
        # command line

        label=model.name
        linest=self.styles[iplot]

        ax.plot(x,y,color=self.colors[iplot],linestyle=linest,label=label)

      else:
        if opactype=="both" or opactype=="abs":
          y=model.dust.kabs
          # TODO: this is not consistent with providing the linestyle via the
          # command line

          if opactype=="both":
            label=model.name+" abs"
            linest="-"
          else:
            label=model.name
            linest=self.styles[iplot]

          lineabs,=ax.plot(x,y,color=self.colors[iplot],linestyle=linest,
                label=label)

        if opactype=="both" or opactype=="sca":
          # TODO: this is not consistent with providing the linestyle via the
          # command line
          y=model.dust.ksca

          if opactype=="both":
            col=lineabs.get_color()
            linest="--"
            label=model.name+" sca"
          else:
            col=self.colors[iplot]
            linest=self.styles[iplot]
            label=model.name

          line,=ax.plot(x,y,color=col,linestyle=linest,
                label=label)
          if line.is_dashed(): self._set_dashes(line)

      # y=model.dust.ksca_an*1000.0
      # line, =ax.plot(x, y, color=lineabs.get_color(),linestyle=":",
      #        label=model.name+" sca (pa)")

      iplot=iplot+1

      if max(x)>xmax: xmax=max(x)
      if np.nanmin(y)<ymin: ymin=np.nanmin(y)

      if max(y)>ymax: ymax=max(y)

    # TODO: sometimes it is just zero
    if ymin<1.e-100: ymin=1.e-20
    # set defaults, can be overwritten by the kwargs
    # ax.set_xlim(xmin,xmax)
    # ax.set_ylim([ymin,ymax])
    ax.semilogx()
    ax.semilogy()
    if opactype=="ext":
      ax.set_ylabel(r"ext. opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")
    if opactype=="both":
      ax.set_ylabel(r"opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")
    elif opactype=="abs":
      ax.set_ylabel(r"abs. opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")
    elif opactype=="sca":
      ax.set_ylabel(r"sca. opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")
    if xenergy:
      ax.set_xlabel(r"Energy [keV]")
    else:
      ax.set_xlabel(r"wavelength $\mathrm{[\mu m]}$")

    self._dokwargs(ax,**kwargs)

    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_starspec_xray(self,models,nuInu=False,ax=None,**kwargs):
    '''
    Plots the X-ray spectrum.
    '''
    print("PLOT: plot_starspec_xray ...")
    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:

      idx=np.argmin(np.abs(model.starSpec.lam-0.0124))
      x=model.starSpec.lam[0:idx:2]
      x=x*(u.micrometer).cgs
      x=(const.h.cgs*const.c.cgs/x).to(u.keV)
      x=x.value
      y=(model.starSpec.Inu)[0:idx:2]
      if nuInu:
        y=y*model.starSpec.nu[0:idx:2]
      x=x[::-1]
      y=y[::-1]

      ax.plot(x,y,color=self.colors[iplot],linestyle=self.styles[iplot],
              label=model.name)

#      ax.plot(x, y, color=self.colors[iplot],linestyle=self.styles[iplot],
#              marker=self.markers[iplot],ms=2,markeredgecolor=self.colors[iplot],
#              label=model.name)

      iplot=iplot+1

      if max(x)>xmax: xmax=max(x)
      if np.nanmin(y)<ymin: ymin=np.nanmin(y)

      if max(y)>ymax: ymax=max(y)

    xmin=0.1  # keV

    # TODO: sometimes it is just zero
    if ymin<1.e-100: ymin=1.e-20
    # set defaults, can be overwritten by the kwargs
    ax.set_xlim(xmin,xmax)
    ax.set_ylim([ymin,ymax])
    ax.semilogx()
    ax.semilogy()
    if nuInu:
      ax.set_ylabel(r"$\mathrm{\nu I_\nu\,[erg\,cm^{-2}\,s^{-1}\,sr^{-1}]}$")
    else:
      ax.set_ylabel(r"$\mathrm{I_\nu\,[erg\,cm^{-2}\,s^{-1}\,sr^{-1}\,Hz^{-1}]}$")
    ax.set_xlabel(r"Energy [keV]")

    self._dokwargs(ax,**kwargs)

    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_starspec(self,models,step=10,xunit="micron",nuInu=True,ax=None,**kwargs):
    '''
    Plots the full Stellar Spectrum for each model.

    Parameters
    ----------
    models : list(:class:`~prodimopy.read.Data_ProDiMo`)
      the models to plot

    step : int
      Only plot every `step` point of the spectrum.

    xunit : str
      Unit for the x-axis. Currently `mircon` and `eV` are possible.

    nuInu : boolean
      Plut nu times Inu instead of Inu only.

    '''
    print("PLOT: plot_starspec ...")
    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    xmin=1.e100
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    for model in models:

      x=model.starSpec.lam[0::step]
      if xunit=="eV":
        x=(x*u.micron).to(u.eV,equivalencies=u.spectral()).value
        # switch the axes
        xmin=(1000.0*u.micron).to(u.eV,equivalencies=u.spectral()).value
        xmax=x.max()
        xlabel=r"energy [eV]"
      else:
        xmin=x.min()
        xmax=1000.0
        xlabel=r"wavelength [$\mathrm{\mu}$m]"

      y=(model.starSpec.Inu)[0::step]
      if nuInu:
        y=y*model.starSpec.nu[0::step]

      ax.plot(x,y,color=self.colors[iplot],linestyle=self.styles[iplot],
              ms=2,markeredgecolor=self.colors[iplot],linewidth=1.0,
              label=model.name)
      # marker=self.markers[iplot],

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if y[-1]<ymin: ymin=y[-1]

      if max(y)>ymax: ymax=max(y)

    # TODO: sometimes it is just zero
    if ymin<1.e-100: ymin=1.e-20
    # set defaults, can be overwritten by the kwargs
    ax.set_xlim(xmin,xmax)
    ax.set_ylim([ymin,ymax])
    ax.semilogx()
    ax.semilogy()
    if nuInu:
      ax.set_ylabel(r"$\mathrm{\nu I_\nu\,[erg\,cm^{-2}\,s^{-1}\,sr^{-1}]}$")
    else:
      ax.set_ylabel(r"$\mathrm{I_\nu\,[erg\,cm^{-2}\,s^{-1}\,sr^{-1}\,Hz^{-1}]}$")
#    ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")
    ax.set_xlabel(xlabel)

    self._dokwargs(ax,**kwargs)

    self._legend(ax)

    return self._closefig(fig)

  def plot_line_profil(self,models,wl,ident=None,linetxt=None,lineObs=None,
                       unit="Jy",normalized=False,**kwargs):

    print("WARN: plot_line profil ... please use plot_lineprofile instead. This routine will be removed in the next version.")
    return self.plot_lineprofile(models,wl,ident=ident,linetxt=linetxt,lineObs=lineObs,
                       unit=unit,normalized=normalized,**kwargs)

  def plot_lineprofile(self,models,wl,ident=None,contsub=True,linetxt=None,lineObs=None,
                       normalized=False,convolved=False,style=None,ax=None,**kwargs):
    '''
    Plots the line profile for the given line (id wavelength and line ident)

    Parameters
    ----------
    models : array_like(:class:`~prodimopy.read.Data_ProDiMo`,dim=1)
      the models

    wl : float
      The wavelength of the line in micrometer. Plotted is the line with the wavelength
      closest to `wl`.

    ident : str
      The optional line ident which is additionally use to identify the line.

    contsub : boolean
      Remove the continuum. Default: `True`

    linetxt : str
      A string the is used as the label for the line. Default: `None`

    lineObs : array_like(ndim=1)
      list of :class:`prodimopy.read.DataLineObs` objects. Must be consistent with the list of
      lines from the line radiative transfer.

    normalized : boolean
      if `True` normalize the profile to the peak flux of each line

    convolved : boolean
      if `True` plot the convolved profile.

    style : str
      if style is `step` the profile is plotted as a step function assuming
      the values are the mid point of the bin.

    '''

    print("PLOT: plot_lineprofile ...")
    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    xmin=1.e100
    xmax=-1.e100
    ymin=1.e100
    ymax=-1.e100
    for model in models:
      line=model.getLine(wl,ident=ident)
      if line==None: continue

      # text for the title
      if iplot==0 and linetxt is None:
        linetxt=line.species+"@"+"{:.2f}".format(line.wl)+" $\mathrm{\mu m}$"
      x=line.profile.velo

      # Remove the continuum

      if convolved:
        y=line.profile.flux_conv
        if contsub:
          y=y-line.profile.flux_conv[0]
      else:
        y=line.profile.flux
        if contsub:
          y=y-line.profile.flux[0]

      # normalize to their peak
      if normalized:
        y=y/np.max(y)

      if style=="step":
        ax.step(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name,where="mid")
      else:
        ax.plot(x,y,self.styles[iplot],marker=None,color=self.colors[iplot],label=model.name)
        # ax.plot(x,line.profile.flux_dust,":",marker=None,color=self.colors[iplot],label=model.name)

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    if iplot==0:
      print("WARN: No lines found: ")
      return

    # plot the line profile if it exists
    if lineObs is not None:
      # FIXME: this is not very nice
      # make a warning if lineObs and line Data are not consistent
      # it could be that they are for one model
      lineIdx=models[0]._getLineIdx(wl,ident=ident)

      line=lineObs[lineIdx]
      if line.profile is not None:
        x=line.profile.velo
        y=line.profile.flux
        # # FIXME:
        # if line.profile.flux_unit=="ErgAng":
          # y=line.profile.fluxErgAng
        # else:
          # y=line.profile.flux

        # normalize to their peak
        if normalized:
          y=y/np.max(y)
        if line.profileErr is not None:
          # FIXME: profile error also needs to be converted to the proper units
          ax.fill_between(x,y-line.profileErr ,y+line.profileErr,color='0.8',zorder=0)
        ax.plot(x,y,marker=None,color="black",label="Obs.",zorder=0)

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    # set defaults, can be overwritten by the kwargs
    ax.set_xlim(xmin,xmax)
    ax.set_ylim([ymin,ymax*1.1])

    ax.set_xlabel(r"$\mathrm{velocity\,[km\;s^{-1}}$]")

    if normalized:
      ax.set_ylabel("normalized flux")
    else:
      if line.profile.flux_unit=="ErgAng":
        ax.set_ylabel(r"$\mathrm{flux\,[erg s^{-1}cm^{-2}\AA^{-1}]}$")
      else:
        ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")

    self._dokwargs(ax,**kwargs)

    ax.text(0.03,0.96,linetxt,ha='left',va='top',transform=ax.transAxes)

    self._legend(ax,**kwargs)

    return self._closefig(fig)

