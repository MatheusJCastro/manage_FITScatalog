###########################################
# Cross-Match Fits Catalog                #
# Matheus J. Castro                       #
# Version 6.4                             #
# Last Modification: 18/10/2019           #
###########################################

import numpy as np
import matplotlib.pyplot as plt
import manage_catalog as mancat
import time


def plot_selected(ar, dc, ind_ar, ind_dc):
    x_position_1 = []
    y_position_1 = []
    x_position_1_c = []
    y_position_1_c = []
    x_position_2 = []
    y_position_2 = []

    cat1_eu = [8186-1]
    cat1_cat = [8199-1]
    cat2 = [7713-1]

    # cat1 = [1392, 2703, 5717]
    # cat2 = [829, 1626, 3345]

    for i in cat1_eu:
        x_position_1.append(data[0][i][ind_ar])
        y_position_1.append(data[0][i][ind_dc])
    for i in cat1_cat:
        x_position_1_c.append(data[0][i][ind_ar])
        y_position_1_c.append(data[0][i][ind_dc])
    for i in cat2:
        x_position_2.append(data[1][i][ind_ar])
        y_position_2.append(data[1][i][ind_dc])

    error = np.asarray([3/(60**2)]*len(y_position_2))

    plt.figure(figsize=(5, 5))
    plt.xlabel(ar)
    plt.ylabel(dc)
    plt.xlim(56, 57.8)
    plt.ylim(23.3, 24.9)
    plt.title("{} and {}".format(ar, dc))
    # plt.errorbar(x_position_1, y_position_1, yerr=error, xerr=error, fmt="none")
    plt.errorbar(x_position_2, y_position_2, yerr=error, xerr=error, fmt="none")
    plt.plot(x_position_1, y_position_1, ".", markersize=5, color="black")
    plt.plot(x_position_1_c, y_position_1_c, ".", markersize=5, color="green")
    plt.plot(x_position_2, y_position_2, ".", markersize=5, color="blue")

    fmt = "png"
    plt.savefig("Plot_Mags.{}".format(fmt), format=fmt)
    plt.show()


def plot_mags(listofmag, ar, dc):
    x_axis = "MAGS of CAT 1"
    y_axis = "MAGS of CAT 2"

    x_points = []
    y_points = []
    x_position = []
    y_position = []
    for i in range(len(listofmag)):
        if listofmag[i][5] <= 30 and listofmag[i][6] <= 30:
            x_points.append(listofmag[i][5])
            y_points.append(listofmag[i][6])
        x_position.append(listofmag[i][3])
        y_position.append(listofmag[i][4])

    xmax = int(max(x_points)) + 1
    xmin = int(min(x_points)) - 1
    ymax = int(max(y_points)) + 1
    ymin = int(min(y_points)) - 1

    if xmax < ymax:
        xmax = ymax
    if xmin > ymin:
        xmin = ymin

    plt.figure(figsize=(12, 5))

    plt.subplot(121)
    plt.xlim(xmin, xmax)
    plt.ylim(xmin, xmax)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title("{} and {}".format(x_axis, y_axis))
    plt.plot(x_points, y_points, ".", markersize=5)
    plt.plot([xmin, xmax], [xmin, xmax], "-", markersize=5)

    plt.subplot(122)
    plt.xlabel(ar)
    plt.ylabel(dc)
    plt.title("{} and {}".format(ar, dc))
    plt.plot(x_position, y_position, ".", markersize=5)

    # fmt = "png"
    # plt.savefig("Plot_Variation_of_Mags.{}".format(fmt), format=fmt)
    plt.show()


inicio = time.time()

cat_name_1 = 'j02-20151112T005311-01_proc.proccat'
cat_name_2 = 'j02-20151112T010354-01_proc.proccat'
csv_to_read = "Magnitudes_compared.csv"
right_ascension_column = "ALPHA_J2000"
declination_column = "DELTA_J2000"
c_code_name = "test.so"
mag_to_use = "MAG_AUTO"

data, elements = mancat.setup_catalog(cat_name_1, cat_name_2)

ind_alpha = elements[0].index(right_ascension_column)
ind_delta = elements[0].index(declination_column)

mancat.save_all_obj(data, ind_alpha, ind_delta)
# objects = mancat.find_index(data, ind_alpha, ind_delta)
# objects = mancat.read_cross_match_csv(elements, csv_to_read, right_ascension_column, declination_column)
mancat.execute_c(c_code_name)
objects = mancat.read_c()
mag_pos_list = mancat.get_mag(data, elements, mag_to_use, objects, ind_alpha, ind_delta)[1]
# mancat.save_cross_match_csv(mag_pos_list, right_ascension_column, declination_column)

fim = time.time()
print("Time Python: ", fim - inicio)

plot_mags(mag_pos_list, right_ascension_column, declination_column)
# plot_selected(alpha, delta, ind_alpha, ind_delta)
