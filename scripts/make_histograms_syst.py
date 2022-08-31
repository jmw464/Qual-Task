#!/usr/bin/env python

import os,sys,math,glob,ROOT
import numpy as np
from ROOT import gROOT, TFile, TH1D, TLorentzVector, TCanvas, TTree, gDirectory, TChain, TH2D

from plot_functions import *
import options

#set ATLAS style for plots
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasStyle.C")
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasLabels.C")
from ROOT import SetAtlasStyle


def calc_LLR(num, denom):
    if num <= 0.:
        return -30.
    elif denom <= 0.:
        return 100.
    else:
        return np.log(num/denom)


def main(argv):
    gROOT.SetBatch(True)
    SetAtlasStyle()

    indir = options.indir
    outdir = options.outdir
    jet_flavors = options.jet_flavors
    files = options.dataset

    treename = "bTag_AntiKt4EMPFlowJets_BTagging201903"

    if files == "ttbar":
        dataset_string = "t#bar{t}"
    elif files == "zp":
        dataset_string = "Z'"

    nomfiles = glob.glob(indir+"Nominal/"+'*')
    ovfiles = glob.glob(indir+"Overall/"+'*')
    iblfiles = glob.glob(indir+"IBL/"+'*')
    pp0files = glob.glob(indir+"PP0/"+'*')
    ipbiasdir = glob.glob(indir+"IPSmear/"+'*')
    ipbiasdir = glob.glob(indir+"IPBias/"+'*')
    qpbiasdir = glob.glob(indir+"QPBias/"+'*')

    nomchain = TChain(treename)
    ovchain = TChain(treename)
    iblchain = TChain(treename)
    pp0chain = TChain(treename)
    ipbiaschain = TChain(treename)
    ipsmearchain = TChain(treename)
    qpbiaschain = TChain(treename)

    chain_list_loop = [ovchain, iblchain, pp0chain, nomchain]
    chain_list = [ovchain, iblchain, pp0chain, nomchain, ipbiaschain, ipsmearchain, qpbiaschain]
    infile_lists = [ovfiles, iblfiles, pp0files, nomfiles, ipbiasfiles, ipsmearfiles, qpbiasfiles]
    for i,chain in enumerate(chain_list):
        infile_list = infile_lists[i]
        for ifile in infile_list:
            chain.AddFile(ifile)

    five_bins = np.linspace(-0.5,5.5,7)
    ten_bins = np.linspace(-0.5,10.5,12)
    fifteen_bins = np.linspace(-0.5,15.5,17)
    twenty_bins = np.linspace(-0.5,20.5,22)
    twentyfive_bins = np.linspace(-0.5,25.5,27)

    nom_qoverp_hist = TH1D("nom_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    ov_qoverp_hist = TH1D("ov_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    ibl_qoverp_hist = TH1D("ibl_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    pp0_qoverp_hist = TH1D("pp0_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    cprecbias_qoverp_hist = TH1D("cpbias_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    qoverp_histlist = [ov_qoverp_hist, ibl_qoverp_hist, pp0_qoverp_hist, nom_qoverp_hist, cprecbias_qoverp_hist]

    nom_d0_hist = TH1D("nom_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    ov_d0_hist = TH1D("ov_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    ibl_d0_hist = TH1D("ibl_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    pp0_d0_hist = TH1D("pp0_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    cprecbias_d0_hist = TH1D("cpbias_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    cprecsmear_d0_hist = TH1D("cpsmear_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    d0_histlist = [ov_d0_hist, ibl_d0_hist, pp0_d0_hist, nom_d0_hist, cprecbias_d0_hist, cprecsmear_d0_hist]

    nom_z0_hist = TH1D("nom_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    ov_z0_hist = TH1D("ov_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    ibl_z0_hist = TH1D("ibl_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    pp0_z0_hist = TH1D("pp0_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    cprecbias_z0_hist = TH1D("cpbias_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    cprecsmear_z0_hist = TH1D("cpsmear_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    z0_histlist = [ov_z0_hist, ibl_z0_hist, pp0_z0_hist, nom_z0_hist, cprecbias_z0_hist, cprecsmear_z0_hist]

    if jet_flavors == 'b':
        flavorcut = "&&jet_LabDr_HadF==5"
    elif jet_flavors == 'c':
        flavorcut = "&&jet_LabDr_HadF==4"
    elif jet_flavors == 'l':
        flavorcut = "&&jet_LabDr_HadF!=4&&jet_LabDr_HadF!=5"
    else:
        flavorcut = ""
    cut = "jet_pt>20e3&&fabs(jet_eta)<2.5"+flavorcut

    qpbiaschain.Draw("jet_trk_qoverp_sys/0.001>>cpbias_qoverp",cut,"goff")
    ipbiaschain.Draw("jet_trk_d0_sys>>cpbias_d0",cut,"goff")
    ipbiaschain.Draw("jet_trk_z0_sys>>cpbias_z0",cut,"goff")
    ipsmearchain.Draw("jet_trk_d0_sys>>cpsmear_d0",cut,"goff")
    ipsmearchain.Draw("jet_trk_z0_sys>>cpsmear_z0",cut,"goff")

    for i, chain in enumerate(chain_list_loop):
        if i == 0:
            prefix = "ov"
            print("PROCESSING +5% OVERALL SAMPLE")
        elif i == 1:
            prefix = "ibl"
            print("PROCESSING +10% IBL SAMPLE")
        elif i == 2:
            prefix = "pp0"
            print("PROCESSING +25% PP0 SAMPLE")
        else:
            prefix = "nom"
            print("PROCESSING NOMINAL SAMPLE")

        chain.Draw("jet_trk_qoverp/0.001>>"+prefix+"_qoverp",cut,"goff")
        chain.Draw("jet_trk_d0>>"+prefix+"_d0",cut,"goff")
        chain.Draw("jet_trk_z0>>"+prefix+"_z0",cut,"goff")
        
    canv1 = TCanvas("c1", "c1",200,10,900,900)

    plot_hist(canv1, qoverp_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing'], 3, dataset_string, False, True, outdir+'hist_qoverp_syst.pdf')
    plot_hist(canv1, d0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing', 'smearing'], 3, dataset_string, False, True, outdir+'hist_d0_syst.pdf')
    plot_hist(canv1, z0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing', 'smearing'], 3, dataset_string, False, True, outdir+'hist_z0_syst.pdf')


if __name__ == '__main__':
    main(sys.argv)
