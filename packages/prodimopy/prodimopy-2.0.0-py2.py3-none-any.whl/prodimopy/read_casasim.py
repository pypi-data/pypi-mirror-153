"""
.. module:: read_casasim

.. moduleauthor:: Ch. Rab


"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from astropy import units as u
from astropy.wcs.utils import proj_plane_pixel_scales

import astropy.io.fits as fits
import astropy.wcs as wcs
import numpy as np


class CasaSim():
  """
  Data container for a CASA line simulation (observations).

  The class can be used to quickly read in a CASA simulation for a single
  spectral line. The main purpose is to read in the various different kind
  of observables which have been produced by CASA.

  Can deal with the following files wiht a given PREFIX
    - `PREFIX.cube.fits` the spectral line cube
    - `PREFIX.cube.integrated.fits` the integrated line emission (zeroth moment)
    - `PREFIX.cube.integrated.radial` the azimuthally averaged radial profile (text file produce by casairing task)
    - `PREFIX.cube.specprof` the spectral line profile (text file produced by CASA)
    - `PREFIX.cube.mom1.fits` the first moment of the line emission
    - `PREFIX.cube.pv.fits` the position velocity diagram
    - `PREFIX.cont.fits` the corrresponding continuum
    - `PREFIX.cont.radial` the azimuthally average radial continuum profile

  During the init of this Class it is tried to read all this files. However, all of them are
  optional and the according attribute is set to `None` in case the file could not be read.

  """

  def __init__(self,fn_prefix,directory=".",systemic_velocity=0.0,distance=None,
               coordinates=None,
               fn_cube=".cube.fits",
               fn_cube_diff=".cube.diff.fits",
               fn_integrated=".cube.integrated.fits",
               fn_integrated_diff=".cube.integrated.diff.fits",
               fn_radprof=".cube.integrated.radial",
               fn_specprof=".cube.specprof",
               fn_mom1=".cube.mom1.fits",
               fn_mom1_diff=".cube.mom1.diff.fits",
               fn_pv=".cube.pv.fits",
               fn_pv_diff=".cube.pv.diff.fits",
               fn_cont=".cont.fits",
               fn_cont_diff=".cont.diff.fits",
               fn_cont_radprof=".cont.radial"):
    """
    Parameters
    ----------

    fn_prefix : str
      the prefix used for all files the routine try to read

    directory :
      the directory with the files (optional)

    systemic_velocity : float
      the systemic_velocity of the target (optional)

    distance : float
      the distance of the target (optional).
      Try to read it from the fits file in case of synthetic ProDiMo observations

    coordinates : :class:`astropy.coordinates.sky_coordinate.SkyCoordinate`
      the coordinates of the target/object including the distance
      FIXME: Note used yet!

    fn* : string
      The fn* parameters can be use to change the filenames for the different files.


    Attributes
    ----------
    systemic_velocity : float
      the systemic velocity of the target, will be passed to the other objects

    distance : float
      the distance of the target, will be passed to the other objects

    cube :class:`.LineCube` :
      the line cube.

    integrated : :class:`.LineIntegrated`
      the zeroth moment of the cube (integrated emission)

    specprof : :class:`.LineSpectralProfile`
      the spectral profile

    radprof : :class:`.RadialProfile`
      the spectra profile

    mom1 : :class:`.LineMom1`
      the first moment of the cube

    pv : :class:`.LinePV`
      the position-velocity diagram

    cont : :class:`.Continuum`
      the associated continuum

    cont_rad : :class:`.RadialProfile`
      the radial profile of the continuum

    """
    self.systemic_velocity=systemic_velocity
    self.fn_cube=self._build_fn(directory,fn_prefix,fn_cube)
    self.fn_cube_diff=self._build_fn(directory,fn_prefix,fn_cube_diff)
    self.fn_integrated=self._build_fn(directory,fn_prefix,fn_integrated)
    self.fn_integrated_diff=self._build_fn(directory,fn_prefix,fn_integrated_diff)
    self.fn_specprof=self._build_fn(directory,fn_prefix,fn_specprof)
    self.fn_radprof=self._build_fn(directory,fn_prefix,fn_radprof)
    self.fn_mom1=self._build_fn(directory,fn_prefix,fn_mom1)
    self.fn_mom1_diff=self._build_fn(directory,fn_prefix,fn_mom1_diff)
    self.fn_pv=self._build_fn(directory,fn_prefix,fn_pv)
    self.fn_pv_diff=self._build_fn(directory,fn_prefix,fn_pv_diff)
    self.fn_cont=self._build_fn(directory,fn_prefix,fn_cont)
    self.fn_cont_diff=self._build_fn(directory,fn_prefix,fn_cont_diff)
    self.fn_cont_radprof=self._build_fn(directory,fn_prefix,fn_cont_radprof)

    # all files are optional ... so if they are not there set the attribute to zero
    found=False
    self.cube=None
    if os.path.isfile(self.fn_cube):
      self.cube=LineCube(self.fn_cube,systemic_velocity=systemic_velocity)
      found=True

    self.distance=distance
    if self.distance is None:
      if "P_DIST" in self.cube.header:
        self.distance=self.cube.header['P_DIST']

    self.incl=None
    if "P_INCL" in self.cube.header:
      self.incl=self.cube.header['P_INCL']

    self.cube_diff=None
    if os.path.isfile(self.fn_cube_diff):
      self.cube_diff=LineCube(self.fn_cube_diff,systemic_velocity=systemic_velocity)
      found=True

    self.integrated=None
    if os.path.isfile(self.fn_integrated):
      self.integrated=LineIntegrated(self.fn_integrated)
      found=True

    self.integrated_diff=None
    if os.path.isfile(self.fn_integrated_diff):
      self.integrated_diff=LineIntegrated(self.fn_integrated_diff)
      found=True

    self.radprof=None
    if os.path.isfile(self.fn_radprof):
      self.radprof=RadialProfile(self.fn_radprof,bwidth=self._beam_width_arcsec(self.integrated))
      found=True

    self.specprof=None
    if os.path.isfile(self.fn_specprof):
      self.specprof=LineSpectralProfile(self.fn_specprof,systemic_velocity=systemic_velocity)
      found=True

    self.mom1=None
    if os.path.isfile(self.fn_mom1):
      self.mom1=LineMom1(self.fn_mom1,systemic_velocity=systemic_velocity)
      found=True

    self.mom1_diff=None
    if os.path.isfile(self.fn_mom1_diff):
      self.mom1_diff=LineMom1(self.fn_mom1_diff,systemic_velocity=systemic_velocity)
      found=True

    self.pv=None
    if os.path.isfile(self.fn_pv):
      self.pv=LinePV(self.fn_pv,systemic_velocity=systemic_velocity)
      found=True

    self.pv_diff=None
    if os.path.isfile(self.fn_pv_diff):
      self.pv_diff=LinePV(self.fn_pv_diff,systemic_velocity=systemic_velocity)
      found=True

    self.cont=None
    if os.path.isfile(self.fn_cont):
      self.cont=Continuum(self.fn_cont)
      found=True

    self.cont_diff=None
    if os.path.isfile(self.fn_cont_diff):
      self.cont_diff=Continuum(self.fn_cont_diff)
      found=True

    self.cont_radprof=None
    if os.path.isfile(self.fn_cont_radprof):
      self.cont_radprof=RadialProfile(self.fn_cont_radprof,bwidth=self._beam_width_arcsec(self.cont))
      found=True

    if not found: raise RuntimeError("No data found at all. Check the passed prefix!")
    return

  def _build_fn(self,directory,prefix,filename):
    return directory+"/"+prefix+filename

  def _beam_width_arcsec(self,image):
    if image.header is not None:
      bwidth=(image.header["BMIN"]+image.header["BMAJ"])/2.0
        # FIXME: assume that it is deg to arcsec
      return bwidth*3600.0
    else:
      return None

  def _beam_width_pixel(self,image):
    if image.header is not None:
      bwidth=(image.header["BMIN"]+image.header["BMAJ"])/2.0
      bwidth=bwidth/image.header["CDELT1"]

      return bwidth
    else:
      return None

  @property
  def species(self):
    '''
    Returns the molecular species from the fits file
    '''
    flineid=self.cube.header['P_LINEID']
    if flineid is not None and flineid!="":
      fspecies=(flineid.split()[0]).strip()
    else:
      fspecies+"Unknown"

    return fspecies

  @property
  def restfrq(self):
    '''
    Restfrequency of the line in GHz
    '''
    return self.cube.header['RESTFRQ']/1.e9

  @property
  def restwl(self):
    '''
    Restwavelength of the line in micrometer
    '''
    return (self.restfrq*u.GHz).to(u.micron,equivalencies=u.spectral()).value


class CasaSimContinuum(CasaSim):
  """
  Data container for a CASA continuum simulation (observations).

  The class can be used to quickly read in a CASA simulation for a single
  spectral line. The main purpose is to read in the various different kind
  of observables which have been produced by CASA.

  Can deal with the following files wiht a given PREFIX
    - `PREFIX.contcube.fits` the spectral line cube
    - `PREFIX.cont.radial` the azimuthally average radial continuum profile

  During the init of this Class it is tried to read all this files. However, all of them are
  optional and the according attribute is set to `None` in case the file could not be read.

  """

  def __init__(self,fn_prefix,directory=".",distance=None,
               coordinates=None,
               fn_cube=".cube.fits",
               fn_radprof=".cube.radial"):
    """
    Parameters
    ----------

    fn_prefix : str
      the prefix used for all files the routine try to read

    directory :
      the directory with the files (optional)

    distance : float
      the distance of the target (optional).
      Try to fread it from the fits file in case of synthetic ProDiMo observations

    coordinates : :class:`astropy.coordinates.sky_coordinate.SkyCoordinate`
      the coordinates of the target/object including the distance
      FIXME: Note used yet!

    fn* : string
      The fn* parameters can be use to change the filenames for the different files.


    Attributes
    ----------

    distance : float
      the distance of the target, will be passed to the other objects

    cube :class:`.ContinuumCube` :
      the continuum cube.

    radprof : :class:`..RadialProfile`
      the spectra profile

    """
    self.distance=distance
    self.fn_cube=self._build_fn(directory,fn_prefix,fn_cube)
    self.fn_radprof=self._build_fn(directory,fn_prefix,fn_radprof)

    # all files are optional ... so if they are not there set the attribute to zero
    found=False
    self.cube=None
    print(self.fn_cube)
    if os.path.isfile(self.fn_cube):
      self.cube=ContinuumCube(self.fn_cube)
      found=True

    self.radprof=None
    if os.path.isfile(self.fn_radprof):
      self.radprof=RadialProfile(self.fn_radprof,bwidth=self._beam_width_arcsec(self.integrated))
      found=True

    if not found: raise RuntimeError("No data found at all. Check the passed prefix!")
    return


class CASAImage(object):
  """
  Super class for an observable (CASA Simulation or real Observation) for image data including cubes.

  Should not be instantiated directly.
  Opens the fits file and initializes some helper attributes.

  """

  def __init__(self,filename=None):
    """
    Needs to be called from a subclass.

    Parameters
    ----------
    filename : str
      The file name of the fits file.

    centercoords : :class:`astropy.coordinates.sky_coordinate.SkyCoordinate`
      the desired center coordinates

    Attributes
    ----------
    header :
      the header of the fits file. It is just a reference to the fits header.

    data : array_like(float)
      the fits data. Assumes that is always the image data.

    btable : array_like
      an additioanl extension (table). Assumes that it is a table with beam date
      for e.g. a lie cube

    bmaj : float
      the major axis of the beam (same units as in the fits file)

    bmin : float
      the minor axis of the beam (same units as in the fits file)

    bPA : float
      the beam position angle

    centerpix : array_like(float,ndim=1)
      the pixel coordinates of the center (x and y coordinate)

    wcsabs : :class:`astropy.wcs.WCS`
      an absulte astropy world coordinate system (for the spatial coordinates).
      Can be used for plotting transformation.

    wcsrel : :class:`astropy.wcs.WCS`
      astropy world coordinate system (for the spatial coordinates) relative the
      the center of the image (`centerpix`)
      Can be used for plotting transformation.
      (see :func:`~prodimopy.read_casasim.CASAImage._linear_offset_coords`)

    """
    if filename is not None:  # otherwise assume the file was read already
      fitsdata=fits.open(filename)
      self.header=fitsdata[0].header
      self.data=fitsdata[0].data
      # is there something more
      # we always assume here it is a table with beam sizes and calculte
      if len(fitsdata)>1:
        self.btable=fitsdata[1].data
      else:
        self.btable=None

    if self.btable is not None:
      # calculate an average beam sizes
      # FIXME: that might not be always what somebody wants
      # FIXME assumes that the beam size is in arcsec (usually it is gegree)
      self.bmaj=np.average(self.btable.field(0))/3600.0
      self.bmin=np.average(self.btable.field(1))/3600.0
      self.bPA=np.average(self.btable.field(2))/3600.0
    else:
      self.bmaj=self.header["BMAJ"]
      self.bmin=self.header["BMIN"]
      self.bPA=self.header["BPA"]

    # this is all a bit strange but if it is even pixels now -1 is better
    # FIXME: this is not general
    # CRPIX doe not necessarely has to be the center pixel, it could be
    # that it is the first one (e.g. in the pv diagramm)
    # but this is not what I want, I think
    self.centerpix=[self.header["CRPIX1"],self.header["CRPIX2"]]
    self.centerpix[0]-=1
    self.centerpix[1]-=1

    self.wcsabs=wcs.WCS(self.header,naxis=2)

#    if centercoords is not None:
#      self.centerpix=centercoords.to_pixel(self.wcsabs.celestial,mode="wcs",origin=1)

    self.wcsrel=self._linear_offset_coords(self.wcsabs,self.centerpix)

  def _linear_offset_coords(self,wcsabs,center):
    """
    Returns a locally linear offset coordinate system.

    Given a 2-d celestial WCS object and a central coordinate, return a WCS
    that describes an 'offset' coordinate system, assuming that the
    coordinates are locally linear (that is, the grid lines of this offset
    coordinate system are always aligned with the pixel coordinates, and
    distortions from spherical projections and distortion terms are not taken
    into account)

    taken from: https://github.com/aplpy/aplpy/issues/8

    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
        The original WCS, which should be a 2-d celestial WCS
    center : array_like
        The pixel coordinates on which the offset coordinate system should be
        centered.
    """

    # Convert center to pixel coordinates
    # xp, yp = skycoord_to_pixel(center, wcs)

    # Set up new WCS
    new_wcs=wcs.WCS(naxis=2)
    # FIXME: do not know why +1 but otherwise the 0 points does not fit with the zero point in the pixel scale
    new_wcs.wcs.crpix=center[0]+1,center[1]+1
    new_wcs.wcs.crval=0.,0.
    # FIXME: assumbes that the units are in degree
    scale=proj_plane_pixel_scales(wcsabs)*3600.
    scale[0]=scale[0]*-1.0  # otherwise it is the wrong direction, that does not change the orientation of the image just the labels
    new_wcs.wcs.cdelt=scale
    new_wcs.wcs.ctype='XOFFSET','YOFFSET'
    new_wcs.wcs.cunit='arcsec','arcsec'

    return new_wcs

  def arcsectopix(self,xarcsec=None):
    xpixrel=int(xarcsec/self.wcsrel.wcs.cdelt[1])
    xpix=int(self.centerpix[1]-xpixrel)

    return xpix

  def cut(self,x=None,y=None,width=1,normalized=False):
    '''
    Make a cut along the given x or y coordinate in the image.

    x : float
      make a cut perpenticular to the x-axis a the given position x in arcsec (relative to the center).

    y : float
      make a cut perpenticular to the y-axis a the given position x. in arcsec (relative to the center).

    width :
      widht of the cut in pixels. The values are averaged. Must be an odd number

    normalized : boolean
      If `True` the cut is normalized the the peak.


    '''

    if x is not None:
      coords=np.arange(0,self.data.shape[0])
      coords=coords*self.wcsrel.wcs.cdelt[0]*-1.0  # FIXME: figure out why this is needed
      coords=coords-coords[int(self.centerpix[0])]

      xpixrel=int(x/self.wcsrel.wcs.cdelt[1])
      xpix=int(self.centerpix[1]-xpixrel)

#      print("Cut at x=",xpix)

      wh=int(width/2)
      if wh>0:
        vals=np.average(self.data[:,xpix-wh:xpix+wh],axis=1)
      else:
        vals=self.data[:,xpix]

    elif y is not None:
      coords=np.arange(0,self.data.shape[1])
      coords=coords*self.wcsrel.wcs.cdelt[1]
      coords=coords-coords[int(self.centerpix[1])]

      ypixrel=int(y/self.wcsrel.wcs.cdelt[0])
      ypix=int(self.centerpix[1]-ypixrel)

      wh=int(width/2)
      if wh>0:
        vals=np.average(self.data[ypix-wh:ypix+wh,],axis=0)
      else:
        vals=self.data[ypix,:]

    else:
      print("You have to provide only one coordinate x or y")
      return None

    if normalized:
#      print(vals)
      vals=vals/np.max(vals)

    return coords,vals

#  def __str__(self, *args, **kwargs):
#    return("BEAM(maj,min,PA): "+str(self.bmaj)+","+str(self.bmin)+","+str(self.bPA)+"\n"
#           "CENTERPIX: "+str(self.centerpix))


class LineCube(CASAImage):
  """
  The full line cube.
  """

  def __init__(self,filename,systemic_velocity=0.0):
    CASAImage.__init__(self,filename)

    self.systemic_velocity=systemic_velocity
    if self.header is not None:
      self.vel=self._init_vel()
    else:
      return None

  def _init_vel(self):
    """
    Converts the spectral coordinate to (radio) velocities.

    Currently assumes that the spectral coordinate is in units of Hz.

    FIXME: read unit from fits file

    FIXME: stolen from here ... https://github.com/astropy/astropy/issues/4529
    mabe not the best way to go

    FIXME: maybe could be generalized

    """
    wcsvel=wcs.WCS(self.header)
    xv=np.repeat(0,self.header['NAXIS3'])
    yv=np.repeat(0,self.header['NAXIS3'])
    zv=np.arange(self.header['NAXIS3'])

    wx,wy,wz=wcsvel.wcs_pix2world(xv,yv,zv,0)
    freq_to_vel=u.doppler_radio(self.header['RESTFRQ']*u.Hz)
    vel=(wz*u.Hz).to(u.km/u.s,equivalencies=freq_to_vel)

    return vel


class LineIntegrated(CASAImage):
  """
  Zeroth moment image (Integrated emission)
  """

  def __init__(self,filename,centercoords=None):
    CASAImage.__init__(self,filename)


class LineMom1(CASAImage):
  """
  First Moment image.
  """

  def __init__(self,filename,systemic_velocity=0.0):

    CASAImage.__init__(self,filename)

    self.systemic_velocity=systemic_velocity


class LinePV(CASAImage):
  """
  Position-Velocity diagramm.

  """

  def __init__(self,filename,systemic_velocity=0.0):

    CASAImage.__init__(self,filename)

    self.systemic_velocity=systemic_velocity

    # FIXME: CASA sets the centrpix for the velocity coordinate to a strange value
    # or to one, but I am here interested in the image center
    if self.centerpix[1]<=0:
      # FIXME: work only with odd numbers
      self.centerpix[1]=int(self.header["NAXIS2"]/2)


class LineSpectralProfile():
  """
  The spectral line profile.

  Reads a spectral profile produced with CASA.
  """

  def __init__(self,filename,systemic_velocity=0.0):
    data=np.loadtxt(filename)
    self.vel=data[:,3]
    self.flux=data[:,4]
    self.systemic_velocity=systemic_velocity
    return


class RadialProfile():
  """
  Azimuthally averaged radial intensity profile.

  Reads a file produced by the casa taks casairing.
  see https://www.oso.nordic-alma.se/software-tools.php

  """

  def __init__(self,filename,bwidth=None):
    radprof=np.loadtxt(filename)
    self.arcsec=radprof[:,0]
    self.flux=radprof[:,2]
    self.flux_err=radprof[:,3]
    self.bwidth=bwidth
    return


class Continuum(CASAImage):
  """
  A continuum image.

  """

  def __init__(self,filename):
    CASAImage.__init__(self,filename)


class ContinuumCube(CASAImage):
  """
  A series of continuum images

  Uses the output images from the ProDiMo continuum radiative transfer.
  Need to check if this also works with the CASA simulator.
  """

  def __init__(self,filename):
    if filename is not None:  # otherwise assume the file was read already
      fitsdata=fits.open(filename)
      self.header=fitsdata[0].header
      self.data=fitsdata[0].data
      self.btable=None
      # self.wl=fitsdata[1].data

    # print(self.wl)

    CASAImage.__init__(self,None)

