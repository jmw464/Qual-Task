#!/usr/bin/env python

import os,sys,math,glob,ROOT
import numpy as np
from ROOT import gROOT, TFile, TH1D, TLorentzVector, TCanvas, TTree, gDirectory, TChain, TH2D

#set ATLAS style for plots
gROOT.LoadMacro("/global/homes/j/jmw464/ATLAS/Vertex-GNN/scripts/include/AtlasStyle.C")
gROOT.LoadMacro("/global/homes/j/jmw464/ATLAS/Vertex-GNN/scripts/include/AtlasLabels.C")
from ROOT import SetAtlasStyle

from plot_functions import *


jet_flavors = "incl" #select b, c or l if desired (anything else will run all jets)


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

    indir = "/global/cfs/cdirs/atlas/jmw464/qual_data/"
    outdir = "/global/homes/j/jmw464/ATLAS/Qual-Task/output/"
    treename = "bTag_AntiKt4EMPFlowJets_BTagging201903"
    files = "ttbar"

    if files == "ttbar":
        nomdir = "user.jmwagner.410470.qual_tt_nom_10_Akt4EMPf_BTagging201903/"
        ovdir = "user.jmwagner.410470.qual_tt_ov_3_Akt4EMPf_BTagging201903/"
        ibldir = "user.jmwagner.410470.qual_tt_ibl_4_Akt4EMPf_BTagging201903/"
        pp0dir = "user.jmwagner.410470.qual_tt_pp0_3_Akt4EMPf_BTagging201903/"
        ipbiasdir = "user.jmwagner.410470.qual_tt_nom_7_Akt4EMPf_BTagging201903/"
        ipsmeardir = "user.jmwagner.410470.qual_tt_nom_8_Akt4EMPf_BTagging201903/"
        qpbiasdir = "user.jmwagner.410470.qual_tt_nom_9_Akt4EMPf_BTagging201903/"
    elif files == "zp":
        nomdir = "user.jmwagner.800030.qual_zp_nom_10_Akt4EMPf_BTagging201903/"
        ovdir = "user.jmwagner.800030.qual_zp_ov_3_Akt4EMPf_BTagging201903/"
        ibldir = "user.jmwagner.800030.qual_zp_ibl_3_Akt4EMPf_BTagging201903/"
        pp0dir = "user.jmwagner.800030.qual_zp_pp0_3_Akt4EMPf_BTagging201903/"
        ipbiasdir = "user.jmwagner.800030.qual_zp_nom_6_Akt4EMPf_BTagging201903/"
        ipsmeardir = "user.jmwagner.800030.qual_zp_nom_7_Akt4EMPf_BTagging201903/"
        qpbiasdir = "user.jmwagner.800030.qual_zp_nom_8_Akt4EMPf_BTagging201903/"

    nomfiles = glob.glob(indir+nomdir+'*')
    ovfiles = glob.glob(indir+ovdir+'*')
    iblfiles = glob.glob(indir+ibldir+'*')
    pp0files = glob.glob(indir+pp0dir+'*')
    ipbiasfiles = glob.glob(indir+ipbiasdir+'*')
    ipsmearfiles = glob.glob(indir+ipsmeardir+'*')
    qpbiasfiles = glob.glob(indir+qpbiasdir+'*')

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

    plot_hist(canv1, qoverp_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing'], 3, False, True, outdir+'hist_qoverp.png')
    plot_hist(canv1, d0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing', 'smearing'], 3, False, True, outdir+'hist_d0.png')
    plot_hist(canv1, z0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal', 'biasing', 'smearing'], 3, False, True, outdir+'hist_z0.png')


if __name__ == '__main__':
    main(sys.argv)
