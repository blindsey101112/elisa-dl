import os
import sys
import shutil
from openpyxl import load_workbook
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import pdfkit
import datetime

'''
Credit to https://people.duke.edu/~ccc14/pcfb/analysis.html for the code to fit 
the 4 parameter logistic regression for the standard curve
'''

def get_ods(file):
    wb = load_workbook(file)
    od_ws = wb["Photometric1"]
    ods={}
    std_curve1 = {}
    for cell in od_ws["B23":"M23"][0]:
        std_curve1[cell.coordinate] = cell.value
    ods["std_curve1"] = std_curve1
    std_curve2 = {}
    for cell in od_ws["B24":"M24"][0]:
        std_curve2[cell.coordinate] = cell.value
    ods["std_curve2"] = std_curve2
    pos = {}
    for cell in od_ws["K20":"M20"][0]:
        pos[cell.coordinate] = cell.value
    ods["pos"] = pos
    blk = {}
    for cell in od_ws["K21":"M21"][0]:
        blk[cell.coordinate] = cell.value
    for cell in od_ws["K22":"M22"][0]:
        blk[cell.coordinate] = cell.value
    ods["blk"] =  blk
    sample01 = {}
    for cell in od_ws["B17":"D17"][0]:
        sample01[cell.coordinate] = cell.value
    ods["sample01"] = sample01
    sample02 = {}
    for cell in od_ws["B18":"D18"][0]:
        sample02[cell.coordinate] = cell.value
    ods["sample02"] = sample02
    sample03 = {}
    for cell in od_ws["B19":"D19"][0]:
        sample03[cell.coordinate] = cell.value
    ods["sample03"] = sample03
    sample04 = {}
    for cell in od_ws["B20":"D20"][0]:
        sample04[cell.coordinate] = cell.value
    ods["sample04"] = sample04
    sample05 = {}
    for cell in od_ws["B21":"D21"][0]:
        sample05[cell.coordinate] = cell.value
    ods["sample05"] = sample05
    sample06 = {}
    for cell in od_ws["B22":"D22"][0]:
        sample06[cell.coordinate] = cell.value
    ods["sample06"] = sample06
    sample07 = {}
    for cell in od_ws["E17":"G17"][0]:
        sample07[cell.coordinate] = cell.value
    ods["sample07"] = sample07
    sample08 = {}
    for cell in od_ws["E18":"G18"][0]:
        sample08[cell.coordinate] = cell.value
    ods["sample08"] = sample08
    sample09 = {}
    for cell in od_ws["E19":"G19"][0]:
        sample09[cell.coordinate] = cell.value
    ods["sample09"] = sample09
    sample10 = {}
    for cell in od_ws["E20":"G20"][0]:
        sample10[cell.coordinate] = cell.value
    ods["sample10"] = sample10
    sample11 = {}
    for cell in od_ws["E21":"G21"][0]:
        sample11[cell.coordinate] = cell.value
    ods["sample11"] = sample11
    sample12 = {}
    for cell in od_ws["E22":"G22"][0]:
        sample12[cell.coordinate] = cell.value
    ods["sample12"] = sample12
    sample13 = {}
    for cell in od_ws["H17":"J17"][0]:
        sample13[cell.coordinate] = cell.value
    ods["sample13"] = sample13
    sample14 = {}
    for cell in od_ws["H18":"J18"][0]:
        sample14[cell.coordinate] = cell.value
    ods["sample14"] = sample14
    sample15 = {}
    for cell in od_ws["H19":"J19"][0]:
        sample15[cell.coordinate] = cell.value
    ods["sample15"] = sample15
    sample16 = {}
    for cell in od_ws["H20":"J20"][0]:
        sample16[cell.coordinate] = cell.value
    ods["sample16"] = sample16
    sample17 = {}
    for cell in od_ws["H21":"J21"][0]:
        sample17[cell.coordinate] = cell.value
    ods["sample17"] = sample17
    sample18 = {}
    for cell in od_ws["H22":"J22"][0]:
        sample18[cell.coordinate] = cell.value
    ods["sample18"] = sample18
    sample19 = {}
    for cell in od_ws["K17":"M17"][0]:
        sample19[cell.coordinate] = cell.value
    ods["sample19"] = sample19
    sample20 = {}
    for cell in od_ws["K18":"M18"][0]:
        sample20[cell.coordinate] = cell.value
    ods["sample20"] = sample20
    sample21 = {}
    for cell in od_ws["K19":"M19"][0]:
        sample21[cell.coordinate] = cell.value
    ods["sample21"] = sample21
    return ods

def get_samples(file):
    wb = load_workbook(file)
    sample_ws = wb["PlatePlan"]
    sample_dilution = {"sample01" : sample_ws["B17"].value,
               "sample02" : sample_ws["B18"].value,
               "sample03" : sample_ws["B19"].value,
               "sample04" : sample_ws["B20"].value,
               "sample05" : sample_ws["B21"].value,
               "sample06": sample_ws["B22"].value,
               "sample07": sample_ws["E17"].value,
               "sample08": sample_ws["E18"].value,
               "sample09": sample_ws["E19"].value,
               "sample10": sample_ws["E20"].value,
               "sample11": sample_ws["E21"].value,
               "sample12": sample_ws["E22"].value,
               "sample13": sample_ws["H17"].value,
               "sample14": sample_ws["H18"].value,
               "sample15": sample_ws["H19"].value,
               "sample16": sample_ws["H20"].value,
               "sample17": sample_ws["H21"].value,
               "sample18": sample_ws["H22"].value,
               "sample19": sample_ws["K17"].value,
               "sample20": sample_ws["K18"].value,
               "sample21": sample_ws["K19"].value,
               }
    return sample_dilution

def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    asym_dif = A-D
    con_inflec = x/C
    gradiant_power = np.sign(con_inflec) * (np.abs(con_inflec)) ** B
    equation = (asym_dif/(1.0 + gradiant_power) + D)
    return equation

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)


std_concs = [0.4, 0.200, 0.100, 0.0500, 0.0250, 0.0125, 0.00625, 0.003125, 0.0015625, 0.0007812, 0.0003916, 0.0001958]


if __name__ == "__main__":
    plate_id = sys.argv[1]
    plateplan_file = plate_id + "-pplan.xlsx"
    platereader_file = plate_id + "-preader.xlsx"
    ods = get_ods(platereader_file)
    sample_dilution = get_samples(plateplan_file)


### Fit standard curve using 4 parameter logistic regression ###
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

    plt.xscale("log", basex=2)
    plt.title("Standard curve")
    plt.xlabel("Concentration of standard")
    plt.ylabel("OD")

    fig_name = plate_id + ".png"
    fig_path = os.path.join("figs", fig_name)

    plt.savefig(fig_path)


### sample concentrations ###
    sample_means = {}
    sample_concs = {}

    for sample in ods.keys():
        if "sample" in sample:
            sample_ods = np.asarray(list(ods[sample].values()))
            mean = sum(sample_ods)/3
            sample_means[sample] = sum(sample_ods)/3
            sample_concs[sample] = peval(mean, plsq[0])


### Output to pdf file ###

    now = datetime.datetime.now()
    date = "%s-%s-%s" % (now.day, now.strftime("%b"), now.year)

    html_template = """
    <html>
    <body>
    
    <h1> Plate Report - %s</h1>
    
    <p> Report generated on %s<p>
    
    <img src="%s" alt="Standard curve" />
    
    <p> sample01: %s</p>
    <p> sample02: %s</p>
    <p> sample03: %s</p>
    
    </body>
    </html>
    
    """

    html = html_template % (plate_id, date, fig_path,
                            sample_concs["sample01"],
                            sample_concs["sample02"],
                            sample_concs["sample03"]
                            )

    html_file = plate_id + ".html"
    pdf_file = plate_id + ".pdf"

    with open(plate_id + ".html", 'w') as htmlfile:
        htmlfile.write(html)

    pdfkit.from_file(html_file, pdf_file)

    shutil.move(html_file, os.path.join("html_reports", html_file))

