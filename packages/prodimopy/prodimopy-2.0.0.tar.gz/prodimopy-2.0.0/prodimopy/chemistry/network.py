'''
Created on 15 Feb 2021

@author: Christian Rab
'''
from abc import ABC,abstractmethod
import math
from timeit import default_timer as timer

import numpy as np


class ReactionNetwork(ABC):
  '''
  General representation of a chemical reaction network.

  .. todo::

    make it an abstract class that requires the child classes to implement
    the load_reactions routine. Currently this only works for the Reactions.out
    from ProDiMo.

  '''

  def __init__(self,name="ReactionNetwork"):
    '''
    Create a new Reaction Network.
    '''
    self.name=name
    ''' string :
    A name for the reaction network
    '''
    self.reactions=list()
    ''' list(:class:`Reaction`) :
    The list of reactions included in the network.
    '''
    self._species=list()
    ''' list(str) :
    The list of species derived from the list of Reactions.
    Is create via a property function.
    '''
    self.filename=None
    ''' string :
    The name/path of the file containing the Reaction network.
    '''
    self.non_species=['PE','PHOT','PHOTON','XPHOT','M','ELECTR','PHOTON',
                    'GRAIN','FORM','CRPHOT','CRP','SPONT','DESCR','DESPH','DESTH',
                    'CRP','CP','e-','M',"dust"]
    '''
    A list of Species names that are considerd as non species (not really a chemical species) but
    might be included in the network.
    FIXME: provide a way to change that list
    '''

  @property
  def species(self):
    '''
    The list of individual species in the network.
    '''
    # only load if not yet loaded.
    if len(self._species)==0:
      # Create a species list
      for reac in self.reactions:
        for spec in reac.reactants+reac.products:
          # print(spec)
          if not spec in self._species and spec not in self.non_species:
            self._species.append(spec)

      self._species.sort()
    return self._species

  def __str__(self):
    return "Name: "+self.name+"\n"+" File : "+str(self.filename)+"\n"+" Number of Reactions: "+str(len(self.reactions))+"\n Number of Species: "+str(len(self.species))

  def duplicates(self):
    '''
    Returns possible duplicate reactions in the network.

    TODO: is quite slow
    TODO: properly define what is a duplicate

    Returns
    -------
    list(:class:`Reaction`) :
      Returns a list of the duplicate Reactions or an empty list if there are
      no duplicates
    '''
    dups=list()
    # starttime=timer()
    for ridx,reac in enumerate(self.reactions):
      for reac2 in self.reactions[(ridx+1):]:
        if (self._duplicatereaction(reac.compare(reac2))):
          dups.append((reac,reac2))
          break

    # print("Time: ","{:4.2f}".format(timer()-starttime)+" s")
    return dups

  def compareSpecies(self,reactionNetwork):
    '''
    Compares the species list of two networks.

    Parameters
    ----------

    reactionNetwork : :class:`ReactionNetwork`
      Another reaction network


    Returns
    -------
    (tuple) :

    * `boolean` ... equal or not
    * list ... list of species only in  old network
    * list ... list of species only in new network

    '''

    specOld=self.species
    specNew=reactionNetwork.species

    # propably not very fast but fast enough I guess
    onlyOld=list()
    for spec in specOld:
      if spec not in specNew:
        onlyOld.append(spec)

    onlyNew=list()
    for spec in specNew:
      if spec not in specOld:
        onlyNew.append(spec)

    # if both empty the species are the same,
    return (not onlyOld and not onlyNew,onlyOld,onlyNew)

  def compare(self,reactionNetwork,printresults=False,eqfunc=None,chgfunc=None,log=True):
    '''
    Compares the network to the given reaction network.
    Currently simply prints out the results to stdout.

    Parameters
    ----------

    reactionNetwork : :class:`ReactionNetwork`
      Another reaction network

    printresults : boolean
      Print the results to stdout

    eqfunc :
      Pass a function that decides if two Reactions are equal.
      The function must take as an argument the outcome of the Reaction
      compare function.

    chgfunc :
      Pass a function that decides if two Reactions are the same Reactoin but
      some other quantities changes (coefficients, type etc).
      The function must take as an argument the outcome of the Reaction
      compare function.

    log : boolean
      Include log output (print statements) or not.

    Returns
    -------
    (tuple) :

    * `boolean` ... equal or not
    * list ... list of changed reactions
    * list ... list of reactions only in this network
    * list ... list of reactions only in the passed network
    '''

    starttime=timer()

    if log: print("INFO: compare ",self.name," to ",reactionNetwork.name," ...")
    # Copy the reaction list as we will change it
    reactionsNew=reactionNetwork.reactions.copy()

    eqf=self._equalreaction
    if eqfunc is not None:
      eqf=eqfunc

    chgf=self._changedreaction
    if chgfunc is not None:
      chgf=chgfunc

    # Compare the two databases
    changed=list()
    onlyold=list()
    for reac in self.reactions:
      found=False
      for reacNew in reactionsNew:
        equal=reac.compare(reacNew)
        if eqf(equal):  # found the equal reaction ... done
          found=True
          # now we can remove it is already found
          reactionsNew.remove(reacNew)
          break
        elif chgf(equal):  # found a changed reactions ... done
          changed.append((reac,reacNew,equal))
          found=True
          # now we can remove it is already found
          reactionsNew.remove(reacNew)
          break

      # collect the ones only in the old
      if not found:
        onlyold.append(reac)

    # the rest must be the onlynew ones
    onlynew=reactionsNew

    equal=len(changed)==0 and len(onlyold)==0 and len(onlynew)==0

    if log: print("INFO: time: ","{:4.2f}".format(timer()-starttime)+" s")
    if printresults:
      print(" ")
      print("FOUND "+str(len(changed))+" CHANGED REACTIONS: ")
      for cr in changed:
        print("OLD: ",cr[0])
        print("NEW: ",cr[1])
        print("EQUAL: ",cr[2])
        print(" ")
      print(" ")

      print(" ")
      print("FOUND "+str(len(onlyold))+" REACTIONS THAT ONLY EXIST IN NETWORK "+self.name+" (OLD): ")
      for r in onlyold:
        print(r)
      print(" ")

      print(" ")
      print("FOUND "+str(len(onlynew))+" REACTIONS THAT ONLY EXIST IN NETWORK "+reactionNetwork.name+" (NEW): ")
      for r in onlynew:
        print(r)
      print(" ")

    return equal,changed,onlyold,onlynew

  def _duplicatereaction(self,eq):
    '''
    Defines what is a duplicate reaction depending on the eq dictionary.

    Parameters
    ----------
    eq : dictionary
      The equal dictionsary see

    '''
    return eq["reactants"] and eq["products"]

  def _equalreaction(self,eq):
    '''
    Are the reactions equal?
    '''
    return eq["reactants"] and eq["products"] and eq["coeffs"] and eq["rate"]==True

  def _changedreaction(self,eq):
    '''
    Has the reaction changed?
    '''
    return (eq["reactants"] and eq["products"]) and (eq["coeffs"]==False or eq["type"]==False or eq["gasphase"]==False or eq["rate"]==False)

  @abstractmethod
  def load_reactions(self,filename=None):
    '''
    In this routine the reading of the Reaction network needs to be implemented.

    Fills in the `reactions` field in this class.

    Parameters
    ----------

    filename : str
      The name/path of the file to read
    '''
    pass

  @abstractmethod
  def load_rates(self,filename=None):
    '''
    In this routine the reading of rate coeeficients need to be implemented.

    Parameters
    ----------

    filename : str
      The name/path of the file to read
    '''
    pass


class Reaction(object):
  '''
  General representation of one chemical reaction.
  '''

  def __init__(self):
    self.id=0
    """ int :
    The Reaction Id as is
    """
    self.idU=0
    """ int :
    The Umist reaction id ... it is unclear what this actually is.
    """
    self.type=""
    """ string :
    The Reation type identifier as used in ProDiMo
    """
    self.gasphase=None
    """ boolean :
    Gas phase reaction or not.
    """
    self.reactants=list()
    """ array_like :
    The list of reaction reactants (Species names)
    """
    self.products=list()
    """ array_like :
    The list of reaction products (Species names)
    """
    self.coeffs=np.zeros(shape=(3))
    """ array_like(float,shape=) :
    The `[alpha,beta,gamma]` coefficients per temperature range. For multipe temperature ranges
    it will become a 2D array with shape (3,number of t ranges) e.g. `[[alpha,beta and gamma],[alpha2,beta2,gamma2]]`
    for two temperature ranges.
    FIXME: might be hard to handle as it can either be 1D or 2D array. Could be fixed with a @property decorator
    """
    self.temps=np.zeros(shape=(2))
    """ array_like
    The temperature range ([min,max]). Can have more entries if there are several temperature ranges.
    The shape will than be (2,number of t ranges)).
    FIXME: might be hard to handle as it can either be 1D or 2D array.
    """
    self.rate=None
    """ float :
    The real rate for a given set of physical conditions.
    """
    self.clem=None
    """ str :
    Something from UMIST do not know what it is.
    """
    self.accuracy=None
    """ str :
    A string describing the quality of the reactions coefficients
    """

    self.comment=""
    """ str :
    Any relevant comment for this particular reaction.
    """

  def compare(self,reaction):
    '''
    Compares the Reaction to the passed reaction.

    The routines evaluates for a selection of the properties from `class:`Reaction` individually if it
    is equal or not. See below for the return value.

    Parameters
    ----------
    reaction : :class:`Reaction`

    Returns
    -------
    dictionary :
    A dictionary with boolean values with the following keys. The keys have the
    same names as the properties of the :class:`Reaction`.

    * `type`
    * `gasphase`
    * `reactants`
    * `products`
    * `coeffs`
    * `temps`

    ..todo :
      * deal with comparison of the network if rates only exist in one network
      * the value of the rate coeffs are not compared/checked
      * make the tolerances for comparison of the rate a parameter somehow
    '''

    equal=dict()
#     if self.id != reaction.id:
#       equal["id"]=False

#     if self.idU != reaction.idU:
#       equal["idU"]=False

    equal["type"]=self.type==reaction.type
    equal["gasphase"]=self.gasphase==reaction.gasphase
    equal["reactants"]=sorted(self.reactants)==sorted(reaction.reactants)
    equal["products"]=sorted(self.products)==sorted(reaction.products)

    equal["coeffs"]=True
    # could be different because of multiple temperature ranges
    flat=self.coeffs.flatten()
    flatNew=reaction.coeffs.flatten()
    if len(flat)!=len(flatNew):
      equal["coeffs"]=False
    else:
      if not all(flat==flatNew):
        equal["coeffs"]=False

    equal["temps"]=True
    # could be different because of multiple temperature ranges
    # check for Nones
    if self.temps is None or reaction.temps is None:
      equal["temps"]=False
    else:
      flat=self.temps.flatten()
      flatNew=reaction.temps.flatten()
      if len(flat)!=len(flatNew):
        equal["temps"]=False
      else:
        if not all(flat==flatNew):
          equal["temps"]=False

    # TODO: if not loaded in both reactions, the comparison does not make sense
    # TOD
    # Maybe write an error.
    if self.rate!=None and reaction.rate!=None:
      # print(self.rate,reaction.rate,math.isclose(self.rate,reaction.rate,rel_tol=1e-20,abs_tol=0.0))
      equal["rate"]=math.isclose(self.rate,reaction.rate,rel_tol=1e-4,abs_tol=0.0)
    else:
      equal["rate"]=True

    return equal

  def __str__(self):
    out=str(self.id)+" "+str(self.idU)+" "+str(self.type)+" "+str(self.reactants)+" "+str(self.products)+" "+str(self.coeffs)+" "+str(self.temps)
    if self.rate!=None:
      out=out+"{:13.5e}".format(self.rate)

    out=out+" "+self.comment
    return out


class ReactionNetworkPout(ReactionNetwork):
  '''
  Implementation of ReactionNetwork for the Reaction.out of a ProDiMo model.

  '''

  def __init__(self,name=None,modeldir=None):
    '''

    Parameters
    ----------

    modeldir : str
      If set the init routine trys to load the Reactions.out and the
      rates log file (at the moment). But continues if it does not work
    '''

    super().__init__(name=name)

    if self.name==None and modeldir is not None:
      self.name=modeldir

    if modeldir is not None:
      try:
        self.load_reactions(filename=modeldir+"/Reactions.out")
      except:
        print("WARN: Could not load reactions from Reactions.out")

      try:
        self.load_rates(filename=modeldir+"/rate_coeffs_1NZZ.log")
      except:
        print("WARN: Could not load rate coefficients from rate_coeffs_1NZZ.log")

      print(" ")

  def load_reactions(self,filename="Reactions.out"):
    '''
    Reads a reaction network in the format of the ProDiMo Reactions.out.

    Fills in the `reactions` field in this class.

    Parameters
    ----------

    filename : str
      The name/path of the file to read

    '''
    fr=open(filename)
    self.filename=filename

    lines=fr.readlines()

    # stupid workaround for old format
    oldformat=False
    for line in lines:

      if not oldformat:
        fields=line.split()
        # print(fields[-6])
        try:
          tidx=int(fields[-6])
        except ValueError:
          print("WARN: Try to read an older format ... let's hope it works!")
          oldformat=True

      if oldformat:
      # now insert some spaces at the right places for the coefficients
        line=line[:23]+" "+line[23:]
        line=line[:53]+" "+line[53:]
        line=line[:-43+8]+" "+line[-43+8:]
        line=line[:-43+17]+" "+line[-43+17:]

        fields=line.split()
        tidx=int(fields[-6])

      # new Reaction
      if tidx==1:
        reac=Reaction()
        # new reactions, append it and fill it
        self.reactions.append(reac)
        reac.id=int(fields[0])
        reac.idU=int(fields[1])
        reac.type=fields[2]

        if oldformat:
          reac.gasphase=True

          reacprod=fields[3:-6]
        else:
          reac.gasphase=fields[3].strip()=="T:"
          reacprod=fields[4:-6]

        reac.coeffs[:]=[float(fields[-5]),float(fields[-4]),float(fields[-3])]
        reac.temps[:]=[float(fields[-2]),float(fields[-1])]

        # print(reacprod)
        nextisprod=False
        for entry in reacprod:
          if entry=="-->":
            nextisprod=True

          elif entry=="+":
            continue
          else:
            if nextisprod:
              reac.products.append(entry)
            else:
              reac.reactants.append(entry)
      else:
        reac=self.reactions[-1]
        reac.coeffs=np.vstack((reac.coeffs,[float(fields[-5]),float(fields[-4]),float(fields[-3])]))
        reac.temps=np.vstack((reac.temps,[float(fields[-2]),float(fields[-1])]))

      # print(reac)
    fr.close()
    print("Loaded ",len(self.reactions)," Reactions from ",self.filename)

  def _equalreaction(self,eq):
    '''
    Are the reactions equal?
    '''
    # here we also have the type
    return super()._equalreaction(eq) and eq["type"]==True

  def load_rates(self,filename="rate_coeffs_1NZZ.log"):
    '''
    Load the real rates for a given set of physical conditions.
    Can be use for comparison.

    Has to be run after load_reactions.

    .. todo::

      Is not general; just a test at the moment.

    '''
    rates=np.loadtxt(filename,usecols=[1])

    for i,reaction in enumerate(self.reactions):
      reaction.rate=rates[i]


class ReactionNetworkPin(ReactionNetwork):
  '''
  Implementation of ReactionNetwork for the Reactions.in of ProDiMo.

  '''

  def __init__(self,name=None,modeldir=None):
    '''

    Parameters
    ----------

    name : str
      a name for the network

    modeldir : str
      If set, the init routine trys to load the `Reactions.in` from modeldir.
      But continues if it does not work.

    '''
    super().__init__(name=name)
    self.modeldir=modeldir

    if self.name==None and modeldir is not None:
      self.name=modeldir

    if modeldir is not None:
      try:
        self.load_reactions(filename=modeldir+"/Reactions.in")
      except Exception as err:
        print("WARN: Could not load reactions from Reactions.in",err)
      print(" ")

  def _equalreaction(self,eq):
    '''
    Are the reactions equal?
    '''
    return eq["reactants"] and eq["products"] and eq["coeffs"]

  def _changedreaction(self,eq):
    '''
    Has the reaction changed?
    '''
    return (eq["reactants"] and eq["products"]) and (eq["coeffs"]==False)

  def load_reactions(self,filename="Reactions.in",fmt=None):
    '''
    Reads a reaction network in the format of the ProDiMo Reactions.in

    Fills in the `reactions` field in this class.

    .. todo::

      Include reading of T-dependent rates for the csv format.
      More sophisticated guessing of the file format.

    Parameters
    ----------

    filename : str
      The name/path of the file to read.

    fmt : str
      Format of the file. Currently either `in` for old Reactions.in or `csv` for
      the UMIST csv format. If `None` the routine trys to guess the format (primitive at the moment).
    '''
    # guess the format old .in or csv format
    if fmt is None:
      csv=filename.strip().endswith(".csv")
    elif fmt=="csv":
      csv=True
    else:
      csv=False

    fr=open(filename)
    self.filename=filename

    lines=fr.readlines()

    if csv:
      for line in lines:

        if line.strip()=="": continue
        if line.strip().startswith("#"): continue

        fields=line.split(",")
        reac=Reaction()
        reac.id=int(fields[0])
        reac.idU=None
        reac.type=fields[1]
        reac.clem=fields[12].strip()
        reac.temps[:]=[float(fields[13].strip()),float(fields[14].strip())]
        reac.accuracy=fields[15].strip()
        reac.comment=fields[16].strip()

        # three reactants and four products
        for i,sp in enumerate(fields[2:9]):
          if sp=="": continue

          if i<3:
            reac.reactants.append(sp)
          else:
            reac.products.append(sp)

        reac.coeffs[:]=[float(x.replace("D","E")) for x in fields[9:12]]

        self.reactions.append(reac)

    else:
      for line in lines:

        if line.strip()=="": continue
        # do it similar to ProDiMo

        # print(line)
        idnum=line[0:5]
        specs=line[6:61]
        ABC=line[61:89].split()
        comm=line[89:]

        reac=Reaction()
        reac.id=int(idnum.strip())
        reac.idU=None
        reac.type=None
        reac.temps=None

  #       lensp=8
  #       for i in range(7):
  #         sp=specs[i*lensp:8+i*lensp].strip()
  #         if i<3 and sp!="":
  #           reac.reactants.append(sp)
  #         elif i>=3 and sp!="":
  #           reac.products.append(sp)

        # very tricky, each species should take 8 characters, but the reading routine of PRoDiMo works
        # also if one is only 7 charachters (don't know how), but it seems end the end the species can have
        # mac 6 characters.
        lensp=8
        idxnextsp=0
        for i in range(7):
          sp=specs[idxnextsp:(idxnextsp+lensp)].strip()
          # if (sp.strip()=="1"): return
          # print(i,sp,idxnextsp,specs[idxnextsp:(idxnextsp+lensp)],"+",specs[idxnextsp+lensp],"+")
          if i<3 and sp!="":
            reac.reactants.append(sp)
          elif i>=3 and sp!="":
            reac.products.append(sp)
          if i==6:  # last species
            idxnextsp+=(lensp-1)
          else:
            idxnextsp+=lensp
          # if (idxnextsp+lensp)<61 and specs[idxnextsp+lensp]!=" ": idxnextsp-=1

        reac.coeffs[:]=[float(x.replace("D","E")) for x in ABC]
        reac.comment=comm.strip()
        self.reactions.append(reac)

    fr.close()
    print("Loaded ",len(self.reactions)," Reactions from ",self.filename)

  def write_reactions(self,filename="Reactions.in.new",fmt=None):
    '''
    Writes the network to a file. The default format is the one from
    ProDiMo Reactions.in.

    .. todo::

      does not work yet for reactions with multiple temperatures.

    .. warning::
      Not well tested ... so be carefull.

    Parameters
    ----------

    filename : str
      The name/path of the file to read

    fmt : str
      If `None` format is the one from ProDiMo. if `csv` it is written in a
      csv mode.
    '''
    fw=open(filename,"w+")
    spfmt="{:8s}"
    if fmt=="csv":
      for reac in self.reactions:
        fw.write("{:5d}".format(reac.id).strip())

        fw.write(",")
        fw.write(reac.type.strip())

        fw.write(",")
        for i in range(3):
          if i<len(reac.reactants):
            fw.write(reac.reactants[i].strip())
          else:
            fw.write("")
          fw.write(",")

        for i in range(4):
          if i<len(reac.products):
            fw.write(reac.products[i].strip())
          else:
            fw.write("")
          fw.write(",")

        # assume that it is always positiv
        fw.write("{:8.2E}".format(reac.coeffs[0]).strip())
        fw.write(",")
        # can also be negative
        fw.write("{:+8.5F}".format(reac.coeffs[1]).strip())
        fw.write(",")
        # assume that it is always positiv
        fw.write("{:12.4f}".format(reac.coeffs[2]).strip())

        fw.write(",")
        fw.write(reac.clem.strip())

        for i in range(2):
          fw.write(",")
          fw.write("{:6.0f}".format(reac.temps[i]).strip())

        fw.write(",")
        fw.write(reac.accuracy.strip())

        fw.write(",")
        fw.write(reac.comment.strip())

        fw.write("\n")

    else:
      # abcformat="{:+8.2E}"
      for reac in self.reactions:
        fw.write("{:5d}".format(reac.id))
        fw.write(" ")
        # Three reactants
        for i in range(3):
          if i<len(reac.reactants):
            fw.write(spfmt.format(reac.reactants[i]))
          else:
            fw.write(spfmt.format(" "))

        for i in range(4):
          if i<len(reac.products):
            fw.write(spfmt.format(reac.products[i]))
          else:
            fw.write(spfmt.format(" "))
        # fw.write(" ")

        # assume that it is always positiv
        fw.write("{:8.2E}".format(reac.coeffs[0]))
        fw.write(" ")
        # can also be negative
        fw.write("{:+5.2F}".format(reac.coeffs[1]))
        fw.write(" ")
        # assume that it is always positiv
        fw.write("{:12.4f}".format(reac.coeffs[2]))

        fw.write("    ")
        fw.write(reac.comment)

        fw.write("\n")

      fw.close()

  def load_rates(self,filename=None):
    print("Not usefull for Reactions.in")
