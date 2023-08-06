from abc import ABC,abstractmethod
from builtins import ValueError

from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator
from scipy import interpolate

import matplotlib.pyplot as plt
import numpy as np
import prodimopy.plot as pplot
import prodimopy.read as pread


class MovieABC(ABC):
  '''
  A abstract class to make a movie for a series of ProDiMo models for a 2D contour plot.
  For each model also an age (a time) needs to be supplied.
  To produce a smooth video the data from the ProDiMo models are interpolated.
  For example one can provide 10 ProDiMo models but produce 100 frames for the movie.

  Currently linear intepolation in either logspace or linear space is used.

  Uses `matplotlib.animation.FuncAnimation`. To produce an mp4 movie ffmpeg needs to be
  available.

  Currently this routine was only tested on macOS X with ffmpeg installed via port and on
  a Scientifc Linux maching with ffmpeg preinstalled. Those cases worked without problems.

  Alternatively also an html file (html video tag) can be written. But it is unclear of ffmpeg
  or something similar is required. Worked on macOS X.

  Also calls :func:`~prodimopy.movie.ContourMovie.init_figure`

  Attributes
  ----------
  '''

  def __init__(self,ages,models,
               timescalefac=3.0,
               ageslog=True,
               nframes=40,
               nbins=40):

    if ageslog:
      self.ages=np.log10(ages)  # currently only on log scale
    else:
      self.ages=ages
    """ array_like(float,ndim=1) :
    A list of ages for the model. Each age corresponds to one model (see `models` Attribute).
    The unit is `yr`.
    """
    self.models=models
    """ array_like(objects,ndim=1) :
    A list of model objects (data). Must have the same length as `ages`
    """
    self.timescalefac=timescalefac
    """ float :
    The runtime of the movie will be scaled by this value.
    Currently the runtime of the movie is given by log10 of the maximum age times `timescalefac`.
    """
    self.ageslog=ageslog
    """ bool :
    Use the log10 of ages or not: Defalt `True`
    """
    self.nframes=nframes
    """ int :
    How many frames should this movie have. Has impact on the smoothness and the size of the video.
    Does not afect the runtime of the movie.
    """
    self.nbins=nbins
    """ int :
    How many bins should be use for the contourf plot.
    """

    self._times=None
    self._interval=None
    self._interpolFunc=None

    self._fig=None
    self._timelabel=None

    self._init_times()
    self._init_interpolation()
    self.init_figure()

  def _init_times(self):
    """
    Initialises the runtime and the time per frame.

    The runtime is given by the last entry in ages. But it will be scaled accordingly to
    `timescalefac`

    _todo: allow for linear time

    """

    # either start at zero or the given start time if it is negative
    self._times=np.linspace(np.min([0,self.ages[0]]),self.ages[-1],self.nframes)
    movietime=self.ages[-1]*self.timescalefac  # this is now interpreted as seconds
    self._interval=(self._times[-1]-self._times[-2])*1000*self.timescalefac  # is in millisecons
    print("Movietime [s]: ",movietime," frametime: [ms]: ",self._interval)
    return

  @abstractmethod
  def _init_interpolation(self):
    """
    Should initialize the data array and the interpolation function.

    Uses `scipy.inerpolate.interp1d`.

    Initializes `_interpolFunc`
    """
    pass

  @abstractmethod
  def init_figure(self):
    """
    Initialisation of the matplotlib figure. Also here the parts that stay fixed are plotted.
    In this case for example the colourbar.

    This routine should set the internal attribute `_fig`,`_cont` and `_timelabel` for the
    `ContourMovie` object.

    Needs to be implmented by the subclass.
    """
    pass

  @abstractmethod
  def animate(self,frame):
    """
    Animate function. I called for each frame of the movie.
    This routine should only replot the stuff that is actually animated.

    For more details see also `matplotlib.animation.FuncAnimation`.

    Parameters
    ----------

    frame : int
      The frame number (starting from 0)

    Returns
    -------
      Has to return a list of artists that should be updated.
    """
    pass

  def make_movie(self,outfile):
    """
    Makes the movie and writes it to a file. The routine uses
    `matplotlib.animation.FuncAnimation`

    There are three possivle formats for the movie: `.mp4`,`.html` and `.gif`.
    The mp4 format requires `ffmpeg` installed. In case of the html format
    the html 5 video tag is used. It likely also required ffmpeg (I am not sure).
    For gif format imagemagick is necessary.

    The format is derived from the given filename `outfile`.

    Parameters
    ----------

    outfile : str
      Outputfile name. The name also defines the outputformat.

    """

    # Initialise our plot. Make sure you set vmin and vmax!

    animation=FuncAnimation(
      # Your Matplotlib Figure object
      self._fig,
      # The function that does the updating of the Figure
      self.animate,
      # Frame information (here just frame number)
      np.arange(self.nframes),
      # Extra arguments to the animate function
      fargs=[],
    # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
      interval=self._interval
      )

    # Try to set the DPI to the actual number of pixels you're plotting
    if ".mp4" in outfile:
      print("Make an mp4 movie with ffmpeg ...")
      animation.save(outfile,dpi=256,writer="ffmpeg")
    elif ".gif" in outfile:
      print("Make an animated gif with imagemagick ...")
      animation.save(outfile,dpi=256,writer="imagemagick")
    elif ".html" in outfile:
      print("Make an html with ffmpeg ...")
      fp=open(outfile,"w+")
      fp.write(animation.to_html5_video())
      fp.close()
    else:
      print("Do the default thing ... ")
      animation.save(outfile,dpi=256)


class ContourMovie(MovieABC):
  '''
  A class to make a movie for a series of ProDiMo models for a 2D contour plot.
  For each model also an age (a time) need to be supllied.
  To produce a smooth video the data from the ProDiMo models are interpolated.
  For example one can provide 10 ProDiMo models but produce 100 frames for the movie.

  Currently linear intepolation in either logspace or linear space is used.

  Uses `matplotlib.animation.FuncAnimation`. To produce an mp4 movie ffmpeg needs to be
  available.

  Currently this routine was only tested on macOS X with ffmpeg installed via port and on
  a Scientifc Linux maching with ffmpeg preinstalled. Those cases worked without problems.

  Alternatively also an html file (html video tag) can be written. But it is unclear of ffmpeg
  or something similar is required. Worked on macOS X.

  Also calls :func:`~prodimopy.movie.ContourMovie.init_figure`

  Attributes
  ----------
  '''

  def __init__(self,ages,models,zlim,field=None,species=None,
               timescalefac=3.0,
               ageslog=True,
               nframes=40,
               nbins=40,
               cblabel=None,
               plot_cont_dict={}):

    if field is None and species is None:
      raise ValueError("Eiter `field` or `species` must be set.")

    self.field=field
    """ str :
    The attribute of :class:`~prodimopy.read.Data_ProDiMo` that should be plotted (e.g. tg).
    The routine then trys to find this field for each ProDiMo model.
    Is opitonal, but than species must be set.
    """
    self.species=species
    """ str :
    A species name. If given the abundance of that species is plotted.
    Optional, if not set field must be set.
    """
    self.zlim=zlim
    """ array_like(float,ndim=1) :
    The minimum and maximum for the data range `[min,max]`. Needs to be set and will be
    the same for all frames of the movie.
    """
    self.cblabel=cblabel
    """ str :
    The label for the colorbar.
    """

    self._cont=None
    self._plot_cont_dict=plot_cont_dict
    """ dict :
    A dictionary with parameters for the ":func:`~plot.Plot.plot_cont`. This way one can
    control the style of the plot. For example {'zr': True, 'xlog': True }
    """

    super(ContourMovie,self).__init__(ages,models,
           timescalefac=timescalefac,
           ageslog=ageslog,
           nframes=nframes,
           nbins=nbins)

#   def _init_times(self):
#     """
#     Initialises the runtime and teh time per frame.
#
#     The runtime is given by the last entry in ages. But it will be scaled accordingly to
#     `timescalefac`
#
#     _todo: allow for linear time
#
#     """
#
#     # either start at zero or the given start time if it is negative
#     self._times=np.linspace(np.min([0,self.ages[0]]), self.ages[-1], self.nframes)
#     movietime=self.ages[-1]*self.timescalefac # this is now interpreted as seconds
#     self._interval=(self._times[-1]-self._times[-2])*1000*self.timescalefac # is in millisecons
#     print("Movietime [s]: ",movietime," frametime: [ms]: ",self._interval)
#     return

  def _init_interpolation(self):
    """
    Initializes the data array and the interpolation function.

    Uses `scipy.inerpolate.interp1d`.

    Initializes `_interpolFunc`

    """
    # bulit the data array use for interpolation and plotting
    data=list()
    for model in self.models:
      if self.species is not None:
        data.append(model.getAbun(self.species))
      else:
        data.append(getattr(model,self.field))

    data=np.array(data)

    self._interpolFunc=interpolate.interp1d(self.ages,data,axis=0,fill_value="extrapolate")

  def init_figure(self):
    """
    Initialisation of the matplotlib figure. Also here the parts that stay fixed are plotted.
    In this case for example the colourbar.

    This routines set the internal attribute `_fig`,`_cont` and `_timelabel` for the
    `ContourMovie` object.
    """

    # make the initial plot, using the standard routine (with movie mode)
    pp=pplot.Plot(None)

    if self.species is not None:
      fig,cf=pp.plot_abuncont(self.models[0],self.species,zlim=self.zlim,contour=False,
                              nbins=self.nbins,movie=True,extend="both",**self._plot_cont_dict)
    else:
      fig,cf=pp.plot_cont(self.models[0],getattr(self.models[0],self.field),
                          zlim=self.zlim,contour=False,label=self.cblabel,
                          nbins=self.nbins,movie=True,extend="both",**self._plot_cont_dict)

    ax=fig.axes[0]
    props=dict(boxstyle='round',facecolor='white')
    timelabel=ax.text(0.04,0.96,"",transform=ax.transAxes,ha="left",va="top",bbox=props)

    fig.tight_layout()

    self._fig=fig
    self._cont=cf
    self._timelabel=timelabel

  def animate(self,frame):
    """
    Animate function. I called for each frame of the movie.
    This routine should only replot the stuff that is actually animated.

    Here only the filled contours and the timelabel is updadted.

    For more details see also `matplotlib.animation.FuncAnimation`.

    Parameters
    ----------

    frame : int
      The frame number (starting from 0)

    Returns
    -------
      A list of artists that should be updated.


    """

    # need to remove all filled contours first
    for tp in self._cont.collections:
        tp.remove()

    # time=interval*(frame)/1000*scalefac
    time=self._times[frame]

    print("Do Frame: "+str(frame)+", time: "+str(time))

    modelidx=np.argmin(np.abs(self.ages-time))
    # FIXME: inf the interpolation fails this might cause problems.
    values=np.log10(self._interpolFunc(time))

    # Should not happen to ofen so check first
    if np.isnan(values).any():
      print("Found NaN (likely interpolation problem) ... fix it.")
      values[np.isnan(values)]=np.nanmin(values)
    # values[np.isnan[values]]:
    # vlim=np.log10(self.zlim)

    # levels = MaxNLocator(nbins=self.nbins).tick_values(vlim[1], vlim[0])
    y=self.models[modelidx].z
    if ("zr" in self._plot_cont_dict):
      if self._plot_cont_dict["zr"]==True:
        y=self.models[modelidx].z/self.models[modelidx].x

    self._cont=self._cont.ax.contourf(self.models[modelidx].x,y,values,
                       levels=self._cont.levels,extend="both")

    for c in self._cont.collections:
      c.set_edgecolor("face")

    if frame==0:
      self._timelabel.set_text("{:.2e} yrs".format(0.0))
    else:
      if self.ageslog:
        outtime=10**time
      else:
        outtime=time
      self._timelabel.set_text("{:.2e} yrs".format(outtime))

    return self._cont.collections+[self._timelabel]


class CasaSimMovie(MovieABC):
  '''
  Make a movie out of Casa/ALMA simulations. Currently only integrated
  images (total intensity, continuum) can be used. For example at each age
  there is one image.

  '''

  def __init__(self,ages,models,
               timescalefac=3.0,
               ageslog=True,
               nframes=40,
               nbins=40,
               plot_dict={}):

    self._image=None
    self.plot_dict=plot_dict
    super(CasaSimMovie,self).__init__(ages,models,
       timescalefac=timescalefac,
       ageslog=ageslog,
       nframes=nframes,
       nbins=nbins)

  def init_figure(self):
    ppc=pcasa.PlotCasasim(None,labelspacing=5)
    print(self.plot_dict)
    fig,im=ppc.plot_integrated(self.models[0].integrated,zoomto=16.5,zlim=[0,1.2],movie=True,cmap="hot",**self.plot_dict)

    ax=fig.axes[0]
    props=dict(boxstyle='round',facecolor='white')
    timelabel=ax.text(0.04,0.96,"",transform=ax.transAxes,ha="left",va="top",bbox=props)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.115)

    print(fig.get_size_inches())

    self._fig=fig
    self._image=im
    self._timelabel=timelabel

  def animate(self,frame):
    # time=interval*(frame)/1000*scalefac
    time=self._times[frame]

    print("Do Frame: "+str(frame)+", time: "+str(time))

    # modelidx=np.argmin(np.abs(self.ages-time))
    values=self._interpolFunc(time)

    self._image.set_array(values)

    if frame==0:
      self._timelabel.set_text("{:.2e} yrs".format(0.0))
    else:
      if self.ageslog:
        outtime=10**time
      else:
        outtime=time
      self._timelabel.set_text("{:.2e} yrs".format(outtime))

    return [self._image,self._timelabel]

  def _init_interpolation(self):
    """
    Initializes the data array and the interpolation function.

    Uses `scipy.inerpolate.interp1d`.

    Initializes `_interpolFunc`

    """
    # bulit the data array use for interpolation and plotting
    data=list()
    for model in self.models:
      data.append(model.integrated.data)

    data=np.array(data)

    self._interpolFunc=interpolate.interp1d(self.ages,data,axis=0,fill_value="extrapolate")

