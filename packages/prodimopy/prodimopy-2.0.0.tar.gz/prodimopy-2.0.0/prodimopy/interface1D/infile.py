from scipy import interpolate

import astropy.units as u
import numpy as np

# FIXME: not nice, but use the au to cm conversion constant from ProDiMo
# just to be consisten
autocm=1.495978700e+13


def writeV1(fname,r,sdg,g2dratio):
  '''
  Produces an input file for the 1D interface (version 1) to ProDiMo.

  All array input parameters need to have the same length.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file.

  r : array_like(float,ndim=1)
    radial gridpoints (distance to the star) for the disk.
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The total gas surface density profile (the sum of both sides of the disk)
    `UNIT:` |gcm^-2|

  g2dratio: array_like(float,ndim=1)
    The gas to dust mass ratio as function of radius.

  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n")
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# normalization factor\n")
  fp.write("-2.0\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   gas to dust mass ratio \n")

  # FIXME: workaround
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for rl,pl,g2dl in zip(r,sdg,g2dratio):
      fp.write("{:18.10e}".format(rl))
      fp.write(" ")
      fp.write("{:18.10e}".format(pl))
      fp.write(" ")
      fp.write("{:18.10e}".format(g2dl))
      fp.write("\n")

  fp.close()


def writeV2(fname,r,sdg,sdd_small,sdd_large,amax):
  '''
  Produces an input file for the 1D interface (version 2) to ProDiMo.

  All array input parameters need to have the same length.

  This is format that is used for E. Vorobyovs code.

  However, one should use the newer more flexible, (but compatible) format.
  see :meth:`~writeV3`


  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file.

  r : array_like(float,ndim=1)
    The radius array.
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile.
    `UNIT:` |gcm^-2|

  sdd_small : array_like(float,ndim=1)
    The dust surface density of the small grain dust popoulation
    `UNIT:` |gcm^-2|

  sdd_large : array_like(float,ndim=1)
    The dust surface density of the large grain dust popoulation
    `UNIT:` |gcm^-2|

  amax : array_like(float,ndim=1)
    the maxium grain size at each radial grid point
    `UNIT:` cm

  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n")
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("2\n")
  fp.write("# R [au]   gas surface density [gcm^-2]   sd dust small [gcm^-2]   sd dust large [gcm^-2]   amax [cm]\n")

  # FIXME: workaround
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for rl,pl,sdsmalll,sdlargel,amaxl in zip(r,sdg,sdd_small,sdd_large,amax):
    fp.write("{:18.10e}".format((rl*u.cm).to(u.au).value))
    fp.write(" ")
    fp.write("{:18.10e}".format(pl))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdsmalll))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdlargel))
    fp.write(" ")
    fp.write("{:18.10e}".format(amaxl))
    fp.write("\n")

  fp.close()


def writeV3(fname,r,sdg,sdd_small,sdd_large,amin,atrans,amax):
  '''
  Produces an input file for the 1D interface (version 3) to ProDiMo.

  All array input parameters need to have the same length.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file.

  r : array_like(float,ndim=1)
    The radius array.
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile.
    `UNIT:` |gcm^-2|

  sdd_small : array_like(float,ndim=1)
    The dust surface density of the small grain dust popoulation
    `UNIT:` |gcm^-2|

  sdd_large : array_like(float,ndim=1)
    The dust surface density of the large grain dust popoulation
    `UNIT:` |gcm^-2|

  amin : array_like(float,ndim=1)
    the minimum grain size at each radial grid point
    `UNIT:` cm

  atrans : array_like(float,ndim=1)
    the transition radius at each radial grid point
    `UNIT:` cm

  amax : array_like(float,ndim=1)
    the maxium grain size at each radial grid point
    `UNIT:` cm

  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n")
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("3\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   sd dust small [gcm^-2]")
  fp.write("   sd dust large [gcm^-2]   amin [cm]   atrans [cm]   amax [cm]\n")

  # FIXME: workaround
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for rl,pl,sdsmalll,sdlargel,aminl,atransl,amaxl in zip(r,sdg,sdd_small,sdd_large,amin,atrans,amax):
    fp.write("{:18.10e}".format(rl))
    fp.write(" ")
    fp.write("{:18.10e}".format(pl))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdsmalll))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdlargel))
    fp.write(" ")
    fp.write("{:18.10e}".format(aminl))
    fp.write(" ")
    fp.write("{:18.10e}".format(atransl))
    fp.write(" ")
    fp.write("{:18.10e}".format(amaxl))
    fp.write("\n")

  fp.close()


def writeV4(fname,r,sdg,g2dratio,agrid,fsize):
  '''
  Produces an input file for the 1D interface (version 4) to ProDiMo.

  This routine requires a full size distribution given by the grain size grid
  `a` and the size distribution `fsize`. `fsize` should contain the surface density
  as function of radius for each grain size bin.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file.

  r : array_like(float,ndim=1)
    The radius array.
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile.
    `UNIT:` |gcm^-2|

  g2dratio: array_like(float,ndim=1)
    The gas to dust mass ratio as function of radius.

  agrid : array_like(float,ndim=1)
    The grain size grid.
    `UNIT:` cm

  fsize : array_like(float,ndim=2)
    The grain size distribution given as surface density per grain size bin.
    The dimension is (`len(a),len(r)`). `UNIT:` |gcm^-2|

  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n")
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("4\n")
  fp.write("# number of grain size bins \n")
  fp.write(str(len(agrid))+"\n")
  fp.write("# grain size grid [cm] \n")
  fp.write(("{:18.10e}"*len(agrid)).format(*agrid))
  fp.write("\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   gas to dust mass ratio   fsize [gcm^-2] \n")

  # FIXME: workaround
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for i in range(len(r)):
    fp.write("{:18.10e}".format(r[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdg[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(g2dratio[i]))
    fp.write(" ")
    fp.write(("{:18.10e}"*len(agrid)).format(*fsize[:,i]))
    fp.write("\n")
  fp.close()


def write(fname,r,sdg,g2dratio,agrid=None,fsize=None,amin=None,amax=None,elabunFacs=None):
  '''
  Produces an input file for the general 1D interface to ProDiMo.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file.

  r : array_like(float,ndim=1)
    The radius array.
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile.
    `UNIT:` |gcm^-2|

  g2dratio: array_like(float,ndim=1)
    The gas to dust mass ratio as function of radius.

  agrid : array_like(float,ndim=1)
    The grain size grid. If `None` (default) no size distribution is included.
    Only required if fsize is used. `UNIT:` cm

  fsize : array_like(float,ndim=2)
    The grain size distribution given as surface density per grain size bin.
    If `None` (default) no size distribution is included.
    The dimension is (`len(a),len(r)`). OPTIONAL, `UNIT:` |gcm^-2|

  amin : array_like(float,ndim=1)
    the minimum grain size at each radial grid point.
    OPTIONAL, `UNIT:` cm

  amax : array_like(float,ndim=1)
    the maximum grain size at each radial grid point.
    OPTIONAL, `UNIT:` cm

  elabunFac : dictionary
    Dictionary with correction factors for each Element that should be considered.
    Each entry has to have the Element name (as in ProDiMo) as key and an
    array of len(r) with the correctoin factor (i.e. 1 means no change). Only the
    elements that should be changed need to be included. OPTIONAL.

  '''

  nfields=3

  usefsize=True
  if agrid is None or fsize is None:
    usefsize=False

  nelem=0
  if elabunFacs is not None:
    nelem=len(elabunFacs)

  # make some checks already heare
  if (usefsize and (amin is not None or amax is not None)):
    print("ERROR: It is not possible to combine amin or amax with a full size distribution (fsize)")
    return

  fp=open(fname,"w")
  fp.write(str(len(r))+" ! NXX    number of radii\n")

  colnames="R SIGMAG G2D"
  header="# R [cm]   gas surface density [gcm^-2]   gas to dust mass ratio"

  # prepare the column entries. Do not switch the order. Has to be the
  # same as in the READ_1D (interface1D.f) routine of ProDiMo.
  if usefsize:
    print("INFO: Dust size distribution FSIZE is included.")
    fp.write(str(len(agrid))+" ! NSIZE  number of grain size bins and grid \n")
    fp.write(("{:18.10e}"*len(agrid)).format(*agrid))
    fp.write("\n")
    colnames=colnames+" FSIZE"
    header=header+" fsize [gcm^-2]"
    nfields+=1

  if amin is not None:
    print("INFO: Minimum dust grain size AMIN is included.")
    colnames=colnames+" AMIN"
    header=header+"  amin [cm]"
    nfields+=1

  if amax is not None:
    print("INFO: Maximum dust grain size AMAX is included.")
    colnames=colnames+" AMAX"
    header=header+"  amax [cm]"
    nfields+=1

  if nelem>0:
    print("INFO: Element abundance correction factors ELEM_* are included.")
    fp.write(str(nelem)+" ! NELEM  number of consider elements \n")
    for elname in elabunFacs.keys():
      colnames=colnames+" ELEM_"+elname.strip()
      header=header+"   ELEM_"+elname.strip()
      nfields+=1
  # fp.write("! NCOL   number of columns and column names")

  fp.write(str(nfields)+" ! NFIELDS   number of quantities and their names\n")
  fp.write(colnames+"\n")
  fp.write(header+"\n")

  # FIXME: workaround
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for i in range(len(r)):
    fp.write("{:18.10e}".format(r[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdg[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(g2dratio[i]))
    # write the optional column. Orders has to be the same as given in ! NFIELDS
    if usefsize:
      fp.write(" ")
      fp.write(("{:18.10e}"*len(agrid)).format(*fsize[:,i]))

    if amin is not None:
      fp.write(" ")
      fp.write(("{:18.10e}").format(amin[i]))

    if amax is not None:
      fp.write(" ")
      fp.write(("{:18.10e}").format(amax[i]))

    if nelem>0:
      for fac in elabunFacs.values():
        fp.write(" ")
        fp.write(("{:18.10e}").format(fac[i]))

    fp.write("\n")
  fp.close()

  print("INFO: Generated input file "+fname.strip())


def generate_sdd_twopop(twopp_res,atrans):
  ''''
  Generates a small and large dust surface density profile for the given atrans, from
  the two-pop-py results.

  Parameters
  ----------

  twopp_res : two-pop-py results

  atrans : array_like(float,ndim=1)
    The transition radius from the small to the large population.
    `UNIT:` cm

  '''

  sdsmall=twopp_res.x[:]*0.0
  sdlarge=twopp_res.x[:]*0.0
  sdsmall[:]=1.e-150
  sdlarge[:]=1.e-150

  # for each r we have atrans now, so separate the small and large one for each r
  for ix in range(len(twopp_res.x)):
    itrans=np.argmin(np.abs(twopp_res.a-atrans[ix]))
    sdsmall[ix]=np.sum(twopp_res.sig_sol[0:itrans,ix],axis=0)
    sdlarge[ix]=np.sum(twopp_res.sig_sol[itrans:-1,ix],axis=0)

#    print("{:5.3f} ".format(twopp_res.x[ix]/AU),itrans,("{:5.3e}  "*6).format(twopp_res.a[itrans],a_max[ix],sdsmall[ix],sdlarge[ix],twopp_res.sigma_d[-1,ix],
#                                  (sdsmall[ix]+sdlarge[ix])/twopp_res.sigma_d[-1,ix]))

  sdsmall[sdsmall<1.e-100]=1.e-100
  sdlarge[sdlarge<1.e-100]=1.e-100

  return sdsmall,sdlarge


def generate_from_obsradprof(model,mradprof,oradprof,distance,asmall=None,
                              apowfac=None,outfile=None,rinexclude=None):
  """
  Generates a 1D infile (version1) by using the observed radial intensity profile
  for the continuum. The observed profiles is compared to the modelled one
  to calculate a correction for the dust surface density (gas to dust ratio).
  From this a new 1D input file (with a different gas to dust ratio) is generated.

  .. todo::

    Applying this method can introduce some numerical errors due to
    a lot of conversions and interpolations. However, these should be
    <0.5%. And as this routint is used for fitting it should not be an issue.
    However, the error most likely comes from calculating the gas and dust
    surface densities when a ProDiMo model is read (those are not calculated
    within ProDiMo). So maybe this :func:`~prodimopy.read.calc_surfd`
    should be made more accurate.

  .. note:: Further Ideas

    Focus the fitting on the grain size that is best traced by the wavelength
    of the observations. One could use a gaussian to centered at this grain
    size to estimate the correction factor. However, this is probably more
    useful if mulitple images are available for the fitting.

    Use asmall and apowfac together. The apowfac method is then only applied
    to the grian sizes < asmall. Other anlternative: normalize the apowfac
    function to a grain size of choice (i.e. the one that is most sensitive to the
    wavelength of the observations. And use it to decrease the correctoin for
    grain < asmall and increase the correction for grains > asmall.


  Parameters
  ----------

  model : :class:`~prodimopy.read.Data_ProDiMo`
    the ProDiMo model data (the initial model)

  mradprof : :class:`~prodimopy.read_casasim.RadialProfile`
    The modelled radial profile (the initial one).

  oradprof : :class:`~prodimopy.read_casasim.RadialProfile`
    The observed radial profile.

  distance : float
    the distance of the object in au. Is required to convert the radial
    profiles to au.

  asmall : float
    A grain size in micron. If this is set only the surfacedensities of
    grains with sizes > asmall are adapated all other remain unchanged.
    This can only work if the model has the output dust_sigmaa.out.
    This mode uses :func:`~infile.writeV4` to write the 1D input file.

  apowfac : float
    If apow is set the correction factor becomes a function of the
    dust size. For the largest grain size the correction factor stays the
    same but for all other grains the correction factor is reduced depending
    on the grain size. apow needs to be positive.
    apowfac cannot be used with asmall together.

  outfile : str
    the path/filename of the output file (the 1D input file). Default is
    `sdprofile.in` within the directory of the provided PRoDiMo model.

  rinexclude : float
    within this radius (in au) the surface density profile is not adapted.
    This means for r < rinexclude the gas to dust ratio remains unaffected.

  """

  if outfile is None:
    model.directory+"/sdprofile_new.in"

  # use the error (rms) to define a kind of upper limit for the adaptation
  # this avoids problems with e.g. negative numbers in the observed radial profile.
  # also it reduces fitting within the error
  oflux=np.maximum(oradprof.flux,oradprof.flux_err/2.0)

  # calculate the factor for the dust surface density correction
  frac=oflux/mradprof.flux

  # Interpolate the fraction onto the model grid
  # need to convert arcsecond to au (for the model). So this only works for properly deprojected radial profiles.
  fracr=oradprof.arcsec*distance

  interp=interpolate.interp1d(fracr,frac,bounds_error=False,fill_value="extrapolate",kind="quadratic")
  modelr=model.x[:,0]
  fraci=interp(modelr)

  # beyond the image it is undefined, to avoid that the whole outer disk is fitted to the rms, we use
  # the fraction of the last valid point for the larger radii
  fraci[modelr>fracr[-1]]=frac[-1]

  # exclude some part of the innner disk if some radius is given.
  if rinexclude is not None:
    fraci[modelr<rinexclude]=1.0

  if asmall is None and apowfac is None:
    # now calculate the new dust surface density, leaving the gas surface density untouched.
    dustsd=model.sdd[:,0]*fraci
    # factor two is important as the gas surface density in the input file is defined as the total disk
    # gas surface density. In ProDiMo it is only for half of the disk.
    writeV1(outfile,modelr*autocm,model.sdg[:,0]*2.0,model.sdg[:,0]/dustsd)
  else:  # the more sophisticated methods
    if model.dust.sigmaa is None:
      print("Error: Cannot use asmall/apowfac because the model has no dust.sigmaa.")
      return

    # make a copy, because we do not want to change the original
    sigmaa=np.copy(model.dust.sigmaa)

    if asmall is not None:
      idxasmall=np.argmax(model.dust.asize>asmall)
      # print(idxasmall,model.dust.asize[idxasmall])
      for i in range(idxasmall,model.dust.nsize):
        sigmaa[i,:]=model.dust.sigmaa[i,:]*fraci
    else:
      # make a normalize function which is used to tweak the correction factor
      afunc=(model.dust.asize**apowfac)
      afunc=afunc/afunc[-1]

      for i in range(model.dust.nsize):
        # with this expression the correction faci can be reduced depending
        # on grain size. For the largest grain size fraci remains the same.
        # the smaller the grain size fraci gets close to 1.0 (or remains 1)
        sigmaa[i,:]=model.dust.sigmaa[i,:]*(1.0+(fraci-1.0)*afunc[i])

    dustsd=np.sum(sigmaa,axis=0)
    # factor two is important as the surface densities in the input file is defined as the total disk
    # surface density. In ProDiMo it is only for half of the disk.
    writeV4(outfile,modelr*autocm,model.sdg[:,0]*2.0,model.sdg[:,0]/dustsd,
            (model.dust.asize*u.micron).to(u.cm).value,sigmaa*2.0)

  print("New 1D input file written to "+outfile)

