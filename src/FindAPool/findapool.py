# Import
import numpy as np
import colorsys
from PIL import Image, ImageDraw
import pandas as pd
from sklearn.cluster import MeanShift


class FindAPool:

    def __init__(self):
        pass

    @staticmethod
    def load_image(image):
        return Image.open("{}".format(image))

    @staticmethod
    def image_rgb(image):
        ''' Get the RGB of each pixel of the image'''
        r = [i / 255.0 for i in image.getdata(0)]
        g = [i / 255.0 for i in image.getdata(1)]
        b = [i / 255.0 for i in image.getdata(2)]
        return pd.DataFrame({'r': r, 'g': g, 'b': b})

    @staticmethod
    def rgb_2_hsv(dataframe):
        ''' Convert the RGB to HSV '''
        hsv = np.array([colorsys.rgb_to_hsv(x, y, z) for x, y, z
                       in zip(dataframe.r, dataframe.g, dataframe.b)])
        df = pd.DataFrame(data=hsv, columns=['h', 's', 'v'])
        return df

    @staticmethod
    def find_pix(image, dataframe, h1, h2, s, v):
        ''' Select the pixels who fit the criteria'''
        mask = (dataframe['v'] > v / 100.0) & (dataframe['s'] > s / 100.0) & \
               (dataframe['h'] > h2 / 360.0) & (dataframe['h'] < h1 / 360.0)
        xs, ys = image.size
        maskbool = mask.values.reshape(ys, xs)
        return maskbool, np.argwhere(maskbool)

    @staticmethod
    def colour_pix(image, maskbool):
        ''' Colour the good pixels in red'''
        new_image = image.copy()
        mask = Image.fromarray(np.uint8(255 * maskbool))
        new_image.paste('red', mask=mask)

        return new_image

    @staticmethod
    def cluster_pixels(piscine_locs,
                       clust_algo='meanshift', quantile=0.003):
        ''' Function to group the pixels into swimming pools'''

        if clust_algo == 'meanshift':
            # bandwidth = estimate_bandwidth(piscine_locs, quantile=quantile)
            # if bandwidth == 0:
            #   while bandwidth ==0:
            #       quantile = quantile + 0.001
            #       bandwidth = estimate_bandwidth(piscine_locs,
            #                                      quantile=quantile)
            bandwidth = 6

            ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
            ms.fit(piscine_locs)
            labels = ms.labels_
            cluster_centers = ms.cluster_centers_

            labels_unique = np.unique(labels)
            n_clusters_ = len(labels_unique)

            return n_clusters_, cluster_centers

    @staticmethod
    def draw_pisc(image, clusters):
        ''' Draw circles on'''
        imc = image.copy()
        draw = ImageDraw.Draw(imc)
        r = 2
        for t in clusters:
            draw.ellipse((int(t[1]) - r, int(t[0]) - r, int(t[1]) + r,
                         int(t[0]) + r), fill=(255, 255, 255, 255))

        return imc

    def run(self, image, h1=205, h2=140, s=20, v=65,
            clust_algo='meanshift', quantile=0.003):

        im = self.load_image(image)
        print(im.size)
        rgb_df = self.image_rgb(im)
        hsv_df = self.rgb_2_hsv(rgb_df)
        maskbool, piscine_locs = self.find_pix(im, hsv_df, h1, h2, s, v)
        coloredim = self.colour_pix(im, maskbool)

        nclusts, ccents = self.cluster_pixels(piscine_locs, clust_algo,
                                              quantile)
        piscim = self.draw_pisc(coloredim, ccents)

        return coloredim, piscim, len(piscine_locs), nclusts
