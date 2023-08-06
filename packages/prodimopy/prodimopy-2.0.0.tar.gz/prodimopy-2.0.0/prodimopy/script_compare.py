'''
  Simple script to compare to ProDiMo (standard) models.
  Uses the doAll() method of the compare module.

  This script only provides text output.
  To call it, simply type:
    pcompare modeldir1 modeldir2

  Type pcompare --help for help.
'''
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os

import prodimopy.compare as pcomp
import prodimopy.read as pread
import prodimopy.read_mc as pread_mc


# The main routine is require to have an entry point.
# It is not necessary if you want to write your own script.
def main(args=None):
  parser=argparse.ArgumentParser(description='Compares two ProDiMo models')
  parser.add_argument('model1',help='The directory/path of the first model used for the comparison.')
  parser.add_argument('model2',help='The directory/path of the second/reference model used for comparison.')
  parser.add_argument('-tdIdx1',required=False,default=None,help='The index for the time dependent resulst for model1 (e.g. 02). Default: None')
  parser.add_argument('-tdIdx2',required=False,default=None,help='The index for the time dependent results for model2 (e.g. 02). Default: None')
  args=parser.parse_args()

  print("Compare model "+args.model1+" to "+args.model2)

  # quick and dirty, but this way it works also for automatic tests.
  if pcomp.eval_model_type(args.model1)=="mc":
    if os.path.isfile(args.model1+"/"+"mc_output.txt"):
      print("\nRead model "+args.model1+"...")
      model1=pread_mc.read_mc("mc_output.txt",directory=args.model1)
      print("\nRead model "+args.model2+"...")
      model2=pread_mc.read_mc("mc_output.txt",directory=args.model2)
    elif os.path.isfile(args.model1+"/"+"MC_Results.out"):
      print("\nRead model "+args.model1+"...")
      model1=pread_mc.read_mc("MC_Results.out",directory=args.model1)
      print("\nRead model "+args.model2+"...")
      model2=pread_mc.read_mc("MC_Results.out",directory=args.model2)
    else:
      print("ERROR: Could not find MC outputfile.")
      return

    compare=pcomp.CompareMc(model1,model2)
  else:
    print("\nRead model "+args.model1+"...")
    model1=pread.read_prodimo(args.model1,readlineEstimates=True,td_fileIdx=args.tdIdx1)
    print("\nRead model "+args.model2+"...")
    model2=pread.read_prodimo(args.model2,readlineEstimates=True,td_fileIdx=args.tdIdx1)
    compare=pcomp.Compare(model1,model2)

  compare.doAll()
