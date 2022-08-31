#!/usr/bin/env python

import os,sys,math,glob,ROOT
import numpy as np
import h5py
import argparse
from ROOT import gROOT, TFile, TH1D, TLorentzVector, TCanvas, TTree, gDirectory, TChain, TH2D, gPad

from plot_functions import *
import options

#set ATLAS style for plots
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasStyle.C")
gROOT.LoadMacro(options.atlasstyle_dir+"AtlasLabels.C")
from ROOT import SetAtlasStyle


def convert_wp(wp):
    if wp == 0.6:
        return (4.414999961853027, 4.565000057220459)
    elif wp == 0.7:
        return (3.0950000286102295, 3.244999885559082)
    elif wp == 0.77:
        return (2.015000104904175, 2.194999933242798)
    elif wp == 0.85:
        return (0.36500000953674316, 0.6650000214576721)
    else:
        print("WARNING: WP not found")
        return (0, 0)


def main(argv):
    gROOT.SetBatch(True)
    SetAtlasStyle()

    indir = options.indir 
    outdir = options.outdir
    fc_dl1 = options.fc_dl1
    fc_dl1r = options.fc_dl1r
    files = options.dataset

    treename = "bTag_AntiKt4EMPFlowJets_BTagging201903"
    
    #parse command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-w", "--wp", type=float, required=True, dest="eff_wp", help="0.6, 0.7, 0.77 or 0.85")
    parser.add_argument("-v", "--xvar", type=str, required=True, dest="xvar", help="pt_high, pt_low or eta")
    args = parser.parse_args()

    xvar = args.xvar
    eff_wp = args.eff_wp

    dl1_wp, dl1r_wp = convert_wp(eff_wp)
    wp_ext = str(eff_wp*100)[:2]
    
    if files == "ttbar":
        dataset_string = "t#bar{t}, WP = "+str(eff_wp)
    elif files == "zp":
        dataset_string = "Z', WP = "+str(eff_wp)

    if xvar == "pt_high":
        xlabel = "jet pT [GeV]"
        if files == "ttbar":
            b_bins = np.array([400.,500.,600.,700.,800.,900.,1000.,1100.,1250.]) #,1400.,1550.,1750.,2000.,2250.,2500.,2750.,3000.])
            c_bins = np.array([250.,360.,490.,630.,790.,960.,1160.]) #,1400.,1680.,2070.,3000.])
        elif files == "zp":
            b_bins = np.array([400.,500.,600.,700.,800.,900.,1000.,1100.,1250.,1400.,1550.,1750.,2000.,2250.,2500.,2750.,3000.])
            c_bins = np.array([250.,360.,490.,630.,790.,960.,1160.,1400.,1680.,2070.,3000.])
        l_bins = np.array([300.,3000.])
        xvar = "jet_pt*0.001"
        ext = files+"_"+wp_ext+"_pt_high"
    elif xvar == "pt_low":
        xlabel = "jet pT [GeV]" 
        b_bins = np.array([20.,30.,40.,60.,85.,110.,140.,175.,250., 400.])
        c_bins = np.array([20.,40.,65.,140., 250.])
        l_bins = np.array([20.,50.,100.,150., 300.])
        xvar = "jet_pt*0.001"
        ext = files+"_"+wp_ext+"_pt_low"
    elif xvar == "eta":
        xlabel = "jet eta"
        b_bins = np.linspace(-2.5,2.5,num=20)
        c_bins = b_bins
        l_bins = b_bins
        xvar = "jet_eta"
        ext = files+"_"+wp_ext+"_eta"

    nomfiles = glob.glob(indir+'Nominal/'+'*')
    ovfiles = glob.glob(indir+'Overall/'+'*')
    iblfiles = glob.glob(indir+'IBL/'+'*')
    pp0files = glob.glob(indir+'PP0/'+'*')

    nomchain = TChain(treename)
    ovchain = TChain(treename)
    iblchain = TChain(treename)
    pp0chain = TChain(treename)

    general_cut = "jet_pt>20e3&&fabs(jet_eta)<2.5"
    bcut = general_cut+"&&jet_LabDr_HadF==5"
    ccut = general_cut+"&&jet_LabDr_HadF==4"
    lcut = general_cut+"&&jet_LabDr_HadF!=5&&jet_LabDr_HadF!=4"

    chain_list = [ovchain, iblchain, pp0chain, nomchain]
    infile_lists = [ovfiles, iblfiles, pp0files, nomfiles]
    for i,chain in enumerate(chain_list):
        infile_list = infile_lists[i]
        for ifile in infile_list:
            chain.AddFile(ifile)

    nom_bjet_eff_dl1_hist = TH2D("nom_bjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{b} (DL1)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    ov_bjet_eff_dl1_hist = TH2D("ov_bjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{b} (DL1)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    ibl_bjet_eff_dl1_hist = TH2D("ibl_bjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{b} (DL1)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    pp0_bjet_eff_dl1_hist = TH2D("pp0_bjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{b} (DL1)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    bjet_eff_dl1_histlist = [ov_bjet_eff_dl1_hist, ibl_bjet_eff_dl1_hist, pp0_bjet_eff_dl1_hist, nom_bjet_eff_dl1_hist]
    bjet_eff_dl1_proflist = [None]*4

    nom_cjet_eff_dl1_hist = TH2D("nom_cjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{c} (DL1)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    ov_cjet_eff_dl1_hist = TH2D("ov_cjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{c} (DL1)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    ibl_cjet_eff_dl1_hist = TH2D("ibl_cjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{c} (DL1)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    pp0_cjet_eff_dl1_hist = TH2D("pp0_cjet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{c} (DL1)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    cjet_eff_dl1_histlist = [ov_cjet_eff_dl1_hist, ibl_cjet_eff_dl1_hist, pp0_cjet_eff_dl1_hist, nom_cjet_eff_dl1_hist]
    cjet_eff_dl1_proflist = [None]*4

    nom_ljet_eff_dl1_hist = TH2D("nom_ljet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{l} (DL1)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ov_ljet_eff_dl1_hist = TH2D("ov_ljet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{l} (DL1)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ibl_ljet_eff_dl1_hist = TH2D("ibl_ljet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{l} (DL1)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    pp0_ljet_eff_dl1_hist = TH2D("pp0_ljet_eff_dl1", "WP = "+str(dl1_wp)+";"+xlabel+";#epsilon_{l} (DL1)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ljet_eff_dl1_histlist = [ov_ljet_eff_dl1_hist, ibl_ljet_eff_dl1_hist, pp0_ljet_eff_dl1_hist, nom_ljet_eff_dl1_hist]
    ljet_eff_dl1_proflist = [None]*4

    nom_bjet_eff_dl1r_hist = TH2D("nom_bjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{b} (DL1r)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    ov_bjet_eff_dl1r_hist = TH2D("ov_bjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{b} (DL1r)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    ibl_bjet_eff_dl1r_hist = TH2D("ibl_bjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{b} (DL1r)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    pp0_bjet_eff_dl1r_hist = TH2D("pp0_bjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{b} (DL1r)", len(b_bins)-1, b_bins, 2, -0.5, 1.5)
    bjet_eff_dl1r_histlist = [ov_bjet_eff_dl1r_hist, ibl_bjet_eff_dl1r_hist, pp0_bjet_eff_dl1r_hist, nom_bjet_eff_dl1r_hist]
    bjet_eff_dl1r_proflist = [None]*4

    nom_cjet_eff_dl1r_hist = TH2D("nom_cjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{c} (DL1r)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    ov_cjet_eff_dl1r_hist = TH2D("ov_cjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{c} (DL1r)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    ibl_cjet_eff_dl1r_hist = TH2D("ibl_cjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{c} (DL1r)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    pp0_cjet_eff_dl1r_hist = TH2D("pp0_cjet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{c} (DL1r)", len(c_bins)-1, c_bins, 2, -0.5, 1.5)
    cjet_eff_dl1r_histlist = [ov_cjet_eff_dl1r_hist, ibl_cjet_eff_dl1r_hist, pp0_cjet_eff_dl1r_hist, nom_cjet_eff_dl1r_hist]
    cjet_eff_dl1r_proflist = [None]*4

    nom_ljet_eff_dl1r_hist = TH2D("nom_ljet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{l} (DL1r)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ov_ljet_eff_dl1r_hist = TH2D("ov_ljet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{l} (DL1r)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ibl_ljet_eff_dl1r_hist = TH2D("ibl_ljet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{l} (DL1r)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    pp0_ljet_eff_dl1r_hist = TH2D("pp0_ljet_eff_dl1r", "WP = "+str(dl1r_wp)+";"+xlabel+";#epsilon_{l} (DL1r)", len(l_bins)-1, l_bins, 2, -0.5, 1.5)
    ljet_eff_dl1r_histlist = [ov_ljet_eff_dl1r_hist, ibl_ljet_eff_dl1r_hist, pp0_ljet_eff_dl1r_hist, nom_ljet_eff_dl1r_hist]
    ljet_eff_dl1r_proflist = [None]*4
    
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

        chain.Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>"+str(dl1_wp)+":"+xvar+">>"+prefix+"_bjet_eff_dl1",bcut,"goff")
        bjet_eff_dl1_proflist[i] = bjet_eff_dl1_histlist[i].ProfileX()
        bjet_eff_dl1_proflist[i].GetYaxis().SetTitle(bjet_eff_dl1_histlist[i].GetYaxis().GetTitle())

        chain.Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>"+str(dl1_wp)+":"+xvar+">>"+prefix+"_cjet_eff_dl1",ccut,"goff")
        cjet_eff_dl1_proflist[i] = cjet_eff_dl1_histlist[i].ProfileX()
        cjet_eff_dl1_proflist[i].GetYaxis().SetTitle(cjet_eff_dl1_histlist[i].GetYaxis().GetTitle())

        chain.Draw("(log(jet_dl1_pb/("+str(fc_dl1)+"*jet_dl1_pc+(1-"+str(fc_dl1)+")*jet_dl1_pu)))>"+str(dl1_wp)+":"+xvar+">>"+prefix+"_ljet_eff_dl1",lcut,"goff")
        ljet_eff_dl1_proflist[i] = ljet_eff_dl1_histlist[i].ProfileX()
        ljet_eff_dl1_proflist[i].GetYaxis().SetTitle(ljet_eff_dl1_histlist[i].GetYaxis().GetTitle())

        chain.Draw("(log(jet_dl1r_pb/("+str(fc_dl1r)+"*jet_dl1r_pc+(1-"+str(fc_dl1r)+")*jet_dl1r_pu)))>"+str(dl1r_wp)+":"+xvar+">>"+prefix+"_bjet_eff_dl1r",bcut,"goff")
        bjet_eff_dl1r_proflist[i] = bjet_eff_dl1r_histlist[i].ProfileX()
        bjet_eff_dl1r_proflist[i].GetYaxis().SetTitle(bjet_eff_dl1r_histlist[i].GetYaxis().GetTitle())

        chain.Draw("(log(jet_dl1r_pb/("+str(fc_dl1r)+"*jet_dl1r_pc+(1-"+str(fc_dl1r)+")*jet_dl1r_pu)))>"+str(dl1r_wp)+":"+xvar+">>"+prefix+"_cjet_eff_dl1r",ccut,"goff")
        cjet_eff_dl1r_proflist[i] = cjet_eff_dl1r_histlist[i].ProfileX()
        cjet_eff_dl1r_proflist[i].GetYaxis().SetTitle(cjet_eff_dl1r_histlist[i].GetYaxis().GetTitle())

        chain.Draw("(log(jet_dl1r_pb/("+str(fc_dl1r)+"*jet_dl1r_pc+(1-"+str(fc_dl1r)+")*jet_dl1r_pu)))>"+str(dl1r_wp)+":"+xvar+">>"+prefix+"_ljet_eff_dl1r",lcut,"goff")
        ljet_eff_dl1r_proflist[i] = ljet_eff_dl1r_histlist[i].ProfileX()
        ljet_eff_dl1r_proflist[i].GetYaxis().SetTitle(ljet_eff_dl1r_histlist[i].GetYaxis().GetTitle())

    canv = TCanvas("c1", "c1",200,10,900,900)

    plot_profile(canv, bjet_eff_dl1_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_bjet_eff_dl1_'+ext+'.pdf')
    plot_profile(canv, cjet_eff_dl1_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_cjet_eff_dl1_'+ext+'.pdf')
    plot_profile(canv, ljet_eff_dl1_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_ljet_eff_dl1_'+ext+'.pdf')
    plot_profile(canv, bjet_eff_dl1r_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_bjet_eff_dl1r_'+ext+'.pdf')
    plot_profile(canv, cjet_eff_dl1r_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_cjet_eff_dl1r_'+ext+'.pdf')
    plot_profile(canv, ljet_eff_dl1r_proflist, ['+5% overall', '+10% IBL', '+25% PP0', 'nominal'], 3, dataset_string, outdir+'prof_ljet_eff_dl1r_'+ext+'.pdf')


if __name__ == '__main__':
    main(sys.argv)
