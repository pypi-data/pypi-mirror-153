"""
Default script for plotting the results of several ProDiMo models. 

A script called `pplot_models`, which can directly by called from the command line, 
will be installed automatically during the installation process.  
"""
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import argparse

from matplotlib.backends.backend_pdf import PdfPages

import prodimopy.read as pread
import prodimopy.plot_models as ppms
import prodimopy.utils as putils

# The main routine is require to have an entry point. 
# It is not necessary if you want to write your own script.
def main(args=None):
  ###############################################################################
  # Command line parsing
  parser = argparse.ArgumentParser(description='Plotting and comparing several ProDiMo models.')
  parser.add_argument('dirs', help='The directories of the different models (separated by ",")')
  parser.add_argument('-names', required=False, default=None, help='The names of the models (separated by ",") , DEFAULT: "dir names"')
  parser.add_argument('-tdIdxs', required=False, default=None, help='The file index (postfix) in case of time-dependent models , DEFAULT: None')
  parser.add_argument('-species', required=False, default="CO,H2O,CN,HCN,HCO+,HN2+", help='Which species should be plotted, DEFAULT: "CO,H2O,CN,HCN,HCO+,HN2+"')
  parser.add_argument('-output', required=False, default="out_models.pdf", help='The output filename, DEFAULT: "./out_models.pdf"')
  parser.add_argument('-styles', required=False, default=None, help='The line styles for plotting of each model (separated by ",")')
  parser.add_argument('-colors', required=False, default=None, help='The colors for plotting of each model (separated by ",")')
  parser.add_argument('-markers', required=False, default=None, help='The markers for plotting of each model (separated by ",")')
  parser.add_argument('-mplstyle', required=False, default="prodimopy", help='Use a mpl style file, DEFAULT: prodimopy')
  #parser.add_argument('-readLineEstimates', required=False, default="False", help='Read FlineEstimates.out set to False if disable it. DEFAULT: True')
  args = parser.parse_args()
  
  print("Parameters: ")
  print("dirs: ", args.dirs)
  print("-names: ", args.names)
  print("-tdIdxs: ", args.tdIdxs)
  print("-species: ", args.species)
  print("-output: ", args.output)
  print("-styles: ", args.styles)
  print("-colors: ", args.colors)
  print("-markers: ", args.markers)
  #print("-readLineEstimates: ", args.readLineEstimates)
  print(" ")
  
  
  dirs = args.dirs.split(",")
  
  names=dirs
  if args.names != None:
    names = args.names.split(",")
    
  tdIdxs=None  
  if args.tdIdxs != None:
    tdIdxs=args.tdIdxs.split(",")
    for i in range(len(tdIdxs)):
      if tdIdxs[i]=="None": tdIdxs[i]=None   
  
  #readLineEstimates=args.readLineEstimates=="True"
  readLineEstimates=False
  
  species=None
  if args.species is not None or args.species != "":
    species=args.species.split(",")
    species=map(str,species)
  
  models = list()
  for i in range(len(dirs)):
    if tdIdxs != None:
      models.append(pread.read_prodimo(dirs[i], name=names[i],td_fileIdx=tdIdxs[i],readlineEstimates=readLineEstimates))
    else:
      models.append(pread.read_prodimo(dirs[i], name=names[i],readlineEstimates=readLineEstimates))
     
  styles=None
  if args.styles != None: styles = args.styles.strip().split(",") 
  colors=None
  if args.colors != None: colors=args.colors.strip().split(",")
  markers=None 
  if args.markers != None: markers=args.markers.strip().split(",")  
  
  # loads the prodimopy style
  putils.load_mplstyle(args.mplstyle)
  
  # do the plotting
  with PdfPages(args.output) as pdf:  
    pms=ppms.PlotModels(pdf,colors=colors,styles=styles,markers=markers,ncol_legend=4)
  
    pms.plot_NH(models,ylim=[3.e19,None],xlog=True)    
    pms.plot_starspec(models,ylim=[1.e3,None])
    pms.plot_dust_opac(models)
    
    
    if not all(x.sed is None for x in models): 
      pms.plot_sed(models,ylim=[1.e-17,None],plot_starSpec=False,sedObs=models[0].sedObs)

    #pms.plot_midplane(models, "nHtot", r"$\mathrm{midplane\,n_{<H>}\,[cm^{-3}}]$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "nd", r"$\mathrm{midplane\,n_{dust}\,[cm^{-3}}]$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "rhog", r"$\mathrm{midplane\,\rho_{gas}\,[g cm^{-3}}]$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "rhod", r"$\mathrm{midplane\,\rho_{dust}\,[g cm^{-3}}]$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "sdg", r"$\mathrm{\Sigma_{gas}\,[g cm^{-2}}]$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "sdd", r"$\mathrm{\Sigma_{dust}\,[g cm^{-2}}]$",xlog=True,ylog=True)
    pms.plot_midplane(models, "tg", r"$\mathrm{midplane\,T_{gas}\,[K]}$",xlog=True,ylog=True)
    pms.plot_midplane(models, "td", r"$\mathrm{midplane\,T_{dust}\,[K]}$",xlog=True,ylog=True)
    #pms.plot_midplane(models, "chi", r"$\mathrm{midplane\,\chi\,[Draine]}$",xlog=True,ylog=True)
  # 
    #for r in [1,100]:
    #  pms.plot_vertical(models, r, "chi", r"$\mathrm{\chi}\,[Draine]}$",ylim=[1.e-5,None],xlim=[None,0.5])
    #  pms.plot_vertical(models, r, "td", r"$\mathrm{T_{dust}\,[K]}$",xlim=[None,0.5])
    #  pms.plot_vertical(models, r, "tg", r"$\mathrm{T_{gas}\,[K]}$",xlim=[None,0.5])
            

    if species is not None:
      for spec in species:
        pms.plot_tcdspec(models, spec,xlog=True)
#        pms.plot_avgabun(models,spec,xlog=True)
          
# make single plots for each model
#    pp=ppm.Plot(pdf)
#    for model in models:
#      COabun=model.nmol[:,:,model.spnames["CO"]]/model.nHtot[:,:]
#      pp.plot_cont(model, COabun, r"$\mathrm{\epsilon (CO)}$",rasterized=True,zlim=[1.e-4,1.e-9],
#                   extend="both",title=model.name)
        
    for r in [0.1,1.0,10,100]:
      pms.plot_vertical(models, r, "tg", r"$\mathrm{T_{gas}\,[K]}$")
      pms.plot_vertical(models, r, "td", r"$\mathrm{T_{dust}\,[K]}$")      
    
    if not all(x.lines is None for x in models):
      # find the first one that actually has lines
      for mod in models:
        if mod.lines is not None and len(mod.lines)>0:
          lines=[[line.species,line.wl] for line in mod.lines]
          nlines=len(lines)
          if nlines>30:
            pms.plot_lines(models,lines[0:int(nlines/2)],useLineEstimate=False,lineObs=mod.lineObs)          
            pms.plot_lines(models,lines[int(nlines/2)+1:],useLineEstimate=False,lineObs=mod.lineObs)          
          else:  
            pms.plot_lines(models,lines,useLineEstimate=False,lineObs=mod.lineObs)

          break

        
    
