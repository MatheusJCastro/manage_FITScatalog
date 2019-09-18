###########################################
# Plot Fits Catalog                       #
# Matheus J. Castro                       #
# Version 2.1                             #
# Last Modification: 17/09/2019           #
###########################################

import numpy as np
import matplotlib.pyplot as plt
import manage_catalog as mancat

catalog = mancat.cat_open('j02-20170711T001143-01_proc.proccat')

# save catalog in a csv file
# mancat.save_catalog(catalog, mancat.get_info(catalog)[1], mancat.get_header(catalog)[1])

# get info about catalog
# check the extension do you want to use, the default is 2.
# info = mancat.get_info(catalog)[0]

elements = mancat.get_header(catalog)[0]  # elements of catalog
data = mancat.get_data(catalog)  # data of catalog
mancat.close(catalog)

choose = True
if choose:
    print("Available options for plot:\n|", end="")
    for i in range(len(elements)):
        print(" {:{}}|".format(elements[i], len(max(elements, key=len))+1), end="")
        if (i+1)%7 == 0:
            print("\n|", end="")
    print("")
    x_axis, y_axis = input("Enter chosen options separated by spaces: ").upper().split()
else:
    x_axis = "ALPHA_J2000"
    y_axis = "DELTA_J2000"
    # x_axis = "MAG_AUTO"
    # y_axis = "MAGERR_AUTO"

fmt = "png"
x_column = elements.index(x_axis)
y_column = elements.index(y_axis)

x_points = []
y_points = []
for i in range(len(data)):
    x_points.append(data[i][x_column])
    y_points.append(data[i][y_column])

plt.figure(figsize=(5, 5))
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.title("{} and {}".format(x_axis, y_axis))
plt.plot(x_points, y_points, ".", markersize=1)
plt.savefig("Plot_{}_{}.{}".format(x_axis, y_axis, fmt), format=fmt)

plt.show()
