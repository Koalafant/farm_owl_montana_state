from helper import get_all_combos
import math
import cv2 as cv
import numpy as np


class FeatureMatcher:
    """https://docs.opencv.org/4.x/da/d87/classcv_1_1detail_1_1FeaturesMatcher.html"""

    def __init__(self, features):
        self.matcher = cv.detail_BestOf2NearestMatcher()
        self.matches = self.matcher.apply2(features)
        self.matcher.collectGarbage()

        # match matrix
        matrix_dimension = int(math.sqrt(len(self.matches)))
        rows = []
        for i in range(0, len(self.matches), matrix_dimension):
            rows.append(self.matches[i: i + matrix_dimension])
        self.match_matrix = np.array(rows)

        # confidence matrix (confidence from match matrix)
        self.confidence_matrix = np.array([[m.confidence for m in row] for row in self.match_matrix])

    def draw_matches_matrix(self, imgs, features, **kwargs):
        matches_matrix = self.match_matrix

        for idx1, idx2 in get_all_combos(len(imgs)):
            match = matches_matrix[idx1, idx2]

            if match.confidence < 1:
                continue

            kwargs["matchesMask"] = match.getInliers()
            kwargs.setdefault("flags", cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            yield idx1, idx2, cv.drawMatches(
                imgs[idx1],
                features[idx1].getKeypoints(),
                imgs[idx2],
                features[idx2].getKeypoints(),
                match.getMatches(),
                None,
                **kwargs
            )
