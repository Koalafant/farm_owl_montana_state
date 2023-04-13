import math
import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import helper

'''Inspiration for this stitching algorithm taken from github.com/lukasalexanderweber'''


def all_combos(num):
    ii, jj = np.triu_indices(num, 1)
    for i, j in zip(ii, jj):
        yield i, j
def draw_matches(img_1, features_1, img_2, features_2, match):
    keypoint_1 = features_1.getKeypoints()
    keypoint_2 = features_2.getKeypoints()
    matches = match.getMatches()

    return cv.drawMatches(
        img_1, keypoint_1, img_2, keypoint_2, matches, None
    )


imgs = ['../../data/donkey_split_left.jpg', '../../data/donkey_split_mid.jpg', '../../data/donkey_split_right.jpg']
for i, x in enumerate(imgs):
    imgs[i] = cv.imread(x)

# resize
dim = imgs[0].shape

for i, img in enumerate(imgs):
    print(img.shape)
    imgs[i] = imgs[i][0 : dim[0], 0: dim[1]]
    #cv2.resize(image, (28, 28), interpolation=inter)
    imgs[i] = cv.resize(img, (0, 0), fx = 0.8, fy = 0.8)

# find minutia

orb = cv.ORB.create()

features = []
minutia = []
feature_imgs = []
for i, x in enumerate(imgs):
    features.append(cv.detail.computeImageFeatures2(orb, x))
    minutia.append(features[i].getKeypoints())
    feature_imgs.append(cv.drawKeypoints(x, minutia[i], None, color=(0, 0, 255)))

# match minutia to each image
matcher = cv.detail_AffineBestOf2NearestMatcher()

matches = matcher.apply2(features)

matrix_dim = int(math.sqrt(len(matches)))
rows = []
for i in range(0, len(matches), matrix_dim):
    rows.append(matches[i: i + matrix_dim])

match_matrix = np.array(rows)
match_confidence = [[m.confidence for m in row] for row in match_matrix]
match_confidence_matrix = np.array(match_confidence)

# print(match_confidence_matrix)


matched_imgs = {}

for idx_1, idx_2 in all_combos(len(imgs)):
    match = match_matrix[idx_1, idx_2]
    if match.confidence < 0.9:
        continue
    matched_imgs[f'Image {idx_1} to Image {idx_2}'] = draw_matches(imgs[idx_1], features[idx_1], imgs[idx_2],
                                                                   features[idx_2], match)

# subsetting

# estimate camera parameters

# warping

# timelapsing

# crop

# seam masking

# exposure correction

# blending


while True:
    for img in matched_imgs:
        cv.imshow(img, matched_imgs[img])
   # for img in imgs:
    #    cv.imshow(str(img), img)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        print("Stopping")
        break
