from skimage import morphology
import cv2 as cv
import numpy as np


def deal_pic(src):
    img_src = cv.resize(src, (640, 640))
    ret, img_1 = cv.threshold(img_src[:, :, 1], 150, 255, cv.THRESH_BINARY)
    ret, img_2 = cv.threshold(img_src[:, :, 2], 150, 255, cv.THRESH_BINARY)
    img = cv.bitwise_and(img_1, img_2)
    track_img = np.where(img == 255)
    return img_src, track_img, img


def skeleton_demo(image):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary = image
    binary[binary == 255] = 1
    skeleton0 = morphology.skeletonize(binary)
    skeleton = skeleton0.astype(np.uint8) * 255
    cv.imshow("skeleton", skeleton)
    cv.waitKey(100)
    cv.destroyAllWindows()


def medial_axis_demo(image):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary = image
    binary[binary == 255] = 1
    skel, distance = morphology.medial_axis(binary, return_distance=True)
    dist_on_skel = distance * skel
    skel_img = dist_on_skel.astype(np.uint8) * 255
    contours, hireachy = cv.findContours(skel_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    cv.imshow("result", image)
    cv.waitKey(100)
    cv.destroyAllWindows()


def morph_find(image):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary = image
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    finished = False
    size = np.size(binary)
    skeleton = np.zeros(binary.shape, np.uint8)
    while (not finished):
        eroded = cv.erode(binary, kernel)
        temp = cv.dilate(eroded, kernel)
        temp = cv.subtract(binary, temp)
        skeleton = cv.bitwise_or(skeleton, temp)
        binary = eroded.copy()

        zeros = size - cv.countNonZero(binary)
        if zeros == size:
            finished = True

    contours, hireachy = cv.findContours(skeleton, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    cv.imshow("skeleton", image)
    cv.waitKey(100)
    cv.destroyAllWindows()


def thin_demo(image):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary = image
    thinned = cv.ximgproc.thinning(binary)
    contours, hireachy = cv.findContours(thinned, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    cv.imshow("thin", image)
    cv.waitKey(100)
    cv.destroyAllWindows()


cap = cv.VideoCapture("Webcam/2021-04-17-013257.webm")
count = -1
while cap.isOpened():
    count += 1
    ret, frame = cap.read()
    if frame is not None:
        img_src, track_img, img = deal_pic(frame)
        #skeleton_demo(img)
        #medial_axis_demo(img)
        #morph_find(img)
        thin_demo(img)
    else:
        exit(0)
