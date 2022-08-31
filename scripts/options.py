#file containing options for all other scripts

atlasstyle_dir = "/global/homes/j/jmw464/ATLAS/Vertex-GNN/scripts/include/" #directory where ATLAS style macros are located
indir = "/global/cfs/cdirs/atlas/jmw464/qual_data/" #directory containing input files - must contain "Nominal", "Overall", "IBL" and "PP0" subdirectories
outdir = "/global/homes/j/jmw464/ATLAS/Qual-Task/output/" #directory for output files
dataset = "ttbar" #choose between ttbar and zp - relevant for binning (ttbar bins are cut off for high pT) and display purposes, other options will crash the script
jet_flavors = "l" #include only jets of a certain flavor -> choose between b, c, l or all - any other option is equivalent to all

fc_dl1 = 0.018 #f_c value for DL1
fc_dl1r = 0.018 #f_c value for DL1r