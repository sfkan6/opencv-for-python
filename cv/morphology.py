import numpy as np


MORPH_ERODE = 1
MORPH_DILATE = 2
MORPH_OPEN = 3
MORPH_CLOSE = 4


def morphologyEx(image, mode, kernel, iterations=1):
    morp = Morphology(image, kernel)

    if mode == MORPH_ERODE:
        return morp.erosion(iterations)
    elif mode == MORPH_DILATE:
        return morp.dilation(iterations)
    elif mode == MORPH_OPEN:
        return morp.morph_open(iterations)
    elif mode == MORPH_CLOSE:
        return morp.morph_close(iterations)


class Morphology:
    def __init__(self, image, kernel):
        image = np.array(image)
        image[image > 0] = 1
        self._image = image
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel.copy()

    @property
    def image(self):
        return self._image.copy()

    def morph_open(self, iterations=1):
        image = self._dilation_iter(self.image, iterations)
        image = self._erosion_iter(image, iterations)
        return image * 255

    def morph_close(self, iterations=1):
        image = self._erosion_iter(self.image, iterations)
        image = self._dilation_iter(image, iterations)
        return image * 255

    def dilation(self, iterations=1):
        return self._dilation_iter(self.image, iterations) * 255

    def erosion(self, iterations=1):
        return self._erosion_iter(self.image, iterations) * 255

    def _dilation_iter(self, image, iterations):
        for _ in range(iterations):
            image = self._dilation(image)
        return image

    def _erosion_iter(self, image, iterations):
        for _ in range(iterations):
            image = self._erosion(image)
        return image

    def _dilation(self, image):
        h, w = self.image.shape
        h_ker, w_ker = self.kernel.shape

        output = np.zeros_like(image)
        image_padded = np.zeros((h + h_ker - 1, w + w_ker - 1))
        image_padded[h_ker - 2 : -1 :, w_ker - 2 : -1 :] = image

        for x in range(w):
            for y in range(h):
                summation = (
                    self.kernel * image_padded[y : y + h_ker, x : x + w_ker]
                ).sum()
                output[y, x] = int(summation > 0)
        return output

    def _erosion(self, image):
        h, w = self.image.shape
        h_ker, w_ker = self.kernel.shape
        kernel_sum = self.kernel.sum()

        output = np.zeros_like(image)
        image_padded = np.zeros((h + h_ker - 1, w + w_ker - 1))
        image_padded[h_ker - 2 : -1 :, w_ker - 2 : -1 :] = image

        for x in range(w):
            for y in range(h):
                summation = (
                    self.kernel * image_padded[y : y + h_ker, x : x + w_ker]
                ).sum()
                output[y, x] = int(summation == kernel_sum)
        return output
