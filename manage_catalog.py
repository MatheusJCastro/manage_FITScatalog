###########################################
# Manage Fits Catalog                     #
# Matheus J. Castro                       #
# Version 2.4                             #
# Last Modification: 17/09/2019           #
###########################################

import numpy as np
from astropy.io import fits


######################################################################################


def save_catalog(catalog_file, ext_names, str_element):
    data = get_data(catalog_file)  # Get the data
    col = len(data[0])  # length of columns
    line = len(data)  # length of lines

    # create a list new_data of all the data and reformulating the ndarrays found inside data array
    # useful for save in csv file
    new_data = []
    for i in range(line):
        for j in range(col):
            if type(data[i][j]) == np.ndarray:
                array = ""
                for k in range(len(data[i][j])):
                    array = array + " " + repr(data[i][j][k])
                array = array[1:]
                new_data.append(array)
            else:
                new_data.append(data[i][j])
    new_data = np.asarray(new_data).reshape(line, col)

    np.savetxt("Extension{}_{}.csv".format(2, ext_names[2]), new_data, header=str_element, fmt="%s", delimiter=",")


######################################################################################


def get_header(catalog_file, save=False, extension=2):
    if save:
        # save the header of extension of interest
        header = np.array(repr(catalog_file[extension].header))
        np.savetxt("Header.txt", [header], fmt="%s")

    # create the elemente list with names of the collumns of the catalog
    dic = np.array(catalog_file[extension].header)
    header = catalog_file[extension].header
    element = []
    for i in range(len(dic)):
        if "TTYPE" in dic[i]:
            element.append(header[i])

    # transfor element array into a string of the elements
    str_element = ""
    for i in range(len(element)):
        str_element = str_element + "," + repr(element[i])
    str_element = str_element[1:].replace("'", "")
    # print(str_element)

    return element, str_element
    # return elements of the header on first variable
    # and the string of it on the second variable


######################################################################################


def get_data(catalog_file, extension=2):
    # Save the data
    data = catalog_file[extension].data

    return data


######################################################################################


def get_info(catalog_file):
    # Get information about names of extension of the .proccat
    info = catalog_file.info(0)
    size = len(info)

    # print(catalog_file.info())

    # Create a list of the names of the extensions
    ext_names = []
    for i in range(size):
        ext_names.append(info[i][1])

    info = catalog_file.info()

    return info, ext_names


######################################################################################


def cat_open(cat_name):
    # Open the catalog
    catalog_file = fits.open(cat_name)

    return catalog_file


######################################################################################


def close(catalog_file):
    catalog_file.close()


######################################################################################


if __name__ == '__main__':
    cat_open()
