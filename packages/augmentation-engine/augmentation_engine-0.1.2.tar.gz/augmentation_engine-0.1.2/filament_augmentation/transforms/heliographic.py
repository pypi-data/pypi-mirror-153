__author__ = "Shreejaa Talla"

from matplotlib.patches import Rectangle
import numpy as np
import math
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits


def update_header(header, pcorrect, bcorrect):
    sinrhomax = 0.997

    updated_header = dict()

    # naxis = header['NAXIS']
    x0 = header['CRPIX1']
    y0 = header['CRPIX2']
    p0 = header['SOLAR_P']
    b0 = header['SOLAR_B0']
    r0 = header['IMAGE_R0']
    pixsize = header['CDELT1']

    p0 = p0 + pcorrect
    b0 = b0 + bcorrect
    s0 = r0 * pixsize
    pixsize = pixsize * math.pi / (180 * 3600)
    sr = r0 * pixsize
    rsun = 6.96e8
    dsun = rsun / math.sin(sr)
    e0 = 0
    ellipse = 1

    radsol = r0 * math.cos(sr)
    rsqtest = (r0 ** 2) * (sinrhomax ** 2)
    sins0 = math.sin(sr)
    sinp0 = math.sin(math.radians(p0))
    cosp0 = math.cos(math.radians(p0))
    sinb0 = math.sin(math.radians(b0))
    cosb0 = math.cos(math.radians(b0))

    # image = image.transpose(Image.ROTATE_270)

    updated_header['x0'] = x0
    updated_header['y0'] = y0
    updated_header['p0'] = p0
    updated_header['s0'] = s0
    updated_header['b0'] = b0
    updated_header['r0'] = r0
    updated_header['pixsize'] = pixsize
    updated_header['dsun'] = dsun
    updated_header['radsol'] = radsol
    updated_header['sins0'] = sins0
    updated_header['sinp0'] = sinp0
    updated_header['cosp0'] = cosp0
    updated_header['sinb0'] = sinb0
    updated_header['cosb0'] = cosb0
    updated_header['rsqtest'] = rsqtest
    updated_header['px1'] = int(565.034947578632)
    updated_header['px2'] = int(1259.8227658512233)
    updated_header['px3'] = int(updated_header['px1'] + 177.12730903644547)
    updated_header['px4'] = int(updated_header['px2'] + 195.72041937094355)
    return updated_header


def pixel2latlon(header, pcorrect, bcorrect):
    """
    pcorrect - (artifically rotated, telescope) sun's rotation axes based on the center of solar disk.
    based on the line of sight.
    bcorrect - tilted rotation axes of sun.
    """
    nx = 2048
    updated_header = dict()
    ilat = np.empty((nx, nx))
    ilat[:] = np.nan
    ilon = np.empty((nx, nx))
    ilon[:] = np.nan
    x0 = header['x0']
    y0 = header['y0']
    rsqtest = header['rsqtest']
    radsol = header['radsol']
    sins0 = header['sins0']
    cosp0 = header['cosp0']
    sinb0 = header['sinb0']
    cosb0 = header['cosb0']
    sinp0 = header['sinp0']

    for i in range(nx): # Insead of nx add bounding boxes values instead of pixels
        for j in range(nx): # Insead of nx add bounding boxes values instead of pixels
            x = i - x0
            y = j - y0
            rhoi2 = x ** 2 + y ** 2
            if rhoi2 < rsqtest:
                rhoi = math.sqrt(rhoi2)
                p = radsol / sins0
                a = 1.00 + rhoi2 / (p * p)
                b = -2.00 * rhoi2 / p
                c = rhoi2 - radsol * radsol
                b24ac = b * b - 4.00 * a * c
                if b24ac > 0:
                    zp = (-b + math.sqrt(b24ac)) / (2 * a)
                    rhop = math.sqrt(radsol * radsol - zp * zp)
                    if (x * y) != 0:
                        xp = rhop * x / rhoi
                        yp = xp * y / x
                    elif x == 0:
                        xp = 0
                        if y < 0:
                            yp = -rhop
                        else:
                            yp = rhop
                    elif y == 0:
                        yp = 0
                        if x < 0:
                            xp = -rhop
                        else:
                            xp = rhop
                    xb = xp * cosp0 + yp * sinp0
                    yb = -xp * sinp0 + yp * cosp0
                    zb = zp
                    xs = xb
                    ys = yb * cosb0 + zb * sinb0
                    ilat[i, j] = math.asin(ys / radsol)
                    ilon[i, j] = math.asin(xs / (radsol * math.cos(ilat[i, j])))
    return ilat, ilon, updated_header


# def resize_image(image, bbox):
#     img1 = [[0]*2048]*2048
#     img1 = np.array(img1)
#     img1 = Image.fromarray(img1)
#     img1.paste(image, bbox)
#     return img1
#
# def reset_image(image):
#     image = np.asarray(image)
#     set_bw = set([225,0])
#     for i in range(len(image)):
#         x = set(image[i])
#         if len(x) <= 2:
#             np.delete(image,i,axis=0)
#     return image
#
#
#
def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf,  bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img

if __name__ == "__main__":
    """
    Full disk heliographic project
    """
    image_file = fits.open(r'D:\GSU_Assignments\Semester_2\DL\augmentation_engine\bbso_halph_fl_20150831_181839.fts')
    header = update_header(image_file[0].header, 0, 0)
    ilat, ilon, header = pixel2latlon(header, 0, 0)
    img = Image.open(r'D:\GSU_Assignments\2015\08\31\bbso_halph_fr_20150831_181839.jpg')
    # img = Image.open(
    #     r'D:\GSU_Assignments\Semester_2\DL\augmentation_engine_backup\evalutate_augmentation_engine\filament_images\L\2015083118183905.jpg')
    # img = resize_image(img, (565, 1259))
    img = img.transpose(Image.ROTATE_270)
    plt.pcolor(ilon, ilat, img, cmap='gray')
    # plt.axis('off')
    # img = fig2img(plt)
    # img = img.convert('L')
    # plt.imshow(img)
    # plt.plot(565, 1259, marker='*', color="red")
    # plt.plot(742, 1259, marker='*', color="red")
    # plt.plot(565, 1454, marker='*', color="red")
    # plt.plot(742, 1454, marker='*', color="red")
    # plt.plot(1026, 1024, marker='*', color="green")
    # image = reset_image(img)
    # plt.imshow(image,cmap="gray")
    plt.show()
    # img = np.array(img)
    # rgb = img[:, :, :3]
    # color = [246, 213, 139]  # Original value
    # black = [0, 0, 0, 255]
    # white = [255, 255, 255, 255]
    # mask = np.all(img == color, axis=-1)
    # img[mask] = white
    # new_im = Image.fromarray(img)
    # new_im.show()

