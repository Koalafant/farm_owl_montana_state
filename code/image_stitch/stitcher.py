from helper import plot_images, plot_image, draw_keypoints, subset_list, get_indices_to_keep, subset_matches
from image_handler import Image_Handler
from camera import Camera
import cv2 as cv
from blender import Blender
from feature_matcher import Feature_Matcher
from cropper import Cropper
from warper import Warper
from seam_finder import Seam_Finder


class Stitcher:

    @staticmethod
    def stitch(imgs):
        image_list = imgs

        img_handler = Image_Handler(image_list)
        medium_imgs = img_handler.medium_imgs
        low_imgs = img_handler.low_imgs
        final_imgs = img_handler.final_imgs
        plot_images(low_imgs, (20, 20))

        """https://docs.opencv.org/4.x/d0/d13/classcv_1_1Feature2D.html"""
        feature_detector = cv.ORB.create()
        features = [cv.detail.computeImageFeatures2(feature_detector, img) for img in medium_imgs]
        keypoints_center_img = draw_keypoints(medium_imgs[1], features[1])
        plot_image(keypoints_center_img, (15, 10))

        matcher = Feature_Matcher(features)
        matches = matcher.matches
        all_relevant_matches = matcher.draw_matches_matrix(medium_imgs, features, matchColor=(255, 0, 0))
        for idx1, idx2, img in all_relevant_matches:
            print(f"Matches Image {idx1 + 1} to Image {idx2 + 1}")
            plot_image(img, (20, 10))

        indices = get_indices_to_keep(features, matches)
        medium_imgs = subset_list(medium_imgs, indices)
        low_imgs = subset_list(low_imgs, indices)
        final_imgs = subset_list(final_imgs, indices)
        features = subset_list(features, indices)
        matches = subset_matches(features, matches, matcher.match_matrix)
        img_names = subset_list(img_handler.img_names, indices)
        img_sizes = subset_list(img_handler.img_sizes, indices)
        img_handler.img_names, img_handler.img_sizes = img_names, img_sizes

        print(img_handler.img_names)
        print(matcher.confidence_matrix)

        camera = Camera(features, matches)
        cameras = camera.cameras

        warper = Warper(cameras)

        low_sizes = img_handler.low_img_sizes
        camera_aspect = img_handler.medium_to_low_ratio  # since cameras were obtained on medium imgs

        warped_low_imgs = list(warper.warp_images(low_imgs, cameras, camera_aspect))
        warped_low_masks = list(warper.create_and_warp_masks(low_sizes, cameras, camera_aspect))
        low_corners, low_sizes = warper.warp_rois(low_sizes, cameras, camera_aspect)

        final_sizes = img_handler.final_img_sizes
        camera_aspect = img_handler.medium_to_final_ratio  # since cameras were obtained on medium imgs

        warped_final_imgs = list(warper.warp_images(final_imgs, cameras, camera_aspect))
        warped_final_masks = list(warper.create_and_warp_masks(final_sizes, cameras, camera_aspect))
        final_corners, final_sizes = warper.warp_rois(final_sizes, cameras, camera_aspect)

        plot_images(warped_low_imgs, (10, 10))
        plot_images(warped_low_masks, (10, 10))

        cropper = Cropper()

        mask = cropper.estimate_panorama_mask(warped_low_imgs, warped_low_masks, low_corners, low_sizes)
        plot_image(mask, (5, 5))

        lir = cropper.estimate_largest_interior_rectangle(mask)

        plot = lir.draw_on(mask, size=2)
        plot_image(plot, (5, 5))

        low_corners = cropper.get_zero_center_corners(low_corners)
        rectangles = cropper.get_rectangles(low_corners, low_sizes)

        plot = rectangles[1].draw_on(plot, (0, 255, 0), 2)  # The rectangle of the center img
        plot_image(plot, (5, 5))

        overlap = cropper.get_overlap(rectangles[1], lir)
        plot = overlap.draw_on(plot, (255, 0, 0), 2)
        plot_image(plot, (5, 5))

        intersection = cropper.get_intersection(rectangles[1], overlap)
        plot = intersection.draw_on(warped_low_masks[1], (255, 0, 0), 2)
        plot_image(plot, (2.5, 2.5))

        cropper.prepare(warped_low_imgs, warped_low_masks, low_corners, low_sizes)

        cropped_low_masks = list(cropper.crop_images(warped_low_masks))
        cropped_low_imgs = list(cropper.crop_images(warped_low_imgs))
        low_corners, low_sizes = cropper.crop_rois(low_corners, low_sizes)

        lir_aspect = img_handler.low_to_final_ratio  # since lir was obtained on low imgs
        cropped_final_masks = list(cropper.crop_images(warped_final_masks, lir_aspect))
        cropped_final_imgs = list(cropper.crop_images(warped_final_imgs, lir_aspect))
        final_corners, final_sizes = cropper.crop_rois(final_corners, final_sizes, lir_aspect)

        seam_finder = Seam_Finder()

        seam_masks = seam_finder.find(cropped_low_imgs, low_corners, cropped_low_masks)
        seam_masks = [seam_finder.resize(seam_mask, mask) for seam_mask, mask in zip(seam_masks, cropped_final_masks)]

        seam_masks_plots = [Seam_Finder.draw_seam_mask(img, seam_mask) for img, seam_mask in
                            zip(cropped_final_imgs, seam_masks)]
        plot_images(seam_masks_plots, (15, 10))

        panorama = Blender(cropped_final_imgs, seam_masks, final_corners, final_sizes).result

        plot_image(panorama, (20, 20))


imgs = ['../../data/donkey_split_left.jpg',
        '../../data/donkey_split_mid.jpg',
        '../../data/donkey_split_right.jpg']
Stitcher.stitch(imgs)
