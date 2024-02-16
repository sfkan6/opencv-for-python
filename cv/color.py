import numpy as np


COLOR_BGR2GRAY = 0
COLOR_BGR2HSV = 1
COLOR_HSV2BGR = 2
COLOR_HSV2GRAY = 2


def inMultiRangeHsv(image, ranges):
    return np.array(
        [[get_gray_by_hsv_ranges(bgr2hsv(bgr), ranges) for bgr in row] for row in image]
    )


def inMultiRange(image_hsv, ranges):
    return np.array(
        [[get_gray_by_hsv_ranges(hsv, ranges) for hsv in row] for row in image_hsv]
    )


def inRange(image_hsv, low_border, upper_border):
    return np.array(
        [
            [get_gray_by_hsv_range(hsv, low_border, upper_border) for hsv in row]
            for row in image_hsv
        ]
    )


def get_gray_by_hsv_ranges(hsv, hsv_ranges):
    return max([get_gray_by_hsv_range(hsv, *hsv_range) for hsv_range in hsv_ranges])


def get_gray_by_hsv_range(hsv, low_border, upper_border):
    c, n = 0, 3
    for i in range(n):
        c += low_border[i] <= hsv[i] <= upper_border[i]
    if c == n:
        return 255
    return 0


def cvtColor(image, mode):
    image = np.array(image)
    if mode == COLOR_BGR2GRAY:
        return np.array([[bgr2gray(bgr) for bgr in row] for row in image])
    elif mode == COLOR_BGR2HSV:
        return np.array([[bgr2hsv(bgr) for bgr in row] for row in image])
    elif mode == COLOR_HSV2BGR:
        return np.array([[hsv2bgr(bgr) for bgr in row] for row in image])
    elif mode == COLOR_HSV2GRAY:
        return np.array([[hsv2gray(bgr) for bgr in row] for row in image])

    return image


def hsv2gray(hsv):
    return bgr2gray(hsv2bgr(hsv))


def bgr2gray(bgr):
    r, g, b = bgr[::-1]
    return round(0.299 * r + 0.587 * g + 0.114 * b)


def bgr2hsv(bgr):
    print(bgr)
    b, g, r = bgr[::-1]
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d / high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6
    return [h * 360, s * 255, v]


def hsv2bgr(hsv):
    h, s, v = hsv
    h /= 360
    s /= 255
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i % 6)]
    return [b, g, r]
