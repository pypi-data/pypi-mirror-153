"""
.. module:: grid 
   :synopsis: Simple helper routines to generate small |prodimo| model grids. 

.. moduleauthor:: Ch. Rab
"""

from __future__ import print_function
from __future__ import division 
from __future__ import unicode_literals

import numpy
import math

import os
import shutil
import collections
import glob


def chgriddir(gridname):
  """
  Changes the current working directory to the grid directory.
  
  Verifies if I am already in the grid directory.

  Parameters
  ----------
  gridname : str
    The name of the grid (the directory with the models).

  """
  if not os.getcwd().endswith("/"+gridname):
    os.chdir(gridname)

def genparamentry(name,value):
  
  if name == "fcarbon":
    fsil=1.0-(0.25+value)
    entry = "3           ! NDUST    \n"
    entry = entry+"  "+str(fsil)+"       Mg0.7Fe0.3SiO3[s] \n"
    entry = entry+"  "+str(value)+"      amC-Zubko[s] \n"
    entry = entry+"  0.25      vacuum[s] \n"    
  else:    
    entry=str(value)+"  ! "+name +" \n"
  return entry


def genvalues(param):
  """
  Generates the values for the given parameter.
  
  Currently only lineare and logarithmic spacing is possible. 
  
  .. todo::
    allow boolean type of parameters
  .. todo::
    allow for the dust composition parameters
  """
  start=param[1]
  end=param[2]
  steps=param[3]
  linlog=param[4]
  
  if linlog=="lin":
    return numpy.linspace(start,end,steps)
  elif linlog=="log":
    return numpy.logspace(math.log10(start),math.log10(end),steps,base=10.0)
  else:
    print("Unknown spacing type")
    return None


def run_grid(gridname,modeldirs,runProDiMo):
  """
  Runs the grid.
  
  Changes to the grid directory and runs each model by either calling 
  a passed python function or a system command string (see parameters).
  
  Parameters
  ----------
  gridname : str
    The name of the grid (the directory with the models).
    
  modeldirs : list
    a list of all models in the grid (also the directory name of each model) 

  runProDiMo : str or method object
    if it is a `str` the string is interpreted as a system command.
    Any accurence of `$MODELNAME$` in the given string is replaced by 
    the actual model name (model directory).
    
    if the parameter is a python function. This funcion is called with 
    the modeldir as a parameter.   
    
  """
  chgriddir(gridname)
  for modeldir in modeldirs:
    if isinstance(runProDiMo, collections.Callable):
      print("run "+modeldir+", exec. function: "+runProDiMo.__name__)
      runProDiMo(modeldir)
    else:
      runProDiMoCMD=runProDiMo.replace("$MODELNAME$",modeldir)
      os.chdir(modeldir)
      print("run "+modeldir+", exec. command: "+runProDiMoCMD)
      os.system(runProDiMoCMD)
      os.chdir("..")
  # go back to the original working directory
  os.chdir("..")


def get_modeldirs(modeldirs):
  """
  Returns all grid models of the current grid. 
  If modeldirs is not `
  Assumes that I am already in the grid directory.
  
  .. todo ::
    also pass the gridname as optional parameter. 
  
  Returns
  -------
  list
    If `modeldirs` is not `None` `modeldirs` is returned.
    Otherwise all directory names staring with `model*/` are returned. 
  
  """
  if modeldirs is None:
    modeldirs=glob.glob("model*/")
  return modeldirs

def check_grid(gridname,modeldirs=None):
  """
  Checks if all models look okay.
  
  This routine checks if finished.out exists for all models of the grid.

  Parameters
  ----------
  gridname : str
    The name of the grid (the directory with the models).
    
  modeldirs : list
    a list of all models in the grid (directory name of each model).
    
    If `modeldirs` is `None` all directories with names starting with `model` are 
    considered as potential grid models. 
  """

  chgriddir(gridname)
  
  # guess the model directories  
  modeldirs = get_modeldirs(modeldirs)
    
  for modeldir in modeldirs:
    if not os.path.isfile(modeldir+"/finished.out"):
      print("Model "+modeldir+" failed:") 
  

def sel_lowest_chisquare(gridname,modeldirs=None,tolerance=None):
  """
  Selects the model(s) with the lowest chi squared. If a tolerance is 
  given all models within this tolerance, measured relative to the minimum 
  chi square are selected.
  
  Parameters
  ----------
  gridname : str
    The name of the grid (the directory with the models).
    
  modeldirs : list
    a list of all models in the grid (directory name of each model).
    
    If `modeldirs` is `None` all directories with names starting with `model` are 
    considered as potential grid models. 
  """

  chgriddir(gridname)
  modeldirs=get_modeldirs(modeldirs)
  nmodels=len(modeldirs)
  
  chisquares=numpy.ndarray(shape=(nmodels))
  chisquares[:]=1.e100
  # go through all models and read the chi square  
  for i in range(nmodels):
    modeldir=modeldirs[i]
    if os.path.isfile(modeldir+"/finished.out"):
      ffin=open(modeldir+"/finished.out")
      for line in ffin:
        if "total chi" in line:
          val=float(line.split("=")[1])
          chisquares[i]=val
          
  minchi=numpy.min(chisquares)  
  if tolerance is not None:
    tol=minchi*tolerance
    idx=numpy.where(numpy.abs(chisquares-minchi)<tol)[0]
  else:
    idx=numpy.argmin(chisquares)
  
  # need to convert to numpy array, otherwise selection of multiple indices
  # does not work
  return numpy.array(modeldirs)[idx],chisquares[idx]

def sel_param_val(gridname,param,value,modeldirs=None):
  """
  Very primitiv and inefficient method to select models having a certain 
  value of a parameter.
  """
  chgriddir(gridname)
  modeldirs=get_modeldirs(modeldirs)
  nmodels=len(modeldirs)
  
  selmodels=list()
  for i in range(nmodels):
    modeldir=modeldirs[i]
    if os.path.isfile(modeldir+"/ParameterGrid.in"):
      ffin=open(modeldir+"/ParameterGrid.in")
      for line in ffin:
        if param in line:
          val=float(line.split("!")[0])
          if val == value:
            selmodels.append(modeldir)

  return selmodels


def make_grid(gridname,params,indir=None):
  """
  Produces a grid of prodimo models. 
  
  A directory with the name gridname is created. Within this directory for 
  each parameter combination a directory is created. This directory is initially
  copied from the directory given by indir and additionally the new parameters 
  are added to a ParameterGrid.in file. If ParameterGrid.in does not exist
  it will be created.

  .. todo:: 
    deal with dust composition properties (e.g. carbon fraction)  
  .. todo::
    deal with boolean values  
  .. todo::
    deal with something like stellar particles and CR spectra (e.g. on/off)

  Parameters
  ----------
  gridname : str
    The name of the grid (the directory with the models).

  params : list
    the list of parameters. 
    Each entry contains the parameter name, its start and end value, the number
    of steps and if either linear (lin) or logarithmic (log) spacing should be 
    used.
    
  indir : str
    an input or starting directorz containing the usual |prodimo| input 
    files. This directory is copied into a new model.
    
    If it is `None` only the ParameterGrid.in are created
    
  Returns
  -------
  list
    the list of modelnames (directory names)
  
  """

  # make the list for the meshgrid
  values=list()
  for param in params:
    values.append(genvalues(param))
  
  grid=numpy.meshgrid(*values)

  # create the directory for the grid
  os.mkdir(gridname)
  
  # create an iterator that loops over all indices of the firt grid array (all combinations)
  it = numpy.nditer(grid[0], flags=['multi_index'])
  imodel=0
  modelnames=list()
  while not it.finished:
    # create the model directory
    modelname="model"+"{:07d}".format(imodel)
    modeldir=gridname+"/"+modelname
    if indir is not None:
      shutil.copytree(indir,modeldir)
    else: 
      os.mkdir(modeldir)
    fparam=open(modeldir+"/ParameterGrid.in","a+")
    for iparam in range(len(params)):
      #fparam.write(str(grid[iparam][it.multi_index])+"  ! "+params[iparam][0] +" \n")
      fparam.write(genparamentry(params[iparam][0], grid[iparam][it.multi_index]))
    fparam.close()
    imodel=imodel+1
    modelnames.append(modelname)  
    it.iternext()

  return modelnames