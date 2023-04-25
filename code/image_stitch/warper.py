from statistics import median
import cv2 as cv
import numpy as np

class Warper:
    """https://docs.opencv.org/4.x/da/db8/classcv_1_1detail_1_1RotationWarper.html"""

    def __init__(self, cameras):
        self.warper_type = 'spherical'
        focals = [cam.focal for cam in cameras]
        self.scale = median(focals)

    def warp_images(self, imgs, cameras, aspect=1):
        for img, camera in zip(imgs, cameras):
            warper = cv.PyRotationWarper(self.warper_type, self.scale * aspect)
            _, warped_image = warper.warp(
                img,
                Warper.get_K(camera, aspect),
                camera.R,
                cv.INTER_LINEAR,
                cv.BORDER_REFLECT,
            )
            yield warped_image

    def create_and_warp_masks(self, sizes, cameras, aspect=1):
        for size, camera in zip(sizes, cameras):
            warper = cv.PyRotationWarper(self.warper_type, self.scale * aspect)
            mask = 255 * np.ones((size[1], size[0]), np.uint8)
            _, warped_mask = warper.warp(
                mask,
                Warper.get_K(camera, aspect),
                camera.R,
                cv.INTER_NEAREST,
                cv.BORDER_CONSTANT,
            )
            yield warped_mask

    def warp_rois(self, sizes, cameras, aspect=1):
        roi_corners = []
        roi_sizes = []
        for size, camera in zip(sizes, cameras):
            warper = cv.PyRotationWarper(self.warper_type, self.scale * aspect)
            K = Warper.get_K(camera, aspect)
            roi =  warper.warpRoi(size, K, camera.R)
            roi_corners.append(roi[0:2])
            roi_sizes.append(roi[2:4])
        return roi_corners, roi_sizes

    @staticmethod
    def get_K(camera, aspect=1):
        K = camera.K().astype(np.float32)
        """ Modification of intrinsic parameters needed if cameras were
        obtained on different scale than the scale of the Images which should
        be warped """
        K[0, 0] *= aspect
        K[0, 2] *= aspect
        K[1, 1] *= aspect
        K[1, 2] *= aspect
        return K