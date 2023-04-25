from megapix_scaler import MegapixScaler
from megapix_scaler import MegapixDownscaler
import cv2 as cv


class ImageHandler:

    def __init__(self, imgs):
        self.img_names = imgs
        self.scales_set = False
        self.img_sizes = []

        # scaler init (to actually scale an image proportionately
        self.medium_scaler = MegapixDownscaler(0.6)
        self.low_scaler = MegapixDownscaler(0.1)
        self.final_scaler = MegapixDownscaler(-1)

        # use above scalers to scale images down to respective sizes
        self.medium_imgs = list(self.read_and_resize_imgs(self.medium_scaler))
        self.low_imgs = list(self.read_and_resize_imgs(self.low_scaler))
        self.final_imgs = list(self.read_and_resize_imgs(self.final_scaler))

        # ratios (for cameras and croppers)
        self.medium_to_final_ratio = self.final_scaler.scale / self.medium_scaler.scale
        self.medium_to_low_ratio = self.low_scaler.scale / self.medium_scaler.scale
        self.final_to_low_ratio = self.low_scaler.scale / self.final_scaler.scale
        self.low_to_final_ratio = self.final_scaler.scale / self.low_scaler.scale

        # sizes (for warpers)
        self.final_img_sizes = [self.final_scaler.get_scaled_img_size(sz) for sz in self.img_sizes]
        self.low_img_sizes = [self.low_scaler.get_scaled_img_size(sz) for sz in self.img_sizes]
        # medium size is get_img_sizes() or img[x].shape

    def read_and_resize_imgs(self, scaler):
        for img, size in self.input_images():
            desired_size = scaler.get_scaled_img_size(size)
            yield cv.resize(img, desired_size, interpolation=cv.INTER_LINEAR_EXACT)

    def resize_imgs_by_scaler(self, imgs, scaler):
        for img, size in zip(imgs, self.img_sizes):
            yield self.resize_img_by_scaler(scaler, size, img)

    def input_images(self):
        self.img_sizes = []
        for name in self.img_names:
            img = self.read_image(name)
            size = self.get_image_size(img)
            self.img_sizes.append(size)
            self.set_scaler_scales()
            yield img, size

    @staticmethod
    def get_image_size(img):
        # width, height (everything in OpenCV is backwards)
        return img.shape[1], img.shape[0]

    @staticmethod
    def read_image(img_name):
        img = cv.imread(img_name)
        return img

    def set_scaler_scales(self):
        if not self.scales_set:
            first_img_size = self.img_sizes[0]
            self.medium_scaler.set_scale_by_img_size(first_img_size)
            self.low_scaler.set_scale_by_img_size(first_img_size)
            self.final_scaler.set_scale_by_img_size(first_img_size)
        self.scales_set = True
