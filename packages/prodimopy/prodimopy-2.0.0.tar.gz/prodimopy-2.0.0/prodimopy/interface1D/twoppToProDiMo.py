import math
import os

import twopoppy

import numpy as np
import prodimopy.interface1D.infile as pinfile


def twopp_to_ProDiMo(twopp_res,fname,timeidx=-1):
  '''
  Interface from two-pop-py to ProDiMo. Does the necessary post-processing steps
  and produces the ProDiMo input file (`fname`)

  Parameters
  ----------

  twopp_res : :class:`~twopoppy.results.results`
    The results of a two-pop-py run.

  fname : str
    The filename (or path) for the ProDiMo input file.

  timeidx : int
    index of the two-pop-py time snapshot to use. DEFAULT: the last one.

  '''

  sig_sol=pp_tpp_results(twopp_res,timeidx)

  # define a cut off in radius ... to avoid the empty stuff at the end
  # that should be roughly at NH_ver=1.e20 cm^-2 as in ProDiMo
  li=np.argmin(np.abs(twopp_res.sigma_g[timeidx,:]-1.e-4))

  print()
  print("Write input file for ProDiMo to "+fname)
  print()

  # write the input file
  pinfile.write(fname,
                  twopp_res.x[0:li],
                  twopp_res.sigma_g[timeidx,0:li],
                  twopp_res.sigma_g[timeidx,0:li]/twopp_res.sigma_d[timeidx,0:li],
                  agrid=twopp_res.a,
                  fsize=sig_sol[:,0:li])


def pp_tpp_results(twopp_res,timeidx=-1):
  '''
  Some post-processing of the two-pop-py results for ProDiMo.
  Also writes out additional results from two-pop-py (to the directory set via the `twopp_res` object.

  TODO: document the additional output files.

  Parameters
  ----------
  twopp_res : :class:`~twopoppy.results.results`
    The results of a two-pop-py run.

  a_max : array_like(float,ndim=1)
    The maximum grain sizes as a function of radius from the grain size distribution recontruction
    of two-pop-py.
    `UNIT:` cm

  timeidx : int
    the index of the two-pop-py time snapshot that should be used.


  Returns
  -------
  array_like(float,ndim=2)
    grain size distribution which shape `(na,nx)`, where `na` is the len of the grain size grid
    and `nx` is the len of the radial grid of two-pop-py. The size distribution is provide in
    surface density per grain size bin, just like in two-pop-py.

  '''
  # Reconstruct the size distribution again to get all information (functionality from two-pop-py)
  sig_sol,a_max,r_f,sigma_f,sigma_omf,sigma_ddd=twopoppy.distribution_reconstruction.reconstruct_size_distribution(
  twopp_res.x,twopp_res.a,twopp_res.timesteps[timeidx],
  twopp_res.sigma_g[timeidx,:],twopp_res.sigma_d[timeidx,:],
  twopp_res.args.alpha*np.ones(twopp_res.args.nr),
  twopp_res.args.rhos,twopp_res.T,twopp_res.args.mstar,
  twopp_res.args.vfrag,
  a_0=twopp_res.args.a0,
  estick=twopp_res.args.estick)

  # do some post-processing and write additional files as output

  # amax=amin can cause problems in ProDiMo
  # take the next largest
  a_max[a_max<twopp_res.args.a0]=twopp_res.a[1]

  # calculate a_eq according to paper in the most simple way (Eq. 30 in 2015 paper)
  # use approximation of the stokes number.
  # FIXME: very primitive approximation
  a_trans=calc_atrans(twopp_res,a_max,timeidx)

  # Normalization is now done withing ProDiMo
  # normsizedist=sizedist_from_sigmaa(twopp_res.a,sig_sol)

  np.savetxt(twopp_res.args.dir+os.sep+'a_eq.dat',a_trans)
  np.savetxt(twopp_res.args.dir+os.sep+'a_max.dat',a_max)
  np.savetxt(twopp_res.args.dir+os.sep+'sigma_f.dat',sigma_f)
  np.savetxt(twopp_res.args.dir+os.sep+'sigma_omf.dat',sigma_omf)
  np.savetxt(twopp_res.args.dir+os.sep+'sigma_ddd.dat',sigma_ddd)
  # np.savetxt(twopp_res.args.dir + os.sep + 'normsizedist.dat', normsizedist)

  return sig_sol


def calc_atrans(twopp_res,a_max,timeidx=-1):
  '''
  Calculate the transition grain radius as a function of radius for the small and large population
  according to the two-pop-py paper in the most simple way (Eq. 30-32 in Birnstiel+ (2012))

  FIXME: uses the most simple approximation, might not be valid

  Parameters
  ----------

  twopp_res : :class:`~twopoppy.results.results`
    The results of a two-pop-py run.

  a_max : array_like(float,ndim=1)
    The maximum grain sizes as a function of radius from the grain size distribution recontruction
    of two-pop-py.
    `UNIT:` cm

  timeidx : int
    the index of the two-pop-py time snap shot that should be used.

  Returns
  -------
  array_like(float,ndim=1)
    The transition radius that separates the small and large populatoin as function
    of radius (shape `nx`). `UNIT: cm`
  '''

  # use approximation of the stokes number.
  Steq=twopp_res.args.alpha/2.0
  a_trans=Steq*(2.0*twopp_res.sigma_g[timeidx,:]/math.pi/twopp_res.args.rhos)
  a_trans[a_trans<twopp_res.args.a0]=twopp_res.args.a0
  a_trans[a_trans>a_max]=a_max[a_trans>a_max]

  return a_trans


def construct_2pop_sdd(twopp_res,a_trans,a_max):
  '''
  Constructs a small and large dust surface density profile from the two-pop-py results.

  This routine is only for comparison, on should use the interface with the full size
  distribution.

  Parameters
  ----------

  twopp_res : :class:`~twopoppy.results.results`
    The results of a two-pop-py run.

  a_trans : array_like(float,ndim=1)
    The transition dust grain radius that separates the small from from the large population at
    each radial grid point. Must have the same len as the two-pop-py radial grid (`twopp_res.x`)
    `UNIT:` cm

  a_max : array_like(float,ndim=1)
    The maximum dust grain radius that at each radial grid point.
    Must have the same len as the two-pop-py radial grid (`twopp_res.x`).
    `UNIT:` cm

  Returns
  -------

  array_like(float,ndim=1): small dust surface density profile `UNIT:` |gcm^-2|
  array_like(float,ndim=1) : large dust surface density profile `UNIT:` |gcm^-2|

  '''
  sddsmall=twopp_res.x[:]*0.0
  sddlarge=twopp_res.x[:]*0.0
  sddsmall[:]=1.e-100
  sddlarge[:]=1.e-100

  # for each r we have a a_eq now, so separate the small and large one for each r
  for ix in range(len(twopp_res.x)):
    itrans=np.argmin(np.abs(twopp_res.a-a_trans[ix]))
    sddsmall[ix]=np.sum(twopp_res.sig_sol[0:itrans,ix],axis=0)
    sddlarge[ix]=np.sum(twopp_res.sig_sol[itrans:-1,ix],axis=0)

#    print("{:5.3f} ".format(twopp_res.x[ix]/AU),itrans,("{:5.3e}  "*6).format(twopp_res.a[itrans],a_max[ix],sddsmall[ix],sddlarge[ix],twopp_res.sigma_d[-1,ix],
#                                  (sddsmall[ix]+sddlarge[ix])/twopp_res.sigma_d[-1,ix]))

  sddsmall[sddsmall<1.e-100]=1.e-100
  sddlarge[sddsmall<1.e-100]=1.e-100

  return sddsmall,sddlarge


def sizedist_from_sigmaa(a_grid,sdda):
  '''
  Creates a normalized grain size distribution from the given grain size grid and
  the according dust surface densities.

  This one is not used anymore for the 1D interface to ProDiMo. However, it might be usefull
  for test.

  Parameters
  ----------
  a_grid : array_like(float,ndim=1)
    The grain size grid.
    `UNIT:` cm

  sdda : array_like(float,ndim=2)
    The dust surface density per grain size as function of radius with
    shape(len(a_agrid),len(twopp_res.x))
    `UNIT:` `UNIT:` |gcm^-2|

  Returns
  -------
  array_like(float,ndim=2)
    normalized size distribution which shape `(na,nx)`, where `na` is the len of the grain size grid
    and `nx` is the len of the radial grid of two-pop-py.

  '''

  na=len(a_grid)
  nx=len(sdda[0,:])

  # calculate the integration weights in the same way as is done in ProDiMo
  aweights=np.zeros(na)
  for ia in range(1,na):
    da=0.5*(a_grid[ia]-a_grid[ia-1])
    aweights[ia]=aweights[ia]+da
    aweights[ia-1]=aweights[ia-1]+da

  # calculate the number density per grain 1/cm^2 for each size bin
  ndda=np.zeros(sdda.shape)
  for ia in range(na):
    # just use one, assuming the the particle mass density is the same for all particles
    ndda[ia,:]=sdda[ia,:]/(4.0*math.pi/3.0*a_grid[ia]**3)/aweights[ia]

  for ix in range(nx):
    ndda[:,ix]=ndda[:,ix]/np.sum(ndda[:,ix]*aweights)

  # check if everything is fine
  import scipy.integrate as integrate
  for ix in range(nx):
    if np.abs(integrate.trapz(ndda[:,ix],a_grid)-1.0)>1.e-5:
      print("Inaccurate at ",ix)

  return ndda
