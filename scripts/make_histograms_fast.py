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

    five_bins = np.linspace(-0.5,5.5,7)
    ten_bins = np.linspace(-0.5,10.5,12)
    fifteen_bins = np.linspace(-0.5,15.5,17)
    twenty_bins = np.linspace(-0.5,20.5,22)
    twentyfive_bins = np.linspace(-0.5,25.5,27)

    nom_pt_hist = TH1D("nom_pt", ";track pT [GeV];Entries", 20, 0, 5)
    ov_pt_hist = TH1D("ov_pt", ";track pT [GeV];Entries", 20, 0, 5)
    ibl_pt_hist = TH1D("ibl_pt", ";track pT [GeV];Entries", 20, 0, 5)
    pp0_pt_hist = TH1D("pp0_pt", ";track pT [GeV];Entries", 20, 0, 5)
    pt_histlist = [ov_pt_hist, ibl_pt_hist, pp0_pt_hist, nom_pt_hist]

    nom_qoverp_hist = TH1D("nom_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    ov_qoverp_hist = TH1D("ov_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    ibl_qoverp_hist = TH1D("ibl_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    pp0_qoverp_hist = TH1D("pp0_qoverp", ";track q/p [1/GeV];Entries", 20, -1, 1)
    qoverp_histlist = [ov_qoverp_hist, ibl_qoverp_hist, pp0_qoverp_hist, nom_qoverp_hist]

    nom_d0s_hist = TH1D("nom_d0s", ";unsigned d0 significance;Entries", 20, -10, 10)
    ov_d0s_hist = TH1D("ov_d0s", ";unsigned d0 significance;Entries", 20, -10, 10)
    ibl_d0s_hist = TH1D("ibl_d0s", ";unsigned d0 significance;Entries", 20, -10, 10)
    pp0_d0s_hist = TH1D("pp0_d0s", ";unsigned d0 significance;Entries", 20, -10, 10)
    d0s_histlist = [ov_d0s_hist, ibl_d0s_hist, pp0_d0s_hist, nom_d0s_hist]

    nom_d0_hist = TH1D("nom_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    ov_d0_hist = TH1D("ov_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    ibl_d0_hist = TH1D("ibl_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    pp0_d0_hist = TH1D("pp0_d0", ";unsigned d0 [mm];Entries", 20, -0.5, 0.5)
    d0_histlist = [ov_d0_hist, ibl_d0_hist, pp0_d0_hist, nom_d0_hist]

    nom_d0sign_hist = TH1D("nom_d0sign", ";signed d0 [mm];Entries", 20, -0.5, 0.5)
    ov_d0sign_hist = TH1D("ov_d0sign", ";signed d0 [mm];Entries", 20, -0.5, 0.5)
    ibl_d0sign_hist = TH1D("ibl_d0sign", ";signed d0 [mm];Entries", 20, -0.5, 0.5)
    pp0_d0sign_hist = TH1D("pp0_d0sign", ";signed d0 [mm];Entries", 20, -0.5, 0.5) 
    d0sign_histlist = [ov_d0sign_hist, ibl_d0sign_hist, pp0_d0sign_hist, nom_d0sign_hist]

    nom_z0s_hist = TH1D("nom_z0s", ";unsigned z0 significance;Entries", 20, -10, 10)
    ov_z0s_hist = TH1D("ov_z0s", ";unsigned z0 significance;Entries", 20, -10, 10)
    ibl_z0s_hist = TH1D("ibl_z0s", ";unsigned z0 significance;Entries", 20, -10, 10)
    pp0_z0s_hist = TH1D("pp0_z0s", ";unsigned z0 significance;Entries", 20, -10, 10)
    z0s_histlist = [ov_z0s_hist, ibl_z0s_hist, pp0_z0s_hist, nom_z0s_hist]

    nom_z0_hist = TH1D("nom_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    ov_z0_hist = TH1D("ov_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    ibl_z0_hist = TH1D("ibl_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    pp0_z0_hist = TH1D("pp0_z0", ";unsigned z0 [mm];Entries", 20, -0.5, 0.5)
    z0_histlist = [ov_z0_hist, ibl_z0_hist, pp0_z0_hist, nom_z0_hist]

    nom_z0sign_hist = TH1D("nom_z0sign", ";signed z0 [mm];Entries", 20, -0.5, 0.5)
    ov_z0sign_hist = TH1D("ov_z0sign", ";signed z0 [mm];Entries", 20, -0.5, 0.5)
    ibl_z0sign_hist = TH1D("ibl_z0sign", ";signed z0 [mm];Entries", 20, -0.5, 0.5)
    pp0_z0sign_hist = TH1D("pp0_z0sign", ";signed z0 [mm];Entries", 20, -0.5, 0.5) 
    z0sign_histlist = [ov_z0sign_hist, ibl_z0sign_hist, pp0_z0sign_hist, nom_z0sign_hist]

    nom_nPixHits_hist = TH1D("nom_nPixHits", ";Number of pixel hits;Entries", 11, ten_bins)
    ov_nPixHits_hist = TH1D("ov_nPixHits", ";Number of pixel hits;Entries", 11, ten_bins)
    ibl_nPixHits_hist = TH1D("ibl_nPixHits", ";Number of pixel hits;Entries", 11, ten_bins)
    pp0_nPixHits_hist = TH1D("pp0_nPixHits", ";Number of pixel hits;Entries", 11, ten_bins)
    nPixHits_histlist = [ov_nPixHits_hist, ibl_nPixHits_hist, pp0_nPixHits_hist, nom_nPixHits_hist]

    nom_nSCTHits_hist = TH1D("nom_nSCTHits", ";Number of SCT hits;Entries", 16, fifteen_bins)
    ov_nSCTHits_hist = TH1D("ov_nSCTHits", ";Number of SCT hits;Entries", 16, fifteen_bins)
    ibl_nSCTHits_hist = TH1D("ibl_nSCTHits", ";Number of SCT hits;Entries", 16, fifteen_bins)
    pp0_nSCTHits_hist = TH1D("pp0_nSCTHits", ";Number of SCT hits;Entries", 16, fifteen_bins)
    nSCTHits_histlist = [ov_nSCTHits_hist, ibl_nSCTHits_hist, pp0_nSCTHits_hist, nom_nSCTHits_hist]

    nom_nBLHits_hist = TH1D("nom_nBLHits", ";Number of BL hits;Entries", 6, five_bins)
    ov_nBLHits_hist = TH1D("ov_nBLHits", ";Number of BL hits;Entries", 6, five_bins)
    ibl_nBLHits_hist = TH1D("ibl_nBLHits", ";Number of BL hits;Entries", 6, five_bins)
    pp0_nBLHits_hist = TH1D("pp0_nBLHits", ";Number of BL hits;Entries", 6, five_bins)
    nBLHits_histlist = [ov_nBLHits_hist, ibl_nBLHits_hist, pp0_nBLHits_hist, nom_nBLHits_hist]

    nom_nPixHoles_hist = TH1D("nom_nPixHoles", ";Number of pixel holes;Entries", 6, five_bins)
    ov_nPixHoles_hist = TH1D("ov_nPixHoles", ";Number of pixel holes;Entries", 6, five_bins)
    ibl_nPixHoles_hist = TH1D("ibl_nPixHoles", ";Number of pixel holes;Entries", 6, five_bins)
    pp0_nPixHoles_hist = TH1D("pp0_nPixHoles", ";Number of pixel holes;Entries", 6, five_bins)
    nPixHoles_histlist = [ov_nPixHoles_hist, ibl_nPixHoles_hist, pp0_nPixHoles_hist, nom_nPixHoles_hist]

    nom_nSCTHoles_hist = TH1D("nom_nSCTHoles", ";Number of SCT holes;Entries", 6, five_bins)
    ov_nSCTHoles_hist = TH1D("ov_nSCTHoles", ";Number of SCT holes;Entries", 6, five_bins)
    ibl_nSCTHoles_hist = TH1D("ibl_nSCTHoles", ";Number of SCT holes;Entries", 6, five_bins)
    pp0_nSCTHoles_hist = TH1D("pp0_nSCTHoles", ";Number of SCT holes;Entries", 6, five_bins)
    nSCTHoles_histlist = [ov_nSCTHoles_hist, ibl_nSCTHoles_hist, pp0_nSCTHoles_hist, nom_nSCTHoles_hist]

    nom_nPixShared_hist = TH1D("nom_nPixShared", ";Number of pixel shared;Entries", 6, five_bins)
    ov_nPixShared_hist = TH1D("ov_nPixShared", ";Number of pixel shared;Entries", 6, five_bins)
    ibl_nPixShared_hist = TH1D("ibl_nPixShared", ";Number of pixel shared;Entries", 6, five_bins)
    pp0_nPixShared_hist = TH1D("pp0_nPixShared", ";Number of pixel shared;Entries", 6, five_bins)
    nPixShared_histlist = [ov_nPixShared_hist, ibl_nPixShared_hist, pp0_nPixShared_hist, nom_nPixShared_hist]

    nom_nSCTShared_hist = TH1D("nom_nSCTShared", ";Number of SCT shared;Entries", 6, five_bins)
    ov_nSCTShared_hist = TH1D("ov_nSCTShared", ";Number of SCT shared;Entries", 6, five_bins)
    ibl_nSCTShared_hist = TH1D("ibl_nSCTShared", ";Number of SCT shared;Entries", 6, five_bins)
    pp0_nSCTShared_hist = TH1D("pp0_nSCTShared", ";Number of SCT shared;Entries", 6, five_bins)
    nSCTShared_histlist = [ov_nSCTShared_hist, ibl_nSCTShared_hist, pp0_nSCTShared_hist, nom_nSCTShared_hist]

    nom_nBLShared_hist = TH1D("nom_nBLShared", ";Number of BL shared;Entries", 6, five_bins)
    ov_nBLShared_hist = TH1D("ov_nBLShared", ";Number of BL shared;Entries", 6, five_bins)
    ibl_nBLShared_hist = TH1D("ibl_nBLShared", ";Number of BL shared;Entries", 6, five_bins)
    pp0_nBLShared_hist = TH1D("pp0_nBLShared", ";Number of BL shared;Entries", 6, five_bins)
    nBLShared_histlist = [ov_nBLShared_hist, ibl_nBLShared_hist, pp0_nBLShared_hist, nom_nBLShared_hist]

    nom_nPixSplit_hist = TH1D("nom_nPixSplit", ";Number of pixel split;Entries", 6, five_bins)
    ov_nPixSplit_hist = TH1D("ov_nPixSplit", ";Number of pixel split;Entries", 6, five_bins)
    ibl_nPixSplit_hist = TH1D("ibl_nPixSplit", ";Number of pixel split;Entries", 6, five_bins)
    pp0_nPixSplit_hist = TH1D("pp0_nPixSplit", ";Number of pixel split;Entries", 6, five_bins)
    nPixSplit_histlist = [ov_nPixSplit_hist, ibl_nPixSplit_hist, pp0_nPixSplit_hist, nom_nPixSplit_hist]

    nom_nBLSplit_hist = TH1D("nom_nBLSplit", ";Number of BL split;Entries", 6, five_bins)
    ov_nBLSplit_hist = TH1D("ov_nBLSplit", ";Number of BL split;Entries", 6, five_bins)
    ibl_nBLSplit_hist = TH1D("ibl_nBLSplit", ";Number of BL split;Entries", 6, five_bins)
    pp0_nBLSplit_hist = TH1D("pp0_nLBSplit", ";Number of BL split;Entries", 6, five_bins)
    nBLSplit_histlist = [ov_nBLSplit_hist, ibl_nBLSplit_hist, pp0_nBLSplit_hist, nom_nBLSplit_hist]

    nom_jetpt_hist = TH1D("nom_jetpt", ";jet pT [GeV];Entries", 20, 0, 150)
    ov_jetpt_hist = TH1D("ov_jetpt", ";jet pT [GeV];Entries", 20, 0, 150)
    ibl_jetpt_hist = TH1D("ibl_jetpt", ";jet pT [GeV];Entries", 20, 0, 150)
    pp0_jetpt_hist = TH1D("pp0_jetpt", ";jet pT [GeV];Entries", 20, 0, 150)
    jetpt_histlist = [ov_jetpt_hist, ibl_jetpt_hist, pp0_jetpt_hist, nom_jetpt_hist]

    nom_jeteta_hist = TH1D("nom_jeteta", ";jet eta;Entries", 20, -2.5, 2.5)
    ov_jeteta_hist = TH1D("ov_jeteta", ";jet eta;Entries", 20, -2.5, 2.5)
    ibl_jeteta_hist = TH1D("ibl_jeteta", ";jet eta;Entries", 20, -2.5, 2.5)
    pp0_jeteta_hist = TH1D("pp0_jeteta", ";jet eta;Entries", 20, -2.5, 2.5)
    jeteta_histlist = [ov_jeteta_hist, ibl_jeteta_hist, pp0_jeteta_hist, nom_jeteta_hist]

    nom_jetntrk_hist = TH1D("nom_jetntrk", ";Number of tracks per jet;Entries", 26, twentyfive_bins)
    ov_jetntrk_hist = TH1D("ov_jetntrk", ";Number of tracks per jet;Entries", 26, twentyfive_bins)
    ibl_jetntrk_hist = TH1D("ibl_jetntrk", ";Number of tracks per jet;Entries", 26, twentyfive_bins)
    pp0_jetntrk_hist = TH1D("pp0_jetntrk", ";Number of tracks per jet;Entries", 26, twentyfive_bins)
    jetntrk_histlist = [ov_jetntrk_hist, ibl_jetntrk_hist, pp0_jetntrk_hist, nom_jetntrk_hist]

    nom_evnjet_hist = TH1D("nom_evnjet", ";Number of jets per event;Entries", 21, twenty_bins)
    ov_evnjet_hist = TH1D("ov_evnjet", ";Number of jets per event;Entries", 21, twenty_bins)
    ibl_evnjet_hist = TH1D("ibl_evnjet", ";Number of jets per event;Entries", 21, twenty_bins)
    pp0_evnjet_hist = TH1D("pp0_evnjet", ";Number of jets per event;Entries", 21, twenty_bins)
    evnjet_histlist = [ov_evnjet_hist, ibl_evnjet_hist, pp0_evnjet_hist, nom_evnjet_hist]

    nom_ip3dLLbl_hist = TH1D("nom_ip3dLLbl", ";IP3D log(Pb/Pl);Entries", 20, -4, 2)
    ov_ip3dLLbl_hist = TH1D("ov_ip3dLLbl", ";IP3D log(Pb/Pl);Entries", 20, -4, 2)
    ibl_ip3dLLbl_hist = TH1D("ibl_ip3dLLbl", ";IP3D log(Pb/Pl);Entries", 20, -4, 2)
    pp0_ip3dLLbl_hist = TH1D("pp0_ip3dLLbl", ";IP3D log(Pb/Pl);Entries", 20, -4, 2)
    ip3dLLbl_histlist = [ov_ip3dLLbl_hist, ibl_ip3dLLbl_hist, pp0_ip3dLLbl_hist, nom_ip3dLLbl_hist]

    nom_ip3dLLbc_hist = TH1D("nom_ip3dLLbc", ";IP3D log(Pb/Pc);Entries", 20, -3, 2)
    ov_ip3dLLbc_hist = TH1D("ov_ip3dLLbc", ";IP3D log(Pb/Pc);Entries", 20, -3, 2)
    ibl_ip3dLLbc_hist = TH1D("ibl_ip3dLLbc", ";IP3D log(Pb/Pc);Entries", 20, -3, 2)
    pp0_ip3dLLbc_hist = TH1D("pp0_ip3dLLbc", ";IP3D log(Pb/Pc);Entries", 20, -3, 2)
    ip3dLLbc_histlist = [ov_ip3dLLbc_hist, ibl_ip3dLLbc_hist, pp0_ip3dLLbc_hist, nom_ip3dLLbc_hist]

    nom_ip3dLLcl_hist = TH1D("nom_ip3dLLcl", ";IP3D log(Pc/Pl);Entries", 20, -2, 3)
    ov_ip3dLLcl_hist = TH1D("ov_ip3dLLcl", ";IP3D log(Pc/Pl);Entries", 20, -2, 3)
    ibl_ip3dLLcl_hist = TH1D("ibl_ip3dLLcl", ";IP3D log(Pc/Pl);Entries", 20, -2, 3)
    pp0_ip3dLLcl_hist = TH1D("pp0_ip3dLLcl", ";IP3D log(Pc/Pl);Entries", 20, -2, 3)
    ip3dLLcl_histlist = [ov_ip3dLLcl_hist, ibl_ip3dLLcl_hist, pp0_ip3dLLcl_hist, nom_ip3dLLcl_hist]

    nom_rnnipLLbl_hist = TH1D("nom_rnnipLLbl", ";RNNIP log(Pb/Pl);Entries", 20, -4, 0)
    ov_rnnipLLbl_hist = TH1D("ov_rnnipLLbl", ";RNNIP log(Pb/Pl);Entries", 20, -4, 0)
    ibl_rnnipLLbl_hist = TH1D("ibl_rnnipLLbl", ";RNNIP log(Pb/Pl);Entries", 20, -4, 0)
    pp0_rnnipLLbl_hist = TH1D("pp0_rnnipLLbl", ";RNNIP log(Pb/Pl);Entries", 20, -4, 0)
    rnnipLLbl_histlist = [ov_rnnipLLbl_hist, ibl_rnnipLLbl_hist, pp0_rnnipLLbl_hist, nom_rnnipLLbl_hist]

    nom_rnnipLLbc_hist = TH1D("nom_rnnipLLbc", ";RNNIP log(Pb/Pc);Entries", 20, -2, 2)
    ov_rnnipLLbc_hist = TH1D("ov_rnnipLLbc", ";RNNIP log(Pb/Pc);Entries", 20, -2, 2)
    ibl_rnnipLLbc_hist = TH1D("ibl_rnnipLLbc", ";RNNIP log(Pb/Pc);Entries", 20, -2, 2)
    pp0_rnnipLLbc_hist = TH1D("pp0_rnnipLLbc", ";RNNIP log(Pb/Pc);Entries", 20, -2, 2)
    rnnipLLbc_histlist = [ov_rnnipLLbc_hist, ibl_rnnipLLbc_hist, pp0_rnnipLLbc_hist, nom_rnnipLLbc_hist]

    nom_rnnipLLcl_hist = TH1D("nom_rnnipLLcl", ";RNNIP log(Pc/Pl);Entries", 20, -3, 0)
    ov_rnnipLLcl_hist = TH1D("ov_rnnipLLcl", ";RNNIP log(Pc/Pl);Entries", 20, -3, 0)
    ibl_rnnipLLcl_hist = TH1D("ibl_rnnipLLcl", ";RNNIP log(Pc/Pl);Entries", 20, -3, 0)
    pp0_rnnipLLcl_hist = TH1D("pp0_rnnipLLcl", ";RNNIP log(Pc/Pl);Entries", 20, -3, 0)
    rnnipLLcl_histlist = [ov_rnnipLLcl_hist, ibl_rnnipLLcl_hist, pp0_rnnipLLcl_hist, nom_rnnipLLcl_hist]

    nom_dl1LLbl_hist = TH1D("nom_dl1LLbl", ";DL1 log(Pb/Pl);Entries", 20, -4, 1)
    ov_dl1LLbl_hist = TH1D("ov_dl1LLbl", ";DL1 log(Pb/Pl);Entries", 20, -4, 1)
    ibl_dl1LLbl_hist = TH1D("ibl_dl1LLbl", ";DL1 log(Pb/Pl);Entries", 20, -4, 1)
    pp0_dl1LLbl_hist = TH1D("pp0_dl1LLbl", ";DL1 log(Pb/Pl);Entries", 20, -4, 1)
    dl1LLbl_histlist = [ov_dl1LLbl_hist, ibl_dl1LLbl_hist, pp0_dl1LLbl_hist, nom_dl1LLbl_hist]

    nom_dl1LLbc_hist = TH1D("nom_dl1LLbc", ";DL1 log(Pb/Pc);Entries", 20, -3, 2)
    ov_dl1LLbc_hist = TH1D("ov_dl1LLbc", ";DL1 log(Pb/Pc);Entries", 20, -3, 2)
    ibl_dl1LLbc_hist = TH1D("ibl_dl1LLbc", ";DL1 log(Pb/Pc);Entries", 20, -3, 2)
    pp0_dl1LLbc_hist = TH1D("pp0_dl1LLbc", ";DL1 log(Pb/Pc);Entries", 20, -3, 2)
    dl1LLbc_histlist = [ov_dl1LLbc_hist, ibl_dl1LLbc_hist, pp0_dl1LLbc_hist, nom_dl1LLbc_hist]

    nom_dl1LLcl_hist = TH1D("nom_dl1LLcl", ";DL1 log(Pc/Pl);Entries", 20, -2, 2)
    ov_dl1LLcl_hist = TH1D("ov_dl1LLcl", ";DL1 log(Pc/Pl);Entries", 20, -2, 2)
    ibl_dl1LLcl_hist = TH1D("ibl_dl1LLcl", ";DL1 log(Pc/Pl);Entries", 20, -2, 2)
    pp0_dl1LLcl_hist = TH1D("pp0_dl1LLcl", ";DL1 log(Pc/Pl);Entries", 20, -2, 2)
    dl1LLcl_histlist = [ov_dl1LLcl_hist, ibl_dl1LLcl_hist, pp0_dl1LLcl_hist, nom_dl1LLcl_hist]

    nom_dl1rLLbl_hist = TH1D("nom_dl1rLLbl", ";DL1R log(Pb/Pl);Entries", 20, -4, 1)
    ov_dl1rLLbl_hist = TH1D("ov_dl1rLLbl", ";DL1R log(Pb/Pl);Entries", 20, -4, 1)
    ibl_dl1rLLbl_hist = TH1D("ibl_dl1rLLbl", ";DL1R log(Pb/Pl);Entries", 20, -4, 1)
    pp0_dl1rLLbl_hist = TH1D("pp0_dl1rLLbl", ";DL1R log(Pb/Pl);Entries", 20, -4, 1)
    dl1rLLbl_histlist = [ov_dl1rLLbl_hist, ibl_dl1rLLbl_hist, pp0_dl1rLLbl_hist, nom_dl1rLLbl_hist]

    nom_dl1rLLbc_hist = TH1D("nom_dl1rLLbc", ";DL1R log(Pb/Pc);Entries", 20, -3, 2)
    ov_dl1rLLbc_hist = TH1D("ov_dl1rLLbc", ";DL1R log(Pb/Pc);Entries", 20, -3, 2)
    ibl_dl1rLLbc_hist = TH1D("ibl_dl1rLLbc", ";DL1R log(Pb/Pc);Entries", 20, -3, 2)
    pp0_dl1rLLbc_hist = TH1D("pp0_dl1rLLbc", ";DL1R log(Pb/Pc);Entries", 20, -3, 2)
    dl1rLLbc_histlist = [ov_dl1rLLbc_hist, ibl_dl1rLLbc_hist, pp0_dl1rLLbc_hist, nom_dl1rLLbc_hist]

    nom_dl1rLLcl_hist = TH1D("nom_dl1rLLcl", ";DL1R log(Pc/Pl);Entries", 20, -3, 2)
    ov_dl1rLLcl_hist = TH1D("ov_dl1rLLcl", ";DL1R log(Pc/Pl);Entries", 20, -3, 2)
    ibl_dl1rLLcl_hist = TH1D("ibl_dl1rLLcl", ";DL1R log(Pc/Pl);Entries", 20, -3, 2)
    pp0_dl1rLLcl_hist = TH1D("pp0_dl1rLLcl", ";DL1R log(Pc/Pl);Entries", 20, -3, 2)
    dl1rLLcl_histlist = [ov_dl1rLLcl_hist, ibl_dl1rLLcl_hist, pp0_dl1rLLcl_hist, nom_dl1rLLcl_hist]

    nom_sv1m_hist = TH1D("nom_sv1m", ";SV mass (SV1);Entries", 20, 0, 5)
    ov_sv1m_hist = TH1D("ov_sv1m", ";SV mass (SV1);Entries", 20, 0, 5)
    ibl_sv1m_hist = TH1D("ibl_sv1m", ";SV mass (SV1);Entries", 20, 0, 5)
    pp0_sv1m_hist = TH1D("pp0_sv1m", ";SV mass (SV1);Entries", 20, 0, 5)
    sv1m_histlist = [ov_sv1m_hist, ibl_sv1m_hist, pp0_sv1m_hist, nom_sv1m_hist]

    nom_sv1fe_hist = TH1D("nom_sv1fe", ";SV energy fraction (SV1);Entries", 20, 0, 1)
    ov_sv1fe_hist = TH1D("ov_sv1fe", ";SV energy fraction (SV1);Entries", 20, 0, 1)
    ibl_sv1fe_hist = TH1D("ibl_sv1fe", ";SV energy fraction (SV1);Entries", 20, 0, 1)
    pp0_sv1fe_hist = TH1D("pp0_sv1fe", ";SV energy fraction (SV1);Entries", 20, 0, 1)
    sv1fe_histlist = [ov_sv1fe_hist, ibl_sv1fe_hist, pp0_sv1fe_hist, nom_sv1fe_hist]

    nom_sv1ntrkatvtx_hist = TH1D("nom_sv1ntrkatvtx", ";Number of tracks at SV (SV1);Entries", 11, ten_bins)
    ov_sv1ntrkatvtx_hist = TH1D("ov_sv1ntrkatvtx", ";Number of tracks at SV (SV1);Entries", 11, ten_bins)
    ibl_sv1ntrkatvtx_hist = TH1D("ibl_sv1ntrkatvtx", ";Number of tracks at SV (SV1);Entries", 11, ten_bins)
    pp0_sv1ntrkatvtx_hist = TH1D("pp0_sv1ntrkatvtx", ";Number of tracks at SV (SV1);Entries", 11, ten_bins)
    sv1ntrkatvtx_histlist = [ov_sv1ntrkatvtx_hist, ibl_sv1ntrkatvtx_hist, pp0_sv1ntrkatvtx_hist, nom_sv1ntrkatvtx_hist]

    nom_sv1n2trkvtx_hist = TH1D("nom_sv1n2trkvtx", ";Number of SV candidates (SV1);Entries", 11, ten_bins)
    ov_sv1n2trkvtx_hist = TH1D("ov_sv1n2trkvtx", ";Number of SV candidates (SV1);Entries", 11, ten_bins)
    ibl_sv1n2trkvtx_hist = TH1D("ibl_sv1n2trkvtx", ";Number of SV candidates (SV1);Entries", 11, ten_bins)
    pp0_sv1n2trkvtx_hist = TH1D("pp0_sv1n2trkvtx", ";Number of SV candidates (SV1);Entries", 11, ten_bins)
    sv1n2trkvtx_histlist = [ov_sv1n2trkvtx_hist, ibl_sv1n2trkvtx_hist, pp0_sv1n2trkvtx_hist, nom_sv1n2trkvtx_hist]

    nom_sv1lxy_hist = TH1D("nom_sv1lxy", ";SV Lxy (SV1);Entries", 20, 0, 20)
    ov_sv1lxy_hist = TH1D("ov_sv1lxy", ";SV Lxy (SV1);Entries", 20, 0, 20)
    ibl_sv1lxy_hist = TH1D("ibl_sv1lxy", ";SV Lxy (SV1);Entries", 20, 0, 20)
    pp0_sv1lxy_hist = TH1D("pp0_sv1lxy", ";SV Lxy (SV1);Entries", 20, 0, 20)
    sv1lxy_histlist = [ov_sv1lxy_hist, ibl_sv1lxy_hist, pp0_sv1lxy_hist, nom_sv1lxy_hist]

    nom_sv1lxyz_hist = TH1D("nom_sv1lxyz", ";SV Lxyz (SV1);Entries", 20, 0, 30)
    ov_sv1lxyz_hist = TH1D("ov_sv1lxyz", ";SV Lxyz (SV1);Entries", 20, 0, 30)
    ibl_sv1lxyz_hist = TH1D("ibl_sv1lxyz", ";SV Lxyz (SV1);Entries", 20, 0, 30)
    pp0_sv1lxyz_hist = TH1D("pp0_sv1lxyz", ";SV Lxyz (SV1);Entries", 20, 0, 30)
    sv1lxyz_histlist = [ov_sv1lxyz_hist, ibl_sv1lxyz_hist, pp0_sv1lxyz_hist, nom_sv1lxyz_hist]

    nom_sv1sxyz_hist = TH1D("nom_sv1sxyz", ";SV Sxyz (SV1);Entries", 20, 0, 60)
    ov_sv1sxyz_hist = TH1D("ov_sv1sxyz", ";SV Sxyz (SV1);Entries", 20, 0, 60)
    ibl_sv1sxyz_hist = TH1D("ibl_sv1sxyz", ";SV Sxyz (SV1);Entries", 20, 0, 60)
    pp0_sv1sxyz_hist = TH1D("pp0_sv1sxyz", ";SV Sxyz (SV1);Entries", 20, 0, 60)
    sv1sxyz_histlist = [ov_sv1sxyz_hist, ibl_sv1sxyz_hist, pp0_sv1sxyz_hist, nom_sv1sxyz_hist]

    nom_sv1deltaR_hist = TH1D("nom_sv1deltaR", ";SV deltaR (SV1);Entries", 20, 0, 0.5)
    ov_sv1deltaR_hist = TH1D("ov_sv1deltaR", ";SV deltaR (SV1);Entries", 20, 0, 0.5)
    ibl_sv1deltaR_hist = TH1D("ibl_sv1deltaR", ";SV deltaR (SV1);Entries", 20, 0, 0.5)
    pp0_sv1deltaR_hist = TH1D("pp0_sv1deltaR", ";SV deltaR (SV1);Entries", 20, 0, 0.5)
    sv1deltaR_histlist = [ov_sv1deltaR_hist, ibl_sv1deltaR_hist, pp0_sv1deltaR_hist, nom_sv1deltaR_hist]

    nom_sv1nvtx_hist = TH1D("nom_sv1nvtx", ";Number of SVs (SV1);Entries", 2, -0.5, 1.5)
    ov_sv1nvtx_hist = TH1D("ov_sv1nvtx", ";Number of SVs (SV1);Entries", 2, -0.5, 1.5)
    ibl_sv1nvtx_hist = TH1D("ibl_sv1nvtx", ";Number of SVs (SV1);Entries", 2, -0.5, 1.5)
    pp0_sv1nvtx_hist = TH1D("pp0_sv1nvtx", ";Number of SVs (SV1);Entries", 2, -0.5, 1.5)
    sv1nvtx_histlist = [ov_sv1nvtx_hist, ibl_sv1nvtx_hist, pp0_sv1nvtx_hist, nom_sv1nvtx_hist]

    nom_jfLLbl_hist = TH1D("nom_jfLLbl", ";JF log(Pb/Pl);Entries", 20, -5, 5)
    ov_jfLLbl_hist = TH1D("ov_jfLLbl", ";JF log(Pb/Pl);Entries", 20, -5, 5)
    ibl_jfLLbl_hist = TH1D("ibl_jfLLbl", ";JF log(Pb/Pl);Entries", 20, -5, 5)
    pp0_jfLLbl_hist = TH1D("pp0_jfLLbl", ";JF log(Pb/Pl);Entries", 20, -5, 5)
    jfLLbl_histlist = [ov_jfLLbl_hist, ibl_jfLLbl_hist, pp0_jfLLbl_hist, nom_jfLLbl_hist]

    nom_jfLLbc_hist = TH1D("nom_jfLLbc", ";JF log(Pb/Pc);Entries", 20, -2, 5)
    ov_jfLLbc_hist = TH1D("ov_jfLLbc", ";JF log(Pb/Pc);Entries", 20, -2, 5)
    ibl_jfLLbc_hist = TH1D("ibl_jfLLbc", ";JF log(Pb/Pc);Entries", 20, -2, 5)
    pp0_jfLLbc_hist = TH1D("pp0_jfLLbc", ";JF log(Pb/Pc);Entries", 20, -2, 5)
    jfLLbc_histlist = [ov_jfLLbc_hist, ibl_jfLLbc_hist, pp0_jfLLbc_hist, nom_jfLLbc_hist]

    nom_jfLLcl_hist = TH1D("nom_jfLLcl", ";JF log(Pc/Pl);Entries", 20, -4, 3)
    ov_jfLLcl_hist = TH1D("ov_jfLLcl", ";JF log(Pc/Pl);Entries", 20, -4, 3)
    ibl_jfLLcl_hist = TH1D("ibl_jfLLcl", ";JF log(Pc/Pl);Entries", 20, -4, 3)
    pp0_jfLLcl_hist = TH1D("pp0_jfLLcl", ";JF log(Pc/Pl);Entries", 20, -4, 3)
    jfLLcl_histlist = [ov_jfLLcl_hist, ibl_jfLLcl_hist, pp0_jfLLcl_hist, nom_jfLLcl_hist]

    nom_jfm_hist = TH1D("nom_jfm", ";SV mass (JF);Entries", 20, 0, 4)
    ov_jfm_hist = TH1D("ov_jfm", ";SV mass (JF);Entries", 20, 0, 4)
    ibl_jfm_hist = TH1D("ibl_jfm", ";SV mass (JF);Entries", 20, 0, 4)
    pp0_jfm_hist = TH1D("pp0_jfm", ";SV mass (JF);Entries", 20, 0, 4)
    jfm_histlist = [ov_jfm_hist, ibl_jfm_hist, pp0_jfm_hist, nom_jfm_hist]

    nom_jffe_hist = TH1D("nom_jffe", ";SV energy fraction (JF);Entries", 20, 0, 1)
    ov_jffe_hist = TH1D("ov_jffe", ";SV energy fraction (JF);Entries", 20, 0, 1)
    ibl_jffe_hist = TH1D("ibl_jffe", ";SV energy fraction (JF);Entries", 20, 0, 1)
    pp0_jffe_hist = TH1D("pp0_jffe", ";SV energy fraction (JF);Entries", 20, 0, 1)
    jffe_histlist = [ov_jffe_hist, ibl_jffe_hist, pp0_jffe_hist, nom_jffe_hist]

    nom_jfntrkatvtx_hist = TH1D("nom_jfntrkatvtx", ";Number of tracks at SV (JF);Entries", 11, ten_bins)
    ov_jfntrkatvtx_hist = TH1D("ov_jfntrkatvtx", ";Number of tracks at SV (JF);Entries", 11, ten_bins)
    ibl_jfntrkatvtx_hist = TH1D("ibl_jfntrkatvtx", ";Number of tracks at SV (JF);Entries", 11, ten_bins)
    pp0_jfntrkatvtx_hist = TH1D("pp0_jfntrkatvtx", ";Number of tracks at SV (JF);Entries", 11, ten_bins)
    jfntrkatvtx_histlist = [ov_jfntrkatvtx_hist, ibl_jfntrkatvtx_hist, pp0_jfntrkatvtx_hist, nom_jfntrkatvtx_hist]

    nom_jfn1trkvtx_hist = TH1D("nom_jfn1trkvtx", ";Number of 1 track SV candidates (JF);Entries", 6, five_bins)
    ov_jfn1trkvtx_hist = TH1D("ov_jfn1trkvtx", ";Number of 1 track SV candidates (JF);Entries", 6, five_bins)
    ibl_jfn1trkvtx_hist = TH1D("ibl_jfn1trkvtx", ";Number of 1 track SV candidates (JF);Entries", 6, five_bins)
    pp0_jfn1trkvtx_hist = TH1D("pp0_jfn1trkvtx", ";Number of 1 track SV candidates (JF);Entries", 6, five_bins)
    jfn1trkvtx_histlist = [ov_jfn1trkvtx_hist, ibl_jfn1trkvtx_hist, pp0_jfn1trkvtx_hist, nom_jfn1trkvtx_hist]

    nom_jfn2trkvtx_hist = TH1D("nom_jfn2trkvtx", ";Number of 2 track SV candidates (JF);Entries", 11, ten_bins)
    ov_jfn2trkvtx_hist = TH1D("ov_jfn2trkvtx", ";Number of 2 track SV candidates (JF);Entries", 11, ten_bins)
    ibl_jfn2trkvtx_hist = TH1D("ibl_jfn2trkvtx", ";Number of 2 track SV candidates (JF);Entries", 11, ten_bins)
    pp0_jfn2trkvtx_hist = TH1D("pp0_jfn2trkvtx", ";Number of 2 track SV candidates (JF);Entries", 11, ten_bins)
    jfn2trkvtx_histlist = [ov_jfn2trkvtx_hist, ibl_jfn2trkvtx_hist, pp0_jfn2trkvtx_hist, nom_jfn2trkvtx_hist]

    nom_jfsxyz_hist = TH1D("nom_jfsxyz", ";SV Sxyz (JF);Entries", 20, 0, 50)
    ov_jfsxyz_hist = TH1D("ov_jfsxyz", ";SV Sxyz (JF);Entries", 20, 0, 50)
    ibl_jfsxyz_hist = TH1D("ibl_jfsxyz", ";SV Sxyz (JF);Entries", 20, 0, 50)
    pp0_jfsxyz_hist = TH1D("pp0_jfsxyz", ";SV Sxyz (JF);Entries", 20, 0, 50)
    jfsxyz_histlist = [ov_jfsxyz_hist, ibl_jfsxyz_hist, pp0_jfsxyz_hist, nom_jfsxyz_hist]

    nom_jfdeltaR_hist = TH1D("nom_jfdeltaR", ";SV deltaR (JF);Entries", 20, 14, 16)
    ov_jfdeltaR_hist = TH1D("ov_jfdeltaR", ";SV deltaR (JF);Entries", 20, 14, 16)
    ibl_jfdeltaR_hist = TH1D("ibl_jfdeltaR", ";SV deltaR (JF);Entries", 20, 14, 16)
    pp0_jfdeltaR_hist = TH1D("pp0_jfdeltaR", ";SV deltaR (JF);Entries", 20, 14, 16)
    jfdeltaR_histlist = [ov_jfdeltaR_hist, ibl_jfdeltaR_hist, pp0_jfdeltaR_hist, nom_jfdeltaR_hist]

    nom_jfnvtx_hist = TH1D("nom_jfnvtx", ";Number of SVs (JF);Entries", 3, -0.5, 2.5)
    ov_jfnvtx_hist = TH1D("ov_jfnvtx", ";Number of SVs (JF);Entries", 3, -0.5, 2.5)
    ibl_jfnvtx_hist = TH1D("ibl_jfnvtx", ";Number of SVs (JF);Entries", 3, -0.5, 2.5)
    pp0_jfnvtx_hist = TH1D("pp0_jfnvtx", ";Number of SVs (JF);Entries", 3, -0.5, 2.5)
    jfnvtx_histlist = [ov_jfnvtx_hist, ibl_jfnvtx_hist, pp0_jfnvtx_hist, nom_jfnvtx_hist]

    nom_bhadptfrac_hist = TH1D("nom_bhadptfrac", ";bH/jet pT ratio;Entries", 20, 0.0, 1.0)
    ov_bhadptfrac_hist = TH1D("ov_bhadptfrac", ";bH/jet pT ratio;Entries", 20, 0.0, 1.0)
    ibl_bhadptfrac_hist = TH1D("ibl_bhadptfrac", ";bH/jet pT ratio;Entries", 20, 0.0, 1.0)
    pp0_bhadptfrac_hist = TH1D("pp0_bhadptfrac", ";bH/jet pT ratio;Entries", 20, 0.0, 1.0)
    bhadptfrac_histlist = [ov_bhadptfrac_hist, ibl_bhadptfrac_hist, pp0_bhadptfrac_hist, nom_bhadptfrac_hist]

    nom_nosecs_hist = TH1D("nom_nosecs", ";Number of secondary tracks;Entries", 11, ten_bins)
    ov_nosecs_hist = TH1D("ov_nosecs", ";Number of secondary tracks;Entries", 11, ten_bins)
    ibl_nosecs_hist = TH1D("ibl_nosecs", ";Number of secondary tracks;Entries", 11, ten_bins)
    pp0_nosecs_hist = TH1D("pp0_nosecs", ";Number of secondary tracks;Entries", 11, ten_bins)
    nosecs_histlist = [ov_nosecs_hist, ibl_nosecs_hist, pp0_nosecs_hist, nom_nosecs_hist]

    nom_d0sz0s_hist = TH2D("nom_d0sz0s", ";z0 significance;d0 significance", 20, -5, 5, 20, -5, 5)
    ov_d0sz0s_hist = TH2D("ov_d0sz0s", ";z0 significance;d0 significance", 20, -5, 5, 20, -5, 5)
    ibl_d0sz0s_hist = TH2D("ibl_d0sz0s", ";z0 significance;d0 significance", 20, -5, 5, 20, -5, 5)
    pp0_d0sz0s_hist = TH2D("pp0_d0sz0s", ";z0 significance;d0 significance", 20, -5, 5, 20, -5, 5)
    d0sz0s_histlist = [ov_d0sz0s_hist, ibl_d0sz0s_hist, pp0_d0sz0s_hist, nom_d0sz0s_hist]
    d0sz0s_ratiolist = [None]*4

    for i, chain in enumerate(chain_list):
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

        if jet_flavors == 'b':
            flavorcut = "&&jet_LabDr_HadF==5"
            appendix = '_b'
        elif jet_flavors == 'c':
            flavorcut = "&&jet_LabDr_HadF==4"
            appendix = '_c'
        elif jet_flavors == 'l':
            flavorcut = "&&jet_LabDr_HadF!=4&&jet_LabDr_HadF!=5"
            appendix = '_l'
        else:
            flavorcut = ""
            appendix = ""
        cut = "jet_pt>20e3&&fabs(jet_eta)<2.5"+flavorcut

        chain.Draw("jet_trk_pt*0.001>>"+prefix+"_pt",cut,"goff")
        chain.Draw("jet_trk_qoverp/0.001>>"+prefix+"_qoverp",cut,"goff")
        chain.Draw("jet_trk_d0/(jet_trk_cov_d0d0**0.5)>>"+prefix+"_d0s",cut,"goff")
        chain.Draw("jet_trk_d0>>"+prefix+"_d0",cut,"goff")
        chain.Draw("jet_trk_ip3d_d0>>"+prefix+"_d0sign",cut,"goff")
        chain.Draw("jet_trk_z0/(jet_trk_cov_z0z0**0.5)>>"+prefix+"_z0s",cut,"goff")
        chain.Draw("jet_trk_z0>>"+prefix+"_z0",cut,"goff")
        chain.Draw("jet_trk_ip3d_z0>>"+prefix+"_z0sign",cut,"goff")
        chain.Draw("jet_trk_nPixHits>>"+prefix+"_nPixHits",cut,"goff")
        chain.Draw("jet_trk_nSCTHits>>"+prefix+"_nSCTHits",cut,"goff")
        chain.Draw("jet_trk_nBLHits>>"+prefix+"_nBLHits",cut,"goff")
        chain.Draw("jet_trk_nPixHoles>>"+prefix+"_nPixHoles",cut,"goff")
        chain.Draw("jet_trk_nSCTHoles>>"+prefix+"_nSCTHoles",cut,"goff")
        chain.Draw("jet_trk_nsharedPixHits>>"+prefix+"_nPixShared",cut,"goff")
        chain.Draw("jet_trk_nsharedSCTHits>>"+prefix+"_nSCTShared",cut,"goff")
        chain.Draw("jet_trk_nsharedBLHits>>"+prefix+"_nBLShared",cut,"goff")
        chain.Draw("jet_trk_nsplitPixHits>>"+prefix+"_nPixSplit",cut,"goff")
        chain.Draw("jet_trk_nsplitBLHits>>"+prefix+"_nBLSplit",cut,"goff")
        chain.Draw("jet_eta>>"+prefix+"_jeteta",cut,"goff")
        chain.Draw("jet_pt*0.001>>"+prefix+"_jetpt",cut,"goff")
        chain.Draw("jet_btag_ntrk>>"+prefix+"_jetntrk",cut,"goff")
        chain.Draw("njets>>"+prefix+"_evnjet",cut,"goff")
        chain.Draw("log(jet_ip3d_pb/jet_ip3d_pu)>>"+prefix+"_ip3dLLbl",cut+"&&jet_ip3d_pb>0&&jet_ip3d_pu>0","goff")
        chain.Draw("log(jet_ip3d_pb/jet_ip3d_pc)>>"+prefix+"_ip3dLLbc",cut+"&&jet_ip3d_pb>0&&jet_ip3d_pc>0","goff")
        chain.Draw("log(jet_ip3d_pc/jet_ip3d_pu)>>"+prefix+"_ip3dLLcl",cut+"&&jet_ip3d_pc>0&&jet_ip3d_pu>0","goff")
        chain.Draw("log(jet_rnnip_pb/jet_rnnip_pu)>>"+prefix+"_rnnipLLbl",cut+"&&jet_rnnip_pb>0&&jet_rnnip_pu>0","goff")
        chain.Draw("log(jet_rnnip_pb/jet_rnnip_pc)>>"+prefix+"_rnnipLLbc",cut+"&&jet_rnnip_pb>0&&jet_rnnip_pc>0","goff")
        chain.Draw("log(jet_rnnip_pc/jet_rnnip_pu)>>"+prefix+"_rnnipLLcl",cut+"&&jet_rnnip_pc>0&&jet_rnnip_pu>0","goff")
        chain.Draw("log(jet_dl1_pb/jet_dl1_pu)>>"+prefix+"_dl1LLbl",cut+"&&jet_dl1_pb>0&&jet_dl1_pu>0","goff")
        chain.Draw("log(jet_dl1_pb/jet_dl1_pc)>>"+prefix+"_dl1LLbc",cut+"&&jet_dl1_pb>0&&jet_dl1_pc>0","goff")
        chain.Draw("log(jet_dl1_pc/jet_dl1_pu)>>"+prefix+"_dl1LLcl",cut+"&&jet_dl1_pc>0&&jet_dl1_pu>0","goff")
        chain.Draw("log(jet_dl1r_pb/jet_dl1r_pu)>>"+prefix+"_dl1rLLbl",cut+"&&jet_dl1r_pb>0&&jet_dl1r_pu>0","goff")
        chain.Draw("log(jet_dl1r_pb/jet_dl1r_pc)>>"+prefix+"_dl1rLLbc",cut+"&&jet_dl1r_pb>0&&jet_dl1r_pc>0","goff")
        chain.Draw("log(jet_dl1r_pc/jet_dl1r_pu)>>"+prefix+"_dl1rLLcl",cut+"&&jet_dl1r_pc>0&&jet_dl1r_pu>0","goff")
        chain.Draw("log(jet_jf_pb/jet_jf_pu)>>"+prefix+"_jfLLbl",cut+"&&jet_jf_pb>0&&jet_jf_pu>0","goff")
        chain.Draw("log(jet_jf_pb/jet_jf_pc)>>"+prefix+"_jfLLbc",cut+"&&jet_jf_pb>0&&jet_jf_pc>0","goff")
        chain.Draw("log(jet_jf_pc/jet_jf_pu)>>"+prefix+"_jfLLcl",cut+"&&jet_jf_pc>0&&jet_jf_pu>0","goff")
        chain.Draw("jet_jf_m*0.001>>"+prefix+"_jfm",cut,"goff")
        chain.Draw("jet_jf_efc>>"+prefix+"_jffe",cut,"goff")
        chain.Draw("jet_jf_ntrkAtVx>>"+prefix+"_jfntrkatvtx",cut,"goff")
        chain.Draw("jet_jf_nvtx1t>>"+prefix+"_jfn1trkvtx",cut,"goff")
        chain.Draw("jet_jf_n2t>>"+prefix+"_jfn2trkvtx",cut,"goff")
        chain.Draw("jet_jf_sig3d>>"+prefix+"_jfsxyz",cut,"goff")
        chain.Draw("jet_jf_dR>>"+prefix+"_jfdeltaR",cut,"goff")
        chain.Draw("jet_jf_nvtx>>"+prefix+"_jfnvtx",cut,"goff")
        chain.Draw("jet_sv1_m*0.001>>"+prefix+"_sv1m",cut,"goff")
        chain.Draw("jet_sv1_efc>>"+prefix+"_sv1fe",cut,"goff")
        chain.Draw("jet_sv1_ntrkv>>"+prefix+"_sv1ntrkatvtx",cut,"goff")
        chain.Draw("jet_sv1_n2t>>"+prefix+"_sv1n2trkvtx",cut,"goff")
        chain.Draw("jet_sv1_Lxy>>"+prefix+"_sv1lxy",cut,"goff")
        chain.Draw("jet_sv1_L3d>>"+prefix+"_sv1lxyz",cut,"goff")
        chain.Draw("jet_sv1_sig3d>>"+prefix+"_sv1sxyz",cut,"goff")
        chain.Draw("jet_sv1_deltaR>>"+prefix+"_sv1deltaR",cut,"goff")
        chain.Draw("jet_sv1_Nvtx>>"+prefix+"_sv1nvtx",cut,"goff")
        chain.Draw("jet_bH_pt/jet_pt>>"+prefix+"_bhadptfrac",cut+"&&jet_bH_pt>0","goff")
        chain.Draw("Sum$(jet_trk_barcode>200000)>>"+prefix+"_nosecs",cut,"goff")

        chain.Draw("jet_trk_d0/(jet_trk_cov_d0d0**0.5):jet_trk_z0/(jet_trk_cov_z0z0**0.5)>>"+prefix+"_d0sz0s",cut,"goff")

    canv1 = TCanvas("c1", "c1",200,10,900,900)

    ####
    for hist in evnjet_histlist:
        print(hist.GetEntries())

    plot_hist(canv1, qoverp_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_qoverp'+appendix+''+appendix+'.pdf')
    plot_hist(canv1, d0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_d0'+appendix+'.pdf')
    plot_hist(canv1, z0_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_z0'+appendix+'.pdf')
    plot_hist(canv1, pt_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_pt'+appendix+'.pdf')
    plot_hist(canv1, d0s_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_d0s'+appendix+'.pdf')
    plot_hist(canv1, d0sign_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_d0sign'+appendix+'.pdf')
    plot_hist(canv1, z0s_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_z0s'+appendix+'.pdf')
    plot_hist(canv1, z0sign_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_z0sign'+appendix+'.pdf')
    plot_hist(canv1, nPixHits_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nPixHits'+appendix+'.pdf')
    plot_hist(canv1, nSCTHits_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nSCTHits'+appendix+'.pdf')
    plot_hist(canv1, nBLHits_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nBLHits'+appendix+'.pdf')
    plot_hist(canv1, nPixHoles_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nPixHoles'+appendix+'.pdf')
    plot_hist(canv1, nSCTHoles_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nSCTHoles'+appendix+'.pdf')
    plot_hist(canv1, nPixShared_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nPixShared'+appendix+'.pdf')
    plot_hist(canv1, nSCTShared_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nSCTShared'+appendix+'.pdf')
    plot_hist(canv1, nBLShared_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nBLShared'+appendix+'.pdf')
    plot_hist(canv1, nPixSplit_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nPixSplit'+appendix+'.pdf')
    plot_hist(canv1, nBLSplit_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nBLSplit'+appendix+'.pdf')
    plot_hist(canv1, jetpt_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jetpt'+appendix+'.pdf')
    plot_hist(canv1, jeteta_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jeteta'+appendix+'.pdf')
    plot_hist(canv1, jetntrk_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jetntrk'+appendix+'.pdf')
    plot_hist(canv1, evnjet_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_evnjet'+appendix+'.pdf')
    plot_hist(canv1, ip3dLLbl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_ip3dLLbl'+appendix+'.pdf')
    plot_hist(canv1, ip3dLLbc_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_ip3dLLbc'+appendix+'.pdf')
    plot_hist(canv1, ip3dLLcl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_ip3dLLcl'+appendix+'.pdf')
    plot_hist(canv1, rnnipLLbl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_rnnipLLbl'+appendix+'.pdf')
    plot_hist(canv1, rnnipLLbc_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_rnnipLLbc'+appendix+'.pdf')
    plot_hist(canv1, rnnipLLcl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_rnnipLLcl'+appendix+'.pdf')
    plot_hist(canv1, dl1LLbl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1LLbl'+appendix+'.pdf')
    plot_hist(canv1, dl1LLbc_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1LLbc'+appendix+'.pdf')
    plot_hist(canv1, dl1LLcl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1LLcl'+appendix+'.pdf')
    plot_hist(canv1, dl1rLLbl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1rLLbl'+appendix+'.pdf')
    plot_hist(canv1, dl1rLLbc_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1rLLbc'+appendix+'.pdf')
    plot_hist(canv1, dl1rLLcl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_dl1rLLcl'+appendix+'.pdf')
    plot_hist(canv1, jfLLbl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfLLbl'+appendix+'.pdf')
    plot_hist(canv1, jfLLbc_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfLLbc'+appendix+'.pdf')
    plot_hist(canv1, jfLLcl_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfLLcl'+appendix+'.pdf')
    plot_hist(canv1, jfm_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfm'+appendix+'.pdf')
    plot_hist(canv1, jffe_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jffe'+appendix+'.pdf')
    plot_hist(canv1, jfntrkatvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfntrkatvtx'+appendix+'.pdf')
    plot_hist(canv1, jfn1trkvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfn1trkvtx'+appendix+'.pdf')
    plot_hist(canv1, jfn2trkvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfn2trkvtx'+appendix+'.pdf')
    plot_hist(canv1, jfsxyz_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfsxyz'+appendix+'.pdf')
    plot_hist(canv1, jfdeltaR_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfdeltaR'+appendix+'.pdf')
    plot_hist(canv1, jfnvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_jfnvtx'+appendix+'.pdf')
    plot_hist(canv1, sv1m_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1m'+appendix+'.pdf')
    plot_hist(canv1, sv1fe_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1fe'+appendix+'.pdf')
    plot_hist(canv1, sv1ntrkatvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1ntrkatvtx'+appendix+'.pdf')
    plot_hist(canv1, sv1n2trkvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1n2trkvtx'+appendix+'.pdf')
    plot_hist(canv1, sv1lxy_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1lxy'+appendix+'.pdf')
    plot_hist(canv1, sv1lxyz_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1lxyz'+appendix+'.pdf')
    plot_hist(canv1, sv1sxyz_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1sxyz'+appendix+'.pdf')
    plot_hist(canv1, sv1deltaR_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1deltaR'+appendix+'.pdf')
    plot_hist(canv1, sv1nvtx_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_sv1nvtx'+appendix+'.pdf')
    plot_hist(canv1, bhadptfrac_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_bhadptfrac'+appendix+'.pdf')
    plot_hist(canv1, nosecs_histlist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, False, True, outdir+'hist_nosecs'+appendix+'.pdf')

    canv2 = TCanvas("c2", "c2", 800, 600)
    plot_2dhist_ratio(canv2, ov_d0sz0s_hist, nom_d0sz0s_hist, 'overall', outdir+'2dhist_ipsig_ov'+appendix+'.pdf')
    plot_2dhist_ratio(canv2, ibl_d0sz0s_hist, nom_d0sz0s_hist, 'ibl', outdir+'2dhist_ipsig_ibl'+appendix+'.pdf')
    plot_2dhist_ratio(canv2, pp0_d0sz0s_hist, nom_d0sz0s_hist, 'pp0', outdir+'2dhist_ipsig_pp0'+appendix+'.pdf')


if __name__ == '__main__':
    main(sys.argv)
