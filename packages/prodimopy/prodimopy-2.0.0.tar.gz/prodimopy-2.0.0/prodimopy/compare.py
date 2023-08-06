from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import difflib
import glob
from inspect import ismethod
import inspect
import os

from astropy.io.fits.diff import FITSDiff

import numpy as np


class CompareAbs(object):
  """
  An "abstract" class for comparing some kind of |prodimo| model.

  A subclass of this class needs to implement the necessary compare routine(s).
  (example see :class:`Compare`)

  .. todo::
    * make tolerances configurable via config file (see punit checkModels).

  """

  def diffArrayRel(self,a,aref,diff):
    """
    Checks the relative difference between two arrays.

    If the arrays do not have the same shape they are considered
    as inequal (return `False`).

    Parameters
    ----------
    a : array_like(float,ndim=whatever)
      an array.

    aref: array_like(float,ndim=same as a)
      the reference array for comparison.

    diff : float
      if the values of the arrays differe only by <diff they are considered
      as equal.
    """
    if a.shape!=aref.shape:
      return False,None

    da=np.absolute(a/aref-1.0)
    if da.max()>=diff:
      return False,da

    return True,da

  def diffArray(self,a,aref,rtol=1.e-3,atol=0.0,nlimfrac=0.0,mask=None):
    """
    Checks the difference between two arrays using the np.isclose routine but
    additionally allows to set a limit for how many elements can be different
    in the arrays to still be considered as equal (or similar).

    If the arrays do not have the same shape they are considered
    as inequal (return `False`).

    Parameters
    ----------
    a : array_like(float,ndim=whatever)
      an array.

    aref: array_like(float,ndim=same as a)
      the reference array for comparison.

    rtol : float
      Relative tolerance as used in :func:`numpy.iclose`.

    atol : float
      Absolute tolerance as used in :func:`numpy.iclose`.

    nlimfrac : float
      Relative limit of elements that are allowed to be not equal.
      If less than `nlim *  len(aref)` elements are different, the arrays
      are still considered as equal.

    mask : mask for the array
      Mask for the elements that should not be included in the evaluation.
      Those elements are set to True in any case.
    """

    dbool=np.isclose(a,aref,rtol=rtol,atol=atol,equal_nan=True)

    #
    # Calculate the difference in percent, only for the values that are
    # deal with zero values.
    # check for zero values
    maskZ=aref!=0
    da=aref*0.0
    da[maskZ]=np.absolute(a[maskZ]/(aref[maskZ])-1.0)*100
    da[~maskZ]=np.absolute(a[~maskZ]+1.e-100/(aref[~maskZ]+1.e-100)-1.0)*100
    # set the value that are masked to zero (not considered in for e.g. max error)
    if mask is not None:
      dbool[mask]=True
      da[mask]=0.0

    # set the values that are considered as similar to 0 ... because of atol
    # da[dbool]=0.0

    # check if the number of inequal elements is lower than allowed.
    if nlimfrac>0.0:
      eq=(np.size(dbool)-np.count_nonzero(dbool))<int(nlimfrac*np.size(dbool))
    else:
      eq=dbool.all()
    # if da.max()>=diff:
    #   return False,da

    # return True,da
    return eq,da,dbool

  def diff(self,val,valref,rtol=1.e-10,atol=0.0):
    """
    Checks the relative difference between two values.
    FIXME: is not inconsisten with diffArr

    Parameters
    ----------
    a : float
      a value.

    aref: float
      the reference value

    diff : float
      if the two values differe only by <diff the are considered
      as equal.
    """

    dbool=np.isclose(val,valref)
    d=abs(val/valref-1.0)*100

    return dbool,d

  def diffFile(self,fname):
    """
    Compares the file with the name given by `fname` (a file produced by ProDiMo)
    for the the two models.

    Parameters
    ----------
    fname : str
      the Filename to compare, (must exist for both models)
    """
    # check if file exist
    fe=os.path.isfile(self.m.directory+"/"+fname)
    feref=os.path.isfile(self.mref.directory+"/"+fname)

    # File does not exist in any model -> that is okay
    if ((not fe) and (not feref)): return True,None

    # if the file exists in only one model, the routine returns false!
    if (fe^feref): return False,None

    # now compare the files
    f=open(self.m.directory+"/"+fname)
    fref=open(self.mref.directory+"/"+fname)
    fcont=f.readlines()
    fcontRef=fref.readlines()

    diff=list(difflib.unified_diff(fcont,fcontRef,n=0))

    if len(diff)==0:
      return True,None
    else:
      return False,diff

  def diffFitsFile(self,fname,atol=0.0,rtol=2.e-7):
    """
    Compares two fits Files using the astropy routines.

    Parameters
    ----------
    fname : str
      the Filename to compare, (must exist for both models)
    """
    # check if file exist
    fe=os.path.isfile(self.m.directory+"/"+fname)
    feref=os.path.isfile(self.mref.directory+"/"+fname)

    # File does not exist in any model -> that is okay
    if ((not fe) and (not feref)): return True,None

    # if the file exists in only one model, the routine returns false!
    if (fe^feref): return False,None

    # FIXME: in restart.dat this CONVERGENCE keywordk makes problems,
    # I think the KEYWORD name is too long (see the fitsheader of reastart.fits.gz)
    # do not test for MAINIT, so that also models that were rerun can be compared
    try:
      diff=FITSDiff(self.m.directory+"/"+fname,self.mref.directory+"/"+fname,
                    ignore_keywords=['CONVERGENCE',"MAINIT"],
                    numdiffs=3,atol=atol,rtol=rtol)
    except Exception as e:
      print("Exception in FITSDiff: ",e)
      return False,None

    if diff.identical:
      return True,None
    else:
      return False,diff.report()

  def doAll(self):
    """
    Utility function to call all `compare*` method.

    Prints out what function failed and the errors.

    Assume a naming convention. The method needs to start
    with `compare`. If the compare method uses the :func:`diffFile`,
    the method name should start with `compareFile`.

    """
    for name in dir(self):
      if name.startswith("compare"):
        cfun=getattr(self,name)
        if ismethod(cfun):
          print("{:30s}".format(name+": "),end="")
          ret=cfun()
          ok=ret[0]
          val=ret[1]
          valb=None
          if len(ret)>2:
            valb=ret[2]

          if ok:
            print("{:8s}".format("OK"),end="")
          else:
            print("{:8s}".format("FAILED"),end="")

          # Special treatment for the case of comparing Files
          if name.startswith("compareFile"):
            if val is None and not ok:
              print("  File does only exist in one model.")
            elif val is not None:
              for line in val:
                if line.startswith("@@"):
                  print("")
                print(line,end="")
            else:
              print("")
          elif name.startswith("compareFitsFile"):
            if val is None and not ok:
              print("  File does only exist in one model.")
            elif val is not None:
              print(val)
            else:
              print("")
          else:
            # TODO: also add the number of wrong points in the array
            if val is not None:
              if valb is not None:
                nnoteqp=(np.size(valb)-np.count_nonzero(valb))/np.size(valb)*100

              print("  different/Avg Err/Max Err/ Max Err Index: ","{:8.2e}%".format(nnoteqp),"/","{:8.2e}%".format(np.average(val)),"/",
                    "{:8.2e}%".format(np.max(val)),"/",np.unravel_index(val.argmax(),val.shape))

              # print the first 10 species (lines) that show the largest differences
              if name.startswith("compareLineEstimates") and not ok:
                sortidx=np.flip(np.argsort(val),axis=0)
                lastIdents=list()
                iprint=0
                for i in range(len(val)):
                  # if self.m.lineEstimates[sortidx[i]].flux>1.e-24 or self.mref.lineEstimates[sortidx[i]].flux>1.e-24:
                  # check also if the value is not masked (then it is true in valb anyway)
                  if not valb[sortidx[i]] and not self.m.lineEstimates[sortidx[i]].ident in lastIdents:
                    print("{:40s}".format(str(self.m.lineEstimates[sortidx[i]])),
                          "{:40s}".format(str(self.mref.lineEstimates[sortidx[i]])))
                    lastIdents.append(self.m.lineEstimates[sortidx[i]].ident)
                    iprint+=1
                  if iprint>5: break
                print("")

              # FIXME: currently only works for CompareMC
              if name.startswith("compareAbundances") and not ok and isinstance(self,CompareMc):

                # find out the ages with maximum error
                # the age index for each species with the maximum error
                maxa=np.argmax(val,axis=0)
                # print(maxa[self.m.species.index("Cl+")])
                # print(self.m.abundances[:,self.m.species.index("Cl+")])
                # print(self.mref.abundances[:,self.mref.species.index("Cl+")])
                # no make a list for those values and sort it (find the maximum species index)
                diffspec=np.array([val[idx,i] for i,idx in enumerate(maxa)])
                # print(diffspec,np.max(diffspec))
                sortidx=np.flip(np.argsort(diffspec))
                lastIdents=list()
                iprint=0
                for i in range(len(sortidx)):
                  # if self.m.lineEstimates[sortidx[i]].flux>1.e-24 or self.mref.lineEstimates[sortidx[i]].flux>1.e-24:
                  if not valb[maxa[sortidx[i]],sortidx[i]] and not self.m.species[sortidx[i]] in lastIdents:
                    print("{:20s}".format(self.m.species[sortidx[i]]),"{:10.3f}".format(val[maxa[sortidx[i]],sortidx[i]]),
                          # need +1 here because the 0 age index is not considerd in the comparison, see compare_abundances
                          "{:40s}".format(str(self.m.abundances[maxa[sortidx[i]]+1,sortidx[i]])),
                          "{:40s}".format(str(self.mref.abundances[maxa[sortidx[i]]+1,sortidx[i]])))
                    lastIdents.append(self.m.species[sortidx[i]])
                    iprint+=1
                  if iprint>5: break

            elif val is None and not ok:
              print("  Value/array is None in only one model.")
            else:
              print("")


class Compare(CompareAbs):
  """
  Class for comparing to ProDiMo models of type :class:`~prodimopy.read.Data_ProDiMo`

  Every compare Function returns true or false, and the relative differences
  (in case of arrays these are arrays).

  Can be used in e.g. automatic testing routines or in simple command line
  tools to compare ProDiMo model results.
  """

  def __init__(self,model,modelref):
    """
    Parameters
    ----------
    model : :class:`~prodimopy.read_mc.Data_mc`
      The model one wants to compare.

    modelref : :class:`~prodimopy.read_mc.Data_mc`
      The reference model to compare with.

    Attributes
    ----------

    """

    if model is None or modelref is None:
      raise TypeError("Either model or modelref is None, no comparison possible.")

    self.m=model
    """ :class:`~prodimopy.read.Data_ProDiMo` :
    The model one wants to compare.
    """
    self.mref=modelref
    """ :class:`~prodimopy.read.Data_ProDiMo` :
    The reference model agains which model is compared..
    """
    self.tolerances={}
    """ dict :
    A dictionary of tolerances. The naming convention has to follow the naming
    of the compare Function. e.g. If one wants to provide tolerances for
    `compareAbundances` the key names are `Abundances.rtol` and `Abundances.atol`.

    FIXME: This is still experimental and not implemented for all compare routines.

    """

    # the default allowed difference

#     self.d=1.e-3
#     self.dcdnmol=0.5  # the allowed differences for the column densities (radial and vertical)
#                       # chemistry is difficult and uncertain :) FIXME: this has to become better, there
#                       # a simply some columns which usually fail an require time-dependent chemistry and
#                       # the outcome seems to depend on numerical uncertainties ...
#     # (e.g. 7% point in the column density goes crazy ... still oka
#     self.fcdnmol=0.1
#     self.lcdnmol=1.e-10  # lower limit for the column density to avoid problems with "empty" columns
#     self.dTgas=5e-1  # FIXME: 50% Tgas is also quite sensitive, but lower would be better
#     self.dZetaCR=self.d
#     self.dZetaX=5.e-1  # FIXME: 50% , should not be that high
#     self.dHX=3.e-1  # FIXME: 50% , should not be that high
#     self.lZetaX=1.e-25  # lower limit for the check
# #    self.specCompare=("e-","H2","CO","H2O","Ne+","Ne++","H+")
# #    self.specCompare=("N2","N2#","CO#","H2O#","H3","H3+","HCO+","HN2+","SO2","SiO")
# #    self.specCompare=("CO","CN")

    self.specCompare=("e-","H","H2","CO","H2O","N2","N2#","CO#","H2O#","H3+","HCO+","HN2+","SO2","SiO",
                      "Ne+","Ne++","H+","OH","C+","S+","Si+","N+","CN","HCN","NH3")

    # switch of some logging
    self.m._log=False
    self.mref._log=False

  def getTols(self,atol=None,rtol=None,nlimfrac=None):
    '''
    Get the tolerance values from the `self.tolerances` dictionary

    Returns
    -------

    dict: containing {"atol": value, "rtol": value } if set. Can also be empty

    '''

    # This gives me the name of the caller function. Check if it is a compare
    # function
    callername=inspect.currentframe().f_back.f_code.co_name
    if not callername.startswith("compare"):
      raise ValueError("getTols can only be called from a compare function!")

    # strip the compare
    valname=callername.replace("compare","")

    # The dictonary that contains the return values, if any
    retdict={}

    for key,defval in zip(["atol","rtol","nlimfrac"],[atol,rtol,nlimfrac]):
      if valname+"."+key in self.tolerances:
        retdict[key]=self.tolerances[valname+"."+key]
      elif defval is not None:
        retdict[key]=defval

    return retdict

  def compareX(self):
    '''
    Compares the x grid points.
    '''
    return self.diffArray(self.m.x,self.mref.x,**self.getTols(rtol=1.e-5))

  def compareZ(self):
    '''
    Compares the z grid points.
    '''
    ret=self.diffArray(self.m.z,self.mref.z,**self.getTols(rtol=1.e-5))
    return ret

  def compareLineFluxes(self):
    '''
    Compares the line fluxes
    Currently assumes that both models include the same lines in the same order.
    '''
    if self.m.lines is None and self.mref.lines is None: return True,None

    if self.m.lines is not None and self.mref.lines is None: return False,None

    if self.m.lines is None and self.mref.lines is not None: return False,None

    mFluxes=np.array([x.flux for x in self.m.lines])
    mrefFluxes=np.array([x.flux for x in self.mref.lines])
    return self.diffArray(mFluxes,mrefFluxes,**self.getTols(rtol=0.05))

  def compareLineEstimates(self):
    '''
    Compares the fluxes from the line estimates
    Currently assumes that both models include the same lines in the same order.

    TODO: can actually be merged with compareLineFluxes
    '''
    if self.m.lineEstimates is None and self.mref.lineEstimates is None: return True,None

    if self.m.lineEstimates is not None and self.mref.lineEstimates is None: return False,None

    if self.m.lineEstimates is None and self.mref.lineEstimates is not None: return False,None

    mFluxes=np.array([x.flux for x in self.m.lineEstimates])
    mrefFluxes=np.array([x.flux for x in self.mref.lineEstimates])

    mask=np.logical_and(mFluxes<1.e-24,mrefFluxes<1.e-24)

    return self.diffArray(mFluxes,mrefFluxes,mask=mask,**self.getTols(rtol=3.e-1,nlimfrac=0.01))

  def compareSED(self):
    """
    Compares the SEDs
    """
    if self.m.sed is None and self.mref.sed is None: return True,None
    if self.m.sed is not None and self.mref.sed is None: return False,None
    if self.m.sed is None and self.mref.sed is not None: return False,None
    return self.diffArray(self.m.sed.fnuErg,self.mref.sed.fnuErg,**self.getTols(rtol=1.e-3))

  def compareContinuumImages(self):
    """
    Compares some of the continuum images.
    """
    if self.m.contImages is None and self.mref.contImages is None: return True,None
    if self.m.contImages is not None and self.mref.contImages is None: return False,None
    if self.m.contImages is None and self.mref.contImages is not None: return False,None

    for wl in [1,10,100,1000]:
      imm,immwl=self.m.contImages.getImage(wl)
      imref,imrefwl=self.mref.contImages.getImage(wl)

      f,d=self.diff(immwl,imrefwl)
      if f==False:
        return False,d

      f,d,b=self.diffArray(imm,imref)

      if f==False:
        return False,d,b

    return True,d,b

  def compareCdnmol(self):
    '''
    checks the vertical column densities
    only the outermost points (e.g. total column density) are checked
    '''
    # specidxM=[self.m.spnames[spname] for spname in self.specCompare if spname in self.m.spnames]
    # specidxMref=[self.mref.spnames[spname] for spname in self.specCompare if spname in self.mref.spnames]

    # get rid of very small column densities
    # for i in specidxM:
    #   self.m.cdnmol[self.m.cdnmol[:,0,i]<self.lcdnmol,0,i]=self.lcdnmol
    #
    # for i in specidxMref:
    #   self.mref.cdnmol[self.mref.cdnmol[:,0,i]<self.lcdnmol,0,i]=self.lcdnmol

    return self.diffArray(self.m.cdnmol[:,0,:],self.mref.cdnmol[:,0,:],**self.getTols(rtol=1.e-1,nlimfrac=0.1))
    # ok,d,b=self.diffArray(self.m.cdnmol[:,0,specidxM],self.mref.cdnmol[:,0,specidxMref],1.e-1,1.0,0.1)

    # if false check if it is only a certain fraction of the columns, it than can
    # be still okay
    # is not really elegant I would say
    # TODO: also somehow return the number of failed columns
    # TODO: maybe merge rcdnmol
    # if ok is False and d is not None:
    #   ok=True  # and check if any columns faild
    #   for i in range(len(specidxMref)):
    #     faildcolumns=(d[:,i]>self.dcdnmol).sum()
    #     if ((float(faildcolumns)/float(len(d[:,i])))>self.fcdnmol):
    #       ok=False
#          specs=list(self.mref.spnames.items())
#          print(faildcolumns,specs[specidxM[i]])

    # return ok,d,b

  def compareRcdnmol(self):
    '''
    Checks the radial column densities.
    Only the outermost points are checked (i.e. the total radial column density)
    '''

    # specidxM=[self.m.spnames[spname] for spname in self.specCompare if spname in self.m.spnames]
    # print(specidxM)
    # specidxMref=[self.mref.spnames[spname] for spname in self.specCompare if spname in self.mref.spnames]

    # for i in specidxM:
    #   self.m.rcdnmol[-1,self.m.rcdnmol[-1,:,i]<self.lcdnmol,i]=self.lcdnmol
    #
    # for i in specidxMref:
    #   self.mref.rcdnmol[-1,self.mref.rcdnmol[-1,:,i]<self.lcdnmol,i]=self.lcdnmol

    return self.diffArray(self.m.rcdnmol[-1,:,:],self.mref.rcdnmol[-1,:,:],**self.getTols(rtol=1.e-1,nlimfrac=0.1))
    # ok,d,b=self.diffArray(self.m.rcdnmol[-1,:,specidxM],self.mref.rcdnmol[-1,:,specidxMref],1.e-1,1.0,0.1)

    # if false check if it is only a certain fraction of the columns, it than can
    # be still okay
    # is not really elegant I would say
    # TODO: also somehow return the number of failed columns
    # TODO: maybe merge Cdnmol
    # if ok is False:
    #   ok=True  # and check if any columns faild
    #   for i in range(len(specidxMref)):
    #     faildcolumns=(d[:,i]>self.dcdnmol).sum()
    #     if ((float(faildcolumns)/float(len(d[:,i])))>self.fcdnmol):
    #       print(faildcolumns,len(d[:,i]),list(self.mref.spnames)[i])
    #       ok=False

    # return ok,d,b
  def compareSolved_chem(self):
    '''
    Compares the solved_chem field. The flag for the quality of the chemical solution.
    '''
    return self.diffArray(self.m.solved_chem,self.mref.solved_chem,**self.getTols(rtol=1.e-10,nlimfrac=0.1))

  def compareAbundances(self):
    """
    Compare the abundances.
    """
    if self.m.nspec!=self.mref.nspec: return False,None

    # set low values to zero
    # self.m.nmol[self.m.nmol<self.lAbundances]=self.lAbundances
    # self.mref.nmol[self.mref.nmol<self.lAbundances]=self.lAbundances

    # print(self.m.nmol[:,0,0])
    # print(self.mref.nmol[:,0,0])
    # only check a small selection of species
    # spec=("H2","CO","H2O","CO#","H2O#","H3+")
    specs=self.mref.spnames

    # want to compare the abundances
    amref=self.mref.nmol[:,:,:]*0.0
    am=self.m.nmol[:,:,:]*0.0
    for i in range(len(specs)):
      amref[:,:,i]=self.mref.nmol[:,:,i]/self.mref.nHtot
      am[:,:,i]=self.m.nmol[:,:,i]/self.m.nHtot

    # specidxM=[self.m.spnames[idx] for idx in specs if idx in self.m.spnames]
    # print(specidxM)
    # specidxMref=[self.mref.spnames[idx] for idx in specs if idx in self.mref.spnames]
    # print(specidxMref)
    # self.mref.solved_chem!=1 and
    mask=np.logical_and(am<1.e-20,amref<1.e-20)

    masknotsolved=np.logical_or(self.m.solved_chem!=1,self.mref.solved_chem!=1)

    # do not know a better ways
    for i in range(len(specs)):
      mask[:,:,i]=np.logical_or(mask[:,:,i],masknotsolved)

    return self.diffArray(am,amref,mask=mask,**self.getTols(rtol=1.e-3,nlimfrac=0.05))

  def compareElements(self):
    '''
    Compares the numbers from the Elemenst.out file.
    '''
    ok,val=self.diff(self.m.elements.muHamu,self.mref.elements.muHamu,rtol=1.e-5)
    if ok==False: return ok,val

    ok,val,b=self.diffArray(np.array(list(self.m.elements.amu.values())),
                          np.array(list(self.mref.elements.amu.values())),rtol=1.e-5)
    if ok==False: return ok,val,b

    ok,val,b=self.diffArray(np.array(list(self.m.elements.massRatio.values())),
                          np.array(list(self.mref.elements.massRatio.values())),rtol=1.e-5)
    if ok==False: return ok,val,b

    return self.diffArray(np.array(list(self.m.elements.abun12.values())),
                          np.array(list(self.mref.elements.abun12.values())),rtol=1.e-5)

  def compareSpecies(self):
    '''
    Compares the numbers from the Species.out file.
    '''

    ok,val,b=self.diffArray(np.array(list(self.m.species.mass.values())),
                          np.array(list(self.mref.species.mass.values())),rtol=1.e-5)
    if ok==False: return ok,val,b

    ok,val,b=self.diffArray(np.array(list(self.m.species.charge.values())),
                          np.array(list(self.mref.species.charge.values())),rtol=1.e-5)
    if ok==False: return ok,val,b

    return self.diffArray(np.array(list(self.m.species.chemPot.values())),
                          np.array(list(self.mref.species.chemPot.values())),rtol=1.e-5)

  def compareDustOpacEnv(self):
    '''
    Compares the dust opacities for an envelope model (optional output).
    '''
    if self.m.env_dust is None and self.mref.env_dust is None: return True,None
    if self.m.env_dust is not None and self.mref.env_dust is None: return False,None
    if self.m.env_dust is None and self.mref.env_dust is not None: return False,None

    return self.diffArray(self.m.env_dust.kext,self.mref.env_dust.kext,**self.getTols(rtol=1.e-3))

  def compareDustOpac(self):
    '''
    Compares the dust opacities.
    '''
    # self.tolerances["DustOpac.rtol"]=0.06
    return self.diffArray(self.m.dust.kext,self.mref.dust.kext,**self.getTols(rtol=1.e-3))

  def compareStarSpec(self):
    '''
    Compares the input Stellar spectrum, from X-rays to mm
    '''
    return self.diffArray(self.m.starSpec.Inu,self.mref.starSpec.Inu)

  def compareNHtot(self):
    '''
    checks the total hydrogen number density
    '''
    return self.diffArray(self.m.nHtot,self.mref.nHtot)

  def compareRhog(self):
    '''
    checks the gas density
    '''
    return self.diffArray(self.m.rhog,self.mref.rhog)

  def compareRhod(self):
    '''
    checks the dust density
    '''
    return self.diffArray(self.m.rhod,self.mref.rhod)

  def compareD2g(self):
    '''
    checks the resulting dust to gass mass ratio
    '''
    return self.diffArray(self.m.d2g,self.mref.d2g)

  def compareDamean(self):
    '''
    checks the resulting dust to gass mass ratio
    '''
    return self.diffArray(self.m.damean,self.mref.damean)

  def compareTg(self):
    '''
    checks the gas temperature
    '''
    return self.diffArray(self.m.tg,self.mref.tg,**self.getTols(rtol=2.e-2,nlimfrac=0.01))

  def compareTd(self):
    '''
    checks the dust temperature
    '''
    return self.diffArray(self.m.td,self.mref.td,**self.getTols(rtol=2.e-3,nlimfrac=0.01))

  def compareRadFields(self):
    '''
    checks the radiation fields
    '''
    return self.diffArray(self.m.radFields,self.mref.radFields,**self.getTols(rtol=2.e-2,nlimfrac=0.01))

  def compareZetaCR(self):
    '''
    checks the cosmic ray ionisation rate
    '''
    return self.diffArray(self.m.zetaCR,self.mref.zetaCR,**self.getTols(rtol=1.e-5))

  def compareZetaX(self):
    '''
    checks the Xray ionisation rate
    '''

    mask=np.logical_and(self.m.zetaX<1.e-25,self.mref.zetaX<1.e-25)

    return self.diffArray(self.m.zetaX,self.mref.zetaX,mask=mask,**self.getTols(rtol=1.e-1,nlimfrac=0.05))

  def compareHX(self):
    '''
    checks the Xray energy deposition rate
    '''
        # set low values to zero
#    self.m.Hx[self.m.zetaX < self.lZetaX]=self.lZetaX
#    self.mref.Hx[self.mref.zetaX < self.lZetaX]=self.lZetaX

    return self.diffArray(self.m.Hx,self.mref.Hx,**self.getTols(rtol=1.e-1,nlimfrac=0.05))

  def compareChemnet(self):
    '''
    Compare the chemical network. Uses the compare routine from `:class:~prodimopy.chemistry.network.ReactionNetwork
    '''
    # only tell if it is equal or  not, i.e. ingore all the other output
    ret=self.m.chemnet.compare(self.mref.chemnet,printresults=False,log=False)
    return (ret[0],None,None)

  def compareFileCheckNetworkLog(self):
    '''
    Makes a file comparison with CheckNetwork.log
    '''
    return self.diffFile("CheckNetwork.log")

  def compareFileCheckChemLog(self):
    '''
    Makes a file comparison with CheckChem.log
    '''
    return self.diffFile("CheckChem.log")

  def compareFitsFileRestart(self):
    '''
    Makes a fits file comparison with restart.fits.gz
    '''
    return self.diffFitsFile("restart.fits.gz",rtol=1.e-3)

  def compareFitsFileMie(self):
    '''
    Makes a fits file comparison with Mie.fits.gz
    '''
    return self.diffFitsFile("Mie.fits.gz",rtol=1.e-5)

  def compareFitsFileLineCubes(self):
    '''
    Makes a fits file comparison with Mie.fits.gz
    '''
    fcubes=glob.glob(self.m.directory+"/LINE_3D_???.fits")

    # FIXME: rtol is pretty high
    # FIXME: this deos not work if the other model actually has linecubes
    # e.g. it would say that it is okay
    if fcubes is not None:
      for fname in fcubes:
        ok,val=self.diffFitsFile(os.path.basename(fname),rtol=1.e-3)
        if not ok:  # stop the whole thing if one cube went wrong
          return ok,val

    return True,None


class CompareMc(CompareAbs):
  """
  Class for comparing two ProDiMo models of type :class:`~prodimopy.read_mc.Data_mc`

  Every compare Function returns true or false, and the relative differences
  (in case of arrays these are arrays).

  Can be used in e.g. automatic testing routines or in simple command line
  tools to compare ProDiMo model results.
  """

  def __init__(self,model,modelref):
    """
    Parameters
    ----------
    model : :class:`~prodimopy.read_mc.Data_mc`
      The model one wants to compare.

    modelref : :class:`~prodimopy.read_mc.Data_mc`
      The reference model to compare with.

    Attributes
    ----------

    """

    if model is None or modelref is None:
      raise TypeError("Either model or modelref is None, no comparison possible.")

    self.m=model
    """ :class:`~prodimopy.read_mc.Data_mc` :
    The model one wants to compare.
    """
    self.mref=modelref
    """ :class:`~prodimopy.read_mc.Data_mc`  :
    The reference model to compare with.
    """

  def compareAbundances(self):
    """
    Compares the abundances of two molecular cloud (0D chemistry) models.

    Assumes that both models used the same number of ages and species in the same order.
    """

    # set low values to equal numbers, which means they are kind of ignored
    # in the comparison
    # self.m.abundances[self.m.abundances<self.lAbundances]=self.lAbundances
    # self.mref.abundances[self.mref.abundances<self.lAbundances]=self.lAbundances

    # Do not consider the first age entry at it is the initial conditions
    # that can vary from model two model and are not really a result

    mask=np.logical_and(self.m.abundances[1:,:]<1.e-20,self.mref.abundances[1:,:]<1.e-20)
    return self.diffArray(self.m.abundances[1:,:],self.mref.abundances[1:,:],rtol=5.e-2,mask=mask)

  def compareRatecoefficients(self):
    """
    Compares the rate coefficients of two molecular cloud (0D chemistry) models.

    Assumes that both models have exactly the same chemical reactions in the same order.
    """

    if len(self.m.ratecoefficients)!=len(self.mref.ratecoefficients):
      return False,None,None

    mask=np.logical_and(self.m.ratecoefficients<1.e-50,self.mref.ratecoefficients<1.e-50)
    return self.diffArray(self.m.ratecoefficients,self.mref.ratecoefficients,rtol=2.e-7,mask=mask)


def eval_model_type(modelDir):
  """
  Try to guess the model type (e.g. mc, full prodimo etc.).
  Default is always prodimo.

  Possible types:

    `prodimo` .... full prodimo model (:class:`prodimopy.read.Data_ProDiMo`)

    `mc` ......... molecular cloud model (:class:`prodimopy.read_mc.Data_mc`)

  Returns
  -------
    str either `prodimo` or `mc`

  FIXME: this is maybe not the best place for this routine
  FIXME: provide constants for the values (what's the best way to do this in pyhton?)
  FIXME: this is just a quick hack, it would be better to use the parameters in Parameter.in

  """

  if os.path.isfile(modelDir+"/ProDiMo_01.out") or \
     os.path.isfile(modelDir+"/ProDiMo_001.out") or \
     os.path.isfile(modelDir+"/ProDiMo_0001.out") or \
     os.path.isfile(modelDir+"/ProDiMo_00001.out"):
    mtype="prodimoTD"
  elif os.path.isfile(modelDir+"/Molecular_Cloud_Input.in"):
    mtype="mc"
  else:
    mtype="prodimo"

  return mtype

#   def compareFlineEstimates(self):
#     '''
#     Compares the FlineEstimaes
#     '''
#
#     if len(self.m.lineEstimates) !=len(self.mref.lineEstimates):
#       return False,None
#
#
#     self.diff(self.m.lineEstimate[i].flux, self.mref.lineEstimate[i].flux, self.dLineFluxes)
#
#     # Compare fluxes
#     for i in range(len(self.m.lines)):
#         f,d=
#         if f == False:
#           return False,d
#
#     return True,None
#

