"""
.. module:: utils_casasim

.. moduleauthor:: Ch. Rab

Requires CASA 6 python installation to work.

"""

import math
import os

import astropy.io.fits as fits
import casatasks as ct
from casatools import image as iatool
import numpy as np


def radprof(infile,incl,PA,fracbeam=0.33,rms=None,r_out=None):
  """
  Make an azimuthally averaged deprojected radial profile of an 2D fits image.

  Used casatasks to make the radial profiles.

  The radial gridding is determined by the beam size. By default 1/3 of the beam
  size are used to define the width of one annulus.

  The information of the center of the image, beam sizes etc. are read from the
  fits header. So they have to be there. Ususullay that routine works fine with
  images that can be opened within casa.


  incl and PA have to be in degree.

  Parameters
  ----------

  infile : str
    The path/filename of the fits file to use.

  incl : float
    The inclination in degrees

  PA : float
    The position angle in degrees

  fracbeam : float
    What fraction of the beam should be used for the radial spacing.
    Can also be >1. DEFAULT: 0.33

  rms : float
    rms value of the image. Is used to determine the error.
    DEFAULT: `None` (no error estimate)

  r_out : float
    the maximum outer radius use for the radial profile in arcsec.
    Default: `None` (whole image is used)


  Returns
  -------
  r,flux,fluxerr : array_like(ndim=1)
    Three arrays with the radius (in arcsec) the flux at each radius (units of the Image) and
    the error for the flux.

  """

  if not os.path.isfile(infile):
    print("ERROR: Input fitsfile "+infile+" not found.")
    return None

  RA=ct.imhead(imagename=infile,mode='get',hdkey='CRVAL1')
  RA=str(RA["value"])+RA["unit"]
  DEC=ct.imhead(imagename=infile,mode='get',hdkey='CRVAL2')
  DEC=str(DEC["value"])+DEC["unit"]
  print("CENTER:",RA,DEC)

  BMAJ=ct.imhead(imagename=infile,mode='get',hdkey='BMAJ')
  BMIN=ct.imhead(imagename=infile,mode='get',hdkey='BMIN')
  print("BEAM: ",BMAJ["value"],BMAJ["unit"],BMIN["value"],BMIN["unit"])
  bmaj=BMAJ["value"]
  bmin=BMIN["value"]
  bwidth=(bmaj+bmin)/2.0

  # assume it is in degree
  CDELT1=ct.imhead(imagename=infile,mode='get',hdkey='CDELT1')
  print("CDELT1: ",CDELT1["value"],CDELT1["unit"])
  # convert to arcsec
  pix_to_arcsec=np.abs(CDELT1["value"])/(math.pi/180.0)*3600.0
  print("PIXSCALE: ",pix_to_arcsec," arcsec")

  # assume a certain fraction of the beam as the width
  width=fracbeam*bwidth
  print("WIDTH: ",str(width)+" arcsec")

  barea=math.pi*bmaj*bmin/(4.0*math.log(2.0))
  bwidthpix=bwidth/pix_to_arcsec
  bareapix=barea/(pix_to_arcsec**2.0)
  print(barea,bwidth,bareapix,bwidthpix)

  cosinc=math.cos(incl*math.pi/180.0)
  if r_out is None:
    # assume it is a square image
    NPIX=ct.imhead(imagename=infile,mode='get',hdkey='SHAPE')[0]
    # take half of NPIC as the maximum extension, and convert it to arcsec
    r_out=NPIX/2*pix_to_arcsec
  print("r_out: ",r_out)

  rings=np.arange(width/2.0,r_out+width,width)

  # TODO check that but it seems for the ellipse we need a sign change
  # for the PV diagramm it seems to work.
  PAstring="-"+str(PA)+"deg"

  fluxes=list()
  rs=list()
  err=list()
  ioutput=0
  for ring in rings:
    ioutput+=1
    if ioutput%10==0:
        print("DO RING: ",ring,"/",r_out)

    maje=ring+width/2.0
    mine=maje*cosinc
    maje=str(maje)+"arcsec"
    mine=str(mine)+"arcsec"
    region='ellipse[['+RA+', '+DEC+'], ['+mine+', '+maje+'],'+PAstring+']'

    stat=ct.imstat(imagename=infile,region=region)
    bigflux=stat['sum'][0]
    bigarea=stat['npts'][0]

    maje=ring-width/2.0
    # treatment for the first point
    if maje<1.e-20:
        smallflux=0.0
        smallarea=0.0
    else:
        mine=maje*cosinc
        maje=str(maje)+"arcsec"
        mine=str(mine)+"arcsec"
        region='ellipse[['+RA+', '+DEC+'], ['+mine+', '+maje+'],'+PAstring+']'

        stat=ct.imstat(imagename=infile,region=region)
        smallflux=stat['sum'][0]
        smallarea=stat['npts'][0]

    # calculate the flux for the annulus
    ringarea=bigarea-smallarea
    flux=bigflux-smallflux
    fluxes.append(flux/ringarea)
    # average of major and minor axis ... same as the DSHARP people did
    rs.append(ring)
    # rs.append((ring+ring*cosinc)/2)

    if rms is not None:
        err.append(3.0*rms/(math.sqrt(ringarea/bareapix)))
    else:
        err.append(0.0)

  return np.array(rs),np.array(fluxes),np.array(err)


def write_radprof(outfile,r,flux,fluxerr):
  '''
  Writes a radial profile to a file in the format used by casairing.
  This is only for compatibility for older projects.
  '''

  header="#    Distance (as),  Frequency (GHz),  Average (Jy/beam.km/s),  Avg. Error (Jy/beam.km/s)"
  # just a dummy for the moment. Use the same format as the casairing task, that"s why this is here.
  output=np.column_stack((r,r*0.0,flux,fluxerr))
  np.savetxt(outfile,output,header=header)


class _PostProcess(object):

  def get_beam_refimage(self):
    '''
    Trys to read the beam information from the given reference image.
    '''
    if self.refimage is None:
      return None

    try:
      bmaj=ct.imhead(imagename=self.refimage,mode='get',hdkey='BMAJ')  # must be in arcsec
      bmin=ct.imhead(imagename=self.refimage,mode='get',hdkey='BMIN')  # must be in arcsec
      # FIXME: assumes that it is in degrees and makes a conversion
      bPA=ct.imhead(imagename=self.refimage,mode='get',hdkey='BPA')['value']  # must be in deg
      # bPAFull=ct.imhead(imagename=refimagename,mode='get',hdkey='BPA')
      # print(bPAFull)
      # print(bPAFull['value'],bPAFull['unit'])
      # PA has to be in rad I guess
      beamloc=[str(bmaj["value"])+bmaj["unit"],str(bmin["value"])+bmin["unit"],str(bPA*0.01745329252)+"rad"]
    except AssertionError as error:
      print("ERROR: get_beam_refimage: The image "+self.refimage+" was not found by CASA (most likely cause of error).")
      raise

    return beamloc

  def _convole_spatial(self,infile,outfile,beam,noise=None):
    ia=iatool()
    ia.fromfits(infile=infile)

    # FIXME: quick hack for noise, currently one has to experiment with the value
    # to e.g. get the desired rms
    if noise is not None:  # noise is given in Jy/beam
      print("INFO: Adding noise: ",noise)
      # print(ia.statistics())
      ia.addnoise(type="uniform",pars=[-noise,noise],zero=False,seeds=[1,2])
      # print(ia.statistics())

    imconv=ia.convolve2d(major=beam[0],minor=beam[1],pa=beam[2],outfile=outfile)
    # beamarea=imconv.beamarea()["pixels"]
    # print(beamarea)
    imconv.done()
    ia.close()

  def _radial_profile(self,fitsfile,incl=None,PA=None,fracbeam=0.33,rms=None,r_out=None):

    print("radial_profile for "+fitsfile+" ...")

    if incl is None:
      incl=self.incl

    if PA is None:
      PA=self.PA

    if incl is None or PA is None:
      print("ERROR: Please provide inclination and position angle.")

    outfile=fitsfile.replace(".fits",".radial")
    write_radprof(outfile,*radprof(fitsfile,incl,PA,fracbeam=fracbeam,rms=rms,r_out=r_out))
    print("Produced radial profile: "+outfile)


class ContinuumPP(_PostProcess):
  """
  Object to post-process ProDiMo continuum images for CASA.
  """

  def __init__(self,proj,modelfits,chans=None,band=None,incl=None,PA=None,
               refimage=None,singleimage=False,removeBackground=False):
    """
    Atrributes
    ----------

    """
    self.proj=proj
    """ string :
      A project name which will be used to store the casa files in a directoy with name `proj`. Also
      all files will start with the prefix `proj`.
    """
    self.modelfits=modelfits
    """ string :
      The path/filename for the continuum images output of ProDiMo. Usually this file is called image.fits.
    """
    self.chans=chans
    """ string :
      A string with the desired channel number for the image. E.g. "0" selctes the first one.
      "50,51,51" will produce an average of this three channels.
    """
    self.band=band
    """ array_like(ndim=1) :
    start and end wavelength `[start,end]` in [micron] of a "band". All images found withing this
    wavelength range will be combined to one.
    """

    self.incl=incl
    self.PA=PA
    self.refimage=refimage

    self.projn=os.path.basename(proj)
    self.fprefix=self.proj+"/"+self.projn+"."
    self.fprefixtmp=self.proj+"/"+self.projn+"tmp."
    self.wlgrid=None
    self.singleimage=singleimage

    self.fmimage=self.fprefix+"mcont.fits"
    self.fmimageconv=self.fprefix+"cont.conv.fits"
    self.fmimageregrid=self.fprefix+"cont.conv.regrid.fits"
    self.fmimagefinal=self.fprefix+"cont.fits"

    os.system("rm -rfv "+proj+"/"+self.projn+"*")
    print("make Directory"+proj)
    os.system("mkdir "+proj)

    if (self.chans is None and self.band is None):
      raise ValueError("Either chans or band have to be set.")

    if not singleimage:
      self._read_wlgrid()
    self._init_image(removeBackground=removeBackground)

  def _read_wlgrid(self):
    """
    Reads the wavelength grid from ProDiMo continuum fits image.

    TODO: Could be a general utility function.

    """
    ct.importfits(fitsimage=self.modelfits,imagename=self.fprefixtmp+"wlgrid.im",overwrite=True,whichhdu=1)
    self.wlgrid=np.array(ct.imval(self.fprefixtmp+"wlgrid.im")["data"])
    # print("Wavelength grid of image.fits",wlgrid)
    os.system("rm -rfv "+self.fprefixtmp+"wlgrid.im")

  def _init_image(self,removeBackground=False):
    """
    Gets the desired image frome the image.fits produced by PRoDiMo. image.fits includes all
    the continuum images. Currently the image can be selected by providing the index (e.g. 0 first image) to
    select the image from image.fits. If a lilst of indices is provided the routine combines those images
    into one. This is usefull to produce an averaged image for e.g. one alma Band.

    TODO: make the routine more user friendly. For example one could provide the wavelength instead of the
    indices.
    """

    print("init_image ...")

    if self.singleimage:
      print("cp -v "+self.modelfits+" "+self.fmimage)
      os.system("cp -v "+self.modelfits+" "+self.fmimage)
    else:
      if self.band is not None:
        # findd the indices (chanels)
        idxstart=np.argmax(self.wlgrid>=self.band[0])
        idxend=np.argmin(self.wlgrid<=self.band[1])
        wls=self.wlgrid[idxstart:idxend]
        idxs=list(map(str,np.arange(idxstart,idxend,1)))
        self.chans=",".join(idxs)
        nwl=len(idxs)
        print("Band: ",self.band,"combining channels (wavelengths): ",self.chans,wls)
      else:
        idxs=list(map(int,self.chans.split(",")))
        wls=[self.wlgrid[idx] for idx in idxs]
        nwl=len(idxs)
        print("combining channels (wavelengths): ",self.chans,wls)

      # FIXME: not nice
      # STRANGE: the oufiles must end with .image ... outerwise casa gives an error
      if nwl==1:
        ct.imsubimage(imagename=self.modelfits,outfile=self.fprefixtmp+"sub.image",chans=self.chans,dropdeg=True)
      else:
        ct.imsubimage(imagename=self.modelfits,outfile=self.fprefixtmp+"sub2.image",chans=self.chans,dropdeg=True)
        ct.imrebin(imagename=self.fprefixtmp+"sub2.image",outfile=self.fprefixtmp+"sub.image",factor=[1,1,nwl],dropdeg=True)

      ct.exportfits(fitsimage=self.fmimage,imagename=self.fprefixtmp+"sub.image",dropdeg=True,overwrite=True)
      os.system("rm -rfv "+self.fprefixtmp+"sub.image")
      os.system("rm -rfv "+self.fprefixtmp+"sub2.image")

      # FIXME: quick hack to remove the background, havent found another way yet, maybe just do it with astropy
      if (removeBackground):
        print("INFO: remove Background")
        ia=iatool()
        ia.fromfits('tmpimg',infile=self.fmimage,overwrite=False)
        # print(ia.summary())
        # print(ia.name())
        expr=r"tmpimg-min(tmpimg)"
        ia.calc(expr)
        ia.done()
        ct.exportfits(fitsimage=self.fmimage,imagename="tmpimg",dropdeg=True,overwrite=True)
        os.system("rm -rfv tmpimg")

  def cleanup(self):
    # just to be sure, delete all casa stuff
    os.system("rm -rfv "+self.fprefix+"*.image")
    os.system("rm -rfv "+self.fprefix+"*.im")

    os.system("rm -fv "+self.fmimageconv)
    os.system("rm -fv "+self.fmimageregrid)
    os.system("rm -fv "+self.fmimage)

  def conv_image(self,beam=None,noise=None):
    if beam is None:
      beam=self.get_beam_refimage()
      if beam is None:
        print("ERROR: Cannot convolve image, no beam found.")

    print("conv_image with beam: ",beam)

    outfile=self.fmimageconv.replace(".fits",".im")

    self._convole_spatial(self.fmimage,outfile,beam,noise=noise)

    ct.exportfits(fitsimage=self.fmimageconv,imagename=outfile,dropdeg=True,overwrite=True)
    os.system("rm -rfv "+outfile)
    # copy it to the final image, can still be overwritten
    os.system("cp "+self.fmimageconv+" "+self.fmimagefinal)

  def regrid_image(self,fitsfile=None):
    if self.refimage is None:
      return None

    if fitsfile is None:
      fitsfile=self.fmimageconv

    print("regrid_image to "+self.refimage)

    RA,DEC=self.get_coord_refimage()

    outfile=fitsfile.replace(".fits",".im")
    ia=iatool()
    ia.fromfits(infile=fitsfile,outfile=outfile)
    ia.close()

    # set the center coordinates
    ct.imhead(imagename=outfile,mode='put',hdkey='CRVAL1',hdvalue=RA)
    ct.imhead(imagename=outfile,mode='put',hdkey='CRVAL2',hdvalue=DEC)
    # this is required in case one wants to do some regridding
    ct.imhead(imagename=outfile,mode='put',hdkey='TELESCOPE',hdvalue='ALMA')

    ia=iatool()
    ia.fromfits(infile=self.refimage)
    cs1=ia.coordsys()
    s1=ia.shape()
    # print(s1)
    ia.close()

    ia=iatool()
    ia.open(infile=outfile)
    newim=ia.regrid(shape=s1,csys=cs1.torecord(),overwrite=True,decimate=1)

    self.fmimageregrid=fitsfile.replace(".fits",".regrid.fits")
    newim.tofits(outfile=self.fmimageregrid,overwrite=True)
    newim.done()
    ia.close()
    os.system("rm -rfv "+outfile)
    os.system("cp "+self.fmimageregrid+" "+self.fmimagefinal)

  def residual_image(self):
    '''

    '''
    if self.refimage is None:
      return None

    print("residual_image ...")

    outfile=self.fmimagefinal.replace(".fits",".im")
    val=ct.immath(imagename=[self.refimage,self.fmimageregrid],expr='IM0-IM1',outfile=outfile)
    ct.exportfits(outfile,fitsimage=self.fmimagefinal.replace(".fits",".diff.fits"),dropdeg=True,overwrite=True)
    os.system("rm -rfv "+outfile)

  def radial_profile(self,incl=None,PA=None,fracbeam=0.33,rms=None,r_out=None,fitsfile=None):
    if fitsfile is None:
      fitsfile=self.fmimagefinal

    self._radial_profile(fitsfile,incl=incl,PA=PA,fracbeam=fracbeam,rms=rms,r_out=r_out)

  def get_coord_refimage(self):
    '''

    '''
    if self.refimage is None:
      return None

    RA=ct.imhead(imagename=self.refimage,mode='get',hdkey='CRVAL1')
    RA=str(RA["value"])+RA["unit"]
    DEC=ct.imhead(imagename=self.refimage,mode='get',hdkey='CRVAL2')
    DEC=str(DEC["value"])+DEC["unit"]

    return RA,DEC

  def doall(self):
    '''

    '''
    print("doall ...")
    self.conv_image()
    self.regrid_image()
    self.radial_profile()
    self.residual_image()
    self.cleanup()


class LinePP(_PostProcess):
  """
  Object to post-process ProDiMo linecubes for comparison to observations.

  This is all still very experimental and everything can still change.

  """

  def __init__(self,proj,modelfits,sys_vel=None,incl=None,PA=None,refimage=None):
    """
    Atrributes
    ----------

    """
    self.proj=proj
    """ str :
      A project name which will be used to store the casa files in a directoy with name `proj`. Also
      all files will start with the prefix `proj`.
    """
    self.modelfits=modelfits
    """ str :
      The path/filename for the line cube output of ProDiMo. Usually this file is called LINE_3D_xxx.fits.
    """
    self.incl=incl
    self.PA=PA
    self.lineid=None
    """ str :
      The identificatoin string for the spectral line (From ProDiMo).
    """
    self.linewl=None
    """ str :
      The wavelength of the line [micron]
    """
    self.linefreq=None
    """ str :
      The frequency of the line [GHz]
    """

    self.sys_vel=None
    self.refimage=refimage

    self.projn=os.path.basename(proj)
    self.fprefix=self.proj+"/"+self.projn+"."
    self.fprefixtmp=self.proj+"/"+self.projn+"tmp."

    self.fmimage=self.fprefix+"mcube.fits"
    self.fmimage_contsubm=self.fprefix+"mcube.contsub.fits"
    self.fmimage_contsubmcont=self.fprefix+"mcube.contsubcont.fits"
    self.fmimageconv=self.fprefix+"cube.conv.fits"
    self.fmimageregrid=self.fprefix+"cube.conv.regrid.fits"
    self.fmimagefinal=self.fprefix+"cube.fits"
    self.fmimagemom0=self.fprefix+"cube.integrated.fits"
    self.fmimagemom1=self.fprefix+"cube.mom1.fits"

    os.system("rm -rfv "+proj+"/"+self.projn+"*")
    print("make Directory"+proj)
    os.system("mkdir "+proj)

    self._init_image()

  def _init_image(self):
    '''
    Copies the original image to avoid any troubles,
    and reads certain header attributes from the ProDiMo fits file (e.g. incl
    PA ) if they were not overwritten.
    '''
    os.system("cp "+self.modelfits+" "+self.fmimage)

    fitscube=fits.open(self.fmimage)

    self.lineid=(fitscube[0].header["P_LINEID"]).strip()
    self.linewl=float(fitscube[0].header["P_LINEWL"])
    self.linefreq=float(fitscube[0].header["P_LINEFR"])

    if self.incl is None:
      self.incl=fitscube[0].header["P_INCL"]

    if self.PA is None:
      self.PA=fitscube[0].header["P_PAOBJ"]
    fitscube.close()

  def __str__(self):
    output="Line cube: "+self.lineid.split()[0]+" "+"{:7.4e} mic".format(self.linewl)+" / {:7.4e} GHz".format(self.linefreq)+"\n"
    output+="Filename: "+str(self.fmimage)
    output+=" / Inclination: "+str(self.incl)
    output+=" / Position angle: "+str(self.PA)
    output+="\n"
    return output

  def cleanup(self):
    # just to be sure, delete all casa stuff
    os.system("rm -rfv "+self.fprefix+"*.image")
    os.system("rm -rfv "+self.fprefix+"*.im")

  def conv_image(self,infits,outfits,beam=None,noise=None):
    if beam is None:
      beam=self.get_beam_refimage()
      if beam is None:
        print("ERROR: Cannot convolve image, no beam found.")

    print("conv_image with beam: ",beam," ...")

    outfile=outfits.replace(".fits",".im")

    self._convole_spatial(infits,outfile,beam,noise=noise)

    ct.exportfits(fitsimage=outfits,imagename=outfile,dropdeg=True,overwrite=True)

    os.system("rm -rfv "+outfile)

    print("Produced convolved cube: "+outfits)

    # os.system("rm -rfv "+outfile)
    # self.lastimage=outfits
    # copy it to the final image, can still be overwritten
    # os.system("cp "+self.fmimageconv+" "+self.fmimagefinal)

#   def conv_casaimage(self,infile,outfits,beam=None):
#     '''
#     Spatially convolves the given casa images and exports it to a fits file.
#
#     '''
#     if beam is None:
#       beam=self.get_beam_refimage()
#       if beam is None:
#         print("ERROR: Cannot convolve image, no beam found.")
#
#     outfile=infile+".tmp"
#     self._convole_spatial(infile, outfile, beam)
#     ct.exportfits(fitsimage=outfits,imagename=outfile,dropdeg=True,overwrite=True)
#     os.system("rm -rfv "+outfile)

  def momentmap(self,infits,outfits,moment=0,immomentsparams=None):

    print("momentmap moment "+str(moment)+" ...")

    outfile=outfits.replace(".fits",".im")
    if immomentsparams is not None:
      ct.immoments(infits,outfile=outfile,moments=[moment],**immomentsparams)
    else:
      ct.immoments(infits,outfile=outfile,moments=[moment])

    ct.exportfits(fitsimage=outfits,imagename=outfile,dropdeg=True,overwrite=True)

    print("Produced moment "+str(moment)+" map: "+outfits)

    os.system("rm -rfv "+outfile)

  def radial_profile(self,incl=None,PA=None,fracbeam=0.33,rms=None,r_out=None,infits=None):
    if infits is None:
      infits=self.fmimagemom0

    self._radial_profile(infits,incl=incl,PA=PA,fracbeam=fracbeam,rms=rms,r_out=r_out)

  def spectral_profile(self,infits=None):
    if infits is None:
      infits=self.fmimagefinal

    outfile=infits.replace(".fits",".specprof")
    ct.specflux(imagename=infits,logfile=outfile,overwrite=True)

    print("Produced spectral profile "+outfile)

  def contsub_model(self,removeBackground=False,realcont=False):
    '''
    Removes the continuum. This is done in the image plane. By default it uses
    directly the model continuum in the cube (this cannot be done in reality).

    Parameters
    ----------

    removeBackground : bool
      Remove the background from the continuum result. Simply removes the min
      value if the continuum image from the image.

    realcont : bool
      Uses the real continuum from the cube. This real continuum is included
      the _CONT output files. This is useful to test the impact of continuum
      oversubtraction. With this option the absorption of the continuum by
      the line is considered and therefore the continuum subtraction is exact.
      But this is not something that can be done in reality.

    TODO: quick and dirty stuff ...
    TODO: include method to use certain channels from the cube for the cont subtraction
    '''
    print("contsub_model ...")

    ct.importfits(fitsimage=self.fmimage,imagename=self.proj+"/cube.im",overwrite=True,whichhdu=0)

    if realcont:
      # Use the CONT cube for the exact continuum subtraction
      ct.importfits(fitsimage=self.modelfits.replace(".fits","_CONT.fits"),imagename=self.proj+"/cont.im",overwrite=True,whichhdu=0)
    else:
      ct.importfits(fitsimage=self.fmimage,imagename=self.proj+"/cont.im",overwrite=True,whichhdu=1)

    rval=ct.immath(imagename=[self.proj+"/cube.im",self.proj+"/cont.im"],
                      expr='IM0-IM1',outfile=self.proj+"/cubemcont.im",imagemd=self.proj+"/cube.im")

    ct.exportfits(fitsimage=self.fmimage_contsubm,imagename=self.proj+"/cubemcont.im",dropdeg=True,overwrite=True)

    if removeBackground:
      rval=ct.immath(imagename=[self.proj+"/cont.im"],
                        expr='IM0-min(IM0)',outfile=self.proj+"/contbg.im",imagemd=self.proj+"/cont.im")
      ct.exportfits(fitsimage=self.fmimage_contsubmcont,imagename=self.proj+"/contbg.im",dropdeg=True,overwrite=True)
      os.system("rm -rfv "+self.proj+"/contbg.im")

    else:
      ct.exportfits(fitsimage=self.fmimage_contsubmcont,imagename=self.proj+"/cont.im",dropdeg=True,overwrite=True)

    os.system("rm -rfv "+self.proj+"/cubemcont.im")
    os.system("rm -rfv "+self.proj+"/cont.im")
    os.system("rm -rfv "+self.proj+"/cube.im")
    print("Produced continuum subtraced cube: "+self.fmimage_contsubm)

