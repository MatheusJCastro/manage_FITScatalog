###########################################
# Cross-Match Fits Catalog                #
# Matheus J. Castro                       #
# Version 1.0                             #
# Last Modification: 07/10/2019           #
###########################################

import numpy as np
import matplotlib.pyplot as plt
import manage_catalog as mancat

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
    # print(ind_ar, ind_dc)

    equal_objects = []
    tam = len(data[0])
    tam2 = list(range(len(data[1])))
    for i in range(tam):
        for j in tam2:
            ar_check = check_equal(data[0][i][ind_ar], data[1][j][ind_ar])
            dc_check = check_equal(data[0][i][ind_dc], data[1][j][ind_dc])
            if ar_check and dc_check:
                equal_objects.append((i, j))
                tam2.remove(tam2[equal_objects[len(equal_objects)-1][1]])
                break
        print("Load: {:.3f}%".format((i/tam)*100))
        print(len(tam2))

    print(equal_objects)


def check_equal(n, m, threshold=1):
    # threshold in arcsecond
    # need to transform to degrees
    threshold = threshold / 60**2

    if n - threshold <= m <= n + threshold:
        return True
    else:
        return False


x = setup()
find_index()
