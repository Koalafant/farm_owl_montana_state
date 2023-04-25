import cv2 as cv
import numpy as np

class Camera:
    """https://docs.opencv.org/4.x/df/d15/classcv_1_1detail_1_1Estimator.html"""
    """https://docs.opencv.org/4.x/d5/d56/classcv_1_1detail_1_1BundleAdjusterBase.html"""
    """https://docs.opencv.org/4.x/d7/d74/group__stitching__rotation.html#ga8faf9588aebd5aeb6f8c649c82beb1fb"""

    def __init__(self, features, matches, **kwargs):
        self.estimator = cv.detail_HomographyBasedEstimator(**kwargs)
        self.adjuster = cv.detail_BundleAdjusterRay()
        self.wave_correct_kind = cv.detail.WAVE_CORRECT_HORIZ
        self.adjuster.setRefinementMask(np.ones((3, 3), np.uint8))
        self.adjuster.setConfThresh(1.0)

        self.cameras = self.estimate(features, matches)
        self.cameras = self.adjust(features, matches, self.cameras)
        self.cameras = self.correct(self.cameras)

    def estimate(self, features, pairwise_matches):
        b, cameras = self.estimator.apply(features, pairwise_matches, None)
        for cam in cameras:
            cam.R = cam.R.astype(np.float32)
        return cameras

    def adjust(self, features, pairwise_matches, estimated_cameras):
        b, cameras = self.adjuster.apply(features, pairwise_matches, estimated_cameras)
        return cameras

    def correct(self, cameras):
        rmats = [np.copy(cam.R) for cam in cameras]
        rmats = cv.detail.waveCorrect(rmats, self.wave_correct_kind)
        for idx, cam in enumerate(cameras):
            cam.R = rmats[idx]
        return cameras
