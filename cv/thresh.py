import numpy as np


THRESH_OTSU = 0
THRESH_BINARY = 1


def threshold(image, thresh, maxval, flag):
    if flag == THRESH_OTSU:
        return threshold_otsu(image, maxval)
    elif flag == THRESH_BINARY:
        return threshold_binary(image, thresh, maxval)
    return image


def threshold_otsu(image, maxval=255):
    image = np.array(image)
    pixel_number = image.shape[0] * image.shape[1]
    mean_weight = 1.0 / pixel_number
    his, bins = np.histogram(image, np.arange(0, 257))
    final_thresh = -1
    final_value = -1
    intensity_arr = np.arange(256)
    for t in bins[1:-1]:
        pcb = max(np.sum(his[:t]), 1)
        pcf = max(np.sum(his[t:]), 1)
        Wb = pcb * mean_weight
        Wf = pcf * mean_weight

        mub = np.sum(intensity_arr[:t] * his[:t]) / float(pcb)
        muf = np.sum(intensity_arr[t:] * his[t:]) / float(pcf)

        value = Wb * Wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value

    return threshold_binary(image, final_thresh, maxval)


def threshold_binary(image, thresh, maxval):
    final_img = np.array(image).copy()
    final_img[image >= thresh] = maxval
    final_img[image < thresh] = 0
    return final_img
