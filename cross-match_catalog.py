###########################################
# Cross-Match Fits Catalog                #
# Matheus J. Castro                       #
# Version 1.2                             #
# Last Modification: 07/10/2019           #
###########################################

import numpy as np
import matplotlib.pyplot as plt
import manage_catalog as mancat
import time

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


def find_index(data, elements):

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

    equal_objects = []
    tam = len(data[0])
    tam2 = list(range(len(data[1])))
    for i in range(tam):
        found = False
        x = 0
        j_list = []
        for j in tam2:
            check = check_equal(ar_list_1[i], dc_list_1[i], ar_list_2[j], dc_list_2[j])
            if check:
                j_list.append(j)
                found = True
            if found:
                x += 1
                if x >= 100:
                    break
        if found:
            result = []
            for j in j_list:
                result.append(check_equal(ar_list_1[i], dc_list_1[i], ar_list_2[j], dc_list_2[j],
                                          value=True))
            best = j_list[result.index(min(result))]
            equal_objects.append((i, best))
            tam2.remove(best)
        print("Load: {:.2f}%".format(((i+1)/tam)*100))
    print(equal_objects)
    print("Number of founded objects:", len(equal_objects))

    return equal_objects, ar, ind_ar, dc, ind_dc


def check_equal(n, m, x, y, threshold=3, value=False):
    # threshold in arcsecond
    # need to transform to degrees
    threshold = threshold / 60**2
    module = np.sqrt((n-x)**2 + (m-y)**2)

    if value:
        return module
    elif module <= threshold:
        return True
    else:
        return False


def read_index():
    name_csv = "Magnitudes_compared.csv"

    ar = "ALPHA_J2000"
    dc = "DELTA_J2000"

    ind_ar = elements[0].index(ar)
    ind_dc = elements[0].index(dc)

    loaded = np.loadtxt(name_csv, delimiter=",")

    equal_objects = []
    for i in range(len(loaded)):
        equal_objects.append((int(loaded[i][1]-1), int(loaded[i][2]-1)))

    return equal_objects, ar, ind_ar, dc, ind_dc


def execute_c():
    import ctypes

    c_lib = ctypes.cdll.LoadLibrary("./test.so")
    c_lib.main()


def read_c():
    name_csv = "saida.csv"

    ar = "ALPHA_J2000"
    dc = "DELTA_J2000"

    ind_ar = elements[0].index(ar)
    ind_dc = elements[0].index(dc)

    loaded = np.loadtxt(name_csv, delimiter=",")

    equal_objects = []
    for i in range(len(loaded)):
        equal_objects.append((int(loaded[i][0] - 1), int(loaded[i][1] - 1)))

    return equal_objects, ar, ind_ar, dc, ind_dc


def save_lists():
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

    lista = [(len(data[0]), len(data[1]))]

    if len(data[0]) >= len(data[1]):
        for i in range(len(data[0])):
            if i < len(data[1]):
                lista.append((ar_list_1[i], dc_list_1[i], ar_list_2[i], dc_list_2[i]))
            else:
                lista.append((ar_list_1[i], dc_list_1[i], 0, 0))
    else:
        for i in range(len(data[1])):
            if i < len(data[0]):
                lista.append((ar_list_1[i], dc_list_1[i], ar_list_2[i], dc_list_2[i]))
            else:
                lista.append((0, 0, ar_list_2[i], dc_list_2[i]))

    np.savetxt("entrada.csv", lista, fmt="%s", delimiter=",")


def get_mag(obj, ind_ar, ind_dc):
    global data

    mag = "MAG_AUTO"
    ind = elements[0].index(mag)

    mags = []

    for i in range(len(obj)):
        mags.append((data[0][obj[i][0]][ind], data[1][obj[i][1]][ind]))

    new_mags = []
    for i in range(len(mags)):
        new_mags.append(("{:d}".format(i+1), obj[i][0]+1, obj[i][1]+1, data[0][obj[i][0]][ind_ar],
                         data[0][obj[i][0]][ind_dc], mags[i][0], mags[i][1]))

    return mags, new_mags


def save_mags(listofmag, ar, dc):
    global data

    head = "Number, Number_1, Number_2, " + ar + ", " + dc + ", MAG_CAT_1, MAG_CAT_2"
    np.savetxt("Magnitudes_compared.csv", listofmag, header=head, fmt="%s", delimiter=",")


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
setup()
save_lists()
# objects, alpha, ind_alpha, delta, ind_delta = mancat.find_index(data, elements)
# objects, alpha, ind_alpha, delta, ind_delta = find_index()
# objects, alpha, ind_alpha, delta, ind_delta = read_index()
#execute_c()
objects, alpha, ind_alpha, delta, ind_delta = read_c()
mag_list, mag_pos_list = get_mag(objects, ind_alpha, ind_delta)
# save_mags(mag_pos_list, alpha, delta)
fim = time.time()
print("Time Python: ", fim - inicio)
plot_mags(mag_pos_list, alpha, delta)
# plot_selected(alpha, delta, ind_alpha, ind_delta)
