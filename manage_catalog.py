###########################################
# Display .FITS file                      #
# Matheus J. Castro                       #
# Version 2.0                             #
# Last Modification: 09/09/2019           #
###########################################

# learn more at: http://learn.astropy.org/FITS-images.html
# example for ZScale: https://qiita.com/phyblas/items/87667c250b29e195f7fb

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

catalog = 'j02-20170711T001143-01_proc.proccat'  # name for your fits file
catalog_file = fits.open(catalog)

info = catalog_file.info(0)
size = len(info)

#print(catalog_file.info())

ext_names = []
for i in range(size):
    ext_names.append(info[i][1])

#for i in range(1, size-1):

header = np.array(repr(catalog_file[2].header))
np.savetxt("Header.txt", [header], fmt="%s")

dic = np.array(catalog_file[2].header)
header = catalog_file[2].header
element = []
for i in range(len(dic)):
    if "TTYPE" in dic[i]:
        element.append(header[i])
#print([element])

np.savetxt("Data.txt", [element], fmt="%s", delimiter=",")

l = len(catalog_file[2].data[0])
data = catalog_file[2].data[0]
print(data)

#data = np.array(repr(catalog_file[2].data))
np.savetxt("Extension{}_{}.csv".format(2, ext_names[2]), data, fmt="%s", delimiter=",")

catalog_file.close()
