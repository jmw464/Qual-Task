#!/usr/bin/env python

import os,sys,math,glob,ROOT
import numpy as np
import h5py
import argparse
import matplotlib.pyplot as plt
from ROOT import gROOT, TFile, TH1D, TLorentzVector, TCanvas, TTree, gDirectory, TChain, TH2D, gPad

from plot_functions import *
import options

#set ATLAS style for plots
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasStyle.C")
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasLabels.C")
from ROOT import SetAtlasStyle


def main(argv):
    gROOT.SetBatch(True)
    SetAtlasStyle()

    indir = options.indir
    outdir = options.outdir
    fc_dl1 = options.fc_dl1
    fc_dl1r = options.fc_dl1r
    jet_flavors = options.jet_flavors
    files = options.dataset

    treename = "bTag_AntiKt4EMPFlowJets_BTagging201903"

    #minor script options - can be modified
    dl1_bound = [-5,4]
    nbins = 20
    W_list = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25]
    maxfiles = -1

    #parse command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-d", "--dataset", type=str, required=True, dest="dataset", help="ttbar or zp")
    args = parser.parse_args()

    if files == "ttbar":
        dataset_string = "t#bar{t}"
    elif files == "zp":
        dataset_string = "Z'"

    nomfiles = glob.glob(indir+"Nominal/"+'*')[:maxfiles]
    ovfiles = glob.glob(indir+"Overall/"+'*')[:maxfiles]
    iblfiles = glob.glob(indir+"IBL/"+'*')[:maxfiles]
    pp0files = glob.glob(indir+"PP0/"+'*')[:maxfiles]

    if jet_flavors == "l":
        flavor_cut = "&&jet_LabDr_HadF!=4&&jet_LabDr_HadF!=5"
        appendix = "_l"
    elif jet_flavors == "b":
        flavor_cut = "&&jet_LabDr_HadF==5"
        appendix = "_b"
    elif jet_flavors == "c":
        flavor_cut = "&&jet_LabDr_HadF==4"
        appendix = "_c"
    else:
        flavor_cut = ""
        appendix = ""

    nomchain = TChain(treename)
    ovchain = TChain(treename)
    iblchain = TChain(treename)
    pp0chain = TChain(treename)

    chain_list = [ovchain, iblchain, pp0chain, nomchain]
    infile_lists = [ovfiles, iblfiles, pp0files, nomfiles]
    for i,chain in enumerate(chain_list):
        infile_list = infile_lists[i]
        for ifile in infile_list:
            chain.AddFile(ifile)

    print(nomchain.GetEntries(), ovchain.GetEntries())

    ov_chi2 = []
    ibl_chi2 = []
    pp0_chi2 = []

    canv = TCanvas("c1", "c1",200,10,900,900)

    for W in W_list:
        print("Working on W = "+str(W))
        general_cut = "(jet_pt>20e3)&&(fabs(jet_eta)<2.5)"+flavor_cut
        jet_weight_dl1 = "pow("+str(W)+",Sum$(jet_trk_barcode>200000))"
        jet_weight_dl1r = "pow("+str(W)+",Sum$(jet_trk_barcode>200000))"

        nom_dl1_hist = TH1D("nom_dl1_"+str(round(W*1000)), ";DL1 score;Count", nbins, dl1_bound[0], dl1_bound[1])
        ov_dl1_hist = TH1D("ov_dl1_"+str(round(W*1000)), ";DL1 score;Count", nbins, dl1_bound[0], dl1_bound[1])
        ibl_dl1_hist = TH1D("ibl_dl1_"+str(round(W*1000)), ";DL1 score;Count", nbins, dl1_bound[0], dl1_bound[1])
        pp0_dl1_hist = TH1D("pp0_dl1_"+str(round(W*1000)), ";DL1 score;Count", nbins, dl1_bound[0], dl1_bound[1])

        nom_nosec_hist = TH1D("nom_nosec_"+str(round(W*1000)), ";Number of secondary tracks;Count", nbins+1, 0, nbins)
        ov_nosec_hist = TH1D("ov_nosec_"+str(round(W*1000)), ";Number of secondary tracks;Count", nbins+1, 0, nbins)
        ibl_nosec_hist = TH1D("ibl_nosec_"+str(round(W*1000)), ";Number of secondary tracks;Count", nbins+1, 0, nbins)
        pp0_nosec_hist = TH1D("pp0_nosec_"+str(round(W*1000)), ";Number of secondary tracks;Count", nbins+1, 0, nbins)

        chain_list[3].Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>>nom_dl1_"+str(round(W*1000)),jet_weight_dl1+"*("+general_cut+")","goff")
        chain_list[0].Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>>ov_dl1_"+str(round(W*1000)),general_cut,"goff")
        chain_list[1].Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>>ibl_dl1_"+str(round(W*1000)),general_cut,"goff")
        chain_list[2].Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>>pp0_dl1_"+str(round(W*1000)),general_cut,"goff")

        chain_list[3].Draw("Sum$(jet_trk_barcode>200000)>>nom_nosec_"+str(round(W*1000)),jet_weight_dl1+"*("+general_cut+")","goff")
        chain_list[0].Draw("Sum$(jet_trk_barcode>200000)>>ov_nosec_"+str(round(W*1000)),general_cut,"goff")
        chain_list[1].Draw("Sum$(jet_trk_barcode>200000)>>ibl_nosec_"+str(round(W*1000)),general_cut,"goff")
        chain_list[2].Draw("Sum$(jet_trk_barcode>200000)>>pp0_nosec_"+str(round(W*1000)),general_cut,"goff")
        
        nom_dl1_hist.Scale(1/nom_dl1_hist.Integral("width"))
        ov_dl1_hist.Scale(1/ov_dl1_hist.Integral("width"))
        ibl_dl1_hist.Scale(1/ibl_dl1_hist.Integral("width"))
        pp0_dl1_hist.Scale(1/pp0_dl1_hist.Integral("width"))

        nom_nosec_hist.Scale(1/nom_nosec_hist.Integral("width"))
        ov_nosec_hist.Scale(1/ov_nosec_hist.Integral("width"))
        ibl_nosec_hist.Scale(1/ibl_nosec_hist.Integral("width"))
        pp0_nosec_hist.Scale(1/pp0_nosec_hist.Integral("width"))

        plot_hist(canv, [ov_dl1_hist, ibl_dl1_hist, pp0_dl1_hist, nom_dl1_hist], ["ov", "ibl", "pp0", "nom"], 3, dataset_string, False, False, outdir+"dl1_hist_"+str(round(W*1000))+appendix+".pdf")
        plot_hist(canv, [ov_nosec_hist, ibl_nosec_hist, pp0_nosec_hist, nom_nosec_hist], ["ov", "ibl", "pp0", "nom"], 3, dataset_string, False, False, outdir+"nosec_hist_"+str(round(W*1000))+appendix+".pdf")

        ov_chi2.append(ov_dl1_hist.Chi2Test(nom_dl1_hist, "WW"))
        ibl_chi2.append(ibl_dl1_hist.Chi2Test(nom_dl1_hist, "WW"))
        pp0_chi2.append(pp0_dl1_hist.Chi2Test(nom_dl1_hist, "WW"))

        nom_dl1_hist.Reset()
        gDirectory.GetList().Remove(nom_dl1_hist)
        del nom_dl1_hist
        ov_dl1_hist.Reset()
        gDirectory.GetList().Remove(ov_dl1_hist)
        del ov_dl1_hist
        ibl_dl1_hist.Reset()
        gDirectory.GetList().Remove(ibl_dl1_hist)
        del ibl_dl1_hist
        pp0_dl1_hist.Reset()
        gDirectory.GetList().Remove(pp0_dl1_hist)
        del pp0_dl1_hist

        nom_nosec_hist.Reset()
        gDirectory.GetList().Remove(nom_nosec_hist)
        del nom_nosec_hist
        ov_nosec_hist.Reset()
        gDirectory.GetList().Remove(ov_nosec_hist)
        del ov_nosec_hist
        ibl_nosec_hist.Reset()
        gDirectory.GetList().Remove(ibl_nosec_hist)
        del ibl_nosec_hist
        pp0_nosec_hist.Reset()
        gDirectory.GetList().Remove(pp0_nosec_hist)
        del pp0_nosec_hist
    
    plt.figure()
    plt.plot(W_list, ov_chi2, label="+5% overall")
    plt.plot(W_list, ibl_chi2, label="+10% IBL")
    plt.plot(W_list, pp0_chi2, label="+25% PP0")
    plt.xlabel("weight")
    plt.ylabel("p-value")
    plt.yscale("log")
    plt.legend()
    plt.savefig(outdir+"weights"+appendix+".pdf")


if __name__ == '__main__':
    main(sys.argv)
