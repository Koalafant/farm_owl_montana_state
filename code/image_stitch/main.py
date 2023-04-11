import os
import cv2 as cv
import helper

'''Inspiration for this stitching algorithm taken from github.com/lukasalexanderweber'''

imgs = ['../../data/donkey_split_left.jpg', '../../data/dokey_split_mid.jpg','../../data/dokey_split_right.jpg']
for i, x in enumerate(imgs):
    imgs[i] = cv.imread(x)
while True:


    # resize
    for i, x in enumerate(imgs):
        imgs[i] = cv.resize(x, (640, 480), interpolation=cv.INTER_LINEAR_EXACT)

    # find minutia

    orb = cv.ORB.create()

    features = []
    minutia = []
    feature_imgs = []
    for i, x in enumerate(imgs):
        features.append(cv.detail.computeImageFeatures2(orb, x))
        minutia.append(features[i].getKeypoints())
        feature_imgs.append(cv.drawKeypoints(x, minutia[i], None, color=(0,0,255)))

    # match minutia to each image
    matcher = cv.detail_AffineBestOf2NearestMatcher()
    '''for i, x in enumerate(imgs):
        matches = matcher.apply2(features[i])
        match_matrix = matches.array_in_square_matrix(matches)
    confidence = [[m.confidence for m in row] for row in match_matrix]
    print(confidence)'''

    # subsetting

    # estimate camera parameters

    # warping

    # timelapsing

    # crop

    # seam masking

    # exposure correction

    # blending



    for i, img in enumerate(imgs):
        cv.imshow(f'image-{i}', feature_imgs[i])



    k = cv.waitKey(5) & 0xFF
    if k == 27:
        print("Stopping")
        # -- controller.setTarget(1,6000)
        break
