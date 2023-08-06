"""
.. module:: read
   :synopsis: Reads the output data of a ProDiMo model.

.. moduleauthor:: Ch. Rab


"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cProfile
from collections import OrderedDict
from collections.abc import MutableMapping
import glob
import io
import math
import os
from timeit import default_timer as timer

from astropy import constants as const
from astropy import units as u
import numpy
from scipy.interpolate import interp1d

import numpy as np
import prodimopy.chemistry.network as pcnet
import tarfile as tar


def _do_cprofile(func):
  """
  Simple profiling

  Taken from here: https://zapier.com/engineering/profiling-python-boss/

  Can be used via a decorator: i.e. place '@do_cprofile' before the method you want to profile.
  But please also remove it again after profiling.
  """

  def profiled_func(*args,**kwargs):
      profile=cProfile.Profile()
      try:
          profile.enable()
          result=func(*args,**kwargs)
          profile.disable()
          return result
      finally:
          profile.print_stats(sort='time')

  return profiled_func


class Data_ProDiMo(object):
  """
  Data container for most of the output produced by |prodimo|.

  The class also includes some convenience functions and also derives/calculates
  some addtionialy quantities not directly included in the |prodimo| output.

  """

  def __init__(self,name):
    """

    Parameters
    ----------
    name : string
      The name of the model (can be empty).

    Attributes
    ----------

    """

    self.name=name
    """ string :
    The name of the model (can be empty)
    """
    self.directory=None
    """ string :
    The directory from which the model was read.
    Is e.g. set by :meth:`~prodimopy.read.read_prodimo`
    Can be a relative path.
    """
    self.__fpFlineEstimates=None  # The path to the FlineEstimates.out File
    self.__tarfile=None
    self.params=None
    """ :class:`prodimopy.read.ModelParameters`
    Dictionary that allows to acces the models Parameters from Parameter.out.
    """
    self.nx=None
    """ int :
    The number of spatial grid points in the x (radial) direction
    """
    self.nz=None
    """ int :
    The number of spatial grid points in the z (vertical) direction
    """
    self.nspec=None
    """ int :
      The number of chemical species included in the model.
    """
    self.nheat=None
    """ int :
      The number of heating processes included in the model.
    """
    self.ncool=None
    """ int :
      The number of cooling processes included in the model.
    """
    self.p_dust_to_gas=None
    """ float :
      The global dust to gass mass ratio (single value, given Parameter)
    """
    self.mstar=None
    """ float :
      The stellar mass in solar units.
      is taken from ProDiMo.out
    """
    self.x=None
    """ array_like(float,ndim=2) :
    The x coordinates (radial direction).
    `UNIT:` au, `DIMS:` (nx,nz)
    """
    self.z=None
    """ array_like(float,ndim=2) :
    The z coordinates (vertical direction).
    `UNIT:` au, `DIMS:` (nx,nz)
    """
    self.vol=None
    """ array_like(float,ndim=2) :
    The volume for each grid point
    `UNIT:` |cm^3|, `DIMS:` (nx,nz)
    """
    self.rhog=None
    """ array_like(float,ndim=2) :
    The gas density.
    `UNIT:` |gcm^-3|, `DIMS:` (nx,nz)
    """
    self.rhod=None
    """ array_like(float,ndim=2) :
    The dust density.
    `UNIT:` |gcm^-3|, `DIMS:` (nx,nz)
    """
    self.d2g=None
    """ array_like(float,ndim=2) :
    The dust to gas mass ratio form ProDiMo
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.sdg=None
    """ array_like(float,ndim=2) :
    The gas vertical surface density. This is for only one half of the disk
    (i.e. from z=0 to z+), like in |prodimo|. For the total surface density multiply by two.
    `UNIT:` |gcm^-2|, `DIMS:` (nx,nz)
    """
    self.sdd=None
    """ array_like(float,ndim=2) :
    The dust vertical surface density. This is for only one half of the disk
    (i.e. from z=0 to z+), like in |prodimo|. For the total surface density multiply by two.
    `UNIT:` |gcm^-2|, `DIMS:` (nx,nz)
    """

    self.nHtot=None
    """ array_like(float,ndim=2) :
    The total hydrogen number density.
    `UNIT:` |cm^-3|, `DIMS:` (nx,nz)
    """
    self.muH=None
    """ float :
    The conversion constant from nHtot to rhog
    It is assume that this is constant throught the disk. It is given by
    by `rhog/nHtot`
    `UNIT:` `g`
    """
    self.NHver=None  #
    """ array_like(float,ndim=2) :
    Vertical total hydrogen column density. `nHtot` is integrated from the disk
    surface to the midplane at each radial grid point. The intermediate results
    are stored at each grid point. For example NHver[:,0] gives the total column
    density as a function of radius.
    `UNIT:` |cm^-2|, `DIMS:` (nx,nz)
    """
    self.NHrad=None  #
    """ array_like(float,ndim=2) :
    Radial total hydrogen column density. Integrated along radial rays, starting
    from the star. Otherwise same behaviour as `NHver`.
    `UNIT:` |cm^-2|, `DIMS:` (nx,nz)
    """
    self.nd=None
    """ array_like(float,ndim=2) :
    The dust number density.
    `UNIT:` |cm^-3|, `DIMS:` (nx,nz)
    """
    self.tg=None
    """ array_like(float,ndim=2) :
    The gas temperature.
    `UNIT:` K, `DIMS:` (nx,nz)
    """
    self.td=None
    """ array_like(float,ndim=2) :
    The dust temperature.
    `UNIT:` K, `DIMS:` (nx,nz)
    """
    self.pressure=None
    """ array_like(float,ndim=2) :
    The gas pressure
    `UNIT:` |ergcm^-3|, `DIMS:` (nx,nz)
    """
    self.soundspeed=None
    """ array_like(float,ndim=2) :
    The isothermal sound speed.
    `UNIT:` |kms^-1|, `DIMS:` (nx,nz)
    """
    self.damean=None
    """ array_like(float,ndim=2) :
    The mean dust particle radius
    `UNIT:` micron, `DIMS:` (nx,nz)
    """
    self.Hx=None
    """ array_like(float,ndim=2) :
    The X-ray energy deposition rate per hydrogen nuclei
    `UNIT:` erg <H>\ :sup:`-1`, `DIMS:` (nx,nz)
    """
    self.zetaX=None
    """ array_like(float,ndim=2) :
    X-ray ionisation rate per hydrogen nuclei.
    `UNIT:` |s^-1|, `DIMS:` (nx,nz)
    """
    self.zetaCR=None  #
    """ array_like(float,ndim=2) :
    Cosmic-ray ionisation rate per molecular hydrogen (H2)
    `UNIT:` |s^-1|, `DIMS:` (nx,nz)
    """
    self.zetaSTCR=None
    """ array_like(float,ndim=2) :
    Stellar energetic particle ionisation rate per H2
    `UNIT:` |s^-1|, `DIMS:` (nx,nz)
    """
    self.tauX1=None
    """ array_like(float,ndim=2) :
    Radial optical depth at 1 keV (for X-rays).
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.tauX5=None
    """ array_like(float,ndim=2) :
    Radial optical depth at 5 keV (for X-rays).
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.tauX10=None
    """ array_like(float,ndim=2) :
    Radial optical depth at 10 keV (for X-rays).
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.AVrad=None
    """ array_like(float,ndim=2) :
    Radial visual extinction (measerd from the star outwards).
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.AVver=None
    """ array_like(float,ndim=2) :
    Vertical visual extinction (measured from the disk surface to the midplane).
    `UNIT:`, `DIMS:` (nx,nz)
    """
    self.AV=None
    """ array_like(float,ndim=2) :
    Given by min([AVver[ix,iz],AVrad[ix,iz],AVrad[nx-1,iz]-AVrad[ix,iz]])
    Gives the lowest visiual extinction at a certain point. Where it is assumed radiation
    can escape either vertically upwards, radially inwards or radially outwards.
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.nlam=None
    """ int :
    The number of wavelength bands used in the continuum radiative transfer.
    """
    self.lams=None
    """ array_like(float,ndim=1) :
    The band wavelengths considered in the radiative transfer.
    \n`UNIT:` microns, `DIMS:` (nlam)
    """
    self.radFields=None
    """ array_like(float,ndim=3) :
    Radiation field (mean intensity) for each wavelength band.
    `UNIT:` erg |s^-1| |cm^-2| |sr^-1| |Hz^-1|, `DIMS:` (nx,nz,nlam)
    """
    self.chi=None
    """ array_like(float,ndim=2) :
    Geometrial UV radiation field in units of the Drain field.
    `UNIT:` Draine field, `DIMS:` (nx,nz)
    """
    self.chiRT=None
    """ array_like(float,ndim=2) :
    UV radiation field as properly calculated in the radiative transfer, in units of the Drain field.
    `UNIT:` Draine field, `DIMS:` (nx,nz)
    """
    self.kappaRos=None
    """ array_like(float,ndim=2) :
    Rosseland mean opacity. In case of gas radiative transfer for the dust plus the gas.
    `UNIT:` |cm^-1|, `DIMS:` (nx,nz)
    """
    self.tauchem=None
    """ array_like(float,ndim=2) :
    Chemical timescale (steady-state)
    `UNIT:` yr, `DIMS:` (nx,nz)
    """
    self.taucool=None
    """ array_like(float,ndim=2) :
    Cooling timescale.
    `UNIT:` yr, `DIMS:` (nx,nz)
    """
    self.taudiff=None
    """ array_like(float,ndim=2) :
    Vertical radiative diffussion timescale (using the Rosseland mean opacities).
    `UNIT:` yr, `DIMS:` (nx,nz)
    """
    self.spnames=None  #
    """ dictionary :
    Dictionary providing the index of a particular species (e.g. spnames["CO"]). This index
    can than be used for arrays having an species dimension (like nmol). The electron is included.
    `UNIT:` , `DIMS:` (nspec)
    """
    self.solved_chem=None
    """ array_like(int,ndim=2) :
    Flag for chemistry solver (values, 0,1,2) (see ProDiMo code)
    1 means everything okay, 0 failure, 2 time-dependent step needed
    DIMS:` (nx,nz)
    """
    self.nmol=None
    """ array_like(float,ndim=3) :
    Number densities of all chemical species (mainly molecules)
    `UNIT:` |cm^-3|, `DIMS:` (nx,nz,nspec)
    """
    self.cdnmol=None
    """ array_like(float,ndim=3) :
    Vertical column number densities for each chemical species at each point in the disk.
    Integrated from the surface to the midplane at each radial grid point.
    `UNIT:` |cm^-2|, `DIMS:` (nx,nz,nspec)
    """
    self.rcdnmol=None
    """ array_like(float,ndim=3) :
    Radial column number densities for each species at each point in the disk.
    Integrated from the star outwards along fixed radial rays given by the vertical grid.
    `UNIT:` |cm^-2|, `DIMS:` (nx,nz,nspec)
    """
    self.rateH2form=None
    """ array_like(float,ndim=3) :
    The H2 formation ratio
    `UNIT:` |s^-1|, `DIMS:` (nx,nz)
    """
    self.rateH2diss=None
    """ array_like(float,ndim=3) :
    The different H2 dissociation rates.
    `UNIT:` |s^-1|, `DIMS:` (nx,nz,3)
    """
    self.heat=None
    """ array_like(float,ndim=3) :
    Heating rates for the various heating processes. `TODO:` unit
    `UNIT:` ?? `DIMS:` (nx,nz,nheat)
    """
    self.cool=None
    """ array_like(float,ndim=3) :
    Cooling rates for the various coling. `TODO:` unit.
    `UNIT:` ??  `DIMS:` (nx,nz,ncool)
    """
    self.heat_names=None
    """ list (string)
    All the names of the cooling processes.
    """
    self.cool_names=None
    """ list (string)
    All the names of the cooling processes.
    """
    self.heat_mainidx=None
    """ array_like(float,ndim=3) :
    Index of the main heating process at the given grid point.
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.cool_mainidx=None
    """ array_like(float,ndim=3) :
    Index of the main cooling process at the given grid point.
    `UNIT:` , `DIMS:` (nx,nz)
    """
    self.lineEstimates=None
    """ list(:class:`prodimopy.read.DataLineEstimate`) :
    All the line estimates from FlineEstimates.out. Each spectral line in FlineEstimates
    corresponds to one :class:`prodimopy.read.DataLineEstimate` object.
    """
    self.lines=None
    """ array_like(:class:`prodimopy.read.DataLine`) :
    Alle the spectral lines from line_flux.out (proper Linetransfer).
    Each spectral line in line_flux.out corresponds to
    one :class:`prodimopy.read.DataLine` object
    """
    self.sed=None  # the spectral energy distribution (from proper ray tracing)
    """ :class:`prodimopy.read.DataSED` :
    The Spectral Energy Distribution for the model (SED) as calculated in the
    radiative transfer with ray tracing.
    see :class:`prodimopy.read.DataSED` for details.
    """
    self.contImages=None
    """ :class:`prodimopy.read.DataContinuumImages` :
    Reads the continuum images data (image.out) if available.
    The full images are only read if requested for a particular wavelength
    see :class:`prodimopy.read.DataContinuumImages` for details.
    """
    self.starSpec=None
    """ :class:`prodimopy.read.DataStarSpec` :
    The (unattenuated) stellar input spectrum.
    see :class:`prodimopy.read.DataStarSpec` for details.
    """
    self.gas=None
    """ :class:`prodimopy.read.DataGas` :
    Holds various properties of the gas component (e.g. opacities).
    see :class:`prodimopy.read.DataGas`
    """
    self.dust=None
    """ :class:`prodimopy.read.DataDust` :
    Holds various properties of the dust component (e.g. opacities).
    see :class:`prodimopy.read.DataDust`
    """
    self.env_dust=None  # dust properties for the envelope structure see :class:`prodimopy.read.DataDust`
    """ :class:`prodimopy.read.DataDust` :
    Holds various properties of the dust component (e.g. opacities) of the envelope.
    Only relevant if |prodimo| is used in the envelope mode.
    see :class:`prodimopy.read.DataDust`
    """
    self.elements=None
    """ :class:`prodimopy.read.DataElements` :
    Holds the initial gas phase element abundances
    """
    self.species=None
    """ :class:`prodimopy.read.DataSpecies` :
    Holds the initial species data
    """
    self.sedObs=None
    """ :class:`prodimopy.read.DataContinuumObs` :
    Holds the provided SED observations (photometry, spectra, extinction etc.)
    TODO: maybe put all the observations into one object (e.g. also the lines)
    """
    self.lineObs=None
    """ :class:`prodimopy.read.DataLineObs` :
    Holds the provide line observations (e.g. LINEObs.dat and line profiles)
    TODO: maybe put all the observations into one object (e.g. also the lines)
    """
    self.FLiTsSpec=None
    """ :class:`prodimopy.read.DataFLiTsSpec` :
    Holds the FLiTs spectrum if it exists.
    """
    self.chemnet=None
    """ :class:`prodimopy.chemistry.network.ReactionNetworkPout` :
    Holds the used chemical network of the model from Reactions.out. Is only read on demand.
    """
    self._log=True
    """ boolean
    Allows to switch off some log statements (not consistently implemented yet)
    """

    # this are some cache variables for lazy initialization. Using them allows to do
    # certain calculations only if the quantities are accessed (used)
    #
    self._cool_cache=None
    self._heat_cache=None
    self._radFields_cache=None
    self._nmol_cache=None
    self._sdg=None
    self._sdd=None
    self._vol=None
    self._cdnmol=None
    self._rcdnmol=None
    self._chemnet=None

  @property
  def nmol(self):
    if self._nmol_cache is not None:
      self._nmol=np.array(self._nmol_cache,dtype=np.float)
      # remove the cache now
      self._nmol_cache=None
    return self._nmol

  @nmol.setter
  def nmol(self,value):
    self._nmol=value

  @property
  def cdnmol(self):
    if self._cdnmol is None:
      _calc_cdnmol(self)
    return self._cdnmol

  @cdnmol.setter
  def cdnmol(self,value):
    self._cdnmol=value

  @property
  def rcdnmol(self):
    if self._rcdnmol is None:
      _calc_rcdnmol(self)
    return self._rcdnmol

  @rcdnmol.setter
  def rcdnmol(self,value):
    self._rcdnmol=value

  @property
  def sdg(self):
    if self._sdg is None:
      calc_surfd(self)
    return self._sdg

  @sdg.setter
  def sdg(self,value):
    self._sdg=value

  @property
  def sdd(self):
    if self._sdd is None:
      calc_surfd(self)
    return self._sdd

  @sdd.setter
  def sdd(self,value):
    self._sdd=value

  @property
  def cool(self):
    if self._cool_cache is not None:
      self._cool=np.array(self._cool_cache,dtype=np.float)
      # remove the cache now
      self._cool_cache=None
    return self._cool

  @cool.setter
  def cool(self,value):
    self._cool=value

  @property
  def heat(self):
    if self._heat_cache is not None:
      self._heat=np.array(self._heat_cache,dtype=np.float)
      # remove the cache now
      self._heat_cache=None
    return self._heat

  @heat.setter
  def heat(self,value):
    self._heat=value

  @property
  def radFields(self):
    if self._radFields_cache is not None:
      self._radFields=np.array(self._radFields_cache,dtype=np.float)
      # remove the cache now
      self._radFields_cache=None
    return self._radFields

  @radFields.setter
  def radFields(self,value):
    self._radFields=value

  @property
  def vol(self):
    if self._vol is None:
      _calc_vol(self)
    return self._vol

  @vol.setter
  def vol(self,value):
    self._vol=value

  @property
  def chemnet(self):
    if self._chemnet is None:
      self._chemnet=pcnet.ReactionNetworkPout(name=self.name,modeldir=self.directory)
    return self._chemnet

  @chemnet.setter
  def chemnet(self,value):
    self._chemnet=value

  def __str__(self):
    output="Info ProDiMo.out: \n"
    output+="NX: "+str(self.nx)+" NZ: "+str(self.nz)+" NSPEC: "+str(self.nspec)
    output+=" NLAM: "+str(self.nlam)+" NCOOL: "+str(self.ncool)+" NHEAT: "+str(self.nheat)
    output+="\n"
    output+="p_dust_to_gas: "+str(self.p_dust_to_gas)
    return output

  def _getLineIdx(self,wl,ident=None):
    if self.lines==None: return None

    wls=numpy.array([line.wl for line in self.lines])

    if ident!=None:
      linestmp=[line for line in self.lines if line.ident==ident]
      if linestmp is not None and len(linestmp)>0:
        wlstmp=numpy.array([line.wl for line in linestmp])
        itmp=numpy.argmin(abs(wlstmp[:]-wl))
        # get the index of the whole line array. That should no find
        # the exact one (e.g. used the exact same wavelength
        idx=numpy.argmin(abs(wls[:]-linestmp[itmp].wl))
        # print(self.lines[idx].ident)
        # check again
        # FIXME: causes problems with _lte lines (have the same wavelenghts)
        if self.lines[idx].ident!=ident:
          print("ERROR: Something is wrong found: ident",self.lines[idx].ident," and wl ",self.lines[idx].wl,
                "for ",ident,wl)
          return None
        else:
          return idx
      else:
        print("WARN: No line found with ident",ident," and wl ",wl)
        return None
    else:
      idx=numpy.argmin(abs(wls[:]-wl))

      if (abs(wls[idx]-wl)/wl)>0.01:
        print("WARN: No line found within 1% of the given wavelengeth:",wl)
        return None
      else:
        return idx

  def getLine(self,wl,ident=None):
    '''
    Returns the spectral line closest to the given wavelentgh.

    Parameters
    ----------
    wl : float
      the wavelength which is used for the search. `UNIT:` micron.
    ident : string, optional
      A line identification string which should also be considered for the
      search. (default: `None`)

    Returns
    -------
    :class:`prodimopy.read.DataLine`
      Returns `None` if no lines are included in the model.

    '''

    idx=self._getLineIdx(wl,ident=ident)

    if idx is None:
      return None
    else:
      return self.lines[idx]

  def gen_specFromLineEstimates(self,wlrange=[10,15],ident=None,specR=3000,
                                unit="W",contOnly=False,noCont=False):
    '''
    Generates a "Spectrum" from the line estimates results of ProDiMo and
    convolves it to the given spectral resolution.
    If the SED was also calculated the line fluxes will be added to the continuum,
    if not a continuum of zero flux is assumed.

    This routine can become very slow, depending on the number of lines
    within a given wavelenght range. It can be more efficient to produce smaller
    chuncks with not so many lines.

    Parameters
    ----------
    wlrange : array_like
      Generate the spectrum in the wavelength range [start,end]
      Default: `[10,15]` Units: micron

    ident : str
      only the lines with this ident (like given in the line estimates) are
      considered. Default: `None` (all lines in the given wlrange are considered)

    specR : int
      the desired spectral resolution. If `None` a spectrum with simple the
      line fluxes added (i.e. as "delta function") is returned.
      Default: `3000`

    unit : str
      desired unit for the output. Current choices `W` (W/m^2/Hz) or 'Jy' (Jansky.
      `W` is the default option.

    contOnly : boolean
      only do it for the continuum (do not add any other lines).
      Default: `False`

    noCont : boolean
      assume zero continuum
      Default: `False`

    Returns
    -------
    (tuple):
      tuple containing: wls(array_like): array of wavelenght points in micron,
      flux(array_like): flux values for each wavelenght point in |Wm^-2Hz^-1|
      or Jy (depending on the `unit` parameter)

    '''
    import astropy.convolution as conv

    startT=timer()

    lmin=wlrange[0]/1.e4
    lmax=wlrange[1]/1.e4
    R=1.e6
    if specR!=None and specR>(0.1*R):
      print("WARN: requested spectral resolution is too high use "+str(0.1*R)+" instead")

    # technical spectral resolution

    # determine the number of points required
    del_loglam=np.log10(1.0+1.0/R)  # log(lam+dlam)-log(lam)
    N=1+int(np.log10(lmax/lmin)/del_loglam)

    mwlsline=np.logspace(np.log10(lmin),np.log10(lmax),N)

    if self.sed==None or noCont==True:
      contfluxline=mwlsline*0.0  # no continuum
    else:
      contfluxline=np.interp(mwlsline,self.sed.lam/1.e4,self.sed.fnuErg)

    # do everything in cgs units
    confac=(1.0*(u.W/(u.m**2))).to(u.erg/u.s/(u.cm**2)).value
    lineest=self.selectLineEstimates(ident=ident,wlrange=wlrange)
    print("INFO: gen_specFromLineEstimates: build spectrum for "+
          str(len(lineest))+" lines ...")
    # this loop is taking most of the time , not the convolution.
    # I guess that could still be faster, but that mighte require a lot more
    # memory
#     from tqdm import tqdm
#     for line in tqdm(lineest):
    tonu=const.c.cgs.value/R
    for line in lineest:
      wlcm=line.wl/1.e4
      # Find the closes wavelength point in the new grid.

      # idx=np.argmin(np.abs(mwlsline-wlcm))
      # this does the same as above but seems to be 10 times faster
      idx=np.argmax(mwlsline>(wlcm))
      if (mwlsline[idx]-wlcm)>(wlcm-mwlsline[idx-1]):
        idx-=1

      # like in the idl script
      # R=mwlsline[idx]/(mwlsline[idx]-mwlsline[idx-1])
      # print(R)
      # just use delta functions -> line profile is a delta function
      if not contOnly:
        if specR is None:
          contfluxline[idx]=contfluxline[idx]+(line.flux*confac)
        else:
          dnu=tonu/wlcm
          contfluxline[idx]=contfluxline[idx]+(line.flux*confac)/dnu

    print("INFO: gen_specFromLineEstimates: convolve spectrum ...")

    if specR is None:
      FWHMpix=1.0
      mwlslinez=mwlsline
      contfluxline_conv=contfluxline
    else:
      # in the idl script this is interpreted as the FWHM,
      # but the convolution routine wants stddev use relation
      # FWHM=2*sqrt(2ln2)*stddev=2.355/stddev
      # this should than be consistent with the result from the
      # ProDiMo idl script
      FWHMpix=R/specR
      g=conv.Gaussian1DKernel(stddev=FWHMpix/2.355,factor=7)

      # Convolve data
      contfluxline_conv=conv.convolve(contfluxline,g)
      # print(z)
      # remove beginning and end ... strange values
      cut=2*int(FWHMpix)
      contfluxline_conv=contfluxline_conv[cut:(len(contfluxline_conv)-cut)]
      mwlslinez=mwlsline[cut:(len(mwlsline)-cut)]

    # now downgrade the grid to something reasonable
    outwls=np.linspace(np.min(mwlslinez),np.max(mwlslinez),int(len(mwlsline)/FWHMpix)*5)
    outflux=np.interp(outwls,mwlslinez,contfluxline_conv)

    outflux=outflux/confac
    if unit=="Jy":
      outflux=(outflux*u.W/u.m**2/u.Hz).to(u.Jy).value

    print("INFO: time: ","{:4.2f}".format(timer()-startT)+" s")

    return outwls*1.e4,outflux

  def getLineEstimate(self,ident,wl):
    '''
    Finds and returns the line estimate for the given species closest
    to the given wavelength.

    Parameters
    ----------
    ident : string
      The line identification string.
    wl : float
      the wavelength which is used for the search. `UNIT:` micron.

    Returns
    -------
    :class:`prodimopy.read.DataLineEstimate`
      Returns `None` if the line is not found.

    Notes
    -----
      The parameters of this method are not consistent
      with :meth:`~prodimopy.read.Data_ProDiMo.getLine`. This might be confusing.
      However, there is a reasong for this. The number of
      included line estimates in a |prodimo| model can be huge and just searching
      with the wavelenght might become slow. However, this probably can be improved.

      To speed up the reading of `FlineEstimate.out` the extra radial info
      (see :class:`~prodimopy.read.DataLineEstimateRInfo` of all the line estimates
      is not read. However, in this routine it is read for the single line estimate
      found. One should use this routine to access the radial info for a single line estimate.
    '''
    found=-1
    i=0
    mindiff=1.e20

    if self.lineEstimates is None:
      print("WARN: No lineEstimates are inluced (or not read) for this model.")
      return None

    # print ident, wl
    for le in self.lineEstimates:
      if le.ident==ident:
        diff=abs(le.wl-wl)
        if diff<mindiff:
          found=i
          mindiff=diff
      i=i+1

    if self.lineEstimates[found].rInfo==None:
      _read_lineEstimateRinfo(self,self.lineEstimates[found])

    return self.lineEstimates[found]

  def selectLineEstimates(self,ident,wlrange=None):
    """
    Returns a list of all line estimates (i.e. all transitions) for the
    given line ident and/or in the given wavelength range.

    Parameters
    ----------
    ident : string
      The line identification (species name) as defined in |prodimo|.
      The ident is not necessarely equal to the underlying chemial species
      name (e.g. isotopologues, ortho-para, or cases like N2H+ and HN2+).
      If wlrange is set ident can be `None` in that case all lines in the given
      wlrange are returned.

    wlrange : array_like
      All lines in the given wavelength range [start,end] and the given ident
      are returned. if the ident is `None` all lines are returned.
      Default: `None` Units: micron

    Returns
    -------
    list(:class:`prodimopy.read.DataLineEstimate`) :
      List of :class:`prodimopy.read.DataLineEstimate` objects, or empty list if nothing was found.

    Notes
    -----
    In this routine the additional radial information of the line esitmate
    (see :class:`~prodimopy.read.DataLineEstimateRInfo`) is not read.


    Examples
    --------

    .. code-block:: python

      # select all line estimates for CO
      lests=model.selectLineEstimates("CO")

      # select only the 1300 micron CO line
      lests=model.selectLineEstimates("CO",wlrange=[1300,1310])

      # select all linest in the given wavelength range
      lests=model.selectLineEstimates(None,wlrange=[1200,1400])

      # print all of them to see what we got
      for lest in lests:
        print(lest)

    """
    lines=list()
    if wlrange is None:
      for le in self.lineEstimates:
        if le.ident==ident:
          lines.append(le)
    else:
      # TODO: this might can be done more efficient
      for le in self.lineEstimates:
        if le.wl>=wlrange[0] and le.wl<=wlrange[1]:
          if ident is None or le.ident==ident:
            lines.append(le)

    return lines

  def selectLines(self,ident):
    """
    Returns a list of all line fluxes included in the line tranfer, for the given line ident.

    Parameters
    ----------
    ident : string
      The line identification (species name) as defined in |prodimo|.
      The ident is not necessarely equal to the underlying chemial species
      name (e.g. isotopologues, ortho-para, or cases like N2H+ and HN2+)

    Returns
    -------
    list(:class:`prodimopy.read.DataLine`) :
      List of :class:`prodimopy.read.DataLine` objects,
      or empty list if nothing was found.

    """
    if self.lines is None: return None

    lines=list()
    for le in self.lines:
      if le.ident==ident:
        lines.append(le)

    return lines

  def getAbun(self,spname):
    '''
    Returns the abundance for a given species.

    Parameters
    ----------
    spname : string
      The name of the chemical species as define in |prodimo|.

    Returns
    -------
    array_like(float,ndim=2)
      an array of dimension [nx,nz] with species abundance or `None` if the species was not found.

    Notes
    -----
      The abundance is given relative to the total hydrogen nuclei density
      (i.e. ``nmol(spname)/nHtot``)

      A warning is printed in case the species was not found in spnames.
    '''
    # check if it exists
    if not spname in self.spnames:
      print("WARN: getAbun: Species "+spname+" not found.")
      return None

    return self.nmol[:,:,self.spnames[spname]]/self.nHtot

  def get_toomreQ(self,mstar=None):
    '''
    Returns the Toomre Q parameter as a function of radius.
    (for the midplane).

    Q is given by

    Q(r)=k(r)*cs(r)/(pi * G * sigma(r))

    for k we use the keplerian frequency, cs is the soundspeed (from the mdoel)
    and sigma is the total gas surface density (both halfs of the disk).

    Parameters
    ----------
    mstar : float
      The stellar mass in solar units (optional).
      If `None` the value from the model is taken.

    Returns
    -------
    array_like(float,ndim=1)
      an array of dimension [nx] with the Q param
    '''
    if mstar is None:
      mstar=self.mstar

    mstarc=(mstar*u.M_sun).cgs.value
    grav=const.G.cgs.value
    r=(self.x[:,0]*u.au).cgs.value
    # isothermal soundspeed
    cs=(self.soundspeed[:,0]*u.km/u.s).cgs.value
    # surface density factor two for both half of the disks
    sigma=2.0*(self.sdg[:,0]*u.g/u.cm**2).cgs.value

    # assuem keplerian rotation for Epicyclic frequency
    kappa=np.sqrt(grav*mstarc/r**3)
    Q=kappa*cs/(math.pi*grav*sigma)

    return Q

  def getSEDAnaMask(self,lam):
    '''
    Returns a numpy mask where only the grid points outside the emission
    origin area for the given wavelength (continuum) are marked as invalid.

    This mask can be used in e.g. :func:`~prodimopy.read.Data_ProDiMo.avg_quantity`

    .. warning::

        in case of optically thin emission only the points of one half
        of the disk are considered. In that case an average quantity of this
        box(mask) will not be completely correct.

    Parameters
    ----------
    lam : float
      the wavelength for which the emission origin region should be determined:
      UNITS: micron

    Returns
    -------
    array_like(float,ndim=2)
      Numpy mask with `DIMS:` (nx,nz)

    '''
    sedAna=self.sed.sedAna
    x15=interp1d(sedAna.lams,sedAna.r15,bounds_error=False,fill_value=0.0,kind="linear")(lam)
    x85=interp1d(sedAna.lams,sedAna.r85,bounds_error=False,fill_value=0.0,kind="linear")(lam)

    mask=numpy.ones(shape=(self.nx,self.nz))
    for ix in range(self.nx):
      if self.x[ix,0]>=x15 and self.x[ix,0]<=x85:
        z85=interp1d(sedAna.lams,sedAna.z85[:,ix],bounds_error=False,fill_value=0.0,kind="linear")(lam)
        z15=interp1d(sedAna.lams,sedAna.z15[:,ix],bounds_error=False,fill_value=0.0,kind="linear")(lam)
        for iz in range(self.nz):
          if self.z[ix,iz]<=z15 and self.z[ix,iz]>=z85:
            mask[ix,iz]=0

    return mask

  def getLineOriginMask(self,lineEstimate):
    '''
    Returns a numpy mask where the grid points outside the emission
    origin area for the given `lineEstimate` are marked as invalid.

    This mask can be used in e.g. :func:`~prodimopy.read.Data_ProDiMo.avg_quantity`

    Parameters
    ----------
    lineEstimate : :class:`prodimopy.read.DataLineEstimate`
      a line Estimate object for which the operation should be done

    Returns
    -------
    array_like(float,ndim=2)
      Numpy mask with `DIMS:` (nx,nz)
    '''
    fcfluxes=np.array([x.Fcolumn for x in lineEstimate.rInfo])

    Fcum=fcfluxes[:]
    for i in range(1,self.nx):
      Fcum[i]=Fcum[i-1]+fcfluxes[i]

    interx=interp1d(Fcum/Fcum[-1],self.x[:,0])
    x15=interx(0.15)
    x85=interx(0.85)

    mask=numpy.ones(shape=(self.nx,self.nz))
    for ix in range(self.nx):
      if (self.x[ix,0]>=x15 and self.x[ix,0]<=x85):
        for iz in range(self.nz):
          rinfo=lineEstimate.rInfo[ix]
        # print(rinfo.z15,rinfo.z85)
          if self.z[ix,iz]<=rinfo.z15 and self.z[ix,iz]>=rinfo.z85:
            mask[ix,iz]=0

    return mask

  def get_VKep(self,mstar=None,type=2):
    '''
    Returns the Keplerian rotation velocity [km/s] as a function
    of radius and height (same as in ProDiMo)


    Type 1: vkep=sqrt((G* mstar) / r)
    Type 2: vkep=sqrt((G* mstar * x**2) / r**3)
    Type 3: with pressure gradient (see Rosenfeld+ 2013)

    Parameters
    ----------
    mstar : float
      The stellar mass in solar units (optional).
      If `None` the value from the model is taken.

    Returns
    -------
    array_like(float,ndim=1)
      Rotation velocity [km/s]
    '''
    if mstar is None:
      mstar=self.mstar

    mstarc=(mstar*u.M_sun).cgs.value
    grav=const.G.cgs.value

    tocm=((1*u.au).to(u.cm)).value
    r=numpy.sqrt(self.x**2+self.z**2)*tocm

    if type==1:
      # FIXMEL Should be radius, but to be consisten do it like this.
      # but check again
      vkep=numpy.sqrt(grav*mstarc/(self.x*tocm))
    else:
      vrot2=(grav*mstarc*(self.x*tocm)**2)/r**3

      if type==2:  # standard in ProDiMo
        vkep=np.sqrt(vrot2)
      elif type==3:  # include the pressure term
        # pressuregradient like Rosenfeld+ 2013
        dp=self.x*0.0
        for iz in range(self.nz):
          # this is used in e.g. Rosenfeld et al 2013 and others
          dp[:,iz]=numpy.gradient(self.pressure[:,iz],self.x[:,iz]*tocm)
          # this we use in ProDiMo currently I think that is correct
          # doesn't seem to much of a difference
          # dp[:,iz]=numpy.gradient(self.pressure[:,iz],r[:,iz])
        vkep=numpy.sqrt(vrot2+(self.x*tocm)/self.rhog*dp)
      else:
        vkep=np.sqrt(vrot2)

    vkep=((vkep*u.cm/u.s).to(u.km/u.s)).value
    return vkep

  def get_KeplerOmega(self,mstar=None):
    '''
    Returns the Keplerian orbital frequency [1/s]
    (for the midplane).

    omega=sqrt(G*mstar/r**3)

    Parameters
    ----------
    mstar : float
      The stellar mass in solar units (optional).
      If `None` the value from the model is taken.

    Returns
    -------
    array_like(float,ndim=1)
      Keplerian orbital frequency as function of radius [1/s]
    '''
    if mstar is None:
      mstar=self.mstar

    mstarc=(mstar*u.M_sun).cgs.value
    grav=const.G.cgs.value
    r=(self.x[:,0]*u.au).cgs.value

    # assuem keplerian rotation for Epicyclic frequency
    omega=np.sqrt(grav*mstarc/r**3)

    return omega

  def int_ring(self,quantity,r1=None,r2=None):
    '''
    Integrates the given quantitiy (needs to be a function of r) from
    rin to rout.

    No interpolation is done. Simply the nearest neighbour for rin and rout
    are taken.

    The integration is done in cgs units and also the return value is in cgs units.

    For example if the total gas surfacedensity is passed this routine gives the disk mass.
    (if r1=rin and r2=rout).

    Parameters
    ----------
    quantity : array_like(float,ndim=1)
      the quantity to average. `DIMS:` (nx).
    r1: float
      inner radius [au].
      optional DEFAULT: inner disk radius
    r2: float
      inner radius [au].
      optional DEFAULT: outer disk radius
    '''

    if r1 is None:
      r1idx=0
    else:
      r1idx=np.argmin(np.abs(self.x[:,0]-r1))

    if r2 is None:
      r2idx=self.nx-1
    else:
      r2idx=np.argmin(np.abs(self.x[:,0]-r2))

    print("INFO: Integrate from "+
          "{:8.4f} ({:4d})".format(self.x[r1idx,0],r1idx)+" au to "+
          "{:8.4f} ({:4d})".format(self.x[r2idx,0],r2idx)+" au")

    r=(self.x[:,0]*u.au).to(u.cm).value
    out=2.0*math.pi*np.trapz(quantity[r1idx:r2idx+1]*r[r1idx:r2idx+1],x=r[r1idx:r2idx+1])

    return out

  def avg_quantity(self,quantity,weight="gmass",weightArray=None,mask=None):
    '''
    Calculates the weighted mean value for the given field (e.g. td).
    Different weights can be used (see `weight` parameter)

    Parameters
    ----------
    quantity : array_like(float,ndim=2)
      the quantity to average. `DIMS:` (nx,nz).

    weight : str
      option for the weight. Values: `gmass` (gass mass) `dmass` (dust mass) or
      `vol` (Volume). DEFAULT: `gmass`

    weightArray : array_like(float,ndim=2)
      Same dimension as `quantity`. If `weightArray` is not `None` it is used
      as the weight for calculating the mean value.

    mask : array_like(boolean,ndim=2)
      A mask with the same dimension as `quantity`. All elements with `True` are
      masked, i.e. not considered in the average (see numpy masked_array).
      For example one can pass the result of :meth:`~prodimopy.read.getLineOriginMask`
      to calculate average quantities over the emitting region of a line.


    Examples
    --------

    Here is an example for making a mass weighted average for the gas temperature in the main
    line emitting region for the CO 1.3 mm line.  `model` is the model data read with
    :func:`~prodimopy.read.read_prodimo`.

    .. code-block:: python

      avgtg=model.avg_quantity(model.tg,weight="gmass",
                         mask=model.getLineOriginMask(model.getLineEstimate("CO",1300.)))

    '''
    vol=np.ma.masked_array(self.vol,mask=mask)
    quantitym=np.ma.masked_array(quantity,mask=mask)

    if weightArray is not None:
      wA=np.ma.masked_array(weightArray,mask=mask)
      mean=np.sum(np.multiply(wA,quantitym))
      return mean/np.sum(wA)
    else:
      if weight=="vol":
        mean=np.sum(np.multiply(vol,quantitym))
        return mean/np.sum(vol)
      else:
        if weight=="dmass":
          rho=np.ma.masked_array(self.rhod,mask=mask)
        else:
          rho=np.ma.masked_array(self.rhog,mask=mask)

        mass=np.multiply(vol,rho)
        mean=np.sum(np.multiply(mass,quantitym))
        mean=mean/np.sum(mass)
        return mean


class ModelParameters(MutableMapping):
  '''
  Access to the Parameters of a model. Reads Parameter.out and provides
  some utiliy functions fo access a Parameters


  .. todo::
    * Currently all Parameters are strings. make type conversions.
    * provide utility functions to access special Parameters
    * maybe inherit from Dictionary class and mat custom getters

  '''

  def __init__(self,filename="Parameter.out",directory="."):
    """
    Opens the file and fills a dictrionary with all Parameters.
    This dictionary cannot be changed anymore. One can only read the parameters.
    The get routine has some special treatment for certain parameters, but does
    not do any type converting. Except that list separated with "," will be returned
    a lists.

    .. todo::

      things like `SPNOERASE= 30*"         "` not interpreted yet

    Parameters
    ----------
    filename : string
      The Filename of the Parameter file.

    directory : string
      The directory the contains the ProDiMo model output.


    """
    self.mapping={}
    # self.update(data)

    fparams,fpath=_getfile(filename,directory=directory)

    lines=fparams.readlines()
    # print(lines)

    # some special treatment as it seems that arrays can be written out in fortran
    # over multiple lines .... properly an error in how the  namelist is written, but could not fix it
    # (might also be just gfortran issue
    # very stupid
    for i in range(4,len(lines)-1,1):
      if "=" not in lines[i]: continue
      fields=lines[i].split("=")
      fields[1]=fields[1].strip()
      # check if there are more values in the next line
      if "=" not in lines[i+1]:
        fields[1]+=lines[i+1].strip()
      # the last character should always be a , don't need that
      self.mapping[fields[0].strip()]=(fields[1][:-1]).strip()

    # for line in fparams:
    #   fields=line.split("=")
    #   if len(fields)<2: continue
    #   self.mapping[fields[0].strip()]=fields[1].strip()

  def __getitem__(self,key):
    value=self.mapping[key.upper()]

      # asssume that this is an array, do the splitting
    if "," in value:
      values=value.split(",")
      values=[val.strip() for val in values]
      values=[val[1:-1].strip() if val.startswith('"') else val for val in values]

      # some special treatments ... because we do not know the length of that array
      if key.upper()=="AGE_DISK":
        nage=int(self.mapping["N_AGE"])
        return values[0:nage]
      else:
        return values

    # get rid of the " " for strings
    if value.startswith('"'):
      value=value[1:-1]
    return value

  def __delitem__(self,key):
    print("Don't delete Parameters ...")

  def __setitem__(self,key,value):
    print("Don't update Parameters ...")
    # if key in self:
    #     del self[self[key]]
    # if value in self:
    #     del self[value]
    # self.mapping[key]=value
    # self.mapping[value]=key

  def __iter__(self):
    return iter(self.mapping)

  def __len__(self):
    return len(self.mapping)


class DataLineProfile():
  """
  Data container for a spectral line profile for a single spectral line.
  """

  def __init__(self,nvelo,restfrequency=None):
    """
    Attributes
    ----------

    """
    self.nvelo=nvelo
    """ int :
    number of velocity points of the profile.
    """
    self.restfrequency=restfrequency
    """ float :
    the restfrequency of the line. Usefull for conversoins. Optional.
    `UNIT:` GHz
    """
    self.velo=numpy.zeros(shape=(self.nvelo))
    """ array_like(float,ndim=1) :
    The velocity grid of the line profile.
    `UNIT:` kms/s, `DIMS:` (nvelo)
    """
    self._flux=numpy.zeros(shape=(self.nvelo))
    """ array_like(float,ndim=1) :
    The flux at each velocity point.
    `UNIT:` Jy, `DIMS:` (nvelo)
    """
    self._flux_dust=numpy.zeros(shape=(self.nvelo))
    """ array_like(float,ndim=1) :
    The flux of the dust at each velocity
    `UNIT:` Jy, `DIMS:` (nvelo)
    """
    self._flux_conv=numpy.zeros(shape=(self.nvelo))
    """ array_like(float,ndim=1) :
    The convolved flux at each velocity point.
    `UNIT:` Jy, `DIMS:` (nvelo)
    """
    self._flux_unit="Jy"
    """ str :
    Set the unit which should be used to return the flux (can be switched)
    Current options: `Jy` and `ErgAng` (erg/s/cm^2/Ang)
    Default: `Jy` other current options  meaning
    """

  @property
  def flux(self):
    if self.flux_unit=="ErgAng":
      return (self._flux*u.Jy).to(u.erg/u.s/u.cm**2/u.angstrom,
                        equivalencies=u.spectral_density(self.restfrequency*u.GHz)).value
    else:
      return self._flux

  @flux.setter
  def flux(self,val):
    self._flux=val

  @property
  def flux_dust(self):
    if self.flux_unit=="ErgAng":
      return (self._flux_dust*u.Jy).to(u.erg/u.s/u.cm**2/u.angstrom,
                        equivalencies=u.spectral_density(self.restfrequency*u.GHz)).value
    else:
      return self._flux_dust

  @flux_dust.setter
  def flux_dust(self,val):
    self._flux_dust=val

  @property
  def flux_conv(self):
    if self.flux_unit=="ErgAng":
      return (self._flux_conv*u.Jy).to(u.erg/u.s/u.cm**2/u.angstrom,
                        equivalencies=u.spectral_density(self.restfrequency*u.GHz)).value
    else:
      return self._flux_conv

  @flux_conv.setter
  def flux_conv(self,val):
    self._flux_conv=val

  @property
  def frequency(self):
    '''
    The frequencies according to the velocity grid. Is relative to the
    restfrequency.
    `UNIT:` GHz

    FIXME: restfreq can be None ...
    FIXME: There is some risk that this is slow, but should not be use very often

    '''
    return (self.velo*u.km/u.s).to(u.GHz,
                                   equivalencies=u.doppler_optical(self.restfrequency*u.GHz)).value

  @property
  def fluxErgAng(self):
    '''
    The fluxes in units of erg/s/cm^2/Angstrom.

    FIXME: Deprecated

    FIXME: needs frequency which breaks if restfrequency is None
    FIXME: There is some risk that this is slow, but should not be used very often
    FIXME: now just takes the restfrequency for conversion which is not correct
    however for the continuum we also take the restfrequency as we have only one value
    Usually this does not introduce a signficant error.
    '''
    return (self._flux*u.Jy).to(u.erg/u.s/u.cm**2/u.angstrom,
                        equivalencies=u.spectral_density(self.restfrequency*u.GHz)).value

  @property
  def flux_unit(self):
    return self._flux_unit

  @flux_unit.setter
  def flux_unit(self,val):

    if val!="Jy" and val!="ErgAng":
      raise ValueError("flux unit not supported")
    self._flux_unit=val

  def convolve(self,R):
    '''
    Convolves the given profile to the spectrayl resolution R.
    The profile is convolved with a Gaussian where R determines the FWHM of that
    Gaussian.

    The results are stored in `flux_conv`

    Parameters
    ----------

    R : float
      the spectral resolution.

    Returns
    -------
    float :
      The FWHM of the Gaussian in units of `km/s` i.e. the spectral resolution.
    '''

    facFWHM=2.355  # for getting the FWHM of a gaussian (i.e. stddev to FWHM

    if R is None or R<=0.0:
      self._flux_conv=self._flux
      return

    delta_v=(const.c/R).to(u.km/u.s).value
    delta_v=delta_v/facFWHM  # need stdv for the  gaussian but R is interpreted as the FWHM

    gaussian=np.exp(-(self.velo)**2./(2.*delta_v**2.))

    # FIXME: does not work if the continuum is not removed
    # also the 0 micht not be the continuum
    flux=self._flux[:]-self._flux[0]

    norm=np.trapz(flux,self.velo)
    flux_convolved=np.convolve(flux,gaussian,'same')
    flux_convolved*=norm/np.trapz(flux_convolved,self.velo)

    self._flux_conv=flux_convolved+self._flux[0]
    return delta_v*facFWHM

  def __str__(self):
    return "nvelo: "+str(self.nvelo)


class DataLine(object):
  """
  Data container for a single spectral line read from `line_flux.out`.
  """

  def __init__(self):
    '''
    Attributes
    ----------

    '''
    self.wl=0.0
    """ float :
    Restwavelenght of the line. UNIT: `micron`
    """
    self.frequency=0.0
    """ float :
    Restfrequency of the line. UNIT: `GHz`
    """
    self.prodimoInf=""
    """ string :
    Some information String from PRoDiMo (i.e. transition)
    """
    self.species=""
    """ string :
    The chemical species of the line. Identical to ident.
    """
    self.ident=""
    """ string :
    The identification of the line (i.e. as given in `LineTransferList.in`)
    """
    self.flux=0.0
    """ float:
    The integrated line flux. UNIT: `W/m^2`
    """
    self.fcont=0.0
    """ float:
    The continuum flux at the line position. UNIT: Jy
    """
    self.profile=None
    """ :class:`prodimopy.read.DataLineProfile` :
    The line profile for this particular line.
    """
    self.distance=None
    """ float :
    The distance use for the line calculations. UNIT: pc
    """
    self.inclination=None
    """ float :
    The inclination use for the line calculations. UNIT: deg
    """

  def __str__(self):
    text=(self.species+"/"+
          self.prodimoInf+"/"+
          self.ident+"/"+
          str(self.wl)+"/"+
          str(self.frequency)+"/"+
          str(self.flux)+"/"+
          str(self.fcont))
    return text

  @property
  def flux_Jy(self):
    '''
    The flux of the line in  Jansky km |s^-1|.
    '''
    return _flux_Wm2toJykms(self.flux,self.frequency)

  @property
  def fcontErgAng(self):
    '''
    The flux of the continuum in erg/s/cm^2/Angstrom
    '''

    return (self.fcont*u.Jy).to(u.erg/u.s/u.cm**2/u.angstrom,
                        equivalencies=u.spectral_density(self.frequency*u.GHz)).value

  @property
  def luminosityErgs(self):
    '''
    Returns the luminosity in erg/s
    '''
    return ((self.luminosityWatt*u.Watt).to(u.erg/u.s)).value

  @property
  def luminosityWatt(self):
    '''
    Returns the line luminosity in Watt
    '''
    return (4.0*math.pi*(self.distance*u.pc).to(u.m)**2*self.flux*u.Watt/u.m**2).value


class DataLineObs(DataLine):
  '''
  Holds the observational data for one line.
  '''

  def __init__(self,flux,flux_err,fwhm,fwhm_err,flag):
    super(DataLineObs,self).__init__()
    self.flux=flux
    self.flux_err=flux_err
    self.fwhm=fwhm
    self.fwhm_err=fwhm_err
    self.flag=flag.lower()
    self.profile=None
    self.profileErr=None


class DataFLiTsSpec(object):
  '''
  Data container for a FLiTs spectrum.
  Currently provides only the wavelength grid and the flux in Jy, as produced
  by FLiTs.
  '''

  def __init__(self):
    self.wl=None
    """ array_like :
    Wavelength grid in micron.
    """
    self.flux=None
    """ array_like :
    Flux in Jy.
    """

  def convolve(self,specR,sample=1):
    '''
    Returns a convolved version of the Spectrum.
    Does not change the original FLiTs spectrum.

    Parameters
    ----------
    specR : int
      The desired spectral resolution.

    Returns
    -------
    (tuple):
      tuple containing: wls(array_like): array of wavelenght points in micron,
      flux(array_like): flux values for each wavelenght point in Jansky.


    .. todo::

      allow for different units.
    '''

    print("INFO: convolve FLiTs spectrum ... ")

    from astropy.convolution import convolve_fft
    from astropy.convolution import Gaussian1DKernel

    wl=self.wl
    flux=self.flux

    # Make a new wl grid
    wl_log=np.logspace(np.log10(np.nanmin(wl)),np.log10(np.nanmax(wl)),num=np.size(wl)*sample)

    # Find stddev of Gaussian kernel for smoothing
    # taken from here https://github.com/spacetelescope/pysynphot/issues/78
    R_grid=(wl_log[1:-1]+wl_log[0:-2])/(wl_log[1:-1]-wl_log[0:-2])/2
    sigma=np.median(R_grid)/specR
    if sigma<1:
      sigma=1

    # Interpolate on logarithmic grid
    f_log=np.interp(wl_log,wl,flux)

    # in the idl script this is interpreted as the FWHM,
    # but the convolution routine wants stddev use relation
    # FWHM=2*sqrt(2ln2)*stddev=2.355/stddev
    # this should than be consistent with the result from the
    # ProDiMo idl script
    gauss=Gaussian1DKernel(stddev=sigma/2.355)
    flux_conv=convolve_fft(f_log,gauss)

    # Interpolate back on original wavelength grid
    flux_sm=np.interp(wl,wl_log,flux_conv)

    cut=2*int(sigma)
    flux_smc=flux_sm[cut:(len(flux_sm)-cut)]
    wlc=wl[cut:(len(wl)-cut)]

    return wlc,flux_smc


class DataLineEstimate(object):
  '''
  Data container for a single line estimate.
  '''

  def __init__(self,ident,wl,jup,jlow,flux):
    """
    Parameters
    ----------
    ident : string
    wl : float
    jup : int
    jlow : int
    flux : float

    """""
    self.ident=ident
    """ string :
      The line identifications (species)
    """
    self.wl=wl
    """ float :
      The wavelength of the line.
      `UNIT: micron`
    """
    self.jup=jup
    """ int :
    Upper level as defined in ProDiMo ((not the real one!)
    """
    self.jlow=jlow
    """  int :
    Lower level as defined in ProDiMo (not the real one!).
    """
    self.flux=flux
    self.rInfo=None
    """ :class:`prodimopy.read.DataLineEstimateRinfo`
      The extra radial information of the line.
    """
    self.__posrInfo=None  # stores the position of the radial information to access is later on

  @property
  def frequency(self):
    '''
    Frequency of the line in [GHz].
    '''
    return (self.wl*u.micrometer).to(u.GHz,equivalencies=u.spectral()).value

  @property
  def flux_Jy(self):
    '''
    The flux of the line Jansky km |s^-1|
    '''
    return _flux_Wm2toJykms(self.flux,self.frequency)

  def __str__(self):
    text=(self.ident+"/"+
          str(self.wl)+"/"+
          str(self.jup)+"/"+
          str(self.jlow)+"/"+
          str(self.flux))
    return text


class DataLineEstimateRInfo(object):
  '''
  Data container for the extra radial info for a single line estimate.
  '''

  def __init__(self,ix,iz,Fcolumn,tauLine,tauDust,z15,z85):
    self.ix=ix
    self.iz=iz
    self.Fcolumn=Fcolumn
    self.tauLine=tauLine
    self.tauDust=tauDust
    self.z15=z15
    self.z85=z85


class DataGas(object):
  '''
  Holds the data for the gas (mainly from dust_opac.out)
  TODO: currently only the init cs is read, not the x,y data
  '''

  def __init__(self,nlam):
    self.nlam=nlam
    self.lam=numpy.zeros(shape=(nlam))
    self.energy=numpy.zeros(shape=(nlam))  # for convinence as often energy is also used for gas [eV]
    self.abs_cs=numpy.zeros(shape=(nlam))  # unit cm^2/H
    self.sca_cs=numpy.zeros(shape=(nlam))  # unit cm^2/H


class DataDust(object):
  '''
  Holds the data for the dust (mainly from dust_opac.out)
  TODO: dust composition is not yet read

  Attributes
  ----------

  '''

  def __init__(self,amin,amax,apow,nsize,nlam):
    self.amin=amin
    ''' float :
      The minimum grain size of the size distribution. `UNIT:` micron
    '''
    self.amax=amax
    ''' float :
      The maximum grain size of the size distribution. `UNIT:` micron
    '''
    self.apow=apow
    ''' float :
      The powerlaw exponent of the grain size distribution.
    '''
    self.nsize=nsize
    ''' int :
      The number for grain size bins
    '''
    self.lam=numpy.zeros(shape=(nlam))
    ''' array_like(float,ndim=1) :
      The wavelength grid for the dust opacities. UNIT: `micron`
    '''
    self.energy=numpy.zeros(shape=(nlam))
    ''' array_like(float,ndim=1) :
      The energy grid for the dust opacities. UNIT: `eV`
      For convinience (i.e. for the X-ray regime)
      TODO: check the unit
    '''
    self.kext=numpy.zeros(shape=(nlam))  # in cm^2 g^-1
    ''' array_like(float,ndim=1) :
      The dust extinction coefficient for each wavelength per g of dust. UNIT: `|cm^2g^-1|`
    '''
    self.kabs=numpy.zeros(shape=(nlam))
    ''' array_like(float,ndim=1) :
      The dust absorption coefficient for each wavelength per g of dust. UNIT: `|cm^2g^-1|`
    '''
    self.ksca=numpy.zeros(shape=(nlam))
    ''' array_like(float,ndim=1) :
      The dust scattering coefficient for each wavelength per g of dust. `UNIT: `|cm^2g^-1|`
    '''
    self.ksca_an=numpy.zeros(shape=(nlam))  # tweaked anisotropic scattering
    ''' array_like(float,ndim=1) :
      The dust anisotropic (approximation) scattering coefficient for each wavelength per g of dust. UNIT: `|cm^2g^-1|`
    '''
    # FIXME: not read by default yet, might not exist so do not init
    self.asize=None
    ''' array_like(float,ndim=1) :
      The grain size for each size bin. `UNIT:` micron
    '''
    self.sigmaa=None
    ''' array_like(float,ndim=2) :
      The radial surface density (g cm^-2) profiles for each individual grain.
      size (shape=[nsize,nr]. Might not exit!
    '''


class DataElements(object):
  '''
  Data for the Element abundances (the input).

  Holds the data from `Elements.out`.

  The data is stored as OrderedDict with the element names as keys.

  Attributes
  ----------
  '''

  def __init__(self):
    self.abun=OrderedDict()
    """
    OrderedDict :
      Ordered Dictionary holding the element abundaces realtive to hydrogen
    """
    self.abun12=OrderedDict()
    """
    OrderedDict :
      abundances in the +12 unit
    """
    self.massRatio=OrderedDict()
    """
    OrderedDict :
      mass ratios
    """
    self.amu=OrderedDict()
    """
    OrderedDict :
      atomic mass unit
    """
    self.muHamu=None
    """
    float :
      rho = muH*n<H> with muH/amu = muHamu
      see the Elements.out file
    """

  def __str__(self):

    output="name   12    X/H\n"
    for key  in self.abun12.keys():
      output=output+"{:3s}".format(key)+" "+"{:6.3f}".format(self.abun12[key])+" "+"{:6.3e}".format(self.abun[key])+"\n"
    return output


class DataSpecies(object):
  '''
  Data for the Species (the input).

  Holds the data from `Species.out`.

  The data is stored as OrderedDict with the element names as keys.

  Attributes
  ----------
  '''

  def __init__(self):
    self.mass=OrderedDict()
    """
    OrderedDict(float) :
      The mass of the species `UNIT:` g.
    """
    self.charge=OrderedDict()
    """
    OrderedDict(int) :
      The mass of the species `UNIT:` g.
    """

    self.chemPot=OrderedDict()
    """
    OrderedDict(float) :
      chemical potential as determined by ProDiMo.
    """

  def get_spdata(self,name):
    '''
    Returns all data of the species with `name`.

    Parameters
    ----------

    name : str or int
      The name of the species.
      if int then use it as index

    Returns
    -------

    (mass,charge,chemPot)

    '''
    if isinstance(name,int):
      return (list(self.mass.values())[name],
              list(self.charge.values())[name],
              list(self.chemPot.values())[name])
    else:
      return (self.mass[name],self.charge[name],self.chemPot[name])

  def __str__(self):
    output="Number of species: "+str(len(self.mass.keys()))+"\n"
    output+="Name mass [g] charge chemPot [eV]\n"
    for name,mass,charge,chemPot in zip(self.mass.keys(),self.mass.values(),self.charge.values(),self.chemPot.values()):
      output+="{:<15s} {:7.2e} {:5d} {:12.4f}".format(name,mass,charge,chemPot)+"\n"
    return output


class DataContinuumObs(object):
  '''
  Holds the observational data for the continuum (the dust).

  Holds the photometric data, spectra (experimental) and radial profiles
  (experimental).

  '''

  def __init__(self,nlam=None):
    if nlam is not None:
      self.nlam=nlam
      self.lam=numpy.zeros(shape=(nlam))
      self.nu=numpy.zeros(shape=(nlam))
      self.fnuErg=numpy.zeros(shape=(nlam))
      self.fnuJy=numpy.zeros(shape=(nlam))
      self.fnuErgErr=numpy.zeros(shape=(nlam))
      self.fnuJyErr=numpy.zeros(shape=(nlam))
      self.flag=numpy.empty(nlam,dtype="U2")
    else:
      self.nlam=None
      self.lam=None
      self.nu=None
      self.fnuErg=None
      self.fnuJy=None
      self.fnuErgErr=None
      self.fnuJyErr=None
      self.flag=None

    self.specs=None  # holds a list of spectra if available (wl,flux,error)
    self.R_V=None
    self.E_BV=None
    self.A_V=None

    self.radprofiles=None


class DataSED(object):
  '''
  Holds the data for the Spectral Energy Distribution (SED).
  '''

  def __init__(self,nlam,distance,inclination):
    self.nlam=nlam
    self.distance=distance
    self.inclination=inclination

    # the bolometric luminosity will be calculated by integrating over the whole
    # frequency range, considering also the distance)
    # units are Solar luminosities
    self.Lbol=None
    # is also calculated in read_sed
    self.Tbol=None
    self.lam=numpy.zeros(shape=(nlam))
    self.nu=numpy.zeros(shape=(nlam))
    self.fnuErg=numpy.zeros(shape=(nlam))
    self.nuFnuW=numpy.zeros(shape=(nlam))
    self.fnuJy=numpy.zeros(shape=(nlam))
    # self.nuFnu = numpy.zeros(shape=(nlam))

    # the analysis data
    self.sedAna=None

  def setLbolTbol(self):
    """
    Calculates the bolometric temperature and lumionsity for the given
    values of the SED.

    quite approximate at the moment.
    """

    # FIXME: correctness needs to be verified
    # caluclate the bolometric luminosity
    # *-1.0 because of the ordering of nu
      # calculate Tbol see Dunham 2008 Equation 6
    # check what is here the proper value
    # in particular Tbol is very sensitive to this value
    # Lbol does not seem to change much (e.g. if 0.1 is used instead)
    # for the moment exclude the shortest wavelength as these is most likely scattering
    mask=self.lam>0.2

    self.Lbol=numpy.trapz(self.fnuErg[mask],x=self.nu[mask])*-1.0
    self.Lbol=self.Lbol*4.0*math.pi*(((self.distance*u.pc).to(u.cm)).value)**2
    self.Lbol=self.Lbol/(const.L_sun.cgs).value

    # print(numpy.trapz((sed.nu*sed.fnuErg),x=sed.nu))
    # print(numpy.trapz(sed.fnuErg,x=sed.nu))
    self.Tbol=1.25e-11*numpy.trapz((self.nu[mask]*self.fnuErg[mask]),x=self.nu[mask])/numpy.trapz(self.fnuErg[mask],x=self.nu[mask])


class DataSEDAna(object):
  '''
  Holds the analysis data for the Spectral Energy Distribution (SEDana.out).
  '''

  def __init__(self,nlam,nx):
    self.lams=numpy.zeros(shape=(nlam))
    self.r15=numpy.zeros(shape=(nlam))
    self.r85=numpy.zeros(shape=(nlam))
    self.z15=numpy.zeros(shape=(nlam,nx))
    self.z85=numpy.zeros(shape=(nlam,nx))


class DataContinuumImages(object):
  '''
  Holds the continuum images (image.out) and provides a method to read
  one particular image.

  The coordinates x,y are the same for all images, and only stored once.

  '''

  def __init__(self,nlam,nx,ny,filepath="./image.out"):
    self.nlam=None
    """ int:
    The number of wavelenthpoint (== number of images)
    """
    self.lams=numpy.zeros(shape=(nlam))
    """ array_like(float,ndim=1) :
    The wavelengths
    `UNIT:` micron, `DIMS:` (nlam)
    """
    self.nx=nx
    """ int:
    The number of x axis points (radial) of the image
    """
    self.ny=ny
    """ int:
    The number of y axis points (or theta) of the image
    """
    self.x=numpy.zeros(shape=(nx,ny))
    """ array_like(float,ndim=2) :
    x coordindates
    `UNIT:` au, `DIMS:` (nx,ny)
    """
    self.y=numpy.zeros(shape=(nx,ny))
    """ array_like(float,ndim=2) :
    y coordindates
    `UNIT:` au, `DIMS:` (nx,ny)
    """
    self._filepath=filepath

  def getImage(self,wl):
    '''
    Reads the intensities at a certain wavelength (image) from the image.out
    file.

    The image with the closest wavelength to the given wavelength (wl) will be
    returned

    Parameters
    ----------
    wl : float
    the wavelength in micron of the requested image

    Returns
    -------
    tuple : (array_like(float,ndim=2),float) :
    the image intensitis in units ... (dimension nx,ny) and the wavelength
    '''
    idx=numpy.argmin(numpy.abs(self.lams-wl))

    # read the colum according the the wavelength, first 4 columns are
    # ix,iz, x, y ... not required here
    intens=numpy.loadtxt(self._filepath,skiprows=6,usecols=4+idx)

    return intens.reshape((self.nx,self.ny)),self.lams[idx]


class DataBgSpec(object):
  '''
  Backgound field input spectrum
  '''

  def __init__(self,nlam):
    self.nlam=nlam
    self.lam=numpy.zeros(shape=(nlam))
    self.nu=numpy.zeros(shape=(nlam))
    self.Inu=numpy.zeros(shape=(nlam))


class DataStarSpec(object):
  '''
  Stellar input spectrum.

  '''

  def __init__(self,nlam,teff,r,logg,luv):
    """
    Attributes
    ----------

    """
    self.nlam=nlam
    self.teff=teff
    self.r=r
    self.logg=logg
    self.luv=luv
    self.lam=numpy.zeros(shape=(nlam))
    """ array_like(float,ndim=1) :
    wavelength unit : micron
    """
    self.nu=numpy.zeros(shape=(nlam))
    """ array_like(float,ndim=1) :
    frequency unit : Hz
    """
    self.Inu=numpy.zeros(shape=(nlam))
    """ array_like(float,ndim=1) :
    Intensitye unit: erg/cm2/s/Hz/sr
    """


class Chemistry(object):
  """
  Data container for chemistry analysis.
  Holds the information for one particular molecule.

  """

  def __init__(self,name):
    """
    Parameters
    ----------
    name : string
      The name of the model (can be empty).
    Attributes
    ----------

    """
    self.name=name
    """ string :
    The name of the model (can be empty)
    """
    self.totfrate=None
    """ array :
    Total formation rate at each spatial grid point.
    """
    self.totdrate=None
    """ array :
    Total destruction rate at each spatial grid point.
    """
    self.gridf=None
    """ array :
    Contains for each individual grid point a sorted list of the formation reactions including the index (0) and the rate (1)
    """
    self.gridd=None
    """ array :
    Contains for each individual grid point a sorted list of the destruction reactions including the index (0) and the rate (1)
    """
    self.fridxs=None
    """ array :
    List of all formation reaction indices for this species.
    """
    self.dridxs=None
    """ array :
    List of all destruction reaction indices for this species.
    """
    self.species=None
    """ str :
    name of species for which the chamanalysis should be done
    """
    self.chemnet=None
    """ :class:`prodimopy.chemistry.network.ReactionNetworkPout`
    array with nx,ny,species index, reaction number, and reaction rate
    for a given species
    """

  def reac_to_str(self,reac,idx,rate=None):
    '''
    Converts a Reaction to the outputformat we want for the chemanalysis.

    Parameters
    ----------
    reac : :class:`prodimopy.chemistry.network.Reaction`

    '''
    # build the prods string assuming max three products
    reacstr="".join(["{:13s}".format(p) for p in reac.reactants])
    reacstr+="".join(["{:13s}".format("") for p in range(3-len(reac.reactants))])
    prodstr="".join(["{:13s}".format(p) for p in reac.products])
    prodstr+="".join(["{:13s}".format("") for p in range(4-len(reac.products))])
    if rate is not None:
      ratestr="{:10.2e}".format(rate)
    else:
      ratestr=""
    return "{:7d} {:7d} {:2s} {} -> {} {}".format(idx,reac.id,reac.type,reacstr,prodstr,ratestr)

  def get_reac_grid(self,level,rtype):
    '''
    Gets the counting index of the `x`  important Reaction. If it does not exist
    it is set to 0.

    Parameters
    ----------

    level : int
      The level of important `1` meand most important, `2` second most important etc.

    type : str
      Formation (pass `f`) or destruction Reaction (pass `d`)


    Returns
    -------
    tuple :
      And array of shape (model.nx,model.nz) where the first one containts the index
      of the Reactions for the list of reactions from chemanalysis (the outputfile)
      and the second one the rate itself (for this Reaction at each point).

    '''
    if rtype=="d":
      grid=self.gridd
      ridxs=self.dridxs
    else:
      grid=self.gridf
      ridxs=self.fridxs

    nx=grid.shape[0]
    nz=grid.shape[1]

    gidx=np.zeros(shape=(nx,nz),dtype=int)
    grate=np.zeros(shape=(nx,nz))
    for ix in range(nx):
      for iz in range(nz):
        idxs=grid[ix,iz,0]

        if len(idxs)<level:
          val=0
          rate=0.0
        else:
          val=list(ridxs).index(idxs[level-1])+1
          rate=grid[ix,iz,1][level-1]

        gidx[ix,iz]=val
        grate[ix,iz]=rate

    return gidx,grate


def read_prodimo(directory=".",name=None,readlineEstimates=True,readObs=True,
                 readImages=True,filename="ProDiMo.out",
                 filenameLineEstimates="FlineEstimates.out",
                 filenameLineFlux="line_flux.out",
                 td_fileIdx=None):
  '''
  Reads in all (not all yet) the output of a ProDiMo model from the given model directory.

  Parameters
  ----------
  directory : str
    the directory of the model (optional).
  name : str
    an optional name for the model (e.g. can be used in the plotting routines)
  readlineEstimates : boolean
    read the line estimates file (can be slow, so it is possible to deactivate it)
  readObs : boolean
    try to read observational data (e.g. SEDobs.dat ...)
  filename : str
    the filename of the main prodimo output
  filenameLineEstimates : str
    the filename of the line estimates output
  filenameLineFlux : str
    the filename of the line flux output
  td_fileIdx : str
    in case of time-dependent model the index of a particular output age can be provided (e.g. "03")


  Returns
  -------
  :class:`prodimopy.read.Data_ProDiMo`
    the |prodimo| model data or `None` in case of errors.
  '''
  # FIXME: tha reading in via a tar file still needs some work, disable it here for the momen
  # should be a parameter of this routine at some point
#  tarfile : string
#    the path to an e.g. tar file (also compressed, everything which works with the python tarfile).
#    The routine tries to read the files from the archive also considering the `directory` path

  # TODO define this properly
  filenameFLiTs="specFLiTs.out"
  startAll=timer()

  tarfile=None

  # guess a name if not set
  if name==None:
    if directory==None or directory=="." or directory=="":
      dirfields=os.getcwd().split("/")
    else:
      dirfields=directory.split("/")

    name=dirfields[-1]

  # if td_fileIdx is given alter the filenames so that the timedependent
  # files can be read. However this would actually also workd with other kind
  # of indices as td_fileIdx is a strong
  if td_fileIdx!=None:
    rpstr="_"+td_fileIdx+".out"
    filename=filename.replace(".out",rpstr)
    filenameLineEstimates=filenameLineEstimates.replace(".out",rpstr)
    filenameLineFlux=filenameLineFlux.replace(".out",rpstr)
    filenameFLiTs=filenameFLiTs.replace(".out",rpstr)

  f,dummy=_getfile(filename,directory,tarfile)

  # FIXME: with this the calling rouinte can continue
  # The calling routine has to take care of that
  # But this is not very nice
  if f is None: return None

  # read all date into the memory
  # easier to handle afterwards
  lines=f.readlines()
  f.close()

  # start of the array data block
  idata=24

  data=Data_ProDiMo(name)

  data.directory=directory

  # Read first the species, because only from there I can know if the electron
  # is included as Species or not
  # data is filled in the routine
  data.species=read_species(directory,tarfile=tarfile)
  if data.species is not None:  # None should not happen
    data.nspec=len(data.species.mass)

  data.mstar=float(lines[0].split()[1])
  data.p_dust_to_gas=float(lines[9].split()[1])

  strs=lines[21].split()
  data.nx=int(strs[1])
  data.nz=int(strs[2])
  # is not set in read_species() FIXME: not nice
  nspecreal=int(strs[3])
  if data.nspec is None:  # should not happen
    print("WARN: Setting data.nspec, because there is no Species.out")
    data.nspec=nspecreal+1  # +1 for the electron
  data.nheat=int(strs[4])
  data.ncool=int(strs[5])
  data.nlam=int(strs[6])

  # TODO: move this to the constructure which takes nx,nz
  data.x=numpy.zeros(shape=(data.nx,data.nz))
  data.z=numpy.zeros(shape=(data.nx,data.nz))
  data.lams=numpy.zeros(shape=(data.nlam))
  data.AV=numpy.zeros(shape=(data.nx,data.nz))
  data.AVrad=numpy.zeros(shape=(data.nx,data.nz))
  data.AVver=numpy.zeros(shape=(data.nx,data.nz))
  data.NHver=numpy.zeros(shape=(data.nx,data.nz))
  data.NHrad=numpy.zeros(shape=(data.nx,data.nz))
  data.d2g=numpy.zeros(shape=(data.nx,data.nz))
  data.tg=numpy.zeros(shape=(data.nx,data.nz))
  data.td=numpy.zeros(shape=(data.nx,data.nz))
  data.nd=numpy.zeros(shape=(data.nx,data.nz))
  data.soundspeed=numpy.zeros(shape=(data.nx,data.nz))
  data.rhog=numpy.zeros(shape=(data.nx,data.nz))
  data.pressure=numpy.zeros(shape=(data.nx,data.nz))
  data.solved_chem=numpy.zeros(shape=(data.nx,data.nz),dtype=numpy.int32)
  data.tauchem=numpy.zeros(shape=(data.nx,data.nz))
  data.taucool=numpy.zeros(shape=(data.nx,data.nz))
  data.taudiff=numpy.zeros(shape=(data.nx,data.nz))
  data.heat_mainidx=numpy.zeros(shape=(data.nx,data.nz),dtype=numpy.int32)
  data.cool_mainidx=numpy.zeros(shape=(data.nx,data.nz),dtype=numpy.int32)
  data.nHtot=numpy.zeros(shape=(data.nx,data.nz))
  data.damean=numpy.zeros(shape=(data.nx,data.nz))
  data.Hx=numpy.zeros(shape=(data.nx,data.nz))
  data.tauX1=numpy.zeros(shape=(data.nx,data.nz))
  data.tauX5=numpy.zeros(shape=(data.nx,data.nz))
  data.tauX10=numpy.zeros(shape=(data.nx,data.nz))
  data.zetaX=numpy.zeros(shape=(data.nx,data.nz))
  data.chi=numpy.zeros(shape=(data.nx,data.nz))
  data.chiRT=numpy.zeros(shape=(data.nx,data.nz))
  data.kappaRoss=numpy.zeros(shape=(data.nx,data.nz))
  data.zetaCR=numpy.zeros(shape=(data.nx,data.nz))
  data.zetaSTCR=numpy.zeros(shape=(data.nx,data.nz))

  data.heat_names=list()
  data.cool_names=list()
  data.rateH2form=numpy.zeros(shape=(data.nx,data.nz))
  data.rateH2diss=numpy.zeros(shape=(data.nx,data.nz,3))

  # init the caches, to avoid conversion to float if not necessary
  # TODO: check if itemsize is really required ... but the length should be enough
  # for this we use a cache
  data._radFields_cache=numpy.chararray(shape=(data.nx,data.nz,data.nlam),itemsize=13)
  data._nmol_cache=numpy.chararray((data.nx,data.nz,data.nspec),itemsize=13)
  data._heat_cache=numpy.chararray((data.nx,data.nz,data.nheat),itemsize=13)
  data._cool_cache=numpy.chararray((data.nx,data.nz,data.ncool),itemsize=13)

  # Make some checks for the format
  # new EXP format for x and z:
  newexpformat=lines[idata].find("E",0,25)>=0
  # FIXME: that is not very nice
  #        make at least some checks if the output format has changed or something
  # number of fixed fields in ProDiMo.out (before heating and cooling rates)
  nfixFields=21
  # index after the J data/fields in ProDiMo

  iACool=nfixFields+data.nheat+data.ncool
  iASpec=iACool+1+data.nspec

    # FIXME: workaround to deal with el_is_sp
    # this means the e- is also included a species, it is then also included
    # in the output as the last element, simply skip that column then.
  iASpecskip=0
  if (nspecreal==data.nspec):
    iASpecskip=1

  iAJJ=iASpec+iASpecskip+data.nlam

  # read the species names, these are taken from the column titles
  colnames=lines[idata-1]

  # FIXME: Again hardconding. Might be better to read the Species names
  # from Species.out. Assumes that the name for each species has len 13.
  # Assume that the first species is e- and search for that
  # that is more flexible in case other names change
  # specStart = 233 + data.nheat * 13 + data.ncool * 13 + 13
  # do not include the electron in the splitting because that one is speciesl
  specStart=colnames.find("           e-")+13
  # FIXME: workaround to deal with e- as species (el_is_sp=true), in that
  # case it is included twice in the output but using nspec from ProDiMo.out
  # should be fine (i.e. ignore the last column of the species which is then e- again).
  spnames=colnames[specStart:specStart+(data.nspec-1)*13]
  spnames=spnames.split()
  # now insert the electron again.
  # but both are dictionaries so I guess it should be fine
  spnames.insert(0,"e-")
  if (len(spnames)!=data.nspec):
    print("ERROR: something is wrong with the number of Species!")
    return None

  # empty dictionary
  data.spnames=OrderedDict()
  # Make a dictionary for the spnames
  for i in range(data.nspec):
    data.spnames[spnames[i]]=i

  # read the heating and cooling names
  iheat=idata+data.nx*data.nz+2
  for i in range(data.nheat):
    data.heat_names.append(lines[iheat+i][3:].strip())

  icool=idata+data.nx*data.nz+2+data.nheat+2
  for i in range(data.ncool):
    data.cool_names.append(lines[icool+i][3:].strip())

  # read the band wavelenghts
  iwls=idata+data.nx*data.nz+2+data.nheat+2+data.ncool+2
  for i in range(data.nlam):
    data.lams[i]=float((lines[iwls+i].split())[1])

  i=0

  # startLoop=timer()
  for iz in range(data.nz):
    zidx=data.nz-iz-1
    for ix in range(data.nx):

      # stupid workaround for big disks/envelopes where x,y can be larger than 10000 au
      # there is no space between the numbers for x and z so always add one if none is there
      # this might can be removed in the future as the newest ProDiMo version use exp format now
      line=lines[idata+i]
      if (not newexpformat):
        if line[20]!=" ":
          line=line[:20]+" "+line[20:]
        # needs another fix
        if line[8]!=" ":
          line=line[:8]+" "+line[8:]

      # This line is what eats the time, but using genfromtxt for the ProDiMo.out
      # does not seem to be faster
      # fields=numpy.fromstring(line,sep=" ")
      fields=line.split()

      data.x[ix,zidx]=fields[2]
      data.z[ix,zidx]=fields[3]
      data.NHrad[ix,zidx]=fields[4]
      data.NHver[ix,zidx]=fields[5]
      data.AVrad[ix,zidx]=fields[6]
      data.AVver[ix,zidx]=fields[7]
      data.nd[ix,zidx]=fields[8]
      data.tg[ix,zidx]=fields[9]
      data.td[ix,zidx]=fields[10]
      data.soundspeed[ix,zidx]=fields[11]
      data.rhog[ix,zidx]=fields[12]
      data.pressure[ix,zidx]=fields[13]
      data.solved_chem[ix,zidx]=fields[14]
      data.chi[ix,zidx]=fields[15]
      data.tauchem[ix,zidx]=fields[16]
      data.taucool[ix,zidx]=fields[17]
      data.taudiff[ix,zidx]=fields[18]
      data.heat_mainidx[ix,zidx]=fields[19]
      data.cool_mainidx[ix,zidx]=fields[20]
      data._heat_cache[ix,zidx,:]=fields[nfixFields:nfixFields+data.nheat]
      data._cool_cache[ix,zidx,:]=fields[(nfixFields+data.nheat):(nfixFields+data.nheat+data.ncool)]
      data.nHtot[ix,zidx]=fields[iACool]
      data._nmol_cache[ix,zidx,:]=fields[iACool+1:iASpec]
      data._radFields_cache[ix,zidx,:]=fields[(iASpec+iASpecskip):iAJJ]
      data.chiRT[ix,zidx]=fields[iAJJ]
      data.kappaRoss[ix,zidx]=fields[iAJJ+1]
      data.damean[ix,zidx]=fields[iAJJ+3]
      data.d2g[ix,zidx]=fields[iAJJ+4]
      data.Hx[ix,zidx]=fields[iAJJ+5]
      data.tauX1[ix,zidx]=fields[iAJJ+6]
      data.tauX5[ix,zidx]=fields[iAJJ+7]
      data.tauX10[ix,zidx]=fields[iAJJ+8]
      data.zetaX[ix,zidx]=fields[iAJJ+9]
      data.rateH2form[ix,zidx]=fields[iAJJ+10]
      data.rateH2diss[ix,zidx,:]=fields[iAJJ+11:iAJJ+11+3]
      data.zetaCR[ix,zidx]=fields[iAJJ+16]
      if len(fields)>(iAJJ+17): data.zetaSTCR[ix,zidx]=fields[iAJJ+17]

      i=i+1

  # endLoop=timer()

  # derived quantitites
  data.rhod=data.rhog*data.d2g

  # AV like defined in the prodimo idl script
  for ix in range(data.nx):
    for iz in range(data.nz):
      data.AV[ix,iz]=numpy.min([data.AVver[ix,iz],data.AVrad[ix,iz],data.AVrad[data.nx-1,iz]-data.AVrad[ix,iz]])

  # Read FlineEstimates.out
  if readlineEstimates==True:
    read_lineEstimates(directory,data,filename=filenameLineEstimates,tarfile=tarfile)
  else:
    data.lineEstimates=None

  data.elements=read_elements(directory,tarfile=tarfile)

  data.dust=read_dust(directory,tarfile=tarfile)

  fileloc=directory+"/dust_opac_env.out"
  if os.path.isfile(fileloc):
    data.env_dust=read_dust(directory,filename="dust_opac_env.out",tarfile=tarfile)

  data.starSpec=read_starSpec(directory,tarfile=tarfile)

  if os.path.exists(directory+"/gas_cs.out"):
    data.gas=read_gas(directory,tarfile=tarfile)

  if os.path.exists(directory+"/"+filenameLineFlux):
    data.lines=read_linefluxes(directory,filename=filenameLineFlux,tarfile=tarfile)

  if os.path.exists(directory+"/SED.out"):
    data.sed=read_sed(directory,tarfile=tarfile)

  if readObs:
    data.sedObs=read_continuumObs(directory)
    if data.lines is not None:
      if os.path.exists(directory+"/LINEobs.dat"):
        data.lineObs=read_lineObs(directory,len(data.lines))

      # FIXME: workaround set also the frequency for the observed lline
      if data.lineObs is not None:
        for i in range(len(data.lines)):
          data.lineObs[i].frequency=data.lines[i].frequency
          if data.lineObs[i].profile is not None:
            data.lineObs[i].profile.restfrequency=data.lineObs[i].frequency

  if readImages:
    data.contImages=read_continuumImages(directory)

  if os.path.exists(directory+"/"+filenameFLiTs):
    data.FLiTsSpec=read_FLiTs(directory,filenameFLiTs)

  if os.path.exists(directory+"/Parameter.out"):
    data.params=ModelParameters(filename="Parameter.out",directory=directory)

  # print("INFO: Loop time: ","{:4.2f}".format(endLoop-startLoop)+" s")
  print("INFO: Reading time: ","{:4.2f}".format(timer()-startAll)+" s")

  # set muH
  data.muH=data.rhog[0,0]/data.nHtot[0,0]

  print(" ")

  return data


def read_elements(directory,filename="Elements.out",tarfile=None):
  '''
  Reads the Elements.out file.
  Also adds the electron "e-" to the Elements.

  Parameters
  ----------
  directory : str
    the directory of the model

  filename: str
    an alternative Filename

  Returns
  -------
  :class:`~prodimopy.read.DataElements`
    the Elements model data or `None` in case of errors.

  '''

  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  nelements=int(f.readline())

  elements=DataElements()
  f.readline()

  for i in range(nelements):
    line=f.readline()
    fields=line.strip().split()
    name=fields[0].strip()
    # FIXME: Workaround with the quadropole solver an element ch is included
    # don't know what to do with that.
    if name=="ch": continue

    elements.abun12[name]=float(fields[1])
    elements.abun[name]=10.0**(float(fields[1])-12.0)
    elements.amu[name]=float(fields[2])
    elements.massRatio[name]=float(fields[3])

  # also read muH (last element of the string)
  elements.muHamu=float(f.readline().strip().split()[-1])

  return elements


def read_species(directory,filename="Species.out",tarfile=None):
  '''
  Reads the Species.out file.
  Also adds the electron "e-" if necessary.

  Also sets data.nspec as only here I can know if e- was a real species in
  ProDiMo or not. If it was a real species I don't need to add that.

  Parameters
  ----------
  directory : str
    the directory of the model

  pdata : :class:`prodimopy.read.Data_ProDiMo`
    the ProDiMo Model data structure, where the data is stored

  filename: str
    an alternative Filename

  Returns
  -------
  :class:`~prodimopy.read.DataSpecies`
    the Species model data or `None` in case of errors.

  ..todo :
    * stochiometry is still missing

  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None:
    return None

  species=DataSpecies()

  # skip the first line
  f.readline()

  species.mass=OrderedDict()
  species.charge=OrderedDict()
  species.chemPot=OrderedDict()

  for line in f:
    fields=line.strip().split()
    spname=fields[2].strip()
    species.mass[spname]=(float(fields[3].strip())*u.u).cgs.value
    species.charge[spname]=int(fields[4].strip())
    species.chemPot[spname]=float(fields[5].strip())

  # Only do this if it does not exist yet.
  # This is the only place where one can know if the e- is a real species
  # in ProDiMo or not (well could also use Parameter.out)
  if not "e-" in species.mass.keys():
    species.mass["e-"]=const.m_e.cgs.value
    species.charge["e-"]=-1
    species.chemPot["e-"]=0.0
  else:
    # overwrite the mass, as it is not correct due to rounding in Species.out
    species.mass["e-"]=const.m_e.cgs.value

  # electron should be in first place like in ProDiMo.out
  species.mass.move_to_end("e-",last=False)
  species.charge.move_to_end("e-",last=False)
  species.chemPot.move_to_end("e-",last=False)

  return species


def read_lineEstimates(directory,pdata,filename="FlineEstimates.out",tarfile=None):
  '''
  Read FlineEstimates.out Can only be done after ProDiMo.out is read.

  Parameters
  ----------
  directory : str
    the directory of the model

  pdata : :class:`prodimopy.read.Data_ProDiMo`
    the ProDiMo Model data structure, where the data is stored

  filename: str
    an alternative Filename

  '''
  f,rfile=_getfile(filename,directory,tarfile,binary=True)
  if f is None:
    pdata.lineEstimates=None
    return None
  else:
    pdata.__fpFlineEstimates=rfile
    pdata.__tarfile=tarfile

  # check for version currently just check if it exist
  line=f.readline().decode()
  version=1
  if len(line)>68:
    # position of version
    posver=line.find("version")
    if posver>=0:
      version=int(line[posver+len("version"):].strip())

  nlines=int(f.readline().strip())
  f.readline()

  pdata.lineEstimates=list()
  nxrange=list(range(pdata.nx))
  startBytes=0

  for i in range(nlines):
    # has to be done in fixed format
    # FIXME: it can be that nline is not really equal the nubmer of available line
    # this ir probably a bug in ProDiMo but maybe intended (see
    # OUTPUT_FLINE_ESTIMATE in ProDiMo, Therefore add a check
    line=f.readline()
    if not line: break

    line=line.decode()
    # FIXME: has now also a version tag!! this is for the new version
    if version==1:
      le=DataLineEstimate((line[0:9]).strip(),float(line[10:28]),int(line[29:32]),int(line[33:37]),float(line[38:49]))
    elif version==2:
      try:
        le=DataLineEstimate((line[0:9]).strip(),float(line[10:28]),int(line[29:34]),int(line[35:40]),float(line[41:53]))
      except ValueError as err:
        print("Conversion problems: {0}".format(err))
        print("Line (i,text): ",i,line)
        print("Field: ",line[0:9],line[10:28],line[29:34],line[35:40],line[41:53])
        raise err
    else:
      raise ValueError('Unknown version of FlineEstimates.out! version='+str(version))

    # Fine out the number of bytes in one radial line to use seek in the
    # next iterations
    if i==0:
      start=f.tell()
      le.__posrInfo=start  # store the position for reading this info if required
      for j in nxrange:
        f.readline()
      startBytes=f.tell()-start
    else:
      le.__posrInfo=f.tell()
      f.seek(startBytes,1)

    pdata.lineEstimates.append(le)

  f.close()


def _read_lineEstimateRinfo(pdata,lineEstimate):
  '''
  Reads the additional Rinfo data for the given lineEstimate.
  '''
  f,dummy=_getfile(pdata.__fpFlineEstimates,None,pdata.__tarfile,binary=True)
  if f is None: return None

  f.seek(lineEstimate.__posrInfo,0)
  nxrange=list(range(pdata.nx))
  lineEstimate.rInfo=list()
  for j in nxrange:
    fieldsR=f.readline().decode().split()
    ix=int(fieldsR[0].strip())
    iz=int(fieldsR[1].strip())
    Fcolumn=float(fieldsR[2])
    try:
      tauLine=float(fieldsR[3])
    except ValueError as e:
      # print "read_lineEstimates line: ", le.ident  ," error: ", e
      tauLine=0.0
    tauDust=float(fieldsR[4])
    z15=(float(fieldsR[5])*u.cm).to(u.au).value
    z85=(float(fieldsR[6])*u.cm).to(u.au).value
    # ix -1 and iz-1 because in python we start at 0
    rInfo=DataLineEstimateRInfo(ix-1,iz-1,Fcolumn,tauLine,tauDust,z15,z85)
    lineEstimate.rInfo.append(rInfo)

  f.close()


def  read_linefluxes(directory,filename="line_flux.out",tarfile=None):
  """ Reads the line fluxes output.

  Parameters
  ----------
  directory : str
    the model directory.

  filename : str
    the filename of the output file (optional).

  Returns
  -------
  list(:class:`prodimopy.read.DataLine`)
    List of lines.
  """
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  records=f.readlines()
  f.close()

  dist=float(records[0].split("=")[1])
  incl=float(records[1].split("=")[1])
  nlines=int(records[2].split("=")[1])
  nvelo=int(records[3].split("=")[1])

  # number of records in the file
  nrecords=len(records)
  # print dist,incl,nlines,nvelo,nrecords

  lines=list()

  # loop over all lines
  pos=5
  for i in range(nlines):
    # read the data for one line
    line=DataLine()
    rec=records[pos]
    try:
      line.species=(rec[10:20]).strip()
      line.ident=line.species
      line.prodimoInf=rec[21:36].strip()
      line.wl=float(rec[43:54].strip())  # *u.um
      line.frequency=float(rec[63:76].strip())  # *u.GHz
    except:
      # print("read_linefluxes: try new format")
      line.species=(rec[10:20]).strip()
      line.ident=line.species
      line.prodimoInf=rec[21:47].strip()
      line.wl=float(rec[48:64].strip())  # *u.um
      line.frequency=float(rec[74:90].strip())  # *u.GHz

    rec=records[pos+1]
    line.flux=float(rec.split("=")[1].strip())  # *u.Watt/u.m**2

    rec=records[pos+2]
    line.fcont=float(rec.split("=")[1].strip())  # *u.Jansky

    # simply store inclination and distance for each line
    line.distance=dist
    line.inclination=incl

    # one line in the profile is for the continuum
    line.profile=DataLineProfile(nvelo-1,restfrequency=line.frequency)

    for j in range(nvelo-1):
      # skip the header line and the first line (continuum)?
      fields=records[pos+5+j].split()
      line.profile.velo[j]=float(fields[0])  # *u.km/u.s
      line.profile.flux[j]=float(fields[1])  # *u.Jansky
      if (len(fields)>2):
        line.profile.flux_conv[j]=float(fields[2])  # *u.Jansky
      if (len(fields)>3):
        line.profile.flux_dust[j]=float(fields[3])  # *u.Jansky

    lines.append(line)
    pos+=(nvelo+5)

  return lines


def read_lineObs(directory,nlines,filename="LINEobs.dat",tarfile=None):
  '''
  Reads the lineobs Data. the number of lines have to be known.
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  records=f.readlines()
  f.close()

  linesobs=list()
  versionStr=records[0].split()
  version=float(versionStr[0])

  for rec in records[2:2+nlines]:
    fields=rec.split()

    lineobs=DataLineObs(float(fields[0].strip()),\
                        float(fields[1].strip()),\
                        float(fields[2].strip()),\
                        float(fields[3].strip()),\
                        fields[4].strip())

    # FIXME: not very nice
    # in case of upper limits flux might be zero in that case use sig.
    if lineobs.flux<1.e-100:
      lineobs.flux=lineobs.flux_err

    linesobs.append(lineobs)

  # the additional data
  # check if there is actually more data
  if (len(records)>2+nlines+1):
    # FIXME: do this proberly (the reading etc. and different versions)
    profile=(records[2+nlines+1].split())[0:nlines]
    autoC=(records[2+nlines+2].split())[0:nlines]
    vvalid=(records[2+nlines+3].split())[0:nlines]

  # speres = (records[2 + nlines+4].split())[0:nlines]

    offset=5
    if version>2.0: offset=6

    # now go through the profiles
    for i in range(nlines):
      proffilename=records[offset+nlines+i+1].strip()
      if profile[i]=="T":
        if "nodata"==proffilename: print("WARN: Something is wrong with line "+str(i))
        linesobs[i].profile,linesobs[i].profileErr=read_lineObsProfile(proffilename,directory=directory)

  return linesobs


def read_lineObsProfile(filename,directory=".",tarfile=None):
  '''
  reads a line profile file which can be used for ProDiMo
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  records=f.readlines()
  f.close()

  # First line number of velo points and central wavelength, which we do not
  # need here (I think this is anyway optional
  nvelo=int(records[0].split()[0].strip())

  # skip header lines
  profile=DataLineProfile(nvelo)
  for i in range(2,nvelo+2):
    fields=records[i].split()
    profile.velo[i-2]=float(fields[0].strip())
    profile.flux[i-2]=float(fields[1].strip())
    # also fill the convolved flux, which is just the same as the flux
    # for observations
    profile.flux_conv[i-2]=profile.flux[i-2]

  # TODO: some profiles might do not include an err field
  # Check if actually some do?
  if (nvelo+2)>=len(records):
    err=0.0
  else:
    if records[nvelo+2].strip()!="":
      err=float(records[nvelo+2].split()[0].strip())
    else:
      err=0.0

  return profile,err


def read_gas(directory,filename="gas_cs.out",tarfile=None):
  '''
  Reads gas_cs.out
  Returns an object of Type DataDust
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  nlam=int(f.readline().strip())

  # skip one line
  f.readline()

  gas=DataGas(nlam)

  for i in range(nlam):
    fields=[float(field) for field in f.readline().split()]
    gas.lam[i]=float(fields[0])
    gas.abs_cs[i]=float(fields[1])
    gas.sca_cs[i]=float(fields[2])

  gas.energy[:]=((gas.lam[:]*u.micron).to(u.eV,equivalencies=u.spectral())).value

  f.close()

  return gas


def read_continuumImages(directory,filename="image.out"):
  '''
  Reads the image.out file.

  To avoid unnecessary memor usage, the Intensities are not read in this
  routine. For this use :func:`~prodimopy.read.DataContinuumImages.get_image`
  '''

  f,fname=_getfile(filename,directory=directory)

  if f is None: return None

  dummy=f.readline()
  nrnt=f.readline().split()
  nlam=f.readline().split()[0]

  images=DataContinuumImages(int(nlam),int(nrnt[0]),int(nrnt[1]),filepath=fname)

  images.lams[:]=numpy.array(f.readline().split()).astype(numpy.float)
  f.close()

  # Read the coordinates
  xy=numpy.loadtxt(fname,skiprows=6,usecols=(2,3))
  images.x=xy[:,0].reshape(images.nx,images.ny)
  images.y=xy[:,1].reshape(images.nx,images.ny)

  return images


def read_continuumObs(directory,filename="SEDobs.dat"):
  '''
  Reads observational continuum data (SED).

  Reads the file SEDobs.dat (phtotometric points) and all files ending
  with `*spec.dat` (e.g. the Spitzer spectrum)

  FIXME: does not work yet with tar files
  '''
  contObs=None
  rfile=directory+"/"+filename
  if os.path.exists(rfile):
    print("READ: Reading File: ",rfile," ...")
    f=open(rfile,'r')

    nlam=int(f.readline().strip())
    f.readline()  # header line
    contObs=DataContinuumObs(nlam=nlam)
    for i in range(nlam):
      elems=f.readline().split()
      contObs.lam[i]=float(elems[0])
      contObs.fnuJy[i]=float(elems[1])
      contObs.fnuJyErr[i]=float(elems[2])
      contObs.flag[i]=str(elems[3])

    contObs.nu=(contObs.lam*u.micrometer).to(u.Hz,equivalencies=u.spectral()).value
    contObs.fnuErg=(contObs.fnuJy*u.Jy).cgs.value
    contObs.fnuErgErr=(contObs.fnuJyErr*u.Jy).cgs.value

  # check for the spectrum files
  # types of spectra that are understood, is more of a unofficial naming convention
  types=["Spitzer","ISO","PACS","SPIRE"]
  fnames=list()
  for spectype in types:
    fnames.extend(glob.glob(directory+"/"+spectype+"*spec*.dat"))

  if fnames is not None and len(fnames)>0:
    if contObs is None:
      contObs=DataContinuumObs()
    contObs.specs=list()

  for fname in fnames:
    print("READ: Reading File: ",fname," ...")
    # use basename in the if to avoid problems with directory names
    # containing the string of one of the types.
    if types[0] in os.path.basename(fname):
      spec=numpy.loadtxt(fname,skiprows=3)
    elif types[1] in os.path.basename(fname):
      spec=numpy.loadtxt(fname,skiprows=1)
    elif types[2] in os.path.basename(fname):
      spec=numpy.loadtxt(fname)
    elif types[3] in os.path.basename(fname):
      spec=numpy.loadtxt(fname,skiprows=1)
      # convert frequency to micron, SPIRE data
      spec[:,0]=(spec[:,0]*u.GHz).to(u.micron,equivalencies=u.spectral()).value
    else:
      print("Don't know about type of "+fname+" Spectrum. Try anyway")
      spec=numpy.loadtxt(fname)

    # If there is no error provided just and a zero column
    if spec.shape[1]<3:
      spec=numpy.c_[spec,np.zeros(spec.shape[0])]

    contObs.specs.append(spec)

  # check if there is some extinction data
  fn_ext=directory+"/extinct.dat"
  if os.path.exists(fn_ext):
    print("READ: Reading File: ",fn_ext," ...")
    if contObs is None:
      contObs=DataContinuumObs()

    fext=open(fn_ext,"r")
    fext.readline()
    contObs.E_BV=float(fext.readline())
    fext.readline()
    contObs.R_V=float(fext.readline())
    contObs.A_V=contObs.R_V*contObs.E_BV

#   # check if there is an image.in
#   fn_images= directory+"/image.in"
#   if os.path.exists(fn_images):
#     if contObs is None:
#       contObs=DataContinuumObs()
#
#     fext= open(fn_images,"r")
#     fext.readline()
#     fext.readline()
#     nimages=int(fext.readline())
#     positionAngle = float(fext.readline())
#
#     for i in range(9):
#       line = f.readline()

  return contObs


def read_FLiTs(directory,filename="specFLiTs.out",tarfile=None):
  '''
  Reads the FLiTs spectrum.

  Returns
  -------
  :class:`prodimopy.read.DataFLiTsSpec`
    The Spectrum.

  '''
  f,pfilename=_getfile(filename,directory,tarfile)
  if f is None: return None,None
  f.close()

  # currently read only the wavelength and the flux
  spec=np.loadtxt(pfilename,usecols=[0,1])

  specFLiTs=DataFLiTsSpec()
  specFLiTs.wl=spec[:,0]
  specFLiTs.flux=spec[:,1]
  return specFLiTs


def read_sed(directory,filename="SED.out",filenameAna="SEDana.out",tarfile=None):
  '''
  Reads the ProDiMo SED output including the analysis data.
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  elems=f.readline().split()
  distance=float(elems[len(elems)-1])
  # ignore the face-on SED
  f.readline()
  nlam=int(f.readline())
  f.readline()
  for i in range(nlam):
    f.readline()

  f.readline()
  elems=f.readline().split()
  inclination=float(elems[len(elems)-1])
  nlam=int(f.readline())
  f.readline()
  sed=DataSED(nlam,distance,inclination)
  for i in range(nlam):
    elems=f.readline().split()
    sed.lam[i]=float(elems[0])
    sed.nu[i]=float(elems[1])

    # FIXME: Workaround to catch strange values from ProDiMo .. should be fixed
    # in ProDiMo
    try:
      sed.fnuErg[i]=float(elems[2])
      sed.nuFnuW[i]=float(elems[3])
      sed.fnuJy[i]=float(elems[4])
    except ValueError as err:
      print("WARN: Could not read value from SED.out: ",err)

  sed.setLbolTbol()
  f.close()

  # The analysis data, if it is not there not a big problem
  f,dummy=_getfile(filenameAna,directory,tarfile)
  if f is None:
    sed.sedAna=None
    return sed

  nlam,nx=f.readline().split()
  nlam=int(nlam)
  nx=int(nx)

  sed.sedAna=DataSEDAna(nlam,nx)

  for i in range(nlam):
    elems=f.readline().split()
    sed.sedAna.lams[i]=float(elems[0])
    sed.sedAna.r15[i]=float(elems[1])
    sed.sedAna.r85[i]=float(elems[2])
    for j in range(nx):
      elems=f.readline().split()
      sed.sedAna.z15[i,j]=float(elems[0])
      sed.sedAna.z85[i,j]=float(elems[1])

  f.close()

  return sed


def read_starSpec(directory,filename="StarSpectrum.out",tarfile=None):
  '''
  Reads StarSpectrum.out
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  teff=float((f.readline().split())[-1])
  elems=f.readline().split()
  r=float(elems[-1])
  logg=float(elems[2])
  luv=float(f.readline().split()[-1])
  nlam=int(f.readline())
  f.readline()

  starSpec=DataStarSpec(nlam,teff,r,logg,luv)
  for i in range(nlam):
    elems=f.readline().split()
    starSpec.lam[i]=float(elems[0])
    starSpec.nu[i]=float(elems[1])
    starSpec.Inu[i]=float(elems[2])

  f.close()
  return starSpec


def read_bgSpec(directory,filename="BgSpectrum.out",tarfile=None):
  '''
  Reads the BgSpectrum.out file.

  Returns
  -------
    :class:`prodimopy.read.DataBgSpec`
    the background spectra or `None` if not found.
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  nlam=int(f.readline())
  f.readline()

  bgSpec=DataBgSpec(nlam)
  for i in range(nlam):
    elems=f.readline().split()
    bgSpec.lam[i]=float(elems[0])
    bgSpec.nu[i]=float(elems[1])
    bgSpec.Inu[i]=float(elems[2])

  return bgSpec


def read_dust(directory,filename="dust_opac.out",tarfile=None):
  '''
  Reads dust_opac.out and if it exists dust_sigmaa.out.
  Returns an object of Type DataDust
  Does not read the dust composition yet

  FIXME: reading of dust_opac.out should be in separate routine.
  '''
  f,dummy=_getfile(filename,directory,tarfile)
  if f is None: return None

  fields=[int(field) for field in f.readline().split()]
  ndsp=fields[0]
  nlam=fields[1]

  # skip three lines
  for i in range(ndsp):
    f.readline()

  # apow amax etc.
  strings=f.readline().split()

  if len(strings)>0:
    amin=((float(strings[6])*u.cm).to(u.micron)).value
    amax=((float(strings[7])*u.cm).to(u.micron)).value
    apow=float(strings[8])
    nsize=int(strings[9])
    dust=DataDust(amin,amax,apow,nsize,nlam)
  else:
    dust=DataDust(-1,-1,0.0,-1,nlam)

  f.readline()

  for i in range(nlam):
    fields=[float(field) for field in f.readline().split()]
    dust.lam[i]=float(fields[0])
    dust.kext[i]=float(fields[1])
    dust.kabs[i]=float(fields[2])
    dust.ksca[i]=float(fields[3])

    if len(fields)>4:
      dust.ksca_an[i]=float(fields[5])  # skip kprn

  f.close()

  dust.energy[:]=((dust.lam[:]*u.micron).to(u.eV,equivalencies=u.spectral())).value

  # is optional but returns None if file is not there
    # does not have to be there
  if os.path.isfile(directory+"/"+filename):
    dust.asize,dust.sigmaa=read_dust_sigmaa(directory)

  return dust


def read_dust_sigmaa(directory,filename="dust_sigmaa.out",tarfile=None):
  '''
  Reads the radial surface density profiles for each grain size.

  Parameters
  ----------

  directory : str
    The directory where the file is located (the ProDiMo model directory).

  filename : str
    The filename. Default: "dust_sigmaa.out"

  '''
  f,pfilename=_getfile(filename,directory,tarfile)
  if f is None: return None,None
  f.close()  # don't  need it use np for simplicity

  # a bit quick an dirty
  data=np.loadtxt(pfilename,comments="#")

  # the first row in the array are the grain sizes.
  # convert from cm to micron
  asize=(data[0,:]*u.cm).to(u.micron).value
  # used transposed array, to be consistent with ohter stuff.
  sigmaa=np.transpose(data[1:,:])

  return asize,sigmaa


def calc_NHrad_oi(data):
  '''
  Calculates the radial column density from out to in (border of model space to star/center)

  TODO: move this to utils
  '''

  NHradoi=0.0*data.nHtot
  for ix in range(data.nx-2,1,-1):  # first ix point (ix=0= remains zero
    r1=(data.x[ix+1,:]**2+data.z[ix+1,:]**2)**0.5
    r2=(data.x[ix,:]**2+data.z[ix,:]**2)**0.5
    dr=r1-r2
    dr=dr*u.au.to(u.cm)
    nn=0.5*(data.nHtot[ix+1,:]+data.nHtot[ix,:])
    NHradoi[ix,:]=NHradoi[ix+1,:]+nn*dr

  return NHradoi


def calc_surfd(data):
  '''
  Caluclates the gas and dust vertical surface densities at every point in the
  model.

  Only one half of the disk is considered. If one needs the total surface density
  simply multiply the value from the midplane (zidx=0) by two.

  TODO: make it "private" no need to use it directly.

  '''
  print("INFO: Calculate surface densities")

  tocm=(1.0*u.au).to(u.cm).value
  data._sdg=0.0*data.rhog
  data._sdd=0.0*data.rhod
  for ix in range(data.nx):
    for iz in range(data.nz-2,-1,-1):  # from top to bottom
      dz=(data.z[ix,iz+1]-data.z[ix,iz])
      dz=dz*tocm
      nn=0.5*(data.rhog[ix,iz+1]+data.rhog[ix,iz])
      data._sdg[ix,iz]=data._sdg[ix,iz+1,]+nn*dz
      nn=0.5*(data.rhod[ix,iz+1]+data.rhod[ix,iz])
      data._sdd[ix,iz]=data._sdd[ix,iz+1,]+nn*dz


def _calc_vol(data):
  '''
  Inits the vol field (:attr:`~prodimpy.read.Data_ProDiMo._vol` for each individual grid point.

  This is useful to estimate mean quantities which are weighted by volume
  but also by mass.

  The routine follows the same method as in the prodimo.pro (the IDL skript)

  '''

  print("INFO: Calculate volumes")
  tocm=(1.0*u.au).to(u.cm).value
  data._vol=numpy.zeros(shape=(data.nx,data.nz))
  fourthreepi=4.0*math.pi/3.0
  for ix in range(data.nx):
    ix1=np.max([0,ix-1])
    ix2=ix
    ix3=np.min([data.nx-1,ix+1])
    x1=math.sqrt(data.x[ix1,0]*data.x[ix2,0])*tocm
    x2=math.sqrt(data.x[ix2,0]*data.x[ix3,0])*tocm  # does not depend on iz
    for iz in range(data.nz):
      iz1=np.max([0,iz-1])
      iz2=iz
      iz3=np.min([data.nz-1,iz+1])
      tanbeta1=0.5*(data.z[ix,iz1]+data.z[ix,iz2])/data.x[ix,0]
      tanbeta2=0.5*(data.z[ix,iz2]+data.z[ix,iz3])/data.x[ix,0]
      data.vol[ix,iz]=fourthreepi*(x2**3-x1**3)*(tanbeta2-tanbeta1)

  # Test for volume stuff ... total integrated mass
  # mass=np.sum(np.multiply(data.vol,data.rhog))
  # print("Total gas mass",(mass*u.g).to(u.M_sun))


def _calc_cdnmol(data):
  '''
  Calculated the vertical column number densities for every species
  at every point in the disk (from top to bottom). Very simple and rough method.

  Only one half of the disk is considered. If one needs the total surface density
  simply multiply the value from the midplane (zidx=0) by two.

  TODO: make it "private" no need to use it directly.

  '''

  if data._log: print("INFO: Calculate vertical column densities")

  tocm=(1.0*u.au).to(u.cm).value
  data._cdnmol=0.0*data.nmol
  for ix in range(data.nx):
    for iz in range(data.nz-2,-1,-1):  # from top to bottom
      dz=(data.z[ix,iz+1]-data.z[ix,iz])
      dz=dz*tocm
      nn=0.5*(data.nmol[ix,iz+1,:]+data.nmol[ix,iz,:])
      data._cdnmol[ix,iz,:]=data._cdnmol[ix,iz+1,:]+nn*dz

  # check if integration is correct
  # for the total hydrogen column density the error is less than 1.e-3
  # that should be good enough for plotting
  # nHverC=data._cdnmol[:,:,data.spnames["H"]]+data._cdnmol[:,:,data.spnames["H+"]]+data._cdnmol[:,:,data.spnames["H2"]]*2.0
  # print(numpy.max(numpy.abs(1.0-nHverC[:,0]/data.NHver[:,0])))


def _calc_rcdnmol(data):
  '''
  Calculated the radial column number densities for every species
  at every point in the disk. Very simple and rough method.

  TODO: make it "private" no need to use it directly.
  TODO: this can be quire inaccurate as the x info for the innermost points is not printed accurately to PRoDiMo.out which cause dr to be zero
  '''

  if data._log: print("INFO: Calculate radial column densities")

  tocm=(1.0*u.au).to(u.cm).value
  data._rcdnmol=0.0*data.nmol
  for iz in range(data.nz):
    for ix in range(1,data.nx,1):  # first ix point (ix=0= remains zero
      r1=(data.x[ix,iz]**2+data.z[ix,iz]**2)**0.5
      r2=(data.x[ix-1,iz]**2+data.z[ix-1,iz]**2)**0.5
      dr=r1-r2
      dr=dr*tocm
      nn=0.5*(data.nmol[ix,iz ,:]+data.nmol[ix-1,iz,:])
      data._rcdnmol[ix,iz,:]=data._rcdnmol[ix-1,iz,:]+nn*dr
  # FIXME: test the integration error can be at most 16% ... good enough for now (most fields are better)
  # nHverC=data._rcdnmol[:,:,data.spnames["H"]]+data._rcdnmol[:,:,data.spnames["H+"]]+data._rcdnmol[:,:,data.spnames["H2"]]*2.0
  # izt=data.nz-2
  # print(nHverC[:,izt],data.NHrad[:,izt])
  # print(numpy.max(numpy.abs(1.0-nHverC[1:,:]/data.NHrad[1:,:])))


def analyse_chemistry(species,model,name=None,directory=None,filenameReactions="Reactions.out",
                      filenameChemistry='chemanalysis.out',to_txt=True,td_fileIdx=None):
  """
  Function that analyses the chemistry in a similar way to chemanalysis.pro.

  Parameters
  ----------

  species : str
    The species name one wants to analyze.

  model : :class:`prodimopy.read.Data_ProDiMo`
    the |prodimo| model data.

  """
  chemistry=Chemistry(None)

  # has to be from the particular model.
  if directory is None:
    directory=model.directory

  if name==None:
    name=model.name

  start=timer()
  # Read the netork
  # cnet=pchemnet.ReactionNetworkPout(modeldir=directory)
  # print(cnet)
  # print("")

  speciesidx=model.spnames[species]

  if td_fileIdx is not None:
    # FIXME: that might not work if one overwrite filenameChemistry
    filenameChemistry=filenameChemistry.replace(".out","_"+td_fileIdx+".out")
  fchem,dummy=_getfile(filenameChemistry,directory,None)
  if fchem is None: return None
  # skip first line
  fchem.readline()

  # stores all the formation reaction indices and rates for each grid point
  gridf=np.empty((model.nx,model.nz,2),dtype=np.ndarray)
  gridd=np.empty((model.nx,model.nz,2),dtype=np.ndarray)
  totfrate=np.zeros((model.nx,model.nz))  # total formation rate at each point)
  totdrate=np.zeros((model.nx,model.nz))  # total formation rate at each point)
  fidx=list()  # indices of all unique formation reactions
  didx=list()  # indices of all unique destruction reactions
  fidxcount=list()  # count how often the reaction occours over the whole grid
  didxcount=list()  # count how often the reaction occours over the whole grid

  # now read the Reaction network
  # TODO: move some of this to the ReactionNetwork class to make it more general
  # e.g. select routine which gets a product species as input and returns all the
  # formation reatoins (a list, or a network)
  chemnet=pcnet.ReactionNetworkPout(modeldir=directory)
  for line in fchem:
    fields=line.split()
    # not relevant
    if int(fields[2])!=speciesidx: continue

    ix=int(fields[0])-1
    iz=int(fields[1])-1
    reacidx=int(fields[3])
    rate=float(fields[4])
    if gridf[ix,iz,0] is None:
      gridf[ix,iz,0]=np.array([],dtype=np.int)
      gridf[ix,iz,1]=np.array([])

    if gridd[ix,iz,0] is None:
      gridd[ix,iz,0]=np.array([],dtype=np.int)
      gridd[ix,iz,1]=np.array([])

    # get the reaction and see if it is formation or destruction
    reac=chemnet.reactions[reacidx-1]  # fortran starts at 1, python at 0
    if species in reac.products:  # formation reaction
      isort=np.searchsorted(-gridf[ix,iz,1],rate)  # with the minus a descending order is achieved
      gridf[ix,iz,0]=np.insert(gridf[ix,iz,0],isort,reacidx)
      gridf[ix,iz,1]=np.insert(gridf[ix,iz,1],isort,rate)
      totfrate[ix,iz]+=rate
      if not reacidx in fidx:
        fidx.append(reacidx)
        fidxcount.append(0)  # the counter
      else:
        fidxcount[fidx.index(reacidx)]+=1  # the counter
    elif species in reac.reactants:  # formation reaction
      isort=np.searchsorted(-gridd[ix,iz,1],rate)  # with the minus a descending order is achieved
      gridd[ix,iz,0]=np.insert(gridd[ix,iz,0],isort,reacidx)
      gridd[ix,iz,1]=np.insert(gridd[ix,iz,1],isort,rate)
      totdrate[ix,iz]+=rate
      if not reacidx in didx:
        didx.append(reacidx)
        didxcount.append(0)  # the counter
      else:
        didxcount[didx.index(reacidx)]+=1  # the counter
    else:
      raise ValueError('Something is really wrong ...')

  sortidx=np.flip(np.array(fidxcount).argsort())
  # fidx.sort(key=lambda x: fidxcount.index(x),reverse=True)
  fidx=np.array(fidx)[sortidx]
  sortidx=np.flip(np.array(didxcount).argsort())
  didx=np.array(didx)[sortidx]

  # didx.sort(key=didxcount,reverse=True)

  chemistry.species=species
  chemistry.gridf=gridf
  chemistry.gridd=gridd
  chemistry.fridxs=fidx
  chemistry.dridxs=didx
  chemistry.totfrate=totfrate
  chemistry.totdrate=totdrate
  # FIXME:
  # that might be a bit of an overkill, because it includes all Reactoins of
  # the network, not only the ones for this particular species.
  chemistry.chemnet=chemnet

  if to_txt:
    output_chem_fname=directory+'/chemistry_reactions_'+species+'.txt'
    if td_fileIdx is not None:
      output_chem_fname=output_chem_fname.replace(".txt","_"+td_fileIdx+".txt")
    f=open(output_chem_fname,'w')
    f.writelines("-------------------------------------------------------\n")
    f.writelines("formation and destruction reactions \n")
    f.writelines("species: "+species+"\n\n")
    f.writelines("Formation reactions\n")
    for i,ridx in enumerate(chemistry.fridxs):
      f.writelines(chemistry.reac_to_str(chemnet.reactions[ridx-1],i+1))
      f.writelines('\n')
    f.writelines("\n\n")
    f.writelines("Destruction reactions\n")
    for i,ridx in enumerate(chemistry.dridxs):
      f.writelines(chemistry.reac_to_str(chemnet.reactions[ridx-1],i+1))
      f.writelines('\n')
    f.writelines("-------------------------------------------------------\n")
    f.close()
    print("Writing information to: "+output_chem_fname)

    # also print it to stdout
    with open(output_chem_fname) as f:
      print(f.read())

  print("INFO: Calc time: ","{:4.2f}".format(timer()-start)+" s")
  return chemistry


def reac_rates_ix_iz(model,chemana,ix=None,iz=None,locau=None):
  """
  Function that analyses the chemana manually via a point-by-point
  analysis for a given species.
  Start by entering the point-coordinates ix,iz, then you can have a look
  at the most important formation and destruction rates.

  Parameters
  ----------

  model : :class:`prodimopy.read.Data_ProDiMo`
    the model data

  chemana : class:`prodimopy.read.Chemistry`
    data resulting from `prodimopy.read.analise_chemistry` on a single species

  ix : int
    ix corresponding to desired radial location in grid, starting at 0

  iz : int
    iz corresponding to desired radial location in grid, starting at 0

  locau : array_like
    the desired coordinates in au [x,z]. The routine then finds the closest
    grid point for those coordinates.

  """

  if locau is not None:
    ix=np.argmin(np.abs(model.x[:,0]-locau[0]))
    iz=np.argmin(np.abs(model.z[ix,:]-locau[1]))

  if ix is None or iz is None:
    print("Please provide either ix,iz or locau!")
    return

  print("Analysing point x=",str(model.x[ix,iz])+" au z="+str(model.z[ix,iz])+" au")

  print('      Detailed reaction rates for: %10s'%chemana.species)
  print('------------------------------------------------------------------------------------------------------')

  print('                    grid point = %i       %i'%(ix,iz))
  print('        r,z [au] (cylindrical) = %.3f  %.4f'%(model.x[ix,iz],model.z[ix,iz]))
  print('               n<H>,nd [cm^-3] = %.1e  %.1e'%(model.nHtot[ix,iz],model.nd[ix,iz]))
  print('                Tgas,Tdust [K] = %.1e  %.1e'%(model.tg[ix,iz],model.td[ix,iz]))
  print('                 AV_rad,AV_ver = %.1e  %.1e'%(model.AVrad[ix,iz],model.AVver[ix,iz]))
  print('          %10s'%chemana.species+' abundance = %e'%model.getAbun(chemana.species)[ix,iz])
  print('------------------------------------------------------------------------------------------------------')
  print(' Total form. rate [cm^-3 s^-1] = {:10.2e}'.format(chemana.totdrate[ix,iz]))
  for i,ridx in enumerate(chemana.gridf[ix,iz,0]):
    print(chemana.reac_to_str(chemana.chemnet.reactions[ridx-1],list(chemana.fridxs).index(ridx)+1,rate=chemana.gridf[ix,iz,1][i]))
  print('------------------------------------------------------------------------------------------------------')
  print(' Total dest. rate [cm^-3 s^-1] = {:10.2e}'.format(chemana.totdrate[ix,iz]))
  for i,ridx in enumerate(chemana.gridd[ix,iz,0]):
    print(chemana.reac_to_str(chemana.chemnet.reactions[ridx-1],list(chemana.dridxs).index(ridx)+1,rate=chemana.gridd[ix,iz,1][i]))
  print('------------------------------------------------------------------------------------------------------')
  print("")


def _flux_Wm2toJykms(flux,frequency):
  '''
  Converts a flux from W m^-2 to Jy km/s

  Parameters
  ----------
  flux: float
    the flux in units of [W m^-2]

  frequency: float
    the frequency of the flux in [GHz]

  Returns
  -------
  float
    The flux of the line. `UNIT: Jansky km s^-1`
  '''
  res=flux*u.Watt/(u.m**2.0)
  ckm=const.c.to('km/s')

  res=(res).to(u.Jansky,equivalencies=u.spectral_density(frequency*u.GHz))

  return (res*ckm).value


def _getfile(filename,directory=None,tarfile=None,binary=False):
  '''
  Utility function to open a particular file from a ProDiMo model.
  '''
  pfilename=filename

  if tarfile is not None:
    if directory is not None and directory!=".":
      pfilename=directory+"/"+filename

    tararchive=tar.open(tarfile,"r")
    if binary:
      f=tararchive.extractfile(pfilename)
    else:
      f=io.TextIOWrapper(tararchive.extractfile(pfilename))
  else:
    if directory is not None:
      pfilename=directory+"/"+filename

    try:
      if binary:
        f=open(pfilename,'rb')
      else:
        f=open(pfilename,'r')
    except:
      f=None

  if f is None:
    print(("WARN: Could not open "+pfilename+"!"))
  else:
    print("READ: Reading File: ",pfilename," ...")
  return f,pfilename


###############################################################################
# For testing
if __name__=="__main__":
    # import sys
    # import phxpy.io
#     import time
#
#     pd=read_prodimo("/home/rab/MODELS/XRTPaperNew/TEST_full")
#     print pd
#     print pd.nmol[pd.nx-1,0,pd.spnames["N2#"]]
#     print pd.gas.energy/1000.0
#
#     start=time.time()
#     read_lineEstimates("/home/rab/MODELS/XRTPaperNew/TEST_full", pd)
#     print "Time: ",time.time()-start
#
#     line=pd.getLineEstimate("N2H+", 1000.0)
#     line=pd.getLineEstimate("N2H+", 1000.0)
#     print line

    # lines=pd.selectLineEstimates("N2H+")
    # print len(lines)

  tdir="../testdata"

  data=read_prodimo(tdir)

  linesObs=read_lineObs(tdir,len(data.lines))
  print(data.lines[0])
  print(data.lines[1])
  print(linesObs[0])

  profile=read_lineObsProfile(tdir+"/LineProfile_CO_21.dat")
  print(profile)
  print(profile.flux)
  print(profile.velo)

