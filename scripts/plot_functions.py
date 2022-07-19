#!/usr/bin/env python

import os,sys,math,ROOT,glob
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TFile, TH1D, TH1I, gROOT, TCanvas, gStyle, gPad, TLegend, TGaxis, THStack, TMultiGraph, TPad, TLatex


colorlist = [432,600,632,401,616,419]


def find_minmax(histlist):
    nbins = histlist[0].GetNbinsX()
    minimum = 1e10
    maximum = 0
    for hist in histlist:
        for i in range(nbins):
            entry = hist.GetBinContent(i)
            if entry < minimum and entry > 1e-10:
                minimum = entry
            if entry > maximum:
                maximum = entry
    return maximum, minimum


def plot_hist(canv, hist_list, labellist, ratioindex, log, norm, filename):
    gStyle.SetOptStat(0)

    pad1 = TPad("pad1", "pad1", 0.05,0.35,1.0,1.0)
    pad1.SetGrid()
    if log: pad1.SetLogy()
    pad1.Draw()
    pad2 = TPad("pad2", "pad2", 0.05,0.0,1.0,0.35)
    pad2.SetGrid()
    pad2.Draw("SAME")
    pad1.SetBottomMargin(0.05)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.25)

    pad1.cd()
    legend = TLegend(0.75-0.15*(math.ceil(len(hist_list)/3)-1),0.76,0.9,0.92,'','NDC')
    legend.SetNColumns(math.ceil(len(hist_list)/3))
    logo = TLatex(0.2,0.88, "#bf{#it{ATLAS}} #it{Internal}")
    add_text = TLatex(0.2,0.83,"p_{T} > 20 GeV, |#eta| < 2.5")
    logo.SetNDC(True)
    add_text.SetNDC(True)

    #normalize histograms
    if norm:
        for i in range(len(hist_list)):
            entries = hist_list[i].GetEntries()
            if entries: hist_list[i].Scale(1./entries)

    #generate ratio histograms
    nom_hist = hist_list[ratioindex].Clone(hist_list[ratioindex].GetName()+"_nom")
    ratio_list = [None]*len(hist_list)
    for i in range(len(hist_list)):
        ratio_list[i] = hist_list[i].Clone(hist_list[i].GetName()+"_ratio")
        ratio_list[i].Divide(nom_hist)

    maximum = max([hist.GetMaximum() for hist in hist_list])
    minimum = min([hist.GetMinimum() for hist in hist_list])

    for i in range(len(hist_list)):
        hist_list[i].SetMarkerColorAlpha(colorlist[i],.75)
        hist_list[i].SetLineColorAlpha(colorlist[i],.65)
        hist_list[i].SetLineWidth(3)
        hist_list[i].SetTitle("")
        hist_list[i].GetXaxis().SetLabelSize(0)
        hist_list[i].GetXaxis().SetTitleSize(0)
        hist_list[i].GetYaxis().SetLabelSize(0.05)
        hist_list[i].GetYaxis().SetTitleSize(0.05)
        hist_list[i].GetYaxis().SetTitleOffset(1.0)

        legend.AddEntry(hist_list[i], labellist[i], "l")

        if maximum > 0 and not log: hist_list[i].SetMaximum(maximum*1.3)
        elif maximum > 0 and log: hist_list[i].SetMaximum(maximum*10)
        hist_list[i].SetMinimum(minimum*0.7)
        hist_list[i].Draw("SAMES")

    legend.SetTextSize(0.03)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.Draw("SAME")
    logo.Draw("SAME")
    add_text.Draw("SAME")

    pad2.cd()
    
    maximum = max([ratio.GetMaximum() for ratio in ratio_list])
    minimum = min([ratio.GetMinimum() for ratio in ratio_list])
    
    for i in range(len(ratio_list)):
        ratio_list[i].SetMarkerColorAlpha(colorlist[i],.75)
        ratio_list[i].SetLineColorAlpha(colorlist[i],.65)
        ratio_list[i].SetLineWidth(3)
        ratio_list[i].SetTitle("")
        ratio_list[i].GetXaxis().SetLabelSize(0.1)
        ratio_list[i].GetXaxis().SetTitleSize(0.1)
        ratio_list[i].GetXaxis().SetTitleOffset(0.9)
        ratio_list[i].GetYaxis().SetLabelSize(0.05)
        ratio_list[i].GetYaxis().SetTitleSize(0.1)
        ratio_list[i].GetYaxis().SetTitle("Sys/Nom")
        ratio_list[i].GetYaxis().SetTitleOffset(0.5)

        if maximum > 0: ratio_list[i].SetMaximum(maximum*1.1)
        ratio_list[i].SetMinimum(minimum*0.9)
        ratio_list[i].Draw("SAMES")

    canv.cd()
    canv.SaveAs(filename)

    del nom_hist
    for ratio in ratio_list:
        ratio.SetDirectory(0)
        del ratio
    canv.Clear()


def plot_profile(canv, profile_list, labellist, ratioindex, wp, filename):
    gStyle.SetOptStat(0)
    gStyle.SetErrorX(.5)

    pad1 = TPad("pad1", "pad1", 0.0,0.35,1.0,1.0)
    pad1.SetGrid()
    pad1.Draw()
    pad2 = TPad("pad2", "pad2", 0.0,0.0,1.0,0.35)
    pad2.SetGrid()
    pad2.Draw("SAME")
    pad1.SetBottomMargin(0.05)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.25)

    pad1.cd()
    legend = TLegend(0.75-0.15*(math.ceil(len(profile_list)/3)-1),0.76,0.9,0.92,'','NDC')
    legend.SetNColumns(math.ceil(len(profile_list)/3))
    logo = TLatex(0.2,0.88, "#bf{#it{ATLAS}} #it{Internal}")
    cut_text = TLatex(0.2,0.81,"p_{T} > 20 GeV, |#eta| < 2.5")
    wp_text = TLatex(0.2,0.74,"WP = "+str(wp))
    logo.SetNDC(True)
    cut_text.SetNDC(True)
    wp_text.SetNDC(True)

    maximum = max([profile.GetMaximum() for profile in profile_list])
    minimum = min([profile.GetMinimum() for profile in profile_list])

    for i in range(len(profile_list)):
        profile_list[i].SetMarkerColorAlpha(colorlist[i],.75)
        profile_list[i].SetLineColorAlpha(colorlist[i],.65)
        profile_list[i].SetLineWidth(3)
        profile_list[i].SetTitle("")
        profile_list[i].GetXaxis().SetLabelSize(0)
        profile_list[i].GetXaxis().SetTitleSize(0)
        profile_list[i].GetYaxis().SetLabelSize(0.05)
        profile_list[i].GetYaxis().SetTitleSize(0.05)
        profile_list[i].GetYaxis().SetTitleOffset(1.0)
        legend.AddEntry(profile_list[i], labellist[i], "l")
        if maximum > 0: profile_list[i].SetMaximum(maximum*1.3)
        profile_list[i].SetMinimum(minimum*0.7)
        profile_list[i].Draw("SAMES")

    legend.SetTextSize(0.03)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.Draw("SAME")
    logo.Draw("SAME")
    cut_text.Draw("SAME")
    wp_text.Draw("SAME")

    pad2.cd()

    nom_profile = profile_list[ratioindex].ProjectionX(profile_list[ratioindex].GetName()+"_nom")
    ratio_list = [None]*len(profile_list)
    for i in range(len(profile_list)):
        ratio_list[i] = profile_list[i].ProjectionX()
        ratio_list[i].Divide(nom_profile)

    maximum = max([ratio.GetMaximum() for ratio in ratio_list])
    minimum = min([ratio.GetMinimum() for ratio in ratio_list])

    for i in range(len(ratio_list)):
        ratio_list[i].SetMarkerColorAlpha(colorlist[i],.75)
        ratio_list[i].SetLineColorAlpha(colorlist[i],.65)
        ratio_list[i].SetLineWidth(3)
        ratio_list[i].SetTitle("")
        ratio_list[i].GetXaxis().SetLabelSize(0.1)
        ratio_list[i].GetXaxis().SetTitleSize(0.1)
        ratio_list[i].GetXaxis().SetTitleOffset(0.9)
        ratio_list[i].GetYaxis().SetLabelSize(0.05)
        ratio_list[i].GetYaxis().SetTitleSize(0.1)
        ratio_list[i].GetYaxis().SetTitle("Sys/Nom")
        ratio_list[i].GetYaxis().SetTitleOffset(0.5)
        if maximum > 0: ratio_list[i].SetMaximum(maximum*1.01)
        ratio_list[i].SetMinimum(minimum*0.99)
        ratio_list[i].Draw("SAMES")

    canv.cd()
    canv.SaveAs(filename)

    del nom_profile
    for ratio in ratio_list:
        ratio.SetDirectory(0)
        del ratio
    canv.Clear()


def plot_2dhist_ratio(canv, hist1, hist2, var, filename):
    #canv.Clear()
    gStyle.SetOptStat(0)
    canv.SetRightMargin(0.15)

    ratiohist = hist1.Clone(hist1.GetName()+"_ratio")
    divhist = hist2.Clone(hist1.GetName()+"_denom")

    entries1 = ratiohist.GetEntries()
    entries2 = divhist.GetEntries()
    if entries1: ratiohist.Scale(1./entries1)
    if entries2: divhist.Scale(1./entries2)

    ratiohist.Divide(divhist)
    ratiohist.Draw("COLZ")

    canv.SaveAs(filename)
    ratiohist.SetDirectory(0)
    divhist.SetDirectory(0)
    del ratiohist
    del divhist
    canv.Clear()
