import cv2 as cv
import numpy as np
from helper import add_weighted_image, remove_invalid_line_pixels, colored_img_generator
from blender import Blender


class Seam_Finder:

    def __init__(self):
        self.finder = cv.detail_DpSeamFinder("COLOR")

    def find(self, imgs, corners, masks):
        imgs_float = [img.astype(np.float32) for img in imgs]
        return self.finder.find(imgs_float, corners, masks)

    @staticmethod
    def resize(seam_mask, mask):
        dilated_mask = cv.dilate(seam_mask, None)
        resized_seam_mask = cv.resize(
            dilated_mask, (mask.shape[1], mask.shape[0]), 0, 0, cv.INTER_LINEAR_EXACT
        )
        return cv.bitwise_and(resized_seam_mask, mask)

    @staticmethod
    def draw_seam_mask(img, seam_mask, color=(0, 0, 0)):
        seam_mask = cv.UMat.get(seam_mask)
        overlaid_img = np.copy(img)
        overlaid_img[seam_mask == 0] = color
        return overlaid_img

    @staticmethod
    def draw_seam_polygons(panorama, blended_seam_masks, alpha=0.5):
        return add_weighted_image(panorama, blended_seam_masks, alpha)

    @staticmethod
    def draw_seam_lines(panorama, blended_seam_masks, linesize=1, color=(0, 0, 255)):
        seam_lines = Seam_Finder.extract_seam_lines(blended_seam_masks, linesize)
        panorama_with_seam_lines = panorama.copy()
        panorama_with_seam_lines[seam_lines == 255] = color
        return panorama_with_seam_lines

    @staticmethod
    def extract_seam_lines(blended_seam_masks, linesize=1):
        seam_lines = cv.Canny(np.uint8(blended_seam_masks), 100, 200)
        seam_indices = (seam_lines == 255).nonzero()
        seam_lines = remove_invalid_line_pixels(
            seam_indices, seam_lines, blended_seam_masks
        )
        kernelsize = linesize + linesize - 1
        kernel = np.ones((kernelsize, kernelsize), np.uint8)
        return cv.dilate(seam_lines, kernel)

    @staticmethod
    def blend_seam_masks(seam_masks, corners, sizes):
        imgs = colored_img_generator(sizes)
        blended_seam_masks, _ = Blender(
            imgs, seam_masks, corners, sizes
        ).result
        return blended_seam_masks
