import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import random
from itertools import chain


def plot_image(img, figsize_in_inches=(5, 5)):
    fig, ax = plt.subplots(figsize=figsize_in_inches)
    ax.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.show()


def plot_images(imgs, figsize_in_inches=(5, 5)):
    fig, axs = plt.subplots(1, len(imgs), figsize=figsize_in_inches)
    for col, img in enumerate(imgs):
        axs[col].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.show()


def get_all_combos(num_imgs):
    ii, jj = np.triu_indices(num_imgs, k=1)
    for i, j in zip(ii, jj):
        yield i, j


def draw_keypoints(img, features, **kwargs):
    kwargs.setdefault("color", (random.randint(0, 200), random.randint(100, 255), random.randint(50, 150)))
    keypoints = features.getKeypoints()
    return cv.drawKeypoints(img, keypoints, None, **kwargs)


def subset_list(list_to_subset, indices):
    return [list_to_subset[i] for i in indices]


def get_indices_to_keep(features, pairwise_matches):
    indices = cv.detail.leaveBiggestComponent(features, pairwise_matches, 1)
    return indices


def subset_matches(features, matches, match_matrix):
    indices = cv.detail.leaveBiggestComponent(features, matches, 1)
    matches_matrix = match_matrix
    matches_matrix_subset = matches_matrix[np.ix_(indices, indices)]
    matches_subset_list = list(chain.from_iterable(matches_matrix_subset.tolist()))
    return matches_subset_list

def colored_img_generator(
        sizes,
        colors=(
                (255, 000, 000),  # Blue
                (000, 000, 255),  # Red
                (000, 255, 000),  # Green
                (000, 255, 255),  # Yellow
                (255, 000, 255),  # Magenta
                (128, 128, 255),  # Pink
                (128, 128, 128),  # Gray
                (000, 000, 128),  # Brown
                (000, 128, 255), # Orange
        ),
):
    for idx, size in enumerate(sizes):
        if idx + 1 > len(colors):
            raise ValueError(
                "Not enough default colors! Pass additional "
                'colors to "colors" parameter'
            )
        yield create_img_by_size(size, colors[idx])


def create_img_by_size(size, color=(0, 0, 0)):
    width, height = size
    img = np.zeros((height, width, 3), np.uint8)
    img[:] = color
    return img


def add_weighted_image(img1, img2, alpha):
    return cv.addWeighted(img1, alpha, img2, (1.0 - alpha), 0.0)


def remove_invalid_line_pixels(indices, lines, mask):
    for x, y in zip(*indices):
        if is_edge(mask, x, y):
            lines[x, y] = 0
    return lines


def is_edge(img, x, y):
    return any([
        is_black(img, x, y),
        is_black(img, x + 1, y),
        is_black(img, x - 1, y),
        is_black(img, x, y + 1),
        is_black(img, x, y - 1),
    ])

def is_black(img, x, y):
    return np.all(img[x, y] == 0)
