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
from matplotlib.colors import LogNorm
from astropy.visualization import ZScaleInterval, ImageNormalize, MinMaxInterval

image = 'm31_proc.fits'  # name for your fits file
image_file = fits.open(image)
image_data = image_file[0].data  # get the extension 0 of your fits
                                 # normally, the image is on first extension
image_mask = image_file[1].data  # get the extension 1, on my case, the mask of pixel for data reduction

head = image_file[0].header["DATE"]  # example of print one data from fits header
print(head)
head = np.array(repr(image_file[0].header))  # example of print all header
print(head)
print(type(head))
np.savetxt("Header_{}.txt".format(image[:-5]), [head], fmt="%s")  # save header on a .txt file
print(image_file.info())  # print some useful information about your fits

image_file.close()

print('Min:', np.min(image_data))    # min of image
print('Max:', np.max(image_data))    # max of image
print('Mean:', np.mean(image_data))  # mean of image
print('Stdev:', np.std(image_data))  # standard deviation of image
                                     # from numpy

plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.imshow(image_data, cmap='gray', origin='lower')  # the primary image, by default, is set no MinMaxInterval
plt.title("Primary")
# plt.colorbar()  # if you want to add a color bar on your subplot

# OPTIONS FOR DISPLAY IMAGES
# norm=LogNorm() --> display in a logarithmic color scale
# norm=ImageNormalize(image_data, interval=ZScaleInterval()) --> display in zscale

plt.subplot(132)
plt.imshow(image_data, cmap='gray', origin='lower', norm=ImageNormalize(image_data, interval=ZScaleInterval()))
            # print the zscale image
plt.title("Zscale")

plt.subplot(133)
plt.imshow(image_mask, cmap='gray', origin='lower')  # print the pixel mask
plt.title("Masked Pixels")

plt.show()
