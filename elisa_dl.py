import os
import sys
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.stats import variation
import pdfkit
import datetime

'''
Credit to https://people.duke.edu/~ccc14/pcfb/analysis.html for the code to fit 
the 4 parameter logistic regression for the standard curve
'''

def logistic4(x, A, B, C, D):
    """4PL logistic equation. Returns OD (y) based on with standard concentration (x) """
    step1 = A-D
    step2 = x/C
    step3 = np.sign(step2) * (np.abs(step2)) ** B
    log_output = (step1/(1.0 + step3) + D)
    return log_output

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)

def get_conc(y, p):
    """returns concentraion (x) with OD (y) input"""
    A,B,C,D = p
    step1 = ((A-D)/(y-D)) - 1
    step2 = np.sign(step1) * (np.abs(step1)) ** (1/B)
    concentration = step2 * C
    return concentration

std_concs = [1000, 571.4285714, 326.5306122, 186.5889213, 106.6222407, 60.9269947,
             34.81542555, 19.89452888, 11.36830222, 6.496172697, 3.712098684, 2.121199248]

antigens = {"s" : "Spike", "n" : "Nucleocapsid"}

cut_offs = {"s" : 0.23, "n" : 0.76}

if __name__ == "__main__":
    sys.path.insert(1, './scripts')
    from template import html
    from plate_plans import get_ods, get_samples
    plate_id = sys.argv[1]
    antigen = sys.argv[2]
    plateplan_file = plate_id + "-pplan.xlsx"
    platereader_file = plate_id + "-preader.xlsx"
    ods = get_ods(platereader_file) #retutns python dictionary with ods from plate
    sample_dilution = get_samples(plateplan_file) #returns python dictionary with samples names and dilutions

    print("Found plateplan file: %s" % plateplan_file)
    print("Found plate reader file: %s" % platereader_file)
    print("Antigen: %s" % antigens[antigen])

    np.set_printoptions(suppress=True) #suppresses scientific display of numbers

### Fit standard curve using 4 parameter logistic regression ###
    print("Fitting standard curve")
    x = np.asarray(std_concs)

    std_curve1_ods = np.asarray(list(ods["std_curve1"].values()))
    std_curve2_ods = np.asarray(list(ods["std_curve2"].values()))

    y = (std_curve1_ods + std_curve2_ods) / 2.0

    # Initial guess for parameters
    p0 = [0, 1, 1, 1]

    # Fit equation using least squares optimization
    plsq = leastsq(residuals, p0, args=(y, x))

    # Plot results
    plt.plot(x, peval(x, plsq[0]))
    plt.plot(x, std_curve1_ods, '.', color='orange')
    plt.plot(x, std_curve2_ods, '.', color='orange')

    plt.xscale("log", basex=10)
    plt.title("Standard curve")
    plt.xlabel("Unit of standard")
    plt.ylabel("OD")

    fig_name = plate_id + ".png"
    fig_path = os.path.join("figs", fig_name)

    plt.savefig(fig_path)


### calculate output variables###
    print("Calculating concentrations")
    sample_means = {}
    sample_cv = {}
    sample_concs = {}
    pos_neg = {}

    for sample in ods.keys():
        if "sample" in sample:
            sample_ods = np.asarray(list(ods[sample].values()))
            mean = sum(sample_ods)/len(sample_ods)
            sample_concs[sample] = round(get_conc(mean, plsq[0]), 6)
            cv = variation(sample_ods, axis = 0)

            if sample_concs[sample] < std_concs[-1]:
                sample_concs[sample] = "BelowCurve"
            elif sample_concs[sample] > std_concs[0]:
                sample_concs[sample] = "AboveCurve"

            sample_means[sample] = round(mean, 3)
            sample_cv[sample] = round(cv, 2)

            if sample_means[sample].item() > cut_offs[antigen]:
                pos_neg[sample] = "Pos"
            else:
                pos_neg[sample] = "Neg"

    blk_ods = np.asarray(list(ods["blk"].values()))
    blk_mean = sum(blk_ods) / len(blk_ods)
    blk_cv = variation(blk_ods, axis = 0)

    pos_ods = np.asarray(list(ods["pos"].values()))
    pos_mean = sum(pos_ods) / len(pos_ods)
    pos_cv = variation(pos_ods, axis = 0)

    neg_ods = np.asarray(list(ods["neg"].values()))
    neg_mean = sum(neg_ods) / len(neg_ods)
    neg_cv = variation(neg_ods, axis = 0)

### Output to pdf file ###
    print("Generating html file")
    now = datetime.datetime.now()
    date = "%s-%s-%s" % (now.day, now.strftime("%b"), now.year)

    html_page = html % (plate_id,
                            date,
                            antigens[antigen],
                            fig_path,
                            round(blk_mean, 2),
                            round(blk_cv,2),

                            round(pos_mean, 2),
                            round(pos_cv, 2),

                            round(neg_mean, 2),
                            round(neg_cv, 2),

                            sample_dilution["sample01"].split("-")[0],
                                sample_means["sample01"],
                                sample_cv["sample01"],
                                sample_concs["sample01"],
                                pos_neg["sample01"],

                            sample_dilution["sample02"].split("-")[0],
                                sample_means["sample02"],
                                sample_cv["sample02"],
                                sample_concs["sample02"],
                                pos_neg["sample02"],

                            sample_dilution["sample03"].split("-")[0],
                                sample_means["sample03"],
                                sample_cv["sample03"],
                                sample_concs["sample03"],
                                pos_neg["sample03"],

                            sample_dilution["sample04"].split("-")[0],
                                sample_means["sample04"],
                                sample_cv["sample04"],
                                sample_concs["sample04"],
                                pos_neg["sample04"],

                            sample_dilution["sample05"].split("-")[0],
                                sample_means["sample05"],
                                sample_cv["sample05"],
                                sample_concs["sample05"],
                                pos_neg["sample05"],

                            sample_dilution["sample06"].split("-")[0],
                                sample_means["sample06"],
                                sample_cv["sample06"],
                                sample_concs["sample06"],
                                pos_neg["sample06"],

                            sample_dilution["sample07"].split("-")[0],
                                sample_means["sample07"],
                                sample_cv["sample07"],
                                sample_concs["sample07"],
                                pos_neg["sample07"],

                            sample_dilution["sample08"].split("-")[0],
                                sample_means["sample08"],
                                sample_cv["sample08"],
                                sample_concs["sample08"],
                                pos_neg["sample08"],

                            sample_dilution["sample09"].split("-")[0],
                                sample_means["sample09"],
                                sample_cv["sample09"],
                                sample_concs["sample09"],
                                pos_neg["sample09"],

                            sample_dilution["sample10"].split("-")[0],
                                sample_means["sample10"],
                                sample_cv["sample10"],
                                sample_concs["sample10"],
                                pos_neg["sample10"],

                            sample_dilution["sample11"].split("-")[0],
                                sample_means["sample11"],
                                sample_cv["sample11"],
                                sample_concs["sample11"],
                                pos_neg["sample11"],

                            sample_dilution["sample12"].split("-")[0],
                                sample_means["sample12"],
                                sample_cv["sample12"],
                                sample_concs["sample12"],
                                pos_neg["sample12"],

                            sample_dilution["sample13"].split("-")[0],
                                sample_means["sample13"],
                                sample_cv["sample13"],
                                sample_concs["sample13"],
                                pos_neg["sample13"],

                            sample_dilution["sample14"].split("-")[0],
                                sample_means["sample14"],
                                sample_cv["sample14"],
                                sample_concs["sample14"],
                                pos_neg["sample14"],

                            sample_dilution["sample15"].split("-")[0],
                                sample_means["sample15"],
                                sample_cv["sample15"],
                                sample_concs["sample15"],
                                pos_neg["sample15"],

                            sample_dilution["sample16"].split("-")[0],
                                sample_means["sample16"],
                                sample_cv["sample16"],
                                sample_concs["sample16"],
                                pos_neg["sample16"],

                            sample_dilution["sample17"].split("-")[0],
                                sample_means["sample17"],
                                sample_cv["sample17"],
                                sample_concs["sample17"],
                                pos_neg["sample17"],

                            sample_dilution["sample18"].split("-")[0],
                                sample_means["sample18"],
                                sample_cv["sample18"],
                                sample_concs["sample18"],
                                pos_neg["sample18"],

                            sample_dilution["sample19"].split("-")[0],
                                sample_means["sample19"],
                                sample_cv["sample19"],
                                sample_concs["sample19"],
                                pos_neg["sample19"],


                            sample_dilution["sample20"].split("-")[0],
                                sample_means["sample20"],
                                sample_cv["sample20"],
                                sample_concs["sample20"],
                                pos_neg["sample20"],

                            sample_dilution["sample21"].split("-")[0],
                                sample_means["sample21"],
                                sample_cv["sample21"],
                                sample_concs["sample21"],
                                pos_neg["sample21"],

                            sample_dilution["sample22"].split("-")[0],
                                sample_means["sample22"],
                                sample_cv["sample22"],
                                sample_concs["sample22"],
                                pos_neg["sample22"],

                            sample_dilution["sample23"].split("-")[0],
                                sample_means["sample23"],
                                sample_cv["sample23"],
                                sample_concs["sample23"],
                                pos_neg["sample23"],

                            sample_dilution["sample24"].split("-")[0],
                                sample_means["sample24"],
                                sample_cv["sample24"],
                                sample_concs["sample24"],
                                pos_neg["sample24"],

                            sample_dilution["sample25"].split("-")[0],
                                sample_means["sample25"],
                                sample_cv["sample25"],
                                sample_concs["sample25"],
                                pos_neg["sample25"],

                            sample_dilution["sample26"].split("-")[0],
                                sample_means["sample26"],
                                sample_cv["sample26"],
                                sample_concs["sample26"],
                                pos_neg["sample26"],

                            sample_dilution["sample27"].split("-")[0],
                                sample_means["sample27"],
                                sample_cv["sample27"],
                                sample_concs["sample27"],
                                pos_neg["sample27"],

                            sample_dilution["sample28"].split("-")[0],
                                sample_means["sample28"],
                                sample_cv["sample28"],
                                sample_concs["sample28"],
                                pos_neg["sample28"],

                            sample_dilution["sample29"].split("-")[0],
                                sample_means["sample29"],
                                sample_cv["sample29"],
                                sample_concs["sample29"],
                                pos_neg["sample29"],

                            sample_dilution["sample30"].split("-")[0],
                                sample_means["sample30"],
                                sample_cv["sample30"],
                                sample_concs["sample30"],
                                pos_neg["sample30"],

                            sample_dilution["sample31"].split("-")[0],
                                sample_means["sample31"],
                                sample_cv["sample31"],
                                sample_concs["sample31"],
                                pos_neg["sample31"],

                            sample_dilution["sample32"].split("-")[0],
                                sample_means["sample32"],
                                sample_cv["sample32"],
                                sample_concs["sample32"],
                                pos_neg["sample32"]
                            )

    html_file = plate_id + ".html"
    pdf_file = plate_id + ".pdf"

    with open(plate_id + ".html", 'w') as htmlfile:
        htmlfile.write(html_page)


    print("Converting html to pdf...")
    pdfkit.from_file(html_file, pdf_file)

    shutil.move(html_file, os.path.join("html_reports", html_file))

