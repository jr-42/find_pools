from findapool import FindAPool
import sys
import os

from fire import Fire


class Main:

    folder = str(sys.argv[1])

    try:
        sys.argv[2]
        thres = sys.argv[2]
        h1 = thres[0]
        h2 = thres[1]
        s = thres[2]
        v = thres[3]
    
    except IndexError:
        h1, h2, s, v = 205, 140, 20, 65

    print('----')
    print('hsv criteria : ')
    print('{} <= h <= {}'.format(h2, h1))
    print('s >= {}'.format(s))
    print('v >= {}'.format(v))
    print('----')

    images = os.listdir(folder)
    images = [i for i in images if (i[-3:] == 'png')]

    print('----')

    print('List of images in {}:'.format(folder), images)

    print('----')

    for i, image in enumerate(images):
        print("Running FindAPool on the image '{}'".format(image))
        ci, pi, nbpix, nbpool = FindAPool().run(folder + image, h1=h1, h2=h2,
                                                s=s, v=v,
                                                clust_algo='meanshift',
                                                quantile=0.003)
        print('{} pixels match the above criteria'.format(nbpix))
        print('{} pools found on the image'.format(nbpool))
        ci.save('results/' + str(i) + '_pixel_image_' + str(image))
        pi.save('results/' + str(i) + '_pool_image_' + str(image))
        print('****')

    print('****')
    print('Finished. Images with swimming pools saved in results')
    print('****')

def piscine_find_entry_point():
    Fire(Main)
