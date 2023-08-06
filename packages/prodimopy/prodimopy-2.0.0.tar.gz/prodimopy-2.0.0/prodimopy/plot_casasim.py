"""
.. module:: plot_casasim

.. moduleauthor:: Ch. Rab

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from astropy import wcs
from matplotlib import patches
from matplotlib.offsetbox import AnchoredOffsetbox,AuxTransformBox
from matplotlib.ticker import MaxNLocator
import numpy

import astropy.units as u
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import prodimopy.plot as pplot


class PlotCasasim(object):
  '''
  Plot routines for casa simulation results.

  This class can be used together with :mod:`prodimoy.read_casasim`
  '''

  def __init__(self,pdf,labelspacing=1.0):
    """

    Parameters
    ----------
    pdf : class:`matplotlib.backends.backend_pdf.PdfPages`
      this object is used to save the plots in a pdf file.

    labelspacing : int
      the spacing for the x and y labels in images in arcseconds.
      i.e. 1 weans there will be an x(y) tick every 1 arcsec

    """
    self.pdf=pdf
    self.labelspacing=labelspacing

  def _dokwargs(self,ax,**kwargs):
    '''
    Handles the passed kwargs elements (assumes that defaults are already set)
    TODO: make this a general function ....
    TODO: does not work with subplots
    '''
#     if "ylim" in kwargs:
#       ax.set_ylim(kwargs["ylim"])
#
    if "xlim" in kwargs:
      ax.set_xlim(kwargs["xlim"])

    if "ylim" in kwargs:
      ax.set_ylim(kwargs["ylim"])

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
#
#     if "xlabel" in kwargs:
#       ax.set_xlabel(kwargs["xlabel"])
#
#     if "ylabel" in kwargs:
#       ax.set_ylabel(kwargs["ylabel"])
#
#     if self.title != None:
#       if self.title.strip() != "":
#         ax.set_title(self.title.strip())

    if "title" in kwargs:
      if  kwargs["title"]!=None and kwargs["title"].strip()!="":
        ax.set_title(kwargs["title"].strip())
      else:
        ax.set_title("")

  def _initfig(self,ax=None,subplot_kw=None,**kwargs):
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
      fig,ax=plt.subplots(1,1,subplot_kw=subplot_kw,figsize=self._sfigs(**kwargs))

    return fig,ax

  def _sfigs(self,**kwargs):
    '''
    Scale the figure size from matplotlibrc by the factors given in the
    array sfigs (in kwargs) the first element is for the width the second for
    the heigth
    '''
    if "sfigs" in kwargs:
      fac=kwargs["sfigs"]
      print(fac)
      return pplot.scale_figs(fac)
    else:
      return pplot.scale_figs([1.0,1.0])

  def _closefig(self,fig):
    '''
    Save and close the plot (Figure).

    If self.pdf is None than nothing is done and the figure is returned

    FIXME: this routine exists in also in plot.py and plot_models etc.
           make it general
    #set the transparent attribut (used rcParam savefig.transparent)
    '''

    # trans=mpl.rcParams['savefig.transparent']
    if self.pdf is not None:
      self.pdf.savefig(figure=fig,transparent=False)
      plt.close(fig)
      return None
    else:
      return fig

  def add_beam(self,ax,image,color="white"):
    """
    adds a beam to a plot (axis).

    Parameters
    ----------
    ax : class:`matplotlib.axes.Axes`
      the axis for which the beam should be added

    image : class:`~prodimopy.read_casasim.CASAImage`
      some kind of image (can also be a cube)

    FIXME: is proberly not general yet

    """
    bmin=image.bmin/image.header["CDELT1"]
    bmaj=image.bmaj/image.header["CDELT1"]
    bpa=image.bPA

    ae=AnchoredEllipse(ax.transData,width=bmin,height=bmaj,angle=bpa,
                           loc=3,pad=0.5,borderpad=0.4,frameon=False,color=color)
    ax.add_artist(ae)

  def plot_cube(self,cube,nrow=3,ncol=3,cvel_idx=None,step=1,
                zlim=[None,None],rms=False,mJy=False,zlog=False,powerNormGamma=None,
                cb_format="%5.1f",
                cb_fraction=0.015,
                cb_pad=0.005,
                cb_extend="neither",
                cmap="inferno",
                vellabel_fontsize=5,
                clevels=None,
                ccolors=None,
                zoomto=None,
                idxchans=None,
                framecolor="white",
                fig=None,axes=None,
                beam_color="white",
                **kwargs):
    """
    Plots a spectral line cube.

    Parameters
    ----------

    zoomto : float
      this parameters allows to zoom into the image. The unit is in arcsec.
      E.g. zoomto=1.0 will show the region around the the center ranging
      from -1.0 to 1.0 arcsec for the x and y axis.
      It is also possible to provide two values e.g. zoomto=[1.5,1] - region
      -1.5 to 1.0 arcsec for the x and -1.5 to 1.0 for the y axis.


    chans : array_like(int,ndim=1)
      list if indices for the channels (velocities) that should be shown.
      the correspoding images will be shown in the given order starting from
      top left - to bottom right.

    """

    if cube is None: return

    scalefac=1.0
    if mJy==True:
      scalefac=1000.0

    nimages=cube.data.shape[0]

    # wcvel=wcs.WCS(image[0].header)
    # print(wcs.find_all_wcs(image[0].header))

    if cvel_idx is None:
      cvel_idx=int(nimages/2)

    naxesh=int(nrow*ncol/2)

    vmin=zlim[0]
    vmax=zlim[1]
    if vmin is None: vmin=numpy.nanmin(cube.data)
    if vmax is None: vmax=numpy.nanmax(cube.data)
    vmin=vmin*scalefac
    vmax=vmax*scalefac

    norm=None
    if zlog:
      norm=mcolors.LogNorm(vmin=vmin,vmax=vmax)
    elif powerNormGamma is not None:
      norm=mcolors.PowerNorm(powerNormGamma,vmin=vmin,vmax=vmax)

    # cube.header['CRVAL1'] = 0.0
    # cube.header['CRVAL2'] = 0.0
    # wcsim=wcs.WCS(cube.header,naxis=(1,2))
    # cpix=[cube.header["CRPIX1"],cube.header["CRPIX2"]]
    # wcsrel=linear_offset_coords(wcsim, cube.centerpix)

    if fig is None or axes is None:
      fig,axes=plt.subplots(nrow,ncol,sharex=False,sharey=False,subplot_kw=dict(projection=cube.wcsrel))
      fig.subplots_adjust(hspace=-0.1,wspace=0.0)
      # fig,axis= plt.subplots(nrow, ncol,sharex=False,sharey=False)
      # fig=plt.figure()
      # assume the widht of the image is given, scale it with the number of axis
      figsize=fig.get_size_inches()
      figsize[0]=figsize[0]*2.0  # assumes that default size is one column in a Paper
      figsize[1]=figsize[0]/(ncol)*nrow
      fig.set_size_inches(figsize)
      returnFig=False
    else:
      returnFig=True

    for ir in range(nrow):
      for ic in range(ncol):

        # in that case the axis array is only 1D
        # only one plot
        if nrow==1 and ncol==1:
          ax=axes
        elif nrow==1:
          ax=axes[ic]
        else:
          ax=axes[ir,ic]
        iax=ir*ncol+ic

        if idxchans is not None:
          velidx=idxchans[iax]
        else:
          velidx=cvel_idx+(iax-naxesh)*step

        if norm is None:
          im=ax.imshow(cube.data[velidx,:,:]*scalefac,cmap=cmap,norm=norm,
                       vmin=vmin,vmax=vmax,origin="lower")
        else:
          im=ax.imshow(cube.data[velidx,:,:]*scalefac,cmap=cmap,norm=norm,origin="lower")

        if zoomto is not None:
          if type(zoomto) is list:
            pixels1=zoomto[0]/np.abs(cube.wcsrel.wcs.cdelt[0])
            pixels2=zoomto[1]/np.abs(cube.wcsrel.wcs.cdelt[0])
            ax.set_xlim(cube.centerpix[0]-pixels1,cube.centerpix[0]+pixels2)
            ax.set_ylim(cube.centerpix[1]-pixels1,cube.centerpix[1]+pixels2)
          else:
            pixels=zoomto/np.abs(cube.wcsrel.wcs.cdelt[0])
            ax.set_xlim(cube.centerpix[0]-pixels,cube.centerpix[0]+pixels)
            ax.set_ylim(cube.centerpix[1]-pixels,cube.centerpix[1]+pixels)

        # set the border of the coordinate frames to white
        # FIXME: spacing is hardcoded, that does not work always
        ax.coords[0].frame.set_color(framecolor)
        ax.coords[0].set_ticks(color=framecolor,spacing=self.labelspacing*u.arcsec)
        ax.coords[1].set_ticks(color=framecolor,spacing=self.labelspacing*u.arcsec)
        if not (ir==nrow-1 and ic==0):
          ax.coords[0].set_ticklabel_visible(False)
        else:
            ax.set_xlabel("rel. RA ['']")

        if ic>0 or (not ir==nrow-1):
          ax.coords[1].set_ticklabel_visible(False)
        else:
          ax.set_ylabel("rel. Dec. ['']")

        # print the velocities relative to the systemic velocities
        props=dict(boxstyle='round',facecolor='white',edgecolor="none")

        if vellabel_fontsize>0:
          ax.text(0.95,0.95,"{:5.2f}".format(cube.vel[velidx]-cube.systemic_velocity*(u.km/u.s)),
                  transform=ax.transAxes,fontsize=vellabel_fontsize,
                  verticalalignment='top',horizontalalignment="right",bbox=props)

        # mark the center
        ax.plot(cube.centerpix[0],cube.centerpix[1],marker="x",color="0.6",linewidth=0.5,ms=2)

        linecont=None
        if clevels is not None:
          if ccolors is None:
            ccolors="black"
          linecont=ax.contour(cube.data[velidx,:,:]*scalefac,np.array(clevels)*scalefac,origin="lower",
                     linewidths=1.0,
                     colors=ccolors)

        # ax.axis('equal')
        self.add_beam(ax,cube,color=beam_color)

        if rms:
        # calculate the rms of the residual
          rms=numpy.nansum((cube.data[velidx,:,:]**2.0)/cube.data[velidx,:,:].size)**0.5
          ax.text(0.05,0.95,"rms="+"{:4.1e}".format(rms),
                 transform=ax.transAxes,fontsize=5,
                 verticalalignment='top',horizontalalignment="left",bbox=props)

    # FIXME: format is hardcoded that does not work always
    ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)
    if nrow==1 and ncol==1:  # single plot case
      axcb=ax
    else:
      axcb=axes.ravel().tolist()

    CB=fig.colorbar(im,ax=axcb,format=cb_format,
                       fraction=cb_fraction,pad=cb_pad,extend=cb_extend)
    CB.set_ticks(ticks)
    if mJy:
      CB.set_label("[mJy/beam]")
    else:
      CB.set_label("[Jy/beam]")
    # plt.tight_layout(pad=0.1)

    if "title" in kwargs:
      fig.suptitle(kwargs["title"],y=0.9)

    if "movie" in kwargs:
      return self._closefig(fig),im,linecont
    elif returnFig:
      return fig
    else:
      return self._closefig(fig)

  def plot_integrated_diff(self,imageObs,imageModel,imageDiff,zlim=[None,None],
                           mJy=False,zoomto=None,**kwargs):
    """
    Plots an image and its diff Model-Obs.

    Parameters
    ----------

    zoomto : float
      this parameters allows to zoom into the image. The unit is in arcsec.
      E.g. zoomto=1.0 will show the region around the the center ranging
      from -1.0 to 1.0 arcsec for the x and y axis.


    """

    if imageObs is None or imageModel is None or imageDiff is None: return

    scalefac=1.0
    if mJy==True:
      scalefac=1000.0

    vmin=zlim[0]
    vmax=zlim[1]
    if vmin is None: vmin=numpy.nanmin([imageObs.data,imageDiff.data])
    if vmax is None: vmax=numpy.nanmax([imageObs.data,imageDiff.data])
    vmin=vmin*scalefac
    vmax=vmax*scalefac
    # print("interated_diff: ",vmin,vmax,numpy.nanmin([imageDiff.data]),numpy.nanmax([imageDiff.data]))

    # wcsim=wcs.WCS(image.header)
    # wcsrel=linear_offset_coords(wcsim, image.centerpix)
    fig,axes=plt.subplots(1,3,subplot_kw=dict(projection=imageObs.wcsrel),
                           figsize=pplot.scale_figs([2.1,1.0]))

    im=axes[0].imshow(imageObs.data*scalefac,cmap="inferno",vmin=vmin,vmax=vmax,origin="lower")
    im2=axes[1].imshow(imageModel.data*scalefac,cmap="inferno",vmin=vmin,vmax=vmax,origin="lower")
    im3=axes[2].imshow(imageDiff.data*scalefac,cmap="inferno",vmin=vmin,vmax=vmax,origin="lower")

    if zoomto is not None:
      for ax,image in zip(axes,(imageObs,imageModel,imageDiff)):
        pixels=zoomto/np.abs(image.wcsrel.wcs.cdelt[0])
        ax.set_xlim(image.centerpix[0]-pixels,image.centerpix[0]+pixels)
        ax.set_ylim(image.centerpix[1]-pixels,image.centerpix[1]+pixels)

    # calculate the rms of the residual
    rms=numpy.nansum((imageDiff.data**2.0)/imageDiff.data.size)**0.5

    # print the velocities relative to the systemic velocities
    props=dict(boxstyle='round',facecolor='white',edgecolor="none")
    axes[0].text(0.95,0.95,"Observation",transform=axes[0].transAxes,
                 fontsize=6,verticalalignment='top',horizontalalignment="right",bbox=props)
    axes[1].text(0.95,0.95,"Model",transform=axes[1].transAxes,
                 fontsize=6,verticalalignment='top',horizontalalignment="right",bbox=props)
    axes[2].text(0.95,0.95,"Residual (rms="+"{:4.1e}".format(rms)+")",
                 transform=axes[2].transAxes,fontsize=6,
                 verticalalignment='top',horizontalalignment="right",bbox=props)
    # axes.coords[0].set_major_formatter('hh:mm:ss')

    for ax in axes:
      ax.coords[1].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
      ax.coords[0].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
      ax.coords[0].frame.set_color("white")
      ax.set_xlabel("rel. RA ['']")

    # needs to be converted to pixels, that is the data unit
    self.add_beam(axes[0],imageObs)

    axes[0].set_ylabel("rel. Dec. ['']")
    # mark the center
    # axes[0].plot(imageObs.centerpix[0], imageObs.centerpix[1], marker="x", color="0.6", linewidth=0.5, ms=3)

    # axes.axvline(image.centerpix[0],color="0.6",linewidth=0.8,linestyle=":")
    # axes.axhline(image.centerpix[1],color="0.6",linewidth=0.8,linestyle=":")

      # FIXME: that would show the image like in the casaviewer
    # axes.invert_yaxis()

    if mJy==True:
      clabel="[mJy/beam km/s]"
    else:
      clabel="[Jy/beam km/s]"

    self._dokwargs(axes[0],**kwargs)

    ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)
    CB=fig.colorbar(im,ax=axes.ravel().tolist(),pad=0.02,
                    format="%5.2f",fraction=0.04)
    CB.set_ticks(ticks)
    CB.set_label(clabel)

    return self._closefig(fig)

  def plot_integrated(self,image,zlim=[None,None],mJy=False,cb_format="%5.1f",cb_show=True,
                      cmap="inferno",clabel=None,zoomto=None,clevels=None,ccolors=None,
                      cb_fraction=0.04,zlog=False,powerNormGamma=None,showBeam=True,
                      cb_pad=0.02,cb_extend="neither",
                      ax=None,**kwargs):
    """
    Plots a zeroth moment image (integrated intensity) image.

    Parameters
    ----------

    zoomto : float
      this parameters allows to zoom into the image. The unit is in arcsec.
      E.g. zoomto=1.0 will show the region around the the center ranging
      from -1.0 to 1.0 arcsec for the x and y axis.

    ax : :class:`~matplotlib.axes.Axes`
      An matplotlic Axes object that is used to make the plot. if 'None' an new one will be created.

    """
    scalefac=1.0
    if mJy==True:
      scalefac=1000.0

    if image is None: return

    vmin=zlim[0]
    vmax=zlim[1]
    if vmin is None: vmin=numpy.min(image.data)
    if vmax is None: vmax=numpy.max(image.data)
    vmin=vmin*scalefac
    vmax=vmax*scalefac

    fig,ax=self._initfig(ax,subplot_kw=dict(projection=image.wcsrel),**kwargs)

#    if zlog:
#      val=np.log10(image.data*scalefac)
#      vmin=np.log10(vmin)
#      vmax=np.log10(vmax)
#    else:

    val=image.data*scalefac

    norm=None
    if zlog:
      norm=mcolors.LogNorm(vmin=vmin,vmax=vmax)
    elif powerNormGamma is not None:
      norm=mcolors.PowerNorm(powerNormGamma,vmin=vmin,vmax=vmax)

    im=ax.imshow(val,norm=norm,
                   cmap=cmap,vmin=vmin,vmax=vmax,
                   origin="lower")

    # FIXME: does not work with zlog
    if clevels is not None:
      if ccolors is None:
        ccolors="black"
      ax.contour(image.data*scalefac,np.array(clevels)*scalefac,origin="lower",
                 linewidths=0.5,
                 colors=ccolors)

    if zoomto is not None:
      if type(zoomto) is list:
        pixels1=zoomto[0]/np.abs(image.wcsrel.wcs.cdelt[0])
        pixels2=zoomto[1]/np.abs(image.wcsrel.wcs.cdelt[0])
        ax.set_xlim(image.centerpix[0]-pixels1,image.centerpix[0]+pixels2)
        ax.set_ylim(image.centerpix[1]-pixels1,image.centerpix[1]+pixels2)
      else:
        pixels=zoomto/np.abs(image.wcsrel.wcs.cdelt[0])
        ax.set_xlim(image.centerpix[0]-pixels,image.centerpix[0]+pixels)
        ax.set_ylim(image.centerpix[1]-pixels,image.centerpix[1]+pixels)

    # ax.coords[0].set_major_formatter('hh:mm:ss')
    # FIXME: spacing is hardcoded that does not work always
    ax.coords[1].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
    ax.coords[0].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
    ax.coords[0].frame.set_color("white")

    # needs to be converted to pixels, that is the data unit
    if showBeam: self.add_beam(ax,image)
    ax.set_xlabel("rel. RA ['']")
    ax.set_ylabel("rel. Dec. ['']")

    # mark the center
    # FIXME: alow to control the size of the cross
    # ax.plot(image.centerpix[0], image.centerpix[1], marker="x", color="0.6", linewidth=0.2, ms=1)

    # ax.axvline(image.centerpix[0],color="0.6",linewidth=0.8,linestyle=":")
    # ax.axhline(image.centerpix[1],color="0.6",linewidth=0.8,linestyle=":")

      # FIXME: that would show the image like in the casaviewer
    # ax.invert_yaxis()

    self._dokwargs(ax,**kwargs)

    # FIXME: format is hardcoded that does not work always
    if clabel is None:
      if mJy==True:
        clabel="[mJy/beam km/s]"
      else:
        clabel="[Jy/beam km/s]"

 #   if zlog:
 #     clabel="log "+clabel

    if cb_show:
      ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)

      axcb=np.array(fig.get_axes()).ravel().tolist()
      CB=fig.colorbar(im,ax=axcb,pad=cb_pad,
                        format=cb_format,fraction=cb_fraction,extend=cb_extend)

      CB.set_ticks(ticks)
      CB.set_label(clabel)

    if "movie" in kwargs:
      return self._closefig(fig),im
    else:
      return self._closefig(fig)

  def plot_mom1_diff(self,imageObs,imageModel,imageDiff,zlim=[None,None],
                     zoomto=None,**kwargs):
    """
    Plots the moment 1 observations , model and the difference map.

    Parameters
    ----------

    zoomto : float
      this parameters allows to zoom into the image. The unit is in arcsec.
      E.g. zoomto=1.0 will show the region around the the center ranging
      from -1.0 to 1.0 arcsec for the x and y axis.

    """

    if imageObs is None or imageModel is None: return

    vmin=zlim[0]
    vmax=zlim[1]

    veldataObs=imageObs.data-imageObs.systemic_velocity
    veldataModel=imageModel.data-imageModel.systemic_velocity
    if vmin is None: vmin=numpy.nanmin(veldataObs)
    if vmax is None: vmax=numpy.nanmax(veldataObs)

    # wcsim=wcs.WCS(image.header)
    # wcsrel=linear_offset_coords(wcsim, image.centerpix)
    fig,axes=plt.subplots(1,3,subplot_kw=dict(projection=imageObs.wcsrel),
                           figsize=pplot.scale_figs([2.25,1.0]))
    for ax in axes:
      ax.set_facecolor("black")

    im=axes[0].imshow(veldataObs,cmap="seismic",vmin=vmin,vmax=vmax,origin="lower")
    im1=axes[1].imshow(veldataModel,cmap="seismic",vmin=vmin,vmax=vmax,origin="lower")
    im2=axes[2].imshow(imageDiff.data,cmap="seismic",vmin=vmin,vmax=vmax,origin="lower")

    if zoomto is not None:
      for ax,image in zip(axes,(imageObs,imageModel,imageDiff)):
        pixels=zoomto/np.abs(image.wcsrel.wcs.cdelt[0])
        ax.set_xlim(image.centerpix[0]-pixels,image.centerpix[0]+pixels)
        ax.set_ylim(image.centerpix[1]-pixels,image.centerpix[1]+pixels)

    rms=numpy.nansum((imageDiff.data**2.0)/imageDiff.data.size)**0.5

    # print the velocities relative to the systemic velocities
    props=dict(boxstyle='round',facecolor='white',edgecolor="none")
    axes[0].text(0.95,0.95,"Observation",transform=axes[0].transAxes,
                 fontsize=6,verticalalignment='top',
                 horizontalalignment="right",bbox=props)
    axes[1].text(0.95,0.95,"Model",transform=axes[1].transAxes,
                 fontsize=6,verticalalignment='top',
                 horizontalalignment="right",bbox=props)
    axes[2].text(0.95,0.95,"Residual (rms="+"{:4.1e}".format(rms)+")",
                 transform=axes[2].transAxes,fontsize=6,
                 verticalalignment='top',horizontalalignment="right",bbox=props)

    for ax in axes:
      ax.coords[1].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
      ax.coords[0].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
      ax.coords[0].frame.set_color("white")
      ax.set_xlabel("rel. RA ['']")
    # needs to be converted to pixels, that is the data unit
    self.add_beam(axes[0],imageObs)

    axes[0].set_ylabel("rel. Dec. ['']")

    self._dokwargs(ax,**kwargs)

    # FIXME: that would show the image like in the casaviewer
    # ax.invert_yaxis()
    ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)
    CB=fig.colorbar(im,ax=axes.ravel().tolist(),pad=0.02,
                    format="%5.2f",fraction=0.04)
    CB.set_ticks(ticks)
    CB.set_label("velocity [km/s]")

    self._closefig(fig)

  def plot_mom1(self,image,zlim=[None,None],zoomto=None,cb_extend="neither",**kwargs):
    """
    Plots the momement 1 map.

    Parameters
    ----------

    zoomto : float
      this parameters allows to zoom into the image. The unit is in arcsec.
      E.g. zoomto=1.0 will show the region around the the center ranging
      from -1.0 to 1.0 arcsec for the x and y axis.

    """
    if image is None: return

    vmin=zlim[0]
    vmax=zlim[1]

    veldata=image.data-image.systemic_velocity
    if vmin is None: vmin=numpy.nanmin(veldata)
    if vmax is None: vmax=numpy.nanmax(veldata)

    # wcsim=wcs.WCS(image.header)
    # wcsrel=linear_offset_coords(wcsim, image.centerpix)
    fig,ax=plt.subplots(1,1,subplot_kw=dict(projection=image.wcsrel))
    ax.set_facecolor("black")

    im=ax.imshow(veldata,cmap="RdBu_r",vmin=vmin,vmax=vmax,origin="lower")
    ax.coords[1].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
    ax.coords[0].set_ticks(color="white",spacing=self.labelspacing*u.arcsec)
    ax.coords[0].frame.set_color("white")

    # needs to be converted to pixels, that is the data unit
    self.add_beam(ax,image)
    ax.set_xlabel("rel. RA ['']")
    ax.set_ylabel("rel. Dec. ['']")

    # mark the center
    ax.plot(image.centerpix[0],image.centerpix[1],marker="x",color="0.6",linewidth=0.5,ms=3)
    if zoomto is not None:
      pixels=zoomto/np.abs(image.wcsrel.wcs.cdelt[0])
      ax.set_xlim(image.centerpix[0]-pixels,image.centerpix[0]+pixels)
      ax.set_ylim(image.centerpix[1]-pixels,image.centerpix[1]+pixels)

    self._dokwargs(ax,**kwargs)

    # FIXME: that would show the image like in the casaviewer
    # ax.invert_yaxis()
    ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)
    CB=fig.colorbar(im,ax=ax,pad=0.02,
                    format="%5.2f",fraction=0.04,extend=cb_extend)
    CB.set_ticks(ticks)
    CB.set_label("velocity [km/s]")

    self._closefig(fig)

  def plot_pv(self,image,zlim=[None,None],ylim=[None,None],**kwargs):
    """
    Plots a position-velocity diagram.
    """

    if image is None: return

    vmin=zlim[0]
    vmax=zlim[1]
    if vmin is None: vmin=numpy.nanmin(image.data)
    if vmax is None: vmax=numpy.nanmax(image.data)

  # FIXME: stolen from here ... https://github.com/astropy/astropy/issues/4529
    # mabe not the best way to go
    # Provide the velocities already at the init step (not in the plot routines)

    wcsa=wcs.WCS(image.header,naxis=(1))
    xpix=numpy.arange(image.header['NAXIS1'])
    arcsec=wcsa.wcs_pix2world(xpix,0)
    xticklabels=MaxNLocator(nbins="auto",symmetric=True,prune="both").tick_values(numpy.min(arcsec),numpy.max(arcsec))

    xticks,=wcsa.wcs_world2pix(xticklabels,0)
    xticks=xticks

    # prepare the y coordinate, want it relative to the center (systemic velocity)
    wcsvel=wcs.WCS(image.header)
    zv=np.arange(image.header['NAXIS2'])
    # this is necessary because of imshow, it always plots in the original pixel scale
    # create symetric ticks in pixel space
    symticks=MaxNLocator(nbins="auto",symmetric=True,prune="both").tick_values(numpy.min(zv-image.centerpix[1]),numpy.max(zv-image.centerpix[1]))
    # this gives then the wantes ytick positions.
    yticks=symticks+image.centerpix[1]

    # now convert the pixel to velocities to get the ylabels
    wv=wcsvel.wcs_pix2world(yticks,yticks,0)[1]
    freq_to_vel=u.doppler_radio(image.header['RESTFRQ']*u.Hz)
    yticklabels=(wv*u.Hz).to(u.km/u.s,equivalencies=freq_to_vel).value
    yticklabels=yticklabels-image.systemic_velocity

    # convert systemtic velocity to pixel coordinates
    sysfrequ=(image.systemic_velocity*u.km/u.s).to(u.Hz,equivalencies=freq_to_vel)
    dummy,sysvelloc=wcsvel.wcs_world2pix(sysfrequ,sysfrequ,0)

    fig,ax=plt.subplots(1,1)
    ax.set_facecolor("black")

    # width in pixel
    # FIXME: use proper units from fits file, here it is assume to be arcsec
    bwidth=(image.bmin*3600/image.header["CDELT1"]+
            image.bmaj*3600/image.header["CDELT1"])/2.0

    ar=AnchoredRectangle(ax.transData,width=bwidth,height=1.0,
                           loc=3,pad=0.5,borderpad=0.4,frameon=False)
    ax.add_artist(ar)

    im=ax.imshow(image.data,cmap="inferno",vmin=vmin,vmax=vmax,aspect='auto',origin="lower")
    ax.set_xticks(xticks)
    ax.set_xticklabels(map(str,xticklabels))
    ax.set_yticks(yticks)
    ax.set_yticklabels([ "{:.2f}".format(x) for x in yticklabels ])

    ax.set_xlabel("offset ['']")
    ax.set_ylabel(r"vel $\mathrm{[km\,s^{-1}]}$")
    ax.axvline(image.centerpix[0],color="0.6",linewidth=0.8,linestyle=":")
    ax.axhline(sysvelloc,color="0.6",linewidth=0.8,linestyle=":")

    ax.tick_params(colors='white',labelcolor='black')
    for spine in ax.spines.values():
      spine.set_edgecolor('white')

    # FIXME: why is this
    ax.invert_yaxis()

    self._dokwargs(ax,**kwargs)

    ticks=MaxNLocator(nbins=6).tick_values(vmin,vmax)
    CB=fig.colorbar(im,ax=ax,pad=0.02,
                    format="%5.2f",fraction=0.04)
    CB.set_ticks(ticks)
    CB.set_label("[Jy/beam]")

    self._closefig(fig)

  def plot_specprof(self,specprof,models=None,xlim=[None,None],modelNames=None,**kwargs):
    """
    Plots a spectral profile (histogram style).
    """

    if specprof is None and models is None: return

    fig,ax=plt.subplots(1,1)

    if models is not None:
      if modelNames is None:
        modelNames=["model"+"{:0d}".format(i+1) for i in range(len(models))]

      for model,label in zip(models,modelNames):
        x,y=self.specprof_xy_hist(model)
        ax.plot(x,y,label=label)

    if specprof is not None:
      x,y=self.specprof_xy_hist(specprof)
      ax.plot(x,y,label="Observation",color="black")

    # pGrayBox=0.3
    # ax.fill_between(x, y *(1.0-pGrayBox), y * (1+pGrayBox), color='0.8')

    ax.set_xlim(xlim)
    ax.set_xlabel("velocity [km/s]")
    ax.set_ylabel("flux [Jy]")

    handles,labels=ax.get_legend_handles_labels()
    if len(labels)>1:
      ax.legend(handles,labels,fancybox=False)

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def plot_radprof(self,radprof,models=None,modelNames=None,pmGrayBox=0.25,**kwargs):
    """
    Plots a radial profile.
    """
    if radprof is None: return

    fig,ax=plt.subplots(1,1)

    # pGrayBox=0.3
    # ax.fill_between(radprof.arcsec, radprof.flux *(1.0-pGrayBox), radprof.flux * (1+pGrayBox), color='0.8')

    if models is not None:
      if modelNames is None:
        modelNames=["model"+"{:0d}".format(i+1) for i in range(len(models))]

      for model,label in zip(models,modelNames):
        ax.errorbar(model.arcsec,model.flux,yerr=model.flux_err,label=label,elinewidth=0.5,zorder=-32)

    if pmGrayBox is not None:
      ax.fill_between(radprof.arcsec,
                      radprof.flux-radprof.flux*pmGrayBox,
                      radprof.flux+radprof.flux*pmGrayBox,color='0.8')

    # ax.plot(radprof.arcsec,radprof.flux)
    ax.errorbar(radprof.arcsec,radprof.flux,
                yerr=radprof.flux_err,label="observation",
                color="black",elinewidth=0.5)

    # indicate the beam
    ax.set_xlabel("radius ['']")
    ax.set_ylabel("flux [$\mathrm{Jy/beam\,km/s}$]")
    ax.set_xlim(0,None)

    if radprof.bwidth is not None:
      ar=AnchoredRectangle(ax.transData,width=radprof.bwidth,height=0.0,
                           loc=3,pad=0.5,borderpad=0.4,frameon=False,color="0.6")
      ax.add_artist(ar)

    handles,labels=ax.get_legend_handles_labels()
    if len(labels)>1:
      ax.legend(handles,labels,fancybox=False)

    self._dokwargs(ax,**kwargs)

    return self._closefig(fig)

  def specprof_xy_hist(self,specprof):
    """
    Produce x,y coordinates to plot spectral profile in histogram style.

    """
    x=list()
    y=list()
    for i in range(len(specprof.vel)):
      if i==0:
        x.append(specprof.vel[i])
        y.append(specprof.flux[i])
      else:
        xval=(specprof.vel[i-1]+specprof.vel[i])/2.0
        x.append(xval)
        y.append(specprof.flux[i-1])
        x.append(xval)
        y.append(specprof.flux[i])

    # relative to the systemic velocity
    # should be zero if not set
    x.append(specprof.vel[-1])
    y.append(specprof.flux[-1])

    x=np.array(x)-specprof.systemic_velocity
    return x,np.array(y)


class AnchoredRectangle(AnchoredOffsetbox):

    def __init__(self,transform,width,height,loc,
                pad=0.1,borderpad=0.1,prop=None,frameon=False,color="white"):
      """
      Draw a rectangle the size in data coordinate of the give axes.

      pad, borderpad in fraction of the legend font size (or prop)
      adapted from :class:`AnchoredEllipse`
      """
      self._box=AuxTransformBox(transform)
      self.rectangle=patches.Rectangle((2,1),width,height,color=color)
      self._box.add_artist(self.rectangle)

      AnchoredOffsetbox.__init__(self,loc,pad=pad,borderpad=borderpad,
                                 child=self._box,
                                 prop=prop,
                                 frameon=frameon)


class AnchoredEllipse(AnchoredOffsetbox):

  def __init__(self,transform,width,height,angle,loc,
              pad=0.1,borderpad=0.1,prop=None,frameon=False,color="white"):
    """
    Draw an ellipse the size in data coordinate of the give axes.

    pad, borderpad in fraction of the legend font size (or prop)
    Copied from https://matplotlib.org/mpl_toolkits/axes_grid/api/anchored_artists_api.html
    Adapted it a bit (I think)

    Check how to use original class properly.

    """
    self._box=AuxTransformBox(transform)
    self.ellipse=patches.Ellipse((0,0),width,height,angle,color=color)
    self._box.add_artist(self.ellipse)

    AnchoredOffsetbox.__init__(self,loc,pad=pad,borderpad=borderpad,
                               child=self._box,
                               prop=prop,
                               frameon=frameon)

