###########################################
# Cross-Match Fits Catalog                #
# Matheus J. Castro                       #
# Version 1.2                             #
# Last Modification: 07/10/2019           #
###########################################

import numpy as np
import matplotlib.pyplot as plt
import manage_catalog as mancat
import astropy.coordinates as coord
from astropy import units as u


###########################################
# Configure the global variables

catalog_1 = None
catalog_2 = None
elements = None
data = None

###########################################


def setup():
    # Call the global variables
    global catalog_1
    global catalog_2
    global elements
    global data

    # Configure all variables
    catalog_1 = mancat.cat_open('j02-20151112T005311-01_proc.proccat')
    catalog_2 = mancat.cat_open('j02-20151112T010354-01_proc.proccat')

    # info = mancat.get_info(catalog_2)[0]

    elements = (mancat.get_header(catalog_1)[0], mancat.get_header(catalog_2)[0])
    # elements of catalog 1 and 2

    if elements[0] != elements[1]:
        print("Error: Catalogs are different.")
        return -1

    data = (mancat.get_data(catalog_1), mancat.get_data(catalog_2))  # data of catalogs
    mancat.close(catalog_1)

    return 1


def find_index():
    global data

    ar = "ALPHA_J2000"
    dc = "DELTA_J2000"

    ind_ar = elements[0].index(ar)
    ind_dc = elements[0].index(dc)

    ar_list_1 = []
    dc_list_1 = []
    ar_list_2 = []
    dc_list_2 = []
    for i in range(len(data[0])):
        ar_list_1.append(data[0][i][ind_ar])
        dc_list_1.append(data[0][i][ind_dc])
    for i in range(len(data[1])):
        ar_list_2.append(data[1][i][ind_ar])
        dc_list_2.append(data[1][i][ind_dc])

    c = coord.SkyCoord(ar_list_2, dc_list_2, frame="icrs", unit="deg")
    catalog = coord.SkyCoord(ar_list_1, dc_list_1, frame="icrs", unit="deg")
    idx, d2d, d3d = c.match_to_catalog_sky(catalog,  nthneighbor=1)

    print("Number of founded objects:", len(idx))
    print(idx)
    list1 = []
    for i in range(len(data[1])):
        list1.append((idx[i], data[1][i][0]-1))
    print(list1)
    return list1, ar, ind_ar, dc, ind_dc


def check_equal(n, m, threshold=3):
    # threshold in arcsecond
    # need to transform to degrees
    threshold = threshold / 60**2

    if n - threshold <= m <= n + threshold:
        return True
    else:
        return False


def get_mag(obj, ind_ar, ind_dc):
    global data

    mag = "MAG_AUTO"
    ind = elements[0].index(mag)

    mags = []

    for i in range(len(obj)):
        mags.append((data[0][obj[i][0]][ind], data[1][obj[i][1]][ind]))

    new_mags = []
    for i in range(len(mags)):
        new_mags.append(("{:d}".format(i+1), obj[i][0]+1, obj[i][1]+1, data[0][obj[i][0]][ind_ar], data[0][obj[i][0]][ind_dc], mags[i][0], mags[i][1]))

    return mags, new_mags


def save_mags(listofmag, ar, dc):
    global data

    head = "Number, Number_1, Number_2, " + ar + ", " + dc + ", MAG_CAT_1, MAG_CAT_2"
    # np.savetxt("Magnitudes_compared.csv", listofmag, header=head, fmt="%s", delimiter=",")


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

    fmt = "png"
    # plt.savefig("Plot_Variation_of_Mags.{}".format(fmt), format=fmt)
    plt.show()


setup()
objects, alpha, ind_alpha, delta, ind_delta = find_index()
mag_list, mag_pos_list = get_mag(objects, ind_alpha, ind_delta)
save_mags(mag_pos_list, alpha, delta)
plot_mags(mag_pos_list, alpha, delta)
