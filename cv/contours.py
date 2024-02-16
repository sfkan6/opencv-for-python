import numpy as np


def boundingRect(contour):
    contour = np.array(contour)
    x_min, y_min = np.min(contour, 0)
    x_max, y_max = np.max(contour, 0)
    return [x_min, y_min, x_max - x_min, y_max - y_min]


def contourArea(contour):
    area = 0
    for i in range(len(contour)):
        area += contour[i - 1][0] * contour[i][1] - contour[i - 1][1] * contour[i][0]
    return 0.5 * abs(area)
