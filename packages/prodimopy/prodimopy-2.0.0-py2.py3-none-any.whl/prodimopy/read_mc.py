"""
.. module:: read_mc
   :synopsis: Read routines and data structure for molecular cloud (0D chemistry) |prodimo| models.

.. moduleauthor:: Ch. Rab


"""
from __future__ import division
from __future__ import print_function

import os

import numpy as np


class Data_mc(object):
  """
  Data structure for molecular cloud (0D chemistry) |prodimo| models.

  Can be used for time-dependent abundances or for steady-state (or final) abundances.
  """

  def __init__(self,name):
    """
    Parameters
    ----------

    name : string
      The name of the model.


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
    Is e.g. set :meth:`~prodimopy.read_mc.read_mc`
    Can be a relative path.
    """
    self.species=None
    """ array_like(string,ndim=1) :
    an ordered list of species names.
    """
    self.ages=None
    """ array_like(float,ndim=1) :
    the output ages of the model.
    """
    self.ratecoefficients=None
    """ array_like(float,ndim=1) :
    The rate coefficients (just the rates as an array)
    """
    self.abundances=None
    """ array_like(float,ndim=2) :
    the abundances for each species and each age `DIMS:` (number of ages,number of species).
    """

  def __str__(self):
    output="Info MC: \n"
    output+="\n Species: \n"
    output+=str(self.species)
    output+="\n"
    output+="\n Ages: \n"
    output+=str(self.ages)
    return output


def _read_ages(filename):
  # f=open(filename,"r")

  # print(f.readlines())
  print("READ: Reading File: ",filename," ...")
  ages=np.loadtxt(filename)
  # insert age zero initial abundance
  ages=np.insert(ages,0,0.0)

  # f.close()

  return ages


def read_tdep_file(filename):
  '''
  Trys to read the MC_conc_tdep.out file and returns the ages and
  and abundances of that file.

  This file actually includes the number densities and not abundances.
  Try to estimate the abundances by adding up H, H2 and H+

  Currently this file does not include the initial abundances!

  .. todo::
    * This is quick and dirty. However, the problem is more in |prodimo| because
      it is unclear what file is for what and when (depending on parameter configuration)
      which file is written.
    * This does not deal with the two e- like in the normal mode. This is inconsistent.

  Returns
  -------
    tuple
      Returns a tuple containen the list of species, the list of ages, and the
      species abundances (in that order)

    '''
  # print(f.readlines())
  print("READ: Reading File: ",filename," ...")
  fp=open(filename)
  line=fp.readline()
  species=line.strip().split()[1:]  # the first column is the time
  print("INFO: Found "+str(len(species))+" species")

  # Replace some species names
  try:
    species[species.index("HN2+")]="N2H+"
  except ValueError:
    pass  # should be fine for python 3

  try:
    species[species.index("el")]="e-"
  except ValueError:
    pass  # should be fine for python 3

  data=np.loadtxt(filename,skiprows=1)
  ages=data[:,0]
  abundances=data[:,1:]

  nH=(abundances[0,species.index("H")]+2*abundances[0,species.index("H2")]+abundances[0,species.index("H+")]
    +abundances[-1,species.index("H")]+2*abundances[-1,species.index("H2")]+abundances[-1,species.index("H+")])/2.0
  abundances=abundances/nH
  print("WARN: Used a hydrogen number density of "+"{:7.5e}".format(nH)+" to calculate the abundances. This might not be accurate enough!")

  return species,ages,abundances


def _read_species(filename):
  print("READ: Reading File: ",filename," ...")
  f=open(filename,"r")

  species=[strr.strip() for strr in f.readlines()]
  species[species.index("HN2+")]="N2H+"

  # quick an dirty fix for el_is_sp. If the first and last element are e-
  # remove the last one
  if species[0]=="e-" and species[-1]=="e-":
    del(species[-1])

  f.close()

  return species


def _read_ratecoefficients(filename):
  """
  Currently returns just an array with the rate coefficients.
  Does not provide information on the reaction etc.
  But this is usefull for comparing models.

  All rates with values <1.e-200 will be set to 1.e-200 to avoid problems
  with zeros
  """
  print("READ: Reading File: ",filename," ...")
  f=open(filename,"r")

  rcs=list()
  for line in f:
    fields=line.split()
    rcs.append(max(1.e-200,float(fields[1])))

  f.close()

  return np.array(rcs)


def read_mc_final(filename="Molecular_cloud.out",directory=".",name=None):
  """
  Reads the final (last timestep) molecular cloud abundances.

  Parameters
  ----------

  filename : string
    The name of the file containing the abundances (optional).

  directory : string
    The model directory (optional).

  name : string
    The name of the model. Will be shown in the plots (optional).


  FIXME: ist not consistent with read_mc, e.g. the species names such as N2H+ are not adapted here

  FIXME: use numpy arrays for the abundances such as for time-dependent models.

  """
  # if name == None:
  #  dirfields = directory.split("/")
  #  name = dirfields[len(dirfields) - 1]

  mc=Data_mc(name)

  f=open(directory+"/"+filename)
  lines=f.readlines()
  f.close()

  species=list()
  abun=list()

  for line in lines:
    fields=line.strip().split()
    species.append(fields[0])
    abun.append(float(fields[2]))

  mc.species=species
  mc.abundances=np.array(abun)

  return mc


def read_mc(filename="mc_output.txt",directory=".",agesfile="mc_ages.txt",speciesfile="mc_species.txt",rcfile="MC_rate_coefficients.txt",name=None):
  """
  Read routine for molecular cloud |prodimo| models including the ages and the species list.

  Parameters
  ----------

  filename: string
    The name of the file containing the abundances for all ages.
    Please check what output file you have in your particular model and adapt
    it here. (default: `mc_output.txt`)

    It is rather confusing how it is done in |prodimo|. So it is hard
    to find a clean solution here.

    The routine also try now to read the `MC_conc_tdep.out` if there is not
    `agesfile` (i.e. "mc_ages.txt"). However, in that file the initial abundances
    are not included.

  directory : string
    The model directory.

  agesfile: string
    The file with the ages (default: `mc_ages.txt`)

  speciesfile: string
    The file with the species names (default: `mc_species.txt`)

  rcfile: string
    The file with the calculated rate coefficients (default: `MC_rate_coefficients.txt`)

  """
  # if name == None: name=
  #  dirfields = directory.split("/")
  #  name = dirfields[len(dirfields) - 1]

  mc=Data_mc(name)

  mc.directory=directory
  mc.ratecoefficients=_read_ratecoefficients(directory+"/"+rcfile)

  # if there is a MC_conc_tdep.out and no mc_ages.txt read the data from there
  if (not os.path.isfile(directory+"/"+agesfile) and
      os.path.isfile(directory+"/MC_conc_tdep.out")):
    mc.species,mc.ages,mc.abundances=read_tdep_file(directory+"/MC_conc_tdep.out")
  else:
    mc.species=_read_species(directory+"/"+speciesfile)
    mc.ages=_read_ages(directory+"/"+agesfile)
    # make ages first index, species second
    print("READ: Reading File: ",directory+"/"+filename," ...")
    mc.abundances=np.transpose(np.loadtxt(directory+"/"+filename))
    # FIXME: quick an dirty fix for el_is_sp true if the len of species is smaller
    if (len(mc.species)<mc.abundances.shape[1]):
      mc.abundances=np.delete(mc.abundances,-1,axis=1)

  return mc


def read_umist(directory,filename="dc_molecules.dat",name=None):
  """
  Reads the results of a UMIST rate13 code model.
  Uses the output produced by dc.pl script provided by the UMIST code distribution.

  The data is provided as a :class:`prodimopy.read_mc.Data_mc` object.
  """

  if name==None:
    dirfields=directory.split("/")
    name=dirfields[len(dirfields)-1]

  f=open(directory+"/"+filename,"r")

  lines=f.readlines()

  header=lines[0].strip()
  header=header[2:]
  species=header.split(" ")

  ages=list()
  abun=list()

  for i in range(1,len(lines)):
    line=lines[i].strip()
    fields=line.split(" ")
    ages.append(float(fields[0]))
    abun.append(fields[1:])

  out=Data_mc(name)
  out.ages=np.array(ages,dtype='|S4').astype(np.float)
  out.ages=np.array(ages)
  out.species=species
  out.abundances=np.array(abun).astype(np.float)

  return out


if __name__=="__main__":
  mc=read_mc("tests/mc","mc.out")

  print(mc.species)
  print(mc.ages)
  print(mc.abundances[:,mc.species.index("H2")])
