import cv2, numpy as np
import cv


class Test:
    morphology_modes = {
        "open": [cv.MORPH_OPEN, cv2.MORPH_OPEN],
        "close": [cv.MORPH_CLOSE, cv2.MORPH_CLOSE],
        "erode": [cv.MORPH_ERODE, cv2.MORPH_ERODE],
        "dilate": [cv.MORPH_DILATE, cv2.MORPH_DILATE],
    }

    threshold_modes = {
        "otsu": [cv.THRESH_OTSU, cv2.THRESH_OTSU],
        "bin": [cv.THRESH_BINARY, cv2.THRESH_BINARY],
    }

    cvt_color_modes = {
        "bgr2gray": [cv.COLOR_BGR2GRAY, cv2.COLOR_BGR2GRAY],
        "bgr2hsv": [cv.COLOR_BGR2HSV, cv2.COLOR_BGR2HSV],
    }

    def __init__(self, path):
        self._path = path
        self._image = cv2.imread(path)
        self._gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(self.gray_image, 127, 255, cv2.THRESH_OTSU)
        self._threshold_image = threshold_image

    @property
    def image(self):
        return self._image.copy()

    @property
    def gray_image(self):
        return self._gray_image.copy()

    @property
    def threshold_image(self):
        return self._threshold_image.copy()

    def morphology(self, mode="open"):
        selected_mode = self.morphology_modes[mode]
        kernel = np.ones((5, 5), np.uint8)
        self.my_morphology(selected_mode[0], kernel)
        self.cv2_morphology(selected_mode[1], kernel)

    def my_morphology(self, mode, kernel):
        image = cv.morphologyEx(self.threshold_image, mode, kernel)
        cv2.imwrite("my_test.jpg", image)

    def cv2_morphology(self, mode, kernel):
        image = cv2.morphologyEx(self.threshold_image, mode, kernel)
        cv2.imwrite("cv2_test.jpg", image)

    def findContours(self):
        self.my_findContours()
        self.cv2_findContours()

    def my_findContours(self):
        image = self.image
        contours, _ = cv.findContours(self.threshold_image)
        for i in range(len(contours)):
            contours[i] = np.array(contours[i], dtype="int32")
        cv2.drawContours(image, tuple(contours), -1, (0, 255, 0), 2)
        cv2.imwrite("my_test.jpg", image)

    def cv2_findContours(self):
        image = self.image
        contours, _ = cv2.findContours(
            self.threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        cv2.imwrite("cv2_test.jpg", image)

    def threshold(self, mode="otsu"):
        selected_mode = self.threshold_modes[mode]
        self.my_threshold(selected_mode[0])
        self.cv2_threshold(selected_mode[1])

    def my_threshold(self, mode):
        _, thresh = cv.threshold(self.gray_image, 127, 255, mode)
        cv2.imwrite("my_test.jpg", thresh)

    def cv2_threshold(self, mode):
        _, thresh = cv2.threshold(self.gray_image, 127, 255, mode)
        cv2.imwrite("cv2_test.jpg", thresh)

    def cvtColor(self, mode="gray"):
        selected_mode = self.cvt_color_modes[mode]
        self.my_cvtColor(selected_mode[0])
        self.cv2_cvtColor(selected_mode[1])

    def my_cvtColor(self, mode):
        image = cv.cvtColor(self.image, mode)
        cv2.imwrite("my_test.jpg", image)

    def cv2_cvtColor(self, mode):
        image = cv2.cvtColor(self.image, mode)
        cv2.imwrite("cv2_test.jpg", image)


def main():
    path = "test.jpg"
    test = Test(path)
    # test.cvtColor('bgr2hsv')
    # test.morphology('erode')
    # test.findContours()
    test.threshold()


if __name__ == "__main__":
    main()
