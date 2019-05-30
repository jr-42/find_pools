from PIL import Image
import sys
from functools import reduce
import numpy as np


class ImageSplitter:

    def __init__(self):
        pass

    @staticmethod
    def load_image(image):
        return Image.open("{}".format(image))

    @staticmethod
    def factors(n):
         return reduce(list.__add__,([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)) 

    @staticmethod
    def outofbounds(box,xs,ys):
        if box[2] > xs:
            box[2] = xs-1

        if box[3] > ys:
            box[3] = ys-1
        return box


    def howcut(self, image, nb_im_out):

        xs,ys = image.size
    

        facts = self.factors(nb_im_out)[-2:]

        if xs > ys:
            cutsx = max(facts) - 1
            cutsy = min(facts) - 1 

        if ys > xs:
            cutsx = min(facts) - 1
            cutsy = max(facts) - 1

        lenxp = round(xs/(cutsx-0.07*cutsx), 0)
        lenyp = round(ys/(cutsy-0.07*cutsy), 0)

        patch = np.array([0,0,lenxp,lenyp])


        return patch, cutsx, cutsy


    def cut(self, image, patch, cutsx, cutsy):

        xs,ys = image.size

        xt = list(np.linspace(0, xs, cutsx+1, endpoint=False))
        yt = list(np.linspace(0, ys, cutsy+1, endpoint=False))


        crops = [image.crop(self.outofbounds(patch + np.array([x, y, x, y]), xs, ys )) for x in xt for y in yt]

        return crops




    def run(self, root, image, nb_im_out = 10):

        if nb_im_out % 2 != 0:
            raise ValueError('Number of out images has to be even')

        im = self.load_image(root+image)

        patch, cutsx, cutsy = self.howcut(im, nb_im_out)
        crops = self.cut(im, patch, cutsx, cutsy)

        # names = []
        # for i,c in enumerate(crops):
        # 	c.save('data/edited/slices/image_{i}.png'.format(i=i))

        return crops