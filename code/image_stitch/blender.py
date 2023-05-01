import cv2 as cv
import numpy as np


class Blender:

    def __init__(self, imgs, masks, corners, sizes):
        # init blender
        self.blender = cv.detail.Blender_createDefault(cv.detail.Blender_NO)

        # prepare step
        roi = cv.detail.resultRoi(corners=corners, sizes=sizes)
        self.blender.prepare(roi)

        # feed to blender
        for img, mask, corner in zip(imgs, masks, corners):
            self.blender.feed(cv.UMat(img.astype(np.int16)), mask, corner)
        # blend and result
        self.result, self.result_mask = None, None
        self.result, self.result_mask = self.blender.blend(self.result, self.result_mask)
        self.result = cv.convertScaleAbs(self.result)
