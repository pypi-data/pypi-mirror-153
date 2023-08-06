"""
Default script for the plotting the results of a single ProDiMo model. 

A script called `pplot`, which can directly by called from the command line, 
will be installed automatically during the installation process.  
"""
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

# the above two statement are for phyton2 pyhton3 compatibility.
# With this statmens you can write python3 code and it should also work
# in python2 (depends on your code) 

# this is for the argument parser included in python
import argparse

# this is for the PDF output
from matplotlib.backends.backend_pdf import PdfPages

# Thats the prodimpy modules 
# The first one is for reading a ProDiMo Model 
# The second one is for plotting
import prodimopy.read as pread
import prodimopy.plot as pplot
import prodimopy.utils as putils
import numpy

# The main routine is require to have an entry point. 
# It is not necessary if you want to write your own script.
def main(args=None):
  ###############################################################################
  # Command line parsing
  # this is optional you do not have to do it this way. 
  # You can use the prodimopy module in any way you want
  parser = argparse.ArgumentParser(description='prodimopy simple example for plotting ')
  parser.add_argument('-dir', required=False, default=".", help='The directory of the input files DEFAULT: "."')
  parser.add_argument('-output', required=False, default="./out.pdf", help='The output filename, DEFAULT: "./out.pdf"')
  parser.add_argument('-td_fileIdx', required=False, default=None, help='The index for the time dependent output file e.g. "01", DEFAULT: None')
  parser.add_argument('-mplstyle', required=False, default="prodimopy", help='Use a mpl style file, DEFAULT: prodimopy')
  args = parser.parse_args()
  
  print("-dir: ", args.dir)
  print("-output: ", args.output)
  print("-td_fileIdx: ", args.td_fileIdx)
  
  # thats for time dependent models, also optional
  outfile=args.output
  if args.td_fileIdx != None:
    outfile=outfile.replace(".pdf","_"+args.td_fileIdx+".pdf")
  
  # This reads the output of a ProDiMo model
  # there are more optional arguments 
  model = pread.read_prodimo(args.dir,td_fileIdx=args.td_fileIdx)
  
  # loads the prodimopy style
  putils.load_mplstyle(args.mplstyle)
  
  # Here the plotting happens. This produces one pdf file
  with PdfPages(outfile) as pdf:
    # Init the prodimo plotting module for one model and an optional title
    # it is required to pass a PdfPages object  
    pp=pplot.Plot(pdf,title=model.name)
    
    zr=True
    xlog=True
    ylog=False

    pp.plot_grid(model)
    # This plots the Stellar spectrum  
    pp.plot_starspec(model)  
    pp.plot_dust_opac(model)
    
    
    #pp.plot_NH(model,sdscale=True,ylim=[5.e27,5.e29])
    pp.plot_NH(model,sdscale=True,ylim=[1.e20,None],xlog=True)


    # here the default contour plots are used not very fancy currently. 
    # you can use latex for the labels!
    # note most of the parameters are optional

    contAV=pplot.Contour(model.AV,[1.0],showlabels=True,label_fmt=r" $A_V$=%.0f ",colors=pp.pcolors["red"])
    pp.plot_cont(model, model.nHtot, r"$\mathrm{n_{<H>} [cm^{-3}]}$",oconts=[contAV],zlim=[1.e4,None],extend="min",
                 zr=zr,xlog=xlog,ylog=ylog)  
    
    pp.plot_cont(model, model.rhod, r"$\mathsf{\rho_{dust} [g\;cm^{-3}]}$",
                zlim=[1.e-25,None],extend="both",
                zr=zr,xlog=xlog,ylog=ylog)



    levels=[10,20,50,100,300,1000]
    pp.plot_cont(model, model.td, r"$\mathrm{T_{dust} [K]}$",
                   zlim=[10,3500],extend="both",clevels=levels,clabels=map(str,levels),
                   zr=zr,xlog=xlog,ylog=ylog)

    levels=[10,20,50,100,300,1000,3000]   
    pp.plot_cont(model, model.tg, r"$\mathrm{T_{gas} [K]}$",
                   zlim=[10,3500],extend="both",clevels=levels,clabels=map(str,levels),
                   zr=zr,xlog=xlog,ylog=ylog)

    pp.plot_cont(model, model.chiRT, r"log $\mathrm{\chi\,[Draine\,field]}$",contour=True,
                    zlim=[1.e-6,1.e6],extend="both",cb_format="%.0f",
                    zr=zr,xlog=xlog,ylog=ylog)

    if numpy.max(model.zetaX)>1.e-99:
      pp.plot_cont(model, model.zetaX, r"$\mathrm{\zeta_{X}\,per\,H\,[s^{-1}]}$",contour=True,
                   zlim=[1.e-19,1.e-13],extend="both",
                   zr=zr,xlog=xlog,ylog=ylog)


    pp.plot_heat_cool(model)
    pp.plot_cont(model,model.taucool,r"log $\tau_\mathrm{cool}\,[yr]$",zlim=[1.e-2,None],extend="min",
                 zr=zr,xlog=xlog,ylog=ylog)
    
    
    
    pp.plot_cont(model,model.tauchem,r"log $\tau_\mathrm{chem}\,[yr]$",zlim=[1.e-2,1.e7],extend="both",
                 zr=zr,xlog=xlog,ylog=ylog)
    
    for spname in model.spnames:
      maxabun=numpy.max(model.getAbun(spname))
      zlim=[maxabun/1.e6,maxabun]
      pp.plot_abuncont(model, spname,zlim=zlim ,extend="both",rasterized=True,
                       zr=True,xlog=True,ylog=False,nbins=40)

    # observables if available
    if model.sed is not None: 
      pp.plot_sed(model,sedObs=model.sedObs)
      # model.rhod, r"$\mathsf{\rho_{dust} [g\;cm^{-3}]}$
      pp.plot_sedAna(model,zr=True,xlog=True,ylog=False)
    
    # line fluxes stuff 
    if model.lines is not None:  
      lineidents=[[line.ident,line.wl] for line in model.lines]            
      pp.plot_lines(model,lineidents,showBoxes=False,lineObs=model.lineObs,useLineEstimate=False)
      
      for line in model.lines:
        pp.plot_lineprofile(model,line.wl, line.ident,lineObs=model.lineObs)

      for line in model.lines:
        if line.species in model.spnames:
          nspmol=model.nmol[:,:,model.spnames[line.species]] 
          label=line.species
        else:
          nspmol=model.nmol[:,:,model.spnames["H2"]]
          label="H2"
        max=numpy.max(nspmol)
        zlim=[max/1.e11,max/1000] 
        pp.plot_line_origin(model,[[line.ident,line.wl]],nspmol,
                        label=r"log $n_{"+pplot.spnToLatex(label)+"}\,[cm^{-3}]$",
                        zlim=zlim,extend="both",showContOrigin=True)


       
    # Plot radiation field at certain wavelengths (here simply done with the index)
    # pp.plot_cont(model,model.radFields[:,:,0],zr=False,xlog=False,label="lam="+str(model.lams[0]))
    # pp.plot_cont(model,model.radFields[:,:,5],zr=False,xlog=False,label="lam="+str(model.lams[5]))     
  