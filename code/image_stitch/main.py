import os
import cv2 as cv
import helper

'''Inspiration for this stitching algorithm taken from github.com/lukasalexanderweber'''

imgs = ['../../data/test1.jpg', '../../data/test2.jpg']
for i, x in enumerate(imgs):
    imgs[i] = cv.imread(x)
while True:

    for i, img in enumerate(imgs):
        # resize
        img = cv.resize(img, (640, 480), interpolation=cv.INTER_LINEAR_EXACT)

        # find minutia

        # match minutia to each image

        # subsetting

        # estimate camera parameters

        # warping

        # timelapsing

        # crop

        # seam masking

        # exposure correction

        # blending



        cv.imshow(f'image-{i}', img)



    k = cv.waitKey(5) & 0xFF
    if k == 27:
        print("Stopping")
        # -- controller.setTarget(1,6000)
        break
