import numpy as np
import math
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from astropy.io import fits

def update_header(header, pcorrect, bcorrect):
    sinrhomax = 0.997

    updated_header = dict()
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

# def resize_image(image, bbox):
#     img1 = [[22]*2048]*2048
#     img1 = np.array(img1)
#     img1 = Image.fromarray(img1)
#     img1.paste(image, bbox)
#     return img1


def latlon2pixel(lon, lat, image, header):
    # image = np.array(image)
    size = len(lon)
    vmap = np.zeros((size, size))
    for i in range(len(lon)):# 1000 1250
        for j in range(len(lon[0])): # 700 900
            theta = lat[i][j]
            phi = lon[i][j]

            sintheta = math.sin(theta)
            costheta = math.cos(theta)
            sinphi = math.sin(phi)
            cosphi = math.cos(phi)

            radsol = header['radsol']
            xs = radsol * sinphi * costheta
            ys = radsol * sintheta
            zs = radsol * cosphi * costheta

            xb = xs
            yb = header['cosb0'] * ys - header['sinb0'] * zs
            zb = header['cosb0'] * zs + header['sinb0'] * ys

            xp = header['cosp0'] * xb - header['sinp0'] * yb
            yp = header['cosp0'] * yb + header['sinp0'] * xb
            zp = zb
            rhoi = 1
            zpmin = header['radsol'] * header['sins0']
            if zp > zpmin:
                rhop = math.sqrt(xp ** 2 + yp ** 2)
                thetap = 0
                if rhop > 0.1:
                    thetap = np.arctan2(yp, xp)
                rhoi = rhop * (1.0 + zp / (header['radsol'] / header['sins0'] - zp))
                x = rhoi * math.cos(thetap)
                y = rhoi * math.sin(thetap)
                lambda_ = math.asin(rhop / header['radsol'])
                s = math.atan(rhoi * header['sins0'] / header['radsol'])

                xi = header['x0'] + x
                yi = header['y0'] + y

                radsq = (xi - header['x0']) * (xi - header['x0']) + (yi - header['y0']) * (yi - header['y0'])

                if radsq < header['rsqtest']:
                    ix = math.floor(xi)
                    iy = math.floor(yi)
                    dx = xi - ix
                    dy = yi - iy
                    data = image[ix - 2:ix + 2, iy - 2:iy + 2]
                    dx2 = dx ** 2
                    dx3 = dx ** 3
                    dy2 = dy ** 2
                    dy3 = dy ** 3
                    wx = np.zeros((4, 4))
                    wx1 = -0.50 * dx + dx2 - 0.50 * dx3
                    wx2 = 1.0 - 2.50 * dx2 + 1.50 * dx3
                    wx3 = 0.50 * dx + 2.0 * dx2 - 1.50 * dx3
                    wx4 = -0.50 * dx2 + 0.50 * dx3
                    # print(wx1,wx2,wx3,wx4)
                    wx[0:4, 0] = [wx1, wx2, wx3, wx4]
                    wx[0:4, 1] = wx[0:4, 0]
                    wx[0:4, 2] = wx[0:4, 0]
                    wx[0:4, 3] = wx[0:4, 0]

                    wy = np.zeros((4, 4))
                    wy[0, 0:4] = [(-0.50 * dy + dy2 - 0.50 * dy3), (1.0 - 2.50 * dy2 + 1.50 * dy3),
                                  (0.50 * dy + 2.0 * dy2 - 1.50 * dy3), (-0.50 * dy2 + 0.50 * dy3)]
                    wy[1, 0:4] = wy[0, 0:4]
                    wy[2, 0:4] = wy[0, 0:4]
                    wy[3, 0:4] = wy[0, 0:4]

                    weight = np.matmul(wx,wy)
                    # sum_w = sum(sum(weight*data))
                    vmap[i, j] = sum(sum(weight*data)) / 4
                else:
                    vmap[i, j] = np.nan

            else:
                vmap[i, j] = np.nan

    return vmap

def lat_lon(pixel):
    R = 6.96
    xmin = - math.pi * R
    xmax = math.pi * R
    x = np.linspace(xmin, xmax, pixel)
    dx = x[1] - x[0]
    dy = 1.3 * dx
    x = np.arange(-(pixel/4) * dx + dx / 2, (pixel/4) * dx - dx / 2 + dx, dx)
    y = np.arange(-(pixel/4) * dy + dy / 2, (pixel/4) * dy - dy / 2 + dy, dy)
    [x, y] = np.meshgrid(x, y)
    lon = x / R
    lat = 2 * np.arctan(np.exp(y / R)) - math.pi / 2
    return lon, lat

# def remove_blackbg(image):
if __name__ == "__main__":
    image_file = fits.open(r'D:\GSU_Assignments\Semester_2\DL\augmentation_engine\bbso_halph_fl_20150831_181839.fts')
    header = update_header(image_file[0].header, 0, 0)
    # img = Image.open(r'D:\GSU_Assignments\Semester_2\DL\augmentation_engine_backup\evalutate_augmentation_engine\filament_images\L\2015083118183905.jpg')
    # img = resize_image(img, (565, 1259))
    # img.show()
    img = Image.open(r'D:\GSU_Assignments\2015\08\31\bbso_halph_fr_20150831_181839.jpg')
    image = np.asarray(img)
    lon, lat = lat_lon(4096)
    vmap = latlon2pixel(lon, lat, image, header)
    vmap = np.flipud(vmap)
    vmap = np.fliplr(vmap)
    plt.imshow(vmap, cmap='gray')
    plt.title("Mercator")
    plt.show()
