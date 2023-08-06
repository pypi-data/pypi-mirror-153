from __future__ import division
from __future__ import print_function

import copy
import math

from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d

import astropy.units as u
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import prodimopy.extinction
import prodimopy.plot_models


# has to be this way because of circular imports
class Plot(object):
  '''
  Plot routines for a single ProDiMo model.
  '''

  def __init__(self,pdf,fs_legend=None,title=None):
    self.pdf=pdf
    if fs_legend is None:
      self.fs_legend=mpl.rcParams['legend.fontsize']
    else:
      self.fs_legend=fs_legend
    self.ncol_legend=5
    self.title=title

    # special colors, forgot the source for it :( somewhere from the internet)
    # FIXME: make an option to activate them
    self.pcolors={"blue": "#5DA5DA",
                  "orange": "#FAA43A",
                  "green": "#60BD68",
                  "pink": "#F17CB0",
                  "brown": "#B2912F",
                  "purple": "#B276B2",
                  "yellow": "#DECF3F",
                  "red": "#F15854",
                  "gray": "#4D4D4D"}

  def _legend(self,ax,**kwargs):
    '''
    plots the legend, deals with multiple columns
    '''
    handles,labels=ax.get_legend_handles_labels()

    if "loc_legend" in kwargs:
      loc=kwargs["loc_legend"]
    else:
      loc="best"

    if len(labels)>0:
      ncol=1
      if self.ncol_legend>1 and len(labels)>self.ncol_legend:
        ncol=int(len(labels)/self.ncol_legend)

      leg=ax.legend(handles,labels,loc=loc,fancybox=False,ncol=ncol,fontsize=self.fs_legend)
      lw=mpl.rcParams['axes.linewidth']
      leg.get_frame().set_linewidth(lw)

  def _dokwargs(self,ax,**kwargs):
    '''
    Handles the passed kwargs elements (assumes that defaults are already set)
    TODO: make this a general function ....
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

    if self.title!=None and (not "notitle" in kwargs):
      if self.title.strip()!="":
        ax.set_title(self.title.strip())

    if "title" in kwargs:
      if  kwargs["title"]!=None and kwargs["title"].strip()!="":
        ax.set_title(kwargs["title"].strip())
      else:
        ax.set_title("")

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

  def _sfigs(self,**kwargs):
    '''
    Scale the figure size from matplotlibrc by the factors given in the
    array sfigs (in kwargs) the first element is for the width the second for
    the heigth
    '''
    if "sfigs" in kwargs:
      fac=kwargs["sfigs"]
      return scale_figs(fac)
    else:
      return scale_figs([1.0,1.0])

  def plot_grid(self,model,zr=False,ax=None,**kwargs):
    '''
    Plots the spatial grid.

    Also all the standard parameter like xlim, ylim etc. can be used.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    zr : boolean
      show the height z as z/r (scaled by the radius)

    '''

    print("PLOT: plot_grid ...")

    fig,ax=self._initfig(ax)

    ax.plot(model.x,model.z,marker="s",ms=0.03,linestyle="None",color=self.pcolors["gray"])

    ax.semilogy()
    ax.semilogx()
    self._dokwargs(ax,**kwargs)

    ax.set_xlabel("r [au]")
    if zr:
      ax.set_ylabel("z/r")
    else:
      ax.set_ylabel("z [au]")

    return self._closefig(fig)

  def plot_NH(self,model,sdscale=False,muH=None,marker=None,ax=None,**kwargs):
    '''
    Plots the total vertical hydrogen column number density
    as a function of radius.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    sdscale : boolean
      show additionally a scale with units in |gcm^-2|


    Returns
    -------
    :class:`~matplotlib.figure.Figure` or `None`
      object if `self.pdf` is `None` the Figure object is reqturned, otherwise
      otherwise the plot is written directly into the pdf object(file) and
      `None` is returned.
    '''
    print("PLOT: plot_NH ...")
    fig,ax=self._initfig(ax,**kwargs)

    if muH is None:
      muH=model.muH

    x=model.x[:,0]
    y=model.NHver[:,0]
    ax.plot(x,y,marker=marker,ms=3.0,color="black")

    ax.set_xlim(min(x),max(x))

    ax.semilogy()
    ax.semilogx()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"N$_\mathrm{<H>,ver}\,\mathrm{[cm^{-2}]}$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax)

    # second sale on the right
    if sdscale:
      ax2=ax.twinx()
      y=model.NHver[:,0]*muH
      # just plot it again, is the easiest way (needs to be the same style etc)
      ax2.plot(x,y,color="black")
      ax2.set_ylabel(r"$\Sigma\,\mathrm{[g\,cm^{-2}]}$")
      # FIXME: does not allow to manually set xlim
      #        need to check if that works with the two scales
      ax2.set_xlim(min(x),max(x))

      # this needs to be done to get the correct scale
      ylim=np.array(ax.get_ylim())*muH
      ax2.set_ylim(ylim)
      # FIXME: check if this is required!
      ax2.semilogy()

    # ax.yaxis.tick_right()
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.set_ticks_position('both')

    return self._closefig(fig)

  # FIXME: this is not really a general plot ....
  def plot_cont_dion(self,model,zr=True,oconts=None,ax=None,**kwargs):
    '''
    plot routine for 2D contour plots.
    plots the regions where either X-rays, CR or SP are the dominant H2 ionization source
    '''

    values=model.zetaX[:,:]*0.0
    values[:,:]=np.nan
    values[model.zetaX*2.0>(model.zetaCR+model.zetaSTCR)]=1.0
    values[model.zetaSTCR>(model.zetaCR+model.zetaX*2.0)]=0.0
    values[model.zetaCR>(model.zetaSTCR+model.zetaX*2.0)]=-1.0
    # print(values)

    print("PLOT: plot_cont_dion ...")
    cX="#F15854"
    cSP="#5DA5DA"
    cCR="#4D4D4D"

    x=model.x
    if zr:
      y=model.z/model.x
    else:
      y=np.copy(model.z)
      y[:,0]=y[:,0]+0.05

    # levels=[1.5,0.5,0.0,-0.5,-1.5]
    # levels=MaxNLocator(nbins=4, prune="both").tick_values(-1.0,1.0)
    levels=[-1.2,-0.01,0.0,0.01,1.2]
    ticks=[0.5,0.0,-0.5]

    # ticks =
    # print(ticks)

    # sclae the figure size if necessary
    # TODO: maybe provide a routine for this, including scaling the figure size
    fig,ax=self._initfig(ax,**kwargs)

    # stupid trick to plot the masked areas
    # plot everything with one color, and than overplot the other stuff.
    valinv=model.zetaX[:,:]*0.0
    valinv[:,:]=10
    # valinv[valinv != 10.0]=np.nan
    CS2=ax.contourf(x,y,valinv,levels=[9.0,10.0,11.0],colors="0.6",hatches=["////","////","////"])
    for c in CS2.collections:
      c.set_edgecolor("face")

    CS=ax.contourf(x,y,values,levels=levels,colors=(cCR,cSP,cSP,cX))
    # This is the fix for the white lines between contour levels
    for c in CS.collections:
      c.set_edgecolor("face")

    ax.set_ylim([y.min(),y.max()])
    ax.set_xlim([x.min(),x.max()])
    ax.semilogx()

    ax.set_xlabel("r [au]")
    if zr:
      ax.set_ylabel("z/r")
    else:
      ax.set_ylabel("z [au]")

    self._dokwargs(ax,**kwargs)

    if oconts is not None:
      for cont in oconts:
        if cont.filled is True:
          ACS=ax.contourf(x,y,cont.field,levels=cont.levels,
                       colors=cont.colors,linestyles=cont.linestyles,linewidths=cont.linewidths)
        else:
          ACS=ax.contour(x,y,cont.field,levels=cont.levels,
                       colors=cont.colors,linestyles=cont.linestyles,linewidths=cont.linewidths)

    CB=fig.colorbar(CS,ax=ax,ticks=ticks,pad=0.01)
    CB.ax.set_yticklabels(['X','SP','CR'])
    CB.ax.tick_params(labelsize=self.fs_legend)

    # CB.set_ticks(ticks)
    CB.set_label("dominant ionization source",fontsize=self.fs_legend)

    return self._closefig(fig)

  def plot_cont(self,model,values,label="value",zlog=True,grid=False,
                zlim=[None,None],zr=True,clevels=None,clabels=None,contour=True,
                extend="neither",oconts=None,acont=None,acontl=None,nbins=70,
                bgcolor=None,cb_format="%.1f",scalexy=[1,1],patches=None,
                rasterized=False,returnFig=False,fig=None,ax=None,movie=False,**kwargs):
    '''
    Plot routine for 2D filled contour plots.

    If an `ax` object is passed to this routine, it is use
    use to do the plotting. This is especially useful if you want to use that
    routine together with subplots (e.g. a grid of plots). see for example
    :func:`~prodimopy.plot.Plot.plot_abuncont_grid`.

    .. todo::
      * Option for passing a norm (`:class:matplotlib.colors.LogNorm`).
        But that does not work nicely fith contourf and colorbars ... works
        with imshow and pcolormesh though ... maybe switch to pcolormesh.

      * option to pass the name of a color map

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    values : array_like(float,ndim=2)
      a 2D array with numeric values for the plotting. E.g. any 2D array
      of the :class:`~prodimopy.read.Data_ProDiMo` object.

    oconts : array_like(:class:`~prodimopy.plot.Contour`,ndim=1)
      list of :class:`~prodimopy.plot.Contour` objects which will be drawn
      as additional contour levels. See also the example at the top of the page.

    ax : :class:`matplotlib.axes.Axes`
      a matplotlib axis object which will be used for plotting

    scalexy: apply a scaling factor for the x and y coordinate (multiplicative)

    patches: a list of matplotlib.patches objects. For each object in the list
      simply ax.add_patch() is called (at the very end of the routine)

    movie : boolean
      Special mode for movies ...


    .. todo::

      * allow to use grid (ix,iz) as spatial coordinates.
      * update documenation for parameters

    '''
    if not ("nolog" in kwargs):
      print("PLOT: plot_cont ...")

    # prepare the data values
    if zlog is True:
      pvals=plog(values)
      values[np.isnan(values)]=0.0

      # TODO: that looks very complicated
      if zlim[1]==None:
        maxval=np.log10(values.max())
      else:
        maxval=np.log10(zlim[1])
      if zlim[0]==None:
        minval=np.log10(values[values>0.0].min())
      else:
        minval=np.log10(zlim[0])
    else:
      pvals=values
      if zlim[1]==None:
        maxval=values.max()
      else:
        maxval=zlim[1]
      if zlim[0]==None:
        minval=values.min()
      else:
        minval=zlim[0]

    levels=MaxNLocator(nbins=nbins).tick_values(maxval,minval)

    if clevels is not None:
      if zlog: clevels=np.log10(clevels)
      ticks=clevels
    else:
      ticks=MaxNLocator(nbins=6,prune="both").tick_values(minval,maxval)

    # TODO: maybe provide a routine for this, including scaling the figure size
    if ax is None:
      fig,ax=plt.subplots(1,1,figsize=self._sfigs(**kwargs))
    else:
      fig=ax.get_figure()
      returnFig=True

    # prepare the spatial coordinates
    if grid:
      x=model.x[:,:]*0.0
      y=model.z[:,:]*0.0
      zr=False
      # Thhre is properly smarter way to do that
      # for iz in range(model.nz):
      #   x[:,iz]=np.array(range(model.nx))+0.5
      # for ix in range(model.nx):
      #   y[ix,:]=np.array(range(model.nz))+0.5

      x=None
      y=None
      ax.set_ylabel("iz ")
      ax.set_xlabel("ir")
      kwargs["xlog"]=False
      kwargs["zlog"]=False
      kwargs["axequal"]=True
    elif zr:
      x=model.x*scalexy[0]
      y=model.z/model.x
      ax.set_ylabel("z/r")
      ax.set_xlabel("r [au]")
    else:
      x=model.x*scalexy[0]
      y=np.copy(model.z)*scalexy[1]
      y[:,0]=y[:,0]+0.05*scalexy[1]
      ax.set_ylabel("z [au]")
      ax.set_xlabel("r [au]")

    # zorder is needed in case if rasterized is true

    if grid:
      CS=ax.contourf(pvals.T,levels=levels,extend=extend,zorder=-20,extent=(-0.5,model.nx-0.5,0.0,model.nz-1.0))
    else:
      CS=ax.contourf(x,y,pvals,levels=levels,extend=extend,zorder=-20,origin="image")

    # This is the fix for the white lines between contour levels
    for c in CS.collections:
      c.set_edgecolor("face")

    # rasterize the filled contours only, text ect. not
    if rasterized:
      ax.set_rasterization_zorder(-19)

    # axis equal needs to be done here already ... at least it seems so
    if "axequal" in kwargs:
      # FIXME: check how this really works ... do not know why both are used
      # but using ax.axis('equal') only, does not really do the trick
      if kwargs["axequal"]: ax.axis('equal')
      ax.set_aspect('equal',adjustable='box')

    if not grid:
      ax.set_ylim([y.min(),y.max()])
      ax.set_xlim([x.min(),x.max()])
      # under certain circumstances semilogx can cauese problems if later on
      # the scale is changed again. So check if the user actually wanst to change it
      if not ("xlog" in kwargs):
        ax.semilogx()

      # ax.text(0.27, 0.95,kwargs["title"], horizontalalignment='center',
      #   verticalalignment='center',fontsize=8,
      #   transform=ax.transAxes)

    self._dokwargs(ax,**kwargs)

    if contour:
      if clevels is not None:
        # if zlog: clevels=np.log10(clevels)
        # ticks=clevels
        ax.contour(CS,levels=clevels,colors='white',linestyles="--",linewidths=1.0)
      else:
        ax.contour(CS,levels=ticks,colors='white',linestyles="--",linewidths=1.0)

    if oconts is not None:
      for cont in oconts:
        if grid:
          ACS=ax.contour(cont.field.T,levels=cont.levels,extent=(-0.5,model.nx-0.5,0.0,model.nz-1.0),
                         colors=cont.colors,linestyles=cont.linestyles,linewidths=cont.linewidths)
        else:
          ACS=ax.contour(x,y,cont.field,levels=cont.levels,
                         colors=cont.colors,linestyles=cont.linestyles,linewidths=cont.linewidths)
        if cont.showlabels:
          ax.clabel(ACS,inline=True,inline_spacing=cont.label_inline_spacing,
                    fmt=cont.label_fmt,manual=cont.label_locations,fontsize=cont.label_fontsize)

    if acont is not None:
      print("WARN: plot_cont: please use the oconts for additional contours ...")
      # for l in acontl:
      #  ACS=ax.contour(x, y,pvals,levels=[l], colors='black',linestyles="solid",linewidths=1.5)
      #  ax.clabel(ACS, inline=1, fontsize=8,fmt=str(l))
      ACS=ax.contour(x,y,acont,levels=acontl,colors='white',linestyles="solid",linewidths=1.5)
      # quick fix for second contour ...
      # ACS2=ax.contour(x, y,model.nHtot,levels=[1.e6], colors='black',linestyles="solid",linewidths=2.5)
      # ax.clabel(ACS, inline=1, fontsize=8,fmt="%.0f")

#    ax.plot(np.sqrt(model.x[:,0]*model.x[:,0]+model.z[:,45]*model.z[:,45]),model.z[:,45],color="black")
#    ax.plot(np.sqrt(model.x[:,0]*model.x[:,0]+model.z[:,35]*model.z[:,35]),model.z[:,35],color="black")

#    ax.plot(model.x[:,0],model.z[:,48],color="black")
#    ax.plot(model.x[:,0],model.z[:,35],color="black")

    if bgcolor is not None:
      ax.set_axis_bgcolor(bgcolor)

    CB=fig.colorbar(CS,ax=ax,ticks=ticks,pad=0.01,format=cb_format)
    # FIXME: this is not very flexible and confusing
    if clabels is not None:
      CB.ax.set_yticklabels(clabels)
    # CB.ax.tick_params(labelsize=self.fs_legend)
    # CB.set_ticks(ticks)
    CB.set_label(label)

    if patches is not None:
      for patch in patches:
        ax.add_patch(patch)

    if movie: return fig,CS

    if returnFig:
      return fig
    else:
      return self._closefig(fig)

  def plot_ionrates_midplane(self,model,ax=None,**kwargs):

    print("PLOT: plot_ionrates_midplane ...")

    cX=self.pcolors["red"]
    cSP=self.pcolors["blue"]
    cCR=self.pcolors["gray"]

    x=model.x[:,0]

  #  print pdata.zetaCR[ix,:]
    y1=model.zetaCR[:,0]
    y2=model.zetaX[:,0]*2.0  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent
    y3=model.zetaSTCR[:,0]  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent

    fig,ax=self._initfig(ax,**kwargs)

    ax.plot(x,y2,color=cX,label="$\zeta_\mathrm{X}$")
    ax.plot(x,y3,color=cSP,label="$\zeta_\mathrm{SP}$")
    ax.plot(x,y1,color=cCR,label="$\zeta_\mathrm{CR}$")

    # print ax.get_xlim()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel("$\mathrm{\zeta\,per\,H_2\,[s^{-1}]}$")

    ax.semilogy()
    self._dokwargs(ax,**kwargs)
    self._legend(ax)
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles, labels, loc="best", fancybox=False)

    return self._closefig(fig)

  # FIXME: this routine is also not very general (e.g. colors)
  def plot_ionrates(self,model,r,ax=None,**kwargs):

    cX=self.pcolors["red"]
    cSP=self.pcolors["blue"]
    cCR=self.pcolors["gray"]

    ix=(np.abs(model.x[:,0]-r)).argmin()
    rstr="r={:.1f} au".format(model.x[ix,0])

    old_settings=np.seterr(divide='ignore')
    nhver=np.log10(model.NHver[ix,:])
    np.seterr(**old_settings)  # reset to default
  #  print pdata.zetaCR[ix,:]
    y1=model.zetaCR[ix,:]
    y2=model.zetaX[ix,:]*2.0  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent
    y3=model.zetaSTCR[ix,:]

    fig,ax=self._initfig(ax,**kwargs)

    ax.plot(nhver,y2,color=cX,label="$\zeta_\mathrm{X}$")
    ax.plot(nhver,y3,color=cSP,label="$\zeta_\mathrm{SP}$")
    ax.plot(nhver,y1,color=cCR,label="$\zeta_\mathrm{CR}$")

    # set the limits

    ax.set_xlim([17.5,nhver.max()])
    ax.set_ylim([1.e-21,1.e-9])

    ax.set_xlabel(r"$\log$ N$_\mathrm{<H>,ver}$ [cm$^{-2}$]")
    ax.set_ylabel("$\zeta$ per H$_2$ [s$^{-1}$]")

    # do axis style
    ax.semilogy()

    # title does not work here
    self._dokwargs(ax,title=None,**kwargs)

    ax2=ax.twiny()
    ax2.set_xlabel("z/r")
    ax2.set_xlim(ax.get_xlim())
    # ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix,ax.get_xticks(),model)])

    handles,labels=ax.get_legend_handles_labels()
    ax.legend(handles,labels,loc="best")
    ax.text(0.025,0.020,rstr,
       verticalalignment='bottom',horizontalalignment='left',
       transform=ax.transAxes,alpha=0.75)

    return self._closefig(fig)

  def plot_avgabun(self,model,species,ax=None,**kwargs):
    '''
    Plots the average abundance for the given species (can be more than one)
    as a function of radius
    '''
    print("PLOT: plot_avgabun ...")

    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    if(type(species)==str): species=[species]
    for spec in species:
    # get the species
      if (spec in model.spnames):
        y=model.cdnmol[:,0,model.spnames[spec]]
        y=y/model.NHver[:,0]
        x=model.x[:,0]

        style="-"
        if "#" in spec: style="--"
        ax.plot(x,y,linestyle=style,marker=None,label="$\mathrm{"+spnToLatex(spec)+"}$")

        iplot=iplot+1

    if iplot==0:
      print("Species "+species+" not found in any model!")
      return

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"average abundance")
    ax.set_xlim([x.min(),x.max()])

    # do axis style
    ax.semilogy()

    self._dokwargs(ax,**kwargs)
    self._legend(ax)

    return self._closefig(fig)

  def plot_radial(self,model,values,ylabel,zidx=0,
                  color=None,ax=None,**kwargs):
    '''
    Plots a quantity along the radial grid for the given zidx (from the ProDiMo Array)
    as a function of radius.

    Parameters
    ----------

    values : array_like(float,ndim=2) or array_like(float,ndim=2)
        `values` is any ProDiMo 2D array in the :class:`~prodimopy.read.Data_ProDiMo` object,
        or a 1D array with dim `nx` if `zidx` is `None`.

    ylabel : str
        The lable for the y axis.

    zidx : int
        The index of the z coordinate that should be plotted.
        If zidx is `None` the values array has to be 1D and needs to be filled with the proper values.
        Default: 0 (midplane)

    color : str
        A matplotlib color for the line to plot. Default: `None`

    ax : :class:`matplotlib.axes.Axes`
        A matplotlib axes object that will be use to do the actual plotting. No new instance is created.
        Default: None (make a new figure and axes object).


    '''
    print("PLOT: plot_radial ...")
    fig,ax=self._initfig(ax,**kwargs)

    if zidx is None:
      x=np.sqrt(model.x[:,0]**2.0+model.z[:,0]**2.0)
      y=values
    else:
      x=np.sqrt(model.x[:,zidx]**2.0+model.z[:,zidx]**2.0)
      y=values[:,zidx]

    ax.plot(x,y,marker=None,color=color)

    ax.set_xlim(np.min(x),np.max(x))
    ax.set_ylim(np.min(y),np.max(y))
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    # self._legend(ax)

    return self._closefig(fig)

  def plot_cdnmol(self,model,species,colors=None,styles=None,
                  scalefacs=None,norm=None,normidx=None,ylabel="$\mathrm{N_{ver}\,[cm^{-2}}]$",
                  patches=None,ax=None,**kwargs):
    '''
    Plots the vertical column densities as a function of radius for the
    given species.

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the ProDiMo model data.

    species : array_like(str,ndim=1)
      a list of species names that should be plotted.

    scalefacs : array_like(float,ndim=1)
      scale the column density to plot by the given factor.
      `len(scalefacs)` must be equal to `len(species)`.

    norm : float
      an abritary normalizatoin factor (i.e. allo column density are divided by `norm`)

    normidx : int
      normalize the plotted column densities to the column density given by
      `normidx`. Where `normidx` is the index of any species in the list of species in the model.
      TODO: Could actually just use a species name, would be easier to use.

    '''
    print("PLOT: plot_cdnmol ...")

    if colors is None:
      colors=[None]*len(species)

    if styles is None:
      styles=[None]*len(species)

    if(type(species)==str): species=[species]

    fig,ax=self._initfig(ax,**kwargs)

    x=model.x[:,0]

    ymin=1.e99
    ymax=1.e-99

    if scalefacs is None:
      scalefacs=np.ones(len(species))

    if normidx is not None:
      normspec=model.cdnmol[:,0,normidx]

    iplot=0
    for spec,fac in zip(species,scalefacs):

      ispec=-1
      try:
        ispec=model.spnames[spec]
      except:
        print("WARNING: Could not find species: ",spec)
        continue

      if normidx is not None:
        y=model.cdnmol[:,0,ispec]/normspec

      y=model.cdnmol[:,0,ispec]/fac
      if norm is not None:
        y=y/norm

      label="$"+spnToLatex(spec)+"$"
      if fac!=1.0 and norm is None:
        label+="/"+"{:3.1e}".format(fac)

      ax.plot(x,y,marker=None,linestyle=styles[iplot],color=colors[iplot],
              label=label)

      ymin=np.min([np.min(y),ymin])
      ymax=np.max([np.max(y),ymax])
      iplot=iplot+1

    if patches is not None:
      for patch in patches:
        ax.add_patch(copy.copy(patch))

    ax.set_xlim(np.min(x),np.max(x))
    ax.set_ylim(ymin,ymax)
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_midplane(self,model,field,ylabel,xRelTo=None,ax=None,**kwargs):
    '''
    Plots a quantitiy in in the midplane as a function of radius
    fieldname is any field in Data_ProDiMo

    Parameters
    ----------

    xRelTo : float
      use `x-xRelTo` as the x axis. Default: `None` (no shif)


    FIXME: remove the fieldname stuff passe  the whole array ...
    '''
    print("PLOT: plot_midplane ...")
    fig,ax=self._initfig(ax,**kwargs)

    x=model.x[:,0]
    if xRelTo is not None:
      x=x-xRelTo

    if type(field)==str:
      y=getattr(model,field)[:,0]
    else:
      y=field[:,0]

    ax.plot(x,y,marker=None)

    ax.set_xlim(np.min(x),np.max(x))
    ax.set_ylim(np.min(y),np.max(y))
    ax.semilogy()

    if xRelTo is not None:
      ax.set_xlabel("r - {:3.1f} [au]".format(xRelTo))
    else:
      ax.set_xlabel(r"r [au]")
    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    # self._legend(ax)

    return self._closefig(fig)

  def _prepareAbunForPlot(self,model,species,label,rel2H,zlog,zlim,extend):
    '''
    Utility function used in :func:`~prodimopy.plot.Plot.plot_abuncont` and
    :func:`~prodimopy.plot.Plot.plot_abuncont_grid`.
    '''
    # Check if species names exists
    try:
      n_rel_index=model.spnames[species]

    except KeyError:
      print("The species "+species+'''you want to access does not exist
             or is spelled incorrectly. Exiting plot_abuncont routine''')
      return

    if rel2H:
      values=model.getAbun(species)

      if label is None:
        label=r"$\mathrm{\epsilon("+spnToLatex(species)+")}$"
        if zlog: label="log "+label

      # define some default lower limit
      if zlim==None or zlim==[None,None]:
        zlim=[3.e-13,None]
        extend="both"

    else:
      values=model.nmol[:,:,n_rel_index]
      if label is None:
        label=r"$\mathrm{n("+spnToLatex(species)+") [cm^{-3}]}$"
        if zlog: label="log "+label

    return values,label,zlog,zlim,extend

  def plot_abuncont(self,model,species='O',rel2H=True,label=None,zlog=True,
                zlim=[None,None],zr=True,clevels=None,clabels=None,contour=True,
                extend="neither",oconts=None,acont=None,acontl=None,nbins=70,
                bgcolor=None,cb_format="%.1f",scalexy=[1,1],patches=None,
                rasterized=False,ax=None,movie=False,**kwargs):
    '''
    Plots the 2D abundance structure of a species.

    This is a convenience function and is simply a wrapper for
    :func:`~prodimopy.plot.Plot.plot_cont` routine.

    The routine checks if the species exists, calculates the abundance and sets some
    defaults (e.g. label) for the :func:`~prodimopy.plot.Plot.plot_cont` routine and calls it.
    However, all the defaults can be overwritten by providing the corresponding parameter.

    Contributors: L. Klarmann, Ch. Rab

    .. todo::

      can be improved with better and smarter default values (e.g. for the colorbar)


    Parameters
    ----------

    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    species : str
      the name of the species as given in |prodimo|

    rel2H : boolean
      plot abundances relative to the total H nuclei number density.
      If `False` the number density of the species is plotted

    label : str
      the label for the colorbar. If None the default is plotted


    For all other parameters see :func:`~prodimopy.plot.Plot.plot_cont`

    '''
    print('PLOT: plot_abuncont ...')

    values,labelN,zlogN,zlimN,extendN=self._prepareAbunForPlot(model,species,label,rel2H,zlog,zlim,extend)

    return self.plot_cont(model,values,label=labelN,zlog=zlogN,
                zlim=zlimN,zr=zr,clevels=clevels,clabels=clabels,contour=contour,
                extend=extendN,oconts=oconts,acont=acont,acontl=acontl,nbins=nbins,
                bgcolor=bgcolor,cb_format=cb_format,scalexy=scalexy,patches=patches,
                rasterized=rasterized,nolog=True,ax=ax,movie=movie,**kwargs)

  def plot_abuncont_grid(self,model,speciesList=['e-','H2','CO',"H2O"],nrows=2,ncols=2,rel2H=True,label=None,zlog=True,
                zlim=[None,None],zr=True,clevels=None,clabels=None,contour=True,
                extend="neither",oconts=None,acont=None,acontl=None,nbins=70,
                bgcolor=None,cb_format="%.1f",scalexy=[1,1],patches=None,
                rasterized=False,**kwargs):
    '''
    Convenience routine to plot a grid of abundance plots in the same way as
    :func:`~prodimopy.plot.Plot.plot_abuncont`.

    The number of plots is given by `nrows` times `ncols` and should be equal to
    the number of species in `speciesList`

    Parameters
    ----------

    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    speciesList : array_like(str,ndim=1) :
      a list of species names that should be plotted. The plots will be made
      in order of that list, starting from top left to the bottom right of the grid.

    nrows : int
      how many rows should the subplots grid have.

    ncols : in
      how many columns should teh subplots grid have.

    zlim : array_like
      can either be of the form [zmin,zmax] ore a list of such entries ([zmin1,zmax1],[zmin1,zmax1], ....).
      For the latter the number of entries must be equal to the number of species.


    For the other parameters see :func:`~prodimopy.plot.Plot.plot_abuncont`

    '''

    print("PLOT: plot_abuncont_grid ...")

    fig,axes=plt.subplots(nrows,ncols,figsize=scale_figs([ncols,nrows]))

    if zlim==None:
      zlims=[(None,None)]*len(speciesList)
    elif len(np.shape(zlim))==1:
      print(zlim)
      zlims=[zlim]*len(speciesList)
    else:
      zlims=zlim

    iax=0
    for species,zliml in zip(speciesList,zlims):
      if species not in model.spnames:
        print("ERROR: Species "+species+" dose not exist in model.")
        iax=iax+1
        continue

      values,labelG,zlogG,zlimG,extendG=self._prepareAbunForPlot(model,species,label,rel2H,zlog,zliml,extend)

      self.plot_cont(model,values,label=labelG,zlog=zlogG,
                zlim=zlimG,zr=zr,clevels=clevels,clabels=clabels,contour=contour,
                extend=extendG,oconts=oconts,acont=acont,acontl=acontl,nbins=nbins,
                bgcolor=bgcolor,cb_format=cb_format,scalexy=scalexy,patches=patches,
                rasterized=rasterized,fig=fig,ax=axes.flatten()[iax],nolog=True,**kwargs)

      iax=iax+1

    fig.tight_layout()

    return self._closefig(fig)

  def plot_reaccont(self,model,chemana,rtype,level=1,showAbun=False,values=None,label=None,zlog=True,
                zlim=[None,None],clevels=None,clabels=None,contour=True,
                extend="neither",oconts=None,nbins=70,
                bgcolor=None,cb_format="%.1f",patches=None,
                rasterized=True,ax=None,**kwargs):
    '''
    Make a contour plot with the reactions numbers from chemanalyse on top.
    As spatial coordinates the indices of the spatial grid are used.

    This is a convenience function and is simply a wrapper for
    :func:`~prodimopy.plot.Plot.plot_cont` routine.

    The same can be achieved by simply using plot_cont and plot the numbers
    on top (see last part of this routine). Then one has more flexibility.

    Parameters
    ----------

    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    chemana : class:`prodimopy.read.Chemistry`
      data resulting from `prodimopy.read.analise_chemistry` on a single species

    rtype : str
      keyword which sets the type of reactions to be shown (destruction or formation)
      must be set to either 'd' (destruction) or 'f' (formation)

    level : int
      1 means most important, 2 second most important etc.

    showAbun : boolean
      Show the abundances of the species that is analysed as filled contours.

    values : array_like(float,ndim=2)
      a 2D array with numeric values for the plotting like in :func:`~prodimopy.plot.Plot.plot_cont`.
      Howver, it an also be `None` (default) in that case the total formation/destruction rate is plotted.


    sfigs : array_like(float,ndim=2)
      Is part of kwargs. But this one is relevant here as one might needs to make
      the figure larger to see the reactoins numbers. e.g. just pass `sfigs=[2.,2.]`
    '''

    if showAbun:
      values=model.getAbun(chemana.species)
      label=r"$\epsilon("+spnToLatex(chemana.species)+"$)"
      if zlog: label="log "+label

    if rtype is None or rtype!="d": rtype="f"

    reacs=chemana.get_reac_grid(level,rtype)

    rlabel="form."
    if rtype=="d": rlabel="dest."

    if values is None:
      if rtype=="d":
        values=chemana.totdrate
      else:
        values=chemana.totdrate

      label=r"(total "+rlabel+" rate) $[cm^{-3} s^{-1}]$"
      if zlog: label="log "+label

    if not "title" in kwargs:
      if level==1:
        tit="main "+rlabel+" reactions"
      else:
        tit=str(level).strip()+r"$^{nd}$ "+rlabel+" reactions"

      kwargs["title"]=tit

    fig=self.plot_cont(model,values,label=label,zlog=zlog,grid=True,
            zlim=zlim,zr=False,clevels=clevels,clabels=clabels,contour=contour,
            extend=extend,oconts=oconts,acont=None,acontl=None,nbins=nbins,
            bgcolor=bgcolor,cb_format=cb_format,scalexy=[1.0,1.0],patches=patches,
            rasterized=rasterized,nolog=True,ax=ax,movie=False,returnFig=True,**kwargs)

    # this is potentially very slow
    xstart=0
    xend=model.nx
    ystart=0
    yend=model.nz-1
    if "xlim" in kwargs:
      if kwargs["xlim"][0] is not None:
        xstart=kwargs["xlim"][0]

      if kwargs["xlim"][1] is not None:
        xend=kwargs["xlim"][1]

    if "ylim" in kwargs:
      if kwargs["ylim"][0] is not None:
        ystart=kwargs["ylim"][0]

      if kwargs["ylim"][1] is not None:
        yend=kwargs["ylim"][1]

    for i in range(xstart,xend,1):
      for j in range(ystart,yend,1):
        fig.axes[0].text(i,j,reacs[0][i,j],fontsize=3.0,horizontalalignment="center",verticalalignment="bottom",color="white")

    return fig

  def plot_reac_ixiz(self,ix,iz,rtype,chemanas,ages,chemana_steadystate=None,ax=None,**kwargs):
    '''
    Plots the rates for the most important reactions and the point ix,iz for the
    given models and chemanalysis list (i.e. a time-dependent |prodimo| disk model.

    Parameters
    ----------

    ix : int
      The ix index of the grid (starts at 0)

    iz : int
      The iz index of the grid (starts at 0)

    rtype : str
      `f` for formation reactions, `d` for destruction reactions.

    models : list
      a list of :class:`prodimopy.read.Data_ProDiMo` objects (e.g. for each
      age in a time-dependent model).

    chemanas : list
      a list of :class:`prodimopy.read.Chemistry` objects (e.g. for each
      age in a time-dependent model). Must have the same length as `models`

    ages : array_like(float)
      a list of the ages for the time-dependent model. Most have the same lengh
      as `models`. This will be the x-Axis

    chemana_steadystate : tuple
      A tuple (:class:`prodimopy.read.Data_ProDiMo`, :class:`prodimopy.read.Chemistry`) representing
      a steady state model. This is useful to compare the results with the time-dependent model.
      Optional parameter

    '''

    def reacstr(reacid,reactions):
      # a utility function to produce  str for the Reactoins that can be use in the legend
      reaction=list(filter(lambda reac: reac.id==reacid,reactions))[0]

      out="{:4d}".format(reaction.id)+" "+reaction.type+": "
      out+="$"
      out+=r"+".join([spnToLatex(reac) for reac in reaction.reactants])
      out+=r"\rightarrow "
      out+="+".join([spnToLatex(prod) for prod in reaction.products])
      out+="$"
      return out

    nmaxreac=3

    if rtype=="d":
      tit="dest. reactions for "
    else:
      tit="form. reactions for "

    totrates=list()
    reacidx=list()
    # for model,chemana in zip(models,chemanas):
    for chemana in chemanas:
      if rtype=="d":
        totrates.append(chemana.totdrate[ix,iz])
        reacs=chemana.gridd[ix,iz,0]
      else:
        totrates.append(chemana.totfrate[ix,iz])
        reacs=chemana.gridf[ix,iz,0]

      # figure out what reactions indices I want to plot
      for i in range(nmaxreac):
        if i<len(reacs):
          reacidx.append(reacs[i])

    reacidx=np.unique(np.array(reacidx))

    reactions=list()
    for ridx in reacidx:
      rates=list()
      for chemana in(chemanas):
        if rtype=="d":
          rate=chemana.gridd[ix,iz,1][chemana.gridd[ix,iz,0]==ridx]
        else:
          rate=chemana.gridf[ix,iz,1][chemana.gridf[ix,iz,0]==ridx]

        if len(rate)==0:
          rates.append(0.0)
        else:
          rates.append(rate[0])
      reactions.append(rates)

    fig,ax=self._initfig(ax,**kwargs)
    ax.plot(ages,totrates,label="totrate",color="black",linewidth="3")
    for i in range(len(reacidx)):
      # FIXME: this assume that all chemanas have the same chemnet in the background ...
      # is currently the case but might change at some point
      ax.plot(ages,reactions[i],label=reacstr(reacidx[i],chemanas[0].chemnet.reactions))

    # for the steady state model
    if chemana_steadystate is not None:
      reacidxsss=list()
      ratesss=list()
      for i in range(nmaxreac):
        if rtype=="d":
          if i<len(chemana_steadystate.gridd[ix,iz,0]):
            reacidxsss.append(chemana_steadystate.gridd[ix,iz,0][i])
            ratesss.append(chemana_steadystate.gridd[ix,iz,1][i])
        else:
          if i<len(chemana_steadystate.gridf[ix,iz,0]):
            reacidxsss.append(chemana_steadystate.gridf[ix,iz,0][i])
            ratesss.append(chemana_steadystate.gridf[ix,iz,1][i])

      colors=np.arange(0.1,0.9,0.7/nmaxreac)
      for i,(reacidx,rate) in enumerate(zip(reacidxsss,ratesss)):
        # FIXME: this assumes t
        ax.scatter(ages[-1]*1.05,rate,label=reacstr(reacidx,chemana_steadystate.chemnet.reactions),marker="<",color=str(colors[i]),s=20/np.log(i+2))

    ax.legend(bbox_to_anchor=(1.01,1.0),loc='upper left',prop={"family": "monospace","size": 5})

    ax.semilogx()
    ax.semilogy()
    ax.set_xlabel("age [yr]")
    ax.set_ylabel(r"rate $[cm^{-3}\,s^{-1}]$")
    ax.set_title(tit+" ix={:5d}, iz={:5d}".format(ix,iz))

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def plot_reac(self,model,chemistry,rtype,level=1,plot_size=10,lograte=True,grid=True,with_abun=False,vmin=None,**kwargs):
    '''
    Plots the 2D main formation/destruction reaction structure for a given species,
    in each grid point. Each number corresponds to the reaction indices in
    `prodimo.read.chemistry.sorted_form_info` or `prodimo.read.chemistry.sorted_form_info`

    By default it is plotted along the 2D main formation/reaction rate structure, but it
    can also be plotted along the abundance of the species.

    The routine checks if the reaction type is set
    plots the data (lograte, rate or abundance) as an image, and fills in the reaction
    indices for each grid point.

    An index of 0 means that the total rate at that point was so low it didn't get
    registered in chemanalysis.out (in ProDiMo)

    Contributors: G. Chaparro, Ch. Rab



    .. warning::
        This routine is deprected please use plot_reaccont instead.

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    chemistry : class:`prodimopy.read.Chemistry`
      data resulting from `prodimopy.read.analise_chemistry` on a single species

    rtype : str
      keyword which sets the type of reactions to be shown (destruction or formation)
      must be set to either 'd' (destruction) or 'f' (formation)

    level : int
      1 means most important, 2 second most important etc.

    plot_size : int
      plot size, it is set to square for now

    lograte : bool
      plot log rate instead of rate, default to True (the difference are more noticeable)

    grid : bool
      plot nx,ny instead of r, z, default to False

    with_abun : bool
      plot abundance instead of formation or destruction rate, overrides lograte,
      default to False

    vmin : float
      sets the minimum value for `plt.imshow` (abundance, rate or lograte)
      default min(array)

    '''
    print('PLOT: plot_reac ...')
    print("WARN: this routine is deprected please use plot_reaccont instead.")

    fig,ax=plt.subplots(figsize=(plot_size,plot_size))

    # label='main '
    # label+=r"$\mathrm{"+spnToLatex(chemistry.species)+"}$"
    splabel=r"$\mathrm{"+spnToLatex(chemistry.species)+"}$"

    if rtype=='f':
      # data=chemistry.farray.T
      data=chemistry.totfrate.T  # transpose because of imshow
      reacs=chemistry.get_reac_grid(level,"f")[0]
      label=r"(total formation rate) $[cm^{-3} s^{-1}]$"
      # label+=' formation rate '
      # ax.set_title('Main formation reaction: '+chemistry.sorted_form_info[0][23:].replace(" ",""))
      ax.set_title(splabel+" main formation reactions")
    elif rtype=='d':
      # data=chemistry.darray.T
      data=chemistry.totdrate.T  # transpose because of imshow
      reacs=chemistry.get_reac_grid(level,"d")[0]
      label=r"(total destruction rate) $[cm^{-3} s^{-1}]$"
      ax.set_title(splabel+" main destruction reactions")
      # label+=' destruction rate '
      # ax.set_title('Main destruction reaction: '+chemistry.sorted_dest_info[0][23:].replace(" ",""))
    else:
      print('ERROR: Unknown rtype.')
      return

    if with_abun:
      label=r"$\mathrm{\epsilon("+spnToLatex(chemistry.species)+")}$"
      label="log "+label
      data=np.log10(model.getAbun(chemistry.species).T)
      lograte=False

    if lograte:
      label="log "+label
      data=np.log10(data)
      # label+='* [s] '
#    else:
#      if not(with_abun):
#        label=r'[$\mathrm{s}^{-1}$]'

    for i in range(model.nx):
      for j in range(model.nz)[::-1]:
        ax.text(i+1-1.2,j+1-1.2,reacs[i,j])

    # FIXME: imshow is maybe not the best optoin here because of the grid
    # of ProDiMo ... however it works if grid=True but otherwise the z coordinate
    # is not shown correctly
    if vmin is None:
      vmin=np.min(data)

    im=ax.imshow(data,vmin=vmin)
    CB=fig.colorbar(im,ax=ax,fraction=0.047,pad=0.01)
    CB.set_label(label)

    if grid:
      ax.set_xlim(-0.5,model.nx-0.5)
      ax.set_ylim(-0.5,model.nz-0.5)
      ax.set_xlabel('ix')
      ax.set_ylabel('iz')

    else:
      ax.set_ylim(-0.5,model.nz-0.5)

      xticks=ax.get_xticks()[1:]
      xticks[-1]=model.nx-1
      ax.set_xticks(xticks)

      xticks_l=list(model.x[:,0][xticks.astype(int)])
      xticks_l=[np.around(item,4) for item in xticks_l]
      ax.set_xticklabels(xticks_l)

      yticks=ax.get_yticks()[1:]
      yticks[-1]=model.nz-1
      ax.set_yticks(yticks)

      # FIXME: this is not correct,
      yticks_l=list(model.z[0,:][yticks.astype(int)])
      yticks_l=[np.around(item,3) for item in yticks_l]
      ax.set_yticklabels(yticks_l)

      ax.set_xlabel('r [au]')
      ax.set_ylabel('z [au]')

    self._dokwargs(ax,**kwargs)
    # self._legend(ax)

    return self._closefig(fig)

  def plot_abunvert(self,model,r,species,useZr=False,useNH=True,useT=False,
                    scaling_fac=None,norm=None,styles=None,
                    colors=None,markers=None,linewidths=None,
                    ax=None,**kwargs):
    '''
    Plots the abundances of all the given species as a function of height at
    the given radius.

    If `useZr`, `useNH` and `useT` are all `False` the abundances are plotted
    as function of z in au. By default `useNH=True`.


    FIXME: Make the inferface consistent with plot_vert. Especially
    the treatment of the xaxis (i.e. what should be use to indicate the height)

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    r : float
      The radius at which the vertical cut is taken. UNIT: `au`

    species : array_like(str,ndim=1) :
      List of species names to plot.

    useZr : boolean
      plot the abundances as function of z/r: Default: `True`

    useNH : boolean
      plot the abundances as function of vertical column densities
      Default: `False`

    useT : boolean
      plot the abundances as function of dust temperature.


    '''

    print("PLOT: plot_abunvert ...")

    if colors is None:
      colors=list(self.pcolors.values())

    rstr=r"r$\approx${:.2f} au".format(r)

    fig,ax=self._initfig(ax,**kwargs)

    ix=(np.abs(model.x[:,0]-r)).argmin()

    iplot=0
    ymin=1.e100
    ymax=-1.0
    if(type(species)==str): species=[species]
    for spec in species:
      if useNH:
        old_settings=np.seterr(divide='ignore')
        x=np.log10(model.NHver[ix,:])
        np.seterr(**old_settings)  # reset to defaul
        xlabelstr=r"$\mathrm{\log\,N_{<H>}\,[cm^{-2}]}$ @"+rstr
      elif useZr:
        x=model.z[ix,:]/model.x[ix,0]
        xlabelstr=r"z/r @"+rstr
      elif useT:
        x=model.td[ix,:]
        xlabelstr=r"$\mathrm{T_d [K]}$ @"+rstr
      else:
        x=model.z[ix,:]
        xlabelstr=r"z [au] @"+rstr

      # check if list of names in list of names, than sum them up
      if isinstance(spec,(list,tuple,np.ndarray)):
        y=model.nHtot[ix,:]*0.0  # just to get an array
        for name in spec:
          y=y+(model.getAbun(name)[ix,:])

      elif spec in model.spnames:
        y=model.nmol[ix,:,model.spnames[spec]]/model.nHtot[ix,:]
      else:
        continue

      if norm is not None:
        y=y/norm

      if scaling_fac is not None:
        y=y*scaling_fac[iplot]

      # FIXME: add proper treatment for styles and colors
      if styles==None:
        style="-"
        if "#" in spec: style="--"
      else:
        style=styles[iplot]

      color=colors[iplot]

      marker=None
      if markers!=None:
        marker=markers[iplot]

      lines=ax.plot(x,y,marker=marker,ms=4,markeredgecolor=color,markerfacecolor=color,
              linestyle=style,color=color,
              label="$\mathrm{"+spnToLatex(spec)+"}$")

      if linewidths!=None:
        if linewidths[iplot]!=None:
          lines[-1].set_linewidth(linewidths[iplot])

      iplot=iplot+1
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    if useT:
      ax.set_xlim([30,5])
    elif useNH:
      ax.set_xlim([17.5,x.max()])
    else:
      ax.invert_xaxis()  # (z/r=0 on the right)
    ax.set_ylim(ymin,ymax)
    ax.semilogy()

#     ax2 = ax.twiny()
#     ax2.set_xlabel("z/r")
#     ax2.set_xlim(ax.get_xlim())
#     #ax2.set_xticks(ax.get_xticks())
#     ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

    ax.set_xlabel(xlabelstr)
    ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)
    return self._closefig(fig)

  def plot_abunrad(self,model,species,useNH=True,
                    norm=None,styles=None,colors=None,markers=None,linewidths=None,
                    ax=None,**kwargs):
    '''
    Plots species abundances as function of radius in the midplane (z=0)
    Similar to abunvert but radially is more usefull for e.g. envelope structures.

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    species : array_like(str,ndim=1) :
      List of species names to plot.

    useNH : boolean
      plot the abundances as function of radial column densities
      Default: `False`

    norm : float
      normalize the y values by the given number (i.e. y=y/norm)
      Default: `None` (i.e. no normalisation)

    '''

    print("PLOT: plot_abunrad ...")

    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    ymin=1.e100
    ymax=-1.0
    if(type(species)==str): species=[species]
    for spec in species:
      if useNH:
        old_settings=np.seterr(divide='ignore')
        x=np.log10(model.NHrad[:,0])
        np.seterr(**old_settings)  # reset to defaul
      else:
        x=model.x[:,0]

      if spec in model.spnames:
        y=model.nmol[:,0,model.spnames[spec]]/model.nHtot[:,0]
        if norm!=None:
          y=y/norm

        # FIXME: add proper treatment for styles and colors
        if styles==None:
          style="-"
          if "#" in spec: style="--"
        else:
          style=styles[iplot]

        color=None
        if colors!=None:
          color=colors[iplot]

        marker=None
        if markers!=None:
          marker=markers[iplot]

        lines=ax.plot(x,y,marker=marker,ms=4,markeredgecolor=color,markerfacecolor=color,
                linestyle=style,color=color,
                label="$\mathrm{"+spnToLatex(spec)+"}$")

        if linewidths!=None:
          if linewidths[iplot]!=None:
            lines[-1].set_linewidth(linewidths[iplot])

        iplot=iplot+1
        if min(y)<ymin: ymin=min(y)
        if max(y)>ymax: ymax=max(y)

    if useNH:
      ax.set_xlim([17.5,x.max()])
    ax.set_ylim(ymin,ymax)
    ax.semilogy()

#     ax2 = ax.twiny()
#     ax2.set_xlabel("z/r")
#     ax2.set_xlim(ax.get_xlim())
#     #ax2.set_xticks(ax.get_xticks())
#     ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

    if useNH:
      ax.set_xlabel(r"$\mathrm{\log\,N_{<H,rad>}\,[cm^{-2}]}$")
    else:
      ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax)
    return self._closefig(fig)

  def plot_abun_midp(self,model,species,norm=None,styles=None,colors=None,ax=None,**kwargs):
    '''
    Plots the abundances in the midplane for the given species (can be more than one)

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the model data

    species : array_like(str,ndim=1) :
      List of species names to plot.

    norm : float
      normalize the y values by the given number (i.e. y=y/norm)
      Default: `None` (i.e. no normalisation)

    '''

    print("PLOT: plot_abun_midp ...")
    fig,ax=self._initfig(ax,**kwargs)

    iplot=0
    xmin=1.e100
    xmax=0
    ymin=1.e100
    ymax=-1.e00
    if(type(species)==str): species=[species]
    for spec in species:
      if spec not in model.spnames:
        print("WARN: Species "+spec+" not found")
        continue

      x=model.x[:,0]
      y=model.nmol[:,0,model.spnames[spec]]/model.nHtot[:,0]
      if norm is not None:
        y=y/norm

      # FIXME: add proper treatment for styles and colors

      if styles==None:
        style="-"
        if "#" in spec: style="--"
      else:
        style=styles[iplot]

      if colors==None:
        color=None
      else:
        color=colors[iplot]

      ax.plot(x,y,marker=None,linestyle=style,color=color,label="$\mathrm{"+spnToLatex(spec)+"}$")

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)
      if min(y)<ymin: ymin=min(y)
      if max(y)>ymax: ymax=max(y)

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.semilogy()
    ax.set_xlabel("r [au]")
    ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax)

    return self._closefig(fig)

  def plot_dust_opac(self,model,dust=None,ax=None,pseudoaniso=False,**kwargs):
    '''
    Plots the dust opacities (dust_opac.out) or the data given in the
    dust object

    Parameters
    ----------

    pseudoaniso : boolean
      Use the pseudoe anisotropic scattering opacity.

    '''
    print("PLOT: dust opacities ...")

    fig,ax=self._initfig(ax,**kwargs)

    x=model.dust.lam

    if dust is None: dust=model.dust

    ax.plot(x,dust.kabs,label="absorption")
    if pseudoaniso:
      ax.plot(x,dust.ksca_an,label="scattering")
      ax.plot(x,dust.kabs+dust.ksca_an,label="extinction")
    else:
      ax.plot(x,dust.ksca,label="scattering")
      ax.plot(x,dust.kext,label="extinction")
    ax.set_xlabel(r"wavelength $\mathrm{[\mu m]}$")
    ax.set_ylabel(r"opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")

    ax.set_xlim(np.min(x),np.max(x))
    # ax.set_ylim(1.e-2,None)

    ax.semilogx()
    ax.semilogy()

    self._dokwargs(ax,**kwargs)
    self._legend(ax)
    return self._closefig(fig)

  def plot_vertical(self,model,r,values,ylabel,zr=True,
                    xfield="zr",marker=None,ax=None,**kwargs):
    '''
    Plots a quantity (values) as a function of height at a certain radius
    radius.

    values : array_like(float,ndim=2)
      a 2D array with numeric values for the plotting. E.g. any 2D array
      of the :class:`~prodimopy.read.Data_ProDiMo` object.

    xfield : str
      What field should be used a x-axis. Options are
      `zr`,`nH`,`tg`,`AVver` .


    FIXME: Make the inferface consistent with plot_abunvert. Especially
    the treatment of the xaxis (i.e. what should be use to indicate the height)

    '''
    print("PLOT: plot_vertical ...")
    rstr=r"r$\approx${:.1f} au".format(r)

    fig,ax=self._initfig(ax,**kwargs)

    ix=(np.abs(model.x[:,0]-r)).argmin()

    if zr and xfield=="zr":
      x=model.z[ix,:]/model.x[ix,0]
    elif xfield=="nH":
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
      x=np.range(model.nz)
      print(x)
    else:
      x=model.z[ix,:]

    y=values[ix,:]

    ax.plot(x,y,marker=marker,ms=4)

    if zr:
      ax.invert_xaxis()
      ax.set_xlabel(r"z/r @ "+rstr)
    elif xfield=="nH":
      ax.set_xlabel(r"$\mathrm{\log\,N_{<H>}\,[cm^{-2}]}$ @"+rstr)
    elif xfield=="AVver":
      ax.set_xlabel(r"$\mathrm{\log\,A_{V,ver}}$ @"+rstr)
    elif xfield=="tg":
      ax.set_xlabel(r"$\mathrm{\log\,T_{gas}\,[K]}$ @"+rstr)
      ax.invert_xaxis()
    else:
      ax.set_xlabel(r"z [au] @ "+rstr)
      ax.invert_xaxis()

    ax.set_ylabel(ylabel)

    self._dokwargs(ax,**kwargs)
    self._legend(ax)

    return self._closefig(fig)

  def plot_taus(self,model,r,ax=None,**kwargs):
    '''
    Plot's taus (A_V, X-rays) as a function of vertical column density
    '''
    ir=(np.abs(model.x[:,0]-r)).argmin()
    rstr="r={:.2f} au".format(model.x[ir,0])

    fig,ax=self._initfig(ax,**kwargs)

    old_settings=np.seterr(divide='ignore')

    x=np.log10(model.NHver[ir,:])

    ax.plot(x,model.tauX1[ir,:],color="blue",label=r"$\mathrm{\tau_{1\;keV}}$")
    ax.plot(x,model.tauX10[ir,:],"--",color="blue",label=r"$\mathrm{\tau_{10\;keV}}$")
    ax.plot(x,model.AVrad[ir,:],color="red",label=r"$\mathrm{A_V,rad}}$")
    ax.plot(x,model.AVver[ir,:],"--",color="red",label=r"$\mathrm{A_{V,ver}}$")

    ax.set_xlim(17.5,x.max())
    ax.set_ylim(1.e-2,np.max([model.AVver[ir,:].max(),2.0]))

    np.seterr(**old_settings)  # reset to default

    ax.hlines(1.0,ax.get_xlim()[0],ax.get_xlim()[1],linestyle=":")

    ax2=ax.twiny()
    ax2.set_xlabel("z/r")
    ax2.set_xlim(ax.get_xlim())
    # ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ir,ax.get_xticks(),model)])

    ax.set_xlabel(r"$\log$ N$_\mathrm{H}$ [cm$^{-2}$]")
    ax.set_ylabel(r"$\mathrm{A_V, \tau}$")

    # do axis style
    ax.semilogy()

    self._dokwargs(ax,**kwargs)

    handles,labels=ax.get_legend_handles_labels()
    ax.legend(handles,labels,loc="best",fancybox=False)
    ax.text(0.025,0.025,rstr,
       verticalalignment='bottom',horizontalalignment='left',
       transform=ax.transAxes,alpha=0.75)

    return self._closefig(fig)

  def plot_starspec(self,model,ax=None,step=10,xunit="micron",**kwargs):
    '''
    Plots the full Stellar Spectrum

    Parameters
    ----------

    step : int
      only every `step` point is plotted from teh Spectrum (makes is less dens)

    xunit : str
      the unit for the x-axes. Current options are `micron` or `eV`.

    '''
    print("PLOT: plot_starspec ...")
    fig,ax=self._initfig(ax,**kwargs)

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

    y=(model.starSpec.nu*model.starSpec.Inu)[0::step]

    ymin=np.min(y[x>1])

    ax.plot(x,y,color="black")

    # set defaults, can be overwritten by the kwargs

    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,None])
    ax.semilogx()
    ax.semilogy()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def plot_sed(self,model,plot_starSpec=True,sedObs=None,unit="erg",reddening=False,
               ax=None,**kwargs):
    '''
    Plots the seds and the StarSpectrum
    '''
    print("PLOT: plot_sed ...")
    fig,ax=self._initfig(ax,**kwargs)

    xmin=0.1
    if model.sed==None: return
    # only use every 5 element to speed up plotting
    x=model.sed.lam
    if unit=="W":
      y=model.sed.nuFnuW
    elif unit=="Jy":
      y=model.sed.fnuJy
    else:
      y=model.sed.nu*model.sed.fnuErg

    ymin=np.min(y[model.sed.lam>1])

    if reddening==True and sedObs is not None and sedObs.A_V is not None:
      # idx validity of extinction function
      ist=np.argmin(np.abs(x-0.0912))
      ien=np.argmin(np.abs(x-6.0))
      y[ist:ien]=y[ist:ien]/prodimopy.extinction.reddening(x[ist:ien]*1.e4,a_v=sedObs.A_V,r_v=sedObs.R_V,model="f99")

    dist=((model.sed.distance*u.pc).to(u.cm)).value

    if plot_starSpec:
      # scale input Stellar Spectrum to the distance for comparison to the SED
      r=((model.starSpec.r*u.R_sun).to(u.cm)).value

      xStar=model.starSpec.lam[0::1]
      yStar=(model.starSpec.nu*model.starSpec.Inu)[0::1]
      yStar=yStar*(r**2.0*math.pi*dist**(-2.0))

      if unit=="W":
        yStar=(yStar*u.erg/(u.s*u.cm**2)).to(u.Watt/u.m**2).value
      elif unit=="Jy":
        yStar=(model.starSpec.Inu)[0::1]
        yStar=yStar*(r**2.0*math.pi*dist**(-2.0))
        yStar=(yStar*u.erg/(u.s*u.cm**2*u.Hz)).to(u.Jy).value

      ax.plot(xStar,yStar,color="black")

    # plot the SED
    ax.plot(x,y,marker=None,label=model.name)

    if sedObs is not None:
      okidx=np.where(sedObs.flag=="ok")

      xsedObs=sedObs.lam
      ysedObs=sedObs.nu*sedObs.fnuErg
      ysedObsErr=sedObs.nu*sedObs.fnuErgErr

      if unit=="W":
        ysedObs=sedObs.nu*((sedObs.fnuJy*u.Jy).si.value)
        ysedObsErr=sedObs.nu*((sedObs.fnuJyErr*u.Jy).si.value)
      elif unit=="Jy":
        ysedObs=sedObs.fnuJy
        ysedObsErr=sedObs.fnuJyErr

      # ax.plot(sedObs.lam[okidx],sedObs.nu[okidx]*sedObs.fnuErg[okidx],linestyle="",marker="x",color="0.5",ms=3)
      ax.errorbar(xsedObs[okidx],ysedObs[okidx],yerr=ysedObsErr[okidx],
                  fmt='o',color="0.5",ms=2,linewidth=1.0,zorder=0)

      ulidx=np.where(sedObs.flag=="ul")
      ax.plot(xsedObs[ulidx],ysedObs[ulidx],linestyle="",marker="v",color="0.5",ms=2.0)

      # FIXME: no proper unit treatment yet
      if sedObs.specs is not None:
        for spec in sedObs.specs:
          nu=(spec[:,0]*u.micrometer).to(u.Hz,equivalencies=u.spectral()).value
          fnuerg=(spec[:,1]*u.Jy).cgs.value
          ax.plot(spec[:,0],nu*fnuerg,linestyle="-",linewidth=0.5,color="0.5")

    # set defaults, can be overwritten by the kwargs
    ax.set_xlim([xmin,None])
    ax.set_ylim([ymin,None])
    ax.semilogx()
    ax.semilogy()
    ax.set_xlabel(r"wavelength [$\mathrm{\mu}$m]")
    if unit=="W":
      ax.set_ylabel(r"$\mathrm{\lambda F_{\lambda}\,[W\,m^{-2}]}$")
    elif unit=="Jy":
      ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")
    else:
      ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")
#    ax.yaxis.tick_right()
#    ax.yaxis.set_label_position("right")

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def _getSEDana_boxpoints(self,lam,model,zr=True):
    '''
    Creates an array of (x,y) coordinates representing the emission origin for
    the SEDana which can be used or the given wavelength. Those coordinates can
    be used to draw a box on a plot (e.g. can be passed to a matplotlib Polygon)
    to draw a box (Polygon).

    Parameters
    ----------
    lam : float
      the wavelength for which the emission origin should be calculated

    model : :class:`prodimopy.read.Data_ProDiMo`
      the ProDiMo model including the SED analysis data (SEDana)

    zr : boolean
      If `zr==True` (default) then the z coordinate of the points is returned in
      z/r units. Optional parameter.

    Returns
    -------
    array_like(float,ndim=1) :
      list of (x,y) points (in au). if zr=True the z coordinate is in z/r units.


    TODO: maybe merge somehow with :func:`~prodimopy.Data_ProDiMo.getSEDAnaMask`
    '''
    # interpolate
    sedAna=model.sed.sedAna

    r15=interp1d(sedAna.lams,sedAna.r15,bounds_error=False,fill_value=0.0,kind="linear")(lam)
    r85=interp1d(sedAna.lams,sedAna.r85,bounds_error=False,fill_value=0.0,kind="linear")(lam)
    xi15=np.argmin(np.abs(model.x[:,0]-r15))
    xi85=np.argmin(np.abs(model.x[:,0]-r85))

    z85s=[[model.x[ix,0],interp1d(sedAna.lams,sedAna.z85[:,ix],bounds_error=False,fill_value=0.0,kind="linear")(lam)]
           for ix in range(xi15,xi85)]
    z15s=[[model.x[ix,0],interp1d(sedAna.lams,sedAna.z15[:,ix],bounds_error=False,fill_value=0.0,kind="linear")(lam)]
          for ix in range(xi85-1,xi15-1,-1)]
    points=z85s+z15s

    for point in points:
      if zr is True:
        point[1]=point[1]/point[0]

    return points

  def plot_sedAna(self,model,lams=[1.0,3.0,6.0,10.0,30.0,60.0,100.0,200.0,1000.0],field=None,label=None,boxcolors=None,zlog=True,
                zlim=[None,None],zr=True,clevels=None,clabels=None,
                extend="neither",oconts=None,nbins=70,
                bgcolor=None,cb_format="%.1f",scalexy=[1,1],patches=None,
                rasterized=False,ax=None,**kwargs):
    '''
    Plots the SED analysis stuff (origin of the emission).

    Parameters
    ----------
    model : :class:`prodimopy.read.Data_ProDiMo`
      the ProDiMo model.

    lams : array_like(float,ndim=1)
      list of wavelengths in micrometer.

    field : array_like(float,ndim=2)
      And array with dimension (nx,nz) with values that should be plotted as filled contours.
      `DEFAULT:` the `nHtot` field of :class:`prodimopy.read.Data_ProDiMo`.


    '''
    print("PLOT: plot_sedAna ...")

    if boxcolors is None:
      boxcolors=list(self.pcolors.values())

    if patches is None:
      patches=list()

    ibox=0
    for lam in lams:
      points=self._getSEDana_boxpoints(lam,model,zr=True)
      if len(points)>0:
        patch=mpl.patches.Polygon(points,True,fill=False,color=boxcolors[ibox],zorder=100,linewidth=2.0)
        patches.append(patch)
      else:
        print("WARN: Could not create box for lam=",str(lam))
      ibox+=1

    if field is None:
      field=model.nHtot
      label=r"log $n_\mathrm{<H>}\,\mathrm{[cm^{-3}]}$"
      oconts=[Contour(model.AV,[1],linestyles="--",colors=self.pcolors["gray"])]

    fig=self.plot_cont(model,field,label=label,zlog=zlog,
                zlim=zlim,zr=zr,clevels=clevels,clabels=clabels,contour=False,
                extend=extend,oconts=oconts,nbins=nbins,
                bgcolor=bgcolor,cb_format=cb_format,scalexy=scalexy,patches=patches,
                rasterized=rasterized,returnFig=True,ax=ax,**kwargs)

    ax=fig.axes[0]

    ibox=0
    for lam in lams:
      ax.text(0.02,0.92-ibox/18.0,"$"+"{:5.1f}".format(lam)+r"\,\mathrm{\mu m}$",
              horizontalalignment='left',
              verticalalignment='bottom',fontsize=6,
              transform=ax.transAxes,color=boxcolors[ibox],
              bbox=dict(boxstyle='square,pad=0.1',fc='white',ec='none'))
      ibox+=1

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def plot_taulines(self,model,lineIdents,showCont=True,ax=None,**kwargs):
    '''
    Plots the line optical depth as a function of radius for the given lines.
    The lines are identified via a list of lineIdents containt of an array with
    ident and wavelength of the line e.g. ["CO",1300.0].
    It searches for the closest lines.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    lineIdents : array_like()
      list of line identifactors of the form `[["ident",wl],["ident2",wl2]]`.

    TODO: there are no options for linestyles and colors yet (the defaults are used).
    '''
    print("PLOT: plot_taulines ...")
    fig,ax=self._initfig(ax,**kwargs)

    # if it is only one line (no list of list) make it a list
    if (type(lineIdents[0])==str): lineIdents=[lineIdents]

    xmin=1.e100
    xmax=0

    iplot=0
    for lineIdent in lineIdents:
      x=model.x[:,0]
      lineEstimate=model.getLineEstimate(lineIdent[0],lineIdent[1])
      y=[dum.tauLine for dum in lineEstimate.rInfo]

      ax.axhline(y=1.0,linestyle="-",color="black",linewidth=0.5)
      label=r"$\mathrm{"+spnToLatex(lineEstimate.ident)+"}$ "+"{:.2f}".format(lineEstimate.wl)+" $\mathrm{\mu m}$"

      line,=ax.plot(x,[dum.tauLine for dum in lineEstimate.rInfo],marker=None,label=label)

      if showCont:
        ax.plot(x,[dum.tauDust for dum in lineEstimate.rInfo],
                marker=None,linestyle="--",color=line.get_color())

      iplot=iplot+1

      if min(x)<xmin: xmin=min(x)
      if max(x)>xmax: xmax=max(x)

    ax.set_xlim(xmin,xmax)

    ax.semilogx()
    ax.semilogy()

    ax.set_xlabel(r"r [au]")
    ax.set_ylabel(r"$\mathrm{\tau_{line}}$")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_line_origin(self,model,lineIdents,field,label="value",boxcolors=None,showBox=True,showRadialLines=True,boxlinewidths=1.5,
                       boxlinestyles=None,boxhatches=None,lineLabels=None,showLineLabels=True,lineLabelsFontsize=6.0,lineLabelsAlign="left",zlog=True,
                zlim=[None,None],zr=True,clevels=None,clabels=None,contour=False,
                extend="neither",oconts=None,nbins=70,
                bgcolor=None,cb_format="%.1f",scalexy=[1,1],patches=None,
                rasterized=False,showContOrigin=False,ax=None,**kwargs):
    '''
    Plots the line origins for a list of lineestimates given by their lineIdents
    (["ident",wavelength]).

    Does not give the exact same results as the corresponding idl routines
    as we do not use interpolation here. We rather use the same method for
    calculating the averaged values over the emission area and for plotting
    this area.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    lineIdents : array_like()
      list of line identifactor of the form `[["ident",wl],["ident2",wl2]]`.

    field : array_like(float,ndim=2)
      a 2D array with numeric values for the plotting. E.g. any 2D array
      of the :class:`~prodimopy.read.Data_ProDiMo` object.

    boxlinewidths : array_like
      the widths of the line for each box showing the line origin. Can be a
      scalar, in that case all boxes have the same linewidth

    '''
    if boxcolors is None:
      boxcolors=[self.pcolors["red"],self.pcolors["orange"],self.pcolors["brown"],
                 self.pcolors["purple"],self.pcolors["gray"]]

    if boxlinestyles is None:
      boxlinestyles=["-"]*10
    elif np.isscalar(boxlinestyles):
      boxlinestyles=[boxlinestyles]*10

    if np.isscalar(boxlinewidths):
      boxlinewidths=[boxlinewidths]*10

    # if it is only one line (no list of list) make it a list
    if (type(lineIdents[0])==str): lineIdents=[lineIdents]

    lestimates=list()
    for id in lineIdents:
      lestimates.append(model.getLineEstimate(id[0],id[1]))

    if patches is None:
      patches=list()

    if len(boxcolors)<len(lestimates) or len(boxlinestyles)<len(lestimates):
      print("Not enough boxcolors or boxlinestyles available! ")
      return

    ibox=0
    for lesti in lestimates:
      # to be consistent we use the LineOriginMask to determine the box
      # as a result the plotted region is not necessarely the same as in idl
      # as we do not interpolate here
      xmasked=np.ma.masked_array(model.x,mask=model.getLineOriginMask(lesti))
      x15=np.min(xmasked)
      x85=np.max(xmasked)
      xi15=np.argmin(np.abs(model.x[:,0]-x15))
      xi85=np.argmin(np.abs(model.x[:,0]-x85))

      z85s=[[model.x[rp.ix,0],rp.z85] for rp in lesti.rInfo[xi15:xi85+1]]
      z15s=[[model.x[rp.ix,0],rp.z15] for rp in lesti.rInfo[xi85:xi15-1:-1]]
      points=z85s+z15s

      if zr is True:
        for point in points:
          point[1]=point[1]/point[0]

      if showBox:
        if len(points)>1:
          patch=mpl.patches.Polygon(points,True,fill=False,color=boxcolors[ibox],
                                      linestyle=boxlinestyles[ibox],
                                      zorder=100,linewidth=boxlinewidths[ibox])

          patches.append(patch)
        else:
          print("WARN: Unable to calculate a proper region for the line origin: "+str(lesti))

      if showContOrigin is True:
        if (model.sed is not None and model.sed.sedAna is not None):
          pointsc=self._getSEDana_boxpoints(lesti.wl,model,zr)
          if len(pointsc)>1:
            patchc=mpl.patches.Polygon(pointsc,True,fill=False,
                                         color=boxcolors[ibox],zorder=100,
                                         linewidth=1.0,linestyle="--")
            patches.append(patchc)
          else:
            print("WARN: Unable to calculate a proper region for the continuum origin: "+str(lesti))

      ibox+=1

    fig=self.plot_cont(model,field,label=label,zlog=zlog,
                zlim=zlim,zr=zr,clevels=clevels,clabels=clabels,contour=False,
                extend=extend,oconts=oconts,acont=None,acontl=None,nbins=nbins,
                bgcolor=bgcolor,cb_format=cb_format,scalexy=scalexy,patches=patches,
                rasterized=rasterized,returnFig=True,ax=ax,**kwargs)

    if ax is None:
      ax=fig.axes[0]

    # show the full emitting layer as function of radius
    if showRadialLines:
      iest=0
      r=model.x[:,0]
      for lesti in lestimates:
        z15=[rinf.z15 for rinf in lesti.rInfo]
        z85=[rinf.z85 for rinf in lesti.rInfo]
        if zr is True:
          z15=z15/r
          z85=z85/r

        if showBox is False:
          lsrad=boxlinestyles[iest]
        else:
          lsrad=":"

        ax.plot(r,z15,color=boxcolors[iest],linestyle=lsrad,linewidth=1.0)
        ax.plot(r,z85,color=boxcolors[iest],linestyle=lsrad,linewidth=1.0)
        if boxhatches is not None:
          ax.fill_between(r,z15,z85,edgecolor=boxcolors[iest],hatch=boxhatches[iest],facecolor="none",linewidth=0.0)

        iest+=1

    if showLineLabels:
      ibox=0
      for idline in lineIdents:
        if lineLabels is not None:
          label=lineLabels[ibox]
        else:
          label="$"+spnToLatex(idline[0])+"$ "+str(idline[1])

        # FIXME: quick and dirty, ref fontsize =6.0
        vpos=ibox/(18.0-(lineLabelsFontsize/6.0-1.0)*12.0)
        if lineLabelsAlign=="right":
          ax.text(0.95,0.92-vpos,label,
                horizontalalignment='right',
                verticalalignment='bottom',fontsize=lineLabelsFontsize,
                transform=ax.transAxes,color=boxcolors[ibox],
                bbox=dict(boxstyle='square,pad=0.1',fc='white',ec='none'))
        else:
          ax.text(0.02,0.92-vpos,label,
                horizontalalignment='left',
                verticalalignment='bottom',fontsize=lineLabelsFontsize,
                transform=ax.transAxes,color=boxcolors[ibox],
                bbox=dict(boxstyle='square,pad=0.1',fc='white',ec='none'))
        ibox+=1

    return self._closefig(fig)

  def plot_lineprofile(self,model=None,wl=None,ident=None,lineObj=None,linetxt=None,lineObs=None,
                       unit="Jy",normalized=False,convolved=False,style=None,ax=None,**kwargs):
    '''
    Plots the line profile for the given line (id wavelength and optionally the line ident)

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data. Only required if wl,ident and or lineObs are passed.

    wl : float
      The wavelength of the line in micrometer. Plotted is the line with the wavelength
      closest to `wl`.

    ident : str
      The optional line ident which is additionally use to identify the line.

    lineObj : :class:`prodimopy.read.DataLine`
      Pass `DataLine` object. In that case wl and ident are ignored.

    linetxt : str
      A string the is used as the label for the line

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
    print("PLOT: plot_line_profile ...")
    fig,ax=self._initfig(ax,**kwargs)

    if lineObj is None:
      line=model.getLine(wl,ident=ident)
      if line==None:
        print("WARN: line "+str(ident)+" at "+str(line.wl)+" micron not found")
    else:
      line=lineObj

    # text for the title

    # FIXME: ist not up to date anymore with the unit treatment in lineprofile
    x=line.profile.velo

    if convolved:
      y=line.profile.flux_conv-line.profile.flux_conv[0]
    else:
      y=line.profile.flux-line.profile.flux[0]

    if normalized:
      y=y/np.max(y)

    if linetxt is None:
      if ident is not None:
        linetxt=ident
      else:
        linetxt=line.species
      linetxt=linetxt+"@"+"{:.2f}".format(line.wl)+" $\mathrm{\mu m}$"

    if style=="step":
      ax.sep(x,y,marker=None,label=linetxt,where="mid")
    else:
      ax.plot(x,y,marker=None,label=linetxt)

    # plot the line profile if it exists
    if lineObs is not None:
      # FIXME: this is not very nice
      # make a warning if lineObs and line Data are not consistent
      # it could be that they are for one model
      lineIdx=model._getLineIdx(wl,ident=ident)

      line=lineObs[lineIdx]
      if line.profile is not None:
        x=line.profile.velo
        y=line.profile.flux  # remove the continuum

        if normalized:
          y=y/np.max(y)

        if line.profileErr is not None:
          ax.fill_between(x,y-line.profileErr ,y+line.profileErr,color='0.8',zorder=0)
        ax.plot(x,y,marker=None,color="black",label="Obs.",zorder=0)

    if normalized:
      ax.set_ylabel("normalized flux")
    else:
      if line.profile.flux_unit=="ErgAng":
        ax.set_ylabel(r"$\mathrm{flux\,[erg s^{-1}cm^{-2}\AA^{-1}]}$")
      else:
        ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")

    ax.set_xlabel("velocity [km/s]")

    self._dokwargs(ax,**kwargs)
    self._legend(ax,**kwargs)

    return self._closefig(fig)

  def plot_lines(self,model,lineIdents,useLineEstimate=True,jansky=False,
                 showBoxes=True,lineObs=None,lineObsLabel="Obs.",peakFlux=False,
                 showCont=False,xLabelGHz=False,showGrid=True,**kwargs):
    """
    Plots a selection of lines or lineEstimates.

    See :func:`~prodimopy.plot.PlotModels.plot_lines` for more details.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    lineIdents : array_like
      a list of line identifiers. Each entry should contain `["ident",wl]`
      (e.g. `["CO",1300],["CO",800]]`. Those values are passed to
      :func:`~prodimopy.Data_ProDiMo.getLineEstimate`. The order of the lineIdents also
      defines the plotting order of the lines (from left to right)


    """
    print("PLOT: plot_lines ...")

    # need the instance
    ppm=prodimopy.plot_models.PlotModels(None,markers=["x"])
    fig=ppm.plot_lines([model],lineIdents,useLineEstimate=useLineEstimate,jansky=jansky,
                 showBoxes=showBoxes,lineObs=lineObs,lineObsLabel=lineObsLabel,peakFlux=peakFlux,
                 showCont=showCont,xLabelGHz=xLabelGHz,showGrid=showGrid,**kwargs)

    return self._closefig(fig)

  def plot_heat_cool(self,model,zr=True,oconts=None,**kwargs):
    """
    Plots the dominant heating and cooling processes.

    The initial python code for this routine is from Frank Backs

    TODO: possibility to have different oconts for the heating and cooling figures
    TODO: possibility to map certain heating/cooling processes always to the same color
    """
    print("PLOT: plot_heat_cool ...")

    colors=np.array([(230,25,75),(60,180,75),(255,225,25),(0,130,200),
                        (245,130,48),(145,30,180),(70,240,240),(240,50,230),
                        (210,245,60),(250,190,190),(0,128,128),(230,190,255),
                        (170,110,40),(255,250,200),(128,0,0),(170,255,95),
                        (128,128,0),(255,215,180),(0,0,128),(128,128,128),
                        (0,0,0),(220,220,220)],dtype=float)
    colors/=255

    if zr:
      z=model.z/model.x
    else:
      z=model.z

    # used for plotting
    max_idx=np.zeros(shape=(model.nx,model.nz),dtype='int16')

    # list of all the dominant heating processes
    idxlisth,idxlisth_counts=np.unique(model.heat_mainidx,return_counts=True)
    idxlistc,idxlistc_counts=np.unique(model.cool_mainidx,return_counts=True)

    # sort it descending
    idxlisth=idxlisth[np.argsort(idxlisth_counts)[::-1]]
    idxlistc=idxlistc[np.argsort(idxlistc_counts)[::-1]]

    # axis equal needs to be done here already ... at least it seems so
    sfigs=[2.0,1.3]
    if "sfigs" in kwargs: sfigs=kwargs["sfigs"]

    fig,axarr=plt.subplots(1,2,figsize=self._sfigs(sfigs=sfigs))
    plt.subplots_adjust(bottom=0.3)
    axh=axarr[0]
    axc=axarr[1]

    if len(idxlisth)>len(colors):
      print("WARN: too many heating processes, do not show the least important ones:")
      for i in range(len(colors),len(idxlisth)):
        print("   ",model.heat_names[idxlisth[i]-1])

    # this if for the labels, and also maps the colors to the names
    for i in range(min(len(idxlisth),len(colors))):
      # -1 because python starts at zero
      axh.scatter(0,0,marker="s",color=colors[i],label=model.heat_names[idxlisth[i]-1])

      # this is necessary to have the fields with increasing number without
      # gaps, otherwhise the colormapping in pcolormesh does not work
      max_idx[model.heat_mainidx==idxlisth[i]]=i

    cMap=mpl.colors.ListedColormap(colors[0:len(idxlisth)-1])
    axh.pcolormesh(model.x,z,max_idx,linewidth=0,cmap=cMap,rasterized=True)
    axh.legend(loc='upper center',bbox_to_anchor=(0.5,-0.175),ncol=2,
               frameon=False,fontsize=5.5)
    axh.set_title("dominant heating processes")

    # now for the cooling

    if len(idxlistc)>len(colors):
      print("WARN: too many cooling processes, do not show the least important ones:")
      for i in range(len(colors),len(idxlistc)):
        print("   ",model.cool_names[idxlistc[i]-1])

    # this if for the labels, and also maps the colors to the names
    for i in range(min(len(idxlistc),len(colors))):
      # -1 because python starts at zeror
      axc.scatter(0,0,marker="s",color=colors[i],label=model.cool_names[idxlistc[i]-1])

      # this is necessary to have the fields with increasing number without
      # gaps, otherwhise the colormapping in pcolormesh does not work
      max_idx[model.cool_mainidx==idxlistc[i]]=i

    cMap=mpl.colors.ListedColormap(colors[0:len(idxlistc)-1])
    axc.pcolormesh(model.x,z,max_idx,linewidth=0,cmap=cMap,rasterized=True)
    axc.legend(loc='upper center',bbox_to_anchor=(0.5,-0.175),ncol=2,
               frameon=False,fontsize=5.5)
    axc.set_title("dominant cooling processes")

    for ax in [axh,axc]:
      # axis equal needs to be done here already ... at least it seems so
      if "axequal" in kwargs:
        if kwargs["axequal"]: ax.axis('equal')

      ax.set_xlim(np.min(model.x),None)
      ax.semilogx()
      ax.set_xlabel("r [au]")
      if zr:
        ax.set_ylim(0,None)
        ax.set_ylabel("z/r")
      else:
        ax.set_ylabel("z [au]")

      # Additional Contours, plot for both plots at the moment
      if oconts is not None:
        for cont in oconts:
          ACS=ax.contour(model.x,z,cont.field,levels=cont.levels,
                         colors=cont.colors,linestyles=cont.linestyles,linewidths=cont.linewidths)
          if cont.showlabels:
            ax.clabel(ACS,inline=True,inline_spacing=cont.label_inline_spacing,
                      fmt=cont.label_fmt,manual=cont.label_locations,fontsize=cont.label_fontsize)

    # need to remove the title, as it does not fit here
    if self.title!=None:
      if self.title.strip()!="":
        fig.suptitle(self.title.strip())

    # remove title so that it does not show up onthe individual panels
    self._dokwargs(axh,notitle=True,**kwargs)
    self._dokwargs(axc,notitle=True,**kwargs)

    return self._closefig(fig)

  def plot_contImage(self,model,wl,zlim=[None,None],cmap="inferno",rlim=[None,None],cb_show=True,cb_fraction=0.15,
                     ax=None,**kwargs):
    """
    Simple plot for the continuum Images as produced by PRoDiMo.
    (The output in image.out).

    The scale is fixed to LogNorm at the moment.

    Parameters
    ----------
    model : :class:`~prodimopy.read.Data_ProDiMo`
      The model data.

    wl : float
      The wavelength in micron for which we should plot the image. The routine simple
      selected the closest one to the given image.

    zlim : array_like(ndim=1)
      the min and max value for the data to plot. Optional.

    rlim : array_like(ndim=1)
      the extension of the image eg. rlim[-1,1] plot the x and y coordinate from
      -1 to 1 au. Optional

    cmap : str
      The name of a matplotlib colormap. Optional.

    cb_show : boolean
      show colorbar or not. Optional.

    cb_fraction : float
      fractoin of the image use for the colorbar. Useful for subplots. Optional

    """
    contImages=model.contImages

    image,wl=np.copy(contImages.getImage(wl))

    # not very elegant, but need to extend the array otherwise the contourf routine is not "closing" the image
    x=np.hstack((contImages.x,contImages.x[:,0:1]))
    y=np.hstack((contImages.y,contImages.y[:,0:1]))
    imagepl=np.hstack((image,image[:,0:1]))

    vmin=zlim[0]
    vmax=zlim[1]

    # set some default values if required
    if vmax is None: vmax=np.max(imagepl)/2.0
    if vmin is None: vmin=vmax/1.e6

    fig,ax=self._initfig(ax,**kwargs)

    norm=mcolors.LogNorm(vmin=vmin,vmax=vmax)
    levels=np.logspace(np.log10(vmin),np.log10(vmax),100)

    CS=ax.contourf(x,y,imagepl,norm=norm,cmap=cmap,levels=levels,extend="both")

    # FIXME: that might not work for all colormaps
    ax.set_facecolor("black")
    ax.axis("equal")
    ax.set_xlim(rlim)
    ax.set_ylim(rlim)
    ax.set_aspect('equal','box')
    ax.set_xlabel("x [au]")
    ax.set_ylabel("y [au]")
    ax.set_title(r"$\lambda= {:6.2f}\, \mu m$".format(wl),pad=0)

    for spine in ax.spines.values():
      spine.set_color('white')
    ax.tick_params(color='white',which='both')

    if cb_show:
      axcb=np.array(fig.get_axes()).ravel().tolist()
      CB=fig.colorbar(CS,ax=axcb,pad=0.01,format="%3.1e",fraction=cb_fraction)
      CB.set_label(r"$I_\mathrm{\nu}\,[erg/cm^2/s/Hz/sr]$")

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)


class Contour(object):
  '''
  Define a Contour that can be used in the contour plotting routines.

  Objects of this class can be passed to e.g. the :func:`~prodimopy.plot.Plot.plot_cont` routine and will be drawn their.

  TODO: provide a field for label strings (arbitrary values) need to be the same size as levels
  '''

  def __init__(self,field,levels,colors="white",linestyles="solid",linewidths=1.5,
               showlabels=False,label_locations=None,label_fmt="%.1f",
               label_fontsize=7,
               label_inline_spacing=5,
               filled=False):
    '''
    Attributes
    ----------

    '''
    self.field=field
    """ array_like(float,ndim=2) :
      A 2D array of values used for the Contours. Needs to have the same
      dimensions as the array used for the contour plotting routine. So any
      2D array of the :class:`prodimopy.read.Data_ProDiMo` will do.
    """
    self.levels=levels
    """ array_like(float,ndim=1) :
      list of values for which contour lines should be drawn.
    """
    self.colors=colors
    """ array_like(ndim=1) :
      list of colors for the idividual contours. If only a single value is
      provided (i.e. no array) this value is applied to all contours.
      The values of colors can be given in the same way as it is done for
      matplotlib.
    """
    self.linestyles=linestyles
    """ array_like(ndim=1) :
      linestyles for the contours. Works like the `colors` parameter.
      Any style that matplotlib understands will work.
    """
    self.linewidths=linewidths
    """ array_like(ndim=1) :
      linewidths for the individual contour levels. Works the same as the
      `colors` parameter.
    """
    self.showlabels=showlabels
    """ boolean : `False`
      show text label for each level or not (default: False)
      Still kind of experimental
    """
    self.label_locations=label_locations
    self.label_fmt=label_fmt
    self.label_fontsize=label_fontsize
    self.label_inline_spacing=label_inline_spacing
    self.filled=filled


def spnToLatex(spname):
  """
  Utilitiy function to convert species names to proper latex math strings.

  The returned string can directly be embedded in a latex $ $ statement.
  """
  # use string in case it is a binary format (python 3 comaptibility)
  name=str(spname)
  # TODO: make this a bit smarter
  if str(spname)=="HN2+": name="N2H+"
  if str(spname)=="C18O": return "C^{18}O"
  if str(spname)=="13CO": return "^{13}CO"
  if str(spname)=="H13CO+": return "H^{13}CO^+"

  newname=""
  previous_char=None
  for c in name:
    if c.isdigit():
      # case for large melecues two digits ... not nice
      if previous_char is not None and previous_char.isdigit():
        newname=newname[0:-2]+"_{"+previous_char+c+"}"
      else:
        newname+="_"+c
    # deal with ortho and para (o-, p-) species
    elif c=="-" and not (previous_char=="o" or previous_char=="p" or previous_char=="-"):
      newname+="^-"
    elif c=="+" and not previous_char=="+":
      newname+="^+"
    elif c=="#":
      newname+="\#"
    else:
      newname+=c

    previous_char=c

  # for line names (species)
  if "_H" in newname:
    newname=newname.replace("_H","\_H")

  # repair the double ionized case
  if "^++" in newname: newname=newname.replace("^++","^{++}")
  # repair the triple ionized case
  if "^+++" in newname: newname=newname.replace("^+++","^{+++}")
  # repair the double ionized case
  if "^--" in newname: newname=newname.replace("^--","^{--}")
  # repair the triple ionized case
  if "^---" in newname: newname=newname.replace("^---","^{---}")

  return newname


def nhver_to_zr(ir,nhver,model,log=True):
  zrs=model.z[ir,:]/model.x[ir,:]

  if log==True:
    old_settings=np.seterr(divide='ignore')
    ipol=interp1d(np.log10(model.NHver[ir,:]),zrs,bounds_error=False,fill_value=0.0,kind="linear")
    np.seterr(**old_settings)  # reset to default
  else:
    ipol=interp1d(model.NHver[ir,:],zrs,bounds_error=False,fill_value=0.0,kind="linear")

  # return 0
  return ipol(nhver)


def plog(array):
  # ignore divide by zero in log10
  old_settings=np.seterr(divide='ignore')
  array=np.log10(array)
  np.seterr(**old_settings)  # reset to default
  return array


def scale_figs(scale):
  '''
  Scale the figure size from matplotlibrc by the factors given in the
  array scale the first element is for the width the second for
  the heigth.
  '''
  figsize=mpl.rcParams['figure.figsize']

  return (figsize[0]*scale[0],figsize[1]*scale[1])


def load_style(style="prodimopy"):
  '''
  Simple utility function to load a matplotlib style

  Parameters
  ----------

  style : str
    The name of the style that should be loaded. Default: prodimopy

  '''
  plt.style.use(style)

